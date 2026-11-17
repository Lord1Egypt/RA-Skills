<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# API Architecture & Contracts

## Stage: 10 of 13
## Phase: 🟢 DESIGN
## Execution: ALWAYS

---

## Purpose

Define how the system exposes its capabilities through APIs — the style, conventions, versioning, authentication, error handling, pagination, and documentation approach. The API is the system's public contract — internal consumers (UIs) and external consumers (integrations) depend on its stability and consistency.

**CTO Mindset:** "The API IS the product. If the API is well-designed, multiple UIs and integrations can be built against it without friction. If it's poorly designed, every consumer carries the cost."

---

## MANDATORY: Stage Sub-Role — API Designer

During THIS stage, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design contract-first — define the interface before the implementation; the API IS the product for consumers
- Define error semantics as carefully as the happy path — uniform error contract across all endpoints
- Version from day one — assume the API will change; bake versioning strategy in before the first call
- Separate internal APIs (richer, between your services) from external APIs (stable, documented, versioned)

### Anti-Patterns for This Stage
- Do NOT design endpoints as CRUD wrappers over database tables — model resources around business capabilities
- Do NOT skip pagination, idempotency, or rate-limiting design — these are architectural, not implementation details

### Quality Check
A good output at this stage sounds like:
- "12 resources across 3 contexts; error contract: {code, message, details[], traceId}; versioning: URL-based v1/v2; idempotency via header; pagination: cursor-based..."

---

## Depth Adaptation

| Depth | API Architecture Behavior |
|-------|--------------------------|
| **Minimal** | Define API style (REST/GraphQL). URL conventions. Error format. Auth method for API. Pagination approach. |
| **Standard** | Full API standards document. Versioning strategy with ADR. Rate limiting approach. Webhook patterns (if applicable). OpenAPI/Swagger documentation approach. |
| **Comprehensive** | Detailed API governance (naming conventions, field standards, envelope patterns). HATEOAS or hypermedia considerations. Advanced rate limiting (per-tenant, per-endpoint). API evolution strategy. SDK generation approach. Contract testing strategy. Multiple ADRs. |

---

## Step-by-Step Execution

### Step 1: Load Context

1. Container list (Stage 5) — which containers expose APIs
2. Technology stack (Stage 6) — framework capabilities, API documentation tools
3. Security architecture (Stage 8) — authentication methods, authorization model
4. Data architecture (Stage 9) — entities that become API resources
5. System Context (Stage 4) — external consumers of the API
6. Principles (Stage 3) — API-related principles (e.g., "API-First, UI-Second")
7. Multi-tenancy (Stage 7) — tenant context in API calls

---

### Step 2: Define API Style

```markdown
### Q-DSG-03: API Style

**Context:** The primary API style determines URL patterns, data format, tooling, and developer experience.

**Options:**
- (a) **REST (Resource-oriented)** — Standard HTTP methods on resources. Widely understood. OpenAPI/Swagger for docs.
- (b) **GraphQL** — Single endpoint; client specifies shape. Flexible queries. Steeper learning curve.
- (c) **gRPC** — Binary protocol; strongly typed; high performance. Best for service-to-service.
- (d) **Hybrid** — REST for external/public API + gRPC for internal service-to-service (if microservices).

**Recommended:** {option — usually (a) for most systems; (d) if microservices}
**Rationale:** {Reference team skills, consumer types, tooling ecosystem, principle alignment}

→ _ADR-{nnn} if non-obvious choice_

**Your Decision:** _[awaiting input]_
```

---

### Step 3: Define REST Conventions (if REST selected)

```markdown
## REST API Conventions

### URL Structure

| Pattern | Convention | Example |
|---------|-----------|---------|
| Base URL | `/{api-prefix}/{version}/{resource}` | `/api/v1/tickets` |
| Collection | `GET /{resources}` | `GET /api/v1/tickets` |
| Single resource | `GET /{resources}/{id}` | `GET /api/v1/tickets/abc-123` |
| Nested resource | `GET /{parent}/{id}/{child}` | `GET /api/v1/tickets/abc-123/comments` |
| Actions (non-CRUD) | `POST /{resources}/{id}/{action}` | `POST /api/v1/tickets/abc-123/assign` |
| Search/filter | `GET /{resources}?{filter_params}` | `GET /api/v1/tickets?status=open&priority=high` |

### Naming Rules

| Rule | Convention | Example |
|------|-----------|---------|
| Resource names | Plural nouns, lowercase, kebab-case | `/service-requests`, `/audit-logs` |
| Path parameters | Resource identifiers | `/tickets/{ticketId}` |
| Query parameters | camelCase | `?sortBy=createdAt&pageSize=20` |
| Request/response bodies | camelCase JSON keys | `{ "ticketId": "...", "createdAt": "..." }` |
| Boolean params | Positive naming | `?includeArchived=true` (not `?excludeActive`) |

### HTTP Methods

| Method | Semantics | Idempotent? | Response |
|--------|-----------|:-----------:|----------|
| GET | Read resource(s) | Yes | 200 + body |
| POST | Create resource / Trigger action | No | 201 + Location header / 200 for actions |
| PUT | Full replace of resource | Yes | 200 + updated body |
| PATCH | Partial update of resource | Yes (should be) | 200 + updated body |
| DELETE | Remove resource | Yes | 204 No Content |

### HTTP Status Codes

| Code | Usage |
|:----:|-------|
| 200 | Success (GET, PUT, PATCH, actions) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request — validation failure, malformed input |
| 401 | Unauthorized — authentication required or failed |
| 403 | Forbidden — authenticated but insufficient permissions |
| 404 | Not Found — resource doesn't exist (or not in this tenant) |
| 409 | Conflict — duplicate, version conflict, state conflict |
| 422 | Unprocessable Entity — semantically invalid (business rule violation) |
| 429 | Too Many Requests — rate limit exceeded |
| 500 | Internal Server Error — unhandled exception |
```

---

### Step 4: Define Request/Response Patterns

```markdown
## Request & Response Patterns

### Response Envelope

| Approach | Description | When to Use |
|----------|-------------|-------------|
| **(a) Flat** | Resource directly in body | Simple APIs; industry standard for REST |
| **(b) Envelope** | `{ "data": {...}, "meta": {...} }` | When metadata (pagination, timing) is needed |
| **(c) JSON:API** | Standardized envelope with relationships | When hypermedia/relationship-heavy |

**Chosen:** {Based on complexity needs}

### Successful Response Format

```json
// Single resource (envelope style)
{
  "data": {
    "id": "abc-123",
    "type": "ticket",
    "attributes": { ... }
  },
  "meta": {
    "requestId": "req-xyz",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}

// Collection
{
  "data": [ { ... }, { ... } ],
  "meta": {
    "total": 142,
    "page": 1,
    "pageSize": 20,
    "totalPages": 8
  }
}
```

### Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "Human-readable description of what went wrong",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Must be a valid email address"
      }
    ],
    "requestId": "req-xyz",
    "timestamp": "2026-01-15T10:30:00Z"
  }
}
```

**Error format rules:**
- Machine-readable `code` (constant, never changes — clients can switch on it)
- Human-readable `message` (can change — for debugging, not business logic)
- `details` array for field-level validation errors
- `requestId` for correlation with logs
- Never expose stack traces, internal paths, or system details
```

---

### Step 5: Define Pagination Strategy

```markdown
## Pagination

### Chosen Strategy: {Offset-based / Cursor-based / Keyset}

| Strategy | How It Works | Pros | Cons |
|----------|-------------|------|------|
| **Offset-based** | `?page=2&pageSize=20` | Simple; random page access | Performance degrades on large offsets; inconsistent if data changes |
| **Cursor-based** | `?after=cursor_token&limit=20` | Stable pagination; performant at any depth | No random page access; more complex client logic |
| **Keyset** | `?after_id=abc-123&limit=20` | Performant; simple | Requires stable sort key; no random page access |

### Pagination Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `meta.total` | integer | Total record count (optional — can be expensive) |
| `meta.page` | integer | Current page number (offset-based) |
| `meta.pageSize` | integer | Items per page (requested) |
| `meta.totalPages` | integer | Total pages (if total is provided) |
| `meta.hasNext` | boolean | Whether more results exist |
| `meta.cursor` | string | Cursor for next page (cursor-based) |

### Default Limits

| Parameter | Default | Maximum |
|-----------|:-------:|:-------:|
| pageSize / limit | {20} | {100} |
```

---

### Step 6: Define Filtering & Sorting

```markdown
## Filtering & Sorting

### Filtering Convention

| Style | Format | Example |
|-------|--------|---------|
| Query parameter per field | `?{field}={value}` | `?status=open&priority=high` |
| Operators | `?{field}[{op}]={value}` | `?createdAt[gte]=2026-01-01` |
| Search | `?q={search_term}` | `?q=email server down` |

### Supported Operators

| Operator | Meaning | Example |
|----------|---------|---------|
| (none) | Equals | `?status=open` |
| `[in]` | In list | `?status[in]=open,pending` |
| `[gt]`, `[gte]` | Greater than | `?priority[gte]=3` |
| `[lt]`, `[lte]` | Less than | `?createdAt[lt]=2026-06-01` |
| `[contains]` | Text contains | `?title[contains]=server` |

### Sorting Convention

| Parameter | Format | Example |
|-----------|--------|---------|
| `sortBy` | `{field}` or `{field}:asc\|desc` | `?sortBy=createdAt:desc` |
| Multiple sorts | Comma-separated | `?sortBy=priority:desc,createdAt:asc` |
| Default sort | Per-resource defined | Tickets: `createdAt:desc` |
```

---

### Step 7: Define Versioning Strategy

```markdown
## API Versioning

### Chosen Strategy: {URL path / Header / Query parameter}

| Strategy | Format | Pros | Cons |
|----------|--------|------|------|
| **URL path** | `/api/v1/tickets` | Visible; cacheable; simple routing | URL pollution; harder migrations |
| **Header** | `Accept: application/vnd.api+json; version=1` | Clean URLs | Less discoverable; harder testing |
| **Query parameter** | `/api/tickets?version=1` | Simple | Caching issues; non-standard |

**Chosen:** {Typically URL path for simplicity}

### Versioning Rules

| Rule | Description |
|------|-------------|
| Breaking change = new version | Field removal, type change, semantic change → v2 |
| Additive change = same version | New optional field, new endpoint → stays in v1 |
| Deprecation period | Old version supported for {n months} after new version ships |
| Maximum active versions | {2 — current + previous} |
| Version in docs | OpenAPI spec generated per version |
```

---

### Step 8: Define API Authentication & Rate Limiting

```markdown
## API Security

### Authentication per Consumer Type

| Consumer | Auth Method | Token/Credential |
|----------|:----------:|:----------------:|
| Web UI (browser SPA) | {Cookie / Bearer token} | {HttpOnly cookie / JWT in header} |
| External integrations | {API key / OAuth client credentials} | {Key in header / Bearer token} |
| Service-to-service (internal) | {Shared secret / mTLS / Service token} | {Header / certificate} |
| Webhooks (outbound) | {Signature verification} | {HMAC signature in header} |

### Rate Limiting

| Scope | Limit | Window | Response When Exceeded |
|-------|:-----:|:------:|:----------------------:|
| Per-tenant | {n} req | {window} | 429 + Retry-After header |
| Per-user | {n} req | {window} | 429 + Retry-After header |
| Per-endpoint (heavy) | {n} req | {window} | 429 + Retry-After header |
| Global (DDoS protection) | {n} req | {window} | 429 or 503 |

### Rate Limit Headers

| Header | Description |
|--------|-------------|
| `X-RateLimit-Limit` | Maximum requests allowed in window |
| `X-RateLimit-Remaining` | Requests remaining in current window |
| `X-RateLimit-Reset` | Timestamp when window resets |
| `Retry-After` | Seconds to wait (on 429 response) |
```

---

### Step 9: Define API Documentation Approach

```markdown
## API Documentation

| Aspect | Approach |
|--------|----------|
| Specification format | {OpenAPI 3.x / AsyncAPI for events} |
| Generation | {Auto-generated from code decorators / Hand-written / Hybrid} |
| Interactive docs | {Swagger UI / Redoc / Custom} |
| Hosted at | {`/api/docs` served by the API itself} |
| Versioned | {Per API version — separate spec per version} |
| Contract testing | {Generated client SDKs / Consumer-driven contract tests} |
```

---

### Step 10: Define Webhook / Event Notification Pattern (if applicable)

```markdown
## Webhooks & Event Notifications

### Outbound Webhooks (if system sends events to external consumers)

| Aspect | Design |
|--------|--------|
| Registration | {API endpoint to register webhook URLs per tenant} |
| Events available | {List of subscribable events — e.g., "ticket.created", "ticket.resolved"} |
| Payload format | {Same as API resource representation + event metadata} |
| Authentication | {HMAC signature in header for consumer verification} |
| Retry policy | {3 retries with exponential backoff; 5s, 30s, 5m} |
| Failure handling | {Disable after {n} consecutive failures; notify tenant admin} |

### Event Payload Structure

```json
{
  "event": "ticket.created",
  "timestamp": "2026-01-15T10:30:00Z",
  "tenantId": "tenant-abc",
  "data": {
    "id": "ticket-123",
    "type": "ticket",
    "attributes": { ... }
  },
  "signature": "sha256=..."
}
```
```

---

### Step 11: Produce ADR(s)

Possible API architecture ADRs:

| ADR | Decision |
|-----|----------|
| ADR-{nnn} | API style (REST vs. GraphQL vs. gRPC) |
| ADR-{nnn} | Versioning strategy (URL path vs. header) |
| ADR-{nnn} | Pagination approach (offset vs. cursor) |
| ADR-{nnn} | Response format (flat vs. envelope vs. JSON:API) |

---

### Step 12: Assemble Document

Compile **API Architecture** document:

1. API Style & Rationale
2. REST Conventions (URLs, methods, status codes)
3. Request/Response Patterns (envelope, errors)
4. Pagination Strategy
5. Filtering & Sorting
6. Versioning Strategy
7. Authentication & Rate Limiting
8. Documentation Approach
9. Webhooks / Event Notifications (if applicable)
10. ADR references

---

### Step 13: Present for Review

```markdown
## Review: API Architecture — {system_name}

I've designed the API architecture.

**Key decisions:**
- **Style:** {REST / GraphQL / gRPC / Hybrid}
- **Versioning:** {URL path / Header} — max {n} active versions
- **Pagination:** {Offset / Cursor / Keyset} — default page size: {n}
- **Auth:** {methods per consumer type}
- **Rate limiting:** {tenant: n/window, user: n/window}
- **Documentation:** {OpenAPI 3.x + Swagger UI}
- **Webhooks:** {Yes — n event types / No}

**Conventions established:**
- URL pattern: `{base_pattern}`
- Error format: structured with code + message + details
- Filtering: query parameter based with operators

**ADRs produced:** {n}

**Full document:** Saved to `{file_path}`

---

**Your response:**
- (a) **Approve** — API design is solid; proceed
- (b) **Adjust conventions** — Naming or patterns need changes
- (c) **Change style** — Different API style preferred
- (d) **Modify rate limits** — Limits need adjustment
- (e) **Add patterns** — Missing API concern (bulk operations, long-running tasks, etc.)
```

---

### Step 14: Log and Transition

1. Update state: Stage 10 = ✅ Done; Current Stage = 11
2. Update ADR register
3. Update Architecture Workbook

Display:

```
✅ Stage 10: API Architecture & Contracts — Complete

🔌 Style: {style} | Versioning: {strategy} | Pagination: {approach}
📄 Saved to: {file_path}

Next → Stage 11: Integration & Infrastructure

Proceeding...
```

---

## Output File

Save to:
- Numbered: `{output_root}/08_API_Architecture.md`
- Phase folders: `{output_root}/design/API_Architecture.md`

---

## API Architecture Quality Checks

| Check | Pass Criteria |
|-------|---------------|
| Consistency | All endpoints follow the same conventions (naming, methods, errors) |
| Completeness | CRUD + search + actions covered for all major resources |
| Security | Every endpoint has auth and rate limiting defined |
| Documentation | Auto-generated spec; interactive docs available |
| Versioning | Strategy defined; breaking change policy clear |
| Error handling | Consistent error format; no information leakage |
| Pagination | All collection endpoints paginated; limits enforced |
| Tenant-aware | Tenant scoping in all queries (if multi-tenant) |
| Consumer-friendly | External developer could integrate from docs alone |
| Principle-aligned | Follows "API-First" principle (if defined) |
