<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: resilience-standards.md (CONDITIONAL)

**Generate IF:** >3 external integrations OR distributed system OR Microservices/Resilience extension active.

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Integration Architecture | date: {generation-date} -->

# Resilience Standards

## Model
**Approach:** {defensive integration with circuit breakers}
**Library:** {tool}

## Timeouts
<!-- begin: AP-sourced -->
| Type | Timeout | Rule |
|------|:-------:|------|
| Internal API | {n}s | RES-TO-01 |
| External API | {n}s | RES-TO-02 |
| Database | {n}s | RES-TO-03 |
| Background job | {n}min | RES-TO-04 |
| Request deadline | {n}s | RES-TO-05 |
<!-- end: AP-sourced -->

## Retry Policies
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| RES-RTY-01 | Retry ONLY idempotent operations |
| RES-RTY-02 | Retry on: timeout, 503, 429 |
| RES-RTY-03 | No retry on: 400, 401, 403, 404, 422 |
| RES-RTY-04 | Max: {n} attempts |
| RES-RTY-05 | Backoff: exponential + jitter |
| RES-RTY-06 | After max: fail with clear error |
<!-- end: AP-sourced -->

## Circuit Breaker
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| RES-CB-01 | Applied to: {scope} |
| RES-CB-02 | Open threshold: {n} failures in {n}s |
| RES-CB-03 | Half-open: {n} request after {n}s |
| RES-CB-04 | Reset: {n} successes in half-open |
| RES-CB-05 | When open: fallback or fail fast |
| RES-CB-06 | Log state changes at WARN |
<!-- end: AP-sourced -->

## Fallback & Degradation
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| RES-FB-01 | Every external dep has fallback |
| RES-FB-02 | Options: cached/default/partial/error |
| RES-FB-03 | Degradation visible to user |
| RES-FB-04 | Core ops complete without non-critical deps |
<!-- end: AP-sourced -->

## Dead Letter
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| RES-DL-01 | Failed messages → DLQ after {n} attempts |
| RES-DL-02 | Preserve payload + failure reason |
| RES-DL-03 | Alert on DLQ depth > {n} |
| RES-DL-05 | Never auto-replay without review |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/integration-to-resilience.md`.
