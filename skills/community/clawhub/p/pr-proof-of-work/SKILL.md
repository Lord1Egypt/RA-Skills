---
name: tdd-e2e-pr-workflow
description: >
  TDD-driven E2E workflow with real Playwright browser screenshots as PR proof.
  Use when: (1) fix bugs or implement features with test-first approach,
  (2) create PRs with visual before/after proof from E2E tests,
  (3) generate Playwright E2E tests with BEFORE/AFTER screenshots from real browser,
  (4) post screenshot comparisons as PR comments on GitHub.
  Workflow: pick one open issue → write E2E test → implement fix → PR with screenshots.
  Process ONE issue at a time. Complete current PR before starting next.
  NEVER use page.setContent() — always test through the real application.
  Triggers: "tdd e2e", "screenshot pr", "before after screenshot", "visual pr proof",
  "e2e pr workflow", "issue to pr with screenshots", "playwright tdd".
---

# TDD E2E PR Workflow

One Issue → One PR with visual proof.

**Flow**: Select one issue → Write test (BEFORE screenshot) → Fix → Test passes (AFTER screenshot) → PR with screenshot comment.

**Golden Rule**: Study ≥2 existing PASSING tests before writing any new test. Wrong fixture/selector usage is #1 failure cause.

---

## Phase 0: Select One Issue

Choose an open issue to work on, or pick randomly:

```bash
# Option A: List and manually select
gh issue list --repo <owner/repo> --state open --json number,title,body

# Option B: Pick one randomly
gh issue list --repo <owner/repo> --state open --json number,title | \
  jq -r '.[] | "\(.number): \(.title)"' | shuf -n 1
```

1. Note the issue number and create a short kebab-case slug from title (e.g. "fix-discard-button")
2. Create isolated worktree:
   ```bash
   git worktree add .worktrees/fix/<slug> -b fix/<slug>
   cd .worktrees/fix/<slug>
   ```
3. Copy [screenshot-reporter.ts](assets/screenshot-reporter.ts) into the worktree's e2e/ directory (not tracked on fix branches)
4. Set screenshot output:
   ```bash
   export E2E_SCREENSHOT_DIR="$(pwd)/e2e-screenshots"
   ```

---

## Phase 1: Write Real Browser Test

### Step A: Study existing tests (MANDATORY)

Read ≥2 passing E2E tests to understand:
- Fixture API (`withProject`, `withSession`, `gotoSession`, `sdk`)
- Action helpers (`waitSessionIdle`, `runTerminal`, `openSettings`)
- Selector patterns (data-component, data-slot, ARIA roles)
- Data seeding (`apply_patch`, terminal commands, SDK methods)

### Step B: Write test with BEFORE screenshot

```typescript
import { test, expect } from "../fixtures"
import { createScreenshotReporter } from "../screenshot-reporter"

test("feature description", async ({ page, withProject }) => {
  const screenshot = createScreenshotReporter(page, "test-name")

  await withProject(async (project) => {
    // ... setup using project's fixture patterns ...
    await screenshot.captureBefore("initial-state")
    // ... assertions ...
  })
})
```

**Playwright TS transform gotcha** — rejects inline object params:
```typescript
// WRONG: fs.mkdirSync(dir, { recursive: true })
// RIGHT:
const opts = { recursive: true }
fs.mkdirSync(dir, opts)
```
Apply to ALL object literals: `fs.mkdirSync`, `page.screenshot`, `page.waitForFunction`, etc.

---

## Phase 2: Implement Fix

Write minimum code to pass. Do NOT modify test assertions.

### Debugging loop (most tests need 2-4 iterations):

1. **Read error carefully** — 90% are selector/fixture mismatches, not logic bugs
2. **Verify DOM** — use `page.waitForSelector` or `page.waitForFunction` to confirm elements exist
3. **Check prerequisites** — hover before clicking, expand before asserting, wait for idle
4. **Use `page.pause()`** to inspect live DOM
5. **Never weaken assertions** — fix the code, not the test

### Common failure patterns (see [references/debugging-guide.md](references/debugging-guide.md)):

| Symptom | Likely Cause | Fix |
|---|---|---|
| Timeout on selector | Wrong data attribute or shadow DOM | Check DOM with `page.pause()`, try ARIA roles |
| `waitMark` never resolves | Seed function missing expected content | Match seed format exactly from passing tests |
| Button not visible | Missing hover/expand step | Hover parent row, expand section first |
| Review panel empty | Wrong changes mode (git vs session) | Switch mode before asserting |
| Stale element reference | Race condition with async updates | Add `waitSessionIdle` after mutations |

---

## Phase 3: AFTER Screenshot + Hard Gate

```typescript
  await expect(fixedElement).toBeVisible()
  await screenshot.captureAfter("feature-working")
```

**Hard gate** — ALL three must be true before PR:
- Test passes (exit code 0)
- `BEFORE-*.png` exists
- `AFTER-*.png` exists

---

## Phase 4: PR + Screenshot Comment

```bash
# Stage, commit, push
git add -A
git commit -m "fix: <issue-description> (closes #<issue-number>)"
git push origin fix/<slug>

# Create PR referencing the issue
gh pr create \
  --title "fix: <short-description>" \
  --body "Closes #<issue-number>

## Summary
<Brief description of the fix>

## Screenshots
| Before | After |
|--------|-------|
| ![Before](<BEFORE-screenshot-url>) | ![After](<AFTER-screenshot-url>) |

## Verification
- [x] E2E test passes
- [x] BEFORE screenshot captured
- [x] AFTER screenshot captured" \
  --repo <owner/repo>

# Push screenshots to branch for GitHub raw URLs
git add e2e-screenshots/
git commit -m "chore: add e2e screenshots"
git push origin fix/<slug>
```

`gh pr comment` has no `--attach` — push images to branch, use raw GitHub URLs.

---

## Backend-Only PRs

For PRs without direct UI changes, find the closest UI-exercisable path:

| Change Type | E2E Strategy | Real Example |
|---|---|---|
| Config utility | Open settings dialog | `openSettings(page)` → screenshot config panel |
| Python resolver | Run terminal command | `runTerminal(page, {cmd: "python3 --version"})` → show output |
| Race condition | Trigger rapid operations | Create file externally → click refresh → verify |
| State management | Multi-session switching | Select file in session A → switch to B → back to A |
| Cache bypass | Force refresh | Add external file → click refresh button → verify |
| URL parsing | Check connection status | `openStatusPopover(page)` → verify connected |
| Focus management | Verify focus after action | Open file → check prompt still focused |

**NEVER use `page.setContent()`** — always test through the real application.

---

## Quick Reference

```bash
# Select an issue (manual or random)
gh issue list --repo owner/repo --state open --json number,title

# Create worktree
git worktree add .worktrees/fix/ISSUE -b fix/ISSUE
cd .worktrees/fix/ISSUE

# Set screenshot dir
export E2E_SCREENSHOT_DIR="$(pwd)/e2e-screenshots"

# Run E2E test
npm run test:e2e -- <test-file>

# Push and create PR
git push origin fix/ISSUE
gh pr create --title "fix: ..." --body "Closes #N" --repo owner/repo
```

---

## Constraints

- **One issue at a time** — complete one PR before starting the next
- BEFORE and AFTER must BOTH exist before PR comment — hard gate, no exceptions
- Screenshots save to worktree via `E2E_SCREENSHOT_DIR`, never to main repo
- Always study ≥2 passing tests first — this is the #1 rule
- NEVER use `page.setContent()` — real app only
- Playwright TS transform rejects inline object params — always extract to variable
- `screenshot-reporter.ts` must be copied to each worktree's e2e/ (not on fix branches)
- Test MUST pass before PR — never create PR with failing tests
