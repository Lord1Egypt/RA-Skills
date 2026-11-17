# API Interface Definition Template

Define every endpoint the feature requires. This becomes the contract between frontend and backend.

## Endpoint Template

For each API endpoint:

### [METHOD] /api/v1/[resource]/[action]

**Purpose**: One sentence describing what this endpoint does.

**Request**
```
Method: GET | POST | PUT | DELETE | PATCH
Content-Type: application/json
Authorization: Bearer {token}  (if applicable)
```

**Request Parameters**

| Field | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| userId | string | Yes | User unique ID | "usr_abc123" |
| page | int | No | Pagination page number, default 1 | 1 |
| pageSize | int | No | Items per page, default 20, max 100 | 20 |

**Request Body (for POST/PUT/PATCH)**
```json
{
  "field_name": "value",
  "optional_field": null
}
```

**Success Response (200)**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "pageSize": 20
  }
}
```

**Error Responses**

| HTTP Code | Business Code | Message | When |
|-----------|--------------|---------|------|
| 400 | 1001 | Invalid parameter: {field} is required | Missing required field |
| 401 | 2001 | Authentication required | No token or expired |
| 403 | 3001 | Permission denied | User lacks access |
| 404 | 4001 | Resource not found | ID doesn't exist |
| 500 | 9999 | Internal server error | Unexpected failure |

## Data Models

Define key data structures used across endpoints:

### Model: [Name]

| Field | Type | Required | Description | Constraints |
|-------|------|----------|-------------|-------------|
| id | string | Yes | Unique identifier | UUID format |
| name | string | Yes | Display name | 1-50 chars |
| status | enum | Yes | Current state | active / inactive / pending |
| createdAt | timestamp | Yes | Creation time | ISO 8601 |
| updatedAt | timestamp | Yes | Last update time | ISO 8601 |

## Business Rules

- Rule 1: [description]
- Rule 2: [description]

## Notes
- Performance: expected response time, cache strategy
- Rate limiting: if applicable
- Idempotency: for mutation endpoints
