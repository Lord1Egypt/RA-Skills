---
name: jpeng-api-tester
description: "API testing and monitoring skill. Test REST and GraphQL APIs, validate responses, and monitor uptime."
version: "1.0.0"
author: "jpeng"
tags: ["api", "testing", "rest", "graphql", "monitoring", "http"]
---

# API Tester

Test and monitor REST and GraphQL APIs with validation.

## When to Use

- User wants to test an API endpoint
- Validate API responses
- Monitor API uptime
- Run API test suites

## Features

- **REST APIs**: GET, POST, PUT, DELETE, PATCH
- **GraphQL**: Queries and mutations
- **Validation**: JSON Schema, assertions
- **Monitoring**: Uptime checks, alerts

## Usage

### Test REST endpoint

```bash
python3 scripts/api_test.py \
  --method GET \
  --url "https://api.example.com/users" \
  --expect-status 200
```

### POST with body

```bash
python3 scripts/api_test.py \
  --method POST \
  --url "https://api.example.com/users" \
  --header "Content-Type: application/json" \
  --body '{"name": "Alice"}' \
  --expect-status 201
```

### Validate response

```bash
python3 scripts/api_test.py \
  --method GET \
  --url "https://api.example.com/users/1" \
  --validate '{
    "type": "object",
    "required": ["id", "name"],
    "properties": {
      "id": {"type": "integer"},
      "name": {"type": "string"}
    }
  }'
```

### Test GraphQL

```bash
python3 scripts/api_test.py \
  --graphql \
  --url "https://api.example.com/graphql" \
  --query '{ users { id name } }'
```

### Run test suite

```bash
python3 scripts/api_test.py \
  --suite ./tests/api_tests.yaml
```

### Monitor uptime

```bash
python3 scripts/api_test.py \
  --monitor \
  --url "https://api.example.com/health" \
  --interval 60
```

## Output

```json
{
  "success": true,
  "status_code": 200,
  "response_time_ms": 145,
  "response": {"id": 1, "name": "Alice"},
  "validation_passed": true
}
```
