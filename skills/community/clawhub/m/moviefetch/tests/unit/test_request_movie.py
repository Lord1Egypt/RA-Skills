import pytest
import responses
from scripts.request_movie import extract_extra_keywords, add_movie, RADARR_URL

def test_extract_extra_keywords():
    assert extract_extra_keywords("inception hindi", "Inception") == {"hindi"}
    assert extract_extra_keywords("the matrix reloaded 1080p", "The Matrix Reloaded") == {"1080p"}
    # testing stopwords and punctuation
    assert extract_extra_keywords("i want inception in hindi!!", "Inception") == {"hindi"}

@responses.activate
def test_add_movie_success():
    movie = {
        "title": "Inception",
        "year": 2010,
        "tmdbId": 27205,
        "titleSlug": "inception-27205",
        "images": []
    }
    responses.add(
        responses.POST,
        f"{RADARR_URL}/movie",
        json={"id": 12, "title": "Inception"},
        status=201
    )
    
    result = add_movie(movie, "Inception")
    assert result["status"] == "queued"
    assert result["title"] == "Inception"

@responses.activate
def test_add_movie_duplicate_no_extra_words():
    movie = {
        "title": "Inception",
        "year": 2010,
        "tmdbId": 27205,
        "titleSlug": "inception-27205",
        "images": []
    }
    responses.add(
        responses.POST,
        f"{RADARR_URL}/movie",
        body='[{"propertyName": "Title", "errorMessage": "This movie has already been added", "attemptedValue": "Inception"}]',
        status=400
    )
    
    result = add_movie(movie, "Inception")
    assert result["status"] == "duplicate"

@responses.activate
def test_add_movie_duplicate_with_extra_words():
    movie = {
        "title": "Inception",
        "year": 2010,
        "tmdbId": 27205,
        "titleSlug": "inception-27205",
        "images": []
    }
    
    # 1. Reject first post as already exists
    responses.add(
        responses.POST,
        f"{RADARR_URL}/movie",
        body='[{"propertyName": "Title", "errorMessage": "This movie has already been added", "attemptedValue": "Inception"}]',
        status=400
    )
    
    # 2. Mock getting local movie id
    responses.add(
        responses.GET,
        f"{RADARR_URL}/movie",
        match=[responses.matchers.query_param_matcher({"tmdbId": 27205})],
        json=[{"id": 42, "title": "Inception"}],
        status=200
    )
    
    # 3. Mock release search
    responses.add(
        responses.GET,
        f"{RADARR_URL}/release",
        match=[responses.matchers.query_param_matcher({"movieId": 42})],
        json=[
            {"title": "Inception.2010.1080p", "guid": "abc", "indexerId": 1, "seeders": 10},
            {"title": "Inception.Hindi.1080p", "guid": "def", "indexerId": 2, "seeders": 5, "rejected": False}
        ],
        status=200
    )
    
    # 4. Mock trigger specific download
    responses.add(
        responses.POST,
        f"{RADARR_URL}/release",
        json={},
        status=200
    )
    
    result = add_movie(movie, "Inception hindi")
    assert result["status"] == "queued_specific_version"
    assert "Inception.Hindi.1080p" in result["release_title"]
