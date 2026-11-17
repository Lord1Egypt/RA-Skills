# Auth — Sessions, Roles, and Parallel-Safe Accounts

Logging in through the UI in every test is the most expensive line in most suites: sign in once, reuse the state, and give every worker an account it owns.

Contents: [The Default Shape](#the-default-shape) · [What storageState Actually Captures](#what-storagestate-actually-captures) · [Faster: Skip The UI Entirely](#faster-skip-the-ui-entirely) · [Multiple Roles](#multiple-roles) · [Parallel-Safe Accounts](#parallel-safe-accounts) · [SSO, 2FA, And Magic Links](#sso-2fa-and-magic-links) · [Expiry And Rotation](#expiry-and-rotation) · [Handling Credentials](#handling-credentials)

## The Default Shape

A setup project signs in once and writes the storage state; every other project starts already authenticated.

```typescript
// global.setup.ts
import { test as setup, expect } from '@playwright/test';

setup('authenticate', async ({ page }) => {
  await page.goto('/login');
  await page.getByLabel('Email').fill(process.env.E2E_USER!);
  await page.getByLabel('Password').fill(process.env.E2E_PASS!);
  await page.getByRole('button', { name: 'Sign in' }).click();
  await expect(page.getByRole('heading', { name: 'Dashboard' })).toBeVisible();
  await page.context().storageState({ path: '.auth/user.json' });
});
```

```typescript
// playwright.config.ts
projects: [
  { name: 'setup', testMatch: /global\.setup\.ts/ },
  { name: 'chromium', dependencies: ['setup'], use: { storageState: '.auth/user.json' } },
]
```

`.auth/` goes in `.gitignore`. A committed storage state is a committed live session.

## What storageState Actually Captures

| Captured | Not captured |
|---|---|
| Cookies (including httpOnly) | `sessionStorage` — per tab, never serialized by default |
| `localStorage` per origin | IndexedDB, unless the Playwright version supports opting it in |
| | Service-worker caches |
| | Anything the server holds against a device fingerprint |

If the app keeps its token in `sessionStorage`, reuse fails silently: the test lands on a login page and the first assertion times out. Workarounds: copy the value in through an init script, or ask the app to accept the cookie path in test builds.

```typescript
await context.addInitScript(([k, v]) => sessionStorage.setItem(k, v), ['token', token]);
```

## Faster: Skip The UI Entirely

The login form is a product feature that deserves **one** test. Everywhere else, mint the session through the API:

```typescript
const res = await request.post('/api/login', { data: { email, password } });
const { token } = await res.json();
await context.addInitScript(t => localStorage.setItem('token', t), token);
// or: await context.addCookies([{ name: 'session', value: token, domain: 'localhost', path: '/' }]);
```

Saves the whole login round trip per worker and removes the login page from the failure surface of 400 unrelated tests.

## Multiple Roles

One storage-state file per role, one project per role:

```typescript
projects: [
  { name: 'setup', testMatch: /auth\.setup\.ts/ },
  { name: 'admin',  dependencies: ['setup'], use: { storageState: '.auth/admin.json' } },
  { name: 'viewer', dependencies: ['setup'], use: { storageState: '.auth/viewer.json' } },
]
```

Per-test override when a spec needs a different identity:

```typescript
test.use({ storageState: '.auth/admin.json' });        // describe or file scope
const anon = await browser.newContext({ storageState: undefined });   // logged-out path
```

Two users interacting (chat, approvals, presence) need two contexts in one test — see `contexts.md`.

## Parallel-Safe Accounts

Shared mutable accounts are the top cause of "passes alone, fails in the suite". Allocate by worker:

```typescript
export const test = base.extend<{}, { account: Account }>({
  account: [async ({}, use, workerInfo) => {
    const account = await api.createUser(`e2e-w${workerInfo.parallelIndex}@example.test`);
    await use(account);
    await api.deleteUser(account.id);
  }, { scope: 'worker' }],
});
```

- With N workers you need N accounts, not one. `parallelIndex` is stable and bounded by the worker count; `workerIndex` grows across restarts and will overrun a fixed pool.
- Sharded CI multiplies workers by shards: 4 shards × 4 workers = 16 concurrent identities. Size the pool for that number.
- Legacy systems with a fixed account list: index into the pool by `parallelIndex` and take a lock (a database row, a lock file) if shards run on separate machines.

## SSO, 2FA, And Magic Links

| Obstacle | Approach |
|---|---|
| OAuth / SSO redirect to an external IdP | Prefer a test IdP or a mocked provider; otherwise a dedicated setup project drives the real login once, and nothing else touches it |
| TOTP 2FA | Generate the code from the shared secret in the setup project — never a phone; store the secret as a CI secret |
| SMS or push 2FA | Not automatable: use a bypass flag, a test tenant with 2FA off, or a provider sandbox |
| Magic link | Read it from a mail-catcher API (Mailhog, Mailpit, provider sandbox), never from a real inbox |
| CAPTCHA on login | Disable in the test environment. Solving services are out of scope and usually a terms violation |
| Corporate IdP with device trust | Test against a staging IdP; production SSO is a manual smoke check |

## Expiry And Rotation

- Short-lived tokens outlive a fast suite but not a slow one. If tests near the end of a 25-minute run fail with 401 and earlier ones pass, the state expired mid-run: re-mint per worker instead of once globally.
- A stale `.auth/*.json` from yesterday's local run is a classic false failure. Regenerate in the setup project every run; never commit, never cache across CI runs.
- CSRF-protected apps may bind the session to a token issued at page load — reusing cookies is fine, reusing an in-page token is not.

## Handling Credentials

- Read from `process.env`, injected by CI secrets. Never hardcoded, never in the repo, never in `~/Clawic/data/playwright/`.
- Traces and videos capture typed values: mask password fields or set `trace: 'off'` for the auth setup project if the app echoes anything sensitive.
- The test user is a real account with real permissions — scope it to a throwaway tenant, not to production data.
