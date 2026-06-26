import pytest
import responses
from scripts.check_plex import get_library_key, search_plex, PLEX_URL

@responses.activate
def test_get_library_key():
    responses.add(
        responses.GET,
        f"{PLEX_URL}/library/sections",
        json={
            "MediaContainer": {
                "Directory": [
                    {"title": "TV Shows", "key": "2"},
                    {"title": "Movies", "key": "1"}
                ]
            }
        },
        status=200
    )
    
    key = get_library_key()
    assert key == "1"

@responses.activate
def test_search_plex():
    responses.add(
        responses.GET,
        f"{PLEX_URL}/library/sections/1/search",
        json={
            "MediaContainer": {
                "Metadata": [
                    {"title": "Inception", "year": 2010, "ratingKey": "123"}
                ]
            }
        },
        status=200
    )
    
    results = search_plex("Inception", "1")
    assert len(results) == 1
    assert results[0]["title"] == "Inception"
