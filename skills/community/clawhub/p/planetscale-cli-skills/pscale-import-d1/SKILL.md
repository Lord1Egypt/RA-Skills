---
name: pscale-import-d1
description: Import Cloudflare D1 SQLite exports into PlanetScale Postgres with pscale import d1. Use when migrating from Cloudflare D1, linting D1 exports, converting SQLite schema to PostgreSQL DDL, starting/resuming D1 imports, verifying row counts/content, or completing local migration state. Triggers on pscale import d1, Cloudflare D1 migration, D1 export, SQLite to Postgres import, pgloader, D1 verify.
---

# pscale import d1

Import a Cloudflare D1 database export into PlanetScale Postgres using `pscale import d1`.

## Capabilities

The `pscale import d1` command group supports offline Cloudflare D1 migrations. It lints a D1 SQL export, converts SQLite DDL to PostgreSQL DDL, loads data into a PlanetScale Postgres branch, stores local migration state, and verifies the import.

All commands support `--format json` through the global pscale flag; use JSON for agent automation.

## Prerequisites

```bash
# Export D1 using Wrangler first
wrangler d1 export <d1-database-name> --remote --output ./d1-export.sql

# Verify local import prerequisites such as pgloader
pscale import d1 doctor --format json
```

`start` requires `pgloader` on `PATH`. For small databases, `--method psql` uses `psql` for schema and `pgloader` for data; for larger exports, use `--method pgloader`.

### SQLite configuration isolation

pscale isolates its internal `sqlite3` calls from `~/.sqliterc` and forces batch, no-header output. User settings such as `.headers on` or `.mode column` therefore do not corrupt D1 import row-count and verification parsing. Integer parsing is strict, stderr stays separate from parsed output, and unusual SQLite identifiers are quoted correctly.

If a D1 import or verification fails with unexpected SQLite output, upgrade pscale to the current release and rerun the same migration step. Treat an `unexpected output` error on a current release as a real parsing/data problem, and preserve the reported output and stderr when troubleshooting.

The CLI hardens generated identifiers and output paths in D1 migration state. Keep migration IDs and output paths literal, avoid deriving filenames from untrusted input in wrapper scripts, and preserve the CLI's final wait/status output before deciding whether to resume, verify, or mark complete.

### Schema conversion behavior

Use the current CLI before converting an untrusted D1 export. The CHECK-expression parser treats doubled SQL quotes as escaped quotes and does not treat backslashes as quote escapes, preventing quoted text from prematurely ending an expression during DDL generation. Still treat the export and generated DDL as untrusted input and inspect the complete conversion before applying it.

The current converter preserves and translates more SQLite schema semantics, including column- and table-level `CHECK` constraints, named constraints, generated columns, `NUMERIC`/`DECIMAL` precision, and common computed defaults such as `date('now')`, `time('now')`, `randomblob()`, UUID generators, and `CAST(unixepoch() AS TEXT)`. For columns inferred as PostgreSQL booleans, integer `0`/`1` literals in applicable `CHECK` comparisons, `IN`, and `BETWEEN` expressions are rewritten to `false`/`true`; non-boolean columns and decimal-like literals are left unchanged. SQLite `VIRTUAL` generated columns are materialized as PostgreSQL `STORED` generated columns because PostgreSQL 16 supports only stored generated columns.

Cloudflare's `_cf_METADATA` table is internal D1 bookkeeping. The current CLI excludes it from schema conversion, data loading, and verification rather than importing it as application data. `lint --format json` still reports it in `issues` as the expected, non-blocking info issue `CLOUDFLARE_D1_METADATA`, with remediation explaining that it is not imported; do not treat that issue as something to fix.

Inside `CHECK` and generated expressions, the converter rewrites selected SQLite-only forms when it recognizes a supported shape that produces valid PostgreSQL syntax—for example, `ifnull()` to `coalesce()`, `iif()` to `CASE`, `instr()` to `strpos()`, `json_valid()` to `IS JSON`, `==` to `=`, and literal `GLOB`/`REGEXP` operators to `~`. Supported date/time rewrites are limited to current-time forms; JSON paths and pattern operands generally need string literals. Function forms `glob()` and `regexp()` are not rewritten, and both are reported as `SQLITE_FUNCTION`. Issue messages hard-code uppercase `GLOB()`/`REGEXP()` for non-literal operator cases; function-form `glob()` preserves the spelling used in the schema (for example, `glob()`), while function-form `regexp()` is detected by the operator fallback and reported as uppercase `REGEXP()`.

These rewrites guarantee neither source semantic equivalence nor complete lint coverage. `json_valid(value, flags)` currently drops the flags argument; `unixepoch()` in `CHECK` and generated expressions maps to `now()` without consulting the destination column type, so an integer-epoch comparison can convert silently and fail at DDL apply; `strftime('%s', 'now')` remains unconverted and is reported as `SQLITE_FUNCTION`; and a double-quoted `GLOB`/`REGEXP` right operand that matches a column name can be misread as a literal. Other unsupported calls—including scalar `max()`/`min()`, function-form `like()`, `format()`, and `date(column)`/`time(column)`—can pass `lint` and then fail or behave differently when PostgreSQL loads or evaluates the DDL. Any lint error blocks `start`, including `--dry-run`.

Supported `strftime()` current-time defaults are mapped according to the inferred destination type: common ISO/date formats on timestamp-like columns, `%s` epoch seconds on numeric columns, and safe day/hour/minute/second or `start of day|month|year` modifiers. `utc` and `localtime` modifiers are treated as no-ops in this UTC-oriented mapping. Unsupported formats, time values, or modifiers such as `weekday N` and calendar-month arithmetic are not guessed; on an inferred non-text destination the converter can omit that default, so inspect the generated DDL and restore an equivalent PostgreSQL expression deliberately when needed.

Defaults and foreign-key action clauses are emitted only when they match validated literal or clause forms. Malformed or untrusted expressions are omitted instead of being copied verbatim into executable PostgreSQL DDL, and parsing stops at the balanced end of each `CREATE TABLE` body so trailing statements are not treated as schema content. Treat an omitted default, reference action, or invalid foreign key as a migration warning: inspect the generated DDL and restore only a reviewed PostgreSQL equivalent.

Foreign keys are applied after tables, data, and indexes rather than relying on `CREATE TABLE` order. This supports cyclic relationships, case-insensitive target matching, schema-qualified and quoted/bracketed references, and column-less references that resolve to the parent primary key; composite foreign-key columns map positionally to the corresponding parent columns. Replay-safe constraint replacement uses `DROP CONSTRAINT IF EXISTS` before `ADD CONSTRAINT`, and generated names are bounded for PostgreSQL. Still inspect lint and converted DDL for unresolved targets, type coercions, actions, and the exact parent-column mapping before a real import.

Still review `convert-schema` output before loading. Expression or partial indexes, views, triggers, and other constructs reported by `lint` can require manual migration decisions; do not assume a successful conversion is semantically identical without inspecting constraints, defaults, generated expressions, foreign-key types, and indexes.

## Recommended migration workflow

Treat these as sequential gates. Inspect step 1's JSON and do not run `start --dry-run` until `error_count` is `0`; warnings may be reviewed and accepted, but errors cannot.

```bash
# 1. Lint the D1 export before touching PlanetScale
pscale import d1 lint --input ./d1-export.sql --format json

# 2. Convert and review the PostgreSQL DDL; lint does not recognize every incompatibility
pscale import d1 convert-schema \
  --input ./d1-export.sql \
  --output ./d1-schema.sql \
  --format json

# 3. Preview the import plan and save a migration ID without loading data
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --dry-run \
  --format json

# 4. Review warnings, converted DDL, and the migration ID from the dry-run
MIGRATION_ID=<migration-id-from-json>

# 5. Run the import after the user confirms the target database/branch
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --migration-id "$MIGRATION_ID" \
  --method pgloader \
  --format json

# 6. Verify source/target counts, sequences, coercions, and content checks
pscale import d1 verify <database> <branch> \
  --migration-id "$MIGRATION_ID" \
  --input ./d1-export.sql \
  --format json

# 7. Mark local migration state complete when verification passes
pscale import d1 complete <database> <branch> --migration-id "$MIGRATION_ID" --format json
```

If `<branch>` is omitted, pscale uses the default branch. Prefer passing the branch explicitly in automation to avoid importing into the wrong target.

## Command map

| Command | Purpose | Typical use |
|---------|---------|-------------|
| `pscale import d1 doctor` | Check local prerequisites | Run before migration to confirm `pgloader` and toolchain availability |
| `pscale import d1 lint --input FILE` | Analyze D1 SQL export | Catch SQLite/D1 features that need manual handling |
| `pscale import d1 convert-schema --input FILE --output schema.sql` | Convert SQLite DDL to PostgreSQL DDL | Review generated schema before loading |
| `pscale import d1 start <database> [branch] --input FILE` | Lint, plan, and load data | Use `--dry-run` first; reuse `--migration-id` for the real run |
| `pscale import d1 status <database> [branch] --migration-id ID` | Show local migration state | Resume or inspect in-progress migration state |
| `pscale import d1 verify <database> [branch] --migration-id ID` | Verify row counts/content | Required before declaring migration complete |
| `pscale import d1 complete <database> [branch] --migration-id ID` | Mark local migration complete | Use only after successful verification |

## Safety rules for agents

1. Treat D1 import as a data migration: identify org, database, branch, export path, and method before running non-dry-run commands.
2. Run `lint` first. Fix every error and re-lint; only then run `start --dry-run` and summarize warnings plus the migration ID.
3. Do not run non-dry-run `start` or `complete` without explicit user confirmation of the target and source export.
4. Prefer `--format json` and preserve the JSON output path/summary for auditability.
5. Use an explicit branch argument and `--dbname` when the destination PostgreSQL database name is not `postgres`.
6. PostgreSQL connections created during import use verified TLS by default; do not weaken that behavior in surrounding tooling.
7. Verify after loading; do not call the migration complete until `verify` succeeds.

The generated destination connection uses `sslmode=verify-full` with `sslrootcert=system`, avoiding libpq's fallback to a missing `~/.postgresql/root.crt`. Libpq 16+ supports the special `system` value; non-libpq driver support is version-specific. Check the actual consumer before reusing an equivalent destination URI. For any consumer that does not support `sslrootcert=system`, including drivers that treat it as a filename, keep `sslmode=verify-full` and replace `system` with an explicit approved trusted CA-bundle path, or upgrade to verified support. Never disable certificate or hostname verification or drop TLS parameters to make the connection work.

Verification normalizes UUID case before comparing source and destination signatures. With an explicit `--sqlite`, omit `--input`: the CLI then loads the original export path from `--migration-id` and fails if that migration state cannot be loaded. Preserve both the local migration state and the original export at its recorded path because verification still parses the export for schema/type context. Supplying `--input` and `--sqlite` together bypasses validation of the input path against saved state, so a mismatched export can produce misleading results.

## Troubleshooting

### `pgloader` missing

Run:

```bash
pscale import d1 doctor
```

Install `pgloader`, then rerun `doctor`. Do not bypass this by starting a real import.

### Lint errors block all starts

Inspect `error_count`, `warning_count`, and each entry in `issues`. Any `severity: "error"` issue makes `can_proceed` false, and `start` returns a `LINT_BLOCKED` error before both a real import and `--dry-run`. `--force` cannot override this gate; it only skips the human confirmation prompt after lint passes.

Follow each issue's `remediation`, fix the source export, and rerun `lint` until `error_count` is `0`. `SQLITE_FUNCTION` identifies recognized unsupported SQLite-only calls and non-literal `GLOB`/`REGEXP` operators, but not every PostgreSQL-incompatible call, so also review `convert-schema` output. Warnings do not block `start` and may be consciously accepted after review; errors cannot.

### Resume an interrupted migration

```bash
pscale import d1 status <database> <branch> --migration-id <existing-migration-id> --format json
pscale import d1 start <database> <branch> \
  --input ./d1-export.sql \
  --migration-id <existing-migration-id> \
  --format json
```

Use the same export file and target branch unless intentionally restarting the migration.

## References

See `references/commands.md` for the current `pscale import d1` command reference.
