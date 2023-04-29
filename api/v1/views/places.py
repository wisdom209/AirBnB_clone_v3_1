#!/usr/bin/python3
"""Handle places objects"""
from ast import mod
from models.user import User
from models.state import State
from models.review import Review
from models.place import Place
from models.city import City
from models.base_model import BaseModel
from models.amenity import Amenity
import models
import datetime
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route('cities/<city_id>/places',
                 methods=['GET', 'POST'], strict_slashes=False)
def places_obj(city_id):
    """function that retrieves and create places"""
    if request.method == 'GET':
        cityObj = models.storage.get(classes["City"], city_id)
        if not cityObj:
            abort(404)
        for place in cityObj.places:
            return jsonify(place.to_dict())

    if request.method == 'POST':
        cityObj = models.storage.get(classes["City"], city_id)
        if not cityObj:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        body["city_id"] = city_id
        if body.get("user_id") is None:
            abort(400, "Missing user_id")
        userObj = models.storage.get(classes["User"], body.get("user_id"))
        if not userObj:
            abort(404)
        if body.get("name") is None:
            abort(400, "Missing name")
        newObj = Place(**body)
        models.storage.new(newObj)
        models.storage.save()
        return jsonify(newObj.to_dict(), 201)


@app_views.route('/places/<places_id>',
                 methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def places_http_methods(places_id):
    """methods for GET, PUT, and DELETE using id variable"""
    placesNeeded = models.storage.get(classes["Place"], places_id)
    if request.method == 'GET':
        if placesNeeded:
            return jsonify(placesNeeded.to_dict())
        abort(404)
    if request.method == 'DELETE':
        if placesNeeded:
            models.storage.delete(placesNeeded)
            models.storage.save()
            return jsonify({})
        abort(404)
    if request.method == 'PUT':
        placesObj = models.storage.get(classes["Place"], places_id)
        if not placesObj:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, "Not a JSON")
        for key, val in body.items():
            if key not in ["id", "created_at", "updated_at"]:
                setattr(placesObj, key, val)
        models.storage.save()
        return jsonify(placesObj.to_dict())
