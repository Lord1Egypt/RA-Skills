---
name: playwright
slug: playwright
version: 1.0.4
description: >-
  Automates, tests, and debugs browsers with Playwright: locators, auto-waiting, traces, CI runs, and MCP browser control.
  Use when a test is flaky, times out, or fails only in CI or headless; when a locator matches multiple elements or the
  wrong one (strict mode violation); when clicks need force, waits become sleeps, or networkidle never settles; for
  storageState and login setup, request mocking and HAR replay, uploads and downloads, iframes and shadow DOM, popups and
  dialogs, screenshot diffs that change per machine, trace and report artifacts, sharding a slow suite, device and
  permission emulation, accessibility checks, driving a real browser through Playwright MCP, extracting data from
  JS-rendered pages, or porting a Cypress, Puppeteer, or Selenium suite to Playwright. Not for maintaining an existing
  Cypress or Puppeteer suite (cypress, puppeteer) or for work a plain HTTP request answers (http).
homepage: https://clawic.com/skills/playwright
changelog: "Full coverage pass: deeper guides, situation-named files, and per-user configuration"
metadata:
  clawdbot:
    emoji: P
    requires:
      bins:
      - node
      - npx
    os:
    - linux
    - darwin
    - win32
    install:
    - id: npm-playwright
      kind: npm
      package: playwright
      bins:
      - playwright
      label: Install Playwright
    - id: npm-playwright-mcp
      kind: npm
      package: '@playwright/mcp'
      bins:
      - playwright-mcp
      label: Install Playwright MCP (optional)
    displayName: Playwright (Automation + MCP + Scraper)
    configPaths:
    - ~/Clawic/data/playwright/
---

User preferences and memory live in `~/Clawic/data/playwright/` (see `setup.md` on first use). If you have data at an old location (`~/playwright/` or `~/clawic/playwright/`), move it to `~/Clawic/data/playwright/`. Everything a run produces — specs, traces, reports, snapshots, `storageState` files — stays inside the repository or its temp dir, never in the preferences folder: auth state is a credential and belongs in a gitignored path.

## When To Use

- Writing or repairing Playwright specs, fixtures, `playwright.config.ts`, or one-off automation scripts
- A run fails: timeout, strict mode violation, flaky click, passes locally and fails in CI or headless
- Login, session reuse, uploads, downloads, iframes, popups, dialogs, or device emulation are in the way
- Visual snapshots, accessibility checks, trace capture, sharding, or cutting suite wall time
- Driving a live browser through Playwright MCP, or extracting data a plain fetch cannot render
- Porting a Cypress, Puppeteer, or Selenium suite to Playwright, including deciding which tests not to port
- Not for maintaining an existing Cypress or Puppeteer suite (→ `cypress`, `puppeteer`) or for anything an HTTP request already answers (→ `http`)

## Quick Reference

| Situation | Play |
|---|---|
| `strict mode violation: resolved to N elements` | Narrow with `.filter({ hasText })` or a parent chain — never `.nth()` unless position is the behavior under test → `selectors.md` |
| `Timeout 30000ms exceeded waiting for locator` | The locator never matched. Trace it, do not raise the timeout → `debugging.md` |
| `element is not visible` / `intercepts pointer events` | An overlay, animation, or disabled state — `force: true` hides the bug → `waiting.md` |
| Test needs a `waitForTimeout` to pass | Replace with a web-first assertion on the state you were sleeping for → `waiting.md` |
| Green locally, red in CI (or only headless) | Compare viewport, workers, timezone, animations, and browser build → `flake.md`, `ci-cd.md` |
| Passes alone, fails in the suite | Shared account, shared server data, or leaked storage — isolate per worker → `auth.md` |
| Same test red 1 run in 20 | Measure before fixing: `--repeat-each`, then classify by cause → `flake.md` |
| Login repeated in every test | Sign in once in a setup project, reuse `storageState` → `auth.md` |
| A test passes while the feature is broken, or nobody knows what deserves an E2E | What earns a test, outcome assertions, skip and fixme annotations → `testing.md` |
| Writing `playwright.config.ts`, adding a project, a setting that will not apply | Config anatomy, precedence, projects, `webServer`, tags → `config.md` |
| Setup repeated in every test, page objects, or where test data comes from | Test- and worker-scoped fixtures, page-object rules, data strategy → `fixtures.md` |
| Third party, payment sandbox, or slow API in the path | Intercept with `page.route`, or record and replay a HAR → `network.md` |
| Upload, download, PDF, or drag-and-drop | Event-first patterns (`waitForEvent('download')`, `setInputFiles`) → `files.md` |
| New tab, popup, `window.alert`, geolocation, dark mode, offline | Context-level control; dialogs auto-dismiss unless handled → `contexts.md` |
| Screenshot diff passes locally, fails on the runner | Snapshots are per-platform; generate them where CI runs → `visual.md` |
| WCAG or keyboard-navigation coverage | axe scan plus real keyboard assertions → `accessibility.md` |
| Suite takes too long | Measure the slowest tests first, then parallelize or seed via API → `performance.md` |
| Browser missing, wrong channel, WebKit-only failure | Version-locked browsers and engine differences → `browsers.md` |
| Agent should click through a live site now | Snapshot-driven MCP browser control → `mcp.md` |
| Pull data from a JS-rendered page | Bounded extraction with throttling → `scraping.md` |
| Porting from Cypress, Puppeteer, or Selenium | Translation table and the habits to drop → `migration.md` |
| Anything else | Reproduce headed with a trace (`npx playwright test <file> --headed --trace on`), open the trace, and read the DOM snapshot at the failing step |

CLI toolkit: `commands.md`. First-use preference loading: `setup.md`.

## Core Rules

1. **Locate by what the user perceives.** Order: role/label/text → test ID → CSS/XPath. `getByRole('button', { name: 'Submit' })` survives a class rename and a CSS-in-JS rebuild; `.css-1a2b3c` does not. Test IDs are a contract you own — fine, but they assert nothing about accessibility.
2. **Never sleep; assert.** `page.waitForTimeout(500)` is simultaneously too slow on a fast run and too short on a loaded runner. Web-first assertions re-check until the expect timeout (5 s default) and stop the moment the condition holds — strictly faster and strictly more reliable.
3. **Budget the timeouts, do not inflate them.** Defaults: test 30 000 ms, expect 5 000 ms, action and navigation 0 (unbounded, so the test timeout is the real ceiling), `webServer` 60 000 ms. Sizing rule: sum the slowest legitimate path, measured not guessed, and keep the total inside the 30 000 ms default — login 4 s + dashboard render 8 s + one 5 s assertion = 17 s, comfortably inside 30 s. When one step is genuinely slow, raise that assertion's `timeout`, not the global test timeout: a global bump turns every real hang into a 2-minute wait.
4. **One test, one fresh context, one account it owns.** Playwright gives each test a new browser context; that resets cookies and storage but not your database. With N workers, allocate N accounts and index them by `parallelIndex` — sharing one mutable user makes failures order-dependent, and order-dependent failures are unfixable by reading the diff.
5. **Capture before you rewrite.** For any failure you did not cause in the last edit, get a trace first (`trace: 'on-first-retry'`, or `--trace on` for one run). Rewriting a locator against a symptom you never observed is how a two-line bug becomes a rewritten suite.
6. **Retries buy green builds and hide the bill.** A per-test failure probability p across N tests makes a full run red with probability 1 − (1 − p)^N: p = 0.005 across 300 tests → 78% of runs red. Two retries mask that, but the flake is still there and now costs 3× wall time on every occurrence. Keep retries, and track the flaky count as a number that must go down (`flake.md`).
7. **Mock what you do not own; seed through the API, click through the UI only for what is under test.** Creating a user by API and starting the test on the target page removes minutes and removes the upstream service from your failure surface. Exception: the integration itself is the thing being verified.
8. **Treat production and destructive flows as opt-in.** Automating a real payment, deletion, or email send needs the user to say so in this session; default to local or staging. `storageState` files are live credentials — gitignore them and never write one into a shared or synced folder.
9. **Pin the browsers to the Playwright version.** Browser builds ship with the package, so `mcr.microsoft.com/playwright:vX.Y.Z-*` must match the installed `@playwright/test` exactly, and a CI cache key must include that version. A mismatch surfaces as `Executable doesn't exist at .../ms-playwright/...` or, worse, as a silent behavior difference.

## Failure Signatures

Read the first line of the error before anything else; it names the subsystem.

| Message | Real cause | First move |
|---|---|---|
| `strict mode violation: ... resolved to 3 elements` | The locator describes a category, not an element | Filter or chain (`selectors.md`); the error lists the matches — read them |
| `Timeout 30000ms exceeded. waiting for locator(...)` | Never matched: wrong frame, wrong name, not rendered | Trace → DOM snapshot at that step (`debugging.md`) |
| `waiting for element to be visible, enabled and stable` | Matched but not actionable: animation, overlay, `disabled` | `waiting.md` actionability table — not `force: true` |
| `element intercepts pointer events` | Another node covers the target (cookie banner, toast, modal backdrop) | Dismiss it in a fixture; the banner is real user-facing state |
| `Test timeout of 30000ms exceeded while running "beforeEach" hook` | Setup, not the test, is slow or hanging | Move it to a setup project or fixture with its own timeout |
| `Target page, context or browser has been closed` | Action after `close()`, or the process crashed mid-run | Check for a crash in the worker log; in Docker suspect `/dev/shm` (`ci-cd.md`) |
| `Executable doesn't exist at .../ms-playwright/...` | Browsers not installed or version-mismatched | `npx playwright install --with-deps` at the pinned version (rule 9) |
| `net::ERR_CONNECTION_REFUSED` | App not up, wrong port, or `webServer` exited | `webServer` block plus `reuseExistingServer: !process.env.CI` |
| `net::ERR_CERT_AUTHORITY_INVALID` | Self-signed cert on staging or a corporate MITM proxy | `ignoreHTTPSErrors: true` scoped to that project only |
| Screenshot comparison failed, `-linux.png` missing | Snapshots are keyed by platform and project | Generate baselines on the CI platform (`visual.md`) |
| No error, test passes, feature is broken | Asserted on the command, not the outcome | Assert user-visible state (`testing.md`) |

## Isolation Model

What resets, and when — the mental model behind most "it only fails in the suite" bugs.

| Layer | Cost to create | Resets | Leaks across tests |
|---|---|---|---|
| Browser | Expensive; one per worker, reused | Nothing between tests | Yes, by design |
| Context | Cheap; new one per test by default | Cookies, localStorage, sessionStorage, permissions, service workers | No |
| Page | Cheapest; many per context | Nothing (shares the context jar) | Within the test only |
| Worker process | Restarted after a failure and on retry | Worker fixtures re-run | Module-level globals inside one worker |
| Server, database, mailbox | Not managed by Playwright | Nothing | **Yes — this is the real leak** |

Consequences: `fullyParallel: true` runs tests inside one file across workers, so file-level ordering guarantees vanish. `test.describe.serial` restores order but skips the remaining tests on the first failure and re-runs the whole group on retry. A retried test starts in a fresh worker — which is exactly why some flake "fixes itself" on retry and tells you the leak was in-process.

## Output Gates

Before delivering a spec, script, or config:

- Zero `waitForTimeout` used for synchronization and zero `networkidle` waits — each replaced by an assertion on the state being waited for (a politeness delay in extraction is the only exception, `scraping.md`)?
- Every locator resolves to exactly one element, without `.first()`/`.nth()` standing in for a real filter?
- Assertions check user-visible outcomes (text, URL, enabled state, download), not that a call returned?
- No shared mutable account or shared seed data between tests that can run in parallel?
- Trace configured (`on-first-retry` at minimum) and failure artifacts uploaded in CI?
- No credential, token, or `storageState` path committed; production URLs absent unless the user asked for them?
- Runs headless on a clean checkout with browsers installed at the pinned version?

## Configuration

User-dependent variables. Defaults apply until the user states a preference; store them in `~/Clawic/data/playwright/config.yaml`.

| Variable | Type | Default | Effect |
|---|---|---|---|
| language | typescript \| javascript | typescript | Language of every emitted spec, config, and snippet; switches `playwright.config.ts` to `.js` and drops type imports |
| runner_mode | test \| script \| mcp | test | Which path Quick Reference proposes first: `@playwright/test` suite, standalone Playwright script, or MCP browser control |
| default_browsers | list (chromium, firefox, webkit) | chromium | Projects written into config and the engines assumed when diagnosing a failure (`browsers.md`) |
| cross_browser_cadence | pr \| nightly \| release | nightly | Which gate the non-default engines run at: every PR, a scheduled run, or release only — sets the matrix in `browsers.md` and the jobs written in `ci-cd.md` |
| headed_by_default | bool | false | Adds `--headed` to suggested commands and `headless: false` to launch options during exploration |
| test_id_attribute | string | data-testid | Value written to `testIdAttribute` and the attribute `getByTestId` examples use |
| ci_provider | github \| gitlab \| other | github | Which pipeline template `ci-cd.md` guidance is rendered for, including artifact and cache steps |
| scrape_delay_ms | number (0-60000) | 1000 | Minimum gap between page loads in multi-page extraction (`scraping.md` throttling) |

Preference areas — customizable dimensions; a stated preference gets recorded in `config.yaml` and applied:

- **Tooling** — package manager (`npm`/`pnpm`/`yarn`/`bun`) used in every command, UI mode vs CLI, codegen vs hand-written locators
- **Conventions** — spec layout and naming, page-object vs inline fixtures, tag vocabulary (`@smoke`, `@flaky`), assertion style
- **Platform** — browser channels (`chrome`, `msedge`), device emulation set, CI runner OS, official Docker image vs manual browser install
- **Safety posture** — whether non-local base URLs may be automated at all, confirmation before destructive or paid flows, how loudly to flag production targets
- **Flake policy** — retry count in CI, quarantine-and-file vs fix-before-merge, whether a flaky pass fails the build
- **Cadence** — what runs at which gate (PR, nightly, release), how often the `@integration` spec hits the real third party, how long a `@flaky` quarantine may last before the test is fixed or deleted, when a recorded HAR and an accessibility scan are refreshed
- **Extraction posture** — crawl breadth, robots and terms strictness, asset blocking, stop conditions
- **Output format** — reporter set (`list`, `html`, `blob`, `junit`), how much trace and video to retain, verbosity of failure summaries

## Traps

| Trap | Why it fails | Do instead |
|---|---|---|
| `force: true` to get past a failing click | Bypasses the actionability checks that were reporting a real overlay or disabled control — the test goes green while the user stays blocked | Find the blocker in the trace; dismiss banners in a fixture (`waiting.md`) |
| `waitForLoadState('networkidle')` | Analytics beacons, polling, and websockets keep an SPA "busy" forever; the docs discourage it | Assert on the element or response you actually need |
| `.first()` / `.nth(0)` to silence strict mode | Freezes an accidental DOM order; a new promo card at index 0 silently retargets the test | `.filter({ hasText })`, `.filter({ has })`, or scope to a parent |
| `page.$$eval` / `locator.all()` for lists | Neither auto-waits; both snapshot whatever exists at call time, so a slow render yields an empty array and a passing test | `await expect(list).toHaveCount(n)` first, then read |
| `locator.isVisible()` in an `if` | Returns immediately without retrying — the classic "works on my fast machine" conditional | `await expect(locator).toBeVisible()`, or `toBeHidden()` for the negative |
| Storing an `ElementHandle` across a re-render | The handle points at a detached node; locators re-resolve at action time, handles do not | Keep locators in variables; handles only when you need the raw node |
| One `storageState` for every test that mutates data | Parallel workers fight over the same server-side rows | One account per worker indexed by `parallelIndex` (`auth.md`) |
| Building the app's own page objects before any duplication exists | An abstraction layer nobody needed makes every future failure two files away from its cause | Inline first; extract on the third repeat (`fixtures.md`) |
| Locators reaching into an iframe | Locators pierce open shadow DOM but never an iframe boundary | `page.frameLocator(...)` / `locator.contentFrame()` (`selectors.md`) |
| Registering a `dialog` handler and forgetting to respond | The page hangs; without any handler Playwright auto-dismisses, so adding one changes behavior | Always `accept()` or `dismiss()` inside the handler (`contexts.md`) |
| Committing a suite that only passes headed | Headless differs in fonts, media codecs, and window size, and CI has no display | Run headless locally before handing off (`browsers.md`) |
| Driving a full browser to read static HTML | Slower, flakier, and a browser process per request for data a fetch returns | Try the HTTP path first (`scraping.md`, `http`) |

## Where Experts Disagree

- **Test IDs vs semantic locators.** Role and label locators double as an accessibility smoke test and break when the UI genuinely changes for users; test IDs never break and never tell you anything. Default: semantic first, test IDs for elements with no accessible name (icon buttons, list rows, canvas widgets). The boundary is whether the string a locator uses is one a user could perceive.
- **Retries in CI.** Two retries is the scaffolded default and keeps a large suite mergeable; the zero-retry camp argues every masked flake is a real race in the product. Workable line: retries on, flaky count reported and trending down, and no test allowed to stay flaky across two sprints.
- **How many E2E tests.** Pyramid says a handful of journeys; the trophy argues browser tests are the only ones that check what ships. Decide by cost: an E2E test that takes 20 s and catches a class of bug unit tests structurally cannot is worth it; one that re-tests validation logic is not.
- **Agent-driven browsing vs committed automation.** MCP is unbeatable for exploration and one-off tasks and leaves nothing reviewable behind. Anything that must run again next week gets written down as code (`mcp.md`).

## Security & Privacy

| Endpoint | Data sent | Purpose |
|---|---|---|
| Sites the user asks to automate | Navigation, form input, cookies, uploaded files, page interactions | The requested automation, testing, capture, or extraction |
| `https://registry.npmjs.org` | Package metadata and tarballs on install | Install Playwright or Playwright MCP |
| Playwright browser CDN (during `playwright install`) | Browser build downloads | Fetch the version-locked browser binaries |

This skill does NOT: persist sessions or credentials by default; write anything outside the repository except the preferences folder above; recommend fingerprint spoofing, CAPTCHA-solving services, or rotating exits; automate production, payment, or destructive flows without the user asking in the current session; or send page content anywhere beyond the sites involved in the task.

Guardrails: auth artifacts stay in a gitignored path and are never printed into logs or reports; traces and videos can contain tokens and personal data, so treat uploaded CI artifacts as sensitive and cap retention; extraction stays inside the scope the user named.

## Related Skills
More Clawic skills, get them at https://clawic.com/skills/playwright (install if the user confirms):
- `cypress` — the same job in a Cypress codebase
- `puppeteer` — Chrome-only automation without the test runner
- `http` — methods, status codes, headers, and caching when the answer needs no browser at all
- `scrape` — robots, rate limits, and data-handling compliance for larger crawls
- `screenshot` — capture craft beyond test assertions

## Feedback
- If useful, star it: https://clawic.com/skills/playwright
- Latest version: https://clawic.com/skills/playwright

Part of [Clawic](https://clawic.com), the verified skill library. Get this skill: https://clawic.com/skills/playwright.
