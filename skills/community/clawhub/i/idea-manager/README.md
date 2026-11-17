# IDEA Manager

Idea Manager is a structured command-line tool for managing your ideas, proposals, todos, and wishlist items. The script saves your ideas to a file named `IDEAS.md` in the root of the `~/.openclaw/workspace` directory. Originally, I was having different agents write notes to this file. But, over time I noticed that the formatting and data started changing depending on which LLM was being used. So, to prevent format drift and enforce consistent conventions, I came up with this script and turned it into an OpenClaw skill. The script provides both CLI and JSON input options for flexible usage by agents or other scripts. You can use it by just telling the agent what you want to do. Example: "Add a new idea for....[describe your idea]". Later you can ask your agent to show you previously saved ideas. Try asking: "Show me the list of my ideas". You can also request ideas by status. Example: "Show me the blocked ideas on my list".

## What It Does

- **Manages `IDEAS.md`**: A persistent file in the OpenClaw workspace that tracks ideas, feature requests, wishlist items, and to-do list tasks over time.
- **Prevents format drift**: All entries are written through this tool, ensuring consistent structure and preventing manual edit errors.
- **Atomic writes**: Uses tempfile + atomic move to prevent corruption if a write is interrupted.
- **Duplicate prevention**: Checks for existing IDs before creating new entries.
- **Flexible input**: Supports both CLI flags (for interactive use) and JSON input (for scripting and programmatic use).
- **Schema validation**: When using JSON input, validates that both `id` and `title` fields are present; well-formed JSON that doesn't match this schema is rejected with a clear error message.

## Scope and Side Effects

`idea-manager` performs state-changing operations on files in the workspace. Before using it, understand what it does:

- **Reads and writes `IDEAS.md`** — the primary ideas file. The tool rewrites this file atomically on every `write`, `edit`, `delete`, and `archive` operation.
- **Creates files under `memory/`** — `archive` writes completed entries to `memory/IDEAS-Archive-YYYY-MM-DD.md`.
- **Permanently deletes content** — `delete` removes entries from `IDEAS.md` without an undo mechanism. This is intended to remove old ideas that aren't being pursued. We recommend keeping regular backups of the `IDEAS.md` (or even your entire OpenClaw workspace directory).
- **Reindexes IDs and rewrites references** — `archive` reassigns sequential IDs to remaining entries (IDEA-001, IDEA-002, …) and updates `related_files` references automatically. This is intended to reorganize your ideas after archiving completed items.

## File Modified

- **`IDEAS.md`**: The main ideas file where all entries are stored. It is auto-created on first run and lives in the workspace root. Each entry uses a consistent markdown format with metadata fields (priority, status, area, etc.) followed by a details section.

- **`memory/IDEAS-Archive-YYYY-MM-DD.md`**: is generated when the `archive` command is used. It moves all ideas which have status `completed` to this archive file. It then reindexes and renumbers the remaining ideas in the `IDEAS.md` file.

## Installation

No installation needed — the tool is already available as an OpenClaw skill. If you have the source, run it with Python:

```bash
python3 scripts/idea_manager.py <command> [options]
```

## Global Options

- `--file <path>`: Path to IDEAS.md file (default: auto-detects workspace root IDEAS.md)

## Usage

### List All Ideas
```bash
python3 scripts/idea_manager.py read
```

### Find a Specific Idea
```bash
python3 scripts/idea_manager.py read --id IDEA-001
```

### Search Ideas
```bash
python3 scripts/idea_manager.py read --search "cron"
```
Searches for the keyword in titles and details (case-insensitive).

### Add a New Idea (CLI)

#### Using Explicit ID
```bash
python3 scripts/idea_manager.py write \
  --id IDEA-001 \
  --title "Add cron failure alerts" \
  --priority high \
  --status active \
  --area cron,monitoring \
  --source "User request" \
  --details "Configure failureAlert..."
```
Required: `--id`, `--title`
Recommended: `--priority`, `--status`, `--area`, `--details`

#### Using Auto-Generated ID
If you don't want to manually track ID numbers, use `--auto-id` to have the script calculate the next available `IDEA-NNN` sequence:
```bash
python3 scripts/idea_manager.py write \
  --auto-id \
  --title "Add cron failure alerts" \
  --priority high \
  --status active \
  --details "Configure failureAlert..."
```

### Add a New Idea (JSON - Recommended for Scripts)
```bash
python3 scripts/idea_manager.py write --json '{
  "id": "IDEA-001",
  "title": "Add cron failure alerts",
  "priority": "high",
  "status": "active",
  "area": "cron,monitoring",
  "source": "User request",
  "details": "Configure failureAlert..."
}'
```
Note: JSON must include both `id` and `title` fields.
Or from a file (must be in the same directory as `IDEAS.md`):
```bash
python3 scripts/idea_manager.py write --json @path/to/idea.json
```

### Update an Existing Idea
```bash
python3 scripts/idea_manager.py edit --id IDEA-001 --status completed
```

### Delete an Idea
```bash
python3 scripts/idea_manager.py delete --id IDEA-001 --decision "Replaced by LRN-20260822-001"
```

Removes the entry from `IDEAS.md` **permanently** without an undo mechanism. The `--decision` flag records why it was removed (recommended). The content is recoverable from git history if the workspace is versioned.

### Archive Completed Items
```bash
python3 scripts/idea_manager.py archive
python3 scripts/idea_manager.py archive --archive-details
python3 scripts/idea_manager.py archive --force  # skip confirmation
```

Moves matching entries from `IDEAS.md` to `memory/IDEAS-Archive-YYYY-MM-DD.md`, removes them from `IDEAS.md`, and reindexes the remaining entries sequentially (IDEA-001, IDEA-002, …). Any `related_files` references are updated automatically to reflect the new IDs.

By default, the archive file contains only entry metadata (logged date, status, area, decision). This avoids duplicating full details outside `IDEAS.md`. Use `--archive-details` to include source, tags, owner, related files, pattern keys, and the full `details` field.

`archive` is a destructive, irreversible operation. By default it shows a warning and requires typing `yes` to proceed. In non-interactive environments (e.g., cron, piped input), it refuses unless `--force` is provided.

### See Summary Statistics
```bash
python3 scripts/idea_manager.py status
```

Shows total count and distribution by status, priority, and area.

For programmatic use, add `--json`:
```bash
python3 scripts/idea_manager.py status --json
```
Returns JSON like `{"total": 29, "by_status": {...}, "by_priority": {...}, "by_area": {...}}`

### Export All Ideas as JSON
```bash
python3 scripts/idea_manager.py read --json
```

Useful for scripting or processing with tools like `jq`.

### Generate a Report (Markdown Table)
```bash
python3 scripts/idea_manager.py report
```

Generates a markdown table of all non-completed items (status != completed), ready for pasting into chat or docs. Use `--json` for structured output:
```bash
python3 scripts/idea_manager.py report --json
```

Filter by a specific status (including `completed`):
```bash
python3 scripts/idea_manager.py report --status pending
```

Sort the results (default: lowest ID first):
```bash
python3 scripts/idea_manager.py report --sort id-asc   # Lowest ID first (default)
python3 scripts/idea_manager.py report --sort id-desc   # Highest ID first
python3 scripts/idea_manager.py report --sort status    # Group by status
```

## Available Fields

| Field | Description | Example |
|-------|-------------|---------|
| `id` | Unique identifier | `IDEA-001`, `BUG-003` |
| `title` | Short description | "Add cron failure alerts" |
| `logged` | When logged (ISO format) | `2026-08-10T12:30:00Z` |
| `priority` | Importance | `low`, `medium`, `high`, `critical` |
| `status` | Current state | `active`, `pending`, `completed`, `superseded`, `blocked` |
| `area` | Domain(s) affected | `cron`, `monitoring`, `docs` |
| `source` | Where it came from | `User request`, `Bug report` |
| `recurrence_count` | Times pattern repeated | `3` |
| `first_seen` / `last_seen` | Date range | `2026-08-01` |
| `related_files` | Files touched | `TOOLS.md`, `AGENTS.md` |
| `pattern_key` | For recurring patterns | `cron.failure-alert` |
| `tags` | Free-form tags | `urgent,backend` |
| `decision` | Final outcome | "Replaced by LRN-20260810-002" |
| `owner` | Responsible person | `Ken` |
| `details` | Full description | Multi-line explanation |

## Status Meanings

- **`active`**: Currently being worked on or relevant
- **`pending`**: Waiting on something external
- **`blocked`**: Cannot proceed due to dependency
- **`completed`**: Resolved or implemented
- **`superseded`**: Replaced by a better approach

## Tips

- Use **JSON input** (`--json`) when calling from scripts or other tools — it's more reliable than long CLI flag lists.
- Use `idea-manager delete` to remove ideas cleanly — no need to manually edit `IDEAS.md`.
- Use `idea-manager archive` to prune completed items and reindex the list, keeping `IDEAS.md` tidy.
- Use **`--search`** to quickly find ideas by keyword in titles or details.
- Combine filters like `--search`, `--status`, and `--area` to narrow results.
- The tool validates entries and prevents duplicate IDs automatically.
- All writes are atomic — if the process is interrupted, the file won't be corrupted.
- Use `--json` output with `jq` to query and filter ideas programmatically.


