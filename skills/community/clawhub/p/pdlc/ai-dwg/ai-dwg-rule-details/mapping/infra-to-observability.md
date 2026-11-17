<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Infrastructure (Observability Section) → observability-logging.md + observability-sensitive.md + observability-tracing.md (conditional)

## Purpose

This mapping rule transforms the **observability section** of the Infrastructure & Deployment document into two or three steering files:
1. `rules/observability-logging.md` — ALWAYS generated (log levels, format, required logging points)
2. `rules/observability-sensitive.md` — ALWAYS generated (what NEVER to log, masking rules)
3. `rules/observability-tracing.md` — CONDITIONAL (only if distributed tracing tool specified or Microservices extension active)

---

## MANDATORY: Stage Sub-Role — Automation Engineer

During THIS activity, ALSO adopt the mindset of an **Automation Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Design logging for production debuggability — structured JSON with correlation IDs enables finding the needle in the haystack
- Think about observability as three pillars (logs, metrics, traces) that must correlate — request_id bridges them all
- Enforce sensitive data rules as absolute prohibitions — a PII leak in logs is a compliance incident, not a bug
- Make required logging points prescriptive — "log these events at these levels" not "log important things"
- Ensure tenant_id propagation through async contexts — background jobs and events are the most common correlation gaps

### Anti-Patterns for This Activity
- Do NOT write vague masking rules ("hide sensitive data somehow") — specify exact patterns per data type
- Do NOT generate tracing rules for monoliths without explicit tracing tool in the AP — tracing is conditional
- Do NOT forget that metrics are also a security surface — don't expose internal system paths or tenant data in metric labels

### Quality Check
A good output from this activity sounds like:
- "LOG-FMT-03: Request ID propagated from entry point — present on EVERY log within that request. Async jobs carry originating request_id via event metadata."
- "SENS-01: Token masking pattern: first/last 4 chars shown (`eyJh...xyz9`). Credit card: last 4 only (`****-****-****-4242`). Email: domain only (`***@example.com`)."

---

## Source (AP Artifact)

**Document:** Infrastructure & Deployment (typically `10_Infrastructure_Deployment.md`) — specifically the **Observability** subsection

**Sections to extract:**

| Section | Contains | Maps To |
|---------|----------|---------|
| Logging Strategy | Structured format, centralization, retention | observability-logging.md |
| Log Levels | When to use each level | observability-logging.md |
| Metrics | What to measure, dashboards | observability-logging.md (metrics mention) |
| Tracing | Distributed tracing tool, span naming | observability-tracing.md (conditional) |
| Alerting | Thresholds, escalation | observability-logging.md (alerting context) |
| Sensitive Data Handling | What not to log, PII masking | observability-sensitive.md |

**Additional sources:**
- Security Architecture (sensitive data categories, audit logging requirements)
- Multi-Tenancy Architecture (tenant context in logs)
- Technology Stack (observability tools: Grafana, ELK, OTEL, etc.)

---

## Conditional Trigger (observability-tracing.md)

| Generate | Skip |
|----------|------|
| Infrastructure doc specifies a distributed tracing tool (Jaeger, Zipkin, Tempo, AWS X-Ray, OTEL Collector) | No tracing tool mentioned |
| Microservices extension was active in AI-ADLC | Single-service monolith without tracing |
| AP explicitly mentions "distributed tracing" or "span" or "trace propagation" | Logging-only observability strategy |

---

## Target 1: observability-logging.md (ALWAYS)

### Role

Defines how the system produces logs — format, levels, required logging points, and correlation. Ensures logs are consistent, searchable, and useful for debugging without being noisy or exposing sensitive data.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment (Observability) | date: {generation-date} -->

# Observability — Logging

## Logging Stack

**Format:** {from AP — e.g., Structured JSON}
**Transport:** {from AP — e.g., stdout → Fluentd → Elasticsearch}
**Storage:** {from AP — e.g., Elasticsearch with 30-day retention}
**Visualization:** {from AP — e.g., Kibana / Grafana Loki}
**Correlation:** {from AP — e.g., request ID (X-Request-Id) propagated through all services}

---

## Log Format

<!-- begin: AP-sourced -->

Every log entry MUST be structured JSON with these fields:

```json
{
  "timestamp": "ISO-8601 UTC",
  "level": "info|warn|error|debug",
  "service": "{service-name}",
  "module": "{module-name}",
  "requestId": "{correlation-id}",
  "tenantId": "{tenant-id or null}",
  "userId": "{user-id or null}",
  "message": "Human-readable description",
  "data": { },
  "error": {
    "name": "ErrorClass",
    "message": "error message",
    "stack": "only in debug/dev"
  }
}
```

### Format Rules

| Rule | Standard |
|------|----------|
| LOG-FMT-01 | ALL logs MUST be structured JSON — no plain text console.log in production code |
| LOG-FMT-02 | Timestamp: UTC, ISO-8601 format — NEVER local timezone |
| LOG-FMT-03 | Request ID: propagated from entry point (middleware sets `X-Request-Id`) — present on EVERY log within that request |
| LOG-FMT-04 | Tenant ID: included on every log where tenant context exists — enables per-tenant log filtering |
| LOG-FMT-05 | Service name: identifies which deployable unit produced the log |
| LOG-FMT-06 | Module name: identifies which application module (from module-structure.md) produced the log |
| LOG-FMT-07 | Stack traces: included ONLY at ERROR level and ONLY in non-production OR when explicitly configured |

<!-- end: AP-sourced -->

---

## Log Levels

<!-- begin: AP-sourced -->

| Level | When to Use | Examples |
|-------|------------|---------|
| **ERROR** | System cannot perform a requested operation; requires investigation | Unhandled exception, external service unreachable after retries, data integrity violation |
| **WARN** | Unexpected condition that doesn't prevent operation but may indicate a problem | Retry attempt, deprecated API called, approaching rate limit, slow query (>{threshold}ms) |
| **INFO** | Significant business events and state changes | Request received/completed, entity created/updated/deleted, user authenticated, job started/finished |
| **DEBUG** | Detailed diagnostic information for troubleshooting | Query parameters, intermediate calculations, cache hit/miss, full request/response (dev only) |

### Level Rules

| Rule | Standard |
|------|----------|
| LOG-LVL-01 | Production default level: {from AP — e.g., INFO}. DEBUG enabled per-module via configuration. |
| LOG-LVL-02 | ERROR: use ONLY for conditions requiring human investigation — not for expected failures (validation, 404) |
| LOG-LVL-03 | WARN: conditions that should be investigated if frequent — acceptable if occasional |
| LOG-LVL-04 | INFO: one entry per significant business operation (not per internal step) — avoid log flooding |
| LOG-LVL-05 | DEBUG: NEVER enabled globally in production — enable per-module when troubleshooting |
| LOG-LVL-06 | A 400 response (client error) is NOT an ERROR log — it's INFO or WARN at most |
| LOG-LVL-07 | A 500 response (server error) is ALWAYS an ERROR log |

<!-- end: AP-sourced -->

---

## Required Logging Points

<!-- begin: AP-sourced -->

Every application MUST log at these points (minimum):

| When | Level | What to Include |
|------|:-----:|----------------|
| Request received | INFO | method, path, user_id, tenant_id |
| Request completed | INFO | method, path, status_code, duration_ms |
| Authentication success | INFO | user_id, tenant_id, auth_method |
| Authentication failure | WARN | attempted_user, reason, IP |
| Authorization denied | WARN | user_id, resource, action, reason |
| Entity created | INFO | entity_type, entity_id, created_by |
| Entity updated | INFO | entity_type, entity_id, updated_by, changed_fields (names only, not values) |
| Entity deleted | INFO | entity_type, entity_id, deleted_by |
| External service call (start) | DEBUG | service_name, endpoint, method |
| External service call (complete) | INFO | service_name, endpoint, status, duration_ms |
| External service call (failure) | ERROR | service_name, endpoint, error_type, retry_count |
| Background job started | INFO | job_type, job_id, tenant_id |
| Background job completed | INFO | job_type, job_id, duration_ms, result |
| Background job failed | ERROR | job_type, job_id, error, will_retry |
| Cache miss | DEBUG | cache_key, entity_type |
| Slow query detected | WARN | query_summary (no params), duration_ms, threshold |
| Unhandled exception | ERROR | error_name, error_message, stack (non-prod), request context |

<!-- end: AP-sourced -->

---

## Correlation & Context

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| LOG-CTX-01 | Request ID: generated at API entry (or extracted from `X-Request-Id` header) — propagated through ALL downstream calls |
| LOG-CTX-02 | Tenant ID: extracted from auth context — present on every log within that tenant's request |
| LOG-CTX-03 | User ID: from auth context — present on authenticated request logs |
| LOG-CTX-04 | Span/Trace ID: if tracing enabled, include trace_id in log entries for log↔trace correlation |
| LOG-CTX-05 | Async context: background jobs/events MUST carry originating request_id and tenant_id |

<!-- end: AP-sourced -->

---

## Metrics (Brief Reference)

<!-- begin: AP-sourced -->

| Category | Key Metrics |
|----------|-------------|
| Request | request_count, request_duration_ms (p50, p95, p99), error_rate |
| Database | query_duration_ms, connection_pool_usage, slow_query_count |
| Cache | hit_rate, miss_rate, eviction_count |
| Queue | queue_depth, processing_time, dead_letter_count |
| System | cpu_usage, memory_usage, disk_usage |
| Business | {domain-specific from AP — e.g., incidents_created, sla_breaches} |

Metrics implementation details are technology-specific — follow the observability stack conventions.

<!-- end: AP-sourced -->

---

## Anti-Patterns (DO NOT)

1. **DO NOT** use `console.log` / `print` / `System.out` in production code — use the structured logger
2. **DO NOT** log at INFO level inside loops — log once before/after or use DEBUG
3. **DO NOT** log full request/response bodies at INFO level — use DEBUG only
4. **DO NOT** create custom log levels — use only ERROR, WARN, INFO, DEBUG
5. **DO NOT** log "entering function" / "exiting function" at INFO — that's DEBUG at best, noise at worst
6. **DO NOT** swallow exceptions silently (catch without logging)
7. **DO NOT** log the same event at multiple levels (e.g., WARN then ERROR for the same failure)
```

---

## Target 2: observability-sensitive.md (ALWAYS)

### Role

Defines what MUST NEVER appear in logs, metrics, traces, or error messages. This is the data protection enforcement for observability — preventing PII leaks, credential exposure, and compliance violations through logging.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Security Architecture + Infrastructure (Observability) | date: {generation-date} -->

# Observability — Sensitive Data Rules

## Purpose

This file defines what MUST NEVER be logged, traced, or included in metrics/error messages. Violations are SECURITY INCIDENTS.

---

## NEVER Log (Absolute Prohibitions)

<!-- begin: AP-sourced -->

| Category | Specific Items | Why |
|----------|---------------|-----|
| Credentials | Passwords, password hashes, API keys, tokens (access/refresh), private keys | Credential exposure |
| Secrets | Encryption keys, signing secrets, connection strings with credentials | Secret leakage |
| PII (direct) | {from AP — e.g., SSN, national ID, passport number, credit card number, bank account} | Compliance (GDPR, PCI, etc.) |
| PII (contact) | {from AP — e.g., email address, phone number, physical address — in bulk/list form} | Privacy |
| Session data | Full session tokens, cookie values | Session hijacking |
| Request bodies containing auth | Login request payloads, token exchange bodies | Credential exposure |
| Query parameters with secrets | `?token=xxx`, `?api_key=xxx` | URL logging exposes secrets |
| Internal system paths | Full filesystem paths, internal IP addresses, infrastructure hostnames | Reconnaissance aid |
| Multi-tenant data in wrong context | Another tenant's data appearing in current tenant's log stream | Cross-tenant leakage |

<!-- end: AP-sourced -->

---

## Masking Rules

<!-- begin: AP-sourced -->

When sensitive data MUST be referenced for debugging context (but not exposed):

| Data Type | Masking Pattern | Example |
|-----------|----------------|---------|
| Email | Show domain only | `***@example.com` |
| Phone | Last 4 digits | `***-***-1234` |
| Token | First/last 4 chars | `eyJh...xyz9` |
| API Key | Prefix only | `sk_live_***` |
| Credit Card | Last 4 digits | `****-****-****-4242` |
| IP Address | {from AP — e.g., full allowed / last octet masked} | `192.168.1.***` |
| User ID | {from AP — e.g., full UUID allowed (not PII)} | `550e8400-e29b-41d4-a716-446655440000` |

### Masking Rules

| Rule | Standard |
|------|----------|
| SENS-01 | If you MUST reference sensitive data for context, use the masking patterns above — NEVER full values |
| SENS-02 | Masking happens at LOG TIME — never store unmasked then mask on display |
| SENS-03 | Error messages returned to clients: NEVER include sensitive data — use error codes |
| SENS-04 | Stack traces in production responses: NEVER — only in logs (and only at ERROR level) |
| SENS-05 | Log sampling: if bulk-logging entities, NEVER include PII fields — only IDs and status |

<!-- end: AP-sourced -->

---

## Safe to Log

| Data | Allowed Because |
|------|----------------|
| User ID (UUID) | Not PII by itself — opaque identifier |
| Tenant ID | Required for multi-tenant debugging — opaque identifier |
| Entity IDs | Required for tracing operations — opaque identifiers |
| Timestamps | Operational data |
| HTTP status codes | No sensitive content |
| Request duration | Performance metric |
| Module/service name | System metadata |
| Error names/types | Debugging context (no user data) |
| Changed field NAMES (not values) | Audit trail without data exposure |

---

## Enforcement

| Rule | Standard |
|------|----------|
| SENS-06 | Code review: EVERY log statement involving user data MUST be reviewed against this list |
| SENS-07 | Automated scanning: configure log analyzer to alert on patterns matching sensitive data (email regex, card numbers, etc.) |
| SENS-08 | Test coverage: include tests that verify sensitive fields are NOT present in log output |
| SENS-09 | Incident response: if sensitive data found in logs, treat as security incident — purge affected log entries |

---

## Anti-Patterns

1. **NEVER** log full request bodies on endpoints that accept credentials
2. **NEVER** log full database query results (may contain PII)
3. **NEVER** include error.stack in production API responses
4. **NEVER** log "for debugging" and forget to remove — use DEBUG level
5. **NEVER** log webhook payloads verbatim (may contain third-party secrets)
```

---

## Target 3: observability-tracing.md (CONDITIONAL)

### Role

Defines distributed tracing conventions — span naming, attribute standards, instrumentation requirements, and trace propagation. Only relevant for systems with multiple services or explicit tracing requirements.

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Infrastructure & Deployment (Tracing) | date: {generation-date} -->

# Observability — Distributed Tracing

## Tracing Stack

**Protocol:** {from AP — e.g., OpenTelemetry (OTLP)}
**Collector:** {from AP — e.g., OTEL Collector → Tempo / Jaeger}
**Visualization:** {from AP — e.g., Grafana Tempo / Jaeger UI}
**Sampling:** {from AP — e.g., 100% in dev, 10% in production / adaptive}

---

## Span Naming Conventions

<!-- begin: AP-sourced -->

| Span Type | Naming Pattern | Example |
|-----------|---------------|---------|
| HTTP server (incoming) | `{HTTP_METHOD} {route_template}` | `GET /api/v1/incidents/:id` |
| HTTP client (outgoing) | `{service_name}.{HTTP_METHOD} {path}` | `notification-service.POST /send` |
| Database query | `db.{operation} {table}` | `db.select incidents` |
| Cache operation | `cache.{operation} {key_pattern}` | `cache.get incident:{id}` |
| Queue publish | `queue.publish {queue_name}` | `queue.publish incident-events` |
| Queue consume | `queue.consume {queue_name}` | `queue.consume incident-events` |
| Internal operation | `{module}.{operation}` | `incident-management.escalate` |

<!-- end: AP-sourced -->

---

## Span Attributes (Required)

<!-- begin: AP-sourced -->

| Attribute | When | Value |
|-----------|------|-------|
| `service.name` | Always | Name of the deployable service |
| `service.version` | Always | Current version of the service |
| `tenant.id` | When tenant context exists | Active tenant UUID |
| `user.id` | When authenticated | Requesting user UUID |
| `http.method` | HTTP spans | GET, POST, etc. |
| `http.route` | HTTP spans | Route template (not actual URL with IDs) |
| `http.status_code` | HTTP spans | Response status code |
| `db.system` | Database spans | `postgresql`, `redis`, etc. |
| `db.operation` | Database spans | `select`, `insert`, `update`, `delete` |
| `db.table` | Database spans | Table name (not query content) |
| `error` | On failure | `true` |
| `error.type` | On failure | Exception class name |

<!-- end: AP-sourced -->

---

## Instrumentation Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| TRACE-01 | Automatic instrumentation for: HTTP server, HTTP client, database, cache, queue — via {from AP — e.g., OTEL SDK auto-instrumentation} |
| TRACE-02 | Manual spans for significant business operations: `{module}.{operation}` — e.g., `incident.escalate`, `sla.evaluate` |
| TRACE-03 | Propagation: {from AP — e.g., W3C TraceContext (traceparent header)} across ALL service boundaries |
| TRACE-04 | Context propagation in async: events/messages MUST carry trace context in metadata/headers |
| TRACE-05 | Span status: set ERROR status on business failures (not just exceptions) |
| TRACE-06 | Span events: add events for significant checkpoints within long operations |
| TRACE-07 | NEVER include sensitive data in span attributes — same rules as observability-sensitive.md |
| TRACE-08 | Sampling: {from AP — e.g., always sample errors (100%), sample success at configured rate} |

<!-- end: AP-sourced -->

---

## Trace-Log Correlation

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| TRACE-09 | Include `trace_id` in every structured log entry — enables jumping from log to trace |
| TRACE-10 | Include `span_id` in log entries within active spans |
| TRACE-11 | Log request_id maps to trace root span — one request = one trace |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **DO NOT** create spans for trivial operations (< 1ms utility functions)
2. **DO NOT** include request/response bodies in span attributes (use events sparingly)
3. **DO NOT** propagate trace context to external third-party systems (unless they support it)
4. **DO NOT** disable tracing in tests — verify instrumentation is correct
5. **DO NOT** use actual parameter values in span names (use templates: `:id` not the UUID)
```

---

## Transformation Rules

| AP Content | Transformation | Output |
|-----------|---------------|--------|
| Logging format (structured/unstructured) | Set log format standard + LOG-FMT rules | observability-logging.md |
| Log levels guidance | Convert to LOG-LVL-NN rules | observability-logging.md |
| What to log (audit/operational events) | Convert to Required Logging Points table | observability-logging.md |
| Sensitive data categories (from Security) | Convert to NEVER-log list + masking rules | observability-sensitive.md |
| PII handling policy | Convert to SENS-NN rules | observability-sensitive.md |
| Distributed tracing tool + config | Set tracing stack + TRACE-NN rules | observability-tracing.md |
| Span naming conventions | Convert to span naming table | observability-tracing.md |
| Metrics list | Convert to Metrics reference table | observability-logging.md |
| Alerting thresholds | Context in logging rules (what to WARN on) | observability-logging.md |

### Numbering Convention

| Prefix | Domain |
|--------|--------|
| LOG-FMT-NN | Log format |
| LOG-LVL-NN | Log levels |
| LOG-CTX-NN | Correlation and context |
| SENS-NN | Sensitive data |
| TRACE-NN | Distributed tracing |

---

## Key Rules for This Mapping

1. **Logging is ALWAYS generated** — every system needs consistent logging regardless of size
2. **Sensitive data rules are ALWAYS generated** — even monoliths must not log credentials
3. **Tracing is CONDITIONAL** — only when tracing tool is specified or system is distributed
4. **Cross-reference security-rules.md** — sensitive categories must be consistent
5. **Cross-reference multi-tenancy.md** — tenant_id in logs is mandatory for multi-tenant systems
6. **Log format is prescriptive** — exact JSON schema, not "use structured logging"
7. **Required logging points prevent silent failures** — minimum logging guarantees debuggability
8. **Masking rules are specific** — exact patterns, not "hide sensitive data somehow"

---

## Depth Adaptation

| Depth | observability-logging.md | observability-sensitive.md | observability-tracing.md |
|-------|------------------------|---------------------------|------------------------|
| **Minimal** | Log format + levels + 10 key logging points | Core NEVER-log list (credentials + PII) | Basic span naming only |
| **Standard** | Full structure as defined above | Full structure with masking patterns | Full structure as defined |
| **Comprehensive** | Full + log analysis playbook + runbook triggers + SLO-based alerting rules | Full + data classification matrix + compliance mapping (GDPR Art. 30) | Full + custom span attribute registry + sampling strategy optimization + trace-based testing |

---

## Reconciliation Behavior

| Change | Impact | Action |
|--------|--------|--------|
| Observability stack changed (e.g., ELK → Loki) | Transport and visualization references | Update stack identity; format rules likely unchanged |
| New sensitive data category identified | NEVER-log list expanded | Add to observability-sensitive.md; signal AI-GCE |
| Tracing tool added (was previously absent) | observability-tracing.md now needed | Generate new conditional file |
| Tracing removed | observability-tracing.md no longer justified | Flag for removal (user confirms) |
| New required logging point added | Required Logging Points table | Add entry; no other files affected |
| Log retention changed | Stack identity section | Update retention value |
| Multi-tenancy added after initial gen | LOG-CTX-02 + LOG-FMT-04 need tenant_id | Add tenant context rules; cross-ref multi-tenancy.md |
