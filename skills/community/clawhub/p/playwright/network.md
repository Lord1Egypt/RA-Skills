# Network — Interception, Mocking, HAR, and API Calls

Every request the page makes is yours to observe, rewrite, or replace. Use it to remove other people's servers from your failure surface.

Contents: [Routing Basics](#routing-basics) · [What To Mock, What To Keep Real](#what-to-mock-what-to-keep-real) · [Waiting On Requests And Responses](#waiting-on-requests-and-responses) · [HAR Record And Replay](#har-record-and-replay) · [API Requests Alongside The Browser](#api-requests-alongside-the-browser) · [Errors, Offline, And Slow Networks](#errors-offline-and-slow-networks) · [Headers, Auth, And Proxies](#headers-auth-and-proxies) · [Debugging Mocks That Do Not Fire](#debugging-mocks-that-do-not-fire)

## Routing Basics

```typescript
await page.route('**/api/checkout', route => route.fulfill({
  status: 500,
  contentType: 'application/json',
  body: JSON.stringify({ error: 'Payment failed' }),
}));

await page.route('**/api/user', async route => {
  const response = await route.fetch();          // let it hit the server
  const json = await response.json();
  json.plan = 'enterprise';                       // then patch the answer
  await route.fulfill({ response, json });
});

await page.route('**/*.{png,jpg,woff2}', route => route.abort());   // strip assets
await page.unroute('**/api/user');                                  // remove one handler
```

Rules that decide whether a route fires:

- Handlers are matched **last registered first**; the first one that calls `fulfill`, `abort`, or `fallback` decides. `route.fallback()` passes to the next handler, `route.continue()` skips straight to the network.
- Register routes **before** the navigation that triggers the request. A route added after `goto` misses everything already in flight.
- `context.route` covers every page and popup in the context; `page.route` covers one page. Multi-tab flows need the context level.
- Glob patterns match the **full URL**, so `**/api/x` and `*/api/x` behave differently; a regex is clearer for anything with query strings.
- Requests served by a service worker never reach `route` — register the route on the context and disable the service worker in tests (`serviceWorkers: 'block'`) when mocks mysteriously do nothing.

## What To Mock, What To Keep Real

| Dependency | Default |
|---|---|
| Your own backend | Real — it is part of what you are testing |
| Payment provider, email provider, SMS | Mocked, plus one opt-in `@integration` spec against the sandbox |
| Analytics, session replay, chat widgets, ads | Aborted — pure flake with zero signal |
| Maps, embeds, fonts from a CDN | Mocked or aborted unless the visual is under test |
| Feature-flag service | Mocked to a fixed set; a remote flag flip is an invisible test rewrite |
| Auth provider | See `auth.md` |

A single `beforeEach` that aborts analytics and ad domains removes a whole class of intermittent timeouts and shortens every run.

## Waiting On Requests And Responses

```typescript
const responsePromise = page.waitForResponse(r => r.url().includes('/api/data') && r.ok());
await page.getByRole('button', { name: 'Load' }).click();
const data = await (await responsePromise).json();

await page.waitForRequest('**/analytics/**');       // assert a call WAS made
```

Register before the trigger (`waiting.md`). For "no request should be made", assert on the observable consequence instead — proving a negative by waiting is a guaranteed timeout.

## HAR Record And Replay

Best tool for a third-party flow too complex to hand-mock.

```typescript
// record once
const context = await browser.newContext({
  recordHar: { path: 'fixtures/checkout.har', mode: 'minimal' },
});

// replay in tests
await page.routeFromHAR('fixtures/checkout.har', {
  url: '**/api/**',
  update: false,          // true re-records; keep false in CI
  notFound: 'abort',      // 'fallback' lets unmatched requests hit the network
});
```

- `mode: 'minimal'` records only what replay needs; full mode captures headers and timings and gets large.
- Scrub the HAR before committing: it contains cookies, tokens, and response bodies verbatim.
- A HAR is a snapshot with an expiry — when the upstream API changes shape, the tests keep passing against a fossil. Re-record on a schedule and diff (the `Cadence` preference area; gates in `ci-cd.md`).

## API Requests Alongside The Browser

```typescript
test('seeds via API, verifies in UI', async ({ page, request }) => {
  const res = await request.post('/api/todos', { data: { title: 'Buy milk' } });
  expect(res.ok()).toBeTruthy();
  await page.goto('/todos');
  await expect(page.getByText('Buy milk')).toBeVisible();
});
```

Two contexts, one distinction that costs hours: **`page.request` shares the browser context's cookie jar** (so it is already authenticated as the page), while the standalone **`request` fixture has its own storage** and is not. Use `page.request` for calls that must be the logged-in user; use `request` for setup calls with a service token.

Pure API tests are legitimate in the same suite — `request` needs no browser and runs in milliseconds. Keep them in their own project so a browser-less job can run them fast.

## Errors, Offline, And Slow Networks

```typescript
await context.setOffline(true);                              // offline UI state
await page.route('**/api/**', r => r.abort('failed'));       // network error path
await page.route('**/api/**', async r => {                   // latency injection
  await new Promise(res => setTimeout(res, 2000));
  await r.continue();
});
await page.route('**/api/**', r => r.fulfill({ status: 429, headers: { 'retry-after': '1' } }));
```

Error-path coverage is where mocking pays for itself: a 500, a 429, and a timeout are three states users hit and no staging environment reproduces on demand.

## Headers, Auth, And Proxies

```typescript
use: {
  extraHTTPHeaders: { 'x-test-run': process.env.RUN_ID ?? 'local' },
  httpCredentials: { username: 'staging', password: process.env.BASIC_PASS! },
  ignoreHTTPSErrors: true,        // scope to the staging project only
  proxy: { server: 'http://proxy.internal:8080' },
}
```

Tagging every test request with a header makes server logs greppable and lets the backend refuse test traffic in production — a cheap guardrail worth adding on day one.

## Debugging Mocks That Do Not Fire

1. Log every request: `page.on('request', r => console.log(r.url()))` and compare the real URL with your pattern.
2. Check the order: a later `page.route` shadows an earlier one.
3. Check the scope: the request may come from a popup or an iframe on another page object.
4. Check service workers (above).
5. Check timing: registered after `goto`.
6. The trace's Network tab shows which requests were served from a route — it marks them, so the answer is in the artifact you already have.
