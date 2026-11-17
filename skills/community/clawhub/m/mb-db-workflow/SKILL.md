---
name: mb-db-workflow
description: "Record and read Memory Bank state via mb-cli. Use for projects with memory-bank/database/ and a memory_bank.db. Triggers on: db workflow, record session work, regenerate memory bank, update tasks."
---

# Memory Bank DB-Native Workflow (v6.12)

Use the `mb` CLI to read and write project memory banks that use the SQLite backend. Do not hand-edit generated markdown files — they are overwritten on regeneration.

## Prerequisites

- `mb` CLI is installed and on PATH
- Project has `memory-bank/database/` (create with `mb init --database`)
- SQLite database exists at `memory-bank/database/memory_bank.db` (create with `mb db init`)

## Quick Reference

### Read state
```bash
# List tasks
mb task list
mb task list --status in_progress

# Show task details
mb task show T25

# Query DB directly (table output)
mb db query "SELECT * FROM task_items WHERE status = 'in_progress'"

# Query DB (JSON output)
mb db query "SELECT * FROM edit_entries ORDER BY timestamp DESC LIMIT 5" --json

# List sessions
mb session list

# Show session cache
mb session cache
```

### Record work
```bash
# Record edit entry + file changes + optional status update
mb workflow --task T3 --description "Implemented feature X" \
  --files "Created:src/feature.js,Modified:src/app.js" \
  --status in_progress --period afternoon

# Same, but also regenerate all markdown files immediately
mb workflow --record --regenerate --task T3 \
  --description "Implemented feature X" \
  --files "Created:src/feature.js" --status completed

# Regenerate markdown without recording new work
mb workflow --regenerate
```

### Task management
```bash
mb task create "Build quantum simulator" --id T26 --priority high
mb task update T26 --status in_progress
mb task delete T26 --yes
```

### Session management
```bash
mb session start --focus T26 --period afternoon
mb session complete --notes "Finished core logic"
```

### Sync templates
When `mb-core` template files change, update the project's DB files:
```bash
mb db sync --all       # Sync everything
mb db sync --libs      # Sync lib/ only (workflow.js, inserts.js, regenerate.js, sqlite.js)
mb db sync --parsers   # Sync parser scripts only
mb db sync --dry-run   # Preview what would change
```

## Two-Layer Documentation

The DB workflow automates the **chronological layer** (edit entries, tasks, sessions). You must still maintain the **knowledge layer** manually:

- `implementation-details/` — architecture, design decisions
- `techContext.md` — system architecture, dependencies
- `productContext.md` — goals, user stories
- `systemPatterns.md` — established patterns

Anti-pattern: "The DB workflow handled the update, so I'm done." It only writes the timeline. The knowledge layer requires manual attention.

## File Change Syntax

`--files` uses comma-separated `action:path` pairs:
- `Created:src/index.js`
- `Modified:lib/util.js`
- `Updated:package.json`
- `Deleted:old-file.js`

Example:
```bash
mb workflow --task T1 --description "Setup project" \
  --files "Created:package.json,Modified:README.md,Deleted:legacy.py"
```

## Workflow vs Update

- `mb workflow` — Low-level: record work, optionally regenerate. Explicit flags for each action.
- `mb update` — High-level: combines record + regenerate in one shot. Simpler but less granular.

Use `mb workflow` when you need precise control. Use `mb update` for quick session wraps.

## Anti-Patterns

- NEVER edit generated markdown directly (`edit_history.md`, `tasks.md`, `session_cache.md`) — they are overwritten on regeneration
- NEVER run DB workflow in projects without `memory-bank/database/schema.sql`
- NEVER skip knowledge-layer updates after recording chronological work
- NEVER pass `--files` with spaces around the colon — use `action:path` exactly

## Error Recovery

- No database found: `mb db init` then `mb init --database`
- Missing lib files: `mb db sync --libs`
- Schema mismatch: `mb db sync --database-files` to refresh schema.sql

## References

- `references/api-reference.md` — Full JS library API (recordSessionWork, regenerateAll, etc.)
- `references/schema.sql` — Full SQLite schema
- `references/integrated-rules-v6.12.md` — Complete v6.12 protocol rules
