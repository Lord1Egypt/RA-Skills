---
name: json-to-api
description: >
  Use when (1) user provides JSON data and asks to design a REST API endpoint around it. 
  (2) user says "create an API for this", "design an endpoint", "write the OpenAPI spec for this JSON", 
  or "make this a web API". (3) user pastes a JSON payload and wants the corresponding request/response schema. 
license: MIT
metadata:
  version: "1.0"
  category: data
  author: wangjipeng
  sources:
    - https://github.com/MiniMax-AI/skills
---

# JSON to API

Use when (1) user provides JSON data and asks to design a REST API endpoint around it. (2) user says "create an API for this", "design an endpoint", "write the OpenAPI spec for this JSON", or "make this a web API". (3) user pastes a JSON payload and wants the corresponding request/response schema.

## Core Position

This skill solves the specific problem of: *raw JSON data needs a proper API contract — endpoints, HTTP methods, status codes, and schemas — not just a data dump.*

This skill IS NOT:
- A data transformation tool — it designs the interface, not the implementation
- A backend code generator — it produces specs, not runnable server code
- An API client — it designs the server-side contract

This skill IS activated ONLY when: JSON data + API design intent are both present.

## Modes

### `/json-to-api`

**Default mode.** Designs REST API endpoints from JSON data with full OpenAPI 3.0 spec.

When to use: User provides JSON and wants endpoint design, HTTP methods, and request/response schemas.

### `/json-to-api/expand`

Adds pagination, filtering, sorting, and embedded resource support to the base design.

When to use: The JSON represents a collection and user wants a production-grade API surface.

## Execution Steps

### Step 1 — Analyze the JSON Structure

1. Receive JSON (pasted, file, or path)
2. Detect data type:
   - **Single object**: likely a resource with GET (one), PUT/PATCH (update), DELETE
   - **Array of objects**: likely a collection with GET (list), POST (create)
   - **Nested object**: indicates sub-resources or embedded entities
   - **Flat key-value**: simple configuration or state object
3. Identify resource candidates:
   - Top-level keys become resource names
   - Nested objects become sub-resources
   - Arrays become collection endpoints
4. Infer data types for each field: string, number, boolean, null, array, object

### Step 2 — Design API Surface

Determine resources and endpoints:

| JSON Shape | HTTP Method | Endpoint |
|---|---|---|
| Single object | GET | `GET /{resource}/{id}` |
| Array of objects | GET (list), POST (create) | `GET /{resource}`, `POST /{resource}` |
| Nested resource | GET | `GET /{resource}/{id}/{sub-resource}` |
| Object with ID field | PUT, PATCH, DELETE | `PUT /{resource}/{id}` |

### Step 3 — Write OpenAPI 3.0 Schema

Generate the full OpenAPI spec:

```yaml
openapi: 3.0.0
info:
  title: Resource API
  version: 1.0.0
paths:
  /resources:
    get:
      summary: List all resources
      responses:
        '200':
          description: Success
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Resource'
```

For each schema field:
- Map JSON types to OpenAPI types
- Mark required fields (non-nullable, must be present)
- Add `example` values from the provided JSON

### Step 4 — Validate

- All JSON fields are represented in the schema
- HTTP methods are appropriate for the resource type
- Status codes are standard (200, 201, 400, 404, 500)
- No invented endpoints not implied by the JSON structure

## Mandatory Rules

### Do not

- Do not invent API endpoints not implied by the JSON structure
- Do not set arbitrary status codes (use standard REST conventions)
- Do not add authentication schemes not mentioned by the user
- Do not assume database schema — design the API surface only

### Do

- Use plural nouns for collection endpoints (`/users`, not `/user`)
- Map JSON field names to camelCase in the schema
- Include the provided JSON as an `example` in the schema
- Follow REST conventions: GET (no body), POST/PUT/PATCH (JSON body), DELETE (no body)

## Quality Bar

**A good output:**
- Every field in the JSON appears in the schema with correct type
- HTTP methods and endpoints match JSON structure
- OpenAPI spec is valid YAML and renderable in Swagger UI
- Examples in schema match the provided JSON values

**A bad output:**
- Missing fields from the original JSON
- Wrong HTTP method for the operation (GET with body)
- Non-standard status codes (201 for GET, 200 for DELETE)
- camelCase/snake_case inconsistency in field naming

## Good vs. Bad Examples

| Scenario | Bad Output | Good Output |
|---|---|---|
| Array of users | `GET /user` (singular) | `GET /users` (plural) |
| Nested address object | Flattened into user object | `GET /users/{id}/addresses` as sub-resource |
| Optional phone field | Marked as required | Marked optional with `nullable: true` |
| Created timestamp | Number type | String with `format: date-time` |

## References

- `references/` — OpenAPI 3.0 schema templates, HTTP method conventions, status code guide