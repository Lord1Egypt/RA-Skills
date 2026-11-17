<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: error-handling.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Component Design + API Architecture | date: {generation-date} -->

# Error Handling

## Error Strategy
**Pattern:** {Result pattern / Exception-based / Hybrid}

## Error Classification
<!-- begin: AP-sourced -->
| Category | HTTP | Handling | Retry? |
|----------|:----:|---------|:------:|
| Validation | 400 | Field-level details | No |
| Auth | 401 | Generic message | No |
| Forbidden | 403 | Generic | No |
| Not found | 404 | Resource + ID | No |
| Conflict | 409 | Description | Maybe |
| Business rule | 422 | Rule + code | No |
| Rate limit | 429 | Retry-After | Yes |
| Internal | 500 | Generic; log full | Yes |
| External failure | 502/503 | Retry + circuit break | Yes |
<!-- end: AP-sourced -->

## Internal Error Pattern
<!-- begin: AP-sourced -->
{Result pattern OR Exception hierarchy — per AP choice}
| Rule | Standard |
|------|----------|
| ERR-INT-01 | {pattern rule} |
| ... | ... |
<!-- end: AP-sourced -->

## Error Propagation
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| ERR-PROP-01 | Errors bubble UP through layers |
| ERR-PROP-02 | Each layer may WRAP with context |
| ERR-PROP-03 | Cross-module: convert to consumer's vocabulary |
| ERR-PROP-04 | External errors: wrap in internal type |
| ERR-PROP-05 | Async errors: log + dead letter |
<!-- end: AP-sourced -->

## API Error Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| ERR-API-01 | Standard format from api-standards.md |
| ERR-API-02 | Error codes: UPPER_SNAKE_CASE |
| ERR-API-03 | No stack traces in responses |
| ERR-API-04 | Validation: field-level details |
| ERR-API-05 | Include traceId |
<!-- end: AP-sourced -->

## Error Logging
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| ERR-LOG-01 | 4xx = INFO/WARN (not ERROR) |
| ERR-LOG-02 | 5xx = ALWAYS ERROR |
| ERR-LOG-03 | External failures = ERROR |
<!-- end: AP-sourced -->

## Anti-Patterns
1. NEVER return stack traces in responses
2. NEVER catch-and-ignore
3. NEVER use errors for control flow
4. NEVER expose DB errors to clients
5. NEVER return different error structures per endpoint
```

## Filling: Refer to `mapping/components-to-error-handling.md`.
