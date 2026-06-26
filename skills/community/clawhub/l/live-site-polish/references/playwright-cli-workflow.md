# Playwright CLI Workflow

Use `playwright-cli` as the default control plane for live page editing.

For this skill, `playwright-cli` is not just preferred, it is required. Do not mix in other browser tools during the same task.

If `playwright-cli` actions start timing out, try:

```bash
export PLAYWRIGHT_MCP_TIMEOUT_ACTION=30000
```

Default to headless operation. Use `--headed` only when the user must intervene directly.

## Session Start

Before exploration, choose an output directory for the task and create `<output>/tmp/`. Use that `tmp/` directory as the default destination for temporary screenshots, draft scripts, and review artifacts.

Run these as separate commands, not a chained shell line:

```bash
playwright-cli open
playwright-cli goto https://example.com
playwright-cli snapshot
```

If you hit login, MFA, CAPTCHA, or another manual checkpoint, switch to:

```bash
playwright-cli open --headed
```

Then ask the user to take over for that step and continue after they finish.

If the user wants the current page preserved, still run `playwright-cli open` once, then inspect the existing tab before deciding whether `goto` is safe.

If a runtime already provided a browser session, `playwright-cli open` is still the session bootstrap step. Run it once, then keep using that same session.

## Core Loop

Use this loop repeatedly:

1. Inspect current state

```bash
playwright-cli snapshot
```

Prefer `snapshot` for structure checks and `screenshot` for visual checks.

2. Move to the target area

```bash
playwright-cli mousewheel 0 900
```

3. Capture a review image

```bash
playwright-cli screenshot --filename <output>/tmp/after-round-1.png
```

4. Apply a small patch

```bash
playwright-cli run-code "async page => {
  await page.evaluate(() => {
    const target = document.querySelector('[data-test=\"hero\"]');
    if (!target) return;
    target.style.maxWidth = '1200px';
  });
}"
```

5. Review or iterate

- compare screenshots
- check the latest snapshot
- self-check alignment, centering, padding, and spacing before sending anything to reviewer
- decide whether to refine or send to independent review

## Patch Guidance

- Keep each patch small enough to reason about.
- Namespace added elements or classes when possible, for example `ux-live-design-*`.
- Prefer `page.evaluate()` DOM edits and scoped `<style>` injection.
- Capture a new screenshot after each meaningful refinement.
- Do not use `run-code` to dump whole-page HTML or crawl the full DOM when a focused query is enough.
- Use `run-code` for targeted inspection such as `getComputedStyle`, `getBoundingClientRect`, visibility checks, and `scrollIntoView`.
- Use targeted inspection to verify centering and spacing facts when they matter, for example: parent width vs child width, left/right padding symmetry, flex/grid alignment, and text alignment.

## Self-Check Before Review

Before you hand a round to the reviewer, verify both:

1. Code-level signals
   - computed padding and margin are plausible
   - alignment properties match the intended layout
   - bounding boxes place the element where you expect
2. Screenshot-level signals
   - the block actually looks centered if it should be centered
   - spacing looks even, not accidentally lopsided
   - there is no obvious oversized padding or awkward gap

## Direction Selection

Before the first real patch:

1. Explore the page and inspect the target area
2. Write 3 clearly different design directions
3. Ask the user to pick one unless the task explicitly says to choose autonomously
4. Implement only the chosen direction

Do not build 3 variants in the page at once.

## Before/After Capture

Use clean captures:

- `before`: after exploration and popup cleanup, before any live modifications
- `after`: after the latest refinement round or after the final accepted version

If the target area is below the fold, center it in the viewport before each capture so the comparison is obvious.

If the target area is dynamic, freeze both captures to the same state:

- same carousel slide
- same tab or accordion state
- same video poster or paused frame
- same timer or banner state when possible

If necessary, pause autoplay, click to the same slide, or reopen the same panel before both captures.

## Failure Handling

- If the page gets into a bad temporary state, reload only when that will not destroy important session state.
- If the page requires login and reloading is risky, continue from the current session and keep patches local to the visible area.
- If the site is inaccessible or heavily canvas/video driven, stop early and state that the page is not a good fit for this skill.
- If the task is blocked on a manual checkpoint, do not thrash in headless mode. Switch to `--headed`, let the user complete the checkpoint, then resume.

## Large Patches

If the patch exceeds roughly 20 lines of JavaScript, move it into a standalone `.js` file instead of keeping it inline in a shell command. This avoids quoting, escaping, and newline corruption.

Save those draft scripts under `<output>/tmp/` until the result passes review.

## Patch Hygiene

- If you reload the page, you can usually assume previous runtime injections are gone.
- If you do not reload, clean up old injected nodes and style tags before starting a fresh attempt unless you explicitly mean to build on the current mutated state.
- Prefer stable IDs or `data-*` markers so cleanup is deterministic.

## Known CLI Pitfalls

- `snapshot` is accessibility-tree oriented, not a DOM dump. Search by visible text and roles, not CSS selectors.
- Take a fresh `snapshot` after navigation or a meaningful state change before grepping `.playwright-cli/page-*.yml`, otherwise you may inspect stale YAML.
- `mousewheel` has a known argument quirk in some environments. The first numeric argument is the vertical movement. Use `mousewheel <y> 0` for normal scrolling.
- If two cycles of scroll plus snapshot still do not show the target, take a full-page screenshot before guessing.
- Use `run-code` to return to the top reliably:

```bash
playwright-cli run-code "async page => {
  await page.evaluate(() => window.scrollTo(0, 0));
}"
```

- If the page state does not change after a click or scroll, suspect a blocking popup or stale focus state before assuming your patch failed.

## Output Timing

- Temporary screenshots, draft notes, and draft scripts should live under `<output>/tmp/` during iteration.
- Final handoff files should be organized only after the review loop reaches its stopping condition.
