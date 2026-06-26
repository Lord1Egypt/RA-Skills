---
name: kubeblocks-rebuild-replica
metadata:
  version: "0.1.0"
description: Rebuild a failed replica in MySQL or PostgreSQL clusters managed by KubeBlocks. Use when a replica's data is corrupted, the pod is in CrashLoopBackOff, replication is broken, or you need to recover or repair a secondary instance. NOT for planned switchover (see switchover) or full cluster restore (see restore).
---

# Rebuild Failed Replica

## Overview

Rebuild replica recovers a failed secondary instance by recreating its data from the primary or from a backup. Use this when:

- Replica pod is in **CrashLoopBackOff** or unrecoverable
- **Data corruption** on the replica (storage/volume issues)
- Replication lag is irrecoverable or replication slot is corrupted
- Replica cannot rejoin the replication group

Supported engines: **MySQL** (ApeCloud MySQL) and **PostgreSQL** only — engines with primary-secondary replication.

Official docs: [MySQL](https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/11-rebuild-replica) | [PostgreSQL](https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/11-rebuild-replica)

## Workflow

```
- [ ] Step 1: Identify the failed replica
- [ ] Step 2: Choose rebuild source (from primary vs from backup)
- [ ] Step 3: Apply RebuildInstance OpsRequest (dry-run then apply)
- [ ] Step 4: Monitor and verify
```

## Step 1: Identify the Failed Replica

Check pod status and roles:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Identify the pod that is `CrashLoopBackOff`, `Error`, or has `secondary` role but is unhealthy. Note the component name (e.g. `mysql`, `postgresql`) from the Cluster spec.

## Step 2: Choose Rebuild Source

| Source | When to use |
|--------|-------------|
| **From primary** | Primary is healthy; fastest option. Omit `backupName`. |
| **From backup** | Primary unavailable or you need a specific point-in-time. Set `backupName`. |

List backups (if rebuilding from backup):

```bash
kubectl get backup -n <ns> -l app.kubernetes.io/instance=<cluster>
```

## Step 3: Apply RebuildInstance OpsRequest

### Rebuild from Primary

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: rebuild-<cluster>-<pod>
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: RebuildInstance
  rebuildFrom:
    - componentName: <component>
      instances:
        - name: <failed-pod-name>
```

### Rebuild from Backup

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: rebuild-<cluster>-<pod>
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: RebuildInstance
  rebuildFrom:
    - componentName: <component>
      backupName: <backup-name>
      instances:
        - name: <failed-pod-name>
```

Optional: `inPlace: true` keeps the same pod name and recreates PVC; omit or `false` for non-in-place (new pod, then old one removed). Add `force: true` if preconditions block the operation.

Dry-run first:

```bash
kubectl apply -f rebuild-ops.yaml --dry-run=server
```

If dry-run succeeds, apply:

```bash
kubectl apply -f rebuild-ops.yaml
kubectl get ops rebuild-<cluster>-<pod> -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 5–15 min | **If stuck >20 min:** `kubectl describe ops <name> -n <ns>`

Status progresses: `Pending` → `Running` → `Succeed`

## Step 4: Verify

Confirm the replica pod is Running and has the `secondary` role:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.status.phase}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Verify replication:

```bash
# MySQL
kubectl exec -it <replica-pod> -n <ns> -- mysql -u root -p<password> -e "SHOW REPLICA STATUS\G"

# PostgreSQL
kubectl exec -it <primary-pod> -n <ns> -- psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

## Troubleshooting

**OpsRequest fails or stays Pending:**
- Ensure cluster is `Running` and no other OpsRequest is in progress
- For backup source: verify `backupName` exists and is `Completed`
- Check `kubectl describe ops <name> -n <ns>` for events

**Replica still unhealthy after rebuild:**
- Inspect pod logs: `kubectl logs <pod> -n <ns> --tail=100`
- Verify primary is healthy and reachable from the replica

**Non-in-place: pod name changed:**
- Expected: old pod is replaced by a new one (e.g. `mysql-0` → `mysql-2`). The cluster keeps the same replica count.

## Additional Reference

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
