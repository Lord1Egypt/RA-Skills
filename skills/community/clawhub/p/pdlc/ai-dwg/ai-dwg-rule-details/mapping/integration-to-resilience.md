<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Integration Architecture (Failure Handling) → resilience-standards.md (CONDITIONAL)

## Purpose

Transforms failure handling patterns from the Integration Architecture into a steering file governing retry policies, circuit breakers, timeouts, and graceful degradation.

**Output:** `rules/resilience-standards.md`

**Condition:** Generate IF Integration Architecture shows >3 external integrations OR system is distributed (microservices) OR Microservices/Resilience extension was active in AI-ADLC.

---

## MANDATORY: Stage Sub-Role — API Designer

During THIS activity, ALSO adopt the mindset of an **API Designer**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Think about failure as the normal state — external systems WILL go down; the question is how gracefully the system handles it
- Design resilience patterns per-integration, not globally — different integrations have different failure profiles and SLAs
- Ensure every external dependency has a defined fallback behavior — "it fails and we show an error" is not graceful degradation
- Write retry rules that prevent harm — retrying non-idempotent operations creates duplicates; retrying without backoff creates cascading failures
- Consider resource exhaustion — circuit breakers and bulkheads protect the system from one failing dependency starving others

### Anti-Patterns for This Activity
- Do NOT write generic "use circuit breakers" advice — specify thresholds, timeouts, and half-open behaviors from the AP
- Do NOT assume all integrations need the same resilience pattern — tailor retry counts and fallbacks per integration criticality
- Do NOT forget dead letter handling — unprocessable messages are lost business operations if not tracked

### Quality Check
A good output from this activity sounds like:
- "RES-CB-02: Circuit breaker opens after 5 failures in 60 seconds. Half-open after 30s allows 1 probe request. 3 successes resets to closed."
- "RES-FB-01: Every external dependency MUST define a fallback: cached data / default value / partial response / degraded feature / error with explanation."

---

## Source

**From:** Integration Architecture — failure handling section (retry, circuit breaker, dead letter patterns)
**Also from:** Infrastructure & Deployment (HA, failover), Technology Stack (resilience libraries)

---

## Target: resilience-standards.md

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Integration Architecture | date: {generation-date} -->

# Resilience Standards

## Resilience Model

**Approach:** {from AP — e.g., Defensive integration with circuit breakers on all external calls}
**Library:** {from AP — e.g., built-in retry decorators / Polly / resilience4j / custom}

---

## Timeout Policies

<!-- begin: AP-sourced -->

| Integration Type | Timeout | Rule |
|-----------------|:-------:|------|
| Synchronous API calls (internal) | {from AP — e.g., 5s} | RES-TO-01: All internal HTTP calls MUST have timeout configured |
| Synchronous API calls (external) | {from AP — e.g., 10s} | RES-TO-02: External calls get longer timeout but MUST have one |
| Database queries | {from AP — e.g., 30s} | RES-TO-03: Kill queries exceeding timeout |
| Background job execution | {from AP — e.g., 5min} | RES-TO-04: Jobs MUST have max execution time |
| Overall request deadline | {from AP — e.g., 30s} | RES-TO-05: No request may exceed overall deadline regardless of downstream timeouts |

<!-- end: AP-sourced -->

---

## Retry Policies

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| RES-RTY-01 | Retry ONLY idempotent operations — NEVER retry non-idempotent writes without idempotency key |
| RES-RTY-02 | Retry on: network timeout, 503, 429 (after Retry-After), connection reset |
| RES-RTY-03 | DO NOT retry on: 400, 401, 403, 404, 409, 422 (client errors = won't succeed on retry) |
| RES-RTY-04 | Max retries: {from AP — e.g., 3 attempts total (1 initial + 2 retries)} |
| RES-RTY-05 | Backoff: {from AP — e.g., exponential with jitter (100ms, 200ms, 400ms + random 0-100ms)} |
| RES-RTY-06 | After max retries exhausted: fail with clear error + log all attempt results |
| RES-RTY-07 | Retry budget: {from AP — e.g., no more than 20% of total traffic should be retries} |

<!-- end: AP-sourced -->

---

## Circuit Breaker

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| RES-CB-01 | Circuit breaker on: {from AP — e.g., all external HTTP integrations + database connections} |
| RES-CB-02 | Failure threshold to OPEN: {from AP — e.g., 5 failures in 60 seconds} |
| RES-CB-03 | Half-open: allow {from AP — e.g., 1 request} through after {from AP — e.g., 30 seconds} |
| RES-CB-04 | Reset to CLOSED: after {from AP — e.g., 3 successful requests in half-open state} |
| RES-CB-05 | When OPEN: return fallback response OR fail fast with 503 — NEVER queue/block indefinitely |
| RES-CB-06 | Circuit state changes: log at WARN level with integration name and state transition |

<!-- end: AP-sourced -->

---

## Fallback & Graceful Degradation

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| RES-FB-01 | Every external dependency MUST define a fallback behavior when unavailable |
| RES-FB-02 | Fallback options (choose per integration): cached data / default value / partial response / degraded feature / error with explanation |
| RES-FB-03 | Degradation MUST be visible: indicate to user when data is stale or feature degraded |
| RES-FB-04 | Core business operations MUST complete even if non-critical integrations are down |
| RES-FB-05 | Feature flags: {from AP — e.g., disable non-essential integrations via configuration when unstable} |

<!-- end: AP-sourced -->

---

## Bulkhead (If Applicable)

<!-- begin: AP-sourced -->

{Include if AP mentions bulkhead / resource isolation between integrations}

| Rule | Standard |
|------|----------|
| RES-BH-01 | Separate thread/connection pools per external integration — failure in one MUST NOT exhaust resources for others |
| RES-BH-02 | Pool size per integration: {from AP — e.g., max 10 concurrent calls to any single external service} |
| RES-BH-03 | When pool exhausted: reject immediately with 503 — do not queue unbounded |

<!-- end: AP-sourced -->

---

## Dead Letter / Poison Message

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| RES-DL-01 | Messages that fail processing after {from AP — e.g., 3} attempts → move to dead letter queue |
| RES-DL-02 | Dead letter messages: preserve original payload + failure reason + attempt history |
| RES-DL-03 | Dead letter monitoring: alert when DLQ depth > {from AP — e.g., 10 messages} |
| RES-DL-04 | Dead letter resolution: manual review → fix → replay OR discard with documentation |
| RES-DL-05 | NEVER auto-replay dead letter messages without human review |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **NEVER** retry without backoff — hammering a failing service makes it worse
2. **NEVER** retry non-idempotent operations — creates duplicates
3. **NEVER** set infinite timeout — always configure explicit deadline
4. **NEVER** let one failing integration block the entire request — use circuit breakers + fallbacks
5. **NEVER** ignore dead letter messages — they represent lost business operations
6. **NEVER** hide degradation from users — be transparent about stale/partial data
```

---

## Transformation Rules

| AP Content | Output |
|-----------|--------|
| Timeout values per integration type | RES-TO rules |
| Retry strategy (attempts, backoff) | RES-RTY rules |
| Circuit breaker configuration | RES-CB rules |
| Fallback behavior definitions | RES-FB rules |
| Bulkhead/isolation patterns | RES-BH rules (if applicable) |
| Dead letter queue strategy | RES-DL rules |
