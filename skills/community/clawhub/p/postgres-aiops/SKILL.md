---
name: postgres-aiops
slug: postgres-aiops
displayName: "Postgres AIops"
summary: "Governed PostgreSQL DBA ops: slow-query RCA, bloat/vacuum & blocking-lock analysis; 35 MCP tools."
license: MIT
homepage: https://github.com/AIops-tools/Postgres-AIops
tags: [aiops, mcp, governance, postgres]
description: >
  Use this skill whenever the user needs to operate or troubleshoot a PostgreSQL server/cluster as a DBA — a one-shot cluster health overview; server reads (version/uptime, settings, extensions, databases, roles); activity (sessions, idle-in-transaction, long-running queries, locks); query stats (pg_stat_statements top-N, EXPLAIN a statement); index health (unused indexes, missing-index hints, bloat, invalid/duplicate); table health (sizes, dead-tuple bloat, autovacuum status); replication (standby lag, replication slots, WAL); three flagship analyses — slow-query RCA (worst pg_stat_statements entry + EXPLAIN → cause/action), bloat & vacuum analysis (dead tuples + autovacuum lag → recommendation), and blocking lock-chain RCA (build the wait-for tree, name the root blocker); and guarded writes (terminate a backend, cancel a query, VACUUM/ANALYZE, create/drop an index, REINDEX, ALTER SYSTEM SET a parameter, reset query stats).
  Always use this skill for "postgres health check", "why is this query slow", "pg_stat_statements top queries", "EXPLAIN this", "table/index bloat", "which indexes are unused", "missing index", "autovacuum status", "who is blocking whom", "kill the backend holding the lock", "replication lag", "replication slots", "VACUUM this table", "create/drop an index", or "ALTER SYSTEM SET work_mem" when the context is a PostgreSQL database.
  Do NOT use when the target is OT / industrial equipment (Modbus, OPC-UA, PLCs — use industrial-aiops), a hypervisor, a storage appliance, a backup product, a container/cluster orchestrator, or a non-PostgreSQL database (negative routing hints only).
  Covers common PostgreSQL DBA operations with a built-in governance harness (audit, token budget, undo, risk-tiers). Beyond the mock suite, the reads plus a governed write and its undo have been exercised against a live PostgreSQL 16.14 instance (see docs/VERIFICATION.md).
installer:
  kind: uv
  package: postgres-aiops
argument-hint: "[pid / table / index name or describe your DBA task]"
allowed-tools:
  - Bash
metadata: {"openclaw":{"requires":{"anyBins":["postgres-aiops","uvx"]},"optional":{"env":["POSTGRES_AIOPS_CONFIG","POSTGRES_AIOPS_MASTER_PASSWORD"]},"homepage":"https://github.com/AIops-tools/Postgres-AIops","emoji":"🐘","os":["macos","linux"]}}
compatibility: >
  Standalone, self-governed PostgreSQL DBA operations. The governance harness (audit, token/runaway budget, undo, risk-tiers) is bundled in the package — no external skill-family dependency. Connects via psycopg 3 and reads the system catalogs and pg_stat_* views.
  All write operations are audited to a local SQLite DB under ~/.postgres-aiops/ (relocatable via POSTGRES_AIOPS_HOME).
  Credentials: the PostgreSQL role password is stored ENCRYPTED in ~/.postgres-aiops/secrets.enc (Fernet/AES-128 + scrypt-derived key) — never plaintext on disk. Run 'postgres-aiops init' to onboard, or 'postgres-aiops secret set <target>' to add one. The store is unlocked by a master password from POSTGRES_AIOPS_MASTER_PASSWORD (non-interactive/MCP/CI) or an interactive prompt (CLI on a TTY). A legacy plaintext env var PG_<TARGET_NAME_UPPER>_PASSWORD is still honoured as a fallback with a deprecation warning (migrate with 'postgres-aiops secret migrate'). The password is passed to psycopg.connect at connect time and held only in memory; it is never logged or echoed.
  SQL safety: all values are bound query parameters; the few identifiers that cannot be parameterised (table/index/GUC names, ORDER BY columns, index methods) are validated against strict allow-lists and quoted before interpolation. EXPLAIN rejects multi-statement input.
  State-changing operations require double confirmation at the CLI layer and support --dry-run. All write tools pass through the @governed_tool decorator (budget guard + audit + risk-tier tagging) and take a dry_run preview. Reversible writes fetch the real before-state first and record a faithful inverse (create_index↔drop_index, where drop captures pg_get_indexdef; update_setting restores the prior value); irreversible ops (terminate/cancel, vacuum/analyze, reindex, reset stats) record prior stats only.
  Webhooks: none — no outbound network calls beyond the configured PostgreSQL connection.
  SSL: sslmode follows libpq (default prefer); set require/verify-full on untrusted networks.
  Transitive dependencies: psycopg[binary] (PostgreSQL driver) and the MCP SDK. No post-install scripts or background services.
  Verification status: the catalog / pg_stat_* reads, the bloat/vacuum RCA, and the create_index/drop_index governed write path (audit + undo) have been exercised against a live PostgreSQL 16.14 instance; docs/VERIFICATION.md records what was and was not covered. Community-maintained; not affiliated with the PostgreSQL project — trademarks belong to their owners.
---

# Postgres AIops

> **Disclaimer**: Community-maintained open-source project, **not affiliated with, endorsed by, or sponsored by the PostgreSQL Global Development Group or any vendor.** "PostgreSQL" and related trademarks belong to their owners. Source at [github.com/AIops-tools/Postgres-AIops](https://github.com/AIops-tools/Postgres-AIops) under the MIT license.

Governed PostgreSQL DBA operations — **35 MCP tools**, every one wrapped with the bundled `@governed_tool` harness: a local unified audit log under `~/.postgres-aiops/`, token/runaway budget guard, undo-token recording, and descriptive risk-tier labels. The role password is stored **encrypted** (`~/.postgres-aiops/secrets.enc`, Fernet + scrypt) — never plaintext on disk.

> **Standalone**: the governance harness is bundled in the package (`postgres_aiops.governance`) — postgres-aiops has no external skill-family dependency. Beyond the mock suite, the reads plus a governed write and its undo have been exercised against a live PostgreSQL 16.14 instance (see `docs/VERIFICATION.md`).

## What This Skill Does

| Domain | Tools | Count | Read or Write |
|--------|-------|:-----:|:-------------:|
| **Overview** | cluster health snapshot | 1 | 1 read |
| **Server** | version, settings, extensions, databases, roles | 5 | 5 read |
| **Activity** | sessions, long-running queries, locks | 3 | 3 read |
| **Queries** | top-N (pg_stat_statements), EXPLAIN | 2 | 2 read |
| **Indexes** | unused, missing hints, bloat, invalid/duplicate | 4 | 4 read |
| **Tables** | sizes, dead-tuple bloat, autovacuum status | 3 | 3 read |
| **Replication** | status/lag, slots, WAL | 3 | 3 read |
| **Analysis (flagship)** | slow-query RCA, bloat/vacuum, blocking chains | 3 | 3 read |
| **Writes** | terminate, cancel, drop-index | 3 | 3 write (high) |
| | vacuum, analyze, create-index, reindex, ALTER SYSTEM, reset-stats | 6 | 6 write (medium) |

The flagship analyses accept injected records for pure/offline analysis, or pull live from a configured target. `top_queries` / `slow_query_rca` require the `pg_stat_statements` extension; the read role should have `pg_monitor`.

## Quick Install

```bash
uv tool install postgres-aiops
postgres-aiops init       # interactive wizard: connection + encrypted password
postgres-aiops doctor
```

Or as an OpenClaw plugin, which installs this skill and its MCP server together:

```bash
openclaw plugins install clawhub:@zw008/postgres-aiops
openclaw skills info postgres-aiops          # expect: Visible to model: yes
```

Needs `uvx` on `PATH`: the MCP server is fetched with uv, pinned to this release.

## When to Use This Skill

- Triage a cluster (`overview`): version/uptime, connections by state, idle-in-transaction, longest query, worst bloat, replica lag
- Root-cause a slow query (`analyze slow-query` / `slow_query_rca`): the worst `pg_stat_statements` entry + EXPLAIN → cited cause and action
- Decide what to vacuum (`analyze bloat-vacuum` / `bloat_and_vacuum_analysis`): tables ranked by dead-tuple ratio + autovacuum lag
- Untangle a lock pile-up (`analyze blocking` / `blocking_lock_chain_rca`): the wait-for tree with the root blocker named
- Find unused / missing / bloated indexes; check autovacuum status and table sizes; inspect replication lag and slots
- Terminate/cancel a backend, VACUUM/ANALYZE, create/drop an index (reversible), REINDEX, or ALTER SYSTEM SET — all with dry-run + double-confirm

**Do NOT use when** the target is OT/industrial equipment (use industrial-aiops), a hypervisor, a storage appliance, a backup product, a container cluster, or a non-PostgreSQL database.

## Related Skills — Skill Routing

| If the user wants… | Use |
|--------------------|-----|
| PostgreSQL DBA-ops: slow queries, bloat, locks, index/vacuum maintenance | **postgres-aiops** (this skill) |
| OT / industrial edge (Modbus, OPC-UA, PLC, PROFINET) | the **industrial-aiops** line |
| Hypervisor VM lifecycle (power, snapshot, migrate) | a hypervisor ops skill |
| Container/cluster lifecycle | a cluster ops skill |

## Common Workflows

### "The app got slow this afternoon" — root-cause and add the missing index

1. `postgres-aiops overview` → one-shot cluster picture: connections, database sizes, obvious saturation
2. `postgres-aiops analyze slow-query` → the worst `pg_stat_statements` entry with cited findings (seq scan, low cache-hit ratio, temp spill, high call count) and a concrete action for each
3. `postgres-aiops query explain "<sql>"` → confirm the plan yourself; a Seq Scan on a large table is the index signal
4. `postgres-aiops index missing` → the tool's own index hints, to cross-check that step 3's conclusion is not a one-off
5. `postgres-aiops remediate create-index <table> <col> --concurrently --dry-run` → preview the exact DDL; then run without `--dry-run` (double confirmation). `create_index` is reversible — an inverse `drop_index` is recorded
6. `postgres-aiops query reset` then re-run `analyze slow-query` after a while → confirm the query actually dropped out of the top, rather than assuming
7. **Failure branch**: if the new index does not help, or `--concurrently` left an `INVALID` index (`postgres-aiops index invalid`), roll it back with `postgres-aiops undo list` → `postgres-aiops undo apply <id>`. An invalid index still costs writes — drop it rather than leaving it behind.

### Reclaim table bloat and retire a redundant index (reversible)

1. `postgres-aiops analyze bloat-vacuum` → tables ranked by dead-tuple ratio and autovacuum lag, each citing the measured numbers
2. `postgres-aiops table autovacuum` → check whether autovacuum is simply behind (last run, thresholds) before doing it by hand
3. `postgres-aiops remediate vacuum <table> --analyze --dry-run` → preview; then run for real to `VACUUM ANALYZE` (double confirmation)
4. `postgres-aiops index unused` and `postgres-aiops index bloat` → find indexes that cost writes and return nothing
5. `postgres-aiops remediate drop-index <name> --concurrently --dry-run`, then for real → the tool captures `pg_get_indexdef` **before** dropping and records an inverse recreate descriptor
6. **Failure branch**: dropped the wrong index — `postgres-aiops undo apply <id>` recreates it from the captured definition (not a guess). Note `--full` on `remediate vacuum` takes an **exclusive lock** and rewrites the table; it has no undo, so never reach for it as a first response on a live table.

### Break a blocking pile-up during an incident

1. `postgres-aiops analyze blocking` → the wait-for chain, naming the **root blocker** pid rather than the visible victims
2. `postgres-aiops activity locks` → the raw lock rows behind the chain; confirm the blocker is what the RCA says it is
3. `postgres-aiops activity long --min-seconds 60` → how long the blocker has actually been running, and whether it is idle-in-transaction
4. `postgres-aiops remediate cancel <pid> --dry-run` → preview; then for real. **Cancel before terminate** — cancel ends the query, terminate kills the whole backend and rolls back its transaction
5. Only if cancel does not clear it: `postgres-aiops remediate terminate <pid>` (double confirmation)
6. **Failure branch**: both `cancel_query` and `terminate_backend` declare **no undo** — a killed session cannot be restored. The audit row in `~/.postgres-aiops/audit.db` captures the prior query text and state for the incident write-up. If the same blocker reappears, the fix is upstream (application transaction scope), not another terminate.

### Tune a parameter and prove it moved the needle (reversible)

1. `postgres-aiops server settings work_mem` → the current value and where it came from
2. `postgres-aiops analyze slow-query` → confirm a temp-spill finding is what actually motivates the change
3. `postgres-aiops remediate set work_mem 64MB --dry-run` → preview the `ALTER SYSTEM SET`; then run for real (double confirmation) — the prior value is captured and an inverse `update_setting` is recorded
4. Reload/restart per the parameter's context, then `postgres-aiops server settings work_mem` to confirm the value took effect
5. **Failure branch**: if the change causes memory pressure, `postgres-aiops undo apply <id>` restores the **prior** value. `ALTER SYSTEM` only writes `postgresql.auto.conf` — a parameter with `context = postmaster` needs a restart, so a "successful" write that did not change behaviour usually means the restart is still pending, not that the tool failed.

### Offline analysis (no live cluster)

1. Export `pg_stat_statements`, table-bloat, and blocking-pair rows to JSON
2. Feed them straight to the analysis tools — `slow_query_rca(statements=[...])`, `bloat_and_vacuum_analysis(tables=[...])`, `blocking_lock_chain_rca(pairs=[...])` — no connection or credentials required
3. **Failure branch**: a tool that rejects the injected rows means the export is missing the columns the analysis needs (calls/total_time/rows, dead-tuple counts, blocked/blocking pids) — re-export rather than hand-editing, so the findings stay traceable to the cluster.

## Governance & Safety

The skill delivers reads and writes and records them; it does **not** decide whether a write is
permitted. That is your agent's judgement, or the permission of the account you connect it with
(connect with a PostgreSQL role that has no write privileges (a read-only role, or one without
INSERT/UPDATE/DELETE/DDL) — writes then fail at the server). There is no read-only switch, policy
file, or approval gate.

- **Audit is the guarantee, and it is not bypassable.** Every operation — MCP and CLI alike — is logged to `~/.postgres-aiops/audit.db` (relocatable via `POSTGRES_AIOPS_HOME`): params, result, status, duration, and the risk tier. The CLI writes the same row the MCP path does.
- `POSTGRES_AUDIT_APPROVED_BY` / `POSTGRES_AUDIT_RATIONALE` are optional annotations recorded on the audit row (who/why); they are never required and never block.
- **Runaway guard** — a safety backstop, not authorization: the same call looped in a tight window trips a circuit breaker. Disable with `POSTGRES_RUNAWAY_MAX=0`.
- Writes support `--dry-run` / `dry_run=True` and double confirmation at the CLI.
- Reversible writes fetch the real before-state and record an inverse descriptor; irreversible ops (terminate/cancel, vacuum/analyze, reindex, reset stats) record prior stats only.
- All values are bound query parameters; identifiers that cannot be parameterised are validated and quoted.

## References

- `references/capabilities.md` — full tool + field reference
- `references/cli-reference.md` — CLI command reference
- `references/setup-guide.md` — onboarding, credentials, and connectivity
