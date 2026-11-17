# Architecture

InfinityContext has one portable core and no hidden execution path.

## Core (this package)

```
session transcript (JSONL)
        │
        ├─ 0. bound         --max-session-bytes / --max-line-bytes / --max-messages / --max-total-chars
        ├─ 1. redact        session_to_sqlite.py  (fail-closed: nothing is stored if this step fails)
        ├─ 2. truncate      MAX_ARCHIVE_LENGTH    (head + tail kept, middle discarded)
        └─ 3. store         SQLite + FTS5 trigram (session_chunks → chunk_fts trigger)
                │
                └─ 4. retrieve   search.py  (read-only FTS5 with LIKE fallback)
                    5. prune     cleanup.py (retention, canonical path anchoring, VACUUM)
                    6. protect   secure_fs.py (owner-only directory, database and WAL sidecars)
```

### Why an archive instead of a bigger window

A 128K window is consumed by one deep reply: system prompt + tools (~30K), summary
(~7K), recent turns (15K) and a worst-case answer (55K) already exceed it. Compression
keeps the *working* context small; the archive keeps the *history* exact. When a detail
from an earlier turn matters, the agent queries the archive instead of replaying it.

### File layout

A source install copies exactly these files into the skill directory; nothing else is
needed and no wildcard should ever be used:

| Destination | Files |
|-------------|-------|
| `<skill-dir>/` | `SKILL.md`, `README.md`, `说明.md`, `CHANGELOG.md`, `SPONSORS.md`, `LICENSE`, `checksums.txt` |
| `<skill-dir>/scripts/` | `session_to_sqlite.py`, `search.py`, `cleanup.py`, `secure_fs.py` |
| `<skill-dir>/references/` | `architecture.md`, `languages.md` |

### Retention (bounded persistence)

Archiving has a ceiling by default. Every run of `session_to_sqlite.py` deletes chunks older
than `--retention-days` (default **30**, range `1..3650`) from `session_chunks` and its FTS
mirror inside the same transaction as the insert, and reports the count as `purged_chunks`.
`--purge-only --output-dir <dir>` applies the same policy to existing archives without
ingesting; it requires the archive marker and skips any database lacking both
`session_chunks` and `chunk_fts`. `--retention-days 0` disables time-based purging, but it is
rejected unless `--allow-unbounded-retention` is also given. Setting `INFINITY_CONTEXT_NO_ARCHIVE=1`
disables archiving entirely — the script writes no file and returns `status: disabled`.

### Data model

| Table | Purpose |
|-------|---------|
| `session_chunks` | one row per conversation chunk: `session_key`, `start_msg_id`, `end_msg_id`, `summary`, `keywords`, `anchor_questions`, `raw_content`, `created_at` |
| `chunk_fts` | FTS5 (trigram) mirror of the searchable columns, kept in sync by an `AFTER INSERT` trigger |
| `archive_metadata` | one row per session key (`session_key`, `format_version`, `app`, `archive_id`); written on create and on append, and checked read-only before any append or purge touches the file. `archive_id` is generated once per archive directory and stored in the marker, so a database copied in from elsewhere is refused |
| indexes | `idx_session_key`, `idx_created_at`, `idx_chunk_unique (session_key, start_msg_id, end_msg_id)` |

`INSERT OR IGNORE` plus the unique index makes re-importing the same transcript
idempotent, so a host can safely re-run the archiver.

### Append target selection (T09)

`--append` never picks a database by prefix. It requires the complete artifact name
`{safe_key}-YYYYMMDD-HHMMSS.db`, opens the candidate **read-only** and verifies that
`archive_metadata.session_key` equals the requested key (an archive created before
`archive_metadata` existed falls back to an exact row check in `session_chunks` and is
upgraded on the next write). A symlink, a foreign database, a path outside `--output-dir`,
or more than one matching candidate aborts with exit 9 before any row is touched;
`--db-path` chooses one explicitly. Retention purging therefore can only ever run against
the database that was identity-checked.

### Exclusive creation and purge scope (T09)

A new archive file is reserved with `O_CREAT | O_EXCL | O_NOFOLLOW` and `0600` before SQLite
opens it, in append mode as well as create mode. A pre-existing file with the predicted name
is a **collision**: the run aborts with exit 10 instead of hardening and writing into it.
`--purge-only` enumerates only the complete artifact filename pattern
`{key}-YYYYMMDD-HHMMSS.db`, opens each candidate **read-only** first and requires
`archive_metadata` to carry the expected app id, a supported format version and the archive
id from the directory marker, plus the expected `session_chunks` columns; it then re-checks
`lstat` device and inode immediately before opening read-write. Anything that fails is
reported as `skipped` and left untouched.


### Redaction and minimisation

Redaction runs **before** any derived field (keywords, anchors, summary) is computed, and
again on each text column immediately before insert. The rule set covers API keys,
bearer tokens, passwords, JWTs, AWS/Google/Slack credentials, PEM private keys,
connection strings, cookies, webhooks, phone numbers and email addresses. High-entropy
candidates are excluded from the keyword index.

The redaction path is fail-closed at every step:

| Stage | Failure behaviour |
|-------|-------------------|
| rule file (`redact_rules.json`) | malformed JSON, non-object schema, wrong field type or empty pattern aborts with `RedactionConfigError` **before any file or database is created** (exit 2) |
| regex compilation | every rule (built-in and custom) is compiled at startup; an uncompilable rule aborts the same way |
| rule application | a substitution error raises instead of `continue`-ing past the rule |
| `session_key` | sanitised before any path or filename is built; non-conforming or sensitive values become `opaque-<sha256[:16]>` |
| database write | the transcript is fully redacted in memory first, then written in one transaction; a failure rolls back and removes only a database created by that run |
| rule path override | `INFINITY_CONTEXT_REDACT_RULES` can point at an alternate rule file; a broken file aborts instead of falling back to defaults |
| in-place redaction | `--redact-file` refuses to run without `--allow-dir`; the lexical path, the `realpath`-resolved path and the resolved allowed directory must all agree, so a symlinked ancestor inside the allowed tree cannot redirect the write |
| output directory | a non-ASCII path that would break SQLite is **refused** (exit 8); `--allow-dir-fallback` opts into the ASCII directory, and the fallback is then reported (`archive_dir_fallback: true`, `requested_dir`, `archive_dir`) and warned about — never silent |

The rule path can be overridden with `INFINITY_CONTEXT_REDACT_RULES`, which is also how
the regression tests exercise a broken rule file without touching the installed copy.

### Ingestion bounds (T09)

Limits are applied **while reading**, not after the whole transcript has been parsed and
processed:

| Bound | Default | Flag | Effect |
|-------|---------|------|--------|
| transcript bytes | 64 MiB | `--max-session-bytes` | only `cap + 1` bytes are read from the head; a partial trailing line is dropped and `ingest.truncated_reason = file-size-limit:<cap>` is reported |
| line bytes | 1 MiB | `--max-line-bytes` | the line is discarded **before** `json.loads` or any regex runs; counted in `ingest.skipped_oversized_lines` |
| message count | 200000 | `--max-messages` | parsing stops; `ingest.truncated_reason = message-count-limit:<cap>` |
| cumulative characters | 64 MiB | `--max-total-chars` | parsing stops; `ingest.truncated_reason = total-chars-limit:<cap>` |
| in-place redaction | 64 MiB | `MAX_REDACT_FILE_BYTES` | `--redact-file` refuses the file before reading it |

Every limit is validated before any file is opened: each flag must be an integer in
`1..hard ceiling`, so a negative or oversized value is rejected instead of bypassing the
cap (a negative byte limit would otherwise reach `file.read(-1)` and read the whole
transcript). `read_messages()` enforces the same range for library callers.

Truncation is never silent: the JSON result carries `ingest.truncated` and
`ingest.truncated_reason`, and `SECURITY_WARN: INGEST_TRUNCATED` is printed to stderr.

### Path and permission rules

`cleanup.py` canonicalises the archive directory, refuses to operate on a relative path,
requires the owner-only `.infinity-context-archive` marker, refuses protected directories
(filesystem root, home, common user folders), deletes only files whose full name matches an
InfinityContext artifact pattern, never recurses into subdirectories, re-checks every
candidate with `lstat` immediately before `unlink`, probes the `session_chunks`/`chunk_fts`
schema read-only before any `VACUUM`, never follows or deletes a symbolic link, and does
nothing without `--apply --confirm-destructive`. `--init-marker` migrates an archive created
by an older version, and only after one of our databases is found in the directory. `search.py` opens the database read-only
(`file:...?mode=ro`). Neither script opens a network socket or spawns a process.

### Filesystem hardening (T09)

The archive holds conversation history, so the store is owner-only by construction:

| Layer | POSIX | Windows |
|-------|-------|---------|
| archive directory | `chmod 0700` | protected DACL: current user + LOCAL SYSTEM, inheritance removed |
| archive marker | `0600`, atomic `O_CREAT\|O_EXCL\|O_NOFOLLOW` | inherits the protected directory DACL |
| database file | `0600`, created atomically with `O_CREAT\|O_EXCL\|O_NOFOLLOW` | protected DACL granting the file itself (`F`, no `(OI)(CI)`) |
| `-wal` / `-shm` | `0600` after the WAL pragma and again after the final checkpoint | inherits the protected directory DACL |

Creating the file with `O_CREAT | O_EXCL | O_NOFOLLOW` and `0600` removes both the
check-then-chmod window and the symlink race. A pre-existing archive directory owned by
another account is refused outright; a directory that is merely too permissive is
tightened; a symbolic link anywhere on the path is refused — every existing component
between the root and the target is inspected, and Windows directory junctions are caught
by comparing each component with its resolved path. Windows ACLs are written with
in-process Win32 security API calls (`ctypes`), not by spawning `icacls`.

The policy is **fail-closed**: if owner-only access cannot be enforced, the archiver
aborts, destroys the half-written database and sidecars, and exits with code 3. The only
opt-out is `--allow-insecure-storage`, which prints a warning and reports
`insecure_storage: true` in the JSON result.

In-place redaction writes through `tempfile.mkstemp` (kernel `O_EXCL`, 0600) in the
target directory, `fsync`s before the atomic replace, cleans the temporary file on every
failure path, and refuses symlinks and foreign-owned parent directories.
