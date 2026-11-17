# Fixtures — Setup, Page Objects, and Test Data

Where a test gets its world from. Config and projects: `config.md`. Accounts and sessions: `auth.md`.

## Fixtures Over Helpers

```typescript
import { test as base } from '@playwright/test';

type Fixtures = { cart: CartPage };
type WorkerFixtures = { seededOrg: Org };

export const test = base.extend<Fixtures, WorkerFixtures>({
  cart: async ({ page }, use) => {
    await page.goto('/cart');
    await use(new CartPage(page));
  },
  seededOrg: [async ({}, use, workerInfo) => {
    const org = await api.createOrg(`w${workerInfo.parallelIndex}`);
    await use(org);
    await api.deleteOrg(org.id);      // teardown after the LAST test in this worker
  }, { scope: 'worker' }],
});
```

- Test-scoped fixtures run per test; worker-scoped run once per worker process and are the right home for expensive setup (a seeded tenant, a running service).
- Everything after `use()` is teardown and runs even when the test fails — the only reliable cleanup point.
- `auto: true` fixtures run without being requested: use for global listeners or per-test tracing, sparingly.
- Fixtures beat `beforeEach` helpers because a failure inside a fixture is reported as setup, not as a mysterious assertion failure inside the test.
- Overriding a built-in fixture (`page`, `context`, `baseURL`) is legal and is the clean way to apply a route or an init script to every test: `page: async ({ page }, use) => { await page.route(...); await use(page); }`.

## Page Objects: Late, Not Early

Extract on the third repetition. Rules that keep them useful:

```typescript
export class CheckoutPage {
  constructor(private page: Page) {}
  readonly total = this.page.getByTestId('total-price');
  readonly pay = this.page.getByRole('button', { name: 'Pay' });

  async removeItem(name: string) {
    await this.page.getByRole('listitem').filter({ hasText: name })
      .getByRole('button', { name: 'Remove' }).click();
  }
}
```

- Expose **locators**, not `getTotal(): Promise<string>` accessors — the caller keeps retrying assertions.
- No assertions inside page objects except an explicit `expectX()` method; a page object that asserts hides which check failed.
- No conditional branching on page state inside the object; that is the test's decision.
- Hand the object out through a fixture rather than constructing it in every test: one place changes when the constructor grows a dependency.

## Data Strategy

| Approach | Use when | Cost |
|---|---|---|
| Create via API in a fixture | Default | Fast, isolated, needs API access |
| Seed script before the run | Read-only reference data | Shared state risk if tests mutate it |
| Create through the UI | The creation flow is what is under test | Slowest, couples every test to that flow |
| Fixed test accounts | Legacy systems with no provisioning API | Needs per-worker allocation (`auth.md`) |

Unique-value rule: derive from `workerInfo.parallelIndex` plus a timestamp, never a bare `Date.now()` — two workers starting in the same millisecond collide on a unique constraint, and that failure looks exactly like flake.

Cleanup belongs to the fixture that created the record, in the teardown half after `use()`. A test that deletes data it did not create is the polluter in someone else's failure.
