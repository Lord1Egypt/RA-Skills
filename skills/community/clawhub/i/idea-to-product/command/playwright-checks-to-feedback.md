---
description: Route failed browser checks back into backlog, UX, or system mismatch
---

# /playwright-checks-to-feedback

Route failed checks into the right layer.

## Failure classes

1. `story gap`
2. `ux gap`
3. `system mismatch`

## Rules

- do not send every failure back to backlog
- use UX when the page responsibility or CTA is wrong
- use system mismatch when docs say "done" but the browser says otherwise

## Output

- failure id
- failed check
- failure class
- next file to update
- next action
