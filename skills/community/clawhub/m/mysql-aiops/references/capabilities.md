# mysql-aiops capabilities

> 35 MCP tools (26 read, 9 write); mock-validated, see `docs/VERIFICATION.md`. The
> `information_schema` / `performance_schema` queries are modelled from
> documented MySQL 8.x / MariaDB 10.6+ shapes and need live verification.
> `top_queries` / `slow_query_rca` require `performance_schema=ON`; the read
> account should have `PROCESS`, `REPLICATION CLIENT` and `SELECT` on
> `performance_schema`.

## Read tools (25)

| Tool | Source | Returns |
|------|--------|---------|
| `overview` | several reads (resilient) | version, flavor, uptimeDays, readOnly, role, connections{}, sessionsByCommand, longestQuery, mostFragmentedTable, secondsBehindSource |
| `server_version` | `version()`, `SHOW GLOBAL STATUS/VARIABLES` | version, flavor (mysql/mariadb), uptimeSeconds/Days, readOnly, superReadOnly, dataDirectory |
| `show_variables` | `SHOW GLOBAL VARIABLES` | name, value (optional LIKE filter) |
| `show_status` | `SHOW GLOBAL STATUS` | name, value (optional LIKE filter) |
| `list_databases` | `information_schema.tables` | name, tableCount, data/index/totalBytes, totalPretty |
| `list_engines` | `SHOW ENGINES` | engine, support, isDefault, transactions |
| `connection_stats` | `SHOW GLOBAL STATUS/VARIABLES` | maxConnections, threadsConnected/Running, maxUsedConnections, abortedConnects, usedPct |
| `list_sessions` | `information_schema.processlist` | total, byCommand, sleepingCount, sessions[] |
| `long_running_queries` | processlist | thresholdSeconds, count, queries[] (oldest first) |
| `list_transactions` | `information_schema.innodb_trx` | count, lockWaitCount, transactions[] (rowsLocked/Modified) |
| `lock_waits` | `performance_schema.data_lock_waits` (MariaDB: `information_schema.innodb_lock_waits`) | pairs[] {blockedId, blockingId, waitSeconds, queries} |
| `top_queries` | `events_statements_summary_by_digest` | statements[] (calls, total/mean ms, lockTimePct, noIndexUsedPct, rowsExaminedPerSent, tmpDiskTables) |
| `explain_query` | `EXPLAIN FORMAT=JSON` | plan (JSON; planned, not executed) |
| `unused_indexes` | `table_io_waits_summary_by_index_usage` | indexes[] with zero I/O since restart |
| `redundant_indexes` | `information_schema.statistics` | redundant[] {index, coveredBy, exactDuplicate} |
| `index_stats` | `information_schema.statistics` | indexes[] {columns, unique, cardinality} |
| `table_sizes` | `information_schema.tables` | tables[] data/index/totalBytes, engine, estRows |
| `table_fragmentation` | `information_schema.tables` | tables[] freeBytes (data_free), freePct |
| `table_status` | `information_schema.tables` | tables[] engine, rowFormat, autoIncrement, updateTime; nonInnodbTables[] |
| `replica_status` | `SHOW REPLICA STATUS` (MariaDB: `SHOW SLAVE STATUS`) | isReplica, replicas[] {ioThreadRunning, sqlThreadRunning, secondsBehindSource, lastIo/SqlError, gtid} |
| `binlog_status` | `SHOW BINARY LOGS` + variables + processlist | logBin, serverId, binlogFormat, gtidMode, binlogCount/TotalBytes, downstreamReplicas[] |
| `slow_query_rca` | digest rows + EXPLAIN | worst{}, planAccessTypes[], findings[] (cited cause/action) |
| `lock_wait_rca` | lock-wait pairs + `SHOW ENGINE INNODB STATUS` | roots[] (rootQuery — `null` when the root is idle inside an open transaction —, rootTrxState — InnoDB trx_state, RUNNING even when idle —, rootIdle, action), worstRootId, deadlockSuspected, lastDeadlock{victim, transactions} |
| `replication_lag_rca` | replica status record | findings[] (IO/SQL thread stopped, lagging, intentional delay, healthy) |
| `fragmentation_analysis` | fragmentation rows | recommendations[] (cited reasons + OPTIMIZE action) |

The flagship analyses accept injected records (`statements=` / `pairs=` /
`status=` / `tables=`) for pure/offline analysis, or pull live from a
configured `target`.

## Write tools (8)

| Tool | Risk | SQL | Undo / safety |
|------|------|-----|---------------|
| `kill_session` | **high** | `KILL CONNECTION <id>` | captures session user/host/query for audit; no safe inverse; dry-run + double-confirm |
| `kill_query` | **high** | `KILL QUERY <id>` | captures session; session survives, statement aborted; no inverse; dry-run + double-confirm |
| `drop_index` | **high** | `DROP INDEX ... ON ...` | rebuilds the definition from `SHOW CREATE TABLE` FIRST; undo = recreate exactly (replays via `create_index(definition=…)`); dry-run + double-confirm |
| `optimize_table` | medium | `OPTIMIZE TABLE` | records prior size/data_free stats; no undo (rebuild) |
| `analyze_table` | medium | `ANALYZE TABLE` | records prior stats; no undo |
| `create_index` | medium | `CREATE [UNIQUE] INDEX` | returns created (table, name); undo = drop it |
| `set_global_variable` | medium | `SET GLOBAL <name> = %s` | captures prior value from `SHOW GLOBAL VARIABLES`; undo = set back; runtime-only (persist yourself) |
| `reset_query_stats` | medium | `TRUNCATE ...events_statements_summary_by_digest` | irreversible; no undo |

All values are bound query parameters; identifiers that cannot be parameterised
(schema/table/index/column/variable names, ORDER BY columns) are validated
against a strict identifier charset / allow-lists and backtick-quoted before
interpolation.

## Flavor branching

| Concern | MySQL 8.x | MariaDB 10.6+ |
|---------|-----------|----------------|
| Replica status | `SHOW REPLICA STATUS` (`Source_*`/`Replica_*` fields) | `SHOW SLAVE STATUS` (`Master_*`/`Slave_*` fields) |
| Lock waits | `performance_schema.data_lock_waits` | `information_schema.innodb_lock_waits` |
| Detection | `version()` without "MariaDB" | `version()` contains "MariaDB" |

Both result shapes are normalised into one record family; `doctor` and
`overview` report the detected flavor.

## Out of scope (by design)

- Application-schema **migrations** / DDL beyond index maintenance
- ORM / model management
- Logical or physical **backup/restore** orchestration (mysqldump, PITR)
- User/grant management and `CREATE`/`DROP DATABASE`
- PostgreSQL (use **postgres-aiops**); OT / industrial equipment (use the
  `industrial-aiops` line)

Want one of these? Open an issue or PR — feedback and contributions welcome.
