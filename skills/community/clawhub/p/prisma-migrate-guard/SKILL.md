---
name: prisma-migrate-guard
description: Preflight Prisma migration state before deploy; fails fast on drift, failed migrations, missing DB URLs, or unapplied migration files.
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","node","npx"]}}}
---

# Prisma Migrate Guard

Use this skill before deploys or CI release steps to verify Prisma migrations are healthy and ready to apply.

## What this skill does
- Verifies required Prisma CLI/runtime tools are available
- Validates migration DB URL inputs (`DATABASE_URL` by default)
- Runs `prisma migrate status` against a target schema
- Fails on common dangerous states:
  - failed migrations
  - migration drift warnings
  - unapplied migration files
  - missing migration history table hints
- Exits non-zero for CI/deploy gating

## Inputs
- Optional env vars:
  - `PRISMA_SCHEMA_PATH` (default: `prisma/schema.prisma`)
  - `PRISMA_MIGRATE_DB_URL_ENV` (default: `DATABASE_URL`)
  - `PRISMA_MIGRATE_GUARD_ALLOW_UNAPPLIED` (`1` to warn instead of fail)
  - `PRISMA_MIGRATE_GUARD_ALLOW_DRIFT` (`1` to warn instead of fail)

## Run

```bash
bash scripts/check-prisma-migrate.sh
```

With explicit schema and env key:

```bash
PRISMA_SCHEMA_PATH=apps/api/prisma/schema.prisma \
PRISMA_MIGRATE_DB_URL_ENV=POSTGRES_PRISMA_URL \
bash scripts/check-prisma-migrate.sh
```

## Output contract
- Prints a concise PASS/FAIL report
- Exit code `0` on healthy status
- Exit code `1` on blocking migration issues

## Notes
- This guard is read-only (`migrate status`), it does not apply migrations.
- Keep it in CI before deploy or startup migration steps.
