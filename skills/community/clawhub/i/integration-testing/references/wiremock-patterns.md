# WireMock Patterns

Common patterns and best practices for using WireMock in API testing.

## What is WireMock?

WireMock is a tool for mocking HTTP services. It creates a standalone HTTP server that can simulate any API, allowing you to test applications in isolation from external dependencies.

## Key Benefits

- **API isolation**: Test without depending on real external APIs
- **Reproducible tests**: Consistent mock responses across test runs
- **Performance**: Faster than real API calls
- **Error simulation**: Test error handling and edge cases
- **Parallel testing**: Run multiple tests simultaneously

## Basic Setup

### Start WireMock Server

```python
from wiremock import WireMockServer

# Start with default port (8080)
with WireMockServer() as wiremock:
    # WireMock server is running at http://localhost:8080
    pass

# Start with custom port
with WireMockServer(port=9090) as wiremock:
    # WireMock server is running at http://localhost:9090
'    pass
```

## Core Patterns

### 1. Simple GET Response

```python
def test_simple_get():
    with WireMockServer(port=8080) as wiremock:
        # Stub GET /api/users
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body='{"users": [{"id": 1, "name": "John"}]}',
            response_status=200
        )
        
        # Test against mocked API
        response = requests.get("http://localhost:8080/api/users")
        assert response.status_code == 200
        assert len(response.json()["users"]) == 1
```

### 2. POST Request with Body Matching

```python
def test_post_with_body():
    with WireMockServer(port=8080) as wiremock:
        # Stub POST with exact body match
        wiremock.stub_for(
            request_method="POST",
            request_url="/api/users",
            request_body='{"name": "John", "email": "john@example.com"}',
            response_body='{"id": 1, "name": "John", "email": "john@example.com"}',
            response_status=201
        )
        
        # Test POST request
        user_data = {"name": "John", "email": "john@example.com"}
        response = requests.post(
            "http://localhost:8080/api/users",
            json=user_data
        )
        assert response.status_code == 201
        assert response.json()["id"] == 1
```

### 3. Path Parameters

```python
def test_path_parameters():
    with WireMockServer(port=8080) as wiremock:
        # Stub with path parameter
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users/123",
            response_body='{"id": 123, "name": "User 123"}',
            response_status=200
        )
        
        # Test with specific user ID
        response = requests.get("http://localhost:8080/api/users/123")
        assert response.status_code == 200
        assert response.json()["id"] == 123
```

### 4. Query Parameters

```python
def test_query_parameters():
    with WireMockServer(port=8080) as wiremock:
        # Stub with query parameter
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            request_query_params="active=true",
            response_body='{"users": [{"id": 1, "name": "Active User"}]}',
            response_status=200
        )
        
        # Test with query parameter
        response = requests.get("http://localhost:8080/api/users?active=true")
        assert response.status_code == 200
        assert len(response.json()["users"]) == 1
```

### 5. Headers

```python
def test_headers():
    with WireMockServer(port=8080) as wiremock:
        # Stub requiring specific header
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/protected",
            request_headers="Authorization: Bearer token123",
            response_body='{"message": "Authorized"}',
            response_status=200
        )
        
        # Test with authorization header
        headers = {"Authorization": "Bearer token123"}
        response = requests.get(
            "http://localhost:8080/api/protected",
            headers=headers
        )
        assert response.status_code == 200
```

## Advanced Patterns

### 6. JSON Response

```python
def test_json_response():
    with WireMockServer(port=8080) as wiremock:
        # Response with JSON content type
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/data",
            response_body='{"key": "value", "number": 123}',
            response_status=200,
            response_headers="Content-Type: application/json"
        )
        
        response = requests.get("http://localhost:8080/api/data")
        assert response.headers["Content-Type"] == "application/json"
        assert response.json()["key"] == "value"
```

### 7. Array Responses

```python
def test_array_response():
    with WireMockServer(port=8080) as wiremock:
        # Response with array
        users = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Jane"}
        ]
        
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body=json.dumps({"users": users}),
            response_status=200
        )
        
        response = requests.get("http://localhost:8080/api/users")
        users_data = response.json()["users"]
        assert len(users_data) == 2
```

### 8. Error Responses

```python
def test_error_responses():
    with WireMockServer(port=8080) as wiremock:
        # Stub 404 Not Found
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/notfound",
            response_body='{"error": "Resource not found"}',
            response_status=404
        )
        
        # Test 404 handling
        response = requests.get("http://localhost:8080/api/notfound")
        assert response.status_code == 404
        
        # Stub 500 Internal Server Error
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/error",
            response_body='{"error": "Internal server error"}',
            response_status=500
        )
        
        response = requests.get("http://localhost:8080/api/error")
        assert response.status_code == 500
```

### 9. Delayed Responses

```python
def test_delayed_responses():
    with WireMockServer(port=8080) as wiremock:
        # Stub with 2 second delay
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/slow",
            response_body='{"message": "Delayed response"}',
            response_status=200,
            fixed_delay_milliseconds=2000
        )
        
        # Test with timeout
        import time
        start = time.time()
        response = requests.get("http://localhost:8080/api/slow")
        elapsed = time.time() - start
        
        assert elapsed >= 2.0  # At least 2 second delay
        assert response.status_code == 200
```

### 10. Multiple Stubs

```python
def test_multiple_stubs():
    with WireMockServer(port=8080) as wiremock:
        # Stub 1: Get all users
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body='{"users": []}',
            response_status=200
        )
        
        # Stub 2: Get specific user
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users/1",
            response_body='{"id": 1, "name": "User 1"}',
            response_status=200
        )
        
        # Test both stubs
        response1 = requests.get("http://localhost:8080/api/users")
        assert response1.status_code == 200
        
        response2 = requests.get("http://localhost:8080/api/users/1")
        assert response2.status_code == 200
```

## Request Matching Patterns

### URL Pattern Matching

```python
def test_url_patterns():
    with WireMockServer(port=8080) as wiremock:
        # Match any path starting with /api/users/
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users/[0-9]+",  # Regex pattern
            response_body='{"user": "found"}',
            response_status=200
        )
        
        response = requests.get("http://localhost:8080/api/users/123")
        assert response.status_code == 200
```

### Body Pattern Matching

```python
def test_body_patterns():
    with WireMockServer(port=8080) as wiremock:
        # Match JSON body containing specific field
        wiremock.stub_for(
            request_method="POST",
            request_url="/api/users",
            request_body_pattern='{"name": ".+"}',  # Regex pattern
            response_body='{"created": true}',
            response_status=201
        )
        
        user_data = {"name": "John", "email": "john@example.com"}
        response = requests.post(
            "http://localhost:8080/api/users",
            json=user_data
        )
        assert response.status_code == 201
```

## Best Practices

### 1. Clean Up Between Tests

```python
def test_cleanup():
    with WireMockServer(port=8080) as wiremock:
        wiremock.reset_all()  # Clear all stubs
        
        # Add fresh stubs for this test
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/test",
            response_body='{"test": "data"}',
            response_status=200
        )
```

### 2. Use Descriptive Response Bodies

```python
def test_descriptive_responses():
    with WireMockServer(port=8080) as wiremock:
        # Include helpful error messages
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/error",
            response_body=json.dumps({
                "error": "Resource not found",
                "message": "The requested resource could not be found",
                "path": "/api/error",
                "timestamp": "2024-01-01T12:00:00Z"
            }),
            response_status=404
        )
```

### 3. Mock Realistic Responses

```python
def test_realistic_responses():
    with WireMockServer(port=8080) as wiremock:
        # Use realistic data structures
        wiremock.stub_for(
            request_method="GET",
            request_url="/api/users",
            response_body=json.dumps({
                "users": [
                    {
                        "id": 1,
                        "name": "John Doe",
                        "email": "john@example.com",
                        "created_at": "2024-01-01T10:00:00Z",
                        "updated_at": "2024-01-01T10:00:00Z"
                    }
                ],
                "pagination": {
                    "page": 1,
                    "per_page": 20,
                    "total": 1,
                    "total_pages": 1
                }
            }),
            response_status=200
        )
```

## Integration with Test Frameworks

### pytest

```python
import pytest
from wiremock import WireMockServer

@pytest.fixture(scope="session")
def wiremock_server():
    with WireMockServer(port=8080) as wiremock:
        yield wiremock

def test_api_integration(wiremock_server):
    # Setup stub
    wiremock_server.stub_for(
        request_method="GET",
        request_url="/api/test",
        response_body='{"test": "passed"}',
        response_status=200
    )
    
    # Test against mocked API
    response = requests.get("http://localhost:8080/api/test")
    assert response.json()["test"] == "passed"
```

## Troubleshooting

### Stubs Not Matching

1. Check exact URL matching
2. Verify HTTP method (GET, POST, etc.)
3. Check headers and body patterns
4. Use WireMock: Reset all between tests

### Port Already in Use

- Use different ports for parallel tests
- Check for existing processes on port
- Use context managers for automatic cleanup

### Performance Issues

- Use `reset_all()` instead of restarting server
- Minimize number of stubs
- Use URL patterns instead of multiple specific stubs

## Further Reading

- [Official WireMock Documentation](http://wiremock.org/docs/)
- [WireMock Python Wrapper](https://github.com/wiremock/python-wiremock)
- [API Mocking Best Practices](https://martinfowler.com/articles/mocksArentStubs.html)
