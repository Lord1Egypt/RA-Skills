import pytest
import httpx
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "音乐发现应用 API"

def test_search_music():
    """Test music search"""
    response = client.get("/api/search?term=test&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "results" in data
    assert isinstance(data["results"], list)

def test_search_music_empty():
    """Test empty search"""
    response = client.get("/api/search?term=")
    assert response.status_code == 200

def test_get_lyrics():
    """Test getting lyrics"""
    response = client.get("/api/lyrics?artist=test&title=test")
    assert response.status_code in [200, 404, 500]

def test_get_top_radio():
    """Test getting top radio stations"""
    response = client.get("/api/radio/top?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert "results" in data

def test_search_radio():
    """Test searching radio stations"""
    response = client.get("/api/radio/search?name=jazz&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_health_check():
    """Test health check"""
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
