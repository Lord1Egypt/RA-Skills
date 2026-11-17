# Waiting — Actionability, Timeouts, and Never Sleeping

Playwright already waits. Every failure that looks like "needs a bigger wait" is really one of: the condition never happens, the wrong condition is being waited on, or the element is actionable-blocked by something real.

Contents: [The Actionability Checks](#the-actionability-checks) · [Timeout Defaults](#timeout-defaults) · [Wait On The Right Thing](#wait-on-the-right-thing) · [Retrying vs Non-Retrying](#retrying-vs-non-retrying) · [Arbitrary Conditions](#arbitrary-conditions) · [Waiting For Events, Not After Them](#waiting-for-events-not-after-them) · [Navigation](#navigation) · [When The Wait Is Legitimately Long](#when-the-wait-is-legitimately-long)

## The Actionability Checks

Before a click, Playwright waits for all of these, then retries until the timeout:

| Check | Meaning | Typical blocker |
|---|---|---|
| Attached | In the DOM | Rendered later, or in an iframe |
| Visible | Non-empty box, no `visibility: hidden` | `display: none`, zero height, `opacity` is **not** checked |
| Stable | Same bounding box for two consecutive animation frames | CSS transition, sliding drawer, layout shift from a late image |
| Receives events | Hit-testing at the action point lands on the target | Cookie banner, toast, modal backdrop, sticky header |
| Enabled | Not `disabled` | Form still validating |
| Editable (fill only) | Not `readonly` | Field waiting on an async default |

The error message names which check failed — read it before changing anything. `force: true` skips the checks (the element must still resolve) and therefore skips the diagnosis: use it only when you have confirmed the blocker is a test artifact you cannot remove, and leave a comment saying so.

## Timeout Defaults

Canonical values (same set as SKILL.md rule 3):

| Setting | Default | Meaning |
|---|---|---|
| `timeout` (test) | 30 000 ms | Whole test including `beforeEach`; the real ceiling for everything below |
| `expect.timeout` | 5 000 ms | Per web-first assertion |
| `actionTimeout` | 0 | Unbounded — an action can consume the entire test timeout |
| `navigationTimeout` | 0 | Same, for `goto`/`waitForURL` |
| `globalTimeout` | 0 | Whole run; set it in CI so a hung job dies in minutes, not hours |
| `webServer.timeout` | 60 000 ms | Waiting for the dev server to answer |
| `expect.toPass` intervals | 100, 250, 500, 1000 ms | Backoff between probes, then 1000 ms repeating |

Sizing rule: sum the slowest legitimate path, measured not guessed, and keep the total inside the 30 000 ms default — login 4 s + dashboard render 8 s + one 5 s assertion = 17 s, comfortably inside 30 s. A path that does not fit has a product problem or a missing mock, not a config problem: raise the one slow assertion, never the default.

Raise the narrow one:

```typescript
await expect(report).toBeVisible({ timeout: 30_000 });   // this export really takes 25 s
test.setTimeout(120_000);                                // this one test only
test.slow();                                             // triples the timeout for this test
```

Never raise `timeout` globally to fix one test: every genuine hang then costs the new ceiling, and a 60 s default turns a 30-test failure into a half-hour CI job.

## Wait On The Right Thing

| Instead of | Wait for |
|---|---|
| `waitForTimeout(1000)` | `await expect(locator).toBeVisible()` |
| `waitForLoadState('networkidle')` | The element, the response, or the URL you care about |
| Sleep after clicking Save | `await expect(page.getByText('Saved')).toBeVisible()` |
| Sleep after navigation | `await page.waitForURL(/\/dashboard/)` or an assertion on the new page |
| Sleep waiting for an API | `const r = page.waitForResponse('**/api/x'); await click; await r;` |
| Sleep waiting for a spinner | `await expect(spinner).toBeHidden()` |
| Sleep for an animation | `await expect(drawer).toHaveCSS('transform', 'none')`, or disable animations |
| Sleep for a debounce | Assert on the debounced result, not the delay |

`networkidle` is discouraged in the docs for a reason: analytics beacons, polling, and websockets mean "quiet network" never arrives in a real SPA — and when it does arrive, it arrived late.

## Retrying vs Non-Retrying

This distinction causes more false greens than any other API detail.

```typescript
await expect(locator).toBeVisible();          // retries until expect timeout
await expect(locator).toHaveText('Done');     // retries
await expect(page).toHaveURL(/checkout/);     // retries
await expect(locator).toHaveCount(3);         // retries

expect(await locator.count()).toBe(3);        // ONE shot, no retry — races the render
if (await locator.isVisible()) { ... }        // ONE shot, returns false instantly
expect(await locator.textContent()).toBe('x') // ONE shot
```

Rule: `expect(locator)` with the `await` **outside** retries; `expect(await ...)` does not. When you truly need a conditional, gate it with a retrying assertion first, or use `expect.poll`.

## Arbitrary Conditions

```typescript
await expect.poll(async () => (await api.jobStatus(id)).state, {
  timeout: 60_000,
}).toBe('complete');

await expect(async () => {
  const r = await page.request.get('/api/report');
  expect(r.status()).toBe(200);
}).toPass({ timeout: 30_000 });
```

Use these for backend state, third-party propagation, and eventual consistency — anything with no DOM signal. Keep the probe cheap: it runs every interval until it passes.

## Waiting For Events, Not After Them

Register the waiter **before** the action that triggers it, or you race it:

```typescript
const downloadPromise = page.waitForEvent('download');
await page.getByRole('button', { name: 'Export' }).click();
const download = await downloadPromise;
```

Same shape for `popup`, `filechooser`, `dialog`, `response`, `request`, and `page` (new tab). The `await click` in the middle is the point — `await page.waitForEvent(...)` written after the click misses events that already fired.

## Navigation

- `goto` resolves on `load` by default; `waitUntil: 'domcontentloaded'` is faster and usually enough, `'commit'` when you only need the navigation to start.
- Client-side routing fires no navigation event: wait for the destination's content or `waitForURL`.
- A click that triggers a full navigation needs no `waitForNavigation` — assert on the new page instead; the legacy `waitForNavigation` pattern races and is superseded by `waitForURL`.
- Redirect chains: assert the final URL with a regex, not an exact string, or a trailing slash flips the test.

## When The Wait Is Legitimately Long

Batch jobs, video encoding, cold serverless starts. Do not stretch the test — split it: trigger through the API, poll with `expect.poll`, then open the UI to assert the result. A 4-minute UI test blocks a worker for 4 minutes; a 4-minute poll on a fixture blocks one.
