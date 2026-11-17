# Performance — Suite Wall Time and Page Metrics

Two different jobs share one word. First: make the suite fast enough that people run it. Second: use Playwright to measure the app itself.

## Find The Time Before Spending It

```bash
npx playwright test --reporter=list          # per-test durations in the console
npx playwright show-report                   # sortable durations, slowest first
```

The HTML report's duration column is the whole diagnosis. Typical distribution in a slow suite: a handful of tests hold most of the wall time, and inside them the top costs are UI login, `waitForTimeout`, and real third-party latency — in that order.

Optimize in this sequence; each step is cheaper than the next:

| Step | Typical saving | Cost |
|---|---|---|
| 1. Delete sleeps | Their full duration, every run | Minutes of edits |
| 2. Skip UI login (API session, `storageState`) | The login flow × every test | An hour once (`auth.md`) |
| 3. Seed data by API instead of clicking | Multi-step setup per test | Needs an API |
| 4. Mock third parties | Their latency and their outages | Fixtures to maintain |
| 5. Raise parallelism (`fullyParallel`, workers) | Divides wall time | Requires real isolation |
| 6. Shard across machines | Divides again | CI complexity (`ci-cd.md`) |
| 7. Delete tests that assert nothing unique | Their full duration | Judgment |

Doing 5 before 1-4 is the classic mistake: parallelizing a suite full of shared state converts slowness into flakiness.

## Parallelism Math

Wall time ≈ (total test time ÷ workers) + fixed overhead. Overhead is browser launch per worker, `webServer` startup, and install. A 20-minute suite on 4 workers lands near 5-6 minutes, not 5 — and going from 8 to 16 workers on a 4-core runner makes it slower, because the workers compete for CPU and every actionability check starts missing its window.

Sizing rule: the default is half the logical cores; raising it toward the core count helps only while memory holds (a Chromium context under load is comfortably in the hundreds of megabytes; a 2 GB runner will not host 8). If timeouts appear as you raise workers, you have passed the limit.

## Cheap Wins

```typescript
// Kill asset traffic in tests that do not assert visuals
await page.route('**/*.{png,jpg,jpeg,gif,woff,woff2,mp4}', r => r.abort());

// Reuse one context in a plain script instead of launching a browser per job
const browser = await chromium.launch();
const context = await browser.newContext();

// Start where the test begins, not at the homepage
await page.goto('/checkout?cart=seeded');
```

Also: `trace: 'on'` records everything on every run and slows the suite; `'on-first-retry'` costs nothing on green. Video is heavier still — `retain-on-failure` only.

## Measuring The App

```typescript
const nav = JSON.parse(await page.evaluate(() =>
  JSON.stringify(performance.getEntriesByType('navigation')[0])));
expect(nav.domContentLoadedEventEnd).toBeLessThan(3000);

const lcp = await page.evaluate(() => new Promise<number>(resolve => {
  new PerformanceObserver(list => {
    const entries = list.getEntries();
    resolve(entries[entries.length - 1].startTime);
  }).observe({ type: 'largest-contentful-paint', buffered: true });
}));
```

Caveats that decide whether the number means anything:

- A CI runner's timings are noisy and machine-dependent. Track **trends and relative regressions** on identical hardware, never an absolute threshold copied from a blog post.
- Headless and unthrottled is a best case no user experiences. Throttle deliberately (below) or state the assumption.
- Lab numbers are not field numbers: use them to catch regressions, use real-user monitoring to know what users get.

## Throttling

```typescript
const cdp = await context.newCDPSession(page);       // Chromium only
await cdp.send('Network.emulateNetworkConditions', {
  offline: false, downloadThroughput: 1.5 * 1024 * 1024 / 8,
  uploadThroughput: 750 * 1024 / 8, latency: 40,
});
await cdp.send('Emulation.setCPUThrottlingRate', { rate: 4 });
```

CPU throttling is the more revealing of the two for modern SPAs — a 4× slowdown approximates a mid-range phone and surfaces races that a fast laptop hides. It doubles as a flake detector: a test that fails under 4× throttling has a timing assumption baked into it (`flake.md`).

## Budgets That Hold

- Assert on the slowest reasonable case with headroom, not the median: `expect(duration).toBeLessThan(p95Observed * 1.3)`.
- Fail on a **regression** (this build vs the last N on the same runner), not on a fixed millisecond count — fixed budgets get raised until they mean nothing.
- Keep performance specs in their own project with `workers: 1`; measuring while three other browsers compete for CPU produces numbers that describe the runner, not the app.
