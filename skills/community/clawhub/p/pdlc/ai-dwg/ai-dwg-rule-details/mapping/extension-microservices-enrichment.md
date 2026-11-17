<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Microservices Extension Enrichment

## Purpose

When the **Microservices** extension was active in AI-ADLC, this mapping enriches steering files with distributed systems patterns and FORCES generation of `resilience-standards.md` and `observability-tracing.md` regardless of normal conditional triggers.

**Trigger:** `adlc-state.md` → Enabled Extensions includes `microservices`

---

## MANDATORY: Stage Sub-Role — Distributed Systems Engineer

During THIS activity, ALSO adopt the mindset of a **Distributed Systems Engineer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Every service boundary is a failure boundary — design for independence, not for the happy path of all services being available
- Eventual consistency is the default, not the exception — code, tests, and user interfaces must all handle lag between services
- Idempotency is non-negotiable for cross-service communication — without it, retries create duplicates and sagas create chaos
- Shared databases are forbidden — each service owns its data; shared contracts live in a versioned library
- Force generation of resilience-standards.md and observability-tracing.md — distributed systems REQUIRE both regardless of normal conditional triggers

### Anti-Patterns for This Activity
- Do NOT allow services to read another service's database directly — all inter-service data access goes through APIs or events
- Do NOT skip contract testing — consumer-driven contracts are the safety net for independently deployed services
- Do NOT generate microservices enrichment unless the `microservices` extension is confirmed active

### Quality Check
A good output from this activity sounds like:
- "MS-MOD-01: Services communicate via APIs or events — NEVER shared database. MS-CODE-04: Outbox pattern for reliable event publishing — event + business data in same transaction."
- "MS-API-04: Idempotency keys REQUIRED on all cross-service write operations. MS-CODE-02: All event handlers MUST be idempotent — duplicate delivery is expected."

---

## Files Enriched

| File | Enrichment |
|------|-----------|
| `module-structure.md` | Service boundary definitions, inter-service communication rules |
| `resilience-standards.md` | FORCED generation — full catalog (circuit breakers per service, saga patterns) |
| `observability-tracing.md` | FORCED generation — distributed trace propagation mandatory |
| `api-standards.md` | Inter-service API conventions, service discovery references |
| `coding-standards.md` | Distributed patterns (idempotency, eventual consistency handling) |
| `testing-strategy.md` | Contract testing, service-level integration tests |

---

## Forced Conditional Generation

| File | Normal Trigger | With Microservices Extension |
|------|---------------|:---------------------------:|
| `resilience-standards.md` | >3 integrations | ✅ ALWAYS — required for service-to-service calls |
| `observability-tracing.md` | Tracing tool specified | ✅ ALWAYS — required to trace requests across services |

---

## Enrichment Rules

### module-structure.md Additions

```markdown
## Service Boundaries

| Service | Owns Modules | Communication |
|---------|-------------|--------------|
| {service-a} | `{module-1}`, `{module-2}` | HTTP REST / gRPC / Events |
| {service-b} | `{module-3}` | HTTP REST / Events |

### Inter-Service Communication Rules

| Rule | Standard |
|------|----------|
| MS-MOD-01 | Services communicate via defined APIs or events — NEVER shared database |
| MS-MOD-02 | Each service owns its data — no service reads another's database directly |
| MS-MOD-03 | Shared contracts (DTOs, event schemas) live in a shared library — versioned independently |
| MS-MOD-04 | Service dependencies must be explicit and documented — no hidden couplings |
```

### api-standards.md Additions

```markdown
## Inter-Service API Conventions

| Rule | Standard |
|------|----------|
| MS-API-01 | Service-to-service auth: {from AP — e.g., mTLS / service API keys / JWT with service identity} |
| MS-API-02 | Service discovery: {from AP — e.g., DNS-based / service registry / hardcoded in config} |
| MS-API-03 | Inter-service timeout: stricter than external (e.g., 5s) — fail fast |
| MS-API-04 | Idempotency keys: REQUIRED on all cross-service write operations |
| MS-API-05 | Correlation ID (X-Request-Id): MUST be propagated across all service calls |
```

### coding-standards.md Additions

```markdown
## Distributed System Patterns

| Rule | Standard |
|------|----------|
| MS-CODE-01 | Design for eventual consistency — never assume synchronous state across services |
| MS-CODE-02 | Idempotency: all event handlers and cross-service endpoints MUST be idempotent |
| MS-CODE-03 | Saga pattern: for multi-service transactions — implement compensating actions for rollback |
| MS-CODE-04 | Outbox pattern: for reliable event publishing — write event + business data in same transaction |
| MS-CODE-05 | Schema registry: event schemas versioned and validated — breaking changes require new version |
```

### testing-strategy.md Additions

```markdown
## Microservices Testing

| Rule | Standard |
|------|----------|
| MS-TEST-01 | Contract tests: verify API contracts between services (consumer-driven) |
| MS-TEST-02 | Service integration tests: test with real dependencies via Docker (one service at a time) |
| MS-TEST-03 | Chaos testing: {from AP — e.g., simulate service failures in staging / not practiced yet} |
| MS-TEST-04 | Each service MUST be independently testable — no test requires all services running |
```

---

## Key Rule

Microservices enrichment fundamentally changes how module-structure.md and resilience-standards.md are generated — it introduces service boundaries as a first-class concept above module boundaries.
