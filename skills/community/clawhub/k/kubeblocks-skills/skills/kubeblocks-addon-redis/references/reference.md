# Redis Addon Reference

Detailed YAML examples and configurations for the Redis addon on KubeBlocks v1.0.x.

Source: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/create-and-connect-a-redis-cluster

## Topologies Overview

| Topology | Spec Field | clusterDef | topology | componentDef |
|---|---|---|---|---|
| Standalone | `componentSpecs` | `redis` | `standalone` | — |
| Replication | `componentSpecs` | `redis` | `replication` | — |
| Sharding | `shardings` | — | — | `redis-cluster-7` |

## Standalone

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-standalone
  namespace: demo
spec:
  clusterDef: redis
  topology: standalone
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
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

## Replication with Sentinel

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-replication
  namespace: demo
spec:
  clusterDef: redis
  topology: replication
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 2
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: redis-sentinel
      serviceVersion: "7.2.4"
      replicas: 3
      resources:
        limits: {cpu: "0.2", memory: "256Mi"}
        requests: {cpu: "0.2", memory: "256Mi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

## Redis Cluster (Sharding)

### Basic Sharding

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster
  namespace: demo
spec:
  terminationPolicy: Delete
  shardings:
    - name: shard
      shards: 3
      template:
        name: redis-shard
        componentDef: redis-cluster-7
        serviceVersion: "7.2.4"
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

### Sharding with NodePort (External Access)

To expose Redis Cluster nodes externally using NodePort services:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster-external
  namespace: demo
spec:
  terminationPolicy: Delete
  shardings:
    - name: shard
      shards: 3
      template:
        name: redis-shard
        componentDef: redis-cluster-7
        serviceVersion: "7.2.4"
        replicas: 2
        resources:
          limits: {cpu: "0.5", memory: "0.5Gi"}
          requests: {cpu: "0.5", memory: "0.5Gi"}
        volumeClaimTemplates:
          - name: data
            spec:
              accessModes: [ReadWriteOnce]
              resources: {requests: {storage: 20Gi}}
        services:
          - name: nodeport
            serviceType: NodePort
            podService: true
```

Setting `podService: true` creates a separate NodePort service per pod, which is required for Redis Cluster since clients need direct access to each node.

## Sharding vs componentSpecs

**Critical difference:** Redis Cluster (sharding) uses `spec.shardings` instead of `spec.componentSpecs`.

| Field | Standalone / Replication | Sharding |
|---|---|---|
| Spec field | `spec.componentSpecs` | `spec.shardings` |
| `clusterDef` | `redis` | Not set |
| `topology` | `standalone` / `replication` | Not set |
| `componentDef` | Not needed (from clusterDef) | `redis-cluster-7` |
| Scaling | Change `replicas` | Change `shards` count |

## Supported Versions

| Version | serviceVersion | Notes |
|---|---|---|
| Redis 7.0 | `7.0.6` | Stable |
| Redis 7.2 | `7.2.4` | Latest, recommended |

## Connection Details

| Property | Value |
|---|---|
| Port | 6379 |
| Sentinel Port | 26379 |
| Default Secret | `<cluster>-redis-account-default` |
| Secret Keys | `username`, `password` |

## Sentinel Commands

```bash
# List monitored masters
kubectl -n demo exec -it redis-replication-redis-sentinel-0 -- redis-cli -p 26379 SENTINEL masters

# Get current master address
kubectl -n demo exec -it redis-replication-redis-sentinel-0 -- redis-cli -p 26379 SENTINEL get-master-addr-by-name
```

## Redis Cluster Commands

```bash
# Cluster info
kubectl -n demo exec -it <shard-pod> -- redis-cli -c CLUSTER INFO

# Cluster nodes
kubectl -n demo exec -it <shard-pod> -- redis-cli -c CLUSTER NODES

# Check slot distribution
kubectl -n demo exec -it <shard-pod> -- redis-cli -c CLUSTER SLOTS
```

## Termination Policies

| Policy | Behavior |
|---|---|
| `DoNotTerminate` | Block deletion |
| `Halt` | Delete workloads, keep PVCs and secrets |
| `Delete` | Delete workloads and PVCs, keep backups |
| `WipeOut` | Delete everything including backups |

## Documentation Links

- Create Cluster: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/create-and-connect-a-redis-cluster
- Scaling: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/scale-for-a-redis-cluster
