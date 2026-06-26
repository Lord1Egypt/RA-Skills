# Restore Reference

## Table of Contents

- [Addon-Specific Restore Behaviors](#addon-specific-restore-behaviors)
- [PITR Time Range Details](#pitr-time-range-details)
- [Restore Annotation Schema](#restore-annotation-schema)
- [Volume Restore Policies](#volume-restore-policies)

## Addon-Specific Restore Behaviors

### MySQL

- Full backup method: `xtrabackup`
- Continuous backup method: `archive-binlog` (streams binlogs to BackupRepo)
- PITR supported: Yes — requires both a completed xtrabackup and a running archive-binlog backup
- Restore creates a new cluster; the restored MySQL instance replays binlogs to reach the target timestamp
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/05-backup-restore/05-restoring-from-full-backup
- PITR docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/05-backup-restore/06-restore-with-pitr

### PostgreSQL

- Full backup method: `pg-basebackup`
- Continuous backup method: `wal-archive` (streams WAL segments)
- PITR supported: Yes — requires both a completed pg-basebackup and a running wal-archive backup
- The restored PostgreSQL instance uses `recovery_target_time` in the recovery configuration
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/05-backup-restore/05-restoring-from-full-backup
- PITR docs: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/05-backup-restore/06-restore-with-pitr

### Redis

- Full backup method: `datafile` (RDB dump)
- Continuous backup method: not available for Redis in KubeBlocks
- PITR supported: Limited — Redis PITR depends on AOF if configured; KubeBlocks primarily supports full restores
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-redis/05-backup-restore/05-restoring-from-full-backup

### MongoDB

- Full backup method: `datafile`
- Continuous backup method: not available in standard KubeBlocks MongoDB addon
- PITR supported: No (full restore only)
- For replica set restore, the new cluster re-initializes replication from the restored data

### Qdrant

- Full backup method: `datafile`
- PITR supported: No
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/05-restoring-from-full-backup

## PITR Time Range Details

The recoverable time window for PITR is determined by:

1. **Start time**: the completion timestamp of the earliest full backup
2. **End time**: the latest timestamp in the continuous backup's log stream

To find the valid time range:

```bash
# Check continuous backup status
kubectl describe backup <continuous-backup-name> -n <ns>
```

Look for `status.timeRange`:

```yaml
status:
  timeRange:
    start: "2025-01-01T00:00:00Z"
    end: "2025-01-15T14:30:00Z"
```

The `restoreTime` in the restore annotation must fall within `[start, end]`.

If the continuous backup has been running for a while but no full backup exists, PITR is not possible — you need at least one completed full backup as the base.

## Restore Annotation Schema

The restore annotation `kubeblocks.io/restore-from-backup` is a JSON string with this structure:

```json
{
  "<component-name>": {
    "name": "<backup-name>",
    "namespace": "<backup-namespace>",
    "volumeRestorePolicy": "Parallel|Serial",
    "restoreTime": "2025-01-01T12:00:00Z"
  }
}
```

| Field | Required | Description |
|---|---|---|
| `name` | Yes | Name of the Backup CR to restore from |
| `namespace` | Yes | Namespace where the Backup CR lives |
| `volumeRestorePolicy` | No | `Parallel` (default) or `Serial` |
| `restoreTime` | No | RFC 3339 UTC timestamp for PITR; omit for full restore |

Multiple components can be restored simultaneously by adding multiple keys.

## Volume Restore Policies

| Policy | Behavior | When to use |
|---|---|---|
| `Parallel` | Restores all PVCs simultaneously | Default; faster for most cases |
| `Serial` | Restores PVCs one at a time | Use when storage backend has IOPS limits or when restoring very large volumes |

General reference: https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/restore/restore-data-from-backup-set
