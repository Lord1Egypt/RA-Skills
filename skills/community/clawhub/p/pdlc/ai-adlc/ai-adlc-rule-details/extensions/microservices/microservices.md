<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Microservices Deep-Dive

**Extension ID:** microservices
**Version:** 1.1.0
**Rule Prefix:** MS
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 5 (Container Design)
- **Secondary Stages:** Stage 11 (Integration Architecture), Stage 10 (Infrastructure & Deployment)

These rules apply to service decomposition, inter-service communication, data ownership, and operational concerns for microservice architectures.

---

## MANDATORY: Extension Sub-Role — Distributed Systems Engineer

When this extension is active, ALSO adopt the mindset of a **Distributed Systems Engineer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of microservices rule enforcement.

### Behavioral Shifts
- Assume the network is unreliable — every inter-service call can fail, timeout, or return partial results; design for it
- Enforce exclusive data ownership per service — sharing databases is coupling in disguise
- Map failure cascades: if Service A fails, trace what happens to B, C, D
- Prefer async over sync — synchronous chains create tight coupling and cascade failures

### Anti-Patterns for This Extension
- Do NOT create a "distributed monolith" — services that must deploy together or share databases are not microservices
- Do NOT design services around technical layers (API service, DB service) — design around business capabilities

### Quality Check
A good output with this extension sounds like:
- "5 services, each owning its data store; communication: 2 sync (gRPC), 3 async (events via broker); saga for checkout; service mesh for mTLS + tracing..."

---

## Rules

### Rule MS-01: Single Responsibility per Service

**Statement:** Each microservice must own exactly one business capability or bounded context. A service must be independently deployable and have a clear, singular reason to change.

**Verification:**
- [ ] Each service maps to one and only one business capability
- [ ] No single business change requires simultaneous deployment of multiple services
- [ ] Service responsibilities are documented and non-overlapping
- [ ] Service can be described in one sentence without using "and" for unrelated concerns
- [ ] Team ownership is clear (one team per service; one service may have one team)

**Anti-Pattern:** "Distributed monolith" — services that must be deployed together, share release trains, or contain logic for multiple unrelated capabilities.

**ADR Trigger:** Yes — When deciding how to split or merge services (boundary definition for ambiguous capabilities).

---

### Rule MS-02: Per-Service Data Ownership

**Statement:** Each microservice must own its data store exclusively. No other service may read from or write to another service's data store directly. Data sharing happens only through published APIs or events.

**Verification:**
- [ ] Each service has its own logical data store (not a shared schema)
- [ ] No direct database queries across service boundaries
- [ ] Data needed by other services is exposed via APIs or events
- [ ] No shared database tables between services
- [ ] Data duplication (read models, caches) is explicitly documented and managed

**Anti-Pattern:** Shared database — multiple services reading/writing to the same tables, creating hidden coupling and preventing independent schema evolution.

**ADR Trigger:** Yes — When introducing data duplication or choosing between API calls and event-driven data replication for cross-service data access.

---

### Rule MS-03: Service Mesh Definition

**Statement:** Inter-service communication must be managed through a service mesh or equivalent infrastructure layer that provides mTLS, traffic management, observability, and policy enforcement transparently to application code.

**Verification:**
- [ ] Service mesh (or equivalent) is identified in the architecture
- [ ] mTLS between services is enabled (zero-trust inter-service communication)
- [ ] Traffic management capabilities are documented (retries, timeouts, circuit breaking)
- [ ] Observability (distributed tracing, metrics) is provided at the mesh layer
- [ ] Application code does not implement cross-cutting communication concerns directly

**Anti-Pattern:** Each service implementing its own retry logic, TLS configuration, and observability instrumentation, leading to inconsistent behavior and duplicated infrastructure code.

**ADR Trigger:** Yes — When selecting the service mesh technology or deciding whether a full mesh is needed vs. simpler alternatives (e.g., client-side libraries).

---

### Rule MS-04: Distributed Tracing Design

**Statement:** Every inter-service request must carry a correlation ID (trace ID) that propagates across all synchronous and asynchronous calls. Tracing must enable reconstruction of the full request path across all services.

**Verification:**
- [ ] A trace ID is generated at the system entry point and propagated through all calls
- [ ] Both synchronous (HTTP/gRPC) and asynchronous (message/event) paths propagate trace context
- [ ] Trace ID appears in all logs for every service in the chain
- [ ] Sampling strategy is defined (trace 100% vs. sample percentage)
- [ ] Trace visualization tooling is identified (capable of showing full call chains)

**Anti-Pattern:** Services generating their own unrelated request IDs without propagating a system-wide correlation ID, making it impossible to trace a request across services.

**ADR Trigger:** No

---

### Rule MS-05: Saga Pattern for Distributed Transactions

**Statement:** Any business operation spanning multiple services must use a saga pattern (choreography or orchestration). Two-phase commit (2PC) across services is prohibited.

**Verification:**
- [ ] All multi-service operations use saga (not distributed transactions)
- [ ] Each saga has documented compensating actions for every step
- [ ] Saga pattern choice (choreography vs. orchestration) is documented per workflow
- [ ] Failure scenarios and their compensation paths are explicitly designed
- [ ] Saga state is persisted (survives service restarts)
- [ ] Idempotency of saga steps is ensured

**Anti-Pattern:** Attempting distributed transactions (2PC/XA) across microservices, creating tight coupling, latency, and availability issues when any participant is unavailable.

**ADR Trigger:** Yes — When choosing between choreography and orchestration for a specific multi-service workflow.

---

### Rule MS-06: Schema Registry and Event Contract Management

**Statement:** All events published between services must be registered in a schema registry with explicit versioning and compatibility rules. Producers cannot publish breaking changes without following the compatibility policy.

**Verification:**
- [ ] A schema registry (or equivalent contract management) is identified
- [ ] Every inter-service event has a registered schema
- [ ] Compatibility mode is defined (backward, forward, or full compatibility)
- [ ] Schema evolution process is documented (how to add fields, deprecate, version)
- [ ] Breaking changes require a new event version (not in-place modification)
- [ ] Consumer-driven contract testing is in place

**Anti-Pattern:** Publishing events without schema management, leading to silent consumer breakage when producers change event structure.

**ADR Trigger:** Yes — When defining the compatibility mode (backward vs. forward vs. full) for event schemas.

---

### Rule MS-07: Service Discovery and Routing

**Statement:** Services must discover each other through a service registry or DNS-based discovery mechanism. No hard-coded addresses or host names in application configuration.

**Verification:**
- [ ] Service discovery mechanism is defined (DNS, registry, mesh-provided)
- [ ] No service-to-service communication uses hard-coded IPs or hostnames
- [ ] Health checks determine service availability in the discovery registry
- [ ] Load balancing strategy is documented (client-side vs. server-side)
- [ ] Graceful handling of service instances appearing/disappearing

**Anti-Pattern:** Configuration files listing specific IP addresses or hostnames for upstream services, breaking when instances scale or move.

**ADR Trigger:** No

---

### Rule MS-08: API Gateway as Single Entry Point

**Statement:** All external (north-south) traffic must enter through an API gateway. The gateway handles cross-cutting concerns (authentication, rate limiting, routing) and shields internal service topology from external consumers.

**Verification:**
- [ ] An API gateway is defined as the external entry point
- [ ] Internal service topology is not exposed to external consumers
- [ ] Cross-cutting concerns (auth, rate limiting, CORS) are handled at the gateway
- [ ] Gateway routing rules are documented
- [ ] Gateway failure mode is designed (what happens when gateway is down)
- [ ] No external traffic bypasses the gateway to reach internal services directly

**Anti-Pattern:** Exposing individual microservice endpoints directly to the internet, leaking internal architecture and duplicating cross-cutting logic in each service.

**ADR Trigger:** No

---

### Rule MS-09: Independent Deployment Verification

**Statement:** Every microservice must be independently deployable without requiring coordinated deployments of other services. Backward compatibility of APIs and events must be maintained across deployments.

**Verification:**
- [ ] Each service can be deployed without deploying any other service
- [ ] API changes are backward compatible (additive only; breaking changes go through versioning)
- [ ] Event schema changes follow the compatibility policy (MS-06)
- [ ] No shared libraries with business logic that require lockstep upgrades
- [ ] Database migrations are backward compatible (expand-then-contract)
- [ ] Deployment pipeline is per-service (not monorepo-wide)

**Anti-Pattern:** "Deploy train" — requiring multiple services to release simultaneously, negating the key benefit of microservices (independent deployability).

**ADR Trigger:** No

---

### Rule MS-10: Contract Testing Between Services

**Statement:** Every service-to-service integration (API or event) must have contract tests that verify the consumer's expectations against the producer's implementation. Contract tests run independently of end-to-end tests.

**Verification:**
- [ ] Consumer-driven contracts are defined for all inter-service APIs
- [ ] Contract tests run in CI for both producer and consumer
- [ ] Breaking a contract blocks the producer's deployment pipeline
- [ ] Event contracts (schemas) are tested for compatibility on publish
- [ ] Contract tests are lightweight (no full environment required)

**Anti-Pattern:** Relying solely on end-to-end integration tests to catch inter-service incompatibilities, resulting in late and expensive failure detection.

**ADR Trigger:** No

---

### Rule MS-11: Service Autonomy Under Failure

**Statement:** Each service must define its behavior when upstream dependencies are unavailable. Services must continue operating (possibly degraded) when non-critical dependencies fail.

**Verification:**
- [ ] Each service documents its critical vs. non-critical dependencies
- [ ] Fallback behavior is defined for each non-critical dependency failure
- [ ] Circuit breaker or equivalent pattern protects against cascading failure
- [ ] Timeouts are defined for every outbound call
- [ ] Service can start without all dependencies available (eventual readiness)

**Anti-Pattern:** A service that crashes or becomes completely unavailable because a single optional upstream dependency is down, causing cascading failure.

**ADR Trigger:** No

---

### Rule MS-12: Observability per Service

**Statement:** Every microservice must expose health checks, structured logs, metrics, and distributed traces. Observability is not optional — it is a hard requirement for every service in production.

**Verification:**
- [ ] Health endpoint (liveness + readiness) is defined per service
- [ ] Structured logging with correlation IDs is implemented
- [ ] Standard metrics are exposed (request rate, error rate, latency — RED metrics)
- [ ] Distributed traces propagate through the service
- [ ] Alerting rules are defined per service for critical metrics
- [ ] Dashboard or view exists showing service health at a glance

**Anti-Pattern:** "Black box" services that provide no observability, making incidents impossible to diagnose without resorting to log file searches or code inspection.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Microservices rules active, verify:

- [ ] Every service has a single, documented business capability
- [ ] Data ownership is exclusive per service (no shared databases)
- [ ] Service mesh or equivalent is defined for inter-service communication
- [ ] Distributed tracing propagates through all communication paths
- [ ] Multi-service transactions use sagas with documented compensations
- [ ] Event schemas are managed with versioning and compatibility rules
- [ ] All services are independently deployable
- [ ] Contract tests exist for all inter-service integrations
- [ ] Each service defines its failure behavior for dependency unavailability
- [ ] Observability (health, logs, metrics, traces) is a hard requirement per service

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| MS-01 | Service boundary definition for ambiguous capabilities |
| MS-02 | Choosing data replication strategy (API vs. events) |
| MS-03 | Selecting service mesh technology or alternative |
| MS-05 | Choosing choreography vs. orchestration per workflow |
| MS-06 | Defining schema compatibility mode |

---

## Templates

### Service Ownership Card

```
## Service: {Name}

**Business Capability:** {Single capability owned}
**Owning Team:** {Team name}
**Data Store:** {Type + logical name}
**APIs Exposed:** {List of public API endpoints}
**Events Published:** {List of events}
**Events Consumed:** {List of events}
**Critical Dependencies:** {Services that must be available}
**Non-Critical Dependencies:** {Services with fallback on failure}
**SLA:** {Availability target}
```

### Saga Design Card

```
## Saga: {Name}

**Business Operation:** {What the saga achieves}
**Pattern:** Choreography / Orchestration
**Steps:**
| Step | Service | Action | Compensating Action |
|------|---------|--------|---------------------|
| 1 | {Service} | {Action} | {Undo action} |
| 2 | {Service} | {Action} | {Undo action} |

**Failure Handling:** {What happens on partial failure}
**Timeout:** {Max saga duration}
**Idempotency:** {How duplicates are handled}
```

### Contract Test Summary

```
## Contract: {Consumer} → {Producer}

**Integration Type:** API / Event
**Contract Specification:** {Location/reference}
**Compatibility Mode:** Backward / Forward / Full
**CI Pipeline:** {Producer pipeline blocks on break: Yes/No}
**Last Verified:** {Date}
```
