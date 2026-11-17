# Migrations — Getting a Schema Change Into a Database You Cannot Reset

Prisma Migrate is forward-only and diff-based: it compares your schema to a computed state and writes SQL. Everything painful about it comes from one of three places — the diff proposing destruction, the history disagreeing with the database, or a command being run in the wrong environment.

## Contents

- Command matrix
- The shadow database
- Renames without data loss
- Baselining an existing database
- Drift
- Failed migration recovery (P3009)
- Statements migrate cannot wrap
- Zero-downtime sequences
- CI and production pipeline
- Review checklist

## Command Matrix

| Command | What it does | Where it belongs |
|---|---|---|
| `prisma migrate dev` | Applies pending, diffs schema vs shadow DB, writes a new migration, applies it, runs `generate`, seeds on reset | Development only |
| `prisma migrate dev --create-only` | Writes the SQL and stops, without applying | Any change whose SQL you must edit (renames, concurrent indexes, backfills) |
| `prisma migrate deploy` | Applies pending migration files. Never generates, never resets, never touches a shadow DB | CI and production, exclusively |
| `prisma migrate status` | Which migrations are applied, pending, or failed | First command in any migration incident |
| `prisma migrate resolve --applied <name>` | Records a migration as applied without running it | Baselining, and after applying SQL by hand |
| `prisma migrate resolve --rolled-back <name>` | Clears a failed entry after you reverted its effects | P3009 recovery |
| `prisma migrate diff` | Prints SQL between any two states (empty, schema, database, migrations folder) | Baselines, rollback scripts, review diffs |
| `prisma migrate reset` | Drops everything, replays history, seeds | Local and CI test databases only |
| `prisma db push` | Makes the database match the schema with no history, dropping what does not fit | Throwaway prototypes and ephemeral preview branches |
| `prisma db pull` | Rewrites the schema from the database | Introspection-first workflows, and drift diagnosis |
| `prisma db execute --file x.sql` | Runs raw SQL against the datasource | Statements Migrate cannot wrap (below) |
| `prisma db seed` | Runs the script named in `package.json` → `prisma.seed` | Local resets, CI fixtures |

## The Shadow Database

`migrate dev` builds a second, temporary database, replays the whole migration history into it, and diffs it against your schema. That is how it detects drift and computes SQL that assumes nothing about your local mess.

- It needs permission to create and drop a database. Managed providers that refuse this need an explicit, separate `shadowDatabaseUrl` in the datasource block — a second empty database, not the production one.
- `migrate deploy` never uses it. A shadow-database error in a production pipeline means someone put `migrate dev` in the pipeline.
- P3006 (migration fails to apply cleanly to the shadow database) means your history is not replayable from zero, usually because an earlier migration was hand-edited after being applied. Fix the historical file or squash the history in a maintenance window; do not disable the check.

## Renames Without Data Loss

The diff is name-based, so a rename is invisible to it: it sees a dropped field and a new one.

1. Preferred: do not rename in the database at all. `name String @map("fullName")` renames only in Prisma and generates zero SQL.
2. When the column must really be renamed: `npx prisma migrate dev --create-only`, then replace the generated `DROP COLUMN`/`ADD COLUMN` pair with `ALTER TABLE "User" RENAME COLUMN "fullName" TO "name";`, then apply. Review that the generated file contains nothing else you did not intend.
3. Never edit a migration that has already been applied anywhere — that is the direct route to P3006 and to two environments with the same history and different schemas.

## Baselining an Existing Database

For a database that predates Prisma, or one whose `migrations` folder was lost:

```bash
npx prisma db pull                                   # schema from the live database
mkdir -p prisma/migrations/0_init
npx prisma migrate diff \
  --from-empty --to-schema-datamodel prisma/schema.prisma --script \
  > prisma/migrations/0_init/migration.sql
npx prisma migrate resolve --applied 0_init          # record it without running it
```

P3005 ("database schema is not empty") is exactly this situation announcing itself. Baseline every environment before the first real migration reaches any of them.

## Drift

Drift means the database no longer matches what the history says it should be. `migrate dev` reacts by offering a reset; in a database with data, that offer is the incident.

Diagnose before answering anything:

```bash
npx prisma migrate status
npx prisma migrate diff \
  --from-migrations ./prisma/migrations \
  --to-schema-datasource prisma/schema.prisma --script    # what the DB has that history does not
```

| Cause | Tell | Resolution |
|---|---|---|
| Someone ran `db push` | Schema matches the models but no migration explains it | Generate the equivalent migration and `resolve --applied` |
| Manual DDL (an index, a trigger, a column) | Diff shows objects Prisma never wrote | Adopt it into a migration, or accept it will be proposed for deletion forever |
| A migration applied then hand-edited | P3006 on the shadow database | Restore the file to what was applied; write a new migration for the change |
| Branch switch | Migrations exist in the DB that are absent from the folder | Rebase the branch, do not reset the database |
| Failed migration left partial state | `migrate status` shows a failed entry | P3009 recovery, below |

## Failed Migration Recovery (P3009)

A failed migration stays recorded as failed, and every later `migrate deploy` refuses to run — deliberately, so nobody stacks changes on an unknown state.

1. `npx prisma migrate status` — name the failed migration.
2. Inspect the database and decide what actually landed. On PostgreSQL each migration file runs inside a transaction, so a failure usually rolled the whole file back; on MySQL DDL is not transactional, so partial application is normal.
3. If nothing landed: fix the SQL, then `npx prisma migrate resolve --rolled-back <name>` and deploy again.
4. If it partially landed: finish or undo it by hand (`prisma db execute --file fix.sql`), then `npx prisma migrate resolve --applied <name>`.
5. Only then deploy. Adding a new migration to "fix forward" while the failed entry is still recorded leaves the history lying about the database.

## Statements Migrate Cannot Wrap

PostgreSQL migrations run inside a transaction, which is what makes them atomic — and what makes these fail:

- `CREATE INDEX CONCURRENTLY` / `REINDEX CONCURRENTLY` → "cannot run inside a transaction block".
- Long backfills that would hold a transaction open for the whole run.

Pattern for both: create the migration with `--create-only`, keep the transactional parts in it, and run the non-transactional statement separately with `prisma db execute` (or by hand in a maintenance window), then `migrate resolve --applied`. Record what you did in the migration folder — a `README` next to the SQL is worth more than the memory of whoever was on call.

## Zero-Downtime Sequences

Old and new code run simultaneously during any deploy. Every change that both must survive is expand → migrate → contract, across three deploys:

| Change | Deploy 1 (expand) | Deploy 2 (migrate) | Deploy 3 (contract) |
|---|---|---|---|
| Rename a column | Add the new column, write both, read old | Backfill in batches, switch reads to new | Stop writing old, drop it |
| Add a NOT NULL column | Add it nullable with a default | Backfill, then set NOT NULL | — |
| Change a type | Add the new column | Dual-write, backfill, verify equality | Drop the old column |
| Drop a column | Stop reading it in code | — | Drop it, one deploy later |
| Split a table | Create the new table, dual-write | Backfill, move reads | Drop the old columns |

Backfills belong in a script with batching and a resume key, not in a migration file: one `UPDATE` across ten million rows holds a transaction, blocks the deploy, and discards everything if it fails at minute forty. Batch size 1k-50k rows per commit, sized so a batch finishes in under a second at production load.

## CI and Production Pipeline

```bash
npx prisma migrate deploy        # release step, before the new code starts serving
npx prisma generate              # build step, always, on every install path
```

- `migrate deploy` takes an advisory lock so two concurrent deploys cannot apply the same migration twice. Disabling it (`PRISMA_SCHEMA_DISABLE_ADVISORY_LOCK`) is only for engines that cannot hold one — do not disable it to make a flaky pipeline quieter.
- Run migrations as a separate release step, not from application startup: N application instances booting means N racing migration attempts, and the lock turns that into N-1 slow starts at best.
- The database user for `migrate deploy` needs DDL rights; the application user should not have them. Two URLs, two roles.
- There are no down migrations. If you need a rollback path, generate the inverse script at authoring time with `migrate diff` between the two schema states and commit it next to the migration — then it exists at 3am.
- Squashing history is legitimate once a project has hundreds of migrations and every environment is past them: baseline from the current schema (above), archive the old folder, and confirm each environment's `_prisma_migrations` table before deleting anything.

## Review Checklist

- Does the generated SQL contain a `DROP` you did not ask for? That is a rename or a drifted database.
- Does it drop an index, trigger or view someone created by hand?
- Is the destructive part separated into its own later migration?
- Is a backfill needed, and is it batched and resumable?
- Was this run with `--create-only` because the SQL needed editing, and is the edit still consistent with the schema?
- Does the environment that will run it use `migrate deploy` and nothing else?
