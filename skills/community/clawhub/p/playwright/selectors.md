# Selectors — Locating Exactly One Element

A locator is a lazy description, not a node: it re-resolves at every action, so storing one in a variable is safe across re-renders. An `ElementHandle` is the opposite — a pointer to a node that a re-render detaches. Default to locators; reach for handles only when you need the raw DOM node.

Contents: [Decision Order](#decision-order) · [Matching Rules Nobody Reads](#matching-rules-nobody-reads) · [Narrowing To One](#narrowing-to-one) · [Iterating A List](#iterating-a-list) · [Frames](#frames) · [Shadow DOM](#shadow-dom) · [Dynamic And Generated Markup](#dynamic-and-generated-markup) · [Common Mistakes](#common-mistakes)

## Decision Order

| Priority | API | Use when | Cost of change |
|---|---|---|---|
| 1 | `getByRole(role, { name })` | The element has an accessible name a user can read | Breaks only when the UI genuinely changed for users |
| 2 | `getByLabel` / `getByPlaceholder` | Form fields | Breaks with copy changes — usually correct |
| 3 | `getByText` / `getByAltText` / `getByTitle` | Static content, images | Copy-sensitive; use regex for volatile strings |
| 4 | `getByTestId` | Icon buttons, rows, canvas, anything with no accessible name | Never breaks, asserts nothing about users |
| 5 | `locator('[data-product-id="123"]')` | A stable semantic attribute exists | Fine |
| 6 | `locator('.css-1a2b3c')`, XPath, `nth-child` | Last resort, with a comment saying why | Breaks on the next refactor |

```typescript
page.getByRole('button', { name: 'Submit' })
page.getByRole('link', { name: /sign up/i })
page.getByRole('heading', { level: 1 })
page.getByRole('textbox', { name: 'Email' })
page.getByLabel('Email address')
page.getByTestId('checkout-button')          // configure: use: { testIdAttribute: 'data-testid' }
```

## Matching Rules Nobody Reads

- `getByText('Log in')` is **substring and case-insensitive** by default. It matches "Log in with Google" too. `{ exact: true }` makes it whole-string **and** case-sensitive.
- `getByRole(..., { name })` matches the **whole accessible name**, case-insensitively, with whitespace normalized. A trailing icon with `aria-label` becomes part of that name — inspect the real name in the trace before guessing.
- Regex options behave differently: `exact` is ignored for regex, and `/log in/i` on `getByText` still matches substrings.
- Whitespace across line breaks is normalized in text matching, so copy indented in the template still matches.
- `getByRole` reads the **accessibility tree**, so `display: none` and `aria-hidden` elements are invisible to it — that is a feature: if the locator cannot find it, a screen reader could not either.

## Narrowing To One

Strict mode makes multiple matches an error on purpose. Narrow, do not index.

```typescript
page.getByRole('listitem').filter({ hasText: 'Product A' })
page.getByRole('row').filter({ has: page.getByRole('button', { name: 'Remove' }) })
page.getByRole('row').filter({ hasNotText: 'Archived' })
page.getByTestId('cart').getByRole('button', { name: 'Remove' })   // scope by parent
page.getByRole('button', { name: 'Save' }).and(page.locator('[data-primary]'))
page.getByRole('alert').or(page.getByRole('status'))               // whichever the app renders
```

`.first()`, `.last()`, `.nth(i)` are legitimate in exactly one case: position is the behavior under test ("the first result is the sponsored one"). Anywhere else they encode an accidental DOM order.

Debugging an over-broad locator: `await page.getByRole('button').count()` in the Inspector, or the strict-mode error itself — it prints every match with its text.

## Iterating A List

```typescript
const rows = page.getByRole('row');
await expect(rows).toHaveCount(5);            // retries — do this FIRST
for (const row of await rows.all()) { ... }   // snapshot, no auto-wait, safe only after the assert
await expect(rows).toHaveText([/Alice/, /Bob/]);   // whole list in one retrying assertion
```

`all()` and `$$eval` never wait. Without the `toHaveCount` gate, a slow render returns zero rows and the loop passes vacuously — the single most common false-green in extraction and table tests.

## Frames

Locators pierce **open shadow DOM automatically** but **never cross an iframe boundary**.

```typescript
const checkout = page.frameLocator('iframe[name="checkout"]');
await checkout.getByRole('button', { name: 'Pay' }).click();

page.frameLocator('iframe[src*="stripe"]').getByLabel('Card number').fill('4242...');

const frame = await page.locator('iframe.embed').contentFrame();   // handle-style access
```

- Payment, captcha, video, and consent widgets are almost always iframes — `Timeout ... waiting for locator` with a visibly present element is this, 9 times out of 10.
- Nested iframes chain: `page.frameLocator('#outer').frameLocator('#inner')`.
- A frame that reloads invalidates in-flight actions; assert on something inside the frame before interacting.
- Cross-origin frames are fine for Playwright (unlike some runners) — no special flag needed.

## Shadow DOM

```typescript
page.locator('my-component').getByRole('button', { name: 'Open' })   // open roots: transparent
```

Closed shadow roots are invisible to every locator and to `page.evaluate` traversal. Options: ask the team to open the root in test builds, use the component's public API through `evaluate` on the host, or test one layer up at the behavior level.

## Dynamic And Generated Markup

| Situation | Locator |
|---|---|
| Class names hashed by CSS-in-JS | Role or test ID; never the hash |
| Virtualized list (only ~20 rows in DOM) | Scroll the container, then filter by text; `toHaveCount` on the full list will never pass |
| Text includes a live counter ("Inbox (3)") | `getByRole('link', { name: /^Inbox/ })` |
| Element identified only by position in a grid | Scope by an ancestor with a stable label, then `nth` inside that scope |
| Locale-dependent copy | Locate by role plus test ID; assert the copy separately |
| Element appears twice (mobile + desktop layout) | Scope to the visible container, or filter `{ visible: true }` via `locator(..., { hasText })` on the shown wrapper |

## Common Mistakes

| Mistake | Better |
|---|---|
| `page.locator('button').click()` | `page.getByRole('button', { name: 'Submit' })` |
| `page.getByTestId('product-card').first()` | `.filter({ hasText: 'Product A' })` |
| `nth-child(3)` | Filter by text, role, or parent context |
| `//div[@class="xyz"]/span[2]` | Role or test ID |
| `page.locator('iframe').getByRole(...)` | `page.frameLocator('iframe').getByRole(...)` |
| Storing `await page.$('.row')` and reusing it | Store the locator, not the handle |
