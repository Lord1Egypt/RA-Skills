<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Error Handling & Resilience Steering Templates

> **Purpose:** Used by the project-init-agent to generate error handling and resilience steering files
> in the target project's `rules/` folder. These templates encode error response patterns,
> result types, exception strategy, and resilience pipelines derived from `error-handling.md`
> and (if present) `resilience-standards.md`.

---

## error-handling.md (Always)

**Generates**: `rules/error-handling.md`
**Derived From**: error-handling.md + api-standards.md + tech-stack.md

```markdown
---
inclusion: always
---

# Error Handling Standards

## Result Pattern
- ALL domain methods that can fail MUST return {result_type} (never throw for business errors)
- ALL command handlers MUST return {result_type}
- ALL query handlers that might not find data MUST return {result_type} (not null)
- NEVER use exceptions for expected business failures

## Exception Usage
- Exceptions are ONLY for unexpected/infrastructure failures ({exception_examples})
- ALL exceptions MUST be caught by the global exception handler
- NEVER catch generic exceptions without logging them
- NEVER swallow exceptions (catch and do nothing)

## API Error Responses
- ALL error responses MUST use {error_format} format
- ALL validation errors MUST return 400 with field-level error details
- ALL business rule violations MUST return 422 with error code and message
- ALL not-found errors MUST return 404
- ALL concurrency conflicts MUST return 409
- NEVER expose internal error details ({prohibited_error_details}) in API responses
- ALL error responses MUST include a {correlation_id_field} for correlation

## Error Codes
- Format: {error_code_format} (e.g., {error_code_examples})
- MUST be unique across the system
- MUST be documented in the module's error catalog
```

---

## resilience-standards.md (Conditional — IF distributed system or >3 integrations)

**Generates**: `rules/resilience-standards.md`
**Condition**: Generated IF `resilience-standards.md` exists in workspace OR architecture has external integrations
**Derived From**: resilience-standards.md + integration architecture

```markdown
---
inclusion: always
---

# Resilience Standards

## External Calls
- ALL external HTTP calls MUST use a resilience pipeline ({resilience_components})
- ALL database operations MUST use the database resilience pipeline (retry on transient)
- ALL resilience events ({resilience_event_types}) MUST be logged with structured logging
- NEVER retry on 4xx responses (client errors are not transient)
- ALL circuit breakers MUST have monitoring/alerting when they open
- ALL fallback strategies MUST log that fallback was used (for monitoring)

## Isolation
- {isolation_strategy} for {isolated_operation_types}
- {bulkhead_pattern_description}

## Timeouts
- {timeout_lookup}s for lookups
- {timeout_write}s for writes
- {timeout_complex}s for complex operations
- {timeout_batch}s for batch/report operations

## Retry Policy
- Max retries: {max_retries}
- Backoff strategy: {backoff_strategy}
- Jitter: {jitter_strategy}
- Non-retryable: {non_retryable_conditions}
```
