# Config — playwright.config.ts, Projects, and Run Shape

Everything that decides what runs, where, and in what order. Fixtures and page objects: `fixtures.md`. What deserves a test at all: `testing.md`.

## Config Anatomy

```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests',
  fullyParallel: true,                       // default is false: files run serially in one worker
  forbidOnly: !!process.env.CI,              // a committed test.only silently skips the suite
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,   // undefined = half the logical cores
  globalTimeout: 30 * 60_000,                // a hung job dies here instead of at the provider limit
  reporter: process.env.CI ? [['blob'], ['github']] : [['html']],
  use: {
    baseURL: process.env.BASE_URL ?? 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    testIdAttribute: 'data-testid',
  },
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,    // locally attach to a running server; in CI always start clean
    timeout: 60_000,
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
  ],
});
```

- `baseURL` makes every `goto('/checkout')` relative — one env var repoints the whole suite at staging.
- `forbidOnly` is the cheapest guard in the file: without it, one committed `.only` turns a 400-test gate into a 1-test gate that still shows green.
- `testIdAttribute` is the only place `getByTestId` reads its attribute name from; changing it in one project and not another produces locators that work in half the matrix.

## Option Precedence

Innermost wins: `test.use()` inside a file or `describe` > the project's `use` > the top-level `use` > the Playwright default. When a setting appears not to apply, read outward from the test, not inward from the config — the override is almost always closer to the test than you expect.

Command-line flags (`--workers`, `--project`, `--grep`, `--headed`) beat all of them for one run and change nothing on disk.

## Projects Are For Dimensions, Not Folders

```typescript
projects: [
  { name: 'setup', testMatch: /global\.setup\.ts/ },
  { name: 'chromium', dependencies: ['setup'], use: { ...devices['Desktop Chrome'], storageState: '.auth/user.json' } },
  { name: 'mobile', dependencies: ['setup'], use: { ...devices['Pixel 7'], storageState: '.auth/user.json' } },
  { name: 'teardown', testMatch: /global\.teardown\.ts/ },
]
```

Use projects for browsers, devices, auth roles, and environments. `dependencies` gives ordered phases (setup runs to completion before dependents start); `teardown` on a project runs after its dependents finish. Do not use projects to group by feature — that is what `--grep` and tags are for.

A project is also the unit of cadence: which projects run on a PR versus a nightly is the `cross_browser_cadence` decision (`browsers.md` matrix), and `--project=chromium` is how the PR job spends one third of the time.

## The webServer Block

- `url` polls until the server answers; use `port` only when the server picks a path you cannot predict. A `url` that returns 404 still counts as up — point it at a route that exists.
- `reuseExistingServer: !process.env.CI` is the local-development half: attach to the dev server already in your terminal, start a clean one in CI. Without it, every local run either fails on a busy port or races your own server.
- `timeout: 60_000` covers a cold compile; a dev server that needs longer is the reason a first test times out on a loaded machine.
- If the command exits, the run aborts with the server's own output — read that before suspecting the tests.
- CI serves a production build instead, with readiness checks and `BASE_URL` for deployed environments (`ci-cd.md`).

## Parallelism Controls

```typescript
test.describe.configure({ mode: 'serial' });   // ordered, and a failure SKIPS the rest of the group
test.describe.configure({ mode: 'parallel' }); // spread across workers even without fullyParallel
test.describe.configure({ retries: 0 });       // per-group override
```

Serial mode is a last resort: it converts one failure into a block of skipped tests and re-runs the whole group on retry. Prefer independent tests with per-test setup.

## Tags And Selective Runs

```typescript
test('checkout @smoke', ...);
test('admin panel', { tag: '@slow' }, ...);
```

```bash
npx playwright test --grep @smoke          # PR gate
npx playwright test --grep-invert @slow    # everything but the long tail
```

Tag vocabulary worth having from day one: `@smoke` (must pass on every PR), `@slow`, `@flaky` (quarantined, `flake.md`), `@integration` (hits a real third party, so it runs on a schedule rather than on every PR).
