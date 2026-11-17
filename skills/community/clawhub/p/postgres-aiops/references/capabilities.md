# postgres-aiops capabilities

> 35 MCP tools (25 read, 10 write). Catalog / `pg_stat_*` queries have been
> exercised against a live PostgreSQL 16.14 instance (see docs/VERIFICATION.md).
> `top_queries` / `slow_query_rca` require the `pg_stat_statements` extension;
> the read role should have `pg_monitor`.

## Read tools (25)

| Tool | Source | Returns |
|------|--------|---------|
| `overview` | several reads (resilient) | version, uptime, connections by state, idleInTransaction, longestQuery, worstBloatTable, replicas |
| `server_version` | `version()`, `pg_postmaster_start_time()` | version, serverVersion, uptime, inRecovery, dataDirectory |
| `show_settings` | `pg_settings` | name, setting, unit, category, context, source, pendingRestart |
| `list_extensions` | `pg_extension` + available | name, installedVersion, defaultVersion, updateAvailable |
| `list_databases` | `pg_database` | name, owner, encoding, sizeBytes, sizePretty |
| `list_roles` | `pg_roles` | name, superuser, canLogin, replication, connLimit |
| `list_activity` | `pg_stat_activity` | total, byState, idleInTransaction[], sessions[] |
| `long_running_queries` | `pg_stat_activity` | thresholdSeconds, count, queries[] (oldest first) |
| `list_locks` | `pg_locks`⋈`pg_stat_activity` | total, waitingCount, waiting[], locks[] |
| `top_queries` | `pg_stat_statements` | orderBy, statements[] (calls, total/mean ms, cacheHitRatioPct) |
| `explain_query` | `EXPLAIN (FORMAT JSON)` | analyze, plan (JSON) |
| `unused_indexes` | `pg_stat_user_indexes` | count, reclaimableBytes, indexes[] (idx_scan=0) |
| `missing_index_hints` | `pg_stat_user_tables` | tables[] with high seq_scan vs idx_scan |
| `index_bloat` | `pg_class`/`pg_index` | indexes[] with estBloatBytes/estBloatPct (coarse) |
| `invalid_indexes` | `pg_index` | invalid[], duplicates[] |
| `table_sizes` | `pg_class` | tables[] total/table/index/toast bytes |
| `table_bloat` | `pg_stat_user_tables` | tables[] deadPct (dead/(live+dead)) |
| `autovacuum_status` | `pg_stat_user_tables` | dead tuples, modSinceAnalyze, last (auto)vacuum/analyze |
| `replication_status` | `pg_stat_replication` | replicas[] with replayLagBytes |
| `replication_slots` | `pg_replication_slots` | slots[], inactive[] (retain WAL) |
| `wal_status` | WAL fns + `pg_stat_archiver` | currentLsn, walLevel, max/minWalSize, archiver |
| `slow_query_rca` | pg_stat_statements + EXPLAIN | worst{}, findings[] (cited cause/action) |
| `bloat_and_vacuum_analysis` | table-bloat rows | recommendations[] (cited reasons + action) |
| `blocking_lock_chain_rca` | `pg_blocking_pids` pairs | roots[] (rootQuery, rootState, rootIdle — true for any `idle*` state; rootQuery is then the last statement run, not a running one — and action), worstRootPid, deadlockSuspected |
| `undo_list` | local undo store | recorded, not-yet-applied reversible writes: undoId, ts, originalTool, inverseTool, note |

The flagship analyses accept injected records (`statements=` / `tables=` /
`pairs=`) for pure/offline analysis, or pull live from a configured `target`.

## Write tools (10)

| Tool | Risk | SQL | Undo / safety |
|------|------|-----|---------------|
| `terminate_backend` | **high** | `pg_terminate_backend(pid)` | captures pid+query for audit; no safe inverse; dry-run + double-confirm |
| `cancel_query` | **high** | `pg_cancel_backend(pid)` | captures pid+query; no inverse; dry-run + double-confirm |
| `drop_index` | **high** | `DROP INDEX` | captures `pg_get_indexdef` FIRST; undo = recreate exactly; dry-run + double-confirm |
| `run_vacuum` | medium | `VACUUM [FULL] [ANALYZE]` | records prior dead-tuple/last-vac stats; no undo |
| `run_analyze` | medium | `ANALYZE` | records prior stats; no undo |
| `create_index` | medium | `CREATE [UNIQUE] INDEX [CONCURRENTLY]` | returns created name; undo = drop it |
| `reindex` | medium | `REINDEX INDEX/TABLE/SCHEMA` | rebuild in place; no undo |
| `update_setting` | medium | `ALTER SYSTEM SET` | captures prior value; undo = set back; reports pg_reload_conf needed |
| `reset_query_stats` | medium | `pg_stat_statements_reset()` | irreversible; no undo |
| `undo_apply` | medium | dispatches the recorded inverse tool | executes a recorded inverse; the inverse runs through its own governed tool (its real risk tier + audit row are recorded there); single-use token; supports `dry_run` |

All values are bound query parameters; identifiers that cannot be parameterised
(table/index/GUC names, ORDER BY columns, index methods, REINDEX kinds) are
validated against strict allow-lists and quoted before interpolation.

## Out of scope (by design)

- Application-schema **migrations** / DDL beyond index maintenance
- ORM / model management
- Logical or physical **backup/restore** orchestration (pg_dump, PITR)
- Role/grant management and `CREATE`/`DROP DATABASE`
- OT / industrial equipment (use the `industrial-aiops` line)

Want one of these? Open an issue or PR — feedback and contributions welcome.
