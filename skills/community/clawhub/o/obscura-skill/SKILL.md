---
name: obscura
description: Use when scraping the web, driving headless browser automation, or running E2E tests from Claude Code. Obscura is a Rust-based, drop-in headless Chrome replacement (~30 MB) compatible with Puppeteer and Playwright via the Chrome DevTools Protocol. Trigger when the user mentions web scraping, headless browser, Puppeteer/Playwright, anti-bot/anti-detection, CDP, JS rendering, parallel page fetching, E2E tests for a React/Vue/Next/SPA frontend, or `obscura`/`obscura serve`/`obscura fetch`.
---

# Obscura — Headless Browser for AI Agents and Web Scraping

> **Source:** https://github.com/h4ckf0r0day/obscura
> **License:** Apache 2.0

## Overview

Obscura is an open-source headless browser engine written in Rust. It runs real
JavaScript via V8, speaks the Chrome DevTools Protocol, and works as a
drop-in replacement for headless Chrome with Puppeteer and Playwright — but
uses ~30 MB of memory instead of 200+ MB and starts instantly.

Use this skill whenever you need to:

- Scrape JavaScript-heavy pages from the CLI
- Drive Puppeteer or Playwright scripts without bundling Chromium
- Spin up a CDP server for an AI agent to control
- Defeat trivial bot-detection (built-in stealth + tracker blocking)
- Parallel-fetch many URLs with low memory overhead

## When to Use

| Trigger | Action |
|---|---|
| User wants to scrape one URL with JS rendering | `obscura fetch <url>` |
| User wants to scrape many URLs in parallel | `obscura scrape url1 url2 ...` |
| User has a Puppeteer/Playwright script | Start `obscura serve` and connect via CDP |
| Page is bot-protected | Add `--stealth` |
| User asks about anti-detect / fingerprinting | Recommend stealth build |

## Installation

### macOS (Apple Silicon)

```bash
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-aarch64-macos.tar.gz
tar xzf obscura-aarch64-macos.tar.gz
sudo mv obscura /usr/local/bin/
obscura --version
```

### macOS (Intel)

```bash
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-macos.tar.gz
tar xzf obscura-x86_64-macos.tar.gz
sudo mv obscura /usr/local/bin/
```

### Linux x86_64

```bash
curl -LO https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux.tar.gz
tar xzf obscura-x86_64-linux.tar.gz
sudo mv obscura /usr/local/bin/
```

### Windows

Download the `.zip` from the [Releases](https://github.com/h4ckf0r0day/obscura/releases)
page and extract it. Add the binary to `PATH`.

### Build from source (with stealth)

```bash
git clone https://github.com/h4ckf0r0day/obscura.git
cd obscura
cargo build --release --features stealth
# Binary: ./target/release/obscura
```

Requires Rust 1.75+ ([rustup.rs](https://rustup.rs)). First build takes ~5 min
because V8 compiles from source — subsequent builds are cached.

### Verify

```bash
obscura fetch https://example.com --eval "document.title"
# Expected output: "Example Domain"
```

## Usage

### 1. Fetch a single page

```bash
# Get the page title
obscura fetch https://example.com --eval "document.title"

# Dump the rendered HTML (after JS executes)
obscura fetch https://news.ycombinator.com --dump html

# Dump only the links
obscura fetch https://example.com --dump links

# Dump plain text
obscura fetch https://example.com --dump text

# Wait for network to be idle before reading
obscura fetch https://example.com --wait-until networkidle0

# Wait for a specific element
obscura fetch https://example.com --selector ".article-body"
```

`--dump` accepts: `html`, `text`, `links`.
`--wait-until` accepts: `load`, `domcontentloaded`, `networkidle0`.

### 2. Scrape many URLs in parallel

```bash
obscura scrape \
  https://example.com/page-1 \
  https://example.com/page-2 \
  https://example.com/page-3 \
  --concurrency 25 \
  --eval "document.querySelector('h1').textContent" \
  --format json
```

`--format` accepts: `json` or `text`. Use `json` when piping into `jq`.

### 3. Start a CDP server for Puppeteer / Playwright

```bash
obscura serve --port 9222

# With anti-detection + tracker blocking
obscura serve --port 9222 --stealth

# Through an HTTP/SOCKS5 proxy
obscura serve --port 9222 --proxy socks5://127.0.0.1:1080

# More worker processes for higher throughput
obscura serve --port 9222 --workers 4
```

Then connect from Node:

**Puppeteer:**

```javascript
import puppeteer from 'puppeteer-core';

const browser = await puppeteer.connect({
  browserWSEndpoint: 'ws://127.0.0.1:9222/devtools/browser',
});

const page = await browser.newPage();
await page.goto('https://news.ycombinator.com');

const stories = await page.evaluate(() =>
  Array.from(document.querySelectorAll('.titleline > a'))
    .map(a => ({ title: a.textContent, url: a.href }))
);
console.log(stories);

await browser.disconnect();
```

**Playwright:**

```javascript
import { chromium } from 'playwright-core';

const browser = await chromium.connectOverCDP({
  endpointURL: 'ws://127.0.0.1:9222',
});

const ctx = await browser.newContext();
const page = await ctx.newPage();
await page.goto('https://en.wikipedia.org/wiki/Web_scraping');
console.log(await page.title());

await browser.close();
```

### 4. Form submission & login

Obscura handles POSTs, follows 302 redirects, and maintains cookies natively.

```javascript
await page.goto('https://quotes.toscrape.com/login');
await page.evaluate(() => {
  document.querySelector('#username').value = 'admin';
  document.querySelector('#password').value = 'admin';
  document.querySelector('form').submit();
});
```

## React (and any SPA) E2E Testing with Playwright + Obscura

This is the most common Claude-Code use case. The agent already has access to
the user's frontend repo and is asked to validate a feature ponta-a-ponta —
not just unit tests, but real browser interaction (login, form submit,
navigation, asserting UI). Use Obscura as a drop-in Chrome replacement so
tests run 5–10× faster with ~1/7 of the memory.

This section is **stack-agnostic**: works with React, Vue, Svelte, Next.js,
Remix, Nuxt, Astro, plain HTML, and anything else that runs in a browser.
Playwright doesn't care what framework rendered the DOM.

### When to invoke this workflow

The agent should reach for this whenever any of these is true:

- The user changed code under a frontend route (`src/pages/**`, `app/**`,
  `client/src/features/**`, `routes/**`)
- The user asks to "test the flow", "validate the page", "make sure login
  still works", "check the UI ponta-a-ponta"
- A unit test is green but the user reports a runtime / integration bug
  (form not submitting, redirect loop, modal not closing, toast still
  showing the wrong message)
- The agent is about to claim a frontend task is done and the project
  has Playwright already configured

### Decision tree before running anything

```
Does the project already have @playwright/test in devDependencies?
├── YES → use the existing config; just plug Obscura in via env var
└── NO  → ask user before scaffolding Playwright; do NOT install silently

Is `obscura --version` available on PATH?
├── YES → start `obscura serve` in the background and run tests
└── NO  → tell the user to install Obscura (see Installation section);
         OR fall back to Playwright's bundled Chromium if the user prefers
         not to install Obscura
```

### Setup (when Playwright is already configured)

The whole integration is one optional env var. Do not rewrite existing
config — add a conditional block.

**1) Patch `playwright.config.ts` to honor `USE_OBSCURA=1`:**

```ts
// playwright.config.ts
import { defineConfig, devices } from "@playwright/test";

const useObscura = process.env.USE_OBSCURA === "1";
const obscuraWs = process.env.OBSCURA_WS || "ws://127.0.0.1:9222";

export default defineConfig({
  // ...keep all existing fields exactly as they are...
  use: {
    ...devices["Desktop Chrome"],
    baseURL: process.env.PLAYWRIGHT_BASE_URL || "http://localhost:5173",
    trace: "on-first-retry",
    video: "on-first-retry",
    screenshot: "only-on-failure",
    // Drop-in switch: if USE_OBSCURA=1, connect over CDP instead of
    // launching the bundled Chromium.
    ...(useObscura && {
      connectOptions: { wsEndpoint: obscuraWs },
    }),
  },
});
```

Without `USE_OBSCURA=1` the project keeps behaving exactly as before.
Setting the env var is an opt-in fast path.

**2) Add npm scripts that orchestrate the Obscura server lifecycle.**

The agent should not assume `obscura serve` is already running. Use a
helper script that starts/stops it around the test run:

```jsonc
// package.json
{
  "scripts": {
    "obscura:start": "obscura serve --port 9222 --stealth &",
    "obscura:stop": "pkill -f 'obscura serve' || true",
    "e2e:fast": "bash ./scripts/run-e2e-obscura.sh"
  }
}
```

```bash
#!/usr/bin/env bash
# scripts/run-e2e-obscura.sh
set -e
obscura serve --port 9222 --stealth &
OBSCURA_PID=$!
trap "kill $OBSCURA_PID 2>/dev/null || true" EXIT
# Wait until the CDP server is reachable (max 5s)
for i in {1..50}; do
  curl -s http://127.0.0.1:9222/json/version >/dev/null && break
  sleep 0.1
done
USE_OBSCURA=1 npx playwright test "$@"
```

Make the script executable: `chmod +x scripts/run-e2e-obscura.sh`.

**3) Verify the dev server is reachable before tests run.**

The agent must guarantee the frontend is up at `baseURL` (default
`http://localhost:5173` for Vite, `http://localhost:3000` for Next.js).
Either:

- Use Playwright's built-in `webServer` block (preferred; auto-starts dev
  server on test run):

  ```ts
  webServer: {
    command: "npm run dev",
    url: "http://localhost:5173",
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  ```

- Or check `curl -fs http://localhost:5173 >/dev/null` in the helper
  script and start `npm run dev &` if it fails.

### Setup (when the project does NOT have Playwright)

Do **not** install Playwright silently. Ask the user first. If they
agree, run:

```bash
npm install -D @playwright/test
npx playwright install chromium       # only needed when NOT using Obscura
mkdir -p e2e
```

Then create a minimal `playwright.config.ts`, a smoke test
`e2e/smoke.spec.ts`, and the helper script above. Keep the smoke test
small (load `/`, assert the title) so the agent can prove the pipeline
works before writing real coverage.

### Writing the actual E2E test (framework-agnostic patterns)

Use these patterns regardless of React/Vue/Next/etc:

```ts
// e2e/login.spec.ts
import { test, expect } from "@playwright/test";

test("login flow works", async ({ page }) => {
  await page.goto("/");

  // Prefer accessibility selectors. They survive markup refactors and
  // work the same across React / Vue / Svelte renders.
  await page.getByRole("link", { name: /entrar|login|sign in/i }).click();
  await page.getByLabel(/email/i).fill("test@example.com");
  await page.getByLabel(/senha|password/i).fill("hunter2");
  await page.getByRole("button", { name: /entrar|submit/i }).click();

  // Auto-wait: Playwright retries the assertion until the timeout.
  // No manual sleeps, no flaky setTimeout.
  await expect(page).toHaveURL(/\/dashboard/);
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});
```

**Selector priority** (most stable to least):

1. `getByRole` + accessible name
2. `getByLabel` (forms)
3. `getByTestId` (`data-testid` attribute the team controls)
4. `getByText` (fragile if copy changes)
5. CSS / XPath (last resort)

**Things to assert** in a typical SPA flow:

- The URL changed to the expected route
- The expected `<h1>` / page title is visible
- Network call returned 2xx — use `page.waitForResponse(/\/api\/.../)`
- Toast / error region is **not** visible (or shows the right message)
- Local/session storage has the token (`page.evaluate(() => localStorage.getItem("token"))`)

### Running the suite

```bash
# Headed (you watch it run, debugging)
npx playwright test --headed

# Full speed via Obscura
npm run e2e:fast

# Only one spec
npm run e2e:fast -- e2e/login.spec.ts

# Open the HTML report after a run
npx playwright show-report
```

### Reading the report when something fails

Playwright drops three artifacts on failure (configured above):

- `playwright-report/index.html` — interactive UI
- `test-results/<spec>/trace.zip` — open with `npx playwright show-trace`
- `test-results/<spec>/video.webm` — full recording of the failing run
- `test-results/<spec>/test-failed-1.png` — screenshot

The agent should always open the trace before guessing the fix. Most
"flaky" failures are real timing bugs in the app code visible in the
trace timeline.

### Common pitfalls in React/SPA E2E

| Symptom | Likely Cause | Fix |
|---|---|---|
| Test passes locally, fails in CI | Race with hydration | Use `await page.waitForLoadState("networkidle")` after `goto` |
| Click hits wrong element | Same role appears twice (header + sidebar) | Scope with `page.getByRole("main").getByRole(...)` |
| Form submit silently no-ops | RHF / Zod async validation | Use `page.getByRole("button").click()` then `expect(toast).toBeVisible()`; don't assert URL immediately |
| `localStorage` is empty in next test | Each test gets a fresh context | Use `test.beforeEach` to seed, or Playwright fixtures |
| Auth cookies dropped between tests | Cross-context isolation | Save state with `page.context().storageState()` and reuse via `test.use({ storageState: ... })` |
| Long animations slow the suite | Framer Motion / CSS transitions | Inject `* { transition: none !important; animation: none !important }` via `page.addStyleTag` |

### CI tips

In GitHub Actions (or any CI), add Obscura as a download step. The
binary is small, the install is fast, and you stop paying the
~300 MB Chromium download per job:

```yaml
- name: Install Obscura
  run: |
    curl -L -o /tmp/obscura.tar.gz \
      https://github.com/h4ckf0r0day/obscura/releases/latest/download/obscura-x86_64-linux.tar.gz
    tar xzf /tmp/obscura.tar.gz -C /usr/local/bin/
- name: Run E2E with Obscura
  run: npm run e2e:fast
```

### What the agent must NOT do

- Do not run `npx playwright install` if Obscura is going to drive the
  tests — that downloads ~300 MB of Chromium for nothing.
- Do not modify existing E2E specs to make them pass; if a spec fails,
  the bug is in the app code 95% of the time.
- Do not hard-code `setTimeout` waits in tests. Use `expect(...).toPass()`
  or built-in auto-waiting locators.
- Do not commit `.env` files with real credentials for E2E. Use
  `process.env.E2E_USER` / `E2E_PASS` and document them in `.env.example`.
- Do not start `obscura serve` and forget to kill it. Always use the
  `trap` pattern in the helper script.

### Decision shortcut for the agent

When the user says "rode os testes" or "valide o fluxo" on a frontend
project, the agent should:

1. Detect Playwright (`grep -q '"@playwright/test"' package.json`).
2. Detect Obscura (`command -v obscura`).
3. If both present → `npm run e2e:fast` (or equivalent).
4. If only Playwright → `npm run e2e` and recommend installing Obscura.
5. If neither → ask the user before scaffolding.

## Stealth Mode

Build with `--features stealth` (or use the stealth release binary) and run
with `--stealth`.

What it does:

- Per-session fingerprint randomization (GPU, screen, canvas, audio, battery)
- Realistic `navigator.userAgentData` (Chrome 145, high-entropy values)
- `event.isTrusted = true` for dispatched events
- Hidden internal properties (`Object.keys(window)` is safe)
- Native function masking (`Function.prototype.toString()` returns `[native code]`)
- `navigator.webdriver = undefined` (matches real Chrome)
- Blocks 3,520 tracker / analytics / fingerprinting domains

## CLI Reference Cheat Sheet

### `obscura serve`

| Flag | Default | Description |
|------|---------|-------------|
| `--port` | `9222` | WebSocket port |
| `--proxy` | — | HTTP/SOCKS5 proxy URL |
| `--stealth` | off | Anti-detection + tracker blocking |
| `--workers` | `1` | Parallel worker processes |
| `--obey-robots` | off | Respect robots.txt |

### `obscura fetch <URL>`

| Flag | Default | Description |
|------|---------|-------------|
| `--dump` | `html` | `html` \| `text` \| `links` |
| `--eval` | — | JS expression to evaluate |
| `--wait-until` | `load` | `load` \| `domcontentloaded` \| `networkidle0` |
| `--selector` | — | Wait for CSS selector |
| `--stealth` | off | Anti-detection mode |
| `--quiet` | off | Suppress banner |

### `obscura scrape <URL...>`

| Flag | Default | Description |
|------|---------|-------------|
| `--concurrency` | `10` | Parallel workers |
| `--eval` | — | JS expression per page |
| `--format` | `json` | `json` \| `text` |

## CDP Coverage

Obscura implements the Chrome DevTools Protocol surface needed by
Puppeteer / Playwright:

| Domain | Methods |
|--------|---------|
| Target | createTarget, closeTarget, attachToTarget, createBrowserContext, disposeBrowserContext |
| Page | navigate, getFrameTree, addScriptToEvaluateOnNewDocument, lifecycleEvents |
| Runtime | evaluate, callFunctionOn, getProperties, addBinding |
| DOM | getDocument, querySelector, querySelectorAll, getOuterHTML, resolveNode |
| Network | enable, setCookies, getCookies, setExtraHTTPHeaders, setUserAgentOverride |
| Fetch | enable, continueRequest, fulfillRequest, failRequest |
| Storage | getCookies, setCookies, deleteCookies |
| Input | dispatchMouseEvent, dispatchKeyEvent |
| LP | getMarkdown (DOM-to-Markdown) |

## Decision Heuristics

When the user asks for web automation, choose this way:

1. **One page, one shot** → `obscura fetch <url> --eval "..."`
2. **Many pages, same selector** → `obscura scrape <urls> --concurrency 25`
3. **Stateful flow, login, multi-step** → `obscura serve` + Puppeteer/Playwright
4. **Page detects bots** → add `--stealth`
5. **Behind a proxy** → `--proxy <url>`
6. **CI / Docker** → use the static Linux binary, no Chrome needed

## Anti-Patterns

- Do **not** use Obscura against sites whose terms of service forbid scraping.
- Do **not** disable `--obey-robots` on third-party sites in production
  pipelines without consent.
- Do **not** treat stealth mode as a bypass for paywalls or auth — it only
  hides the fact that the browser is automated, not the fact that requests
  are made.
- Do **not** spawn `obscura fetch` in a tight shell loop for many URLs — use
  `obscura scrape` (worker pool) instead.

## Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `connection refused` from Puppeteer | Server not running | `obscura serve --port 9222` first |
| Page renders empty HTML | JS hasn't finished | Add `--wait-until networkidle0` |
| Site detects automation | webdriver leak | Build with `--features stealth`, run with `--stealth` |
| Build fails on `v8` | Rust < 1.75 | `rustup update stable` |
| Slow first build | V8 compiling | Expected ~5 min, cached after |

## References

- Repository: https://github.com/h4ckf0r0day/obscura
- Releases (binaries): https://github.com/h4ckf0r0day/obscura/releases
- Chrome DevTools Protocol: https://chromedevtools.github.io/devtools-protocol/
- Puppeteer: https://pptr.dev/
- Playwright: https://playwright.dev/
