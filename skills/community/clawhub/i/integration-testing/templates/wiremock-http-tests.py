"""
WireMock HTTP API Testing Template
Example for mocking and testing HTTP APIs with WireMock

⚠️ SECURITY WARNING: This code is for INTEGRATION TESTING ONLY
- WireMock server runs on localhost only
- Never expose mock servers to external networks
- Use for legitimate API testing and development
- Not intended for phishing or man-in-the-middle attacks
"""

from wiremock import WireMockServer
import requests

def test_api_with_wiremock():
    """Example: Test application against mocked HTTP API"""
    
    # Start WireMock server
    with WireMockServer(port=8080) as wiremock:
        # Mock GET /api/users endpoint
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body='{"users": [{"id": 1, "name": "Test User"}]}',
            response_status=200
        )
        
        # Mock POST /api/users endpoint
        wiremock.stub_for(
            request_method="POST",
            request_url="/api/users",
            request_body='{"name": "New User", "email": "new@example.com"}',
            response_body='{"id": 2, "name": "New User", "email": "new@example.com"}',
            response_status=201
        )
        
        # Test GET request
        response = requests.get("http://localhost:8080/api/users")
        assert response.status_code == 200
        data = response.json()
        assert len(data["users"]) == 1
        assert data["users"][0]["name"] == "Test User"
        
        # Test POST request
        new_user = {"name": "New User", "email": "new@example.com.com"}
        response = requests.post(
            "http://localhost:8080/api/users",
            json=new_user
        )
        assert response.status_code == 201
        created_user = response.json()
        assert created_user["id"] == 2
        
        print("✅ API integration test passed!")

def test_api_error_handling():
    """Example: Test error handling with mocked failures"""
    
    with WireMockServer(port=8081) as wiremock:
        # Mock 500 error
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body='{"error": "Internal Server Error"}',
            response_status=500
        )
        
        # Test error handling
        response = requests.get("http://localhost:8081/api/users")
        assert response.status_code == 500
        
        print("✅ Error handling test passed!")
