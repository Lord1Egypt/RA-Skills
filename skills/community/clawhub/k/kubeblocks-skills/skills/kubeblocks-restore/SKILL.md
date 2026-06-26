---
name: kubeblocks-restore
metadata:
  version: "0.1.0"
description: Restore KubeBlocks database clusters from backups. Supports full restore (create new cluster from backup) and Point-in-Time Recovery (PITR) to a specific timestamp. Use when the user wants to restore, recover, rebuild, or roll back a database cluster from a backup. Requires an existing backup created by the backup skill. NOT for creating backups (see kubeblocks-backup skill) or for creating a brand new cluster without backup data (see kubeblocks-create-cluster).
---

# Restore KubeBlocks Database Clusters

## Overview

KubeBlocks supports restoring database clusters from backups. A restore always creates a **new cluster** from an existing backup — it does not modify the original cluster in-place. This design is intentional: by creating a new cluster, you can verify the restored data before switching traffic, and the original cluster remains available as a fallback.

Two restore modes are available:

- **Full restore**: Restore from a completed full backup to get the exact state at backup time. Use this when you need to recover from a catastrophic failure, clone a cluster for testing, or roll back after a failed upgrade.
- **PITR (Point-in-Time Recovery)**: Restore to any specific timestamp between a full backup and the latest continuous backup. Essential for recovering from accidental data corruption (e.g., a wrong `DELETE` or `DROP TABLE`) where you need to rewind to the moment just before the mistake.

Official docs: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/recovery

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running (if restoring to supplement an existing cluster)
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Verify backups are available for restore:

```bash
kubectl get backup -n <namespace>
```

## Workflow

```
- [ ] Step 1: List available backups
- [ ] Step 2: Create a new cluster with restore annotation or OpsRequest
- [ ] Step 3: Verify restored cluster
```

## Step 1: List Available Backups

```bash
kubectl get backup -n <ns>
```

Example output:

```
NAME                  POLICY                              METHOD         STATUS      AGE
mycluster-full        mycluster-mysql-backup-policy        xtrabackup    Completed   2d
mycluster-continuous  mycluster-mysql-backup-policy        archive-binlog Running     2d
```

Check backup details for restore information:

```bash
kubectl describe backup <backup-name> -n <ns>
```

For PITR, note the time range available from the continuous backup's status.

## Step 2: Restore

### Option A: Full Restore via Cluster Annotation

Create a new Cluster CR with the restore annotation. The new cluster spec should match the original cluster's configuration (same component types, resource requests, etc.):

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <new-cluster>
  namespace: <ns>
  annotations:
    kubeblocks.io/restore-from-backup: '{"<component>":{"name":"<backup-name>","namespace":"<ns>","volumeRestorePolicy":"Parallel"}}'
spec:
  # ... same spec as original cluster ...
```

The `volumeRestorePolicy` options:
- `Parallel` — restore all volumes simultaneously (faster)
- `Serial` — restore volumes one at a time

Before applying, validate with dry-run:

```bash
kubectl apply -f restored-cluster.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f restored-cluster.yaml
kubectl get cluster <new-cluster> -n <ns> -w
```

> **Success condition:** `.status.phase` = `Running` | **Typical:** 2-5min | **If stuck >10min:** `kubectl describe cluster <new-cluster> -n <ns>`

### Option B: Full Restore via OpsRequest

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <new-cluster>-restore-ops
  namespace: <ns>
spec:
  clusterName: <new-cluster>
  type: Restore
  restore:
    backupName: <backup-name>
    backupNamespace: <ns>
```

Before applying, validate with dry-run:

```bash
kubectl apply -f restore-ops.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f restore-ops.yaml
kubectl get ops <new-cluster>-restore-ops -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 2-5min | **If stuck >10min:** `kubectl describe ops <new-cluster>-restore-ops -n <ns>`

### Option C: PITR Restore (Point-in-Time Recovery)

PITR requires **both** a completed full backup **and** a running continuous backup (archive-binlog for MySQL, wal-archive for PostgreSQL).

Use the annotation method with an additional `restoreTime` field:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <new-cluster>
  namespace: <ns>
  annotations:
    kubeblocks.io/restore-from-backup: '{"<component>":{"name":"<continuous-backup>","namespace":"<ns>","volumeRestorePolicy":"Parallel","restoreTime":"2025-01-01T12:00:00Z"}}'
spec:
  # ... same spec as original cluster ...
```

Key points for PITR:
- `name` should reference the **continuous backup** (not the full backup)
- `restoreTime` must be in RFC 3339 format (UTC): `YYYY-MM-DDTHH:MM:SSZ`
- The restore time must fall within the range covered by the full + continuous backups

### Finding the Valid PITR Time Range

```bash
kubectl describe backup <continuous-backup-name> -n <ns>
```

Look for `status.timeRange` which shows the recoverable time window.

## Step 3: Verify Restored Cluster

```bash
# Watch cluster status
kubectl get cluster <new-cluster> -n <ns> -w
```

> **Success condition:** `.status.phase` = `Running` | **Typical:** 2-5min | **If stuck >10min:** `kubectl describe cluster <new-cluster> -n <ns>`

```bash
# Check pods are running
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<new-cluster>
```

The cluster status should transition to `Running`. Verify data integrity by connecting to the database:

```bash
# Get connection credentials
kubectl get secrets -n <ns> <new-cluster>-<component>-account-root -o jsonpath='{.data.password}' | base64 -d
```

## Troubleshooting

**Restore stuck in Creating:**
- Check backup status is `Completed` (for full) or `Running` (for continuous)
- Verify BackupRepo is accessible: `kubectl get backuprepo`
- Check restore job logs: `kubectl get pods -n <ns> -l app.kubernetes.io/name=restore`

**PITR restore fails:**
- Ensure both full and continuous backups exist
- Verify the `restoreTime` is within the valid time range
- Confirm the continuous backup is still running

**New cluster spec mismatch:**
- The restored cluster spec should match the original (same component definitions, storage size)
- Storage size in the new cluster must be >= the original backup's data size

## Additional Reference

For addon-specific restore behaviors (MySQL/PostgreSQL/Redis/MongoDB), PITR time range calculation details, the full restore annotation schema, and volume restore policy comparison, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
