# Backup and Restore — The Only Test That Counts Is a Restore

Two families. **Logical** (`pg_dump`) produces a portable, per-object, per-database snapshot. **Physical** (base backup + WAL) copies the cluster's files and replays WAL, which is what point-in-time recovery needs. A serious setup has both: physical for RTO, logical for "someone dropped one table".

## Logical Dumps

```bash
pg_dump -Fd -j 8 -f /backup/app_dir app        # directory format, parallel dump
pg_dump -Fc -f /backup/app.dump app            # custom format, single file, selective restore
pg_dumpall --globals-only -f /backup/globals.sql   # roles, tablespaces — pg_dump has neither
```

- Format matters: `-Fp` (plain SQL) restores only with psql, all or nothing. `-Fc` and `-Fd` restore with `pg_restore`, allow `-j` parallel restore and selective object restore. Only `-Fd` supports parallel *dump*.
- A dump is one consistent snapshot, which means it holds a transaction open for its entire duration: on a busy database a two-hour dump is a two-hour vacuum horizon (see the horizon checks in the vacuum guide). Dump from a replica when the database is large.
- `pg_dump` takes ACCESS SHARE on every table — it blocks nothing except DDL, and DDL blocks it.
- Always dump with the `pg_dump` binary of the **higher** version when the two differ. Newer server plus older `pg_dump` fails or produces subtly wrong output; the reverse is supported.
- Restore ordering: `pg_restore -j 8 --no-owner --no-privileges -d newdb app.dump`. Indexes and constraints are built after data by design — a restore that seems stuck at 90% is building indexes, and `maintenance_work_mem` is the knob.
- Restore into a *new* database, never over a live one. `--clean --if-exists` on the wrong target is an outage with a dump-shaped alibi.

## Physical Backups and PITR

```bash
pg_basebackup -D /backup/base -Ft -z -Xs -P -c fast
```

The three pieces of PITR:

1. **A base backup** (`pg_basebackup`, pgBackRest, WAL-G, or a filesystem snapshot taken between `pg_backup_start()`/`pg_backup_stop()`).
2. **Continuous WAL archiving** — `archive_mode = on` with an `archive_command` (or `archive_library`, PostgreSQL >=15) that returns non-zero on failure. A command that silently succeeds while writing nothing is the most dangerous line in `postgresql.conf`: backups look green for months.
3. **A recovery target** — restore the base, then in `postgresql.conf` set `restore_command` plus `recovery_target_time = '2026-07-24 14:32:00+00'` (or `recovery_target_lsn`, `_xid`, `_name`), create `recovery.signal`, start the server. `recovery_target_action = 'pause'` lets you inspect before promoting.

- WAL archiving failure fills `pg_wal` until the disk is full and the cluster stops. Alert on `pg_stat_archiver.last_failed_time` and on the gap between `last_archived_wal` and current WAL — this is one of the top causes of a "database down, disk full" page.
- Incremental base backups exist from PostgreSQL 17 (`pg_basebackup --incremental` plus `pg_combinebackup`); before that, use pgBackRest or WAL-G for incrementals and retention.
- Retention has to cover your worst detection lag, not your worst crash: logical corruption discovered on day 9 needs a day-10 retention window.

## Choosing Per Failure Mode

| Failure | What saves you |
|---|---|
| Disk or node loss | Physical backup + WAL, or a standby promoted (a standby is HA, not a backup) |
| `DROP TABLE` in production | PITR to one second before, restored to a scratch instance; copy the table back |
| `UPDATE` without `WHERE`, noticed later | PITR to a scratch instance, then reconcile rows — the live database keeps serving |
| Slow logical corruption (bad code writing bad data) | Logical dumps with long retention; PITR only helps if you can name the moment |
| Provider account or region loss | A copy outside that provider. Snapshots inside the account die with the account |
| Ransomware / malicious operator | Immutable or write-once storage for archives; credentials that can write but not delete |
| Anything else | Restore drill first, theory second |

A replica is not a backup: `DROP TABLE` replicates in milliseconds. Delayed replicas (`recovery_min_apply_delay = '1h'`) buy an hour of human reaction time and are a genuinely cheap safety net.

## The Restore Drill

The measurement that turns a backup into a guarantee (SKILL.md Core Rules 8):

1. Provision a scratch instance from the latest backup, on the same major version.
2. Time it end to end. That number is your real RTO — most teams discover it is 4x their assumption.
3. Verify: row counts on the five biggest tables, the newest timestamp in the busiest table (that gap is your real RPO), `pg_stat_user_tables` sanity, and one application-level query.
4. Run `ANALYZE` (planner statistics do not survive a logical restore, and before PostgreSQL 18 they do not survive `pg_upgrade` either).
5. Record date, duration, size, and version in a log. Repeat on a fixed cadence (`Cadence` preference area in SKILL.md Configuration).

Restore drills also catch the silent killers: missing globals (roles), extensions absent on the target, tablespace paths that do not exist, and dumps taken with an old `pg_dump`.

## Partial and Table-Level Recovery

- Single table from a custom-format dump: `pg_restore -t orders -d target app.dump`. It does not bring FK dependencies or the sequence — check both.
- Single table from PITR: restore the whole cluster to a scratch instance, then `COPY` the table out and back. There is no per-table PITR.
- Row-level oops inside an open transaction: `ROLLBACK` is the whole answer, which is why psql habits (`\set AUTOCOMMIT off` for destructive work) matter more than any tool.
- Extracting objects from a plain SQL dump without restoring it: `pg_restore -l` on a custom dump gives a table of contents you can edit and feed back with `-L`. A plain dump requires text surgery — another reason not to use `-Fp` for anything large.

## Verification You Can Automate

- Checksum the restore: compare `count(*)` and `max(id)` per table between source and restored copy, scripted, as the last step of the drill.
- Enable data checksums at `initdb` (or `pg_checksums --enable` offline). They turn silent bit rot into a loud error, and `pg_stat_database.checksum_failures` is then worth alerting on.
- `amcheck` (`bt_index_check`) verifies index structure against the heap; run it after any hardware incident or storage migration.
