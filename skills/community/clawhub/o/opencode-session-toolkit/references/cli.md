# CLI guide

Run commands from the skill directory. Put `--db-path` after the subcommand when overriding automatic `opencode db path` resolution.

## Route by intent

| Need | Command |
| --- | --- |
| Verify the database is usable | `doctor` |
| Find sessions by metadata | `list` |
| Read one session | `show SESSION_ID` |
| Find literal text | `search TEXT` |
| Write an archive | `export` |
| Diagnose fields or indexes | `schema` |

Use `<command> --help` as the option authority.

## Diagnose first

```bash
./scripts/opencode_sessions.py doctor
./scripts/opencode_sessions.py schema --table session --format json
```

`doctor` reads schema metadata only; it does not read transcript content.

## Discover sessions

```bash
./scripts/opencode_sessions.py list
./scripts/opencode_sessions.py list --project toolkit --start 2026-08-01
./scripts/opencode_sessions.py list --directory /path/to/worktree --format json
./scripts/opencode_sessions.py list --archived only
```

Repeated values for the same filter are OR alternatives. Different filter categories combine with AND. Text filters are literal, case-insensitive substrings: `%` and `_` are not SQL wildcards.

The default list excludes archived sessions and returns 20 rows ordered by update time and session ID.

## Read or search

```bash
./scripts/opencode_sessions.py show ses_example
./scripts/opencode_sessions.py show ses_example --format json
./scripts/opencode_sessions.py search 'exact % text' --scope all
./scripts/opencode_sessions.py search 'tool name' --scope messages --format json
```

Default `show` output includes text and concise tool summaries. It omits reasoning, complete tool inputs/outputs, raw message JSON, and other non-display parts.

Only use this after the user explicitly asks for complete payloads:

```bash
./scripts/opencode_sessions.py show ses_example --include-sensitive
```

Search reports matching sessions without printing matching message snippets. Use `show` on an intended session rather than exposing surrounding payloads automatically.

## Export

Select sessions with the same filters as `list`:

```bash
./scripts/opencode_sessions.py export \
  --project opencode-session-toolkit \
  --output-dir ./exports/toolkit

./scripts/opencode_sessions.py export \
  --start 2026-08-01 \
  --end 2026-08-09 \
  --group-by-project \
  --output-dir ./exports/week
```

Use `--all` to acknowledge an unfiltered full-database export. Date-only `--end` includes the entire local calendar day.

Preview matched output paths and conflict status without creating files:

```bash
./scripts/opencode_sessions.py export \
  --project opencode-session-toolkit \
  --output-dir ./exports/toolkit \
  --dry-run
```

Markdown creates one file per session. Filenames contain a sanitized title, UTC creation time, and session ID. JSONL creates `sessions.jsonl`.

Exports are preflighted before writing:

- Identical existing files are reported as unchanged.
- Changed existing files stop the whole export before new files are written.
- `--overwrite` explicitly replaces changed outputs through same-directory atomic renames.

`--include-sensitive` applies the same opt-in boundary as `show` and emits a warning on stderr.

## Output rules

- Displayed times are UTC ISO-8601.
- Naive datetimes and date-only bounds are interpreted in the machine's local timezone.
- Table output is for humans; JSON output is stable for downstream tools.
- Errors use exit code 2 and a concise `error:` message on stderr.
