# CI — Pipelines, Sharding, Artifacts

A Playwright job has four jobs of its own: install the right browsers, start the app, run the suite deterministically, and leave behind evidence when it fails.

Contents: [GitHub Actions](#github-actions) · [GitLab CI](#gitlab-ci) · [Docker](#docker) · [Caching Browsers](#caching-browsers) · [Sharding](#sharding) · [Serving The App](#serving-the-app) · [Gates And Cadence](#gates-and-cadence) · [Config Recommendations For CI](#config-recommendations-for-ci) · [Debugging A CI-Only Failure](#debugging-a-ci-only-failure)

## GitHub Actions

```yaml
name: e2e
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 30
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: 20, cache: npm }
      - run: npm ci
      - name: Install Playwright browsers
        run: npx playwright install --with-deps chromium
      - run: npx playwright test
        env:
          BASE_URL: http://localhost:3000
      - uses: actions/upload-artifact@v4
        if: ${{ !cancelled() }}
        with:
          name: playwright-report
          path: playwright-report/
          retention-days: 7
```

- `if: ${{ !cancelled() }}` beats `if: failure()`: flaky-but-passed runs still upload the trace that explains the flake.
- `timeout-minutes` on the job plus `globalTimeout` in the config: two independent brakes on a hung run.
- Install only the browsers the projects use; installing all three roughly triples download time for nothing.

## GitLab CI

```yaml
e2e:
  image: mcr.microsoft.com/playwright:v1.XX.Y-noble   # must equal the installed @playwright/test
  script:
    - npm ci
    - npx playwright test
  artifacts:
    when: always
    paths: [playwright-report/, test-results/]
    expire_in: 7 days
```

## Docker

```dockerfile
FROM mcr.microsoft.com/playwright:v1.XX.Y-noble
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
CMD ["npx", "playwright", "test"]
```

Run with `--ipc=host`, or `--shm-size=1gb`. Docker's default `/dev/shm` is **64 MB**, and Chromium exhausting it produces tab crashes that surface as `Target page, context or browser has been closed` — the single most common containerized Playwright failure. `--disable-dev-shm-usage` is the alternative when you cannot change the run flags.

The image tag must match the installed Playwright version exactly (`browsers.md`).

## Caching Browsers

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/ms-playwright
    key: pw-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
```

The key must change when Playwright does — hashing the lockfile achieves that. A cache keyed only on the OS serves stale browsers after every upgrade and produces the "executable doesn't exist" error at random. Note that a cache hit still needs `install-deps` on a bare runner for the system libraries.

## Sharding

```yaml
strategy:
  fail-fast: false
  matrix:
    shard: [1, 2, 3, 4]
steps:
  - run: npx playwright test --shard=${{ matrix.shard }}/4 --reporter=blob
  - uses: actions/upload-artifact@v4
    with: { name: blob-${{ matrix.shard }}, path: blob-report/ }
```

```yaml
merge:
  needs: test
  if: ${{ !cancelled() }}
  steps:
    - uses: actions/download-artifact@v4
      with: { pattern: blob-*, path: all-blobs, merge-multiple: true }
    - run: npx playwright merge-reports --reporter=html ./all-blobs
```

- The blob reporter plus `merge-reports` is what makes sharding usable: without it you get four disconnected reports and no single verdict.
- Shards split the test list deterministically, not by duration, so a shard holding the slow tests finishes last — balance by moving slow specs, not by adding shards.
- `fail-fast: false` or one red shard cancels the others and destroys the evidence.
- Shard only a suite that is already deterministic: four parallel copies of a flaky suite quadruple the chance of a red run (`flake.md`).

## Serving The App

```typescript
webServer: {
  command: 'npm run start',              // a production build, not the dev server
  url: 'http://localhost:3000',
  reuseExistingServer: !process.env.CI,
  timeout: 60_000,
  stdout: 'pipe',                        // server logs land in the report on failure
}
```

Dev servers recompile on demand, so the first test in each area pays a multi-second compile and times out on a cold, loaded runner. Build once, serve the build.

Testing a deployed environment instead: set `BASE_URL`, drop `webServer`, and add a readiness check — a deploy that is still rolling out fails the whole suite on the first navigation.

## Gates And Cadence

Not everything belongs on every push. Split the suite by gate, and let the schedule carry what a PR cannot afford:

```yaml
on:
  pull_request:
  schedule: [{ cron: '0 3 * * *' }]      # the wider matrix runs while nobody waits for it
```

| Gate | What runs | Blocking |
|---|---|---|
| PR | Default engine, `--grep-invert "@flaky\|@slow\|@integration"` | Yes — this is the merge signal |
| Quarantine | `--grep @flaky` on the same commit | No — coverage kept, red ignored (`flake.md`) |
| Nightly | Every engine in `cross_browser_cadence`, plus `@slow` | No, but a red nightly opens an issue |
| Integration | `--grep @integration` against real sandboxes | No — third-party downtime must not block merges |
| Release | Branded `chrome`/`msedge` channels, mobile projects, visual baselines | Yes, on the release branch |

Cadence is a preference, not a constant: `cross_browser_cadence` (default `nightly`) decides where Firefox and WebKit run, and a team shipping Safari-critical features moves them into the PR gate and pays the time. Two dated artifacts need their own schedule regardless: recorded HARs (`network.md`) and accessibility baselines (`accessibility.md`) both pass forever against a fossil.

## Config Recommendations For CI

| Setting | Value | Why |
|---|---|---|
| `retries` | 2 | Absorbs infrastructure noise; the flaky count stays visible (`flake.md`) |
| `workers` | 1 on a 2-core runner, cores/2 on a bigger one | Over-subscribing a shared runner creates timeouts that look like product bugs |
| `forbidOnly` | `!!process.env.CI` | A committed `.only` otherwise greens the gate with one test |
| `trace` | `on-first-retry` | Evidence for every flake, no cost on green runs |
| `reporter` | `[['blob'], ['github']]` sharded, `[['html']]` otherwise | Blob is required for merging |
| `globalTimeout` | 20-30 min | Kills a hung run before the provider does |

## Debugging A CI-Only Failure

1. Download the artifact and open the trace locally — the whole run is in that file.
2. Reproduce in the CI image: `docker run --rm -it -v $PWD:/app -w /app mcr.microsoft.com/playwright:v1.XX.Y-noble npx playwright test`.
3. Match the environment: same viewport, `TZ`, locale, worker count.
4. Still green locally? It is load or ordering: `--workers=<ci value> --repeat-each=5` (`flake.md`).
