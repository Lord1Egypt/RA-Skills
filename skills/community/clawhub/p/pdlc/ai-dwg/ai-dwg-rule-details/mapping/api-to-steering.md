<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: API Architecture → api-standards.md + api-versioning.md (conditional)

## Purpose

This mapping rule transforms the **API Architecture & Contracts** document (AP artifact) into one or two steering files:
1. `rules/api-standards.md` — ALWAYS generated (REST conventions, error format, pagination, etc.)
2. `rules/api-versioning.md` — CONDITIONAL (only if AP specifies multi-version strategy)

---

## MANDATORY: Stage Sub-Role — API Designer

During THIS activity, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design for developer experience — the API standards must make the "right thing" obvious and the "wrong thing" impossible
- Include realistic JSON examples — developers copy-paste from examples; generic placeholders waste time
- Ensure error format is consistent and sacred — it's referenced by error-handling.md and every consumer depends on stability
- Think about API evolution from day one — even if versioning is conditional, non-breaking change rules are always relevant
- Write values as specifics ("pageSize 20", "100 req/min") not abstractions ("reasonable page size")

### Anti-Patterns for This Activity
- Do NOT assume BFF from having a frontend — BFF section only if the extension is active
- Do NOT generate API versioning file unless the AP explicitly discusses multi-version lifecycle
- Do NOT leave filterable fields undocumented — API-FILT-06 requires knowing which fields are indexed (from Data Architecture)

### Quality Check
A good output from this activity sounds like:
- "API-ERR-01: ALL errors follow the standard structure: {error: {code, message, details[], traceId}}. No exceptions — consumers parse this shape."
- "API-PAG-03: Pagination MUST be applied to ALL list endpoints — no unbounded result sets. Default 20, max 100."

---

## Source (AP Artifact)

**Document:** API Architecture (typically `08_API_Architecture.md` or `design/api-architecture.md`)

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| API Style & Standards | REST conventions, URL patterns, HTTP methods | api-standards.md core |
| Request/Response Format | JSON structure, envelope pattern | api-standards.md format rules |
| Pagination Strategy | Cursor/offset, page size limits | api-standards.md pagination |
| Filtering & Sorting | Query parameter conventions | api-standards.md filtering |
| Error Response Format | Error schema, error codes | api-standards.md error format |
| Versioning Strategy | URL/header versioning, deprecation policy | api-versioning.md (conditional) |
| Authentication for API | OAuth, API keys, token usage | api-standards.md auth section |
| Rate Limiting | Global/per-tenant/per-user limits | api-standards.md rate limiting |
| Documentation Approach | OpenAPI/Swagger generation | api-standards.md documentation |
| Webhook/Event Patterns | Notification conventions | api-standards.md webhooks (if applicable) |

**Additional source (if BFF extension active):**
- BFF-specific endpoints and aggregation rules

---

## Target 1: api-standards.md (ALWAYS)

### Role

The complete API contract reference. Every endpoint, controller, and API response in the system must comply with these standards. This file answers: "How do we build APIs here?"

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: API Architecture | date: {generation-date} -->

# API Standards

## API Identity

**Style:** {from AP — e.g., REST (resource-oriented)}
**Format:** {from AP — e.g., JSON only}
**Base path:** {from AP — e.g., /api/v{version}}
**Documentation:** {from AP — e.g., OpenAPI 3.1, auto-generated from decorators}

---

## URL Conventions

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| API-URL-01 | Use kebab-case for URL paths: `/service-requests` not `/serviceRequests` |
| API-URL-02 | Resources are plural nouns: `/incidents`, `/users`, `/assets` |
| API-URL-03 | Nested resources for parent-child: `/tenants/{tenantId}/users/{userId}` |
| API-URL-04 | Maximum nesting depth: {from AP — e.g., 2 levels}. Beyond that, use query filters. |
| API-URL-05 | Actions on resources (non-CRUD): `POST /incidents/{id}/actions/escalate` |
| API-URL-06 | No verbs in URLs (except actions pattern above): ❌ `/getIncidents` ✅ `/incidents` |
| API-URL-07 | Query parameters use camelCase: `?pageSize=20&sortBy=createdAt` |
| API-URL-08 | Base path includes version: `/api/v1/incidents` |

<!-- end: AP-sourced -->

---

## HTTP Methods

<!-- begin: AP-sourced -->

| Method | Usage | Idempotent | Response Code (Success) |
|--------|-------|:----------:|:-----------------------:|
| GET | Retrieve resource(s) | Yes | 200 |
| POST | Create resource / trigger action | No | 201 (create) / 200 (action) |
| PUT | Full replace of resource | Yes | 200 |
| PATCH | Partial update of resource | No | 200 |
| DELETE | Remove resource | Yes | 204 (no body) |

**Rules:**
| Rule | Description |
|------|-------------|
| API-HTTP-01 | Use the correct method for the operation — no POST for retrieval, no GET for mutations |
| API-HTTP-02 | PUT replaces the ENTIRE resource — if you only change one field, use PATCH |
| API-HTTP-03 | DELETE is idempotent — deleting an already-deleted resource returns 204 (not 404) |
| API-HTTP-04 | POST for non-CRUD actions: `/resources/{id}/actions/{action-name}` |

<!-- end: AP-sourced -->

---

## Request Format

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| API-REQ-01 | Content-Type: `application/json` for all request bodies |
| API-REQ-02 | Request body field names: {from AP — e.g., camelCase} |
| API-REQ-03 | Required fields MUST be validated — return 400 with field-level errors if missing |
| API-REQ-04 | Date format: {from AP — e.g., ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)} |
| API-REQ-05 | ID format: {from AP — e.g., UUID v4} |
| API-REQ-06 | Bulk operations: max {n from AP — e.g., 100} items per request |

<!-- end: AP-sourced -->

---

## Response Format

<!-- begin: AP-sourced -->

### Envelope Pattern

{Include if AP specifies an envelope — otherwise use flat responses}

**Single resource:**
```json
{
  "data": {
    "id": "uuid",
    "type": "{resource-type}",
    "attributes": { ... }
  },
  "meta": {
    "timestamp": "ISO-8601"
  }
}
```

**OR Flat pattern (if AP specifies):**
```json
{
  "id": "uuid",
  "field1": "value",
  "field2": "value",
  "createdAt": "ISO-8601",
  "updatedAt": "ISO-8601"
}
```

**Rules:**
| Rule | Standard |
|------|----------|
| API-RES-01 | Response field names: {from AP — e.g., camelCase} |
| API-RES-02 | All responses include: {standard fields from AP — e.g., id, createdAt, updatedAt} |
| API-RES-03 | Null fields: {policy from AP — e.g., include with null value / omit entirely} |
| API-RES-04 | Timestamps: {format from AP — e.g., ISO 8601 UTC always} |
| API-RES-05 | IDs: {format from AP — e.g., UUID v4, never expose sequential DB IDs} |

<!-- end: AP-sourced -->

---

## Pagination

<!-- begin: AP-sourced -->

**Strategy:** {from AP — e.g., offset-based / cursor-based / keyset}

### {Strategy} Pagination

**Request parameters:**
```
GET /resources?page={n}&pageSize={n}&sortBy={field}&sortOrder={asc|desc}
```
OR (cursor-based):
```
GET /resources?cursor={opaque-token}&limit={n}
```

**Response format:**
```json
{
  "data": [...],
  "pagination": {
    "page": 1,
    "pageSize": 20,
    "totalItems": 150,
    "totalPages": 8,
    "hasNext": true,
    "hasPrevious": false
  }
}
```

**Rules:**
| Rule | Standard |
|------|----------|
| API-PAG-01 | Default page size: {from AP — e.g., 20} |
| API-PAG-02 | Maximum page size: {from AP — e.g., 100} |
| API-PAG-03 | Pagination MUST be applied to ALL list endpoints — no unbounded result sets |
| API-PAG-04 | Include total count in response: {from AP — e.g., always / only if requested via ?count=true} |
| API-PAG-05 | Sort default: {from AP — e.g., createdAt DESC} |

<!-- end: AP-sourced -->

---

## Filtering & Sorting

<!-- begin: AP-sourced -->

**Rules:**
| Rule | Standard |
|------|----------|
| API-FILT-01 | Filter via query parameters: `?status=open&priority=high` |
| API-FILT-02 | Multiple values for same field: {from AP — e.g., comma-separated: `?status=open,pending`} |
| API-FILT-03 | Date range filtering: {from AP — e.g., `?createdAfter=ISO&createdBefore=ISO`} |
| API-FILT-04 | Search (free-text): {from AP — e.g., `?q=search+term`} |
| API-FILT-05 | Sorting: `?sortBy={field}&sortOrder={asc|desc}` |
| API-FILT-06 | Only allow filtering/sorting on indexed fields — document which fields are filterable |

<!-- end: AP-sourced -->

---

## Error Response Format

<!-- begin: AP-sourced -->

**Standard error structure:**
```json
{
  "error": {
    "code": "{ERROR_CODE}",
    "message": "Human-readable description",
    "details": [
      {
        "field": "fieldName",
        "issue": "specific validation error"
      }
    ],
    "traceId": "{correlation-id}"
  }
}
```

**HTTP status code usage:**
| Code | When |
|:----:|------|
| 400 | Validation failure, malformed request |
| 401 | Not authenticated (no token / expired token) |
| 403 | Authenticated but not authorized for this action |
| 404 | Resource not found |
| 409 | Conflict (duplicate, state violation) |
| 422 | Business rule violation (valid request but can't process) |
| 429 | Rate limit exceeded |
| 500 | Unexpected server error (never expose details) |

**Rules:**
| Rule | Standard |
|------|----------|
| API-ERR-01 | ALL errors follow the standard error structure — no exceptions |
| API-ERR-02 | Error codes are uppercase snake_case constants: `VALIDATION_FAILED`, `NOT_FOUND`, `UNAUTHORIZED` |
| API-ERR-03 | 400 errors MUST include field-level details array |
| API-ERR-04 | 500 errors MUST NOT expose stack traces, SQL errors, or internal details |
| API-ERR-05 | Include traceId in every error response for debugging |
| API-ERR-06 | {From AP — any project-specific error conventions} |

<!-- end: AP-sourced -->

---

## Rate Limiting

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| API-RATE-01 | Rate limiting applied at: {from AP — e.g., API gateway level} |
| API-RATE-02 | Global limit: {from AP — e.g., 1000 req/min per tenant} |
| API-RATE-03 | Per-user limit: {from AP — e.g., 100 req/min} |
| API-RATE-04 | Auth endpoint limit: {from AP — e.g., 10 req/min (brute-force prevention)} |
| API-RATE-05 | Rate limit headers: include `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` |
| API-RATE-06 | Exceeded: return 429 with `Retry-After` header |

<!-- end: AP-sourced -->

---

## API Authentication

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| API-AUTH-01 | Authentication token passed via: {from AP — e.g., Authorization: Bearer {token}} |
| API-AUTH-02 | Public endpoints (no auth required): {list from AP — e.g., health check, login, password reset} |
| API-AUTH-03 | API key usage: {from AP — e.g., for service-to-service, passed via X-API-Key header} |
| API-AUTH-04 | All non-public endpoints require valid authentication — no anonymous access |

<!-- end: AP-sourced -->

---

## Documentation Requirements

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| API-DOC-01 | Every endpoint MUST have OpenAPI documentation: summary, parameters, request/response schemas, error codes |
| API-DOC-02 | Documentation approach: {from AP — e.g., code-first with decorators, auto-generated at build time} |
| API-DOC-03 | Documentation available at: {from AP — e.g., /api/docs (Swagger UI)} |
| API-DOC-04 | Schema examples MUST be realistic (not "string" placeholders) |

<!-- end: AP-sourced -->

---

## Webhooks / Event Notifications (If Applicable)

<!-- begin: AP-sourced -->

{Include ONLY if AP defines webhook/notification patterns}

| Rule | Standard |
|------|----------|
| API-HOOK-01 | Webhook payload format: {from AP — matches standard response format} |
| API-HOOK-02 | Webhook delivery: {from AP — e.g., at-least-once with retry (3 attempts, exponential backoff)} |
| API-HOOK-03 | Webhook signature: {from AP — e.g., HMAC-SHA256 in X-Signature header} |
| API-HOOK-04 | Idempotency: include event ID — consumers handle deduplication |

<!-- end: AP-sourced -->

---

## BFF Endpoints (If BFF Extension Active)

<!-- begin: AP-sourced -->

{Include ONLY if BFF Pattern extension was active in AI-ADLC}

| Rule | Standard |
|------|----------|
| API-BFF-01 | BFF endpoints serve a SPECIFIC client (web, mobile, etc.) — not generic |
| API-BFF-02 | BFF aggregates multiple backend calls into one response — client MUST NOT call backend directly |
| API-BFF-03 | BFF endpoint naming: `/bff/{client-type}/{resource}` |
| API-BFF-04 | BFF shapes data for the client — different clients may get different response structures for the same data |

<!-- end: AP-sourced -->
```

---

## Target 2: api-versioning.md (CONDITIONAL)

### Trigger Condition

Generate this file ONLY IF:
- AP's API Architecture explicitly defines a multi-version strategy
- OR AP mentions version deprecation lifecycle
- OR multiple API versions are planned (v1, v2)

**Skip IF:** AP says "single version" or doesn't mention versioning beyond the base path `/api/v1`.

### Role

Defines how API versions are managed, deprecated, and sunset. Only relevant for systems expecting to maintain multiple API versions simultaneously.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: API Architecture (versioning section) | date: {generation-date} -->

# API Versioning

## Versioning Strategy

**Method:** {from AP — e.g., URL path versioning (/api/v1/, /api/v2/)}
**Current version:** {from AP — e.g., v1}
**Planned versions:** {from AP — e.g., v2 when breaking changes needed}

## Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| VER-01 | Versioning method: {URL path | header | query param — from AP}. Use consistently. |
| VER-02 | Breaking change definition: {from AP — e.g., field removal, type change, behavior change, required field addition} |
| VER-03 | Non-breaking changes (allowed in current version): {from AP — e.g., adding optional fields, new endpoints, new enum values} |
| VER-04 | New version required when: {breaking change criteria from AP} |
| VER-05 | Maximum supported versions: {from AP — e.g., current + 1 previous} |

<!-- end: AP-sourced -->

## Deprecation Lifecycle

<!-- begin: AP-sourced -->

```
Active (current) → Deprecated (announced) → Sunset (removed)
     │                    │                       │
     │                    │ {n months notice}      │
     │                    │                       │
     ▼                    ▼                       ▼
  Full support      Maintenance only         Removed (410 Gone)
  New features      Security fixes only      No traffic accepted
```

| Phase | Duration | Rules |
|-------|----------|-------|
| Active | Until next version released | Full support, new features added |
| Deprecated | {from AP — e.g., 6 months} | Security fixes only; `Deprecation` header on responses |
| Sunset | After deprecation period | Return 410 Gone; redirect documentation to new version |

<!-- end: AP-sourced -->

## Migration Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| VER-06 | When creating a new version, document ALL changes in a migration guide |
| VER-07 | Deprecated endpoints return `Sunset` and `Deprecation` headers |
| VER-08 | Never break an active version — fix forward in new version |
| VER-09 | Consumer notification: {from AP — e.g., 3 months before deprecation, via email + changelog} |

<!-- end: AP-sourced -->
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| REST conventions (URL patterns, methods) | Convert to API-URL-NN and API-HTTP-NN rules | URL Conventions, HTTP Methods |
| JSON format (envelope, field casing) | Convert to API-REQ-NN and API-RES-NN rules | Request/Response Format |
| Pagination approach | Convert to API-PAG-NN rules with specific values | Pagination section |
| Error format schema | Copy schema + convert to API-ERR-NN rules | Error Response Format |
| Rate limiting numbers | Convert to API-RATE-NN rules with thresholds | Rate Limiting section |
| Versioning strategy | Convert to VER-NN rules | api-versioning.md (if conditional met) |
| Webhook patterns | Convert to API-HOOK-NN rules | Webhooks section |
| OpenAPI requirement | Convert to API-DOC-NN rules | Documentation section |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| API-URL-NN | URL patterns |
| API-HTTP-NN | HTTP method usage |
| API-REQ-NN | Request format |
| API-RES-NN | Response format |
| API-PAG-NN | Pagination |
| API-FILT-NN | Filtering & sorting |
| API-ERR-NN | Error handling |
| API-RATE-NN | Rate limiting |
| API-AUTH-NN | API authentication |
| API-DOC-NN | Documentation |
| API-HOOK-NN | Webhooks |
| API-BFF-NN | BFF pattern |
| VER-NN | Versioning (in separate file) |

---

## Key Rules for This Mapping

1. **Error format is sacred** — it's referenced by error-handling.md; must be consistent across both files
2. **Values are specific** — "pageSize 20" not "reasonable page size"; "100 req/min" not "rate limited"
3. **Include example JSON** — developers copy-paste from examples; make them realistic
4. **Conditional versioning file** — don't generate if AP just uses `/api/v1` without lifecycle discussion
5. **BFF section only if extension active** — don't assume BFF from having a frontend
6. **API-AUTH rules cross-reference security-rules.md** — authentication details live there; API standards cover the header/mechanism only
7. **Document filterable fields** — API-FILT-06 requires knowing which fields are indexed (from Data Architecture)

---

## Depth Adaptation

| Depth | api-standards.md | api-versioning.md |
|-------|-----------------|-------------------|
| **Minimal** | URL conventions + HTTP methods + error format + pagination (core rules only, ~15 rules) | Skip unless explicitly multi-version |
| **Standard** | Full structure as defined above (~35-45 rules) | Generate if trigger met (full structure) |
| **Comprehensive** | Full structure + example request/response for each pattern + anti-patterns per section + HATEOAS links (if AP mentions) | Full + migration guide template + consumer notification template |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Error format changed | api-standards.md + error-handling.md | Update both; flag consistency check |
| Pagination strategy changed (e.g., offset → cursor) | API-PAG rules rewritten | Update; flag as breaking for existing consumers |
| Rate limits changed | API-RATE rules updated | Update; signal AI-GCE if hooks enforce limits |
| New versioning strategy added | api-versioning.md now needed | Generate new conditional file |
| Versioning removed (back to single) | api-versioning.md no longer justified | Flag for removal (user confirms) |
| BFF extension activated after initial generation | BFF section needed | Add BFF section to api-standards.md |
| New webhook pattern added | API-HOOK rules added | Add to Webhooks section |
