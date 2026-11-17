# Partitioning — When One Heap Is Too Big

Partitioning is not a performance feature. It is a **maintenance** feature that sometimes improves performance. Adopt it for one of these reasons or not at all:

- Old data must be deleted in bulk (a partition drop is instant; a `DELETE` of 200M rows is hours plus bloat).
- Vacuum, index builds, or `REINDEX` on the whole table no longer fit in a maintenance window.
- Nearly every query filters on the same key, so pruning removes 90%+ of the data.
- Different age ranges want different storage or compression.

If none applies, a well-indexed 500M-row table is fine. Postgres does not slow down with row count; it slows down with pages touched.

## Choosing the Strategy and Key

| Strategy | Key example | Fits |
|---|---|---|
| RANGE | `created_at` monthly, `id` ranges | Time-series, retention, append-heavy history |
| LIST | `region`, `tenant_id` in groups | A closed, small set of values with different lifecycles |
| HASH | `hash(user_id)` into 8-32 parts | Spreading write contention when there is no natural range |
| No single key fits every query | Do not partition | Two access patterns pulling in different directions means partitioning helps one and taxes the other |

The key must appear in the WHERE clause of the queries you care about, or you get every downside and no pruning. It must also be part of every unique constraint and primary key on the table — a global unique index across partitions does not exist. That constraint kills partitioning for schemas whose uniqueness is on an unrelated column (a `users` table partitioned by `created_at` cannot enforce `UNIQUE (email)`).

Sizing: aim for partitions in the low tens of gigabytes and a total in the dozens to low hundreds. Planning time grows with partition count even when pruning removes them, and thousands of partitions turn a 1ms lookup into a 20ms one. Monthly beats daily unless retention demands otherwise.

## Creating and Attaching

```sql
CREATE TABLE events (id bigint GENERATED ALWAYS AS IDENTITY,
                     created_at timestamptz NOT NULL, payload jsonb,
                     PRIMARY KEY (id, created_at))
  PARTITION BY RANGE (created_at);

CREATE TABLE events_2026_07 PARTITION OF events
  FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');

CREATE TABLE events_default PARTITION OF events DEFAULT;
```

- A DEFAULT partition catches rows outside every range — without it those inserts fail. With it, attaching a new partition must scan the default to prove no rows belong there, which takes an ACCESS EXCLUSIVE lock on it. Keep the default empty and alert when it is not.
- Attaching an existing table: give it a matching `CHECK` constraint *before* `ATTACH PARTITION` and the attach skips the validation scan. Without it, the attach scans the whole table under lock.
- `ATTACH` takes SHARE UPDATE EXCLUSIVE on the parent (PostgreSQL >=12), so it does not block reads. `DETACH PARTITION CONCURRENTLY` (PostgreSQL >=14) avoids the ACCESS EXCLUSIVE that plain DETACH takes.
- Indexes: create them on the parent and Postgres creates and attaches one per partition. On an existing large partitioned table, `CREATE INDEX` on the parent locks everything — instead build each partition's index `CONCURRENTLY`, then `CREATE INDEX ON parent (...) ` with `ONLY` and attach them (`ALTER INDEX parent_idx ATTACH PARTITION child_idx`).
- Create next month's partition *before* it is needed. The most common partitioning incident is inserts failing at midnight on the 1st. Automate with `pg_partman` or a scheduled job, and alert if the newest partition ends within 7 days.

## Pruning: Verify It, Do Not Assume It

```sql
EXPLAIN SELECT * FROM events WHERE created_at >= now() - interval '1 day';
```

The plan must show only the relevant partitions. Pruning fails when:

- The predicate is not on the partition key, or wraps it in a function.
- A `now()`-based bound is compared against a partition key of a different type, forcing a cast.
- The query uses a parameter and the generic plan cannot prune at planning time — execution-time pruning (PostgreSQL >=11) still helps for nested loops and parameters, and shows as "Subplans Removed" in `EXPLAIN ANALYZE`.
- `enable_partition_pruning` is off (rare, but check `EXPLAIN (SETTINGS)`).

Two more planner behaviours worth enabling for analytics: `enable_partitionwise_join` and `enable_partitionwise_aggregate` (both off by default; they cost planning time and win big on matched partition boundaries).

## Retention and Rollover

```sql
-- Drop: instant, reclaims the file
DROP TABLE events_2025_07;
-- Or archive first, keeping it out of the parent
ALTER TABLE events DETACH PARTITION events_2025_07 CONCURRENTLY;
```

This is the whole reason most teams partition: deleting a month of data is a metadata operation instead of an hours-long `DELETE` that leaves the table bloated and the indexes full of holes.

Rollover checklist per period: create the new partition, verify the default is empty, drop or detach the expired one, and confirm the archive copy exists before the drop.

## Costs You Are Accepting

- Every query pays partition-pruning planning work; short OLTP queries against many partitions notice.
- `ON CONFLICT` on a partitioned table requires the conflict target to include the partition key.
- Foreign keys *to* a partitioned table work from PostgreSQL 12; before that, they do not.
- `CREATE INDEX CONCURRENTLY` cannot be run on a partitioned parent — per partition only.
- Row movement between partitions on `UPDATE` of the key is a delete plus insert (PostgreSQL >=11 allows it at all) and invalidates cursors.
- Autovacuum treats partitions as separate tables — good for parallelism, and it means per-table tuning has to be applied per partition (set it on the parent's new partitions as you create them).

## When the Answer Is Not Partitioning

- **Bloat** → fix the vacuum horizon; partitioning a bloated table just distributes the bloat.
- **Slow queries with a selective filter** → an index, verified with a plan.
- **A hot row or hot page** → application-level sharding of the key, or hash partitioning specifically for contention.
- **Time-series with heavy compression and rollup needs** → a purpose-built extension (see the TimescaleDB entry in SKILL.md Related Skills) rather than hand-rolled partition management.
