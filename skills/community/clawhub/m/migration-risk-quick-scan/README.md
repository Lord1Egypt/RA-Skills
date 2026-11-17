# Migration Risk Quick-Scan (Free Edition)

A free, deterministic scanner that checks **raw PostgreSQL migration
files** for the 10 patterns that most often break production databases:
dropped tables/columns, `TRUNCATE`, unscoped `UPDATE`/`DELETE`, renames,
`NOT NULL` without a default, non-concurrent index builds, and type
narrowing.

## Usage

```bash
python3 scripts/scan_risks.py --path migrations/
```

Prints JSON: per-file findings (rule, severity, line, explanation,
one-line recommendation) and a summary verdict
(`GO` / `GO WITH FIXES` / `NEEDS EXPAND-CONTRACT` / `NO-GO`).
Python 3.9+, standard library only. It never connects to a database and
never modifies your files. Paired rollback files (`*.down.sql`) are
skipped automatically; SQL comments are ignored by the matcher.

See `examples/` for a sample input and the scanner's real output on it.

## What the free edition does NOT do

- No Prisma / Django / Alembic adapters (raw SQL only)
- No expand–contract **rewrites** of your migrations
- No application-code cross-checks (is anything still reading that
  dropped column?)
- No rollback plans, no severity taxonomy beyond the top-10

## Full edition

The complete **Zero-Downtime DB Migration Auditor** skill is available
on PromptBase. It adds:

- Prisma, Django and Alembic support (25+ patterns)
- Per-migration GO / NEEDS EXPAND-CONTRACT / NO-GO verdicts
- Application-code cross-checks for dropped/renamed columns
- Ready-to-apply expand–contract rewrites of breaking migrations
- A concrete rollback plan for every migration, with irreversible steps
  flagged before you deploy — not after
