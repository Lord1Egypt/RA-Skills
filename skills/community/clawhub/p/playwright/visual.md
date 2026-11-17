# Visual — Screenshots and Snapshot Testing

Visual tests catch what assertions cannot see and fail for reasons that have nothing to do with your app. Determinism first, coverage second.

## The Assertion

```typescript
await expect(page).toHaveScreenshot('dashboard.png');
await expect(page.getByTestId('chart')).toHaveScreenshot('chart.png');   // element, not page
```

`toHaveScreenshot` re-captures until **two consecutive screenshots are identical**, then compares to the baseline — that built-in stability wait is why it beats `page.screenshot()` plus a manual diff. Its defaults also hide the text caret and disable CSS animations, which `page.screenshot()` does not.

First run with no baseline: the file is written and the test **fails** (by design, so CI can never green-light an unreviewed baseline). Commit it after looking at it.

Pixels are not the only snapshot: `toMatchAriaSnapshot` (playwright >=1.49) freezes structure — roles, names, nesting — and survives every restyle that breaks a screenshot. When the regression you fear is "the button stopped being a button", that is the cheaper assertion (`accessibility.md`); reach for pixels only when the rendering itself is the product.

## Comparison Knobs

| Option | Default | Use |
|---|---|---|
| `threshold` | 0.2 | Per-pixel color distance (YIQ) before a pixel counts as different; lower is stricter |
| `maxDiffPixels` | unset | Absolute tolerance — the right knob for known antialiasing noise |
| `maxDiffPixelRatio` | unset | Proportional tolerance, better across varying element sizes |
| `mask` | `[]` | Locators painted over before comparing — timestamps, avatars, ads |
| `animations` | `'disabled'` | Freezes CSS animations and transitions |
| `fullPage` | `false` | Whole scrollable page; lazy-loaded content below the fold makes this fragile |
| `clip` | unset | A fixed rectangle when you cannot target an element |
| `stylePath` | unset | A stylesheet injected before capture — the cleanest place to kill animations globally |

```typescript
await expect(page).toHaveScreenshot('feed.png', {
  mask: [page.getByTestId('timestamp'), page.getByRole('img', { name: 'avatar' })],
  maxDiffPixelRatio: 0.01,
});
```

Set the tolerance to the noise you have measured, not to whatever makes today's run pass. A `maxDiffPixels` large enough to hide a missing button is worse than no visual test.

## Why It Passes Locally And Fails In CI

Snapshot files are keyed by **project and platform** (`dashboard-chromium-darwin.png` vs `-linux.png`), so a macOS baseline is simply absent on a Linux runner — the failure says the snapshot is missing, not that the UI changed.

| Cause | Fix |
|---|---|
| Different platform | Generate baselines in the CI image: run the official Docker image locally and `--update-snapshots` there |
| Fonts not installed on the runner | Install the same font set in the image, or use a font stack the image ships |
| Device pixel ratio | Pin `deviceScaleFactor` in the project |
| Scrollbar rendering | Overlay scrollbars on macOS take no space; Linux ones do — prefer element screenshots over full page |
| GPU / rasterization differences | Small antialiasing deltas: `maxDiffPixels` in the low hundreds, not a raised `threshold` |
| Dynamic content | Mask it, freeze the clock (`page.clock.setFixedTime`, playwright >=1.45), seed fixed data |

`snapshotPathTemplate` in the config controls the naming when you want one baseline shared across projects — only safe if the render is genuinely identical.

## Updating Baselines

```bash
npx playwright test --update-snapshots                 # all
npx playwright test path/to/spec.ts -g "dashboard" -u  # one
```

Review the image diff in the HTML report before accepting: the report shows expected, actual, and diff side by side. Blind `-u` after a failure converts a regression into a new baseline — the single way a visual suite becomes worthless.

## Where Visual Testing Pays

| Good target | Poor target |
|---|---|
| A design-system component gallery | A full page of user-generated content |
| A chart or canvas with no DOM to assert | Text content — assert the string instead |
| Print or PDF layout | Anything with live data and no mask |
| Empty, error, and loading states | Pages with third-party embeds |
| Dark mode and RTL renderings | Animation mid-states |

Rule of thumb: screenshot the smallest element that can regress. Full-page snapshots fail on every unrelated change and train the team to press `-u`.

## Non-Visual Screenshots

For bug reports, docs, and PR evidence, plain captures are enough:

```typescript
await page.screenshot({ path: 'bug.png', fullPage: true });
await page.getByRole('dialog').screenshot({ path: 'dialog.png' });
await page.screenshot({ path: 'shot.png', style: '.cookie-banner { display: none }' });
```

`page.screenshot` does **not** disable animations by default (unlike `toHaveScreenshot`), so pass `animations: 'disabled'` when the result must be stable. Attach captures to the report with `testInfo.attach` instead of writing loose files nobody finds. Broader capture craft — simulators, desktop windows, marketing shots — is the `screenshot` skill.
