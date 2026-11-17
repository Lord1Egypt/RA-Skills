# Bulk Load — Getting Millions of Rows In

Order of magnitude on ordinary hardware: single-row `INSERT` in autocommit is roughly a thousand rows per second, multi-row `INSERT` tens of thousands, `COPY` hundreds of thousands. If a load is slow, the first question is which of the three it is using — not which setting to change.

## The Loading Ladder

1. **`COPY`** — one command, binary or text protocol, no per-row parse. Always the target.
2. **Multi-row `INSERT`** (`VALUES (...), (...), ...` in batches of 500-1000) when the client cannot stream COPY, or when `ON CONFLICT` is required.
3. **Prepared single-row inserts inside one transaction** — still far behind, but an order of magnitude better than autocommit, because each commit is an fsync.
4. Never: single-row inserts in autocommit over a network. That benchmark measures round trips.

Most drivers expose COPY (`copy_from` in psycopg, `pgx.CopyFrom` in Go, `pg-copy-streams` in Node). Client-side `\copy` in psql covers the file case (psql guide).

## The Session Settings That Matter

```sql
SET maintenance_work_mem = '2GB';     -- index builds after the load
SET synchronous_commit = off;         -- per session; a crash loses this load, which you can rerun
SET statement_timeout = 0;            -- a load is not a runaway query
```

Session-scoped, not global. `synchronous_commit = off` is safe here specifically because the recovery action is "run the load again"; the bounded loss window is in the replication guide's table.

## Load Into a Table With No Indexes

For an initial load or a rebuild, the fastest correct sequence:

1. Create the table, **without** indexes and without foreign keys.
2. `COPY` the data in.
3. Create indexes (`maintenance_work_mem` raised, `max_parallel_maintenance_workers` raised).
4. Add foreign keys and CHECK constraints, `NOT VALID` then `VALIDATE` if the table is already live.
5. `VACUUM ANALYZE` — the planner has no statistics for the new data until then, and the visibility map is unset, so index-only scans will not work (SKILL.md Slow-Query Triage step 3).

Building an index once over the whole table beats maintaining it row by row by a wide margin: each index turns every inserted row into an extra page write plus WAL.

For an *incremental* load into a live table, do not drop indexes — dropping and rebuilding an index on a table serving queries trades a fast load for a slow hour.

## Unlogged and Its Exact Price

`CREATE UNLOGGED TABLE staging (...)` skips WAL entirely, roughly halving write cost. The price is precise:

- The table is **truncated** after a crash or unclean shutdown.
- It is **not replicated** — replicas see an empty table.
- `ALTER TABLE ... SET LOGGED` rewrites the whole table and writes all of it to WAL, so the saving is lost if you convert afterwards.

That makes it right for staging tables you re-load from a source of truth, and wrong for anything else.

## Upserts and Deduplication at Volume

```sql
COPY staging FROM ...;                         -- unlogged, no indexes
CREATE INDEX ON staging (id);
ANALYZE staging;

INSERT INTO target SELECT DISTINCT ON (id) * FROM staging ORDER BY id, updated_at DESC
ON CONFLICT (id) DO UPDATE SET col = EXCLUDED.col
WHERE target.updated_at < EXCLUDED.updated_at;   -- skip no-op updates
```

- `ON CONFLICT DO UPDATE` fails with "cannot affect row a second time" if the *same* statement contains two rows with the same conflict key — deduplicate in the source query (`DISTINCT ON`), not with a retry.
- The `WHERE` on the DO UPDATE clause matters at scale: without it, every unchanged row is still rewritten, producing dead tuples and index churn for nothing.
- Batch the merge in chunks (the backfill loop in the migrations guide) rather than one 50M-row statement.
- `MERGE` (PostgreSQL >=15) expresses multi-action merges, including DELETE. It does **not** have `ON CONFLICT`'s concurrency guarantee: under concurrent writers it can still raise a unique violation, so keep `ON CONFLICT` for the concurrent upsert path.

## During and After

- **Monitor the load, not just its end**: table size growth, `pg_stat_progress_copy` (PostgreSQL >=14) for rows processed, and replica lag — an unthrottled load is the classic cause of a lag spike (replication guide).
- **Autovacuum**: a large load creates work for it immediately, and the default scale factor means it may not start for a long time. `VACUUM (ANALYZE, FREEZE)` explicitly after the load turns a future anti-wraparound emergency into a scheduled minute (vacuum guide).
- **Disk**: a rebuild-style load needs room for the old copy, the new copy, and the WAL generated. Check free space against the sum, not against the table size.
- **Timing check**: if a COPY runs far below a hundred thousand rows per second on local storage, the bottleneck is usually triggers on the target table, foreign key checks, or an index you forgot to drop — in that order.

## Loading From Elsewhere

- Another Postgres: `pg_dump -Fd -j` plus `pg_restore -j`, or logical replication for a continuous feed (backup and replication guides).
- A CSV on the server that is too big for one transaction: split it and load in parallel sessions into a partitioned or unindexed table; COPY does not parallelize inside one statement.
- A remote database or file as a queryable table: `postgres_fdw` / `file_fdw` (extensions guide). Convenient, and much slower than a local COPY of an exported file — use them for occasional access, not for the nightly load.
