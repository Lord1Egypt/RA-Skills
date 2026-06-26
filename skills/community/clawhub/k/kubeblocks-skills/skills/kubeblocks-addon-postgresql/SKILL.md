---
name: kubeblocks-addon-postgresql
metadata:
  version: "0.1.0"
description: Deploy and manage PostgreSQL clusters on KubeBlocks with Patroni-based high availability and automatic failover. Provides Spilo image configuration, replication topology, and connection methods. Use when the user mentions PostgreSQL, Postgres, PG, or explicitly wants to create a PostgreSQL database cluster. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, backup, parameter tuning, etc.), use the corresponding operation skill.
---

# Deploy PostgreSQL on KubeBlocks

## Overview

Deploy highly-available PostgreSQL clusters using KubeBlocks. Uses the Spilo image with Patroni for automatic leader election and failover.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/create-and-connect-a-postgresql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The PostgreSQL addon must be enabled:

```bash
# Check if postgresql addon is installed
helm list -n kb-system | grep postgresql

# Install if missing
helm install kb-addon-postgresql kubeblocks/postgresql --namespace kb-system --version 1.0.0
```

## Cluster Architecture

- **clusterDef:** `postgresql`
- **topology:** `replication`
- **HA Engine:** Patroni (embedded in Spilo image)
- **Components:** `postgresql` (primary + read replicas)

Patroni handles automatic leader election, failover, and replica management. A primary is elected among replicas, and streaming replication keeps replicas in sync.

## Supported Versions

| Major Version | serviceVersion Examples |
|---|---|
| PostgreSQL 12 | `12.14.0`, `12.14.1`, `12.15.0` |
| PostgreSQL 14 | `14.7.2`, `14.8.0` |
| PostgreSQL 15 | `15.7.0` |
| PostgreSQL 16 | `16.4.0` |
| PostgreSQL 17 | `17.4.0` |
| PostgreSQL 18 | `18.0.0` |

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to PostgreSQL
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep postgresql
```

If not found, install it:

```bash
helm install kb-addon-postgresql kubeblocks/postgresql --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Replication Cluster (Standard)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-cluster
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.7.2"
      replicas: 2
      disableExporter: false
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

Apply:

```bash
kubectl apply -f pg-cluster.yaml
```

**Key fields:**
- `disableExporter: false` — enables the metrics exporter sidecar for monitoring
- `replicas: 2` — one primary + one streaming replica (Patroni elects the leader)

### Production Configuration

For production, increase resources and replicas:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-production
  namespace: demo
spec:
  clusterDef: postgresql
  topology: replication
  terminationPolicy: Halt
  componentSpecs:
    - name: postgresql
      serviceVersion: "16.4.0"
      replicas: 3
      disableExporter: false
      resources:
        limits: {cpu: "2", memory: "4Gi"}
        requests: {cpu: "2", memory: "4Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 100Gi}}
```

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster pg-cluster -w
```

Wait until `STATUS` shows `Running`. Typical startup time: 1-3 minutes.

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=pg-cluster
```

## Step 5: Connect to PostgreSQL

### Get Credentials

```bash
# Secret name format: <cluster>-postgresql-account-postgres
kubectl -n demo get secret pg-cluster-postgresql-account-postgres -o jsonpath='{.data.password}' | base64 -d
```

### Connect via kubectl exec

```bash
kubectl -n demo exec -it pg-cluster-postgresql-0 -- bash -c 'psql -U postgres'
```

### Connect via Port-Forward

```bash
kubectl -n demo port-forward svc/pg-cluster-postgresql 5432:5432
# Then from another terminal:
psql -h 127.0.0.1 -p 5432 -U postgres
```

## Backup

PostgreSQL supports three backup methods:

| Method | ActionSet | Use Case |
|---|---|---|
| pg-basebackup | `pg-basebackup` | Logical base backup |
| Volume Snapshot | `postgresql-volumesnapshot` | Storage-level snapshots, fastest |
| WAL Archive | `wal-archive` | Continuous archiving for PITR |

Example backup:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: pg-backup
  namespace: demo
spec:
  backupMethod: pg-basebackup
  backupPolicyName: pg-cluster-postgresql-backup-policy
```

For point-in-time recovery (PITR), enable WAL archiving first, then restore to a specific timestamp.

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster pg-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Patroni issues:**
```bash
# Check Patroni status
kubectl -n demo exec -it pg-cluster-postgresql-0 -- patronictl list
```

**Replication lag:**
```bash
kubectl -n demo exec -it pg-cluster-postgresql-0 -- psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/stop-start-restart-a-postgresql-cluster) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/scale-for-a-postgresql-cluster) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/scale-for-a-postgresql-cluster) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/expand-volume-of-a-postgresql-cluster) |
| Change parameters | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/configuration/configure-cluster-parameters) |
| Switchover primary | [switchover](../kubeblocks-switchover/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/switchover) |
| Upgrade engine version | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/upgrade) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/expose-postgresql) |
| Backup | [backup](../kubeblocks-backup/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/backup-and-restore/backup) |
| Restore | [restore](../kubeblocks-restore/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/backup-and-restore/restore) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.

## Next Steps

- For detailed YAML examples and the vanilla-postgresql variant, see [reference.md](references/reference.md)
