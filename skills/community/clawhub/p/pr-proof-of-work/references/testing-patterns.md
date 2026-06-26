# Testing Patterns — Lessons from 13 Real E2E Tests

Patterns extracted from running 13 Playwright E2E tests across different PR types (UI, backend, config, race conditions).

## Table of Contents

- [Data Seeding Patterns](#data-seeding-patterns)
- [Navigation Patterns](#navigation-patterns)
- [Selector Strategies](#selector-strategies)
- [Timing & Wait Patterns](#timing--wait-patterns)
- [Backend PR Test Strategies](#backend-pr-test-strategies)
- [Review Panel Patterns](#review-panel-patterns)
- [File Tree Patterns](#file-tree-patterns)
- [Common Pitfalls](#common-pitfalls)

---

## Data Seeding Patterns

### Via `apply_patch` (AI prompt)

Used by: upload-improve, ai-visible-undo, doc-shortname, md-render-opt

```typescript
async function patch(sdk, sessionID, patchText) {
  await sdk.session.promptAsync({
    sessionID,
    agent: "build",
    system: [
      "You are seeding deterministic e2e UI state.",
      "Your only valid response is one apply_patch tool call.",
      `Use this JSON input: ${JSON.stringify({ patchText })}`,
      "Do not call any other tools. Do not output plain text.",
    ].join("\n"),
    parts: [{ type: "text", text: "Apply the provided patch exactly once." }],
  })
  // CRITICAL: must wait for session to finish processing
  await waitSessionIdle(sdk, sessionID, 120_000)
}
```

Seed format:
```
*** Begin Patch
*** Add File: src/index.ts
+line 01 mark-value
+line 02 mark-value
*** End Patch
```

**Must include a unique mark line** for `waitMark()` to find in the DOM:
```
+title mark-value
+mark mark-value        ← this is what waitMark looks for
+line 01 mark-value
```

### Via terminal commands

Used by: windows-python, refresh-button, file-management

```typescript
import { runTerminal, waitTerminalReady } from "../actions"

await runTerminal(page, {
  cmd: "python3 --version",
  token: "python3",    // wait for this in output
  timeout: 10_000,
})
```

### Via external file creation

Used by: file-management, refresh-button

```typescript
await page.evaluate(async (dir) => {
  const fs = require("fs")
  const path = require("path")
  const filePath = path.join(dir, "new-file.txt")
  const content = "created externally"
  fs.writeFileSync(filePath, content)
}, projectDirectory)
```

---

## Navigation Patterns

### Open file via `/open` command

Used by: pdf-reader, pdf-focus-translate, md-render-opt

```typescript
// Open the slash command palette
const prompt = page.locator('[data-component="prompt-input"]')
await prompt.click()
await page.keyboard.type("/open")

// Wait for search dialog
await page.waitForSelector('[data-slot="command-palette"]')

// Type filename to search
await page.keyboard.type("test.pdf")

// Click the matching file item
const fileItem = page.locator('[data-slot="command-palette"] [role="option"]').first()
await fileItem.click()

// Wait for file tab to appear
await page.waitForSelector('[data-slot="session-tab"][data-active="true"]')
```

### Session switching

Used by: session-mixing

```typescript
// Create two sessions
await withSession(sdk, "session-a", async (sessionA) => {
  await withSession(sdk, "session-b", async (sessionB) => {
    // Navigate to session A
    await gotoSession(sessionA.id)
    // ... interact with A ...
    // Navigate to session B
    await gotoSession(sessionB.id)
    // ... interact with B ...
    // Navigate back to A
    await gotoSession(sessionA.id)
  })
})
```

### Open settings dialog

Used by: opencode-rename

```typescript
import { openSettings } from "../actions"

const dialog = await openSettings(page)
await expect(dialog.getByText("General")).toBeVisible()
```

### Open status popover

Used by: url-launch

```typescript
import { openStatusPopover } from "../actions"

const { popoverBody } = await openStatusPopover(page)
// Verify server connection status
```

---

## Selector Strategies

### Priority order (most robust first):

1. **ARIA roles** — `getByRole("button", { name: "Refresh" })`
2. **data-component** — `[data-component="prompt-input"]`
3. **data-slot** — `[data-slot="session-tab"]`
4. **data-file** — `[data-file="test.ts"]`
5. **getByText** — `page.getByText("Upload file here")`
6. **CSS classes** — LAST RESORT only (fragile)

### Shadow DOM handling

Some components use shadow DOM (e.g., `diffs-container`):
```typescript
// WRONG: page.locator("diffs-container .content") — can't pierce shadow
// RIGHT:
await page.waitForFunction(
  ({ file, mark }) => {
    const view = document.querySelector(".scroll-view__viewport")
    const head = Array.from(view.querySelectorAll("h3")).find(
      (n) => n.textContent?.includes(file)
    )
    const host = head?.parentElement?.querySelector("diffs-container")
    return host?.shadowRoot?.textContent?.includes(`mark ${mark}`)
  },
  { file, mark },
  { timeout: 60_000 }
)
```

### Markdown table selectors

Markdown is rendered in regular DOM, NOT shadow DOM:
```typescript
// WRONG: page.locator("table td") — may not match rendered structure
// RIGHT:
await expect(page.getByRole("columnheader", { name: "Feature" })).toBeVisible()
await expect(page.getByRole("cell", { name: "Syntax" })).toBeVisible()
```

### Context menu items

```typescript
// Right-click to open
await row.click({ button: "right" })

// Find context menu items
const menu = page.locator('[data-component="context-menu-content"]')
await expect(menu).toBeVisible()

const uploadItem = menu.locator('[data-slot="context-menu-item-label"]', {
  hasText: /上传文件到此处/,
})
await expect(uploadItem).toBeVisible()
```

---

## Timing & Wait Patterns

### Critical wait sequences

```typescript
// After patch via AI prompt
await waitSessionIdle(sdk, sessionID, 120_000)

// After file creation via terminal
await runTerminal(page, { cmd: "...", token: "expected-output" })

// After external file creation + refresh
await page.waitForTimeout(500)  // let filesystem sync
await refreshButton.click()
await page.waitForSelector('[data-file="new-file.txt"]')
```

### Poll pattern for async operations

```typescript
await expect.poll(
  async () => {
    const diff = await sdk.session.diff({ sessionID })
    return (diff.data ?? []).length
  },
  { timeout: 60_000 },
).toBe(expectedCount)
```

---

## Backend PR Test Strategies

Real examples of testing backend changes through UI:

| Backend Change | UI Path | Test |
|---|---|---|
| Python resolver | Terminal → `python3 --version` | Verify output contains "Python" |
| Config dir name | Settings dialog → General panel | Show config UI |
| Race condition | File tree → create + refresh | New file appears after refresh |
| Cache bypass | File tree → force refresh | Fresh data replaces stale |
| State isolation | Two sessions → switch between | Selection preserved per session |
| URL parsing | Status popover → Servers tab | Connected state visible |
| Focus management | Open file → check prompt focus | Prompt still focusable |

---

## Review Panel Patterns

### Switching changes mode (CRITICAL)

Review panel has multiple modes: "git", "session", "turn". Some UI elements only render in specific modes.

```typescript
async function switchToSessionMode(page) {
  // Find the changes mode selector (NOT the diff-style selector)
  const triggers = page.locator('[data-component="select-trigger"]')
  const modeTrigger = triggers.filter({ hasText: /changes/i }).first()
  await modeTrigger.click()

  // Select "Session changes" from dropdown
  const items = page.locator('[data-slot="select-select-item"]')
  const sessionItem = items.filter({ hasText: /session/i }).first()
  await sessionItem.click()
}
```

**Lesson**: The discard button (`onDiscardFile`) only renders when `store.changes === "session" || store.changes === "turn"`. Default is "git". Must switch first.

### Review panel expand/show

```typescript
async function show(page) {
  const btn = page.getByRole("button", { name: "Toggle review" }).first()
  await expect(btn).toBeVisible()
  if ((await btn.getAttribute("aria-expanded")) !== "true") await btn.click()
  await expect(btn).toHaveAttribute("aria-expanded", "true")
}

async function expand(page) {
  const btn = page.getByRole("button", { name: /^Expand all$/i }).first()
  await expect(btn).toBeVisible()
  await btn.click()
}
```

---

## File Tree Patterns

### Expand folders and click files

```typescript
const tree = page.locator("#file-tree-panel")

const expand = async (name) => {
  const folder = tree.getByRole("button", { name, exact: true }).first()
  await expect(folder).toBeVisible()
  if ((await folder.getAttribute("aria-expanded")) === "false") await folder.click()
}

await expand("src")
await expand("components")

const file = tree.getByRole("button", { name: "index.ts", exact: true }).nth(0)
await file.click()
```

### Right-click context menu

```typescript
const row = page.locator(`[data-file="${file}"]`).first()
await expect(row).toBeVisible()
await row.click({ button: "right" })

const menu = page.locator('[data-component="context-menu-content"]')
await expect(menu).toBeVisible()
```

### Refresh button

```typescript
// Refresh button may not have accessible name — use CSS as fallback
const refreshBtn = page.locator("button.ml-auto").first()
await refreshBtn.click()
```

---

## Common Pitfalls

### Pitfall #1: Missing `waitSessionIdle` after operations

```typescript
// WRONG: immediately interact after prompt
await sdk.session.promptAsync({ ... })
await page.click("#review-tab")  // too early!

// RIGHT: wait for session to finish
await sdk.session.promptAsync({ ... })
await waitSessionIdle(sdk, sessionID, 120_000)  // wait up to 2 min
await page.click("#review-tab")
```

**Impact**: Test fails with timeout on DOM assertions. This was the #1 bug in the ai-visible-undo test (failed 5+ times).

### Pitfall #2: Wrong seed format

```typescript
// WRONG: seed missing "mark" line → waitMark() never finds it
function body(mark) {
  return Array.from({ length: 32 }, (_, i) => `line ${i} ${mark}`)
}

// RIGHT: include both title and mark for waitMark
function body(mark) {
  return [`title ${mark}`, `mark ${mark}`,
    ...Array.from({ length: 32 }, (_, i) => `line ${i} ${mark}`)]
}
```

### Pitfall #3: Playwright TS object literal transform

```typescript
// WRONG — Playwright TS transform rejects inline objects
fs.mkdirSync(dir, { recursive: true })
await page.screenshot({ path: file, fullPage: true })

// RIGHT — extract to variable
const mkdirOpts = { recursive: true }
fs.mkdirSync(dir, mkdirOpts)
const shotOpts = { path: file, fullPage: true }
await page.screenshot(shotOpts)
```

### Pitfall #4: Shadow DOM assumptions

```typescript
// WRONG: Playwright locators can't pierce shadow DOM
const content = page.locator("diffs-container .diff-content")

// RIGHT: use waitForFunction with JS querySelector on shadowRoot
await page.waitForFunction((sel) => {
  const host = document.querySelector(sel)
  return host?.shadowRoot?.textContent?.includes("expected")
}, "diffs-container")
```

### Pitfall #5: Review panel mode not set

The review panel has modes (git/session/turn). Some buttons only appear in specific modes. Always check which mode is active before asserting element visibility.

### Pitfall #6: Concurrent git push conflicts

When running batch agents, each agent tries to push to `e2e-screenshots` branch. Solution:
1. Each agent saves screenshots locally
2. Single batch push at end: `git pull` → copy → `git push`
3. Or use unique branch names: `e2e-screenshots-pr-${PR_NUM}`
