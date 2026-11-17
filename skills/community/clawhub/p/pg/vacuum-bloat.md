# Vacuum and Bloat — Why the Table Grows While the Rows Do Not

MVCC keeps an old version of every updated or deleted row until no transaction can still see it. Vacuum marks that space reusable. Bloat is the gap between what vacuum could reclaim and what it did.

## First Question, Always: What Is Holding the Horizon?

Vacuum cannot remove a tuple newer than the oldest thing that might still need it. Four candidates, checked in this order:

```sql
-- 1. Oldest running transaction
SELECT pid, state, now() - xact_start AS age, left(query, 80)
FROM pg_stat_activity WHERE xact_start IS NOT NULL ORDER BY xact_start LIMIT 5;

-- 2. Replication slots (a dead subscriber blocks vacuum AND retains WAL)
SELECT slot_name, active, restart_lsn, xmin, catalog_xmin FROM pg_replication_slots;

-- 3. Standbys with hot_standby_feedback on
SELECT application_name, backend_xmin FROM pg_stat_replication;

-- 4. Prepared transactions nobody committed (two-phase commit leftovers)
SELECT gid, prepared, owner FROM pg_prepared_xacts;
```

One forgotten `BEGIN`, one orphaned slot, or one prepared transaction bloats *every table in the database*, not just the one it touched. Fixing autovacuum settings while any of these is open changes nothing.

## Autovacuum Thresholds, and Why the Default Fails Big Tables

Vacuum triggers when dead tuples exceed:

```
autovacuum_vacuum_threshold (50) + autovacuum_vacuum_scale_factor (0.2) × reltuples
```

On a 100M-row table that is 20M dead tuples before the first pass — by then the table has grown tens of gigabytes. Analyze uses the same shape with `autovacuum_analyze_scale_factor` (0.1).

Per-table fix, the highest-value knob in this file:

```sql
ALTER TABLE big SET (autovacuum_vacuum_scale_factor = 0.01,    -- 1M dead tuples
                     autovacuum_analyze_scale_factor = 0.005,
                     autovacuum_vacuum_cost_delay = 0);         -- run at full speed
```

Other defaults worth knowing: `autovacuum_naptime` 1min, `autovacuum_max_workers` 3 (workers share one cost budget, so raising it does not multiply throughput), `autovacuum_vacuum_cost_delay` 2ms since PostgreSQL 12 (20ms before — an upgrade from 11 makes autovacuum roughly ten times faster overnight), `autovacuum_vacuum_cost_limit` 200.

Signals that autovacuum is losing: `pg_stat_user_tables.n_dead_tup` climbing across days, `last_autovacuum` hours or days old on a hot table, or `autovacuum` workers permanently at `max_workers`.

## Measuring Bloat Honestly

- Estimation queries (the widely copied `pgstattuple`-free SQL) are approximations and routinely report 30-40% on healthy tables. Use them to rank, never to decide.
- Exact: `CREATE EXTENSION pgstattuple;` then `SELECT * FROM pgstattuple('orders')` — `dead_tuple_percent` and `free_percent`. It reads the whole table, so run it off-peak. `pgstattuple_approx` samples and is much cheaper.
- Index bloat: `SELECT * FROM pgstatindex('orders_pkey')` — `avg_leaf_density` under ~60% is a real rebuild candidate.
- A table that is 20% free space is not bloated; it is a table with room to work. Act above roughly 40-50% dead space on a table whose size is causing real I/O.

## Reclaiming Space

| Tool | Lock | Result |
|---|---|---|
| `VACUUM` | SHARE UPDATE EXCLUSIVE | Marks space reusable; file rarely shrinks |
| `VACUUM (VERBOSE, ANALYZE)` | Same | Same, plus fresh statistics and a report of what blocked removal |
| Truncate of trailing empty pages | Brief ACCESS EXCLUSIVE at the end of vacuum | Shrinks the file only when the free space is at the end |
| `pg_repack` | Brief ACCESS EXCLUSIVE at swap time | Full rewrite online; needs disk for a second copy |
| `VACUUM FULL` / `CLUSTER` | ACCESS EXCLUSIVE for the whole rewrite | Smallest result, full outage on that table |
| Partition drop | ACCESS EXCLUSIVE on the parent, instant | The only zero-cost delete of old data |

Reclaimed-but-not-returned space is the normal steady state: a table that cycles between 10GB and 12GB is healthy. Chasing the file size back to 10GB with `VACUUM FULL` every week just pays the rewrite repeatedly.

## Freezing and Wraparound

- Transaction IDs are 32-bit and wrap. Vacuum "freezes" old tuples so they stay visible after the wrap.
- `autovacuum_freeze_max_age` (default 200M) forces an anti-wraparound autovacuum even on tables nothing writes to, and even when autovacuum is disabled. It does not yield to conflicting locks — this is the vacuum that appears to hang your DDL for hours.
- `vacuum_failsafe_age` (default 1.6B, PostgreSQL >=14) makes vacuum drop cost-based throttling and skip index cleanup to catch up.
- At roughly 1M transactions of headroom the cluster refuses new write transactions with "database is not accepting commands to avoid wraparound data loss". The fix at that point is vacuuming the offending tables, not single-user mode — identify them with:

```sql
SELECT relname, age(relfrozenxid) AS xid_age, pg_size_pretty(pg_total_relation_size(oid))
FROM pg_class WHERE relkind IN ('r','m','t') ORDER BY age(relfrozenxid) DESC LIMIT 10;
```

- Monitor `age(datfrozenxid)` per database and alert well before `autovacuum_freeze_max_age`, not at the ceiling.
- Bulk-loaded, never-updated tables still need freezing. `VACUUM (FREEZE)` after a big load turns a future emergency into a scheduled minute. PostgreSQL >=14 freezes whole pages during a `COPY` into an empty table when the transaction is the only writer, which removes much of this for fresh loads.

## Update Patterns That Cause the Bloat

- Updating any indexed column blocks HOT and writes to every index (SKILL.md Indexing Essentials). A `last_seen_at` column indexed "just in case" turns one row update into six index writes.
- `fillfactor = 90` on update-heavy tables leaves in-page room so HOT can reuse it. It costs 10% more space and can eliminate most index churn.
- Queue tables are worst-case: high insert, high delete, tiny live set. Give them aggressive per-table autovacuum settings; a queue table with default settings routinely grows to gigabytes while holding a hundred rows.
- Mass `DELETE` followed by nothing leaves the space allocated to that table forever. Either follow with `pg_repack`, or design the deletion as a partition drop.
- `VACUUM ANALYZE` after any bulk load or mass delete: until then the planner is working from pre-load statistics (SKILL.md Slow-Query Triage step 3).

## Long Transactions and Isolation

- Default READ COMMITTED takes a new snapshot per statement, so a multi-statement report can see inconsistent totals. REPEATABLE READ gives one snapshot for the transaction — and holds the vacuum horizon for its whole life.
- SERIALIZABLE needs a retry loop on 40001; without the loop it is strictly worse than REPEATABLE READ.
- Application connection pools that `BEGIN` on checkout and hold it while the app thinks are the number one source of accidental long transactions. Pair `idle_in_transaction_session_timeout` (SKILL.md Core Rules 4) with a pool that starts transactions lazily.
