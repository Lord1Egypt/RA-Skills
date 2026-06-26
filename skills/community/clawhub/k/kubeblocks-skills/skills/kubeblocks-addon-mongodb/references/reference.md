# MongoDB Addon Reference

Detailed YAML examples and configurations for the MongoDB addon on KubeBlocks v1.0.x.

Source: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/create-and-connect-a-mongodb-cluster

## ClusterDefinition and Topologies

- **clusterDef:** `mongodb`
- **Topologies:** `replicaset`, `sharding`

## ReplicaSet Cluster

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-replicaset
  namespace: demo
spec:
  clusterDef: mongodb
  topology: replicaset
  terminationPolicy: Delete
  componentSpecs:
    - name: mongodb
      serviceVersion: "7.0.12"
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

## Sharded Cluster (Full Example)

A sharded cluster consists of three component types:

1. **Shards** — store the distributed data (defined in `spec.shardings`)
2. **Config Server** — stores sharding metadata (defined in `spec.componentSpecs`)
3. **Mongos** — query router (defined in `spec.componentSpecs`)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-sharded
  namespace: demo
spec:
  clusterDef: mongodb
  topology: sharding
  terminationPolicy: Delete
  shardings:
    - name: shard
      shards: 2
      template:
        name: mongodb
        serviceVersion: "7.0.12"
        replicas: 3
        resources:
          limits: {cpu: "0.5", memory: "0.5Gi"}
          requests: {cpu: "0.5", memory: "0.5Gi"}
        volumeClaimTemplates:
          - name: data
            spec:
              accessModes: [ReadWriteOnce]
              resources: {requests: {storage: 20Gi}}
  componentSpecs:
    - name: config-server
      serviceVersion: "7.0.12"
      replicas: 3
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: mongos
      serviceVersion: "7.0.12"
      replicas: 2
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
```

### Production Sharded Cluster

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-sharded-prod
  namespace: demo
spec:
  clusterDef: mongodb
  topology: sharding
  terminationPolicy: Halt
  shardings:
    - name: shard
      shards: 3
      template:
        name: mongodb
        serviceVersion: "7.0.12"
        replicas: 3
        resources:
          limits: {cpu: "2", memory: "4Gi"}
          requests: {cpu: "2", memory: "4Gi"}
        volumeClaimTemplates:
          - name: data
            spec:
              accessModes: [ReadWriteOnce]
              resources: {requests: {storage: 100Gi}}
  componentSpecs:
    - name: config-server
      serviceVersion: "7.0.12"
      replicas: 3
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: mongos
      serviceVersion: "7.0.12"
      replicas: 3
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
```

## Sharding Architecture

```
Client
  │
  ▼
mongos (query router, stateless)
  │
  ├─── config-server (metadata, 3 replicas)
  │
  ├─── shard-0 (ReplicaSet, 3 replicas)
  ├─── shard-1 (ReplicaSet, 3 replicas)
  └─── shard-N (ReplicaSet, 3 replicas)
```

- Clients connect to **mongos** on port 27017
- mongos routes queries to the appropriate shard(s)
- Each shard is an independent ReplicaSet
- Config-server stores chunk distribution metadata

## Supported Versions

| Version | serviceVersion | Notes |
|---|---|---|
| MongoDB 4.0 | `4.0` | Legacy |
| MongoDB 4.2 | `4.2` | Legacy |
| MongoDB 4.4 | `4.4` | Legacy |
| MongoDB 5.0 | `5.0` | Stable |
| MongoDB 6.0 | `6.0` | Stable |
| MongoDB 7.0 | `7.0.12` | Latest, recommended |

## Connection Details

| Property | Value |
|---|---|
| Port | 27017 |
| Root Secret | `<cluster>-mongodb-account-root` |
| Secret Keys | `username`, `password` |

### Connection Strings

```bash
# ReplicaSet
mongosh "mongodb://root:<password>@<cluster>-mongodb-0.<cluster>-mongodb-headless.<namespace>.svc:27017,<cluster>-mongodb-1.<cluster>-mongodb-headless.<namespace>.svc:27017,<cluster>-mongodb-2.<cluster>-mongodb-headless.<namespace>.svc:27017/admin?replicaSet=<cluster>-mongodb"

# Sharded (via mongos service)
mongosh "mongodb://root:<password>@<cluster>-mongos.<namespace>.svc:27017/admin"
```

## Useful MongoDB Commands

```bash
# ReplicaSet status
kubectl -n demo exec -it <cluster>-mongodb-0 -- mongosh --eval "rs.status()"

# Sharding status
kubectl -n demo exec -it <cluster>-mongos-0 -- mongosh --eval "sh.status()"

# Enable sharding on a database
kubectl -n demo exec -it <cluster>-mongos-0 -- mongosh --eval 'sh.enableSharding("mydb")'

# Shard a collection
kubectl -n demo exec -it <cluster>-mongos-0 -- mongosh --eval 'sh.shardCollection("mydb.mycol", {"_id": "hashed"})'
```

## Termination Policies

| Policy | Behavior |
|---|---|
| `DoNotTerminate` | Block deletion |
| `Halt` | Delete workloads, keep PVCs and secrets |
| `Delete` | Delete workloads and PVCs, keep backups |
| `WipeOut` | Delete everything including backups |

## Documentation Links

- Create Cluster: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/create-and-connect-a-mongodb-cluster
- Scaling: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/scale-for-a-mongodb-cluster
