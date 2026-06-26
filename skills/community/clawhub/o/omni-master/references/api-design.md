# API Design & Testing

## REST API Design

### Principles
- Resources are nouns: `/users`, `/orders`, `/products`
- HTTP verbs: GET (read), POST (create), PUT (update), DELETE
- Consistent naming: kebab-case URLs, camelCase JSON
- Versioning: `/api/v1/resource`

### Response Codes
| Code | Meaning | When |
|---|---|---|
| 200 | OK | Successful GET/PUT |
| 201 | Created | Successful POST |
| 204 | No Content | Successful DELETE |
| 400 | Bad Request | Invalid input |
| 401 | Unauthorized | Missing auth |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 429 | Too Many Requests | Rate limited |
| 500 | Server Error | Unhandled exception |

### Response Format
```json
{
  "data": { ... },
  "meta": {
    "page": 1,
    "total": 100,
    "per_page": 20
  }
}
```

### Error Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Email is required",
    "details": [{ "field": "email", "issue": "required" }]
  }
}
```

## GraphQL
- Single endpoint, flexible queries
- Schema-first design
- Resolvers map to data sources
- Use fragments for reusable field sets

## Testing APIs
```bash
# curl testing
curl -X POST https://api.example.com/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Test", "email": "test@example.com"}'

# With auth
curl -H "Authorization: Bearer TOKEN" https://api.example.com/me
```

## API Documentation
- OpenAPI/Swagger for REST
- GraphQL introspection
- Example requests and responses
- Authentication guide
- Rate limit documentation

## Webhooks
- POST to registered URL on events
- Include signature for verification
- Retry with exponential backoff
- Idempotency keys for reliability

## Rate Limiting
- Token bucket or sliding window
- Return X-RateLimit-* headers
- 429 with Retry-After header
- Different limits per endpoint/tier

## Authentication
- API keys (simple, less secure)
- OAuth 2.0 (standard, flexible)
- JWT (stateless, scalable)
- HMAC signatures (webhook verification)
