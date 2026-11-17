<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Extension Rules: Resilience Patterns

**Extension ID:** resilience-patterns
**Version:** 1.1.0
**Rule Prefix:** RES
**Status:** Active

---

## Activation Point

- **Primary Stage:** Stage 5 (Container Design) / Stage 11 (Integration Architecture)
- **Secondary Stages:** Stage 10 (Infrastructure & Deployment), Stage 12 (Component Design)

These rules apply to distributed system communication, failure handling, and ensuring the system degrades gracefully rather than failing catastrophically.

---

## MANDATORY: Extension Sub-Role — Resilience Engineer

When this extension is active, ALSO adopt the mindset of a **Resilience Engineer**. This does NOT replace your primary role (CTO / Chief Architect) — it ADDS a thinking dimension for the duration of resilience rule enforcement.

### Behavioral Shifts
- Design for failure, not just success — every external call WILL fail eventually; define what happens when it does
- Budget timeouts across the call chain — if 4 sequential calls each timeout at 5s, that's 20s total; is that acceptable?
- Classify dependencies by criticality — failed recommendations (tolerable) vs. failed payments (critical) get different patterns
- Define fallback behaviour explicitly — "circuit open" is not a plan; what does the user experience?

### Anti-Patterns for This Extension
- Do NOT use unbounded retries — always define max attempts, backoff with jitter, and idempotency requirements
- Do NOT treat all dependencies as equally critical — tier them and design proportionate resilience

### Quality Check
A good output with this extension sounds like:
- "Payment gateway: circuit breaker opens after 5 failures/30s, fallback: queue for retry; timeout budget: total 8s across 4 hops; graceful degradation: 3 defined tiers..."

---

## Rules

### Rule RES-01: Circuit Breaker on All External Calls

**Statement:** Every outbound call to an external system or cross-service dependency must be protected by a circuit breaker. The circuit breaker must define thresholds for opening, half-open probing, and closing.

**Verification:**
- [ ] Circuit breaker is applied to every external/cross-service call
- [ ] Open threshold is defined (failure count or failure rate within time window)
- [ ] Half-open behavior is defined (how many probe requests, success criteria to close)
- [ ] Close criteria are defined (when to resume normal traffic)
- [ ] Fallback behavior is defined when circuit is open
- [ ] Circuit state is observable (metrics, logs, dashboards)

**Anti-Pattern:** Continuously retrying a failing upstream service without ever stopping, creating a "retry storm" that amplifies the problem and prevents recovery.

**ADR Trigger:** Yes — When defining circuit breaker thresholds and fallback strategies for critical integration points.

---

### Rule RES-02: Timeout Policy per Integration

**Statement:** Every outbound call must have an explicit timeout. Timeouts must be tuned per integration based on expected latency. No call is allowed to wait indefinitely.

**Verification:**
- [ ] Every outbound call has a defined timeout value
- [ ] Timeout values are based on measured P99 latency of the dependency (not arbitrary)
- [ ] Global request timeout budget exists (sum of sequential calls ≤ total budget)
- [ ] Timeout exceeded behavior is defined (retry, fallback, or fail)
- [ ] No infinite or excessively long timeouts exist
- [ ] Timeout values are configurable without code changes

**Anti-Pattern:** Using framework defaults (often 30–60 seconds) for all calls regardless of expected latency, causing requests to hang for minutes when a dependency is unresponsive.

**ADR Trigger:** No

---

### Rule RES-03: Retry Strategy with Exponential Backoff and Jitter

**Statement:** Retryable operations must use exponential backoff with random jitter. Maximum retry count must be bounded. Only idempotent operations may be retried.

**Verification:**
- [ ] Retry is applied only to idempotent and transient-failure-eligible operations
- [ ] Exponential backoff is used (not fixed delay)
- [ ] Random jitter is added to prevent thundering herd on recovery
- [ ] Maximum retry count is defined and bounded (not infinite)
- [ ] Non-idempotent operations are NOT retried (or have idempotency keys)
- [ ] Retry budget is defined (max % of total requests that can be retries)

**Anti-Pattern:** Immediate, aggressive retries without backoff, creating a thundering herd that overwhelms the recovering service and extends the outage.

**ADR Trigger:** No

---

### Rule RES-04: Bulkhead Isolation

**Statement:** Critical system resources (connection pools, thread pools, memory allocations) must be isolated per dependency using the bulkhead pattern. A slow or failing dependency must not exhaust resources needed by other dependencies.

**Verification:**
- [ ] Resource pools (connections, threads) are isolated per dependency
- [ ] Exhaustion of one pool does not affect other pools
- [ ] Pool sizes are tuned based on expected load per dependency
- [ ] Queue limits are defined for each bulkhead (bounded queues, not unbounded)
- [ ] Bulkhead breach (pool exhaustion) triggers fast failure (not queueing indefinitely)
- [ ] Bulkhead metrics are monitored (utilization, rejections)

**Anti-Pattern:** Single shared connection pool for all outbound calls — a slow dependency exhausts the pool, blocking healthy dependencies too (cascading failure).

**ADR Trigger:** No

---

### Rule RES-05: Graceful Degradation Catalog

**Statement:** Every system capability must be classified as critical or non-critical. For each non-critical capability, a degraded behavior must be defined (fallback, cached data, reduced functionality, feature disabled).

**Verification:**
- [ ] All capabilities are classified: critical (must work) vs. non-critical (can degrade)
- [ ] Degraded behavior is defined for each non-critical capability
- [ ] Degradation is automatic (no manual intervention needed)
- [ ] Users are informed when experiencing degraded mode (clear UI indicators)
- [ ] System can operate in degraded mode indefinitely (not just short bursts)
- [ ] Recovery from degraded to normal mode is automatic when dependency recovers

**Anti-Pattern:** All-or-nothing failure — the entire system becomes unavailable because one non-critical dependency is down, even though 80% of functionality could still work.

**ADR Trigger:** Yes — When classifying capabilities as critical vs. non-critical (affects user expectations and SLA commitments).

---

### Rule RES-06: Health Check Architecture

**Statement:** Every service must expose distinct health check endpoints: liveness (process alive), readiness (can serve traffic), and startup (initialization complete). Orchestrators use these to make routing and restart decisions.

**Verification:**
- [ ] Liveness check exists (confirms process is alive, not deadlocked)
- [ ] Readiness check exists (confirms service can handle requests — dependencies reachable)
- [ ] Startup check exists (for slow-starting services — initialization complete)
- [ ] Health checks are lightweight (no expensive operations)
- [ ] Health check failure triggers documented action (restart, remove from rotation, alert)
- [ ] Health checks do not create cascading failures (downstream health check failure ≠ this service unhealthy)

**Anti-Pattern:** Deep health checks that call all downstream dependencies — if any dependency is unhealthy, this service reports unhealthy, triggering restart, making the situation worse.

**ADR Trigger:** No

---

### Rule RES-07: Failure Mode Analysis per Component

**Statement:** Every component must have a documented failure mode analysis: what can fail, how failure is detected, what the impact is, and what the recovery strategy is.

**Verification:**
- [ ] Each component lists its failure modes (what can go wrong)
- [ ] Detection mechanism is defined per failure mode (how do we know it failed?)
- [ ] Impact is assessed per failure mode (what is affected? blast radius?)
- [ ] Recovery strategy is defined per failure mode (automatic vs. manual)
- [ ] Mean Time to Detection (MTTD) target is established
- [ ] Mean Time to Recovery (MTTR) target is established
- [ ] Failure mode analysis is reviewed when architecture changes

**Anti-Pattern:** Assuming components won't fail, discovering failure modes for the first time during a production incident.

**ADR Trigger:** No

---

### Rule RES-08: Dead Letter Queue for Unprocessable Messages

**Statement:** Every asynchronous message consumer must have a dead letter queue (DLQ). Messages that cannot be processed after maximum retries must be routed to a DLQ for inspection and reprocessing.

**Verification:**
- [ ] DLQ exists for every asynchronous message consumer
- [ ] Retry count before DLQ routing is defined
- [ ] DLQ messages retain full context (original message, error reason, retry count)
- [ ] Monitoring/alerting exists for DLQ depth (messages accumulating)
- [ ] Reprocessing mechanism exists (replay from DLQ after fix)
- [ ] Poison messages (structurally invalid) are detected and DLQ'd immediately (no retry)

**Anti-Pattern:** Silently dropping unprocessable messages or retrying forever, either losing data or creating an infinite retry loop that blocks the queue.

**ADR Trigger:** No

---

### Rule RES-09: Load Shedding Under Pressure

**Statement:** When a service is under excessive load, it must shed lower-priority traffic proactively to protect capacity for higher-priority requests. Overload must result in explicit rejection (with appropriate error signaling), not degraded performance for everyone.

**Verification:**
- [ ] Load shedding triggers are defined (CPU, queue depth, active request count)
- [ ] Priority classification exists for requests (which can be shed first)
- [ ] Shedding returns fast failure to client (e.g., 503 with retry hint, not hanging)
- [ ] Back-pressure mechanism exists for queue-based consumers
- [ ] Shedding is gradual (not cliff-edge all-or-nothing)
- [ ] Load shedding events are logged and alerted

**Anti-Pattern:** Accepting all requests under heavy load, causing response times to degrade for everyone equally until the service collapses entirely.

**ADR Trigger:** Yes — When defining request priority tiers and which traffic to shed first under load.

---

### Rule RES-10: Idempotency for All Retryable Operations

**Statement:** Any operation that may be retried (by client, infrastructure, or resilience mechanisms) must be idempotent. Idempotency keys or natural idempotency must be designed into every such operation.

**Verification:**
- [ ] All retryable operations are idempotent (same input → same effect, regardless of repetition)
- [ ] Idempotency mechanism is defined (idempotency key, natural key, or operation design)
- [ ] Idempotency key storage/TTL is defined (how long to remember a processed key)
- [ ] Non-idempotent operations are explicitly marked as non-retryable
- [ ] Client-generated idempotency keys are used for user-initiated operations

**Anti-Pattern:** Retrying a non-idempotent operation (e.g., "charge payment") without an idempotency key, resulting in duplicate charges.

**ADR Trigger:** No

---

### Rule RES-11: Cascading Failure Prevention

**Statement:** The architecture must explicitly design against cascading failures. No single component failure may propagate to bring down unrelated components. Isolation boundaries are defined and enforced.

**Verification:**
- [ ] Failure blast radius is documented per component (what else fails if this fails?)
- [ ] Isolation boundaries prevent cross-component cascading
- [ ] Circuit breakers, bulkheads, and timeouts work together to contain failures
- [ ] No synchronous chain longer than N hops without async decoupling (N defined)
- [ ] Cascading failure scenarios are tested (chaos testing, fault injection)
- [ ] Maximum fan-out per request is bounded

**Anti-Pattern:** Long synchronous call chains (A → B → C → D → E) where any failure in the chain brings down the entire chain back to the originator.

**ADR Trigger:** No

---

### Rule RES-12: Rate Limiting for Self-Protection

**Statement:** Every externally exposed endpoint and every internal service-to-service endpoint must have rate limiting to prevent abuse and protect service resources from unexpected traffic spikes.

**Verification:**
- [ ] Rate limits are defined per endpoint or endpoint group
- [ ] Rate limiting is per-tenant or per-consumer (not global-only)
- [ ] Rate limit exceeded returns appropriate response (429 with Retry-After header)
- [ ] Rate limits are tunable without deployment
- [ ] Internal services also rate-limit (not just external endpoints)
- [ ] Burst allowance is defined (token bucket or similar with burst tolerance)

**Anti-Pattern:** No rate limiting on internal APIs, allowing a misbehaving internal consumer to exhaust another service's capacity, causing an outage for all consumers.

**ADR Trigger:** No

---

## Verification Checklist (Stage Completion)

Before completing a stage with Resilience rules active, verify:

- [ ] Circuit breakers protect all external and cross-service calls
- [ ] Explicit timeouts are defined per outbound integration
- [ ] Retry strategy uses exponential backoff with jitter (bounded retries)
- [ ] Bulkhead isolation prevents resource exhaustion cascading
- [ ] Graceful degradation catalog classifies all capabilities
- [ ] Health checks (liveness, readiness, startup) are defined per service
- [ ] Failure mode analysis exists for every component
- [ ] Dead letter queues exist for all async consumers
- [ ] Load shedding strategy is defined for overload scenarios
- [ ] All retryable operations are idempotent
- [ ] Cascading failure prevention is designed and testable
- [ ] Rate limiting protects all endpoints

---

## ADR Triggers Summary

| Rule | ADR Required When |
|------|-------------------|
| RES-01 | Defining circuit breaker thresholds and fallback strategies for critical paths |
| RES-05 | Classifying capabilities as critical vs. non-critical |
| RES-09 | Defining request priority tiers and load shedding policy |

---

## Templates

### Failure Mode Analysis Card

```
## Component: {Name}

| Failure Mode | Detection | Impact (Blast Radius) | Recovery | MTTD Target | MTTR Target |
|-------------|-----------|----------------------|----------|-------------|-------------|
| {Failure 1} | {How detected} | {What breaks} | {Auto/Manual — strategy} | {Target} | {Target} |
| {Failure 2} | {How detected} | {What breaks} | {Auto/Manual — strategy} | {Target} | {Target} |
```

### Graceful Degradation Catalog

```
## Capability: {Name}

**Classification:** Critical / Non-Critical
**Normal Behavior:** {What it does when fully healthy}
**Degraded Behavior:** {What happens when dependency fails}
**Trigger:** {What condition activates degradation}
**Recovery:** {How/when normal mode resumes}
**User Impact:** {What the user sees in degraded mode}
```

### Resilience Configuration Summary

```
## Integration: {Service A} → {Service B}

**Timeout:** {value}ms (based on P99: {measured}ms)
**Circuit Breaker:**
- Open after: {N} failures in {T} seconds
- Half-open probe: {N} requests
- Close after: {N} successful probes
**Retry:** {N} attempts, exponential backoff {base}ms, jitter ±{range}ms
**Bulkhead:** Pool size {N}, queue limit {N}
**Fallback:** {Behavior when all else fails}
**Rate Limit:** {N} requests/second per {consumer/tenant}
```
