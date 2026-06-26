---
name: opencode-session-toolkit
description: Read the local OpenCode SQLite database, run cross-directory session queries, and export sessions to Markdown files.
---

# OpenCode Session Toolkit

Read the local OpenCode SQLite database and query or export sessions, messages, parts, and projects across directories.

All commands below assume the workdir is this skill directory. For Markdown export, run the bundled script directly:

```bash
./scripts/export_opencode_sessions.py --help
```

## When to use

- List recent sessions, filter by directory, or search by title
- Read message JSON for a specific session
- Export matched sessions into one-Markdown-per-session archives
- Inspect database schema and indexes (load `references/schema.md` only when needed)

## Workflow

1. Resolve the database path with `opencode db path`.
2. Run all queries in read-only mode.
3. Load `references/schema.md` only when field-level details are required.

## 1. Resolve the database path

```bash
if ! command -v opencode >/dev/null 2>&1; then
  echo "opencode command not found in PATH" >&2
  exit 1
fi

if ! DB_PATH="$(opencode db path 2>/dev/null)"; then
  echo "Failed to resolve OpenCode DB path via: opencode db path" >&2
  exit 1
fi

if [ -z "${DB_PATH:-}" ] || [ ! -f "$DB_PATH" ]; then
  echo "OpenCode DB not found: $DB_PATH" >&2
  exit 1
fi

echo "Using DB: $DB_PATH"
```

List existing DB files (no error when there is no match):

```bash
find "${XDG_DATA_HOME:-$HOME/.local/share}/opencode" -maxdepth 1 -name '*.db' -print 2>/dev/null
```

## 2. Time conversion and output formatting

**Time conversion**: all time fields are Unix timestamps in milliseconds. Convert them directly in SQL with `datetime()`.

```bash
# Convert in SQL (recommended, no external command needed)
datetime(time_updated/1000, 'unixepoch', 'localtime')

# Shell helpers for time windows
NOW_MS=$(date +%s000)
LAST_7D=$((NOW_MS - 7*86400*1000))
LAST_30D=$((NOW_MS - 30*86400*1000))
```

**Table alignment**: for normal fields, pipe SQLite output to `column -t -s '|'` (`|` is SQLite's default delimiter). For long JSON fields such as `message.data`, prefer `-json` output.

```bash
sqlite3 -readonly "$DB_PATH" "SELECT id, title, time_updated FROM session LIMIT 5;" | column -t -s '|'
```

## 3. Common read-only queries

Tip: For queries without large JSON fields, append `| column -t -s '|'` for aligned table output.

**List the latest 20 sessions (most recently updated first)**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, directory,
          datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**Filter sessions by directory**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE directory LIKE '/path/to/project%'
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**Filter sessions by `project_id` (most precise project linkage)**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT s.id, s.title, s.directory,
          datetime(s.time_updated/1000,'unixepoch','localtime') as updated
   FROM session s
   WHERE s.project_id = 'your-project-id'
   ORDER BY s.time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

`project_id` maps to `project.id`. List projects with:

```bash
sqlite3 -readonly "$DB_PATH" "SELECT id, worktree, name FROM project;" | column -t -s '|'
```

**List sessions across all directories (with project info)**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT s.id, s.title, s.directory, p.worktree,
          datetime(s.time_updated/1000,'unixepoch','localtime') as updated
   FROM session s
   LEFT JOIN project p ON s.project_id = p.id
   ORDER BY s.time_updated DESC
   LIMIT 50;" | column -t -s '|'
```

**Filter by time range**

```bash
# Sessions active in the last 7 days
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE time_updated > $(( $(date +%s000) - 7*86400*1000 ))
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'

# Sessions created today (local time)
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, datetime(time_created/1000,'unixepoch','localtime') as created
   FROM session
   WHERE date(time_created/1000,'unixepoch','localtime') = date('now','localtime')
   ORDER BY time_created DESC
   LIMIT 20;" | column -t -s '|'
```

**Read message content for one session**

```bash
sqlite3 -readonly -json "$DB_PATH" \
  "SELECT m.id, datetime(m.time_created/1000,'unixepoch','localtime') as created, m.data
   FROM message m
   WHERE m.session_id = 'your-session-id'
   ORDER BY m.time_created ASC;"
```

**Extract fields from `message.data` JSON**

```bash
# Extract key fields such as role and modelID
sqlite3 -readonly "$DB_PATH" \
  "SELECT id,
          json_extract(data, '$.role') as role,
          json_extract(data, '$.modelID') as model,
          datetime(time_created/1000,'unixepoch','localtime') as created
   FROM message
   WHERE session_id = 'your-session-id'
   ORDER BY time_created ASC;" | column -t -s '|'

# Search message payload text with LIKE
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, json_extract(data, '$.role') as role, time_created
   FROM message
   WHERE data LIKE '%keyword%'
   ORDER BY time_created DESC
   LIMIT 20;" | column -t -s '|'
```

**Search session titles**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT id, title, directory, datetime(time_updated/1000,'unixepoch','localtime') as updated
   FROM session
   WHERE title LIKE '%keyword%'
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

**View session summary stats**

```bash
sqlite3 -readonly "$DB_PATH" \
  "SELECT title, summary_additions, summary_deletions, summary_files,
          datetime(time_created/1000,'unixepoch','localtime') as created
   FROM session
   ORDER BY time_updated DESC
   LIMIT 20;" | column -t -s '|'
```

## 4. Export sessions to Markdown

The export script writes one session per Markdown file. By default:

- filename = `session title + created time`
- time filtering uses `time_updated` unless `--time-field created` is passed
- `step-start` / `step-finish` parts are skipped to reduce noise
- when `project.name` is empty, project folder names fall back to the worktree basename, or `global`

**Export sessions for one project**

```bash
./scripts/export_opencode_sessions.py \
  --project opencode-session-toolkit \
  --output-dir ./exports/opencode-session-toolkit
```

`--project` matches by substring against `project_id`, `project.name`, `project.worktree`, and `session.directory`.

**Export sessions in a time range**

```bash
./scripts/export_opencode_sessions.py \
  --start 2026-03-01 \
  --end 2026-03-24T23:59:59 \
  --time-field updated \
  --output-dir ./exports/march
```

Accepted time formats:

- ISO date: `2026-03-24`
- ISO datetime: `2026-03-24T22:35:37`
- Unix seconds / milliseconds

**Full export grouped by project**

```bash
./scripts/export_opencode_sessions.py \
  --all \
  --group-by-project \
  --output-dir ./exports/all
```

Output example:

```text
exports/all/
  OrchAI/
    Migration work planning with subagent discussion_2026-03-23_23-48-07.md
  global/
    opencode-session-toolkit 命令验证与优化_2026-03-24_22-35-37.md
```

**Useful extra filters**

- `--session-id ses_xxx`: exact session export
- `--title-contains keyword`: match session titles
- `--directory-contains keyword`: match session directories
- `--archived include|exclude|only`: filter archived sessions
- `--filename-time-field created|updated`: choose which session time goes into the filename
- `--include-part-type text --include-part-type tool`: export only certain part types
- `--exclude-part-type reasoning`: drop noisy part types
- `--overwrite`: overwrite existing files instead of appending the session id to avoid collisions

If no filters are provided, the script requires `--all` to avoid accidental full-database exports.

## 5. Inspect schema

```bash
sqlite3 -readonly "$DB_PATH" ".schema session"
sqlite3 -readonly "$DB_PATH" ".schema message"
sqlite3 -readonly "$DB_PATH" ".schema part"
sqlite3 -readonly "$DB_PATH" ".schema project"
```

For complete field and index notes, see `references/schema.md`.

## 6. List all tables

```bash
sqlite3 -readonly "$DB_PATH" ".tables"
```

## 7. Example output

```text
id          title                     directory                   updated
----------  -----------------------  --------------------------  -------------------
ses_abc123  My Session - 2026-03-24  /home/user/project         2026-03-24 10:00:00
ses_def456  Another Session          /home/user/other           2026-03-23 15:30:00
```

(Aligned with `| column -t -s '|'`.)

## 8. Notes

- OpenCode uses SQLite WAL mode, so `.db-wal` and `.db-shm` files are expected.
- Time fields are Unix timestamps in milliseconds. Convert with `datetime(ts/1000,'unixepoch','localtime')`.
- `data` fields are JSON. Use `json_extract(data, '$.field')` for structured extraction, and prefer `sqlite3 -json` for raw message inspection.
- Session isolation is anchored by `project_id`; for cross-directory queries, joining `project.worktree` is recommended.
- Direct writes can corrupt data. Back up before any non-read-only operation.
- `account` and `control_account` tables may contain sensitive credentials. Redact outputs when sharing.
