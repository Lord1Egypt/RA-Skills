---
name: openapi-validator
description: Validate and improve OpenAPI/Swagger specifications — check for completeness, consistency, security definitions, and API design best practices.
metadata:
  tags: ["openapi", "swagger", "api", "validation", "documentation"]
---

# OpenAPI Validator

Validate and improve OpenAPI 3.x specifications for completeness, consistency, security definitions, and API design best practices. Checks endpoint coverage, schema quality, authentication setup, response consistency, and generates improvement recommendations.

## Usage

```
"Validate my OpenAPI spec"
"Check my Swagger file for issues"
"Improve my API specification"
"Audit API design for REST best practices"
```

## How It Works

### 1. Spec Discovery

```bash
# Find OpenAPI/Swagger files
find . -name "openapi.*" -o -name "swagger.*" -o -name "api-spec.*" | head -10
# Check spec version
python3 -c "
import yaml, json, sys
for f in ['openapi.yaml', 'openapi.json', 'swagger.yaml', 'swagger.json']:
    try:
        with open(f) as fh:
            d = yaml.safe_load(fh) if f.endswith('.yaml') else json.load(fh)
            print(f'{f}: {d.get(\"openapi\", d.get(\"swagger\", \"unknown\"))}')
    except: pass
"
```

### 2. Structural Validation

- Valid OpenAPI 3.x or Swagger 2.0 structure
- All \$ref references resolve correctly
- Required fields present (info, paths, components)
- Schema definitions are valid JSON Schema
- Enum values match their types
- Default values match field types

### 3. Completeness Audit

**Endpoint coverage:**
- All paths have descriptions
- All parameters documented (name, type, description, required)
- All response codes documented (200, 400, 401, 403, 404, 500)
- Request body schemas defined
- Response schemas defined
- Examples provided for complex schemas

**Schema quality:**
- All properties have descriptions
- String fields have format/pattern/minLength/maxLength
- Number fields have minimum/maximum
- Arrays have items definition and maxItems
- Required properties listed
- Nullable fields explicitly marked

### 4. API Design Review

**REST conventions:**
- Resource-oriented paths (`/users/{id}` not `/getUser`)
- Consistent naming (camelCase vs snake_case)
- Proper HTTP methods (GET for read, POST for create, etc.)
- Consistent pluralization (`/users` not `/user`)
- Proper use of path vs query parameters
- Pagination pattern consistent across endpoints

**Response consistency:**
- Consistent error response format
- Consistent envelope structure
- Consistent timestamp formats (ISO 8601)
- Consistent ID formats
- Proper use of HTTP status codes

### 5. Security Review

- Security schemes defined (OAuth2, API Key, Bearer)
- Security requirements applied to all endpoints
- Sensitive data not in URL parameters
- Rate limiting documented
- CORS configuration noted

### 6. Versioning

- API version in info.version follows semver
- Version in URL path or header documented
- Deprecation notices on legacy endpoints
- Sunset headers documented

## Output

```
## OpenAPI Specification Audit

**File:** openapi.yaml | **Version:** 3.1.0 | **API:** v2.1.0
**Endpoints:** 23 | **Schemas:** 15

### Completeness Score: 72/100

| Category | Score | Issues |
|----------|-------|--------|
| Paths | 85% | 3 missing descriptions |
| Parameters | 70% | 8 undocumented params |
| Responses | 65% | 12 missing error codes |
| Schemas | 80% | 5 incomplete schemas |
| Security | 60% | 4 unprotected endpoints |
| Examples | 40% | 14 missing examples |

### 🔴 Critical (2)
1. **4 endpoints without security** — POST /webhooks, GET /health,
   GET /api/internal/stats, DELETE /api/cache
   → Apply security scheme or explicitly mark as public

2. **Sensitive data in query param** — GET /api/users?api_key={key}
   → Move to Authorization header

### 🟡 Improvements (6)
3. No error response schema defined (each endpoint ad-hoc)
4. Inconsistent naming: `user_id` vs `userId` across endpoints
5. Missing pagination on GET /api/orders (returns unbounded list)
6. No rate limit documentation
7. 3 deprecated endpoints without sunset date
8. Missing Content-Type requirements on POST/PUT endpoints

### ✅ Good Practices
- Consistent use of semver in API version
- OAuth2 security scheme properly defined
- Request validation schemas thorough
- Proper use of components/schemas for reuse
```
