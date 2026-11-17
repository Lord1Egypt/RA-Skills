# Debugging — Symptom to Cause

Work symptom-first. Each chain is ordered by probability and every step is a check, not a guess.

Contents: [The Universal First Three](#the-universal-first-three) · [Locator Never Matched](#locator-never-matched-timeout--waiting-for-locator) · [Element Found But The Action Fails](#element-found-but-the-action-fails) · [Passes Locally, Fails In CI](#passes-locally-fails-in-ci) · [Only Fails Headless](#only-fails-headless) · [The Suite Hangs](#the-suite-hangs) · [Network-Level Investigation](#network-level-investigation) · [Debug Interactively](#debug-interactively) · [Failure Artifacts Worth Keeping](#failure-artifacts-worth-keeping) · [When You Are Truly Stuck](#when-you-are-truly-stuck)

## The Universal First Three

1. **Read the first line of the error.** Playwright names the failed condition (`strict mode violation`, `waiting for element to be visible`, `waiting for locator`). The rest of the stack rarely adds anything.
2. **Open the trace.** `npx playwright show-trace test-results/**/trace.zip` → click the failing action → the **before** DOM snapshot answers "was it rendered?" and the **after** answers "did anything happen?". Network and Console tabs are in the same file.
3. **Reproduce narrow.** `npx playwright test file.spec.ts:42 --headed --trace on`. If it passes alone but fails in the suite, the bug is isolation, not the test (→ `flake.md`).

If no trace exists, that is the first fix: `use: { trace: 'on-first-retry' }`.

## Locator Never Matched (`Timeout ... waiting for locator`)

1. Trace → before-snapshot at that step. Element visible in the snapshot? Then the locator is wrong, not the timing.
2. Not in the snapshot at all → it renders later (assert on a preceding state), or it lives in an **iframe** (`selectors.md`), or behind a closed shadow root.
3. In the snapshot but not matched → inspect the accessible name; icon buttons often have an `aria-label` different from the visible text, and `getByText` matches substrings while `getByRole` name matching is whole-string.
4. Matched in headed, not in headless → viewport. A 1280×720 headless window hides a desktop-only element behind a responsive breakpoint (`browsers.md`).
5. Only in CI → different data. The row you locate by text does not exist in the seeded environment.

## Element Found But The Action Fails

1. `not visible` → zero-size box, `display: none`, or an ancestor collapsed. Check the parent chain in the snapshot.
2. `intercepts pointer events` → the snapshot shows the covering node; it is usually a consent banner, a toast, or a sticky header. Dismiss it in a fixture — that is real user-facing state, not test noise.
3. `element is not stable` → an animation still running. Disable animations for the run, or assert on the settled state first (`waiting.md`).
4. `element is not enabled` → the app enables the button after async validation; assert `toBeEnabled()` before clicking.
5. Click "works" but nothing happens → a handler attached after hydration. Wait for a hydration signal (a `data-` attribute, a network response) instead of the element's presence.

## Passes Locally, Fails In CI

Each check is under a minute:

| Difference | Check |
|---|---|
| Viewport | CI default is 1280×720; local headed windows are larger |
| Workers | Local half-cores vs CI 1 (or vice versa) changes ordering and load |
| Timezone / locale | `TZ` and `--lang` differ; date assertions break silently |
| Animations and fonts | Missing fonts change layout and text wrapping |
| Machine speed | A shared runner is 2-5× slower; races surface only there |
| Data | Seeded fixtures vs a lived-in local database |
| Browser build | CI image version vs local install (rule 9) |
| Base URL | Staging behind auth, a redirect, or a cold start |

Fastest reproduction of a slow runner locally: `npx playwright test --workers=4 --repeat-each=3` while a build runs, or throttle CPU through CDP (`performance.md`).

## Only Fails Headless

1. Viewport and window size (above).
2. Media: no H.264 or DRM in some headless builds — video and audio tests need a branded channel (`browsers.md`).
3. Downloads and PDFs behave differently; `page.pdf()` is Chromium-headless only (`files.md`).
4. Extensions and profile state that exist only in your headed browser.
5. Confirm with `--headed` **and** the CI browser build before concluding it is headless-specific.

## The Suite Hangs

- `DEBUG=pw:api npx playwright test` — the last logged call before the silence names the stuck operation.
- Unhandled `dialog`: with a handler registered but never answered, the page blocks forever (`contexts.md`).
- `waitForEvent` registered after the action that fired it — the promise never settles (`waiting.md`).
- `webServer` never became ready: its own 60 s timeout fires first; check the command actually serves on the configured port.
- No `globalTimeout` set, so a hung job runs until the CI provider kills it.

## Network-Level Investigation

```typescript
page.on('request', r => console.log('>>', r.method(), r.url()));
page.on('response', r => console.log('<<', r.status(), r.url()));
page.on('requestfailed', r => console.log('XX', r.url(), r.failure()?.errorText));
page.on('console', m => console.log('PAGE', m.type(), m.text()));
page.on('pageerror', e => console.log('PAGEERROR', e.message));
```

Attach these in a fixture during an investigation, not permanently — the noise buries the signal. The trace already records all of it; use the listeners only when you need output during a live run. Deeper interception, mocking, and HAR replay: `network.md`.

## Debug Interactively

```bash
npx playwright test file.spec.ts --debug   # Inspector, timeouts disabled
npx playwright test --ui                   # watch mode, time travel, live locator picker
```

```typescript
await page.pause();   // drop into the Inspector at an exact point
```

UI mode is the better default while iterating: it keeps a trace for every run, lets you edit and re-run a single test, and its locator picker generates a locator from a click — faster than guessing and verifying in a rerun loop.

## Failure Artifacts Worth Keeping

```typescript
// playwright.config.ts
use: {
  trace: 'on-first-retry',        // 'on' bloats storage and slows every run
  screenshot: 'only-on-failure',
  video: 'retain-on-failure',
}
```

Custom evidence for a stubborn failure:

```typescript
test.afterEach(async ({ page }, testInfo) => {
  if (testInfo.status !== testInfo.expectedStatus) {
    await testInfo.attach('dom', { body: await page.content(), contentType: 'text/html' });
  }
});
```

Attachments land in the HTML report next to the failure — better than a console dump nobody scrolls to.

## When You Are Truly Stuck

Rebuild the test forward from `page.goto`, one action at a time in `--debug`, asserting after each. The first step whose assertion needs an explanation is the bug — and it is usually two steps before the one that was failing.
