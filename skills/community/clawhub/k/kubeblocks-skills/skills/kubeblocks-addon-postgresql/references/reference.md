# PostgreSQL Addon Reference

Detailed YAML examples and configurations for the PostgreSQL addon on KubeBlocks v1.0.x.

Source: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/create-and-connect-a-postgresql-cluster

## ClusterDefinition and Topology

- **clusterDef:** `postgresql`
- **Topology:** `replication`

The PostgreSQL addon uses Patroni (via the Spilo image) for high availability. All pods run the same PostgreSQL + Patroni stack; Patroni elects a leader and manages streaming replication.

## Replication Cluster

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

## Vanilla PostgreSQL Variant

KubeBlocks also provides a vanilla PostgreSQL (without Patroni/Spilo) as a separate addon. This is useful for simpler single-instance deployments where HA is not needed.

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-vanilla
  namespace: demo
spec:
  clusterDef: vanilla-postgresql
  topology: standalone
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.7.2"
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

The vanilla-postgresql addon uses the official PostgreSQL image without Patroni.

## Supported Versions

| Major Version | serviceVersion | Notes |
|---|---|---|
| PostgreSQL 12 | `12.14.0` | Legacy |
| PostgreSQL 12 | `12.14.1` | Legacy, patch |
| PostgreSQL 12 | `12.15.0` | Legacy |
| PostgreSQL 14 | `14.7.2` | Stable, widely used |
| PostgreSQL 14 | `14.8.0` | Stable |
| PostgreSQL 15 | `15.7.0` | Current |
| PostgreSQL 16 | `16.4.0` | Current |
| PostgreSQL 17 | `17.4.0` | Latest stable |
| PostgreSQL 18 | `18.0.0` | Latest |

## Backup Methods

### pg-basebackup

Standard PostgreSQL base backup tool. Creates a full backup.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: pg-basebackup
  namespace: demo
spec:
  backupMethod: pg-basebackup
  backupPolicyName: pg-cluster-postgresql-backup-policy
```

### Volume Snapshot

Uses the storage provider's snapshot capability. Requires CSI snapshot support.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: pg-snapshot
  namespace: demo
spec:
  backupMethod: volume-snapshot
  backupPolicyName: pg-cluster-postgresql-backup-policy
```

### WAL Archive (for PITR)

Continuously archives WAL (Write-Ahead Log) files for point-in-time recovery.

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Backup
metadata:
  name: pg-wal
  namespace: demo
spec:
  backupMethod: wal-archive
  backupPolicyName: pg-cluster-postgresql-backup-policy
```

To restore to a specific point in time:

```yaml
apiVersion: dataprotection.kubeblocks.io/v1alpha1
kind: Restore
metadata:
  name: pg-pitr-restore
  namespace: demo
spec:
  backup:
    name: pg-basebackup
    namespace: demo
  restoreTime: "2024-01-15T10:30:00Z"
```

## Connection Details

| Property | Value |
|---|---|
| Port | 5432 |
| Superuser Secret | `<cluster>-postgresql-account-postgres` |
| Secret Keys | `username`, `password` |

## Patroni Commands

Useful Patroni commands via kubectl exec:

```bash
# List cluster members and roles
kubectl -n demo exec -it pg-cluster-postgresql-0 -- patronictl list

# Switchover to a different primary
kubectl -n demo exec -it pg-cluster-postgresql-0 -- patronictl switchover

# Reinitialize a replica
kubectl -n demo exec -it pg-cluster-postgresql-0 -- patronictl reinit pg-cluster-postgresql <member>
```

## Termination Policies

| Policy | Behavior |
|---|---|
| `DoNotTerminate` | Block deletion |
| `Halt` | Delete workloads, keep PVCs and secrets |
| `Delete` | Delete workloads and PVCs, keep backups |
| `WipeOut` | Delete everything including backups |

## Documentation Links

- Create Cluster: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/create-and-connect-a-postgresql-cluster
- Scaling: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/cluster-management/scale-for-a-postgresql-cluster
- Backup & Restore: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-postgresql/backup-and-restore/backup
