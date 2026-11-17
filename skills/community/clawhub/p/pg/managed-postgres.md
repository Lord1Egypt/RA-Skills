# Managed Postgres — What Changes on RDS, Aurora, Cloud SQL, Neon, Supabase

On every managed platform, three things are different before anything else: **you are not superuser**, **`ALTER SYSTEM` is replaced by the provider's parameter mechanism**, and **the extension list is an allowlist**. Most "this doesn't work on RDS" reports are one of those three.

Set the `deployment` variable (SKILL.md Configuration) so recipes come out in the right dialect.

## The Common Constraints

- **No superuser.** You get an admin role with most privileges (`rds_superuser`, `cloudsqlsuperuser`, `supabase_admin`). What it usually cannot do: read server files, `COPY ... FROM '/path'` (use `\copy`), install arbitrary extensions, change `shared_preload_libraries` without a managed restart, or write to the data directory.
- **Configuration is out of band.** Parameter groups (RDS), flags (Cloud SQL), a dashboard or API (Neon, Supabase). Static parameters need a reboot; the console shows "pending reboot" and the setting silently does nothing until then. Verify with `SHOW`, never with the console alone.
- **Extensions are allowlisted** and versioned by the provider; `SELECT * FROM pg_available_extensions` is the ground truth for your instance.
- **Backups are provider snapshots** plus WAL archiving you do not manage. That is real PITR, and it is still inside the same account — a logical dump stored elsewhere is the answer to "the account is gone" (backup guide).
- **Minor upgrades are applied in maintenance windows**, sometimes automatically. Know your window; a surprise restart in the middle of a migration is otherwise unexplainable.
- **Metrics arrive through the provider console**, but `pg_stat_statements` is available on all of them and is more useful than any dashboard graph. Enable it first (monitoring guide).

## Per Platform

**RDS for PostgreSQL** — closest to stock. `rds_superuser` grants most things; `shared_preload_libraries` is a parameter-group entry needing a reboot. Storage autoscaling exists but IOPS may be provisioned separately — a load that suddenly crawls is often a burst-balance cliff, not a plan change. Major upgrades are provider-driven `pg_upgrade`; Blue/Green deployments cut the downtime and are the recommended path. RDS Proxy is a managed pooler in transaction mode with the usual session-state caveats (connections guide). `pg_repack` and `pg_cron` are available; check the version list.

**Aurora PostgreSQL** — Postgres-compatible, different storage engine. Replicas share the storage layer, so replica lag is measured in milliseconds and `pg_stat_replication` does not look like a stock cluster. Physical replication settings, `wal_keep_size`, and slot management largely do not apply. Failover is fast and automatic; the reader endpoint load-balances across replicas, which means read-your-writes needs the writer endpoint explicitly. Costs are per I/O on some configurations, which makes a seq scan a line item — this is the one platform where an unnecessary full scan is billed directly.

**Cloud SQL for PostgreSQL** — flags instead of parameter groups, `cloudsqlsuperuser`, and the Cloud SQL Auth Proxy or a private IP for connectivity. IAM database authentication replaces passwords for service accounts. Extension availability is narrower than RDS; check before designing around one.

**Neon** — separates storage from compute. Scale-to-zero means the first connection after idle pays a cold start (typically sub-second to a few seconds) — a health check every minute changes the cost model, so decide deliberately. Branching is copy-on-write: a full-size branch for testing a migration costs almost nothing, which makes the "rehearse the migration on production-scale data" advice (migrations guide) practically free. Use the pooled endpoint (a Supavisor/PgBouncer-style pooler in transaction mode) for serverless functions and the direct endpoint for migrations and session-state work.

**Supabase** — Postgres plus an auto-generated API, and the reason RLS is not optional there: tables exposed through the API are reachable by the anon key, and RLS is the only thing between them and the internet (security guide). Two ports: session mode and transaction mode through Supavisor — pick transaction mode for serverless, session mode for anything using session state or prepared statements. `supabase_admin` is the elevated role; migrations run as the postgres role.

**Anything else (Azure Flexible Server, DigitalOcean, Heroku, Render, Timescale Cloud)** — ask the same four questions: which admin role, where do parameters live, which extensions are allowlisted, and what exactly the backup covers.

## Decisions the Platform Makes For You

| Question | Self-hosted answer | Managed answer |
|---|---|---|
| Where does pooling live | You install PgBouncer | The provider's pooler, in transaction mode, with its caveats |
| How do parameters change | `ALTER SYSTEM` + reload | Parameter group / flag, sometimes a reboot |
| How do major upgrades happen | `pg_upgrade` or logical replication, your window | Provider workflow (Blue/Green on RDS), still needs your rehearsal |
| Who watches the disk | You | The provider autoscales storage — and bills for it; alert on growth anyway |
| Who has the WAL | You | The provider; PITR window is a setting with a cost |
| What restores a dropped table | Your PITR runbook | A restore to a **new instance** at a timestamp, then copy the table back — the same shape, different buttons |

## What Does Not Change

Everything in the rest of this skill: indexes, plans, locks, vacuum behaviour, MVCC, transaction semantics, SQL. Providers change the operational envelope, not the engine. When a managed database is slow, the cause is a plan or a lock far more often than the platform — read the plan before opening a support ticket.
