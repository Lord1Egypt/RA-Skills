# Indexing — Choosing the Structure, Then Paying for It

Composite ordering, partial, expression and covering indexes are in SKILL.md (Indexing Essentials). This file is index *type* selection, build mechanics, and maintenance.

## Choosing the Index Type

| Access pattern | Index | Notes |
|---|---|---|
| `=`, `<`, `>`, `BETWEEN`, `ORDER BY`, `LIKE 'prefix%'` | B-tree | The default and the only one that serves ordering; `LIKE 'x%'` needs `text_pattern_ops` on a non-C collation |
| Array containment, jsonb `@>`, full-text `@@`, trigram | GIN | Many keys per row; fast reads, expensive writes |
| Range overlap (`&&`), geometry, nearest-neighbour `ORDER BY x <-> y`, exclusion constraints | GiST | Lossy: always followed by a recheck |
| Huge, naturally ordered table (append-only by time) | BRIN | Stores min/max per 128-page range (`pages_per_range`); index of a 1TB table measured in megabytes |
| Equality only, on a wide value | Hash | Crash-safe and replicated since PostgreSQL >=10; smaller than B-tree for long keys, but no ordering, no uniqueness, no multi-column |
| Non-balanced, prefix-heavy data (text, IP, quadtree) | SP-GiST | Niche; benchmark before adopting |
| Anything else | B-tree | Start here; switch only when the plan shows the B-tree cannot serve the predicate |

**BRIN's precondition is physical correlation.** Check it: `SELECT correlation FROM pg_stats WHERE tablename='events' AND attname='created_at';` — above ~0.9 BRIN works, below ~0.7 it degenerates into a full scan with extra steps. Random inserts, heavy updates, or a `pg_repack` reorder can destroy correlation overnight.

**GIN write cost is real.** Each inserted row touches one entry per token, not one per row. `fastupdate = on` (default) buffers into a pending list flushed by autovacuum or at `gin_pending_list_limit` (4MB) — this makes a periodic query pay the flush. For latency-sensitive reads, `ALTER INDEX ... SET (fastupdate = off)` and accept slower writes.

## Multicolumn, Or Several Single-Column?

- Postgres can combine two separate indexes with a **BitmapAnd**, so two single-column indexes are not useless — they are just slower than one composite that matches the predicate, and they cost two write paths.
- Rule of thumb: if a pair of columns appears together in the WHERE clause of a hot query, one composite. If they appear independently in different queries, separate indexes.
- A composite `(a, b, c)` also serves `(a)` and `(a, b)` — do not create those separately. It does **not** serve `(b)` or `(c)` (PostgreSQL >=18 adds B-tree skip scan for such cases, but it depends on `a` having few distinct values; do not design around it).
- `btree_gin` / `btree_gist` let you mix scalar equality into a GIN/GiST index — the standard way to build `(tenant_id, tsvector)` or an exclusion constraint combining `room_id =` with `during &&`.

## Building Without Downtime

- `CREATE INDEX CONCURRENTLY` does two table passes and waits for every transaction older than each pass. One long-running transaction stalls the build indefinitely — check `pg_stat_activity` for old `xact_start` before starting.
- It cannot run inside a transaction block, so most migration frameworks need an explicit "no transaction" escape hatch for that migration.
- Failure leaves an INVALID index that still costs writes: `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` → drop it (`DROP INDEX CONCURRENTLY`) before retrying.
- Build speed is bound by `maintenance_work_mem` (default 64MB — raise to 1-2GB for the session) and `max_parallel_maintenance_workers` (default 2).
- Unique constraint online: build `CREATE UNIQUE INDEX CONCURRENTLY`, then `ALTER TABLE ... ADD CONSTRAINT ... UNIQUE USING INDEX <name>` — the ALTER is instant because the index already exists.

## Bloat and Rebuilds

- B-tree indexes bloat faster than their tables under update-heavy load: every non-HOT update adds an index entry, and deleted entries are only reclaimed when the whole page empties.
- Measure before rebuilding: `pgstattuple_approx` on the table, `pgstatindex(index)` for `avg_leaf_density` — below ~60% is a real candidate. Estimation queries copied from blogs report bloat on healthy indexes routinely.
- `REINDEX INDEX CONCURRENTLY` (PostgreSQL >=12) rebuilds without blocking writes and swaps atomically; a failure leaves an `_ccnew` invalid index to drop.
- Deduplication (PostgreSQL >=13) shrinks indexes with many duplicate keys automatically; a low-cardinality index that used to be huge on 12 may be fine on 13+.
- After a REINDEX, `ANALYZE` is not needed (statistics come from the table), but the index will be cold — the first queries pay I/O.

## Index-Only Scans in Practice

Three conditions, all required: every column referenced by the query is in the index (key or `INCLUDE`), the predicate is served by the index, and the visibility map says the pages are all-visible. The third is why an index-only scan degrades after a bulk load: `VACUUM` sets the visibility map, autovacuum only runs after its thresholds trip. After a large load or delete, run `VACUUM ANALYZE` explicitly.

`INCLUDE` columns are stored only in leaf pages, do not participate in ordering or uniqueness, and cannot be used in the predicate — putting a filter column in `INCLUDE` instead of the key is a common and silent mistake.

## Finding What to Fix

```sql
-- Unused, and big enough to care (check on every node, full business cycle)
SELECT relname, indexrelname, idx_scan, pg_size_pretty(pg_relation_size(indexrelid))
FROM pg_stat_user_indexes JOIN pg_index USING (indexrelid)
WHERE idx_scan = 0 AND NOT indisunique
ORDER BY pg_relation_size(indexrelid) DESC;

-- Duplicate/redundant: same table, one index's columns are a prefix of another's
SELECT indrelid::regclass, array_agg(indexrelid::regclass)
FROM pg_index GROUP BY indrelid, indkey HAVING count(*) > 1;

-- Tables taking sequential scans at scale
SELECT relname, seq_scan, idx_scan, n_live_tup
FROM pg_stat_user_tables WHERE seq_scan > idx_scan AND n_live_tup > 100000;
```

Never drop a unique or FK-supporting index on the basis of `idx_scan = 0`: constraint enforcement does not always increment the counter, and the referential integrity check needs it.

## The Write-Cost Budget

Each index costs on every write: a page write, WAL, and lost HOT eligibility for its columns. A table with 12 indexes is usually four indexes and eight hypotheses. Before adding one, name the query it serves and the plan node it removes; if you cannot, it is a hypothesis. A useful ceiling for OLTP tables: five indexes, and every addition beyond that displaces one.
