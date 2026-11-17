# Incidents — Production Playbooks

Order of operations for every incident: **observe, then act**. `pg_stat_activity` and the log answer "what is happening" in ten seconds, and restarting the database destroys that evidence along with the problem.

## The Universal First Look

```sql
SELECT count(*) FILTER (WHERE state='active')     AS active,
       count(*) FILTER (WHERE state='idle in transaction') AS idle_tx,
       count(*)                                    AS total,
       max(now() - xact_start)                     AS oldest_tx
FROM pg_stat_activity WHERE backend_type = 'client backend';
```

Plus, from the shell: free space on the data and WAL filesystems, and the last 100 lines of the server log. Those three views separate "one bad query" from "the disk is full" from "the app is retry-storming", which need opposite responses.

## Disk Full

The cluster stops accepting writes and may refuse to start. Find the consumer before deleting anything:

| Consumer | Check | Fix |
|---|---|---|
| `pg_wal` growing | `SELECT slot_name, active, pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) FROM pg_replication_slots;` | Drop the inactive slot (`pg_drop_replication_slot`) — that WAL is being kept for a subscriber that is gone |
| `pg_wal` growing, no slots | `SELECT * FROM pg_stat_archiver;` | `archive_command` is failing; fix it, and the backlog drains |
| Table/index bloat | Largest relations by `pg_total_relation_size` | Vacuum horizon first, `pg_repack` after (vacuum guide) |
| Temp files | `log_temp_files`, `base/pgsql_tmp` size | A query spilling: cancel it, then fix `work_mem` for that statement |
| Logs | Filesystem, not Postgres | Rotate; move logs off the data volume permanently |

**Never delete files from `pg_wal` by hand.** Removing an unarchived WAL segment turns a full disk into an unrecoverable cluster. If you need emergency space, delete a log file or an old archive, or grow the volume.

Prevention that actually works: alert at 25% free (monitoring guide), keep WAL on its own filesystem, and set `max_slot_wal_keep_size` so a dead slot cannot take the primary down (replication guide).

## Transaction ID Wraparound

Symptom: warnings in the log about `datfrozenxid`, then "database is not accepting commands to avoid wraparound data loss".

1. Find the tables: order `pg_class` by `age(relfrozenxid)` (query in the vacuum guide).
2. Vacuum them, biggest age first: `VACUUM (FREEZE, VERBOSE) tbl;` — the database still accepts vacuum even when it refuses writes. Single-user mode is a last resort, not step one.
3. Find what stopped autovacuum from doing this months ago: a disabled autovacuum, a long transaction, an orphaned slot, or a table with `autovacuum_enabled = false` set "temporarily" in 2024.
4. After recovery, alert on `age(datfrozenxid)` at 75% of `autovacuum_freeze_max_age`.

## Connection Storm

`FATAL: sorry, too many clients already`, usually with the application retrying and making it worse.

1. Read the state breakdown (connections guide) — `idle in transaction` means an application bug, `active` means real load or one blocker.
2. If one query is blocking everything: `pg_cancel_backend(pid)` on the blocker, not on the victims (locks guide).
3. Stop the retry storm at the application: a client that reconnects instantly on failure is a denial of service against its own database. Exponential backoff with jitter is the fix, and it belongs in the client.
4. Raising `max_connections` requires a restart and makes memory exhaustion the next incident. Put a pooler in front instead, and only after the incident.

## Runaway Query

```sql
SELECT pid, now() - query_start AS runtime, state, left(query, 100)
FROM pg_stat_activity WHERE state = 'active' ORDER BY query_start LIMIT 10;

SELECT pg_cancel_backend(pid);      -- polite: cancels the statement
SELECT pg_terminate_backend(pid);   -- kills the connection, rolls back
```

- Cancel first, terminate second, `kill -9` never (SKILL.md Traps).
- A cancelled long `UPDATE` rolls back, which takes time and produces dead tuples equal to what it wrote. Cancelling at 90% costs almost as much as letting it finish.
- Cancelling a `VACUUM` is safe and resumable. Cancelling `CREATE INDEX CONCURRENTLY` leaves an invalid index to drop (indexing guide).
- Prevention is `statement_timeout` per role, set before the incident (SKILL.md Core Rules 4).

## Accidental DELETE or UPDATE

1. **Still in a transaction?** `ROLLBACK`. This is the entire reason for autocommit-off discipline on production consoles (psql guide).
2. Committed: stop writes to the affected table if you can, and note the wall-clock time immediately — PITR needs a target.
3. Restore the backup to a **scratch instance** at a timestamp a second before the statement, extract the rows, and merge them back. Never restore over the live database: you would trade one table's rows for every write since.
4. If vacuum has not yet run, the old row versions may still be on disk and recoverable with specialist tooling — treat that as a lottery ticket, not a plan, and stop vacuum on that table while you decide.
5. Postmortem action: `default_transaction_read_only` for consoles, RLS or a restricted role for humans, and a review gate on unqualified DML.

## Suspected Corruption

Triggered by: checksum failure messages, "could not read block", a query that crashes a backend reproducibly, or wrong results after a hardware event.

1. **Copy the data directory before touching anything** (or snapshot the volume). Every subsequent action can destroy evidence and options.
2. Verify: `pg_stat_database.checksum_failures`, `amcheck`'s `bt_index_check`, and the kernel log for storage errors. Corruption is nearly always hardware, a filesystem, or a collation change (upgrades guide) — not Postgres.
3. Index-only damage is the good case: `REINDEX` fixes it completely.
4. Heap damage: restore from backup. `zero_damaged_pages = on` discards the damaged pages and their rows — it is a data-loss tool for extracting what remains, used once, on a copy.
5. Turn checksums on afterwards (`pg_checksums --enable`, offline) if they were off. Silent corruption you cannot detect is the worse failure mode.

## After Any Incident

Write down four things: what the first symptom was, which query or view identified the cause, what the fix was, and which alert would have caught it an hour earlier. That last line is the one that changes the next incident — and it usually names a threshold already listed in the monitoring guide.
