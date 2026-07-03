---
name: OpenAPI Spec Generator
slug: openapi-spec-generator
description: Auto-generate OpenAPI 3.x specs from code, traffic logs, or packet captures — with interactive refinement.
tags: [openapi, swagger, api, documentation, code-generation, har, developer-tools]
version: 1.0.0
license: MIT-0
---

# OpenAPI Spec Generator (OpenAPI 规范生成器)

Turn raw API surfaces into production-ready OpenAPI 3.x specifications. Ingest code repositories, HAR files, traffic logs, or packet captures — then interactively refine until you have a validated, shareable spec file.

## Core Capabilities

- **Multi-source ingestion**: Generate specs from Go/Java/Python/Node.js code, HAR captures, Charles Proxy logs, Wireshark PCAPs, or manual endpoint descriptions
- **Route discovery & clustering**: Scan framework-specific route definitions (Gin, Spring, FastAPI, Express) and cluster similar endpoints by path structure
- **Schema inference**: Infer request/response JSON schemas from code structs, sample payloads, or traffic observation — with type, required/optional, format, enum, and validation rules
- **Authentication extraction**: Detect and document auth patterns (Bearer JWT, API Key, OAuth2, Basic Auth) from code annotations, middleware, or captured headers
- **Interactive refinement**: Present draft spec → user confirms, corrects, or supplements → regenerate → validate — loop until production-ready
- **OpenAPI validation**: Run against official OpenAPI validator; flag schema errors, missing required fields, and best-practice violations
- **Mock server generation**: Optionally generate a Prism-compatible mock server configuration for immediate API simulation

## Workflow (8 Steps)

### Step 1: Select Input Source
**Input**: User chooses one or more sources:
- **Code repo path**: Local directory with API source code
- **HAR file**: Exported from Chrome DevTools Network tab
- **Traffic log**: Charles Proxy export, mitmproxy dump, or custom log format
- **PCAP file**: Wireshark/tcpdump capture
- **Manual description**: Natural language endpoint descriptions ("POST /users creates a user with name and email")

**Output**: Confirmed input source and format. If multiple, merge mode (union of endpoints).

### Step 2: Endpoint Discovery
**Input based on source type**:
- **Code**: Scan route registration patterns:
  - Go (Gin): `router.GET("/users/:id", ...)`
  - Java (Spring): `@GetMapping("/users/{id}")`
  - Python (FastAPI): `@app.get("/users/{id}")`
  - Node (Express): `app.get('/users/:id', ...)`
- **HAR/Logs**: Parse log entries, extract unique (method, path) pairs.
- **PCAP**: Reconstruct HTTP requests from TCP streams; deduplicate by (method, parsed-path).

**Action**: Cluster similar paths to identify path parameters:
```
GET /users/1
GET /users/2
GET /users/42
→ GET /users/{id}
```

**Output**: Endpoint list: method + path template + count/confidence.

### Step 3: Request/Response Schema Inference
**Input**: Endpoint list + source data.
**For Code source**: Extract request/response structs/classes:
- Go: parse struct tags (`json:"name" binding:"required"`)
- Java: parse `@RequestBody`, `@Valid`, DTO class fields with annotations
- Python: parse Pydantic models, type hints
- Node: parse Joi/Zod validation schemas, TypeScript interfaces

**For Traffic source**: Aggregate observed request bodies and response bodies per endpoint. Infer JSON Schema from samples:
- Detect field types (string, number, boolean, array, object)
- Detect required fields (present in all samples)
- Detect enums (limited set of observed values)
- Detect formats (date-time, email, uri, uuid patterns)
- Detect nullable fields (null observed in some samples)

**Output**: Per-endpoint: request schema + response schemas (by status code). Confidence score for each inferred field.

### Step 4: Parameter Classification
**Input**: Endpoint list + schemas.
**Action**: Classify parameters:
- **Path parameters**: `{id}`, `{userId}` — extracted from URL template
- **Query parameters**: `?page=1&limit=20` — from HAR query strings
- **Header parameters**: `Authorization`, `X-Request-ID`, `Content-Type`
- **Cookie parameters**: From captured cookie headers
- **Request body**: JSON body or form data

**Output**: Complete parameter list per endpoint with type, location, required flag, description (auto-generated or from code comments).

### Step 5: Authentication Detection
**Input**: Code annotations or captured headers.
**Action**: Detect auth patterns:
- **Bearer JWT**: `Authorization: Bearer eyJ...` header pattern
- **API Key**: `X-API-Key: ...` or `?api_key=...` patterns
- **OAuth2**: `Authorization: Bearer ...` + token refresh patterns in code
- **Basic Auth**: `Authorization: Basic ...` header
- **Cookie-based**: Session cookie pattern
- **No auth**: No auth header in any captured request

**Output**: Security scheme definition + applied endpoints.

### Step 6: OpenAPI Spec Generation
**Input**: All analyzed data.
**Action**: Generate OpenAPI 3.x YAML (default) or JSON:
```yaml
openapi: 3.0.3
info:
  title: {inferred from project name or user input}
  version: 1.0.0
servers:
  - url: {inferred from captured traffic or user input}
paths:
  /users/{id}:
    get:
      summary: Get user by ID
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Successful response
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
      required: [id, name]
```

**Output**: Draft OpenAPI spec file.

### Step 7: Interactive Refinement
**Input**: Draft spec + user feedback.
**Action**: Present spec summary:
- Total endpoints: 42
- Total schemas: 18
- Auth schemes: Bearer JWT
- Warnings: 3 endpoints missing response schema, 2 schemas with low confidence fields

User can:
- Override auto-detected titles, descriptions, server URLs
- Add descriptions and examples to specific endpoints
- Mark fields as required/optional that were misclassified
- Specify error response schemas (the generator may only see 200 responses in HAR)
- Add API-level metadata (contact, license, terms of service)
- Set tag groupings for endpoints

**Output**: Refined spec. Regenerate and validate after each round.

### Step 8: Validation & Export
**Input**: Refined OpenAPI spec.
**Action**:
1. Run OpenAPI structural validation (check required fields, schema references, path uniqueness)
2. Run best-practice checks: all endpoints have descriptions, all schemas have examples, no trailing slashes
3. Generate Swagger UI friendly HTML preview (optional)
4. Export to YAML or JSON file
5. Optionally generate Prism mock server config:
```yaml
# prism-config.yml
mock:
  dynamic: true
  cors: true
```

**Output**: Validated OpenAPI spec file + optional mock server config.

## Sample Prompts

### Prompt 1: From Code Repo
**User**: "从这个Go项目生成OpenAPI文档 [path: ~/projects/user-service/]"
**Expected Output**:
```
Discovered 12 endpoints across 3 route groups:
  GET    /health
  GET    /api/v1/users
  POST   /api/v1/users
  GET    /api/v1/users/{id}
  PUT    /api/v1/users/{id}
  DELETE /api/v1/users/{id}
  ...
Generated 5 schemas: User, CreateUserRequest, UpdateUserRequest, ErrorResponse, Pagination
Auth: Bearer JWT (detected from middleware)
Draft spec saved: openapi.yaml (12 endpoints, 5 schemas)
Warnings: 2 endpoints missing response description
```

### Prompt 2: From HAR File
**User**: "我从浏览器导出了HAR文件，帮我生成API文档 [upload: api-capture.har]"
**Expected Output**:
```
Parsed HAR: 287 requests across 3 domains
Deduplicated to 23 unique endpoints
Confidence: High (multiple samples per endpoint)
14 endpoints have ≥5 response samples (schema inference: high confidence)
9 endpoints have 1-4 samples (schema inference: medium confidence)
Draft spec: openapi.yaml (23 endpoints, 31 schemas)
⚠️ 5 endpoints only have 200 OK responses captured (error schemas may be incomplete)
```

### Prompt 3: From Manual Description
**User**: "帮我写一个用户管理API的OpenAPI文档：注册、登录、获取个人信息、更新个人信息、注销账号"
**Expected Output**: Full OpenAPI spec with 5 endpoints, User/AuthRequest/AuthResponse schemas, JWT auth scheme, and standard error responses. Interactive refinement offered.

### Prompt 4: From Traffic Log
**User**: "分析这个Charles抓包日志，生成API文档 [upload: charles-session.chls]"
**Expected Output**: Parse Charles Proxy session export → extract HTTP requests → deduplicate → infer schemas → generate spec. Note: binary/protobuf bodies flagged as "unparseable."

### Prompt 5: Validation & Improve Existing Spec
**User**: "帮我检查这个OpenAPI文件有没有问题，并补充缺失的描述 [upload: api-spec.yaml]"
**Expected Output**: Validation report: "3 missing response descriptions, 1 broken $ref, 2 schemas missing 'type' field. Fixed version: api-spec-v2.yaml."

### Prompt 6: Generate Mock Server
**User**: "基于刚生成的OpenAPI文档，生成一个Mock服务器配置"
**Expected Output**: Prism-compatible config + docker-compose snippet to start mock server. Instructions: "Run `docker-compose up` and mock API is live at http://localhost:4010."

## Real Task Examples

### Example 1: Legacy System Documentation
**Scenario**: Developer inherits a 5-year-old Go microservice with zero API documentation.
**Input**: "这个老项目没有任何API文档，帮我从代码生成 [path: ~/projects/legacy-order-service/]"
**Steps**:
1. Scan Go code: detect Gin routes, struct definitions, middleware.
2. Extract: 18 endpoints, 12 request/response structs, JWT auth + API key for webhooks.
3. Infer types from Go struct tags: `json:"order_id" binding:"required"` → required field.
4. Detect deprecated endpoints: comment `// DEPRECATED: use /v2/orders`.
5. Generate spec with deprecation warnings.
6. User review: adds business descriptions for 5 cryptic field names.
**Output**: Complete OpenAPI spec + "deprecated endpoints" migration guide.

### Example 2: Third-Party API Reverse Engineering
**Scenario**: Integrating with a partner API that has no documentation.
**Input**: "对接第三方API没有文档，只有这个HAR文件 [upload: partner-api.har]"
**Steps**:
1. Parse 412 requests from HAR.
2. Deduplicate → 34 unique endpoints.
3. Path parameter clustering: `/orders/1001`, `/orders/1002` → `/orders/{orderId}`.
4. Schema inference: 8 samples for CreateOrder → high confidence on required fields.
5. Auth detection: X-API-Key header + HMAC signature in custom header.
6. Warning: HMAC signing algorithm can't be inferred from traffic alone.
**Output**: Spec with 34 endpoints, schemas, auth scheme documented. Flagged: "HMAC signing algorithm unknown — check with partner."

### Example 3: API Standardization
**Scenario**: Team wants to enforce consistent API design across 3 microservices.
**Input**: "我们有3个服务的API，帮我生成统一的OpenAPI规范，检查不一致的地方"
**Steps**:
1. Generate specs for services A, B, C.
2. Cross-service analysis: detect naming inconsistencies (`user_id` vs `userId` vs `userID`).
3. Detect structural inconsistencies (A returns paginated, B returns arrays).
4. Detect missing standard endpoints (A has health check, B doesn't).
5. Generate unified spec with standardized naming + migration notes.
**Output**: Unified spec + inconsistency report + migration plan.

## 🚀 First-Success Path (3 Steps)

1. **Step 1**: Run `openapi-gen.sh scan ~/projects/user-service/` — discovers endpoints and detects framework
2. **Step 2**: Run `openapi-gen.sh infer ~/projects/user-service/` — reviews inferred request/response schemas
3. **Step 3**: Run `openapi-gen.sh generate ~/projects/user-service/ --output openapi.yaml` — generates validated OpenAPI 3.x spec

## Boundary Conditions

| Condition | Behavior |
|-----------|----------|
| Code repo has 0 routes detected | Flag: "No API routes found. Supported frameworks: Gin, Spring, FastAPI, Express. Check path or specify framework." |
| HAR file contains non-HTTP entries | Filter automatically; warn if filtered >50% of entries |
| PCAP contains encrypted HTTPS traffic | Warn: "Cannot decrypt HTTPS without session keys. Provide SSLKEYLOGFILE or use browser HAR export instead." |
| Binary protocols (gRPC, Thrift) | Flag as "protobuf detected — OpenAPI spec for gRPC requires .proto files" |
| >500 endpoints detected | Paginate output; generate spec in sections |
| Duplicate path+method combinations | Merge and warn of possible overloading |
| No response body samples for an endpoint | Flag as "schema unknown"; mark response as `{}` with warning |
| Code uses custom/non-standard routing | Fall back to AST-based function analysis; lower confidence |

## Error Handling

| Error Code | Scenario | Handling |
|-----------|----------|----------|
| E-NO-ROUTES | No API routes found in code | Request framework specification; offer manual entry mode |
| E-HAR-PARSE-FAIL | HAR file is corrupted or invalid JSON | Show parse error location; suggest re-export from browser |
| E-PCAP-DECRYPT | PCAP contains only encrypted traffic | Explain SSLKEYLOGFILE requirement; suggest HAR export |
| E-SCHEMA-CONFLICT | Conflicting schema inference (same field, different types) | Flag field; show evidence for each type; ask user to resolve |
| E-VALIDATION-FAIL | Generated spec fails OpenAPI validation | Show exact validation errors with line numbers; auto-fix common issues |
| E-OVERSIZED | Generated spec exceeds reasonable size (>10K lines) | Offer to split by tag into multiple spec files |
| E-UNSUPPORTED-FRAMEWORK | Codebase uses a framework without route scanner | Offer AST-based scan (lower confidence) or manual endpoint entry |

## Security Requirements

- **Local processing**: All code scanning, HAR parsing, and schema inference runs locally. No source code or traffic data sent to external services.
- **No secrets in spec**: Auto-redact API keys, tokens, passwords, and secrets found in traffic samples or code comments. Replace with `{{YOUR_API_KEY}}` placeholder.
- **Code privacy**: Scanned code is not stored or transmitted. Intermediate analysis data discarded after spec generation.
- **Traffic data sensitivity**: HAR files and PCAPs may contain authentication tokens and PII. Warn user. Process only the URL/schema metadata; strip request/response bodies from memory after schema inference.
- **Spec file safety**: Generated spec is a design document, not executable code. It contains no secrets by design.
- **Internal network data**: If HAR/PCAP contains internal hostnames/IPs, warn user before including in shareable spec.