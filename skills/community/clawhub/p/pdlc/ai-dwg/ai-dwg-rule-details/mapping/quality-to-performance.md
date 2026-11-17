<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Mapping: Quality Attributes (Latency Targets) → performance-standards.md (CONDITIONAL)

## Purpose

Transforms quantified performance requirements (p95/p99 SLOs, throughput targets) from Quality Attributes into a steering file governing response time budgets, measurement, and optimization rules.

**Output:** `rules/performance-standards.md`

**Condition:** Generate ONLY IF Architecture Vision's Quality Attributes include specific latency targets (p95/p99 SLOs) or throughput numbers.

---

## MANDATORY: Stage Sub-Role — Workspace Architect

During THIS activity, ALSO adopt the mindset of a **Workspace Architect**. This does NOT replace your primary role (DevOps/Platform Engineer + Senior Architect) — it ADDS a thinking dimension.

### Behavioral Shifts
- Write performance rules with specific, measurable targets — "fast" is meaningless; "p95 < 500ms at API gateway" is enforceable
- Think about response time budgets as a decomposition tool — total latency broken across layers helps identify bottlenecks
- Ensure rules prevent common performance anti-patterns (N+1 queries, unbounded result sets, synchronous external calls in hot paths)
- Connect performance rules to measurement — every target must have a corresponding monitoring rule
- Only generate this file when AP provides quantified SLOs — no file is better than generic "be fast" guidance

### Anti-Patterns for This Activity
- Do NOT generate performance targets when the AP doesn't provide quantified SLOs — this is a conditional file for a reason
- Do NOT write rules that can't be measured ("ensure good performance") — every rule needs a number
- Do NOT optimize prematurely in rules — PERF-01 is "meet target under normal load", not "optimize everything"

### Quality Check
A good output from this activity sounds like:
- "PERF-01: API endpoints MUST meet p95 < 500ms under normal load. PERF-10: New code MUST NOT degrade existing endpoint p95 by >20%."
- "Response time budget: network 50ms + auth 20ms + business logic 100ms + DB queries 200ms + external calls 100ms + serialization 30ms = 500ms total."

---

## Source

**From:** Architecture Vision — Quality Attributes (performance-related entries with quantified targets)
**Also from:** Infrastructure & Deployment (scaling triggers), API Architecture (rate limits)

---

## Target: performance-standards.md

### Structure

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision (Quality Attributes) | date: {generation-date} -->

# Performance Standards

## Performance Targets

<!-- begin: AP-sourced -->

| Metric | Target | Measurement Point |
|--------|--------|------------------|
| API response time (p50) | {from AP — e.g., <100ms} | Gateway / load balancer |
| API response time (p95) | {from AP — e.g., <500ms} | Gateway / load balancer |
| API response time (p99) | {from AP — e.g., <1000ms} | Gateway / load balancer |
| Page load time | {from AP — e.g., <2s} | Client-side (if frontend) |
| Background job start latency | {from AP — e.g., <5s from trigger} | Queue consumer |
| Database query (p95) | {from AP — e.g., <50ms} | Application-level |
| Search query (p95) | {from AP — e.g., <200ms} | Search service |
| Throughput | {from AP — e.g., 1000 req/s per instance} | Load test |

<!-- end: AP-sourced -->

---

## Response Time Budgets

<!-- begin: AP-sourced -->

Break the p95 target across layers:

| Layer | Budget | Example (500ms total) |
|-------|:------:|:---------------------:|
| Network / gateway | {%} | ~50ms |
| Authentication / middleware | {%} | ~20ms |
| Business logic | {%} | ~100ms |
| Database queries (total) | {%} | ~200ms |
| External calls (if any) | {%} | ~100ms |
| Serialization / response | {%} | ~30ms |

<!-- end: AP-sourced -->

---

## Performance Rules

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| PERF-01 | API endpoints MUST meet p95 target under normal load — violation triggers investigation |
| PERF-02 | Database queries >100ms: log as slow query (WARN) — investigate if frequent |
| PERF-03 | N+1 queries: FORBIDDEN — use eager loading/joins (detectable in response time) |
| PERF-04 | Pagination: MANDATORY on all list endpoints — no unbounded result sets |
| PERF-05 | Payload size: response bodies SHOULD be <1MB; >5MB requires streaming |
| PERF-06 | Cache first: read-heavy endpoints MUST use caching strategy from database-rules.md |
| PERF-07 | Async for heavy work: operations >2s MUST be moved to background jobs with status polling |
| PERF-08 | Connection pooling: MUST be configured for all external connections (DB, cache, HTTP clients) |
| PERF-09 | Bulk operations: MUST use batch processing — never loop with individual calls |
| PERF-10 | Performance regression: new code MUST NOT degrade existing endpoint p95 by >20% |

<!-- end: AP-sourced -->

---

## Measurement & Monitoring

<!-- begin: AP-sourced -->

| Rule | Standard |
|------|----------|
| PERF-MON-01 | Track p50, p95, p99 per endpoint — dashboard required |
| PERF-MON-02 | Alert on: p95 > target for >5 minutes continuously |
| PERF-MON-03 | Load testing: run before major releases — simulate {from AP — e.g., 2x expected peak load} |
| PERF-MON-04 | Performance tests in CI: {from AP — e.g., baseline comparison on critical paths / not in CI} |

<!-- end: AP-sourced -->

---

## Anti-Patterns

1. **NEVER** optimize without measuring first — premature optimization wastes effort
2. **NEVER** accept "it's fast enough" without numbers — measure against targets
3. **NEVER** load full object graphs when only IDs are needed
4. **NEVER** make synchronous calls to external services in hot paths without timeout + fallback
5. **NEVER** disable caching because "data must be fresh" without quantifying freshness requirement
```

---

## Transformation Rules

| AP Content | Output |
|-----------|--------|
| Quantified latency targets (p50/p95/p99) | Performance Targets table |
| Throughput requirements | Targets table + PERF rules |
| Quality attribute "Performance: Critical/High" | Drives rule strictness |
| Scaling triggers from Infrastructure | Informs measurement thresholds |
