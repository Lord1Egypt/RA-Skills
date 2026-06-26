---
name: 跨境卫士客户端
description: Use this skill when the user wants to call, test, debug, or integrate the 跨境卫士客户端 API defined by the bundled OpenAPI specification. Handles endpoint discovery, request construction, authentication, parameter validation, curl generation, and response interpretation for this API.
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins: ["curl", "python3"]
---

# 跨境卫士客户端

Use this skill when the task involves interacting with the 跨境卫士客户端 API, including:

- understanding available endpoints
- generating curl commands
- filling path, query, header, and body parameters
- handling authentication
- testing API requests
- debugging request and response failures
- translating user intent into concrete API calls

## Bundled references

Before making assumptions about endpoints, request bodies, or response schemas, read the bundled OpenAPI specification from one of the following files:

- `references/openapi.yaml`
- `references/openapi.json`

If present, also read:

- `references/auth.md`

Do not invent endpoints, fields, enum values, request formats, or response shapes that are not defined by the bundled specification or auth notes.

## Workflow

1. Read the OpenAPI spec and identify the correct path and HTTP method.
2. Determine:
   - base URL or server
   - authentication scheme
   - required headers
   - path parameters
   - query parameters
   - request body schema
   - expected response schema
3. Translate the user's goal into a concrete API call.
4. Prefer showing the exact curl command before or alongside execution when that improves transparency.
5. Use safe shell quoting when constructing commands.
6. Never expose secrets in full.
7. Summarize the result clearly, including the HTTP status code and important response fields.

## Authentication rules

- First inspect the OpenAPI spec for the declared security scheme.
- If `references/auth.md` exists, follow it as the source of truth for authentication details not fully expressed in the OpenAPI document.
- If credentials are already available in environment variables or local config, use them.
- Never print secret values in full.
- If a token or key must be shown for debugging, redact the middle portion.

Common environment variable patterns to check:

- `BASE_URL`
- `API_APP_ID`
- `API_APP_SECRET`
- `X_APP_ID`
- `X_APP_SECRET`
- `API_KEY`
- `ACCESS_TOKEN`
- `BEARER_TOKEN`

If the local auth notes define different names, follow those instead.

## Request construction rules

### Path parameters

Always substitute all required path parameters.

### Query parameters

Only include query parameters that are relevant or explicitly requested. Do not send null or empty values unless the API expects them.

### Request body

Build JSON request bodies that conform to the schema in the OpenAPI specification. If the schema has required fields, ensure they are present before sending the request.

### Headers

Always include:

- `Accept: application/json`

Include:

- `Content-Type: application/json`

when sending JSON request bodies.

If the API uses custom authentication headers such as `x-app-id` and `x-app-secret`, include them on every authenticated request.

## Execution pattern

Prefer this style for JSON requests:

```bash
curl -sS \
  -X POST "$BASE_URL/example/path" \
  -H "Accept: application/json" \
  -H "Content-Type: application/json" \
  --data '{...}'