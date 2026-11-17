# Replication — Replicas, Lag, Logical Streams, Failover

Two mechanisms with different jobs: **physical** (streaming WAL, byte-identical replica, whole cluster) for high availability and read scaling; **logical** (decoded row changes, per table) for selective replication, cross-version moves, and zero-downtime upgrades.

## Physical Streaming Replication

Primary: `wal_level = replica` (default), `max_wal_senders` (default 10), a replication role. Standby: `pg_basebackup -D data -R --checkpoint=fast` writes the connection info and the `standby.signal` file.

- **Replication slots** guarantee the primary keeps WAL until the standby consumes it. Without a slot, a standby that falls behind past `wal_keep_size` is broken and needs a rebuild. With a slot, a standby that goes away forever fills `pg_wal` and takes the primary down instead. Both failure modes are real: use slots, and cap them with `max_slot_wal_keep_size` (PostgreSQL >=13) so the primary sacrifices the standby rather than itself.
- Since PostgreSQL 12 there is no `recovery.conf`: recovery settings live in `postgresql.conf` plus `standby.signal`. This is the single most common breakage when following an old runbook.

## Measuring Lag Correctly

```sql
-- On the primary: per-standby, in bytes and in time
SELECT application_name, state, sync_state,
       pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) AS replay_bytes,
       write_lag, flush_lag, replay_lag
FROM pg_stat_replication;

-- On the standby: time since the last replayed commit
SELECT now() - pg_last_xact_replay_timestamp() AS replay_delay;
```

- Bytes are the honest metric. The time-based number on an idle primary grows forever even though the standby is perfectly caught up — the classic false alarm at 3am on a quiet Sunday. Alert on bytes, and on time only when the primary is known to be writing.
- `write_lag` / `flush_lag` / `replay_lag` (PostgreSQL >=10) separate network from disk from apply. Apply-only lag means the standby is CPU-bound or blocked by its own queries.

## Conflicts on the Standby

A read replica replaying WAL can need a page that a running query on it still reads. Postgres waits `max_standby_streaming_delay` (default 30s) and then cancels the query: "canceling statement due to conflict with recovery".

Two ways out, and they trade against each other:

- Raise `max_standby_streaming_delay` — long analytics survive, replay lag grows to match.
- `hot_standby_feedback = on` — the standby tells the primary its oldest snapshot, so the primary stops vacuuming those rows. Queries survive, and **the primary bloats** (it shows up as `backend_xmin` in `pg_stat_replication`; see the bloat horizon checks in the vacuum guide).

Pick per workload: a reporting replica gets feedback on and a generous delay; an HA standby that must be ready to promote gets neither.

## Synchronous Replication

`synchronous_standby_names` plus `synchronous_commit` decide how much a commit waits:

| `synchronous_commit` | Commit returns after | Loss window |
|---|---|---|
| `off` | WAL buffered locally | Up to ~3 × `wal_writer_delay` (default 200ms) of committed transactions on a crash; never corruption |
| `local` | Local WAL flush | Local durability only |
| `remote_write` | Standby received it into its OS | Standby OS crash loses it |
| `on` (default) | Standby flushed to disk | Standby disk loss |
| `remote_apply` | Standby applied it — reads are current | Highest latency |

One synchronous standby is an availability trap: if it goes down, every commit on the primary blocks. Use `ANY 1 (s1, s2)` with two candidates, or accept asynchronous replication honestly. `synchronous_commit` can also be set per transaction — durable for payments, `off` for telemetry, in the same database.

## Logical Replication

```sql
-- publisher (wal_level = logical)
CREATE PUBLICATION pub FOR TABLE orders, customers;
-- subscriber
CREATE SUBSCRIPTION sub CONNECTION 'host=... dbname=...' PUBLICATION pub;
```

What it does not do, and every one of these has cost somebody a cutover:

- **No DDL.** Schema changes must be applied on both sides, subscriber first for additive changes.
- **No sequence values.** After a cutover, `setval()` every sequence past the maximum key or the new primary starts issuing duplicates.
- **UPDATE/DELETE need a replica identity.** Default is the primary key; a table without one errors on update. `REPLICA IDENTITY FULL` works and makes the subscriber match rows by full-row comparison — expensive, and it needs an index on the subscriber to avoid a sequential scan per change.
- **Initial sync copies data** while streaming continues; large tables can be excluded and loaded manually (`copy_data = false`).
- **Conflicts stop the stream.** A duplicate key on the subscriber halts apply until you resolve it; monitor `pg_stat_subscription` and the subscriber log.
- Since PostgreSQL 16 a logical replica can be created from a standby, and apply can be parallelized for large transactions.

Use it for: major-version upgrades with seconds of downtime, moving to another provider, feeding an analytics database a subset of tables, splitting a monolith database.

## Failover

- Promote: `SELECT pg_promote()` or `pg_ctl promote`. The standby ends recovery and starts a new timeline.
- The old primary cannot simply be restarted as a standby — it may contain WAL the new primary never had. Either rebuild it with `pg_basebackup`, or use `pg_rewind` (requires `wal_log_hints = on` or data checksums).
- Split brain comes from the application, not the database: two nodes both accepting writes because a proxy or DNS entry still points at the old primary. The fencing step (stop the old primary, move the VIP) belongs in the runbook before the promote step.
- Automate with Patroni, repmgr, or pg_auto_failover. A hand-run failover is fine only if it has been rehearsed on a schedule; the untested runbook fails at 3am, reliably.
- After promotion: verify sequences, re-point read replicas at the new primary (they follow a timeline, not a hostname), and confirm backups are running from the new node.

## Read-Your-Writes on Replicas

Routing reads to a replica breaks the moment a user writes and immediately reads back. Three workable answers:

1. Route the session to the primary for a few seconds after any write (simple, coarse, usually enough).
2. Record `pg_current_wal_lsn()` at write time and only use a replica whose `pg_last_wal_replay_lsn()` has passed it (precise, needs plumbing).
3. Keep write-adjacent reads on the primary by design and send only reporting to replicas (least code, most discipline).

Anything else — "the lag is usually 20ms" — is a bug that appears under load, which is the moment lag is not 20ms.
