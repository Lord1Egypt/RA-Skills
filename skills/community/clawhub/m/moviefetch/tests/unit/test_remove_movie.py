import pytest
import responses
from scripts.remove_movie import find_movie_in_library, remove_from_queue, RADARR_URL

@responses.activate
def test_find_movie_in_library():
    responses.add(
        responses.GET,
        f"{RADARR_URL}/movie",
        json=[
            {"id": 1, "title": "The Matrix"},
            {"id": 2, "title": "The Matrix Reloaded"}
        ],
        status=200
    )
    
    # exact match
    movie = find_movie_in_library("The Matrix")
    assert movie is not None
    assert movie["id"] == 1
    
    # partial match lookup
    movie = find_movie_in_library("reloaded")
    assert movie is not None
    assert movie["id"] == 2
    
    # none
    movie = find_movie_in_library("Inception")
    assert movie is None

@responses.activate
def test_remove_from_queue():
    responses.add(
        responses.DELETE,
        f"{RADARR_URL}/movie/1",
        status=200
    )
    assert remove_from_queue(1, True) is True
    
    responses.add(
        responses.DELETE,
        f"{RADARR_URL}/movie/99",
        status=404
    )
    assert remove_from_queue(99, False) is False
