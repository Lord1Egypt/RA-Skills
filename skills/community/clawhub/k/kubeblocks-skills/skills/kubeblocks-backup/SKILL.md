---
name: kubeblocks-backup
metadata:
  version: "0.1.0"
description: Create backups for KubeBlocks database clusters. Supports on-demand full backups, scheduled (cron-based) backups, and continuous backups for Point-in-Time Recovery (PITR). Covers BackupRepo configuration for S3, GCS, Azure Blob, and MinIO. Use when the user wants to backup, snapshot, protect, or archive database data. NOT for restoring from backups (see restore skill) or managing backup storage infrastructure (see BackupRepo docs).
---

# Backup KubeBlocks Database Clusters

## Overview

KubeBlocks provides data protection through full backups, scheduled backups, and continuous backups (for Point-in-Time Recovery). Backups are managed via the `Backup` CR or `OpsRequest` CR, and stored in a configured `BackupRepo`.

Official docs: https://kubeblocks.io/docs/preview/user_docs/concepts/backup-and-restore/introduction

## Backup Methods by Addon

| Addon      | Physical Backup Method | Snapshot Method     | Continuous (PITR)   |
|------------|----------------------|---------------------|---------------------|
| MySQL      | xtrabackup           | volume-snapshot     | archive-binlog      |
| PostgreSQL | pg-basebackup        | volume-snapshot     | wal-archive         |
| Redis      | datafile             | volume-snapshot     | —                   |
| MongoDB    | datafile             | volume-snapshot     | —                   |

### Choosing a Backup Method

- **Physical backup** (xtrabackup, pg-basebackup, datafile): Portable and self-contained — the backup is a complete copy of the data files stored in BackupRepo. Works on any storage backend. Recommended as the default because it has no infrastructure dependencies beyond BackupRepo.
- **Volume snapshot**: Leverages the storage layer's native snapshot capability (via CSI). Extremely fast for large databases since it's a copy-on-write operation, but requires a VolumeSnapshotClass and a CSI driver that supports snapshots — not always available, especially in local/dev environments.
- **Continuous backup** (archive-binlog, wal-archive): Streams transaction logs in real time to enable Point-in-Time Recovery (PITR). Essential for production workloads where you need to recover to any arbitrary point in time, not just the moment of the last full backup.

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

## Workflow

```
- [ ] Step 1: Ensure BackupRepo exists
- [ ] Step 2: Check BackupPolicy for the cluster
- [ ] Step 3: Create backup (on-demand or scheduled)
- [ ] Step 4: Verify backup
```

## Step 1: Ensure BackupRepo Exists

A `BackupRepo` defines where backups are stored (S3, OSS, MinIO, GCS, etc.). At least one must be configured before creating backups.

```bash
kubectl get backuprepo
```

If no BackupRepo exists, see [reference.md](references/reference.md) for setup instructions with various storage providers.

## Step 2: Check BackupPolicy

Each cluster automatically gets a `BackupPolicy` when KubeBlocks creates it. Verify it exists:

```bash
kubectl get backuppolicy -n <ns>
```

The default naming convention is `<cluster>-<component>-backup-policy`. The BackupPolicy defines available backup methods and their configurations.

## Step 3: Create a Backup

### Option A: On-Demand Backup via OpsRequest

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-backup-ops
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Backup
  backup:
    backupPolicyName: <cluster>-<component>-backup-policy
    backupMethod: <method>    # xtrabackup / volume-snapshot / pg-basebackup etc.
    deletionPolicy: Delete
    retentionPeriod: 7d
```

Before applying, validate with dry-run:

```bash
kubectl apply -f backup-ops.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f backup-ops.yaml
kubectl get ops <cluster>-backup-ops -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** varies | **If stuck >30min:** `kubectl describe ops <cluster>-backup-ops -n <ns>`

### Option B: On-Demand Backup via Backup CR

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <backup-name>
  namespace: <ns>
spec:
  backupMethod: <method>
  backupPolicyName: <policy-name>
  deletionPolicy: Delete
```

Before applying, validate with dry-run:

```bash
kubectl apply -f backup.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f backup.yaml
kubectl get backup <backup-name> -n <ns> -w
```

> **Success condition:** Full backup: `.status.phase` = `Completed` | **Typical:** varies | **If stuck >30min:** `kubectl describe backup <backup-name> -n <ns>` — Continuous backup: `.status.phase` = `Running` | **Typical:** 1min | **If stuck >5min:** `kubectl describe backup <backup-name> -n <ns>`

### Option C: Scheduled Backup (Cluster CR)

Add a `backup` section to the Cluster CR spec:

```yaml
spec:
  backup:
    enabled: true
    retentionPeriod: 30d
    method: xtrabackup
    cronExpression: "0 0 * * *"
    repoName: <repo-name>
```

Common cron expressions:
- `"0 0 * * *"` — daily at midnight
- `"0 2 * * 0"` — weekly on Sunday at 2 AM
- `"0 */6 * * *"` — every 6 hours

### Option D: Continuous Backup for PITR

Continuous backups stream transaction logs (binlogs/WAL) to enable point-in-time recovery. Create a Backup CR with the continuous method:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: <cluster>-continuous
  namespace: <ns>
spec:
  backupMethod: archive-binlog    # MySQL; use wal-archive for PostgreSQL
  backupPolicyName: <cluster>-<component>-backup-policy
  deletionPolicy: Delete
```

For PITR to work, you need **both** a completed full backup **and** a running continuous backup.

## Step 4: Verify Backup

```bash
kubectl get backup -n <ns>
```

Expected output shows `Completed` status:

```
NAME              POLICY                              METHOD        STATUS      AGE
my-backup         mycluster-mysql-backup-policy        xtrabackup   Completed   5m
```

Check backup details:

```bash
kubectl describe backup <backup-name> -n <ns>
```

## Troubleshooting

**Backup stuck in InProgress:**
- Check BackupRepo connectivity: `kubectl describe backuprepo`
- Check backup pod logs: `kubectl logs -n <ns> -l app.kubernetes.io/name=backup`

**BackupPolicy not found:**
- Ensure the cluster is running: `kubectl get cluster -n <ns>`
- BackupPolicy is auto-created with the cluster; check addon installation

**Volume-snapshot backup fails:**
- Ensure a VolumeSnapshotClass exists: `kubectl get volumesnapshotclass`
- CSI driver must support volume snapshots

## Additional Reference

For BackupRepo setup (S3, OSS, MinIO, GCS), continuous backup configuration, and advanced BackupPolicy customization, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
