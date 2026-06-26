# Edge Bookmarks Organization Workflow

This reference records the real workflow that produced a persistent Microsoft Edge bookmark reorganization.

## What failed

### Raw `Bookmarks` JSON editing

The file could be rewritten and its checksum could be recomputed, but Edge later rebuilt the visible tree from its live model and sync state.

Observed symptoms:

- old top-level items returned
- new folders were appended to the end
- some new folders appeared empty
- `Bookmarks.bak` was eventually overwritten too

### Apple Events JavaScript menu path

The concept exists in Chromium-family browsers, but in the tested Edge environment it was not reliable enough to use as the main control path.

### Pure accessibility automation on `edge://favorites/`

The page did not expose a dependable semantic accessibility tree for safe bookmark manipulation.

## Minimal successful path

1. Capture current Edge session state.
2. Quit Edge completely.
3. Relaunch the real profile in a controllable mode.
4. Attach to the live `edge://favorites/` page.
5. Use `chrome.bookmarks` inside the live browser context.
6. Verify by immediate re-read, page reload, and normal restart.
7. Restore important tabs afterward when practical.

## Why it worked

It operated against the same live bookmark model Edge itself was using, instead of hoping the browser would accept an offline file edit.

## Recommended order

1. Confirm exact profile and scope.
2. Inspect sync risk.
3. Avoid raw file edits by default.
4. Prefer live browser bookmark APIs.
5. Use UI automation only if model-level control is unavailable.
6. Verify after reload and restart.

## Safety notes

- Do not delete on first pass.
- Preserve counts unless dedup is explicitly requested.
- Keep a rollback snapshot and dry-run move plan.
- Verify structural placement, not just counts.
