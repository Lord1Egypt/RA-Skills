<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Component Design (Error Patterns) → error-handling.md

## Purpose

Transforms error handling patterns from Component Design (C4 L3 cross-cutting concerns) into a steering file governing how errors are created, propagated, logged, and returned to clients.

**Output:** `rules/error-handling.md` (ALWAYS generated)

---

## Source

**From:** Component Design — cross-cutting concerns section (error handling patterns)
**Also from:** API Architecture (error response format), Technology Stack (language-specific patterns)

---

## Target: error-handling.md

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design (cross-cutting) + API Architecture | date: {generation-date} -->

# Error Handling

## Error Strategy

**Pattern:** {from AP — e.g., Result pattern / Exception-based / Hybrid}
**API error format:** Defined in api-standards.md (API-ERR-01 through API-ERR-06)
**Logging:** All errors logged per observability-logging.md rules

---

## Error Classification

<!-- begin: AP-sourced -->

| Category | HTTP Status | Handling | Retry? |
|----------|:-----------:|---------|:------:|
| Validation errors | 400 | Return field-level details | No |
| Authentication errors | 401 | Return generic message | No |
| Authorization errors | 403 | Return generic "forbidden" | No |
| Not found | 404 | Return resource type + ID | No |
| Conflict / State violation | 409 | Return conflict description | Maybe (after state change) |
| Business rule violation | 422 | Return rule description + code | No |
| Rate limit | 429 | Return Retry-After header | Yes (after delay) |
| Internal / Unexpected | 500 | Log full context; return generic message | Yes (transient) |
| External service failure | 502/503 | Log + retry (if transient); circuit break (if persistent) | Yes (with backoff) |

<!-- end: AP-sourced -->

---

## Internal Error Pattern

<!-- begin: AP-sourced -->

{Pattern based on AP technology + component design approach}

### Result Pattern (If AP specifies)

```
// Pseudocode — adapt to specific language
Result<T, Error> {
  success: boolean
  data?: T
  error?: { code: string, message: string, details?: any }
}
```

**Rules:**
| Rule | Standard |
|------|----------|
| ERR-INT-01 | Service methods return Result<T, Error> — NEVER throw for expected business failures |
| ERR-INT-02 | Throw/raise ONLY for unexpected/unrecoverable errors (infrastructure failure, programming bugs) |
| ERR-INT-03 | Controllers convert Result errors → HTTP responses using error classification table |
| ERR-INT-04 | NEVER catch errors silently — always log or propagate |

### Exception-Based (If AP specifies)

**Rules:**
| Rule | Standard |
|------|----------|
| ERR-INT-01 | Define a domain exception hierarchy: BaseError → {DomainError, ValidationError, NotFoundError, ConflictError} |
| ERR-INT-02 | Domain exceptions carry: error code, message, details (optional), HTTP status mapping |
| ERR-INT-03 | Global exception filter catches all unhandled exceptions → maps to appropriate HTTP response |
| ERR-INT-04 | NEVER use generic Error/Exception — always use typed domain exceptions |

<!-- end: AP-sourced -->

---

## Error Propagation Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| ERR-PROP-01 | Errors bubble UP through layers: infrastructure → application → API — never sideways between modules |
| ERR-PROP-02 | Each layer may WRAP errors with context — never swallow them |
| ERR-PROP-03 | Cross-module errors: convert to the consuming module's error vocabulary (anti-corruption) |
| ERR-PROP-04 | External service errors: wrap in internal error type — never expose third-party error formats to callers |
| ERR-PROP-05 | Async errors (queues, events): log + move to dead letter — NEVER crash the consumer |

<!-- end: AP-sourced -->

---

## API Error Response Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| ERR-API-01 | ALL API errors use the standard format from api-standards.md — no custom formats per endpoint |
| ERR-API-02 | Error codes: uppercase SNAKE_CASE constants — registered in a central error code registry |
| ERR-API-03 | Messages: human-readable, non-technical, i18n-ready — no stack traces, SQL errors, or internal details |
| ERR-API-04 | Validation errors: include field-level details array with field name + specific issue |
| ERR-API-05 | 500 responses: generic "Internal Server Error" message — full details in logs ONLY (with traceId) |
| ERR-API-06 | Include `traceId` in every error response for support correlation |

<!-- end: AP-sourced -->

---

## Error Logging Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| ERR-LOG-01 | 4xx client errors: log at INFO (validation) or WARN (auth failure) — NOT ERROR |
| ERR-LOG-02 | 5xx server errors: ALWAYS log at ERROR with full context (stack, request, user, tenant) |
| ERR-LOG-03 | External service failures: log at ERROR with service name, endpoint, attempt count |
| ERR-LOG-04 | Include error code + classification in log for searchability |
| ERR-LOG-05 | Sensitive data rules from observability-sensitive.md apply to error logs too |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **NEVER** return stack traces in API responses (even in "development mode" headers)
2. **NEVER** catch-and-ignore — every catch block must log or re-throw
3. **NEVER** use error strings for control flow — use typed errors/results
4. **NEVER** expose database errors (constraint names, column names) to API consumers
5. **NEVER** return different error structures from different endpoints — one format everywhere
6. **NEVER** log errors at multiple levels (avoid: WARN in service + ERROR in controller for same error)
7. **NEVER** retry non-idempotent operations without explicit confirmation of safety
```

---

## Transformation Rules

| AP Content | Output |
|-----------|--------|
| Cross-cutting error pattern (Result/Exception) | ERR-INT rules |
| API error format (from API Architecture) | ERR-API rules (cross-reference) |
| Layer dependency rules | ERR-PROP rules |
| Logging requirements (from Observability) | ERR-LOG rules |

---

## Reconciliation

| Change | Action |
|--------|--------|
| Error pattern changed (Result → Exception) | Rewrite ERR-INT section |
| API error format changed | Update ERR-API; cross-check api-standards.md |
| New error category needed | Add to classification table |
