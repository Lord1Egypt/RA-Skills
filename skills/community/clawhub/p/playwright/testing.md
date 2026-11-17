# Testing — What Earns A Test, And How To Assert It

Which tests are worth their runtime, and the assertion craft that decides whether a green run means anything. Config and projects: `config.md`. Fixtures, page objects, and data: `fixtures.md`. Login flows: `auth.md`. Mocks: `network.md`.

## What Earns An E2E Test

| Test it end to end | Test it cheaper |
|---|---|
| Signup, login, permission boundaries | Field-level validation rules |
| Checkout and payment (against a sandbox) | Currency formatting |
| Upload → process → download round trip | File-parser edge cases |
| Multi-step flows with server state between steps | Component render states |
| Anything a regression would cost real money | Copy, spacing, hover styles |
| The one integration you cannot mock away | Everything you can mock away |

Cost model: an E2E test costs its runtime **every run, forever**, plus its share of maintenance on every UI change. A 20-second test in a suite that runs 40 times a day is 13 minutes of machine time daily — worth it for checkout, absurd for a tooltip.

## Structure And Assertions

```typescript
import { test, expect } from '@playwright/test';

test.describe('Checkout', () => {
  test.beforeEach(async ({ page }) => { await page.goto('/products'); });

  test('completes purchase with a valid card', async ({ page }) => {
    await test.step('add to cart', async () => {
      await page.getByRole('listitem').filter({ hasText: 'Product A' }).click();
      await page.getByRole('button', { name: 'Add to Cart' }).click();
    });
    await page.getByRole('link', { name: 'Checkout' }).click();
    await expect(page.getByRole('heading', { name: 'Order Summary' })).toBeVisible();
    await expect(page).toHaveURL(/\/checkout/);
  });
});
```

`test.step` costs one line and turns a 30-step failure in the report into a named stage — the difference between "checkout test failed" and "failed while adding to cart".

Assertion vocabulary worth knowing beyond `toBeVisible`:

```typescript
await expect(rows).toHaveCount(3);
await expect(rows).toHaveText([/Alice/, /Bob/]);          // whole list, ordered
await expect(input).toHaveValue('42');
await expect(button).toBeDisabled();
await expect(banner).toHaveAttribute('role', 'alert');
await expect(el).toHaveCSS('background-color', 'rgb(255, 0, 0)');
await expect(page.getByText('Deleted')).toBeHidden();     // not .not.toBeVisible() for "gone"
await expect.soft(price).toHaveText('$42');               // record and continue
expect(test.info().errors).toHaveLength(0);               // after soft assertions, if you need the gate
```

`toBeHidden()` passes for missing **or** invisible; `not.toBeVisible()` passes for the same set but reads as a negation and tempts a race. Prefer the positive form of what you mean.

Soft assertions are for report quality — checking five fields on one page and reporting all failures — never for skipping a hard gate.

## Asserting The Outcome, Not The Action

The passing test that hides a broken feature always has the same shape: it asserts that something was clicked, requested, or rendered, never that the user got what they came for.

| Weak assertion | What it misses | Assert instead |
|---|---|---|
| `await expect(saveButton).toBeVisible()` after clicking Save | The save failed server-side | The saved value after a reload, or the success state the server drives |
| `await expect(page).toHaveURL(/\/orders/)` alone | The order list is empty or errored | The new order's row, by its own identifier |
| `expect(response.ok()).toBeTruthy()` | The UI never showed it | The rendered consequence of that response |
| A count that matches whatever rendered | Fixture drift; the seed changed | A count derived from what the test itself created |

## Skipping A Case On Purpose

```typescript
test.skip(browserName === 'webkit', 'clipboard API is Chromium-only');   // conditional, with a reason
test.fixme('drag handle drops on Firefox');                               // known broken: does not run, stays visible
test('legacy import fails', { annotation: { type: 'issue', description: 'PROJ-812' } }, async () => {
  test.fail();                                                            // must fail; passing turns the test red
});
```

- `test.skip(condition, reason)` is the mechanism for engine or environment exclusions (`browsers.md`) — the reason string is what stops it from becoming permanent.
- `test.fixme` says "this should work and does not"; unlike a commented-out test, it stays in the report as a number someone can watch.
- `test.fail()` asserts a known failure and flips red when the bug is fixed — the only annotation that tells you to delete it.
- A skip with no condition and no reason is a deleted test with extra steps.

## Component Tests

Playwright can mount components directly (an experimental part of the runner). It fits when a component has real browser behavior — drag, focus trapping, canvas, intersection observers — and a JSDOM-based runner keeps lying to you. It does not replace journey tests, and it costs a second toolchain in the repo: adopt it only for the components where JSDOM actually failed you.
