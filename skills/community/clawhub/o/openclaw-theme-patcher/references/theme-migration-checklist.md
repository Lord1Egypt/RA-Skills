# Theme Migration Checklist

Use this as the short execution checklist when preserving or rebuilding a custom OpenClaw Control UI theme across versions.

## A. Before upgrade

- Resolve the active install:
  - `which openclaw`
  - `readlink -f "$(which openclaw)"`
  - `openclaw status`
- Record the active bundle paths:
  - `dist/control-ui/assets/index-*.js`
  - `dist/control-ui/assets/index-*.css`
- Extract and save:
  - `:root[data-theme=<theme-id>]`
  - `:root[data-theme=<theme-id>-light]` if present
- Save copies of the old live JS/CSS bundles into a workspace backup folder
- Capture old JS snippets for:
  - allowed theme id set
  - alias/default map
  - theme card list
  - resolver branch

## B. After upgrade

- Re-resolve the new active install and new hashed bundle paths
- Do not reuse old offsets, variable names, or patch positions blindly
- Reconfirm the new bundle's real structures for:
  - allowed set
  - alias/default map
  - card list
  - resolver

## C. Rebuild safely

- Port the old theme's CSS token values into the new CSS bundle
- Register the theme in the new JS bundle using the new version's real structures
- Keep edits surgical and reversible
- Never use heuristic replacements like changing the first `return e`

## D. Verify visually

- Theme appears in `Settings -> Appearance`
- Theme selection visibly changes the UI
- Light/dark toggle switches to the correct paired selector
- Built-in themes still behave normally
- The migrated theme still matches the intended old look closely enough

## E. If visuals are wrong

Treat this as one of two different failure classes.

### Structural failure

Signs:
- theme card appears but wrong theme resolves
- light/dark toggle fails
- unrelated UI text/layout regresses

Action:
- inspect JS structures again
- remove broken migrated entry if needed
- restore stock UI first
- retry from structural comparison

### Calibration failure

Signs:
- structure works, but specific surfaces feel off
- common examples: chat bubbles, code blocks, blockquotes, panel/chrome feel

Action:
- inspect exact current CSS rules for the affected component
- prefer small theme-scoped overrides under `:root[data-theme=<theme-id>] ...`
- keep overrides narrow and avoid changing built-in themes

## F. Chat-specific calibration

For chat bubble work, verify which layout branch is actually live in the current bundle.
Common branches may include:
- `.chat-group...`
- `.chat-line...`

Do not assume the first matching branch is the rendered one.
If necessary, override both branches under the custom theme selector.

## G. Leave behind

- backup directory path
- old bundle paths
- patched new bundle paths
- exact JS structures patched
- CSS selectors added
- any theme-scoped component overrides added
