# Accessibility — Automated Scans and Keyboard Paths

Automated scanning catches a minority of real barriers — Deque's own figure for axe-core is around 57% of issues found automatically. Treat the scan as the floor and keyboard plus screen-reader semantics as the actual test.

## Scanning With axe

```typescript
import AxeBuilder from '@axe-core/playwright';

test('dashboard has no critical a11y violations', async ({ page }) => {
  await page.goto('/dashboard');
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
    .analyze();
  expect(results.violations).toEqual([]);
});
```

Scoping and triage:

```typescript
new AxeBuilder({ page })
  .include('#main')                       // scan one region
  .exclude('.third-party-widget')         // an embed you cannot fix
  .disableRules(['color-contrast'])       // temporarily, with a linked issue
```

- Scan **states**, not just routes: open the modal, expand the menu, trigger the error, then analyze. Most violations live in states a route-level scan never renders.
- Adopting on a legacy app: snapshot the current violations as a baseline and fail only on new ones (`expect(results.violations.length).toBeLessThanOrEqual(baseline)`), then ratchet the number down. A first run demanding zero gets the whole check deleted.
- Attach the violation list to the report: `testInfo.attach('axe', { body: JSON.stringify(results.violations, null, 2), contentType: 'application/json' })` — a failure that names the rule and the node is actionable; a bare count is not.

## What The Scan Cannot See

| Barrier | How to test |
|---|---|
| Focus order that jumps around the page | Tab through and assert the sequence (below) |
| Focus lost after a modal closes | Assert focus returns to the trigger |
| A keyboard trap inside a widget | Tab N times and assert you escaped |
| A label that is present but meaningless ("click here") | Human review, or a lint rule on the copy |
| Live-region announcements | Assert `role="status"`/`aria-live` content changes |
| Contrast on a background image | Human review |
| Whether the flow is usable at all with a screen reader | Manual pass; no tool substitutes |

## ARIA Snapshots — Structure As An Assertion

`toMatchAriaSnapshot` (playwright >=1.49) freezes the accessibility tree of a region as YAML: roles, accessible names, and nesting.

```typescript
await expect(page.getByRole('navigation')).toMatchAriaSnapshot(`
  - list:
    - listitem:
      - link "Home"
    - listitem:
      - link /Sign (in|out)/
`);

await expect(page.getByRole('dialog')).toMatchAriaSnapshot({ name: 'checkout-dialog.aria.yml' });
```

- It fails on the regressions a scan and a screenshot both miss: a heading demoted to a `div`, a button that lost its accessible name, a menu item that appeared, an order that changed. It passes through a pure restyle.
- Scope it to the smallest meaningful region — nav, dialog, menu, table, a design-system component. A whole-page tree churns on every copy change and gets `-u`'d blind, which is the same failure mode as full-page screenshots (`visual.md`).
- Generate with `--update-snapshots` and read the YAML like code: it is the machine's transcript of what a screen reader will announce, and an unreviewed baseline freezes today's bugs.
- Regexes match names, and omitted children are allowed — the snapshot asserts what it lists, so a partial tree is a legitimate, lower-churn assertion.

## Keyboard Assertions

```typescript
await page.keyboard.press('Tab');
await expect(page.getByRole('link', { name: 'Skip to content' })).toBeFocused();

for (const name of ['Email', 'Password', 'Sign in']) {
  await page.keyboard.press('Tab');
  await expect(page.getByRole(/button|textbox/, { name })).toBeFocused();
}

await page.getByRole('button', { name: 'Open settings' }).click();
await page.keyboard.press('Escape');
await expect(page.getByRole('button', { name: 'Open settings' })).toBeFocused();   // focus returned
```

Use `ControlOrMeta` for shortcuts so the test survives both macOS and Linux runners. `page.keyboard.press('Shift+Tab')` covers backward order, where most focus bugs hide.

## Semantics You Get For Free

Every `getByRole` locator is an accessibility assertion in disguise: if the role-and-name locator cannot find the control, a screen reader cannot announce it either. Writing the suite with role-based locators (`selectors.md`) means a regression in accessible naming breaks a test before anyone files a ticket — the strongest argument for semantic locators over test IDs.

`await page.getByRole('button', { name: 'Save' })` failing after a refactor to `<div onclick>` is exactly the signal you want.

## Where To Run It

- One a11y spec per major surface, tagged `@a11y`, in the PR gate — the scan takes about as long as a page load.
- Component libraries: scan each component's states in the component suite; it is cheaper and catches issues before they multiply across pages.
- Do not scan every page in every test; duplicate violations flood the report and nobody reads it twice.
- A violation baseline and an ARIA snapshot are both dated artifacts: put their review on a schedule (the `Cadence` preference area, gates in `ci-cd.md`), or the ratchet stops ratcheting and nobody notices.
