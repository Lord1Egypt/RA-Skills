# Benchmark — Integration & Best Practices

## CI Integration

Run `benchmark compare` on every PR to catch regressions early:

```yaml
# .github/workflows/benchmark.yml
name: Performance Benchmark
on: [pull_request]
jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: npm ci
      - run: benchmark compare
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: benchmark-report
          path: .benchmarks/
```

## Pairing with Other Skills

### With Browser QA

Use both for comprehensive pre-ship checks:

1. `browser-qa` — verify UI interactions and accessibility
2. `benchmark` — verify performance meets targets

### With Canary Watch

Deploy to staging with benchmark baseline, then monitor canary deployment:

1. `benchmark baseline` on staging before deploy
2. Deploy to production
3. `canary-watch` monitors live metrics
4. Alert if production metrics regress vs. baseline

## Regression Detection

Common regression patterns to watch:

| Regression | Cause | Fix |
|-----------|-------|-----|
| Bundle size +5% | New dependency | Tree-shake unused exports, use dynamic import |
| LCP +300ms | Render-blocking JS | Defer non-critical scripts |
| API latency +50ms | N+1 query | Batch-load related data, add indexes |
| Build time +1s | New TypeScript project | Use `skipLibCheck: true` in tsconfig |
| Test time +30s | New test file | Parallelize with `jest --maxWorkers=4` |

## Target Values

### Web Vitals (Google standards)

- **Good**: LCP < 2.5s, CLS < 0.1, INP < 200ms
- **Needs Work**: LCP 2.5-4s, CLS 0.1-0.25, INP 200-500ms
- **Poor**: LCP > 4s, CLS > 0.25, INP > 500ms

### API SLAs

- **p50**: target < 50ms
- **p95**: target < 200ms
- **p99**: target < 500ms

### Build Targets

- **Cold build**: < 60s
- **HMR**: < 2s
- **Tests**: < 5min for full suite
- **Type check**: < 30s
