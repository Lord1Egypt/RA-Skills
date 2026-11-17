<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: observability-tracing.md (CONDITIONAL)

**Generate IF:** Infrastructure specifies distributed tracing tool OR Microservices extension active.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment (Tracing) | date: {generation-date} -->

# Observability — Distributed Tracing

## Tracing Stack
**Protocol:** {OTLP/Jaeger/Zipkin}  |  **Collector:** {tool}  |  **UI:** {tool}  |  **Sampling:** {rate}

## Span Naming
<!-- begin: AP-sourced -->
| Span Type | Pattern | Example |
|-----------|---------|---------|
| HTTP server | `{METHOD} {route}` | `GET /api/v1/incidents/:id` |
| HTTP client | `{service}.{METHOD} {path}` | `notification.POST /send` |
| Database | `db.{op} {table}` | `db.select incidents` |
| Cache | `cache.{op} {key}` | `cache.get incident:{id}` |
| Queue publish | `queue.publish {name}` | `queue.publish events` |
| Queue consume | `queue.consume {name}` | `queue.consume events` |
| Internal | `{module}.{operation}` | `incident.escalate` |
<!-- end: AP-sourced -->

## Required Attributes
<!-- begin: AP-sourced -->
| Attribute | When | Value |
|-----------|------|-------|
| service.name | Always | Service identifier |
| tenant.id | When context exists | Tenant UUID |
| http.method | HTTP spans | Method |
| http.route | HTTP spans | Template (not actual URL) |
| http.status_code | HTTP spans | Status |
| db.system | DB spans | postgresql/redis/etc. |
| error | On failure | true |
<!-- end: AP-sourced -->

## Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| TRACE-01 | Auto-instrument: HTTP, DB, cache, queue |
| TRACE-02 | Manual spans for business operations |
| TRACE-03 | Propagation: {W3C TraceContext} across boundaries |
| TRACE-04 | Async: carry trace context in event metadata |
| TRACE-05 | Set ERROR status on business failures |
| TRACE-07 | No sensitive data in attributes |
| TRACE-08 | Sampling: 100% errors, {rate}% success |
| TRACE-09 | Include trace_id in log entries |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/infra-to-observability.md` (Target 3).
