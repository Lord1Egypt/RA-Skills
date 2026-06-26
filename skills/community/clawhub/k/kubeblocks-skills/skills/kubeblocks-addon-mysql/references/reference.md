# MySQL Addon Reference

Detailed YAML examples and configurations for the MySQL addon on KubeBlocks v1.0.x.

Source: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster

## ClusterDefinition and Topologies

- **clusterDef:** `mysql`
- **Topologies:** `semisync`, `semisync-proxysql`, `mgr`, `mgr-proxysql`, `orc`, `orc-proxysql`

## Semi-Synchronous Replication (semisync)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-semisync
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

## Semi-Sync with ProxySQL (semisync-proxysql)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-semisync-proxy
  namespace: demo
spec:
  clusterDef: mysql
  topology: semisync-proxysql
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
    - name: proxysql
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

ProxySQL listens on port 6033 and routes read/write queries automatically.

## Group Replication (mgr)

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

MGR requires a minimum of 3 replicas to form a consensus group.

## MGR with ProxySQL (mgr-proxysql)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-mgr-proxy
  namespace: demo
spec:
  clusterDef: mysql
  topology: mgr-proxysql
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
    - name: proxysql
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

## Orchestrator (orc)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-orc
  namespace: demo
spec:
  clusterDef: mysql
  topology: orc
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
    - name: orchestrator
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

Orchestrator provides external topology discovery and automated failover management.

## Orchestrator with ProxySQL (orc-proxysql)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-orc-proxy
  namespace: demo
spec:
  clusterDef: mysql
  topology: orc-proxysql
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
    - name: orchestrator
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
    - name: proxysql
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

## Backup Methods

### XtraBackup

Physical backup using Percona XtraBackup. Fast and efficient for large databases.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: mysql-xtrabackup
  namespace: demo
spec:
  backupMethod: xtrabackup
  backupPolicyName: mysql-cluster-mysql-backup-policy
```

### Volume Snapshot

Uses the storage provider's snapshot capability. Fastest method but requires CSI driver support.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: mysql-snapshot
  namespace: demo
spec:
  backupMethod: volume-snapshot
  backupPolicyName: mysql-cluster-mysql-backup-policy
```

### Binlog Archive (for PITR)

Continuously archives binary logs for point-in-time recovery.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: mysql-binlog
  namespace: demo
spec:
  backupMethod: archive-binlog
  backupPolicyName: mysql-cluster-mysql-backup-policy
```

## Supported Versions

| Version | serviceVersion | Notes |
|---|---|---|
| MySQL 5.7 | `5.7.44` | Legacy support |
| MySQL 8.0 | `8.0.33` | Stable |
| MySQL 8.0 | `8.0.35` | Latest 8.0, recommended |
| MySQL 8.4 | `8.4.2` | Innovation release |

## Connection Details

| Property | Value |
|---|---|
| Port | 3306 |
| ProxySQL Port | 6033 |
| Root Secret | `<cluster>-mysql-account-root` |
| Secret Keys | `username`, `password` |

## Termination Policies

| Policy | Behavior |
|---|---|
| `DoNotTerminate` | Block deletion |
| `Halt` | Delete workloads, keep PVCs and secrets |
| `Delete` | Delete workloads and PVCs, keep backups |
| `WipeOut` | Delete everything including backups |

## Documentation Links

- Create Cluster: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster
- Scaling: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-for-a-mysql-cluster
- Backup & Restore: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/backup-and-restore/backup
