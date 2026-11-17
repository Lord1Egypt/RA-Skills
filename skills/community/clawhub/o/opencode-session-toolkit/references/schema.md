# Live schema compatibility

Treat the database itself as authoritative. OpenCode adds tables and columns over time, and the CLI detects capabilities at runtime instead of assuming one migration snapshot.

## Core requirements

| Command | Required structures |
| --- | --- |
| `list` and title search | `session`: `id`, `project_id`, `directory`, `title`, `time_created`, `time_updated` |
| message search | the `session` fields above plus `message`: `id`, `session_id`, `time_created`, `data` |
| `show` and `export` | the structures above plus `part`: `id`, `message_id`, `session_id`, `time_created`, `data` |

The `project` table and fields such as `session.version`, summary counts, and archive time are optional enhancements. Their absence must not break commands that do not need them.

## Inspect the actual database

Start with:

```bash
./scripts/opencode_sessions.py doctor --format json
./scripts/opencode_sessions.py schema --format json
```

Limit schema output when investigating one table:

```bash
./scripts/opencode_sessions.py schema --table session --table message
```

The CLI only reports the four core tables. For an advanced fallback, inspect a named core table without dumping data:

```bash
DB_PATH="$(opencode db path)"
sqlite3 -readonly "$DB_PATH" ".schema session"
sqlite3 -readonly "$DB_PATH" ".indexes session"
```

## Data conventions

- Time fields are Unix milliseconds. CLI output renders them as UTC ISO-8601.
- A date-only `--start` begins at local midnight.
- A date-only `--end` includes the whole local calendar day.
- `message.data` and `part.data` are JSON text. Payload shapes vary by OpenCode version and part type.
- Join sessions to projects with `session.project_id = project.id` when `project` is available.
- Order messages by `(time_created, id)` and parts within each message by `(time_created, id)`. Do not rely on a join order that can interleave equal-timestamp messages.

If a required column is absent, stop and report the `doctor` output. Do not guess an old or future schema and do not mutate the database to make it fit.
