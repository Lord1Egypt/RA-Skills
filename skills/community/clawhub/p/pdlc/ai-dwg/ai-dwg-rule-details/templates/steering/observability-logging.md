<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: observability-logging.md

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment (Observability) | date: {generation-date} -->

# Observability — Logging

## Logging Stack
**Format:** {Structured JSON}  |  **Transport:** {stdout → collector → storage}
**Storage:** {tool + retention}  |  **Correlation:** {request ID mechanism}

## Log Format
<!-- begin: AP-sourced -->
{JSON schema with: timestamp, level, service, module, requestId, tenantId, userId, message, data, error}

| Rule | Standard |
|------|----------|
| LOG-FMT-01 | Structured JSON — no plain text |
| LOG-FMT-02 | UTC ISO-8601 timestamps |
| LOG-FMT-03 | Request ID on every log |
| LOG-FMT-04 | Tenant ID when context exists |
| LOG-FMT-05 | Service + module identification |
<!-- end: AP-sourced -->

## Log Levels
<!-- begin: AP-sourced -->
| Level | When | NOT For |
|-------|------|---------|
| ERROR | Requires investigation | Expected failures (400s) |
| WARN | Unexpected but non-blocking | Single occurrence events |
| INFO | Significant business events | Internal steps |
| DEBUG | Diagnostic detail | Production default |

| Rule | Standard |
|------|----------|
| LOG-LVL-01 | Production default: {level} |
| LOG-LVL-02 | 4xx = INFO/WARN, never ERROR |
| LOG-LVL-03 | 5xx = ALWAYS ERROR |
<!-- end: AP-sourced -->

## Required Logging Points
<!-- begin: AP-sourced -->
| When | Level | Include |
|------|:-----:|---------|
| Request received | INFO | method, path, user, tenant |
| Request completed | INFO | method, path, status, duration |
| Auth success | INFO | user, tenant, method |
| Auth failure | WARN | attempted user, reason, IP |
| Entity CUD | INFO | type, id, actor |
| External call complete | INFO | service, status, duration |
| External call failure | ERROR | service, error, retry count |
| Background job | INFO | type, id, result |
| Unhandled exception | ERROR | error, stack (non-prod), context |
<!-- end: AP-sourced -->

## Metrics (Reference)
<!-- begin: AP-sourced -->
| Category | Key Metrics |
|----------|-------------|
| Request | count, duration p50/p95/p99, error_rate |
| Database | query_duration, pool_usage |
| Cache | hit_rate, miss_rate |
| Business | {domain-specific} |
<!-- end: AP-sourced -->

## Anti-Patterns
1. No console.log in production
2. No INFO inside loops
3. No full bodies at INFO
4. No custom log levels
5. No swallowed exceptions
```

## Filling: Refer to `mapping/infra-to-observability.md` (Target 1).
