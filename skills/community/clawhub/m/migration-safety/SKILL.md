---
name: migration-safety
description: Review a schema migration for production safety under live traffic — destructive operations (dropped/renamed columns or tables, type narrowing) gated behind expand-contract plans, lock-taking DDL flagged with the specific lock and its duration driver, the deploy-order contract checked both ways (old code on new schema during rollout, new code on old schema during rollback), backfills separated from DDL and batched, and a rollback path stated per migration. Never executes migrations or DDL. Use this skill whenever the user says "review this migration", "is this migration safe", "will this lock the table", "zero-downtime migration", "check the schema change", "expand and contract", "review the EF migration / alembic / prisma migrate diff", or "/migration-safety" — even if they don't name the skill. Distinct from sql-review (T-SQL antipatterns in procs); this reviews SCHEMA CHANGES against live traffic and deploys.
---

# Migration Safety

A migration runs once, against the production database, usually mid-deploy, while old and new application code overlap. This skill reviews it for the three ways that goes wrong: **locks** (DDL that blocks traffic), **ordering** (schema and code versions that can't coexist), and **irreversibility** (data destroyed with no path back). The core discipline: every migration is judged against the deploy timeline, not against an empty dev database where everything is instant and nothing is watching.

## When to use this skill

- The user says "review this migration", "is this migration safe", "will this lock the table", "zero-downtime", "expand and contract", "check the schema change", "/migration-safety".
- A migration file (EF Core, Prisma, alembic, Rails, Flyway, raw DDL) sits in the diff.
- `ship-it` flags a migration and it needs the dedicated pass.

Do **not** auto-trigger for stored-procedure or query changes (`sql-review`) or for greenfield schemas with no production data — on an empty database most of this catalog is N/A, and the report should say that in one line instead of performing the checklist. This skill **never executes** migrations, DDL, or any SQL against a database — it reads files and reports.

## Workflow

1. **Establish the context the file doesn't show.** Which engine (Postgres/MySQL/SQL Server/SQLite — lock behavior differs by engine and version, and a lock claim that doesn't name the engine is a guess)? Is there production data, and are the touched tables large or hot? Get evidence where possible (the user, a row-count comment, table names like `events`/`audit_log` that are large by nature) — otherwise label the assumption out loud: "assuming `orders` is large and hot; if it's small, findings 2–3 downgrade to noise." How do migrations deploy relative to code (before app deploy? in the same release?) — this determines step 4's ordering checks.
2. **Walk the destructive-operation gate.** `DROP COLUMN`/`DROP TABLE`, column/table **renames** (a rename IS a drop+add to running code), type **narrowing** (`varchar(500)→(50)`, `bigint→int`, nullable→`NOT NULL`), truncates, and `DELETE`/`UPDATE` data mutations. Each is a **blocker unless** an expand-contract plan is stated: expand (add the new thing, dual-write or backfill), migrate readers, contract (drop the old thing **in a later release**, after old code is provably gone). Drop-in-the-same-release-as-the-code-change fails the rollback test by construction.
   - ❌ "Renamed `users.name` to `users.full_name` in one migration — the ORM was updated too, so it's fine."
   - ✅ "Rename is drop+add to the old code still running during rollout: add `full_name`, backfill, deploy code reading `full_name` (writing both), then drop `name` in release N+2. Or, if the deploy has real downtime, say so and the one-step rename is fine — name the assumption."
3. **Flag lock-taking DDL with the specific mechanism.** Name the lock and what drives its duration — "might be slow" is not a finding. The high-yield catalog: index creation without `CONCURRENTLY` (Postgres: blocks writes for the whole build) or `ONLINE = ON` (SQL Server, edition-permitting); `NOT NULL` added without engine-appropriate staging (Postgres: `ADD CONSTRAINT ... NOT VALID` then `VALIDATE`; adding a column `NOT NULL` **with** a constant default is metadata-only on modern PG/SQL Server — don't flag what's actually free, that's severity inflation); full-table-rewrite type changes; adding an FK without `NOT VALID`+`VALIDATE`; MySQL DDL without an online strategy on big tables. For each: the operation, the lock, the duration driver (table size, write rate), and the non-blocking alternative.
4. **Check the deploy-order contract both ways.** During rollout, **old code runs against the new schema** — every added `NOT NULL`-without-default, dropped column old code still selects, or renamed anything breaks it. During rollback, **new-ish data meets old schema expectations** — rows written by new code must not violate what old code assumes. Trace both directions against the actual code in the diff (grep for the column names old code uses). Also: does anything in the release *require* the migration to have run (new code reading a column that doesn't exist yet) — if so the migrate-then-deploy ordering is load-bearing; say it.
5. **Separate backfills from DDL.** Data backfills inside the schema migration (same transaction as DDL, or a single `UPDATE table SET ...` over millions of rows) are findings: long transactions hold locks, bloat undo/WAL, and can't checkpoint. Recommendation shape: DDL migration adds the nullable column; a separate batched job (with progress + resumability) backfills; a later migration adds the constraint. Small-table backfills are fine — say why (the size evidence or assumption from step 1).
6. **Demand the rollback path, per migration.** Three honest answers: (a) reversible — the down-migration exists and actually restores (auto-generated downs that drop a column do NOT restore its data — a down that loses data is not a rollback, label it); (b) roll-forward-only — irreversible by nature, so the plan is a fixing migration, and the deploy gate should know; (c) backup-gated — destructive step requires a named backup/snapshot beforehand. "It has a down file" without reading it is not an answer.
7. **Report.** Findings ranked **blocker** (data loss without a stated plan, traffic-blocking lock on a hot table, rollout/rollback contradiction) / **should-fix** / **note**, each with `file:line`, the failure scenario in one sentence (deploy does X → traffic sees Y), and the safe alternative. State the assumptions from step 1 that findings hang on. A green report on an additive, defaulted, indexed-concurrently migration is a valid outcome — two lines, not a performed checklist. Never edit or execute anything unprompted; ask per-finding whether to draft the fix.

## Examples

### Example 1: the innocent-looking rename

**User:** "Review this EF migration before I merge — just renames a column and adds an index."

**Claude:** Flags the rename as drop+add against live old code (blocker, expand-contract plan sketched across 3 releases), checks the index: `CreateIndex` on `Orders` — SQL Server without `ONLINE = ON`; asks/flags edition support, cites the line. Checks the down: `RenameColumn` back — actually reversible, noted. One assumption stated: `Orders` presumed hot.

### Example 2: honest green

**User:** "Is this migration safe? Adds a nullable `preferences` jsonb column and a partial index CONCURRENTLY."

**Claude:** Nullable add = metadata-only; `CONCURRENTLY` = non-blocking (notes it must run outside a transaction — verifies the tool's migration wrapper handles that, cites how); old code unaffected (column unreferenced by it), rollback trivial. Report: no findings, one note about the transaction wrapper. Done in four lines.

## Anti-patterns

- ❌ Reviewing the migration against an empty dev database mentally — every finding is judged against size, traffic, and the deploy overlap, or labeled with the assumption.
- ❌ Lock claims without the engine — `ADD COLUMN NOT NULL DEFAULT` is free on modern Postgres and was a rewrite on old versions; flagging the free case is severity inflation that erodes trust in the real findings.
- ❌ Accepting a rename or drop because "the code was updated in the same PR" — the whole problem is the minutes-to-hours when old code and new schema coexist.
- ❌ Trusting an auto-generated down-migration as a rollback without reading whether it restores data or just shape.
- ❌ Letting a million-row backfill ride inside the DDL transaction because the migration tool put it there.
- ❌ Executing the migration, `dotnet ef database update`, or ANY SQL "to check" — this skill reads and reports, full stop.
- ❌ Performing the full checklist on a pre-production empty schema — one line of N/A beats a page of theater.
- ✅ Engine-named lock findings, both-direction deploy-order trace, data-preserving rollback verdicts, assumptions stated, blockers with one-sentence failure scenarios.

## Notes

- Tool wrappers matter: some runners wrap every migration in a transaction (breaking `CREATE INDEX CONCURRENTLY`), some apply timeouts, some (SQL Server) do transactional DDL. Find the runner's config in the repo before asserting behavior — a claim about the wrapper you haven't opened is a hypothesis.
- Recommend `lock_timeout`/`statement_timeout` guards (Postgres) on DDL touching hot tables where the repo's runner supports it — a migration that fails fast beats one that queues behind a long transaction and blocks everything behind *it*.
- Apply `think-like-fable`: the risk lives in the destructive ops and the deploy overlap, so they get the effort; every lock/rollback claim is re-derived from the engine + the actual file; the report leads with the one migration that must not run as-is.
