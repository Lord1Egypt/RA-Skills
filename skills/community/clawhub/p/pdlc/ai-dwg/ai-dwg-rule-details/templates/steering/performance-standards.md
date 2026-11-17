<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-DWG
generatedVersion: "{version}"
source: "{upstream-ap-artifact}"
generatedOn: "{generation-date}"
ownership: hybrid
---
# Template: performance-standards.md (CONDITIONAL)

**Generate IF:** Quality Attributes include specific latency targets (p95/p99 SLOs).

```markdown
---
inclusion: always
---

<!-- AI-DWG generated | source: Architecture Vision (Quality Attributes) | date: {generation-date} -->

# Performance Standards

## Targets
<!-- begin: AP-sourced -->
| Metric | Target | Measurement |
|--------|--------|-------------|
| API p50 | {target} | Gateway |
| API p95 | {target} | Gateway |
| API p99 | {target} | Gateway |
| DB query p95 | {target} | App-level |
| Throughput | {target} | Load test |
<!-- end: AP-sourced -->

## Response Time Budgets
<!-- begin: AP-sourced -->
| Layer | Budget |
|-------|:------:|
| Network/gateway | {ms} |
| Auth/middleware | {ms} |
| Business logic | {ms} |
| Database | {ms} |
| External calls | {ms} |
<!-- end: AP-sourced -->

## Rules
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| PERF-01 | Meet p95 under normal load |
| PERF-02 | Slow queries >100ms: WARN |
| PERF-03 | N+1 FORBIDDEN |
| PERF-04 | Pagination mandatory |
| PERF-05 | Responses <1MB |
| PERF-06 | Cache read-heavy endpoints |
| PERF-07 | >2s operations → background job |
| PERF-08 | Connection pooling required |
| PERF-09 | Bulk: batch processing |
| PERF-10 | No >20% regression |
<!-- end: AP-sourced -->

## Monitoring
<!-- begin: AP-sourced -->
| Rule | Standard |
|------|----------|
| PERF-MON-01 | Track p50/p95/p99 per endpoint |
| PERF-MON-02 | Alert: p95 > target for >5 min |
| PERF-MON-03 | Load test before major releases |
<!-- end: AP-sourced -->
```

## Filling: Refer to `mapping/quality-to-performance.md`.
