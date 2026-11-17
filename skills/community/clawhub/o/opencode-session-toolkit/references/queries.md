# Advanced read-only queries

Use this reference only when the bundled CLI cannot answer the question. Inspect `references/schema.md` and the live schema first.

## Guardrails

```bash
DB_PATH="$(opencode db path)"
test -f "$DB_PATH"
sqlite3 -readonly "$DB_PATH" "PRAGMA query_only = ON; SELECT sqlite_version();"
```

- Keep `-readonly` and set `PRAGMA query_only = ON`.
- Query only `session`, `message`, `part`, and `project` unless the user explicitly names another non-credential table.
- Never query `account`, `control_account`, or `credential`.
- Prefer CLI filters for user-provided text. If raw SQL is unavoidable, bind values rather than interpolating them.
- Start exploratory queries with an explicit `LIMIT`.
- Use `-json` for JSON or long text; use `-header -column` for short tabular output.

## Session ancestry

List direct child sessions:

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT id, title, parent_id,
          datetime(time_updated / 1000, 'unixepoch') AS updated_utc
   FROM session
   WHERE parent_id = 'ses_parent_id'
   ORDER BY time_updated DESC, id ASC
   LIMIT 50;"
```

Escape any single quote in a trusted ID as `''`. Prefer `list --session-id` for ordinary ID lookup.

## Part-type distribution

Inspect which part types exist before designing a specialized export:

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT json_extract(data, '$.type') AS part_type, COUNT(*) AS count
   FROM part
   GROUP BY part_type
   ORDER BY count DESC
   LIMIT 100;"
```

## Tool usage summary

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT json_extract(data, '$.tool') AS tool, COUNT(*) AS uses
   FROM part
   WHERE json_extract(data, '$.type') = 'tool'
   GROUP BY tool
   ORDER BY uses DESC
   LIMIT 100;"
```

This reports tool names only. Do not select complete tool payloads unless the user explicitly requests sensitive content.

## Project activity summary

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT s.project_id,
          COALESCE(p.name, p.worktree, s.project_id) AS project,
          COUNT(*) AS sessions,
          datetime(MAX(s.time_updated) / 1000, 'unixepoch') AS latest_utc
   FROM session AS s
   LEFT JOIN project AS p ON p.id = s.project_id
   GROUP BY s.project_id, project
   ORDER BY MAX(s.time_updated) DESC
   LIMIT 100;"
```

## Integrity diagnostics

Find messages or parts whose parent row is missing:

```bash
sqlite3 -readonly -header -column "$DB_PATH" \
  "PRAGMA query_only = ON;
   SELECT 'message_without_session' AS issue, COUNT(*) AS count
   FROM message AS m LEFT JOIN session AS s ON s.id = m.session_id
   WHERE s.id IS NULL
   UNION ALL
   SELECT 'part_without_message', COUNT(*)
   FROM part AS p LEFT JOIN message AS m ON m.id = p.message_id
   WHERE m.id IS NULL;"
```

Report findings; do not repair the OpenCode database.

## Query-plan diagnosis

```bash
sqlite3 -readonly "$DB_PATH" \
  "PRAGMA query_only = ON;
   EXPLAIN QUERY PLAN
   SELECT id FROM message
   WHERE session_id = 'ses_example'
   ORDER BY time_created, id;"
```

Compare the plan with `./scripts/opencode_sessions.py schema --table message`. Do not create indexes in the live database.
