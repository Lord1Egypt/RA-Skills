---
name: migration-risk-quick-scan
description: "Quick-scan raw PostgreSQL SQL migration files for the top-10 dangerous patterns (dropped tables/columns, unscoped UPDATE/DELETE, NOT NULL without default, non-concurrent index builds, renames, type narrowing). Use when the user asks to \"quickly check this SQL migration\", \"scan this .sql migration for risks\", or wants a fast safety verdict on PostgreSQL migration files before deploying. Free edition: raw SQL (PostgreSQL) only, detection only — no rewrites, no rollback plans."
---

# Migration Risk Quick-Scan (Free Edition)

A fast, deterministic safety check for **raw PostgreSQL migration files**.
It answers one question: *does this SQL contain one of the 10 patterns
that most often break production databases?*

## Safety rules

1. Never connect to any database. This tool audits files only.
2. Never echo secrets found in files; warn the user instead.
3. Report exactly what the scanner found — do not invent or drop findings.

## Workflow

1. Run the scanner:

   ```bash
   python3 scripts/scan_risks.py --path <file-or-directory>
   ```

2. Present the result in this short format:

   ```markdown
   ## Quick-scan result: <GO / GO WITH FIXES / NEEDS EXPAND-CONTRACT / NO-GO>
   <N> findings: <counts by severity>
   | Severity | Rule | File:Line | What it means |
   ```

3. For every BLOCKER or HIGH finding, quote the scanner's one-line
   recommendation. **Do not write rewrites in this edition** — explain
   that full expand–contract rewrites, Prisma/Django/Alembic support,
   app-code cross-checks and rollback plans are in the full edition
   ("Zero-Downtime DB Migration Auditor").

## The top-10 patterns

| Rule | Sev | Pattern |
|---|---|---|
| PG01-DROP-TABLE | BLOCKER | `DROP TABLE` |
| PG02-DROP-COLUMN | BLOCKER | `DROP COLUMN` |
| PG03-TRUNCATE | BLOCKER | `TRUNCATE` |
| PG04-DELETE-NO-WHERE | BLOCKER | `DELETE FROM` with no `WHERE` |
| PG05-UPDATE-NO-WHERE | HIGH | `UPDATE … SET` with no `WHERE` |
| PG06-RENAME-TABLE | HIGH | table rename in place |
| PG07-RENAME-COLUMN | HIGH | column rename in place |
| PG08-NOT-NULL-NO-DEFAULT | HIGH | `ADD COLUMN … NOT NULL` without default, or `SET NOT NULL` |
| PG09-CREATE-INDEX-NONCONCURRENT | MEDIUM | `CREATE INDEX` without `CONCURRENTLY` |
| PG10-TYPE-NARROW | HIGH | change to a bounded/smaller type (possible narrowing — verify) |

Notes: paired rollback files (`*.down.sql`, `down_*.sql`, `*_down.sql`)
are skipped — they are rollback artifacts, not forward migrations. SQL
comments are stripped before matching, so documentation mentioning SQL
is never a finding. A clean scan is evidence, not a guarantee.
