---
name: idea-manager
description: A structured command-line tool for managing your ideas, proposals, todos, and wishlist items with validation and drift prevention. Reads and writes IDEAS.md, creates archive files under memory/, and supports alternate target files via --file. Use when someone asks to "show idea list", "review ideas", "add new idea", "update idea status", "delete idea", or "archive completed ideas", or discusses idea tracking or knowledge management.
version: 1.1.1
metadata:
  openclaw:
    requires:
      bins:
        - python3
      config:
        - IDEAS.md
  hermes:
    emoji: "💡"
    category: "productivity"
    platform: "Linux, macOS, Windows"
---

## Requirements

| Binary | Purpose |
|--------|---------|
| `python3` | Run the idea-manager script |

# IDEA Manager

Idea Manager is a structured command-line tool for managing your ideas, proposals, todos, and wishlist items. The script saves your ideas to a file named `IDEAS.md` in the root of the `~/.openclaw/workspace` directory. Originally, I was having different agents write notes to this file. But, over time I noticed that the formatting and data started changing depending on which LLM was being used. So, to prevent format drift and enforce consistent conventions, I came up with this script and turned it into an OpenClaw skill. The script provides both CLI and JSON input options for flexible usage by agents or other scripts. You can use it by just telling the agent what you want to do. Example: "Add a new idea for....[describe your idea]". Later you can ask your agent to show you previously saved ideas. Try asking: "Show me the list of my ideas". You can also request ideas by status. Example: "Show me the blocked ideas on my list".


## Scope and Side Effects

`idea-manager` performs state-changing operations on files in the workspace. Before using it, understand what it does:

- **Reads and writes `IDEAS.md`** — the primary ideas file. The tool rewrites this file atomically on every `write`, `edit`, `delete`, and `archive` operation.
- **Creates files under `memory/`** — `archive` writes completed entries to `memory/IDEAS-Archive-YYYY-MM-DD.md`.
- **Permanently deletes content** — `delete` removes entries from `IDEAS.md` without an undo mechanism. Deleted content may be recoverable from git history if the workspace is versioned.
- **Reindexes IDs and rewrites references** — `archive` reassigns sequential IDs to remaining entries (IDEA-001, IDEA-002, …) and updates `related_files` references automatically.

## Intentions → Commands

| User wants to... | Command |
|---|---|
| See the idea list (uncompleted) | `idea-manager report` |
| Review all ideas | `idea-manager read` |
| Filter by status | `idea-manager read --status active` |
| Search by keyword | `idea-manager read --search cron` |
| Add a new idea (auto ID) | `idea-manager write --auto-id --title ... --priority high` |
| Add a new idea (JSON) | `idea-manager write --json {"id":"IDEA-NNN","title":"..."}` |
| Update an idea status | `idea-manager edit --id IDEA-NNN --status completed` |
| Delete an idea | `idea-manager delete --id IDEA-NNN --decision reason` |
| Archive / reindex | `idea-manager archive` |
| See summary statistics | `idea-manager status` |

## Quick Reference

| User wants... | Do this |
|---------------|---------|
| List all ideas | `idea-manager read` |
| Find specific idea | `idea-manager read --id IDEA-001` |
| Search for keyword | `idea-manager read --search "keyword"` |
| Filter by status | `idea-manager read --status active` |
| Add new idea (CLI) | `idea-manager write --id IDEA-001 --title "..." --priority high` |
| Add new idea (JSON) | `idea-manager write --json '{"id":"...","title":"..."}'` (must include id and title) |
| Update idea status | `idea-manager edit --id IDEA-001 --status completed` |
| Delete an idea | `idea-manager delete --id IDEA-001 --decision "Replaced by LRN-20260822-001"` |
| Archive completed items (metadata only) | `idea-manager archive` |
| Archive completed items (with full details) | `idea-manager archive --archive-details` |
| Archive without confirmation | `idea-manager archive --force` |
| See summary stats | `idea-manager status` |
| Export stats as JSON | `idea-manager status --json` |
| Export as JSON | `idea-manager read --json` |
| Generate report (markdown) | `idea-manager report` |
| Export report as JSON | `idea-manager report --json` |
| Report sorted by ID ascending | `idea-manager report --sort id-asc` |
| Report sorted by status | `idea-manager report --sort status` |

## Trigger Phrases

When the user says any of these, run `idea-manager report` to generate a markdown table of non-completed items:

- What's on the idea list?
- Review idea list
- Idea list
- Review IDEAS.md
- Unfinished ideas from IDEAS.md
- Status of ideas
- Idea list status
- What ideas are not completed?

## Important Rules

1. **Always use structured fields** — Never manually edit IDEAS.md. Use `idea-manager` to ensure consistency and prevent corruption.

2. **ID format matters** — Use `DOMAIN-NNN` format (e.g., `IDEA-001`, `TOOL-003`, `SKL-010`). IDs must be unique.

3. **Status lifecycle** — Typical flow: `active` → `pending`/`blocked` → `completed`/`superseded`.

4. **Atomic updates only** — The tool uses tempfile + atomic move to prevent partial writes that can corrupt the file.

5. **Document decisions** — When marking an idea `completed` or `superseded`, use `--decision` to record why and what replaced it.

6. **JSON schema validation** — When using `--json` flag, input must be a JSON object containing both `id` and `title` fields. Well-formed JSON that doesn't match this schema (e.g., `openclaw.json`) will be rejected with a clear error message. If using `@file.json` syntax, the file must be located in the same directory as `IDEAS.md`.

## Workflow Modes

### Add New Idea

```bash
idea-manager write \
  --id IDEA-001 \
  --title "Add cron failure alerts" \
  --priority high \
  --status active \
  --area cron,monitoring \
  --source "User request" \
  --details "Configure failureAlert on all cron jobs with Telegram notifications."
```

Required: `--id`, `--title`
Recommended: `--priority`, `--status`, `--area`, `--details`

#### Auto-Generate ID

Instead of specifying an explicit ID, use `--auto-id` to have the script calculate the next available `IDEA-NNN` sequence number:

```bash
idea-manager write --auto-id --title "Add cron failure alerts" --priority high --status active
```

This scans existing entries, finds the highest `IDEA-NNN` number, and generates the next one. Useful for interactive use where you don't want to manually track IDs.

### Update Existing Idea

```bash
# Change status
idea-manager edit --id IDEA-001 --status completed

# Update with decision
idea-manager edit --id IDEA-001 \
  --status superseded \
  --decision "Replaced by LRN-20260810-002" \
  --details "New approach uses built-in failureAlert instead of custom monitoring."
```

### Delete an Idea

```bash
# Delete with a decision reason
idea-manager delete --id IDEA-001 --decision "Replaced by LRN-20260822-001"
```

The `--decision` flag records why the idea was removed (recommended). The entry is **permanently removed** from `IDEAS.md` without an undo mechanism. Deleted content may be recoverable from git history if the workspace is versioned.

### Archive Completed Items

```bash
# Archive all completed entries, reindex remaining (metadata only)
idea-manager archive

# Include full entry details in the archive file
idea-manager archive --archive-details

# Skip confirmation prompt (for scripts/non-interactive use)
idea-manager archive --force
```

Moves matching entries from `IDEAS.md` to `memory/IDEAS-Archive-YYYY-MM-DD.md`, removes them from `IDEAS.md`, and reindexes the remaining entries sequentially (IDEA-001, IDEA-002, …). Any `related_files` references are updated automatically to reflect the new IDs.

By default, the archive file contains only entry metadata (logged date, status, area, decision). This avoids duplicating full details outside `IDEAS.md`. Use `--archive-details` to include source, tags, owner, related files, pattern keys, and the full `details` field.

`archive` is a destructive, irreversible operation. By default it shows a warning and requires typing `yes` to proceed. In non-interactive environments (e.g., cron, piped input), it refuses unless `--force` is provided.

### Review and Search

```bash
# All active ideas
idea-manager read --status active

# Specific domain
idea-manager read --area cron

# Export for processing
idea-manager read --status active --json | jq '.[] | select(.priority=="high")'
```

### Summary Statistics

```bash
idea-manager status
```

Output shows total count, distribution by status/priority/area.

## Field Reference

| Field | Values | Purpose |
|-------|--------|---------|
| `id` | e.g., IDEA-001 | Unique identifier |
| `title` | string | Short description |
| `logged` | ISO date | When logged (auto) |
| `priority` | low/medium/high/critical | Importance |
| `status` | active/pending/completed/superseded/blocked | Current state |
| `area` | comma-separated | Domain(s) affected |
| `source` | string | Origin of idea |
| `recurrence_count` | integer | Times pattern repeated |
| `first_seen` / `last_seen` | ISO dates | Pattern timeframe |
| `related_files` | comma-separated | Files touched |
| `pattern_key` | string | For recurring patterns |
| `tags` | comma-separated | Free-form tags |
| `decision` | string | Final outcome |
| `owner` | string | Responsible person |
| `details` | text | Full description |

## Gotchas

- **Don't edit IDEAS.md directly** — Manual edits bypass validation and can cause format drift. Always use `idea-manager`.

- **ID collisions** — The tool checks for duplicate IDs and will refuse to create conflicting entries.

- **JSON output for scripting** — Use `--json` flag when piping to other tools or processing programmatically.

- **Delete is permanent** — `idea-manager delete` removes the entry from `IDEAS.md` and rewrites the file. The content is recoverable from git history.

- **Archive reindexes** — `idea-manager archive` reassigns sequential IDs to remaining entries. Old IDs are recorded in the archive file and the ID mapping is printed. Any `related_files` references are updated automatically.

- **Status meanings**:
  - `active`: Currently being worked on or relevant
  - `pending`: Waiting on something external
  - `blocked`: Cannot proceed due to dependency
  - `completed`: Resolved/implemented
  - `superseded`: Replaced by better approach

## Reference: IDEAS.md Format

The file uses a consistent markdown format with frontmatter-like metadata:

```markdown
## [IDEA-001] Add cron failure alerts

**Logged**: 2026-08-10T12:30:00Z
**Priority**: high
**Status**: active
**Area**: cron,monitoring
**Source**: User request
**Pattern-Key**: cron.failure-alert

Configure failureAlert on all cron jobs...
```

This format is automatically generated and parsed by `idea-manager`. Do not modify it manually.

## Scripts

- `scripts/` — Contains the Python implementation (`idea_manager.py`)

The tool is installed as `idea-manager` command. `IDEAS.md` is user data — it is auto-created on first run and lives in the workspace root. It is gitignored (not tracked in git), so each user gets their own fresh file.

Use `--file /path/to/IDEAS.md` to point the tool at a different file.

## Further Reading

- See `IDEAS.md` in the workspace root for all current tracked ideas.


