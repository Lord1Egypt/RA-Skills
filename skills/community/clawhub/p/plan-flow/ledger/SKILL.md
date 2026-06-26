---
name: ledger
description: Persistent project learning journal that builds institutional memory across sessions
metadata: {"openclaw":{"requires":{"bins":["git"]}}}
user-invocable: false
---

# Project Ledger

A persistent, project-specific learning journal maintained across sessions. Captures mistakes, corrections, discovered patterns, and hard-won knowledge about a specific codebase.

## How It Works

The ledger operates silently in the background:

1. **Session Start**: Read `flow/ledger.md` and apply learnings
2. **During Work**: Record new learnings as they happen
3. **Maintenance**: Periodically consolidate and prune entries

## File Location

```
flow/ledger.md
```

## What Gets Recorded

- Project-specific quirks and gotchas
- Approaches that worked or didn't work
- User preferences beyond documented rules
- Domain context and business logic
- Environment and toolchain surprises
- Self-corrections and mistakes made

## What Doesn't Get Recorded

- Generic programming knowledge
- Patterns already in rules files
- Temporary one-off issues
- Content that belongs in discovery docs or plans

## Entry Style

Write lessons, not logs. Each entry should be concise and actionable.

**Examples:**
- "The `buildWidgets` script requires Node 18+ - fails silently on Node 16"
- "User prefers explicit error types over generic Error class"
- "Tests for streaming endpoints need a 3s timeout override"

## Sections

| Section | Purpose |
|---------|---------|
| Project Quirks | Surprising behaviors, undocumented constraints |
| What Works | Proven approaches for this project |
| What Didn't Work | Failed approaches with reasoning |
| User Preferences | How the user likes things done |
| Domain Context | Business logic and terminology |

## Maintenance

- Keep under 150 lines of high-signal content
- Consolidate every 8-10 sessions
- Remove stale entries when quirks get fixed
- Promote established patterns to rules files

## Integration

Learnings are naturally captured from all plan-flow activities (setup, discovery, execution, reviews). The ledger captures meta-learnings that span across individual artifacts.
