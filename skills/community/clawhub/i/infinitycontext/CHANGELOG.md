# Changelog

All notable changes to InfinityContext are documented here.
Format: version — date — summary.

## 1.8.7 — 2026-09-09

One more pointer so nobody installs the slim package by accident.

### Added
- **`SKILL.md` now says where the complete project lives** (English and 简体中文): the
  GitHub repository is the full, unabridged version — the identical core **plus** the
  optional `openclaw/` host integration with its own README and checksums. The registry
  package is deliberately slimmed to the auditable core.

## 1.8.6 — 2026-09-09

Documentation-only release: the page now says what the skill actually does for you, and the
package boundary is explicit.

### Changed
- **Benefit-first hero in `SKILL.md`, `README.md` and `说明.md`** — what the agent stops
  losing, what it gets back, and a before/after table for a context compaction — immediately
  followed by the unchanged security disclosure.
- **Fixed a broken heading fragment.** ` — portable context compression & memory archive`
  had been split off from the title and rendered as a stray line at the top of the page.
- **The package boundary is now an explicit table.** The registry artifact is the audited
  portable core (15 files); the GitHub repository is the complete project (31 files)
  including `openclaw/`.
- **`openclaw/README.md` version guard corrected** — it was still pinned to an older tag.

### Unchanged
- No change to any script, to permissions, to retention behaviour or to the security posture.

## 1.8.5 — 2026-09-09

Removes the last capability claims that did not match the published package.

### Fixed
- **The permissions section describes only the portable core.** The old table declared a
  "Shell / process" capability for launching an external CLI and PowerShell helpers, and
  the paragraphs below it described an optional hook that runs `pipeline.ps1`. Neither is in
  the published artifact. The section now lists file read, file write and environment
  variables only, and states plainly: **not declared because not used — network, MCP, shell,
  subprocesses**.
- **Every localised section now says the same thing.** The seven non-English sections of
  `README.md` and all eight summaries in `references/languages.md` previously described a
  layered pipeline, automatic backup/export, an integrity check against `pipeline.ps1` and a
  hook layer. They were rewritten as compact summaries of the portable core: what it is,
  where to install it, bounded retention, owner-only storage, confirmed deletion, licence.
- **`SKILL.md` no longer names a hook or a pipeline.** The OpenClaw quick start, the host
  table and the supply-chain section now refer to "host-specific automation" without
  implying it is part of, or launched by, this package.

### Notes
- The only remaining mentions of PowerShell are the explicit statements that the package
  contains none.

## 1.8.4 — 2026-09-09

Closes the two T09 findings from the ClawHub review of 1.8.3.

### Fixed
- **`--purge-only` no longer enumerates arbitrary `.db` files.** Candidates must match the
  complete artifact filename `{key}-YYYYMMDD-HHMMSS.db`. Each candidate is opened
  **read-only** first and must carry a valid `archive_metadata` row (app id
  `infinity-context`, a supported format version, the `archive_id` from the directory
  marker) and the expected `session_chunks` columns. `lstat` device and inode are re-checked
  immediately before the read-write open. Databases that fail any check are reported as
  `skipped` and never modified — including legacy archives without metadata.
- **A new archive file can no longer reuse an existing file.** Create mode (and append mode
  with no existing target) now reserves the path with `O_CREAT | O_EXCL | O_NOFOLLOW` and
  `0600`; a pre-existing file with the predicted name aborts with exit 10 instead of being
  hardened and written into. This closes the same-second / normalized-key collision path.

### Added
- `archive_metadata.archive_id`, generated per archive directory and stored in the marker;
  a database copied in from another archive is refused.
- `archive_metadata.app` and full column validation for `session_chunks`.
- `_test_v184.py`: purge-only scope (stray file, foreign database, wrong app, wrong
  archive id, legacy archive, symlink, tampered marker) and exclusive-create collision —
  16 checks.

## 1.8.3 — 2026-09-09

Fixes a real append-target selection bug found by the ClawHub review of 1.8.2.

### Fixed
- **`--append` no longer selects a database by filename prefix.** A sanitized key of
  `agent` used to match `agent-admin-20260909-010203.db`, and the lexicographically first
  match was opened read/write — so an append could insert rows into, and run retention
  purging against, another session's archive. Selection now requires the complete artifact
  name `{safe_key}-YYYYMMDD-HHMMSS.db`.
- **The append target is identity-checked before it is opened for writing.** The candidate
  is opened **read-only** first and must contain the exact `session_key` in the new
  `archive_metadata` table (archives created before that table fall back to an exact row
  check and are upgraded on the next write). A symlink, a foreign database, a path outside
  `--output-dir`, or more than one candidate aborts with exit 9 before any row is touched.
- **`--db-path`** selects an append target explicitly when more than one database matches,
  and is validated to live inside `--output-dir` and pass the same identity check.
- Retention purging can now only run against the database that passed the identity check.

### Added
- `archive_metadata (session_key, format_version)` table, written on create and append.
- `_test_v183.py`: overlapping keys (`agent` / `agent-admin`, `abc` / `abcd`), multiple
  timestamped databases, foreign databases with valid-looking names, explicit `--db-path`
  selection, legacy archives without metadata, and metadata upgrade — 19 checks.

## 1.8.2 — 2026-09-09

Documentation accuracy pass, driven by the ClawHub review of 1.8.1.

### Fixed
- **Retention wording is consistent everywhere.** The marketing claim that conversations are kept
  "forever" (and the Chinese equivalent) is gone. Every document now states the same policy:
  30 days by default, configurable `1..3650` days, no time limit only with the explicit
  `--allow-unbounded-retention` flag, `--purge-only` for a manual pass, and
  `INFINITY_CONTEXT_NO_ARCHIVE=1` to stop archiving.
- **No capability is claimed for code that is not in the package.** Mentions of the OpenClaw
  auto-wake / continuation behaviour and of the watchdog pipeline were removed from
  `README.md`, `说明.md`, `SKILL.md` and `references/languages.md`. Those components live only in
  the repository's `openclaw/` folder, which is outside the published artifact; the published
  docs now describe the portable core only.

### Changed
- `README.md`: the English and Simplified Chinese sections are rewritten around a 5-minute
  quick start, a "what it does" table, an explicit retention table, a FAQ, and Issues /
  Discussions links. The security section now describes only the published core.
- `说明.md`: rewritten end to end for the portable core (install, quick start, retention,
  security, data model, FAQ, limitations), with a single pointer to the repository integration.
- `references/languages.md`: watchdog references removed.

## 1.8.1 — 2026-09-09

Packaging boundary fix found by the ClawHub review of 1.8.0.

### Fixed
- **The published artifact now contains only the portable Python core.** The registry
  package previously shipped the repository's `openclaw/` folder as well, which
  contradicted the documented boundary ("no JavaScript, no PowerShell") and left
  executable hook files outside the root integrity manifest. `openclaw/` stays in the
  repository with its own `openclaw/checksums.txt`, and is no longer part of the
  published skill: the artifact is exactly the 14 files listed in `checksums.txt`.
- **`openclaw/cleanup-old-backups.ps1` no longer resolves Python through `PATH`.**
  The `Get-Command python3/python/py` lookup and the `print(1)` execution probe are
  gone. Python is taken only from an explicit root (`Program Files`, `Program Files
  (x86)`, `%LOCALAPPDATA%\Programs\Python`, `C:\Python3*`) or from the
  `INFINITY_CONTEXT_PYTHON` absolute-path override, and candidates are validated by
  existence only — never executed before being trusted.

## 1.8.0 — 2026-09-09

Bounded persistence: the archive now has a retention ceiling by default, an off switch,
and a manual retention pass. Documentation stops duplicating install instructions.

### Added
- **Retention is enforced, not advised.** `session_to_sqlite.py --retention-days N`
  (default **30**, range `1..3650`) deletes chunks older than `N` days from
  `session_chunks` and its FTS mirror inside the same transaction as the insert, and
  reports `purged_chunks` in the JSON result. Keeping chunks forever now requires the
  explicit `--allow-unbounded-retention` flag; `0` without it is rejected.
- **`--purge-only --output-dir <dir>`** applies the same retention policy to existing
  archives without ingesting anything. It only touches a directory that carries the
  owner-only archive marker, skips symlinked files, and skips any database that does not
  contain both `session_chunks` and `chunk_fts` (reported as `skipped`).
- **`INFINITY_CONTEXT_NO_ARCHIVE=1`** disables archiving entirely: the script writes no
  file, creates no directory, and returns `status: disabled`.
- `references/architecture.md` documents the exact file layout for a source install, so
  the docs no longer repeat a copy block in every language.

### Changed
- Install instructions are consolidated into one canonical block per document; the
  per-language sections point at it instead of repeating the same command list.
- SKILL.md, README.md and 说明.md carry the attribution line at the very bottom.

## 1.7.0 — 2026-09-09

Blast-radius containment for the destructive tools, plus capability disclosure.

### Fixed
- **`cleanup.py` is bound to a verified archive.** The archiver now writes an owner-only
  `.infinity-context-archive` marker (JSON: `app`, `marker_version`, `created_utc`) when it
  secures the archive directory. `cleanup.py` refuses to delete anything in a directory
  without a valid marker (`app=infinity-context`, supported marker version, regular
  non-symlink file owned by the current user), and refuses protected directories
  (filesystem root, the user home and its common subdirectories, system directories).
  `--init-marker` migrates an archive from an older version, and only after one of our
  databases is found in the directory.
- **Deletion scope is a full-filename allowlist, not an extension list.** Only
  `{safe_key}-YYYYMMDD-HHMMSS.{db,db-wal,db-shm,jsonl,jsonl.bak,bak}` are ever candidates;
  generic `.json`, `.tmp` and `.bak` files are untouched. Enumeration is non-recursive, and
  an unexpected subdirectory is skipped with a warning.
- **`VACUUM` is schema-gated.** A database is opened read-only first and vacuumed only when
  it really contains `session_chunks` and `chunk_fts`.
- **A confirmation boundary.** `--apply` now also requires `--confirm-destructive`; the
  validated scope (canonical root, marker, retention cutoff, file count, bytes) is printed
  first, and every candidate is re-checked with `lstat` immediately before `unlink`.

### Changed
- **Capability disclosure.** `SKILL.md` and `README.md` now open with an explicit
  "Security & Privacy Disclosure (Intended Behavior)" block that names the four local
  operations (persist, delete, in-place rewrite, path fallback) and their scope controls,
  and `SKILL.md` adds a first-run consent requirement so the agent asks before archiving.
  The frontmatter description also names the cleanup and redaction tools, so the declared
  capability set matches the shipped code.

## 1.6.6 — 2026-09-09

Reviewer-driven fail-closed fix for the non-ASCII output path.

### Fixed
- **The non-ASCII output-directory fallback is now opt-in.** The archiver refuses to
  move the archive when `--output-dir` cannot be encoded as ASCII (`status: error`,
  exit 8) instead of silently switching to `~/.openclaw/sqlite-data`. Passing
  `--allow-dir-fallback` restores the old behaviour, and the run still reports
  `archive_dir_fallback: true` with `requested_dir` and `archive_dir` and warns on
  stderr. The check runs before any directory or database is created, so a refused run
  leaves nothing behind.

## 1.6.5 — 2026-09-09

Reviewer-driven hardening of the 1.6.2 ingestion bounds and the filesystem guard.

### Fixed
- **Ingestion limits are validated.** `--max-session-bytes`, `--max-line-bytes`,
  `--max-messages` and `--max-total-chars` must be integers in `1..hard ceiling`; the
  CLI rejects anything else before opening a file, and `read_messages()` enforces the
  same range for library callers. A negative byte limit could otherwise reach
  `file.read(-1)` and pull the whole transcript into memory, and an oversized value
  could exceed the documented ceiling.
- **Every path component is checked for redirection.** `secure_fs` no longer inspects
  only the immediate parent: all existing components between the filesystem root and
  the target are checked with `os.path.islink`, and each component must also equal its
  resolved path, which catches Windows directory junctions (where `islink` is false).
  This closes `/trusted/link/subdir/archive.db`, where the link sits above the parent.

## 1.6.4 — 2026-09-09

Signature refresh requested by the author.

### Changed
- The attribution line at the end of `README.md` and `说明.md` now credits
  `deepseek-v4-flash/pro` without the stray separator and adds `Gemini3.8-flash`:
  `Pondsi (+MiMo-v2.5/v2.5pro+deepseek-v4-flash/pro+deepseek-v4.1-flash-expires-on-0910+GLM5.3-flash+Gemini3.1-pro+Qwen3.8-27b+Gemini3.8-flash) — automatically committed by Openclaw`.
- Source-install comments pin `v1.6.4` with the matching version guard.

## 1.6.3 — 2026-09-09

Documentation-parity release. The ClawHub review of 1.6.2 accepted the install-pin and
ingestion-bound fixes and raised one actionable documentation finding:

> The README advertises broad multilingual support, but most non-English sections omit
> or dilute the detailed privacy, retention, integrity-check, and auto-wake safety
> disclosures present in English.

### Fixed
- Every language section of `README.md` (简体中文, 繁體中文, 日本語, 한국어, Español,
  Português, Français, Deutsch, Русский) now carries the same "security and privacy"
  disclosure as English: local-only operation, full session-trajectory export before
  each compaction, redacted local SQLite/FTS5 archive, regex redaction plus
  `MAX_ARCHIVE_LENGTH` minimisation, fail-closed backup destruction, owner-only ACLs
  with 30-day retention, `enableAutoWake` opt-in with a validated single resume command
  and `WAKE_REQUEST` logging, deny-by-default agent allowlist, and `integrity.json`
  verification of `pipeline.ps1` before the hook runs.
- Source-install comments in every language now say "reviewed release tag" and pin
  `v1.6.3`, matching the version in `SKILL.md`.

## 1.6.2 — 2026-09-09

Install-instruction and ingestion-bound release. The ClawHub review of 1.6.1 accepted
the path-resolution fix and raised two remaining findings:

> Source installation instructions pin an obsolete release with known security
> deficiencies (T08, `SKILL.md:37-40`)
> Transcript size limits are enforced only after unbounded ingestion and regex
> processing (T09, `scripts/session_to_sqlite.py`)

### Fixed
- **T08 — stale source-install pin.** Every quick-start (English, Chinese, OpenClaw
  integration) now pins the tag that matches the reviewed artifact (`v1.6.2`), and a
  version guard stops the install when the checked-out `SKILL.md` version differs from
  the pinned tag. The tag and the frontmatter version are updated in the same commit,
  so the instructions can no longer drift behind the release.
- **T09 — limits applied during ingestion, not after it.** `read_messages()` now reads
  at most `--max-session-bytes` (64 MiB) from the head of the transcript instead of
  loading the whole file; a line longer than `--max-line-bytes` (1 MiB) is dropped
  *before* JSON parsing or regex; ingestion stops at `--max-messages` (200000) and
  `--max-total-chars` (64 MiB). The run reports `ingest.truncated` and
  `ingest.truncated_reason`, and logs `SECURITY_WARN: INGEST_TRUNCATED`, so a bounded
  archive is never mistaken for a complete one.
- `redact_file_in_place()` refuses a file larger than 64 MiB before reading it and
  reads with the same cap, so in-place redaction can no longer pull an unbounded file
  into memory.

## 1.6.1 — 2026-09-09

Path-resolution fix. The ClawHub review of 1.6.0 accepted the previous concerns but
found a precise remaining flaw:

> one file-redaction helper has a real path-scoping weakness that can rewrite
> user-writable files outside the declared directory through symlinked ancestors

### Fixed
- `redact_file_in_place()` now resolves every symbolic link before deciding scope.
  Three checks must all pass: the lexical path must be inside `--allow-dir`; the
  `realpath`-resolved target must be inside the resolved allowed directory; and the
  lexical relative path must equal the resolved relative path, which rejects any
  symlink traversal inside the allowed tree (a junction such as `allowed/jump/x` can
  no longer redirect the write outside the tree).
- The regression suite creates a real directory junction and proves that the outside
  file is refused and left untouched.

## 1.6.0 — 2026-09-09

Scope-and-transparency release. It addresses the two concerns the ClawHub reviewer
raised in the 1.5.0 audit ("under-scoped file mutation" and "can silently store
sensitive archives in an unexpected location").

### Changed
- **In-place redaction is scoped by construction.** `--redact-file` now refuses to run
  unless `--allow-dir` is supplied (exit 7), so the engine can never modify a file
  outside a directory the caller explicitly declares. The OpenClaw integration already
  passes the backup root.
- **The archive directory is never changed silently.** If a non-ASCII output path forces
  the SQLite store into the fallback directory, the run prints
  `SECURITY_WARN: ARCHIVE_DIR_FALLBACK` and the JSON result now carries `archive_dir`,
  `requested_dir` and `archive_dir_fallback`, so the effective location is always
  visible.

### Verified
- Regression suite extended with the `--allow-dir` requirement (refused without it,
  accepted with it).
- Three rounds: static/security, functional, and installed-copy end-to-end.

## 1.5.0 — 2026-09-09

Fail-closed redaction. The audit found that the redaction path itself still contained
silent failure branches: a broken rule file was ignored, an invalid regex was skipped,
the session key was stored verbatim, and a mid-write failure could leave partial data —
or, in append mode, delete a historical archive.

### Fixed
- **Rule loading is fail-closed.** `_load_redact_rules()` no longer swallows exceptions.
  Malformed JSON, a non-object schema, a non-list `custom_redact_rules`, a non-dict
  entry, an empty `pattern` or a non-string `replace` now raises `RedactionConfigError`
  and exits with code 2 **before any file or database is created**.
- **Rules are precompiled at startup.** Every built-in and custom pattern is compiled
  once; an uncompilable pattern aborts the run. `redact_sensitive_info()` no longer
  catches `re.error` and `continue` — an application-time failure raises instead.
- **`session_key` is sanitised before it is used.** It is validated against
  `^[A-Za-z0-9:_\-.@]{1,128}$` and passed through the redactor; anything else (or a
  value that itself looks sensitive) becomes `opaque-<sha256[:16]>`. The sanitised value
  is the only one used for filenames, the table and the FTS index, so a sensitive key can
  no longer leak through a file name.
- **Two-phase write with a non-destructive rollback.** The transcript is fully redacted
  in memory before the database is opened, then written in a single transaction. On
  failure the transaction is rolled back, the handle is closed first, and only a database
  created by that same run is deleted. In append mode the existing archive is never
  touched (`removed_new_db: false`).
- The rule path can be overridden with `INFINITY_CONTEXT_REDACT_RULES`, which the new
  regression tests use to feed deliberately broken rule files.

### Verified
- New regression suite: baseline redaction, malformed JSON, invalid regex, six wrong-type
  payloads, sensitive `session_key`, effective custom rule, non-destructive rollback for
  both new and existing databases, and source-level checks for silent-pass branches.
- Three rounds: static/security, functional, and installed-copy end-to-end.

## 1.4.0 — 2026-09-09

Fail-closed release. The archive now refuses to store readable data when it cannot
prove owner-only access, and the in-place redactor no longer uses a predictable
temporary file name.

### Changed (breaking for filesystems that cannot enforce owner-only access)
- **T09-1 — fail-closed permissions.** `secure_fs` no longer returns a "best effort"
  success. Every hardening step either proves the owner-only result (POSIX mode is
  re-read with `lstat`, ownership is checked) or raises `UnsafeArchiveError`.
  `session_to_sqlite.py` reacts by closing the SQLite handle first, destroying the
  half-written database and its `-wal`/`-shm` sidecars, and exiting with code 3.
  The only opt-out is the explicit `--allow-insecure-storage` flag, which prints a
  warning and reports `insecure_storage: true` in the JSON result.
- Symbolic links on the target path (file or parent directory) are refused, and a
  newly created archive directory is removed again if it cannot be secured.

### Fixed
- **T09-2 — predictable temporary file.** `redact_file_in_place` wrote to
  `<name>.redact.tmp`, which an attacker could pre-create as a symlink. It now uses
  `tempfile.mkstemp` (kernel `O_EXCL`, 0600) in the target directory, refuses symlinks
  and foreign-owned parent directories, `fsync`s before the atomic replace, removes the
  temporary file on every failure path, and re-applies owner-only permissions to the
  final file. The OpenClaw integration passes `--allow-dir` so the engine refuses paths
  outside the backup root.

### License
- The MIT license now carries an explicit **mandatory attribution** clause: any use of
  the source, including modified variants, must credit Pondsi. The requirement is
  repeated in `SKILL.md`, `README.md` (all languages) and `说明.md`.

### Verified
- Three rounds: static/security, functional (including fail-closed abort, symlink
  refusal, temporary-file leftovers, BOM), and installed-copy end-to-end.

## 1.3.3 — 2026-09-09

Robustness fix found while validating the published package end to end.

### Fixed
- **BOM-prefixed transcripts were silently dropped.** A JSONL transcript that starts
  with a UTF-8 byte-order mark made `json.loads` fail on the first line, and the
  archiver skipped it without a word — so a single-line transcript produced zero
  chunks. The reader now opens transcripts as `utf-8-sig`, which transparently
  consumes a BOM and behaves like `utf-8` otherwise. Verified both ways: a BOM file
  and a plain file each archive exactly one chunk.

## 1.3.2 — 2026-09-09

Documentation correctness release. Two defects in the 1.3.1 instructions would have
broken the promised out-of-the-box experience.

### Fixed
- **Registry slug.** Every install command said `clawhub install infinity-context`,
  but the published slug is `infinitycontext` (no hyphen). The command returned
  "Skill not found". All quick-starts, in every language, now use the real slug and
  show a concrete command for dsh / Claude Code (`--workdir ~/.agents --dir skills`)
  and for OpenClaw (`--workdir ~/.openclaw --dir skills`, or the workspace `skills/`
  directory, which wins).
- **dsh skill-discovery rules.** The docs claimed "the directory name must equal the
  frontmatter `name`". The official DeepSeek Harness documentation and the
  `dsh-skill-filesystem` package state otherwise: a skill is a directory bundle one
  level deep (`<root>/<dir>/SKILL.md`) or a flat `<name>.md`, nested `**/SKILL.md`
  files are deliberately not discovered, `name` and `description` are required, and
  `name` must be kebab-case. The folder name is not part of the identity — dsh
  addresses the skill by the frontmatter `name` — so the registry bundle
  `infinitycontext/` works as installed.

## 1.3.1 — 2026-09-09

Security-hardening release. Closes the two remaining audit warnings (T09 archive
permissions, T08 unpinned install instructions) and makes the skill a first-class
citizen on both DeepSeek Harness (dsh) and OpenClaw.

### Added
- `scripts/secure_fs.py` — owner-only filesystem hardening. POSIX forces `0700` on the
  archive directory and `0600` on files; Windows replaces the DACL with a protected DACL
  granting only the current user and LOCAL SYSTEM. Database files are created atomically
  with `os.open(..., 0o600)`, so no file ever exists with wider permissions (TOCTOU
  removed). A pre-existing directory owned by another account is refused; a merely
  over-permissive one is tightened; an unenforceable filesystem produces a loud warning
  and `permissions_enforced: false` in the JSON result.
- `checksums.txt` at the repository root: SHA-256 of every published file (except
  itself), so a source install can be verified byte-for-byte.
- `.gitattributes` (`* -text`) so checkouts are byte-identical on every platform and the
  manifest stays valid.
- `references/languages.md` — the localised summaries moved out of `SKILL.md`.

### Changed
- **T09 (archive permissions).** The archive directory, the database and the `-wal`/`-shm`
  sidecars are owner-only. Windows ACLs are written with in-process Win32 security API
  calls (`ctypes`); the directory ACE uses `(OI)(CI)` inheritance while file ACEs use
  plain `F`, and no external tool is spawned.
- **T08 (unpinned install).** Every quick-start now leads with the registry install and
  pins the audited release tag and verifies `sha256sum -c checksums.txt` for source
  installs. `cp -r` was replaced by explicit per-file copies in all languages.
- `SKILL.md` trimmed: the two canonical sections stay, long reference moved to
  `references/`. Frontmatter `description` now leads with the situations that should
  trigger the skill.
- `cleanup.py` and `search.py` refuse an archive directory owned by another account.

### DeepSeek Harness (dsh) and OpenClaw
- Both are documented as out-of-the-box hosts with an explicit install command for each.
- `openclaw/README.md` install steps now copy the shared Python engine and its helper.

## 1.3.0 — 2026-09-09

Structural release: the portable core and the OpenClaw/Windows integration are now
separate, so the audit findings T07 and T08 cannot recur by construction.

### Changed
- **Package split.** The published artifact contains the portable Python core only
  (`SKILL.md`, `scripts/*.py`, `references/`, docs, sponsors). All PowerShell and the
  OpenClaw hook moved to `openclaw/`, which is outside the published package.
- **T07 (tool hijacking) removed at the root.** The published package invokes no external
  command at all. In the integration folder every external binary is resolved to an
  absolute path from `System32` or a known install directory (`Resolve-TrustedExe`);
  `Get-Command`/`npm root -g` PATH lookups are gone, the process `PATH` is narrowed at
  entry, and a regex self-check confirms zero bare calls.
- **T08 (insecure dependencies) removed at the root.** The package is self-contained and
  installs nothing from the network. The optional integration is documented in
  `openclaw/README.md` with a pinned revision, `openclaw/checksums.txt` verification and
  an explicit file-by-file copy (no wildcards).

### Added
- `scripts/cleanup.py` — portable retention cleanup with canonical path anchoring,
  extension allowlist, symlink refusal, dry-run by default and `VACUUM`.
- `scripts/search.py` — read-only FTS5 retrieval with a `LIKE` fallback for short CJK
  queries.
- `references/architecture.md`, `openclaw/README.md`, `openclaw/checksums.txt`.

### DeepSeek Harness (dsh)
- Documented as a first-class host: `~/.agents/skills/infinity-context/` (rank 500) or
  `<project>/.agents/skills/infinity-context/` (rank 200), directory name must equal the
  frontmatter `name`, and dsh does not support recursive discovery.
- Frontmatter reduced to the Agent Skills fields; `version` moved into `metadata`.

## 1.2.1 — 2026-09-09

Registry-compliance release. ClawHub's static analysis rejects any package containing
self-executing JavaScript (`suspicious.dangerous_exec` on `child_process`), and there is
no suppression mechanism. The published package therefore ships **no `.js` files**.

### Changed
- The optional OpenClaw compaction hook (`src/handler.js`, `src/HOOK.md`,
  `src/integrity.json`) is now distributed **in the GitHub repository only**; it is not
  part of the registry package. `README.md`, `SKILL.md` and `说明.md` state this
  explicitly.
- Everything in the registry package runs as scripts the agent invokes through its
  declared tools — no hidden execution path.
- Verification extended to 3 rounds / 192 checks against the installed copy.

## 1.2.0 — 2026-09-09

Security & compliance hardening round (external audit findings).

### Fixed
- **Fail-closed redaction (T09)**: `pipeline.ps1` now destroys the trajectory artifact
  and aborts the backup whenever redaction is unavailable, exits non-zero, or throws.
  Plaintext retention requires an explicit opt-in (`$AllowUnredactedBackup = $true`).
- **Redactor resolution**: the redaction engine is now located in the script directory
  *or* `~/.openclaw/scripts/`, so the hook copy no longer silently skips redaction.
- **Intent/code divergence**: removed the external notification process
  (the external notification script) from the watchdog. Behaviour now matches the documented policy:
  over-limit, compaction failure and wake failure are **log-only**.

### Changed
- **Auto-recovery is declared, not hidden**: documented as an opt-in capability in the
  skill description, README, `说明.md` and the security notice. It is controlled by
  `enableAutoWake` in `infinity-context.config.json` (default: off).
- **Single attempt, no hidden loop**: replaced the 3 × 10 s blocking retry with one
  validated attempt per monitor round; verification happens on the next round.
- **Hardened entry point**: `Invoke-WakeSession` uses `[CmdletBinding()]` +
  `[ValidatePattern]`, and re-validates the session key before any process boundary.
- **Absolute executable paths**: `powershell.exe` and `taskkill.exe` are resolved from
  `%SystemRoot%\System32` instead of `PATH`.
- **Hook integrity**: `handler.js` verifies `pipeline.ps1` against `integrity.json`
  (SHA-256), rejects symlinks/empty files, requires the script marker, and refuses to
  execute on mismatch. `scripts/update-integrity.ps1` regenerates the manifest.
- **No redundant subprocess**: `pipeline.ps1` calls the Python engine directly instead
  of spawning a nested `powershell.exe`.
- **Host compatibility**: the skill is documented as a standard Agent Skills skill with
  first-class support for DeepSeek Harness (dsh); OpenClaw is optional. Frontmatter now
  declares `license`, `compatibility` and `metadata`.
- **Image metadata**: sponsor QR images had EXIF (including an embedded thumbnail and
  camera model) stripped losslessly — pixel data untouched, codes still scannable.

## 1.1.0 — 2026-09-08

Privacy & compliance hardening.

- Removed the shell-interpreter invocation; direct CLI launch with argument arrays and validation.
- Trajectory backups: ACL restricted to current user + SYSTEM, redacted before landing,
  30-day retention, partial destinations removed on failure.
- Redaction expanded (JWT, AWS, Google, Slack, PEM keys, connection strings, cookies,
  webhooks, phone numbers, emails) and applied **before** metadata derivation.
- Data minimization via `MAX_ARCHIVE_LENGTH` truncation; high-entropy candidates
  excluded from the keyword index.
- Declared `allowed-tools` scope; privacy notice added to README/SKILL/说明.
- `cleanup-old-backups.ps1` adds SQLite `VACUUM`.

## 1.0.0 — 2026-09-08

First public release.

- Deny-by-default agent allowlist (fail-closed; no allow-all fallback).
- No agents-directory enumeration; agent derived from the session key.
- `cleanup-old-backups.ps1` hardening: `ValidateRange(1..3650)`, canonical path
  anchoring, extension allowlist, reparse-point skip, `-WhatIf` support.
- `compaction-pipeline` hook: backup + SQLite + enhanced summary on every compaction path.

## Earlier (0.1.x)

Internal iterations: dual-condition trigger, `session_chunks` table fix, UTF-8 forcing,
Windows path fixes, sticky-state fixes, hook wiring, temp-file Python invocation.
