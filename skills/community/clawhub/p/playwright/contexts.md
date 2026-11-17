# Contexts — Tabs, Popups, Dialogs, and Emulation

The context is the unit of isolation: an incognito profile with its own cookies, storage, permissions, and emulation. Pages inside it share everything; contexts share nothing.

Contents: [Multiple Users In One Test](#multiple-users-in-one-test) · [New Tabs And Popups](#new-tabs-and-popups) · [Dialogs](#dialogs) · [Emulation](#emulation) · [Runtime Overrides](#runtime-overrides) · [Lifecycle And Cost](#lifecycle-and-cost) · [Persistent Profiles](#persistent-profiles)

## Multiple Users In One Test

Chat, approvals, presence, and collaborative editing need two identities simultaneously — two contexts, one browser:

```typescript
test('reviewer sees the submitted doc', async ({ browser }) => {
  const authorCtx = await browser.newContext({ storageState: '.auth/author.json' });
  const reviewCtx = await browser.newContext({ storageState: '.auth/reviewer.json' });
  const author = await authorCtx.newPage();
  const reviewer = await reviewCtx.newPage();

  await author.goto('/docs/new');
  await author.getByRole('button', { name: 'Submit' }).click();

  await reviewer.goto('/queue');
  await expect(reviewer.getByText('Untitled doc')).toBeVisible();

  await authorCtx.close();
  await reviewCtx.close();
});
```

Two pages in the **same** context share a session — that models two tabs of one user, not two users. Getting this wrong produces tests that pass because both "users" are the same person.

## New Tabs And Popups

```typescript
const popupPromise = page.waitForEvent('popup');
await page.getByRole('link', { name: 'Open docs' }).click();   // target="_blank"
const popup = await popupPromise;
await popup.waitForLoadState();
await expect(popup).toHaveURL(/docs/);
```

- Context-level for tabs you did not trigger directly: `context.on('page', p => ...)`.
- `context.pages()` lists open pages; the last one is usually the new tab, but ordering is not a contract — match by URL.
- OAuth popups are a page like any other: fill the IdP form in the popup, then continue on the opener after it closes.
- The opener keeps running: assertions on `page` still work while `popup` is open.

## Dialogs

**Playwright auto-dismisses `alert`, `confirm`, `prompt`, and `beforeunload` when no handler is registered.** Two consequences:

1. A test that "clicks Delete and nothing happens" is often a `confirm()` being dismissed for you.
2. The moment you register a handler, auto-dismissal stops — **you must respond, or the page hangs forever**.

```typescript
page.once('dialog', async dialog => {
  expect(dialog.message()).toContain('Delete 3 items?');
  await dialog.accept();            // or dialog.dismiss()
});
await page.getByRole('button', { name: 'Delete' }).click();

page.on('dialog', d => d.accept('typed answer'));   // prompt value
```

Use `once` when only one dialog is expected — a lingering `on` handler silently accepts a later dialog the test never meant to confirm.

## Emulation

```typescript
const context = await browser.newContext({
  ...devices['iPhone 15'],          // viewport, UA, deviceScaleFactor, isMobile, hasTouch
  locale: 'de-DE',
  timezoneId: 'Europe/Berlin',
  colorScheme: 'dark',
  reducedMotion: 'reduce',
  geolocation: { latitude: 52.52, longitude: 13.405 },
  permissions: ['geolocation'],
  viewport: { width: 1280, height: 720 },
});
```

| Knob | Notes |
|---|---|
| `devices[...]` | Chromium emulation: correct viewport, touch, and UA — **not** a real iOS engine. WebKit + a device descriptor is closer to Safari; only a real device proves iOS behavior |
| `isMobile` | Not supported in Firefox — a mobile project must run on Chromium or WebKit |
| `locale` / `timezoneId` | Set them explicitly in config; the CI runner is UTC and your laptop is not (`flake.md`) |
| `colorScheme` | `'dark'`, `'light'`, `'no-preference'`; a project per scheme is cheaper than in-test toggling |
| `reducedMotion: 'reduce'` | Also a free way to calm animations in visual tests |
| `geolocation` | Requires the `geolocation` permission or the app sees a denial |
| `offline` | `context.setOffline(true)` mid-test to exercise the offline UI |
| `viewport: null` | Uses the real window size — only meaningful headed |

Permissions are context-scoped: `context.grantPermissions(['notifications', 'clipboard-write'], { origin })`, `context.clearPermissions()`. Names and support vary by engine; Chromium has the widest set.

## Runtime Overrides

```typescript
await page.setViewportSize({ width: 375, height: 812 });   // responsive breakpoints mid-test
await page.emulateMedia({ media: 'print', colorScheme: 'dark' });
await page.clock.setFixedTime(new Date('2026-01-01T00:00:00Z'));   // deterministic dates (playwright >=1.45)
await context.addInitScript(() => { window.__E2E__ = true; });     // runs before any page script
```

`addInitScript` is the correct place to stub `window` APIs (analytics, feature flags, `crypto.randomUUID`) because it runs before the app's own code on every page and every navigation — a `page.evaluate` after `goto` is already too late.

## Lifecycle And Cost

| Action | When |
|---|---|
| `browser.newContext()` | Per test (the runner does it for you), or per identity |
| `context.newPage()` | Per tab |
| `browser.close()` | Per worker, at the end — never per test |
| Manual contexts | Always close them in a `finally` or fixture teardown; leaked contexts leak browser memory across a long run |

Launching a browser is the expensive step; a context is comparatively cheap, which is what makes per-test isolation affordable. In a plain script (no test runner), reuse one browser and create a context per logical job.

## Persistent Profiles

```typescript
const context = await chromium.launchPersistentContext('/tmp/pw-profile', { headless: false });
```

Keeps cookies, localStorage, and extensions across runs, and returns a context with no `browser` to close. Legitimate for exploratory work, extension testing, and MCP sessions (`mcp.md`). Wrong for a test suite: persistent state is exactly what makes results irreproducible, and a stale profile is undebuggable a week later.
