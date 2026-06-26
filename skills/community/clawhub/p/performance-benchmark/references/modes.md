# Benchmark Modes — Detailed Reference

## Mode 1: Page Performance (Browser)

Measures real browser metrics:

1. Navigate to target URL
2. Measure Core Web Vitals:
   - LCP (Largest Contentful Paint) — target < 2.5s
   - CLS (Cumulative Layout Shift) — target < 0.1
   - INP (Interaction to Next Paint) — target < 200ms
   - FCP (First Contentful Paint) — target < 1.8s
   - TTFB (Time to First Byte) — target < 800ms
3. Measure resource sizes:
   - Total page weight (target < 1MB)
   - JS bundle size (target < 200KB gzipped)
   - CSS size
   - Image weight
   - Third-party script weight
4. Count network requests
5. Check for render-blocking resources

## Mode 2: API Performance

Benchmarks API endpoints:

1. Hit each endpoint 100 times
2. Measure: p50, p95, p99 latency
3. Track: response size, status codes
4. Test under load: 10 concurrent requests
5. Compare against SLA targets

## Mode 3: Build Performance

Measures development feedback loop:

1. Cold build time
2. Hot reload time (HMR)
3. Test suite duration
4. TypeScript check time
5. Lint time
6. Docker build time

## Mode 4: Before/After Comparison

Run before and after a change:

```bash
benchmark baseline    # saves current metrics
# ... make changes ...
benchmark compare     # compares against baseline
```

Output shows deltas:

- Green (✓) = improvement
- Yellow (⚠) = regression
- Red (✗) = significant regression

## Storage

Baselines stored in `.benchmarks/` as JSON. Git-tracked so the team shares baselines and can track historical performance trends.
