---
name: kubeblocks-addon-mysql
metadata:
  version: "0.1.0"
description: Deploy and manage MySQL clusters on KubeBlocks with topology selection guidance. Covers semi-synchronous replication, MySQL Group Replication (MGR), Orchestrator-managed HA, and optional ProxySQL load balancing. Use when the user mentions MySQL, MariaDB, or explicitly wants to create a MySQL database cluster. Provides engine-specific topology comparison, best-practice defaults, and connection methods. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, backup, etc.), use the corresponding operation skill.
---

# Deploy MySQL on KubeBlocks

## Overview

Deploy highly-available MySQL clusters using KubeBlocks. Multiple topologies are available — from simple semi-synchronous replication to full orchestrator-managed setups with ProxySQL.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The MySQL addon must be enabled:

```bash
# Check if mysql addon is installed
helm list -n kb-system | grep mysql

# Install if missing
helm install kb-addon-mysql kubeblocks/mysql --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | Value | Components | Use Case |
|---|---|---|---|
| Semi-Synchronous | `semisync` | mysql | Standard HA, 2+ replicas |
| Semi-Sync + ProxySQL | `semisync-proxysql` | mysql + proxysql | HA with query routing |
| Group Replication | `mgr` | mysql | Multi-primary capable, 3+ replicas |
| MGR + ProxySQL | `mgr-proxysql` | mysql + proxysql | MGR with load balancing |
| Orchestrator | `orc` | mysql + orchestrator | External HA manager |
| Orc + ProxySQL | `orc-proxysql` | mysql + orc + proxysql | Full HA stack |

**Default recommendation:** `semisync` — simplest, most widely deployed.

## Supported Versions

| Version | serviceVersion |
|---|---|
| MySQL 5.7 | `5.7.44` |
| MySQL 8.0 | `8.0.33`, `8.0.35` |
| MySQL 8.4 | `8.4.2` |

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to MySQL
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep mysql
```

If not found, install it:

```bash
helm install kb-addon-mysql kubeblocks/mysql --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Semi-Synchronous Replication (Recommended)

This is the most common topology. One primary + one or more replicas with semi-sync replication for data safety.

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-cluster
  namespace: demo
spec:
  clusterDef: mysql
  topology: semisync
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.35"
      replicas: 2
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
kubectl apply -f mysql-cluster.yaml
```

### Group Replication (MGR)

Multi-primary capable. Requires 3+ replicas:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-mgr
  namespace: demo
spec:
  clusterDef: mysql
  topology: mgr
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.35"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

For topologies with ProxySQL or Orchestrator, see [reference.md](references/reference.md).

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster mysql-cluster -w
```

Wait until `STATUS` shows `Running`. Typical startup time: 1-3 minutes.

Check component status:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=mysql-cluster
```

## Step 5: Connect to MySQL

### Get Credentials

The root password is stored in a Kubernetes secret:

```bash
# Secret name format: <cluster>-mysql-account-root
kubectl -n demo get secret mysql-cluster-mysql-account-root -o jsonpath='{.data.password}' | base64 -d
```

### Connect via kubectl exec

```bash
kubectl -n demo exec -it mysql-cluster-mysql-0 -- bash -c 'mysql -uroot -p"$(cat /etc/mysql/secret/password)"'
```

### Connect via Port-Forward

```bash
kubectl -n demo port-forward svc/mysql-cluster-mysql 3306:3306
# Then from another terminal:
mysql -h 127.0.0.1 -P 3306 -u root -p
```

## Backup

MySQL supports three backup methods:

| Method | ActionSet | Use Case |
|---|---|---|
| XtraBackup | `xtrabackup` | Physical backup, fast for large DBs |
| Volume Snapshot | `mysql-volumesnapshot` | Storage-level snapshots, fastest |
| Binlog Archive | `archive-binlog` | Continuous archiving for PITR |

Example backup:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: mysql-backup
  namespace: demo
spec:
  backupMethod: xtrabackup
  backupPolicyName: mysql-cluster-mysql-backup-policy
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster mysql-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod CrashLoopBackOff:**
```bash
kubectl -n demo logs mysql-cluster-mysql-0
```

**Semi-sync replica not connecting:**
- Ensure `replicas >= 2` for semisync topology
- Check network policies between pods

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/stop-start-restart-a-mysql-cluster) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-for-a-mysql-cluster) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-for-a-mysql-cluster) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/expand-volume-of-a-mysql-cluster) |
| Change parameters | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/configuration/configure-cluster-parameters) |
| Switchover primary | [switchover](../kubeblocks-switchover/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/switchover) |
| Upgrade engine version | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/upgrade) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/expose-mysql) |
| Backup | [backup](../kubeblocks-backup/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/backup-and-restore/backup) |
| Restore | [restore](../kubeblocks-restore/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/backup-and-restore/restore) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.

## Next Steps

- For detailed YAML examples of all topologies, see [reference.md](references/reference.md)
