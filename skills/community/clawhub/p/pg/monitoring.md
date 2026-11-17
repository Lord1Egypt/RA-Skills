# Monitoring — What to Watch, What to Alert On

## The Catalog Map

| View | Answers |
|---|---|
| `pg_stat_activity` | Who is connected, what they run, what they wait on, how old their transaction is |
| `pg_stat_statements` | Which statements cost the most time in aggregate (extension; needs `shared_preload_libraries`) |
| `pg_stat_user_tables` | Sequential vs index scans, dead tuples, last (auto)vacuum and analyze |
| `pg_stat_user_indexes` | Index usage per node |
| `pg_stat_database` | Commits/rollbacks, deadlocks, temp files, blocks hit/read, checksum failures |
| `pg_stat_io` | Read/write/extend per backend type and context (PostgreSQL >=16) — where the I/O actually goes |
| `pg_stat_checkpointer` / `pg_stat_bgwriter` | Checkpoint counts and timing (split in PostgreSQL 17) |
| `pg_stat_replication` / `pg_stat_wal_receiver` | Replication lag from each side |
| `pg_stat_archiver` | WAL archiving success and, more importantly, failures |
| `pg_locks` | Current lock holders and waiters |
| `pg_settings` | Effective value, source file, and whether a restart is needed |
| Anything else | `\dv pg_stat*` in psql lists every statistics view on your version |

Counters are cumulative since the last reset (`stats_reset` column). Every meaningful metric is a **delta over an interval**, not the raw number.

## The Alert Set That Earns Its Pager

| Alert | Threshold | Why this one |
|---|---|---|
| Disk free on the data and WAL filesystems | Warn 25%, page 15% | A full `pg_wal` stops the cluster; recovery from full is much harder than from 15% |
| WAL archiving failing | `pg_stat_archiver.last_failed_time` recent | Silent failure means no PITR and a growing `pg_wal` |
| Replication lag in **bytes** | Workload-specific; alert on trend | The time-based metric false-alarms on an idle primary (see the replication guide) |
| Oldest transaction age | > 15min | One `BEGIN` blocks vacuum database-wide; anything here outlived the 5min idle-in-transaction timeout, so it is active or exempt |
| `age(datfrozenxid)` | > 75% of `autovacuum_freeze_max_age` | Wraparound is a hard stop, and the fix is slow |
| Connection utilization | > 80% of `max_connections` | The last 20% goes fast under a retry storm |
| Deadlocks per minute | Any sustained rate | Each one is an aborted user transaction |
| Backup age and last successful restore drill | > expected interval | The only backup metric that means anything |
| Anything else | Graph it, do not page on it | Pages that nobody can act on train people to ignore pages |

## Reading pg_stat_statements

```sql
SELECT calls, round(total_exec_time::numeric, 0) AS total_ms,
       round(mean_exec_time::numeric, 2) AS mean_ms, rows,
       round(100 * shared_blks_hit / nullif(shared_blks_hit + shared_blks_read, 0), 1) AS hit_pct,
       left(query, 90)
FROM pg_stat_statements ORDER BY total_exec_time DESC LIMIT 20;
```

- Order by `total_exec_time`, not `mean_exec_time`: the query worth fixing is the one consuming the most server time, which is usually fast and frequent (SKILL.md Slow-Query Triage step 1).
- `pg_stat_statements.max` (default 5000) caps tracked statements; overflow silently evicts the least used. Applications generating unparameterized SQL blow through it and make the view useless — that alone is a reason to parameterize.
- `pg_stat_statements_reset()` before a load test, read after. Comparing two absolute snapshots by hand is how people misattribute regressions.
- `track_io_timing = on` adds `blk_read_time`/`blk_write_time` and separates I/O from CPU. Measure the clock overhead first with `pg_test_timing`; on modern hardware it is negligible, on some virtualized instances it is not.

## Signals and What They Actually Mean

- **Cache hit ratio.** `blks_hit / (blks_hit + blks_read)` from `pg_stat_database`. The "99% is healthy" rule is nearly meaningless: it is cumulative since reset and dominated by trivial index lookups. A 99.9% ratio with one report doing 40GB of reads per hour is a problem the ratio cannot show. Use per-statement hit percentage instead.
- **`temp_files` / `temp_bytes` climbing** — queries are spilling sorts and hashes to disk: `work_mem` too small for those specific queries. Find them with `log_temp_files = 0` (logs every spill with its size).
- **`n_dead_tup` growing across days** — autovacuum is losing (vacuum guide).
- **`seq_scan` high on a large table** — either a missing index or a plan that legitimately scans; check with a plan before adding an index.
- **`xact_rollback` rising** — application errors or serialization failures, not a database problem per se, but a leading indicator of retry storms.
- **`checksum_failures` non-zero** — storage is corrupting data. Stop and treat it as an incident.
- **`wait_event` distribution** sampled from `pg_stat_activity` once a second is a poor man's profiler and remarkably effective: `Lock` dominant means contention, `IO` dominant means storage, `LWLock` dominant means internal contention (often `WALWrite` or buffer mapping).

## Logging Configuration Worth Having On

```
log_min_duration_statement = 1000   # every statement over 1s, with parameters
log_lock_waits = on                 # any wait longer than deadlock_timeout (1s)
log_temp_files = 0                  # every spill to disk
log_autovacuum_min_duration = 0     # every autovacuum run and what it could not remove
log_checkpoints = on                # default since 15
log_connections = on                # audit trail and connection-storm forensics
log_line_prefix = '%m [%p] %q%u@%d app=%a '
```

- `log_min_duration_statement = 0` logs everything and will itself become the bottleneck on a busy server. Use `auto_explain` with `auto_explain.log_min_duration` for plans of slow statements instead; `auto_explain.log_analyze = on` gives real row counts at real per-query cost (measure it before enabling in production).
- `log_line_prefix` without user, database and application name makes every log line ambiguous during the one incident where it matters.

## Baselines Beat Thresholds

Record, on a normal day: peak connections, peak TPS (`xact_commit` delta), the top five statements by total time, replication lag, table sizes, and index sizes. During an incident the question is never "is 400 connections bad" but "was it 90 yesterday". A weekly snapshot of those numbers into a table costs nothing and answers it in seconds.
