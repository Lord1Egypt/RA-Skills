# Server Tuning — postgresql.conf That Matters

Change one thing at a time and measure against a plan or a `pg_stat_statements` delta. Most "tuned" configurations copied from a blog are worse than the defaults plus the six settings below.

Apply with `ALTER SYSTEM SET ... ;` then `SELECT pg_reload_conf()` for reload-only settings; `pg_settings.context` tells you which need a restart (`postmaster`) versus a reload (`sighup`) versus nothing (`user`). On managed platforms `ALTER SYSTEM` is usually blocked — the provider's parameter group is the equivalent, and that is what the `deployment` variable in SKILL.md Configuration selects.

## The Six That Change Everything

| Setting | Default | Set to | Why |
|---|---|---|---|
| `shared_buffers` | 128MB | ~25% of RAM | Postgres's own cache; the OS page cache holds the rest, so more is not linearly better |
| `effective_cache_size` | 4GB | 50-75% of RAM | Pure planner hint about what the OS is likely caching; too low and it refuses index scans |
| `work_mem` | 4MB | 4-16MB globally, raised per session | Per node, not per query — the formula in SKILL.md Core Rules 5 |
| `maintenance_work_mem` | 64MB | 1-2GB | Index builds, `VACUUM`, restores; the difference between a 40-minute and a 6-minute index build |
| `random_page_cost` | 4.0 | 1.1 on SSD/NVMe | The default describes a spinning disk and makes the planner avoid good indexes |
| `max_wal_size` | 1GB | 4-16GB on write-heavy servers | Too small forces requested checkpoints; see the checkpoint section |

`effective_io_concurrency` (default 1) governs prefetch depth for bitmap heap scans: raise it to 100-200 on NVMe, leave it low on network storage where queue depth is not free.

## Checkpoints and WAL

- A checkpoint flushes dirty buffers to disk. `checkpoint_timeout` (default 5min) and `max_wal_size` race: whichever trips first starts one.
- The diagnostic: `checkpoints_req` versus `checkpoints_timed` in `pg_stat_checkpointer` (PostgreSQL >=17; `pg_stat_bgwriter` before that). Requested checkpoints dominating means `max_wal_size` is too small, and every one of them is an I/O spike plus full-page writes for every touched page afterwards.
- `checkpoint_completion_target` is 0.9 since PostgreSQL 14 — spread the writes; there is no reason to lower it.
- `log_checkpoints` is on by default since PostgreSQL 15. Read those lines: `write=...s sync=...s` tells you whether flushing is smooth or a cliff.
- `wal_compression = on` trades CPU for smaller WAL; it pays whenever WAL shipping or archiving is a bottleneck, especially right after checkpoints when full-page images dominate.
- `synchronous_commit = off` is the single biggest write-throughput win available (batch loads, telemetry) and its cost is bounded: a crash can lose the last fraction of a second of committed transactions, never consistency (table in the replication guide).

## Autovacuum

Defaults are per-table budgets set for a 2010 server. Global changes worth making on a busy database:

```
autovacuum_max_workers = 5          # more tables progressing in parallel
autovacuum_vacuum_cost_delay = 2ms  # the default since 12; verify it, older configs carry 20ms
autovacuum_naptime = 30s            # for very churny workloads
```

Then set per-table scale factors on the biggest tables rather than lowering the global one (procedure and thresholds in the vacuum guide). A global `autovacuum_vacuum_scale_factor = 0.01` makes autovacuum thrash small tables for no benefit.

## Parallelism

- `max_worker_processes` (8) is the pool. `max_parallel_workers` (8) is what parallel queries may take from it, and `max_parallel_workers_per_gather` (2) is the per-query cap.
- Raise `per_gather` to 4 for analytics, leave it at 2 for OLTP: parallelism costs a fork and a shared-memory handshake per worker, which a 5ms query cannot amortize.
- `max_parallel_maintenance_workers` (2) speeds up index builds — worth raising temporarily during a migration.
- Under concurrency you get fewer workers than planned, so a plan validated on an idle server regresses at peak (see the parallelism notes in the slow-query guide).

## Planner Knobs, and Restraint

- `default_statistics_target` (100) globally, raised per column with `SET STATISTICS` where the data is skewed. Raising it globally to 1000 makes every `ANALYZE` and every planning cycle more expensive for a benefit that lives in three columns.
- `cpu_tuple_cost` (0.01) is a plausible increase to 0.03 on modern hardware where I/O is cheap, but only after `random_page_cost`.
- `enable_seqscan = off` and friends are **debugging tools**, not configuration. Setting them in production hides the misestimate that is the real bug (SKILL.md Core Rules 1). Use them in a session to prove which plan you wanted, then fix statistics or indexes.
- `jit` costs 50-200ms of compilation on plans that only *look* expensive; turn it off for OLTP workloads that see it firing.

## Memory Safety on Linux

- Postgres never enforces a total memory limit: `work_mem` is per node and unbounded in aggregate. The OOM killer choosing the postmaster kills the entire cluster.
- `vm.overcommit_memory = 2` with a sane `vm.overcommit_ratio` makes allocations fail (one query errors) instead of the kernel killing a process at random.
- Protect the postmaster: `OOMScoreAdjust=-900` in the systemd unit.
- Huge pages (`huge_pages = try`, plus `vm.nr_hugepages` sized for `shared_buffers`) reduce page-table overhead measurably on servers with large `shared_buffers`.
- Cgroup memory limits (containers) apply to the whole cluster, so a single query's `work_mem` explosion kills every connection, not one.

## Connections and Timeouts

`max_connections` sizing, pooling, and the three per-role timeouts belong to the connections guide; the only server-side note here is that `max_connections` is a `postmaster` setting — changing it costs a restart, which is one more reason to pool instead of raise.

## A Sane Starting Point

For a dedicated 32GB, 8-core NVMe server: `shared_buffers = 8GB`, `effective_cache_size = 24GB`, `work_mem = 16MB`, `maintenance_work_mem = 2GB`, `max_wal_size = 8GB`, `random_page_cost = 1.1`, `effective_io_concurrency = 200`, `max_parallel_workers_per_gather = 2` (4 for analytics), autovacuum tuned per table. Everything else: default until a measurement says otherwise.
