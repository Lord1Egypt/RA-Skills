---
name: performance-benchmark
description: "Measure performance baselines, detect regressions, and compare stack alternatives before/after changes. Modes: page performance (Core Web Vitals), API latency, build speed, before/after comparison. Trigger phrases: benchmark, performance baseline, regression test, measure latency."
metadata: {"clawdbot":{"emoji":"⏱️","requires":{"bins":[],"env":[]},"os":["linux","darwin","win32"]}}
---

# Benchmark — Performance Baseline & Regression Detection

Measure performance impact of code changes and set baselines for your project.

## Quick Start

**Required:** Bring your own benchmark tool (e.g. k6 for load testing, autocannon for API benchmarks, hyperfine for build speed).

1. Run baseline: `benchmark baseline` — captures current metrics
2. Make changes to your code
3. Run comparison: `benchmark compare` — measures impact against baseline
4. Review report: tracks deltas for Web Vitals, bundle size, build time, API latency

⚠️ **Safety Warning:** Load tests should not be run against production systems without explicit authorization from your team. Test against staging or local environments only.

## Key Concepts

- **Page Performance**: Core Web Vitals (LCP, CLS, INP, TTFB) and resource sizes
- **API Performance**: p50/p95/p99 latency under load
- **Build Performance**: cold build, hot reload (HMR), test suite, type-check, lint times
- **Before/After**: Compare metrics against stored baseline to detect regressions

## Common Usage

### Page Performance Metrics

```text
Measures on real browser:
- LCP (Largest Contentful Paint) — target < 2.5s
- CLS (Cumulative Layout Shift) — target < 0.1
- INP (Interaction to Next Paint) — target < 200ms
- TTFB (Time to First Byte) — target < 800ms
- Total page weight (target < 1MB)
- JS bundle (target < 200KB gzipped)
- Network requests count
```

### API Performance

```text
Hit each endpoint 100 times:
- p50, p95, p99 latency
- Response size, status codes
- Load test: 10 concurrent requests
- Compare against SLA targets
```

### Build Performance

```text
Measures development feedback loop:
- Cold build time
- Hot reload time (HMR)
- Test suite duration
- TypeScript check time
- Lint time
- Docker build time
```

### Output Format
Reports saved to `.benchmarks/` (git-tracked):
| Metric | Before | After | Delta | Verdict |
|--------|--------|-------|-------|---------|
| LCP | 1.2s | 1.4s | +200ms | ⚠ WARN |
| Bundle | 180KB | 175KB | -5KB | ✓ BETTER |

## References

- `references/integration.md` — CI/CD setup, pairing with canary-watch and browser-qa
- `references/modes.md` — detailed explanation of each measurement mode

---

**Adapted from everything-claude-code by @affaan-m (MIT)**
