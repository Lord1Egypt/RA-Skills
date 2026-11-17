# Upgrades — Minor, Major, OS, and Extensions

## Minor Upgrades Are Not Optional

15.6 → 15.7 is a binary swap plus a restart: no dump, no rewrite, no application change. They carry the security fixes and the data-loss bug fixes. A cluster three minor versions behind is carrying known bugs for no benefit. Read the release notes for the rare "this fix requires a REINDEX of affected indexes" note — those exist and they are the reason to read.

## Major Upgrades: Three Paths

| Path | Downtime | Cost |
|---|---|---|
| `pg_upgrade --link` | Minutes | Hard-links data files; the old cluster is unusable afterwards, so rollback means restoring a backup |
| `pg_upgrade --copy` | Proportional to data size | Old cluster stays intact — the rollback path is "start the old one" |
| Logical replication | Seconds (a controlled cutover) | Most setup work; the only option that also crosses providers or platforms |
| Dump and restore | Hours on large data | Simplest, and the only one that also rebuilds a bloated database |

`pg_upgrade` sequence that avoids the usual surprises:

1. Install the new binaries alongside the old. Both versions must be present.
2. Verify **every extension** has a build for the new version, installed, before starting. A missing extension binary aborts the upgrade mid-flight.
3. `pg_upgrade --check` first. It reports incompatibilities without touching anything.
4. Take a backup you have verified (a restore drill, not a dump file).
5. Stop the old cluster cleanly, run the upgrade, start the new one.
6. **Rebuild planner statistics**: `vacuumdb --all --analyze-in-stages`. Before PostgreSQL 18, `pg_upgrade` does not carry statistics over, so the first minutes on the new version run with no statistics at all — this is the "we upgraded and everything got slower" report, and it is self-inflicted.
7. `ALTER EXTENSION ... UPDATE` for each extension, then run the application's smoke tests before removing the old cluster.

Near-zero-downtime with logical replication: build the new-version cluster, replicate the tables, wait for lag ≈ 0, stop writes, fix sequences with `setval()`, repoint the application, resume. Logical replication does not carry DDL or sequence values (details in the replication guide), and both bite exactly at cutover.

## Version Floors Worth Knowing

Features this skill gates on, oldest first — useful when deciding whether an upgrade unblocks a design:

- **10**: `IDENTITY` columns, declarative partitioning, logical replication, hash indexes made crash-safe
- **11**: `ADD COLUMN ... DEFAULT` without a rewrite, covering `INCLUDE` indexes, `websearch_to_tsquery`, procedures with transaction control
- **12**: CTEs inlined by default, `REINDEX CONCURRENTLY`, generated columns, cheap `SET NOT NULL`, `recovery.conf` removed
- **13**: `gen_random_uuid()` in core, B-tree deduplication, trusted extensions, `max_slot_wal_keep_size`
- **14**: `DETACH PARTITION CONCURRENTLY`, LZ4 TOAST compression, `pg_read_all_data`, `idle_session_timeout`, vacuum failsafe
- **15**: `MERGE`, `UNIQUE NULLS NOT DISTINCT`, ICU collations at database level, `public` schema no longer world-writable
- **16**: `pg_stat_io`, logical replication from a standby, parallel apply
- **17**: incremental base backups with `pg_combinebackup`, `pg_stat_checkpointer`, SQL/JSON (`JSON_TABLE`), `EXPLAIN (SERIALIZE)`
- **18**: `uuidv7()`, virtual generated columns, B-tree skip scan, asynchronous I/O, statistics carried through `pg_upgrade`

## The OS Upgrade Nobody Schedules

Upgrading the operating system changes glibc, and glibc changes text collation. Sort order changes silently, and **every index on a text column built under the old collation is now wrong**: unique constraints can miss duplicates, range scans can skip rows, and nothing errors.

- After any OS major upgrade, container base image change, or migration between distributions: `REINDEX` every index containing a text, varchar, or citext column. `REINDEX DATABASE CONCURRENTLY` if you cannot take the outage.
- PostgreSQL >=15 records collation versions and logs a warning when they mismatch; check `pg_database.datcollversion` and `pg_collation.collversion`, then `ALTER DATABASE ... REFRESH COLLATION VERSION` *after* reindexing, never before (refreshing first hides the problem).
- Prevention: `COLLATE "C"` for identifiers, codes, slugs, and anything not shown to a human in sorted order — byte ordering never changes. ICU collations (PostgreSQL >=15 at database level) are versioned independently of the OS and change on their own schedule, which is at least a schedule you can see.
- The same hazard applies to a restore into a different OS: dump and restore rebuilds indexes, so it is safe; a physical backup or replica moved across OS versions carries the old indexes and the new collation.

## Extension Upgrades

- `SELECT extname, extversion FROM pg_extension;` then `ALTER EXTENSION x UPDATE;` — installing new binaries does not update the catalog definition, and the mismatch produces functions that do not exist.
- PostGIS upgrades are coupled to its own version matrix and often need `postgis_extensions_upgrade()`; treat them as their own project.
- Extensions with background workers or preloaded libraries need the new `shared_preload_libraries` entry present at first start of the new cluster, or it will not start.
- pgvector, TimescaleDB, and pg_partman all store data structures whose format can change between versions — read their upgrade notes, not just Postgres's.

## Rehearse, Then Do

Restore the latest backup into a scratch instance, run the upgrade there, time it, run the application test suite against it, and compare the top twenty statements from `pg_stat_statements` before and after. That rehearsal converts the upgrade window from an estimate into a measurement, and it is where you discover the missing extension build — at no cost.
