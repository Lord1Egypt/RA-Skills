---
name: mysql-aiops
slug: mysql-aiops
displayName: "MySQL AIops"
summary: "Governed MySQL/MariaDB DBA ops: slow-query, lock-wait, replication & fragmentation RCA; 35 tools."
license: MIT
homepage: https://github.com/AIops-tools/MySQL-AIops
tags: [aiops, mcp, governance, mysql]
description: >
  Use this skill whenever the user needs to operate or troubleshoot a MySQL 8.x or MariaDB 10.6+ server as a DBA — a one-shot server health overview (version + flavor, connection headroom, replica role); server reads (global variables, status counters, databases, storage engines); activity (sessions/processlist, long-running queries, open InnoDB transactions, lock waits); query stats (performance_schema statement-digest top-N, EXPLAIN FORMAT=JSON); index health (unused indexes, redundant/duplicate indexes, cardinality); table health (sizes, data_free fragmentation, engine/row-format status); replication (replica IO/SQL thread state and lag, binlog/GTID status); four flagship analyses — slow-query RCA (worst digest + EXPLAIN → cited cause/action incl. full-scan and lock-time-dominant classification), InnoDB lock-wait & deadlock chain RCA (wait-for tree, root blocker, last deadlock parsed from SHOW ENGINE INNODB STATUS), replication lag RCA (thread state/error fields → cause+action), and table fragmentation analysis (data_free → OPTIMIZE candidates); and guarded writes (kill a session or query, OPTIMIZE/ANALYZE TABLE, create/drop an index, SET GLOBAL a variable, reset digest stats).
  Always use this skill for "mysql health check", "why is this query slow", "top queries by time", "EXPLAIN this", "table fragmentation", "which indexes are unused", "redundant index", "who is blocking whom", "deadlock", "kill the session holding the lock", "replication lag", "replica stopped", "seconds behind master/source", "OPTIMIZE this table", "create/drop an index", or "SET GLOBAL max_connections" when the context is a MySQL or MariaDB database.
  Do NOT use for PostgreSQL — use postgres-aiops. Do NOT use when the target is OT / industrial equipment (use industrial-aiops), a hypervisor, a storage appliance, a backup product, or a container/cluster orchestrator (negative routing hints only).
  Common MySQL/MariaDB DBA operations with a built-in governance harness (audit, policy, token budget, undo, risk-tiers). Behaviour is validated by a mock-based test suite; see docs/VERIFICATION.md for the live-verification checklist.
installer:
  kind: uv
  package: mysql-aiops
argument-hint: "[session id / table / index name or describe your DBA task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["mysql-aiops","uvx"]},"optional":{"env":["MYSQL_AIOPS_CONFIG","MYSQL_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/MySQL-AIops","emoji":"🐬","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed MySQL/MariaDB DBA operations. The governance harness (audit, policy, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Connects via PyMySQL (30s timeouts) and reads information_schema / performance_schema; the server flavor (mysql vs mariadb) is detected from version() and flavor-dependent statements branch (SHOW REPLICA STATUS vs SHOW SLAVE STATUS; performance_schema.data_lock_waits vs information_schema.innodb_lock_waits).
  All write operations are audited to a local SQLite DB under ~/.mysql-aiops/ (relocatable via MYSQL_AIOPS_HOME).
  Credentials: the MySQL account password is stored ENCRYPTED in ~/.mysql-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'mysql-aiops init' to onboard, or 'mysql-aiops secret set <target>' to add one. The store is unlocked by a master password from MYSQL_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var MYSQL_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning (migrate with 'mysql-aiops secret migrate'). The password is passed to pymysql.connect at connect time and held only in memory; it is never logged or echoed.
  SQL safety: all values are bound query parameters; the few identifiers that cannot be parameterised (schema/table/index/column/variable names, ORDER BY columns) are validated against a strict identifier charset / allow-lists and backtick-quoted before interpolation. EXPLAIN rejects multi-statement input; the drop_index undo replay path is shape-gated to CREATE [UNIQUE] INDEX statements.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (budget/runaway guard + audit + risk-tier label — it records, not authorizes) and take a dry_run preview. Reversible writes fetch the real before-state first and record a faithful inverse (create_index↔drop_index, where drop rebuilds the definition from SHOW CREATE TABLE; set_global_variable restores the prior value); irreversible ops (kill session/query, optimize/analyze, reset stats) record prior state only.
  Webhooks: none — no outbound network calls beyond the configured MySQL connection.
  TLS: ssl_mode follows MySQL client semantics (default preferred); set verify_ca/verify_identity (with ssl_ca) on untrusted networks.
  Transitive dependencies: PyMySQL (pure-Python MySQL driver) and the MCP SDK. No post-install scripts or background services.
  VERIFICATION: the information_schema / performance_schema queries are modelled from documented MySQL 8.x / MariaDB 10.6+ shapes and are validated by a mock-based test suite; they have not yet been exercised against a live server (see docs/VERIFICATION.md). Community-maintained; not affiliated with Oracle or the MariaDB Foundation — trademarks belong to their owners.
---

# MySQL AIops

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by Oracle Corporation or the MariaDB Foundation.** "MySQL" and "MariaDB" trademarks belong to their owners. Source at [github.com/AIops-tools/MySQL-AIops](https://github.com/AIops-tools/MySQL-AIops) under the MIT license.

Governed MySQL / MariaDB DBA operations — **35 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.mysql-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk-tier labels. The account password is stored **encrypted** (`~/.mysql-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`mysql_aiops.governance`) — mysql-aiops has no external skill-family dependency. Behaviour is covered by a mock-based test suite; `docs/VERIFICATION.md` is the checklist for a live run against a real MySQL / MariaDB server.

## What This Skill Does

| Domain | Tools | Count | Read or Write |
|--------|-------|:-----:|:-------------:|
| **Overview** | server health snapshot (version+flavor, connections, replica role) | 1 | 1 read |
| **Server** | version+flavor, variables, status, databases, engines, connection stats | 6 | 6 read |
| **Activity** | sessions, long-running queries, transactions, lock waits | 4 | 4 read |
| **Queries** | top-N statement digests, EXPLAIN FORMAT=JSON | 2 | 2 read |
| **Indexes** | unused, redundant/duplicate, cardinality stats | 3 | 3 read |
| **Tables** | sizes, data_free fragmentation, engine/row-format status | 3 | 3 read |
| **Replication** | replica status/lag, binlog/GTID | 2 | 2 read |
| **Analysis (flagship)** | slow-query RCA, lock-wait & deadlock RCA, replication-lag RCA, fragmentation | 4 | 4 read |
| **Writes** | kill-session, kill-query, drop-index | 3 | 3 write (high) |
| | optimize, analyze-table, create-index, SET GLOBAL, reset-stats | 5 | 5 write (medium) |
| **Undo** | undo list, undo apply | 2 | 1 read / 1 write |

The flagship analyses accept injected records for pure/offline analysis, or pull live from a configured target. `top_queries` / `slow_query_rca` require `performance_schema=ON`; the read account should have `PROCESS`, `REPLICATION CLIENT` and `SELECT` on `performance_schema`.

## Quick Install

```bash
uv tool install mysql-aiops
mysql-aiops init       # interactive wizard: connection + encrypted password
mysql-aiops doctor     # connectivity + flavor + performance_schema + replica role
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/mysql-aiops
openclaw skills info mysql-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage a server (`overview`): version + flavor, uptime, connection headroom, sessions by command, longest query, most fragmented table, replica role
- Root-cause a slow query (`analyze slow-query` / `slow_query_rca`): the worst statement digest + EXPLAIN → cited cause and action (full scan, lock-time dominant, tmp-disk spill, N+1)
- Untangle a lock pile-up or deadlock (`analyze lock-waits` / `lock_wait_rca`): the wait-for tree with the root blocker named + the last deadlock parsed from `SHOW ENGINE INNODB STATUS`
- Diagnose replication (`analyze replication` / `replication_lag_rca`): IO/SQL thread state, `Seconds_Behind_Source`, error fields → cause + action
- Decide what to OPTIMIZE (`analyze fragmentation` / `fragmentation_analysis`): tables ranked by reclaimable `data_free`
- Find unused / redundant indexes; check table sizes and engines; inspect binlog/GTID state
- Kill a session or its query, OPTIMIZE/ANALYZE a table, create/drop an index (reversible), or SET GLOBAL a variable — all with dry-run + double-confirm

**Do NOT use for PostgreSQL — use postgres-aiops.** Do NOT use when the target is OT/industrial equipment (use industrial-aiops), a hypervisor, a storage appliance, a backup product, or a container cluster.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| MySQL / MariaDB DBA-ops: slow queries, lock waits, replication, fragmentation | **mysql-aiops** (this skill) |
| PostgreSQL DBA-ops | **postgres-aiops** |
| OT / industrial edge (Modbus, OPC-UA, PLC, PROFINET) | the **industrial-aiops** line |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### 1. "The application is slow" — from complaint to a working index

1. `mysql-aiops doctor` → connectivity, detected flavor, and whether
   `performance_schema` is actually enabled (if it is off, the digest-based analysis
   below has nothing to read — fix that first).
2. `mysql-aiops overview` → one-shot: version, connection counts, buffer-pool and
   activity headline, so you know whether this is a query problem or a load problem.
3. `mysql-aiops analyze slow-query` → the worst statement digests, each with cited
   findings (full scan / no index used, lock time dominant, rows examined per row sent,
   tmp-table spill to disk, high call count) and a concrete action per finding.
4. `mysql-aiops query top --limit 20` → confirm the digest the RCA blamed really is the
   top consumer, not a one-off.
5. `mysql-aiops query explain "<sql>"` → read the actual plan. `access_type: ALL` on a
   large table is the signature that an index will help; a plan already using an index
   means the fix is elsewhere.
6. `mysql-aiops index unused` and `mysql-aiops index redundant` → before adding one,
   check you are not duplicating an index that already exists (a redundant index costs
   writes and buys nothing).
7. `mysql-aiops remediate create-index <table> <col> --name idx_x --dry-run` → prints
   the exact DDL; re-run without `--dry-run` (double-confirm). The write is reversible
   and records an inverse `drop_index` undo descriptor.
8. Re-run `mysql-aiops query explain "<sql>"` and `analyze slow-query` to prove the plan
   changed and the digest dropped.
9. **Failure branch**: if the plan did not change, the optimizer may be working from
   stale statistics — `mysql-aiops remediate analyze-table <table>` and re-check. If the
   index made things *worse* (write amplification, or the optimizer picking it wrongly),
   reverse it: `mysql-aiops undo list` → `mysql-aiops undo apply <id>` drops exactly the
   index that was created. Index DDL on a large table can be long-running — if it stalls,
   `mysql-aiops activity long --min-seconds 60` will show it, and cancelling mid-DDL is
   its own risk, so size the table with `mysql-aiops table sizes` *before* step 7.

### 2. A lock pile-up is stalling writes

1. `mysql-aiops activity lock-waits` → the raw blocking/blocked pairs, straight from
   the server.
2. `mysql-aiops analyze lock-waits` → the wait-for tree resolved down to the **root
   blocker** session, with the last deadlock (victim + both statements) attached.
3. `mysql-aiops activity transactions` → what the root blocker is actually doing and how
   long it has been open. An idle-in-transaction blocker is an application bug, not a
   database one.
4. `mysql-aiops activity sessions --no-sleeping` → confirm the blocker's user, host, and
   statement before you touch it.
5. Cancel the statement, not the connection, if that is enough:
   `mysql-aiops remediate kill-query <session-id> --dry-run` then for real
   (double-confirm). Escalate to `mysql-aiops remediate kill <session-id>` only if the
   session must go.
6. Re-run `mysql-aiops analyze lock-waits` → the tree should be empty.
7. **Failure branch**: `kill` and `kill-query` are **irreversible — they record no
   undo**, and killing a long-running transaction triggers a rollback that can itself
   take a long time and hold locks meanwhile. If the tree does not clear, do not kill
   more sessions in a loop (the runaway budget guard will stop you anyway): re-read
   `activity transactions` to see whether the rollback is in progress, and go after the
   application holding the transaction open instead.

### 3. A replica has fallen behind

1. `mysql-aiops analyze replication` → the cited cause: IO thread stopped (with the real
   `Last_IO_Error`), SQL thread stopped (with `Last_SQL_Error`), applier simply lagging,
   or an intentional `SQL_Delay`.
2. `mysql-aiops repl status` → the raw replica record, so you can see the seconds-behind
   value and thread states the analysis quoted. Note the tool branches on flavor
   automatically (`SHOW REPLICA STATUS` on MySQL, `SHOW SLAVE STATUS` on MariaDB).
3. `mysql-aiops repl binlog` → binlog position and retention, to judge whether the
   replica can still catch up or has fallen off the end of the logs.
4. `mysql-aiops overview` on the replica → check the lag is not just resource pressure
   masquerading as a replication fault.
5. Apply the cause-specific fix: connectivity/credentials for a stopped IO thread, the
   diverged row for a stopped SQL thread, or parallel apply for a slow applier —
   `mysql-aiops remediate set slave_parallel_workers 4 --dry-run` first (reversible; the
   prior value is captured as the undo descriptor).
6. **Failure branch**: an intentional `SQL_Delay` is *not* a fault — the analysis says so,
   and "fixing" it defeats a deliberate safety window. If a `SET GLOBAL` made things
   worse, `mysql-aiops undo apply <id>` restores the **prior** value. If the replica has
   fallen off the retained binlogs, no setting will recover it — it needs a reseed, which
   is out of this tool's scope.

### 4. Reclaim space from a bloated table

1. `mysql-aiops analyze fragmentation` → tables ranked by reclaimable `data_free`, each
   citing the measured bytes.
2. `mysql-aiops table sizes` and `mysql-aiops table fragmentation` → confirm the size and
   free space independently, and see how big the rebuild will actually be.
3. `mysql-aiops index unused` → while you are here, an index nothing has used is dead
   weight; `mysql-aiops index stats` shows the usage numbers behind that claim.
4. `mysql-aiops remediate drop-index <table> <index-name> --dry-run` then for real — the
   write rebuilds the index definition from `SHOW CREATE TABLE` **before** dropping, so
   the undo descriptor recreates exactly the index that existed.
5. `mysql-aiops remediate optimize <table> --dry-run` → preview, then re-run to
   `OPTIMIZE TABLE` (double-confirm).
6. Re-run `mysql-aiops analyze fragmentation` to confirm the space came back.
7. **Failure branch**: `OPTIMIZE TABLE` rebuilds the table and can lock or block writes
   for the duration on a large table — run it in a maintenance window, and check
   `mysql-aiops activity long` if the system goes quiet. It records **no** undo (there is
   nothing to reverse). If dropping the index turned out to be wrong,
   `mysql-aiops undo apply <id>` recreates it from the captured definition — this is the
   one step in this recipe that *is* reversible, which is why it comes before the
   OPTIMIZE.

### Offline analysis (no live server)

Pass data straight to the analysis tools — `slow_query_rca(statements=[...])`, `lock_wait_rca(pairs=[...])`, `replication_lag_rca(status={...})`, or `fragmentation_analysis(tables=[...])` — to analyse an exported dataset without connecting.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide whether a write is
permitted. That is your agent's judgement, or the permission of the account you connect it with
(point it at a MySQL/MariaDB account granted only SELECT / PROCESS / REPLICATION CLIENT and no
write privileges (no INSERT/UPDATE/DELETE/DDL) — writes then fail at the server). There is no
read-only switch, policy file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.mysql-aiops/audit.db` (relocatable via `MYSQL_AIOPS_HOME`): params, result, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `MYSQL_AUDIT_APPROVED_BY` / `MYSQL_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `MYSQL_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Reversible writes fetch the real before-state and record an inverse descriptor; irreversible ops (kill session/query, optimize/analyze, reset stats) record prior state only.
- All values are bound query parameters; identifiers that cannot be parameterised are validated and backtick-quoted.

## References

- `references/capabilities.md` — full tool + field reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
