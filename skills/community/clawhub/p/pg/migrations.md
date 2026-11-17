# Migrations — Changing a Schema Nobody Can Take Offline

Per-statement lock recipes are in SKILL.md (Safe DDL on Busy Tables). This file is sequencing: how a change lands across several deploys without an outage.

## The Rule That Generates the Others

Old code and new code run at the same time during every deploy. Therefore **every migration must be compatible with the code version before it and after it**. That forces expand/contract:

1. **Expand** — add the new thing, nullable and unconstrained. Old code ignores it.
2. **Dual-write** — new code writes both old and new. Deploy. Old code still works.
3. **Backfill** — batched, resumable, off-peak.
4. **Switch reads** — new code reads the new thing. Deploy. Verify.
5. **Contract** — drop the old thing, in a separate migration, after a bake period long enough to roll back the code (a day is typical; a week if rollback is manual).

A "rename a column" migration is these five steps, not one. `ALTER TABLE ... RENAME COLUMN` is instant and metadata-only, and it breaks every running instance of the old code the moment it commits.

## The Lock Queue, Concretely

```
SET lock_timeout = '2s';   -- lock_timeout_default
ALTER TABLE orders ADD COLUMN note text;
```

Without the timeout: your ALTER waits behind a 40-minute analytics SELECT for the ACCESS EXCLUSIVE lock, and every query arriving after it — including trivial primary-key lookups — queues behind *your* pending lock. The table is effectively down while nothing appears to be running.

Retry pattern: `lock_timeout` fires with SQLSTATE 55P03; sleep a few seconds and retry, up to N times. Never solve it by raising the timeout. On very hot tables, retry in a loop during a low-traffic window and cancel the blocker deliberately after identifying it.

## Backfill Loop

```sql
-- resumable; one transaction per batch; no long-lived snapshot
DO $$
DECLARE last_id bigint := 0; n int;
BEGIN
  LOOP
    WITH batch AS (
      SELECT id FROM users WHERE tz IS NULL AND id > last_id ORDER BY id LIMIT 5000
    ), upd AS (
      UPDATE users u SET tz = 'UTC' FROM batch b WHERE u.id = b.id RETURNING u.id
    )
    SELECT count(*), coalesce(max(id), last_id) INTO n, last_id FROM upd;
    EXIT WHEN n = 0;
    COMMIT;                 -- transaction control inside DO/procedures: PostgreSQL >=11
    PERFORM pg_sleep(0.1);  -- give autovacuum and replicas air
  END LOOP;
END $$;
```

Run it from a client that is not already inside a transaction — `COMMIT` inside `DO` fails if the caller opened one (psql with `\set AUTOCOMMIT off`, or a framework that wraps migrations).

- Batch size 1k-50k rows (SKILL.md Core Rules 7). Larger batches mean longer locks and bigger WAL bursts; smaller batches mean more round trips. Start at 5000 and measure.
- Sleep between batches on a replicated cluster: an unthrottled backfill is the classic cause of replica lag spikes.
- Every batch creates dead tuples equal to the rows touched. Watch table size during the backfill; if autovacuum cannot keep up, lower its scale factor for that table for the duration.
- A backfill that cannot resume from a key is a backfill you will restart from zero at 3am.

## Operation Cost Table

| Operation | Lock | Cost |
|---|---|---|
| `ADD COLUMN` nullable, no default | ACCESS EXCLUSIVE, instant | Metadata only |
| `ADD COLUMN ... DEFAULT <constant>` | ACCESS EXCLUSIVE, instant (>=11) | Metadata only; volatile default rewrites the table |
| `DROP COLUMN` | ACCESS EXCLUSIVE, instant | Metadata only; space is reclaimed on later rewrites |
| `RENAME COLUMN`/`TABLE` | ACCESS EXCLUSIVE, instant | Metadata only — but breaks running code |
| `ALTER COLUMN TYPE varchar(n)→text`, widening `varchar(n)` | ACCESS EXCLUSIVE, instant (>=9.2) | Metadata only |
| `ALTER COLUMN TYPE int→bigint` | ACCESS EXCLUSIVE, full rewrite | Table plus every index rebuilt; use expand/contract |
| `SET NOT NULL` | ACCESS EXCLUSIVE, full scan | Instant with a validated CHECK first (>=12) |
| `ADD CONSTRAINT ... NOT VALID` | ACCESS EXCLUSIVE, instant | Then `VALIDATE` under SHARE UPDATE EXCLUSIVE |
| `ADD FOREIGN KEY` | ACCESS EXCLUSIVE on both tables | Split: `NOT VALID` then `VALIDATE` |
| `CREATE INDEX` | SHARE (blocks writes) | Use CONCURRENTLY |
| `CREATE INDEX CONCURRENTLY` | SHARE UPDATE EXCLUSIVE | Two passes, waits for old transactions, no transaction block |
| `ADD PRIMARY KEY` | ACCESS EXCLUSIVE | Build unique index CONCURRENTLY first, then `ADD CONSTRAINT ... USING INDEX` |
| `SET DEFAULT` / `DROP DEFAULT` | ACCESS EXCLUSIVE, instant | Metadata only |
| `CLUSTER`, `VACUUM FULL` | ACCESS EXCLUSIVE, full rewrite | Outage; use pg_repack |
| Anything not listed | Assume a rewrite | Test on a copy of production-scale data and time it |

## int → bigint on a Live Primary Key

The one migration that eats a weekend if improvised:

1. `ADD COLUMN id_new bigint` (nullable, no default).
2. Trigger on insert/update to fill `id_new` from `id`.
3. Backfill in batches, oldest first.
4. `CREATE UNIQUE INDEX CONCURRENTLY` on `id_new`; repeat for every FK column in every child table (steps 1-4 apply there too).
5. In one short transaction with `lock_timeout`: drop the old FK constraints, rename columns, add the new primary key `USING INDEX`, recreate FKs as `NOT VALID`.
6. `VALIDATE` the FKs afterwards, and fix the sequence: `ALTER SEQUENCE ... AS bigint; SELECT setval(...)`.

## Migration Tooling, Whatever the Framework

- One migration file = one logical change, forward-only in production. "Down" migrations are a development convenience; the production rollback path is a new forward migration plus a restore plan.
- Migrations that must not run in a transaction (`CREATE INDEX CONCURRENTLY`, `ALTER TYPE ... ADD VALUE` before 12) need the framework's explicit non-transactional flag. Frameworks that wrap everything silently produce "cannot run inside a transaction block" at deploy time.
- Set `lock_timeout` and `statement_timeout` *inside* the migration session, not globally — the migration runner's defaults are usually unlimited.
- Test every migration against a restored copy of production, not against an empty dev database. The only number that matters is how long it holds a lock on real data volume.
- Advisory lock around the runner (`pg_advisory_lock` on a fixed key) prevents two deploy jobs from migrating simultaneously; every mature framework does this, and hand-rolled runners usually do not.

## Rollback Reality

- Additive changes (new nullable column, new index, new table) roll back by doing nothing.
- Destructive changes do not roll back — a dropped column is gone, and a restore loses every write since the dump. This is why contract steps ship separately and late.
- Before any destructive step: confirm the column or table has had zero reads for the bake period (`pg_stat_user_tables.seq_scan`/`idx_scan` for tables; for columns, application logs or a temporary rule/trigger).
- Keep the migration and the code deploy independent: if they must ship together, you have a coupling that will fail at the worst moment.
