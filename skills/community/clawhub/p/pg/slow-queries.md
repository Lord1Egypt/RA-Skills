# Slow Queries — Reading the Plan and Finding the Lie

The triage order lives in SKILL.md (Slow-Query Triage). This file is what to do once you have the plan in front of you.

## The Options That Earn Their Keep

`EXPLAIN (ANALYZE, BUFFERS)` is the floor. Add:

- `VERBOSE` — output columns per node; finds the overwide `SELECT *` feeding a sort.
- `SETTINGS` — non-default planner GUCs in effect (PostgreSQL >=12). The fastest way to catch a session with `enable_seqscan = off` left over.
- `WAL` — WAL bytes written; on `EXPLAIN ANALYZE INSERT/UPDATE` this is where index write amplification becomes visible.
- `FORMAT JSON` — for tooling and diffing two plans mechanically.
- `SERIALIZE` (PostgreSQL >=17) — includes the cost of forming and sending the result rows, which plain ANALYZE discards. Wide `text`/`jsonb` results are often slower in the client than in the plan.

`EXPLAIN ANALYZE` **executes** the statement. On a write, wrap it: `BEGIN; EXPLAIN (ANALYZE) UPDATE ...; ROLLBACK;`.

## Reading a Plan in Four Passes

1. **Bottom-up, innermost first** — the leaves are the scans, the root is the last thing to finish. Time is inclusive of children.
2. **`rows=` estimated vs `actual rows=`** at every node. The first node where they diverge more than 10x is the origin; everything above it inherited a bad decision.
3. **`loops=`** — actual time in a plan node is *per loop*. A node showing `actual time=0.05..0.08 rows=1 loops=240000` cost 19 seconds, not 0.08ms. This is the single most misread number in Postgres.
4. **Buffers** — `shared hit` (cache), `read` (disk or OS cache), `dirtied`/`written` (this SELECT is doing write work: hint bits or spilling). `temp read/written` at any node means it spilled to disk.

## Node Types and What They Actually Mean

| Node | Says | Act when |
|---|---|---|
| Seq Scan | Full heap read | It is fine below ~5-15% selectivity (SKILL.md triage step 5); above that, look for a missing or unusable predicate |
| Index Scan | Index then heap fetch per row | Rows returned are high → the heap fetches dominate; consider `INCLUDE` for index-only |
| Index Only Scan | No heap fetch — check `Heap Fetches:` | Heap Fetches large means the visibility map is stale: vacuum the table |
| Bitmap Heap Scan | Many matches, heap read in physical order | `Recheck Cond` plus `lossy=N` blocks means `work_mem` was too small for exact bitmaps |
| Nested Loop | Inner side run once per outer row | Outer rows badly underestimated → this is how a 3ms plan becomes 3 minutes |
| Hash Join | Builds a hash of the smaller side | `Batches: > 1` means the hash spilled; raise `work_mem` for this query |
| Merge Join | Both sides sorted | Cheap when both sides arrive pre-sorted by index; expensive if it forces two sorts |
| Sort | Explicit ordering | `Sort Method: external merge Disk: NkB` = spilled; `quicksort Memory` = fine |
| Incremental Sort | Partially sorted input (>=13) | Signals an index that covers a prefix of your ORDER BY — extend it |
| Memoize | Caches inner results of a nested loop (>=14) | High `Hits` is good; near-zero hits with high memory means the planner guessed wrong |
| Gather / Gather Merge | Parallel workers | `Workers Launched` < `Workers Planned` means the pool was exhausted |
| Materialize / CTE Scan | Result buffered | On <12 a CTE Scan is the optimization fence (SKILL.md Query Patterns) |
| Anything else | — | Compare the node's actual time against its children; the difference is the work it did itself |

## The Four Root Causes of a Bad Plan

**1. Stale or insufficient statistics.** `ANALYZE tbl` first. Then `SET STATISTICS 1000` on the skewed column. For correlated columns (`city`/`country`, `status`/`type`) the planner multiplies independent probabilities and underestimates catastrophically: `CREATE STATISTICS s (dependencies, ndistinct) ON city, country FROM addresses; ANALYZE addresses;`.

**2. Non-sargable predicates.** The index is unusable when the column is wrapped:
- `WHERE date(created_at) = '2026-07-01'` → `WHERE created_at >= '2026-07-01' AND created_at < '2026-07-02'`
- `WHERE amount::text LIKE '1%'`, `WHERE col + 0 = 5`, `WHERE upper(name) = 'X'` without a matching expression index
- Implicit casts across types: a `bigint` column compared to a `numeric` parameter, or a `text` column compared to a `citext`/`varchar` of a different collation — the plan shows the cast and the index disappears

**3. Parameter-sensitive plans.** With protocol-level prepared statements, PostgreSQL builds a custom plan for the first five executions, then compares against a generic plan and may lock onto it (`plan_cache_mode = force_custom_plan` disables the switch). Symptom: the same statement is fast from psql and slow from the app, or fast for four hours then slow forever. On skewed data (one tenant with 90% of rows) the generic plan is a coin flip.

**4. Cost model versus hardware.** Defaults describe a spinning disk: `random_page_cost = 4.0`, `effective_cache_size = 4GB`. On NVMe with 64GB RAM the planner is being told random I/O is four times sequential and that almost nothing is cached. Correct both (values in SKILL.md triage step 5 and the tuning guide) before adding indexes to compensate.

## LIMIT: the Trap of the Cheap-Looking Plan

`ORDER BY x LIMIT 10` makes the planner assume it can stop early, so it picks an index scan on `x` and walks it until 10 rows pass the WHERE clause. If the matching rows live at the far end, it walks the whole index. Symptom: adding `LIMIT` makes a query 100x *slower*. Fix: a composite index that satisfies both the filter and the ordering, so the first 10 index entries are already the answer.

## Parallelism

- Gated by `max_parallel_workers_per_gather` (default 2), the table's size, and `min_parallel_table_scan_size` (8MB). Small tables never go parallel no matter the setting.
- Parallel workers are capped globally by `max_parallel_workers` and `max_worker_processes`; under concurrency you get fewer than planned, and a plan tuned with 4 workers regresses at peak.
- CTEs marked `MATERIALIZED`, `FOR UPDATE`, and functions not marked `PARALLEL SAFE` disable parallelism for the whole query. A single `VOLATILE` user function in the SELECT list is a common accidental cause.
- `work_mem` is per worker as well as per node — parallelism multiplies the memory formula in SKILL.md rule 5.

## JIT: the Silent Regression

`jit = on` triggers when the *estimated* total cost exceeds `jit_above_cost` (default 100000). On a misestimated OLTP query, compilation costs 50-200ms and buys nothing — the plan shows `JIT: Functions: N, Timing: ... Total: X ms`. If JIT timing rivals execution time, set `jit = off` for that workload; keep it for genuine analytic scans.

## Confirming the Fix

- Re-run with `EXPLAIN (ANALYZE, BUFFERS)` and compare **buffers**, not wall time — wall time moves with cache state, buffers move with the plan.
- Run it twice: the first run pays for cold cache; the second is what production sees at steady state.
- Check `pg_stat_statements` for the statement's `total_exec_time` share the next day. A query that is 10x faster and called 10x more often has not helped the server.
- Hypothetical indexes (`hypopg`) let you test whether an index would even be chosen before paying to build it.
