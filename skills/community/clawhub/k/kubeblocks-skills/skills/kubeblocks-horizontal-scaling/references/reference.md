# Horizontal Scaling Reference

## OpsRequest API Reference

Full API docs: https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations

### Scale Out

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scaleout-<cluster>
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component>
      scaleOut:
        replicaChanges: <count>
```

### Scale In

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: scalein-<cluster>
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: HorizontalScaling
  horizontalScaling:
    - componentName: <component>
      scaleIn:
        replicaChanges: <count>
```

### Decommission Specific Instances

```yaml
  horizontalScaling:
    - componentName: <component>
      scaleIn:
        replicaChanges: <count>
        onlineInstancesToOffline:
          - "<pod-name-1>"
          - "<pod-name-2>"
```

## Engine-Specific Scaling Behaviors

### MySQL

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| Semi-sync | `mysql` | 2 | New replicas auto-join as secondaries. Semi-sync replication configured automatically. |
| MGR (Group Replication) | `mysql` | 3 | Raft-based consensus requires odd numbers. Min 3 for fault tolerance. |
| Orchestrator | `mysql` | 2 | Orchestrator auto-discovers and manages new replicas. |

- Scale-out: new replicas provision from backup or full clone of primary
- Scale-in: cannot remove the primary; switchover happens automatically if needed
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/03-horizontal-scaling

### PostgreSQL

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| Patroni replication | `postgresql` | 1 | Patroni manages replication slots and leader election. |

- Scale-out: new replicas stream from primary via pg_basebackup
- Scale-in: Patroni handles slot cleanup; cannot remove current leader
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/03-horizontal-scaling

### Redis

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| Standalone | `redis` | 1 | Cannot scale (single instance) |
| Replication | `redis` | 2 | Sentinel manages failover. Min 1 primary + 1 replica. |
| Cluster (sharding) | `redis-shard` | 3 shards | Each shard = 1 primary + N replicas. Auto-resharding on scale. |

- **Replication topology**: scaling adds/removes read replicas
- **Cluster topology**: scaling adds/removes entire shard groups
  - Scale-out: new shard created, hash slots automatically redistributed
  - Scale-in: data migrated from removed shard, then shard terminated
  - Monitor resharding: `redis-cli --cluster check <host>:<port>`
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-redis/04-operations/03-horizontal-scaling

### MongoDB

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| ReplicaSet | `mongodb` | 1 | New members auto-join the replica set. |
| Sharding — mongos | `mongos` | 1 | Stateless query routers, safe to scale freely. |
| Sharding — configsvr | `configsvr` | 3 | Config servers, typically stay at 3. |
| Sharding — shard | `shard` | 1+ | Each shard is a replica set. |

- **ReplicaSet**: scaling adds/removes secondaries
- **Sharding**: scaling the `shard` component adds/removes entire shard groups
  - The MongoDB balancer auto-redistributes chunks after shard changes
  - Large datasets may take significant time to rebalance
  - Monitor: `db.adminCommand({ balancerStatus: 1 })` inside mongos
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-mongodb/04-operations/03-horizontal-scaling

### Kafka

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| Combined | `kafka-combine` | 1 | Broker + controller co-located |
| Separated — broker | `kafka-broker` | 1 | Data brokers only |
| Separated — controller | `kafka-controller` | 3 | Raft-based, odd numbers recommended |

- Scale-out: new brokers join the cluster, but existing topic partitions are NOT automatically rebalanced
- Scale-in: remove only brokers with no partition assignments (or reassign first)
- Partition reassignment must be done manually or via tools like `kafka-reassign-partitions.sh`
- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-kafka/04-operations/03-horizontal-scaling

### Elasticsearch

| Topology | Component | Min Replicas | Scaling Notes |
|----------|-----------|-------------|---------------|
| Default | `elasticsearch` | 1 | New nodes auto-join. Shard rebalancing is automatic. |

- Docs: https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/03-horizontal-scaling

## kubectl Patch Alternative

For simple replica count changes without OpsRequest:

```bash
kubectl patch cluster <cluster> -n <ns> \
  --type merge \
  -p '{"spec":{"componentSpecs":[{"name":"<component>","replicas":<new-total>}]}}'
```

This sets the absolute replica count (not a delta).

## Replicas vs Shards: Key Differences

| Concept | Replicas | Shards |
|---------|----------|--------|
| Data model | Each replica holds a full copy of data | Each shard holds a subset (partition) of data |
| Purpose | High availability, read scaling | Horizontal data partitioning, write scaling |
| Engines | All engines | Redis Cluster, MongoDB Sharding |
| Scaling effect | More read capacity, better HA | More storage capacity, more write throughput |
| Data movement | New replica syncs full dataset | Hash slots / chunks redistribute across shards |

## Decommissioning Specific Instances

When scaling in, by default KubeBlocks removes the last-created instance. To choose a specific instance:

```yaml
  horizontalScaling:
    - componentName: mysql
      scaleIn:
        replicaChanges: 1
        onlineInstancesToOffline:
          - "mysql-cluster-mysql-2"
```

Use cases:
- Remove a replica on a specific node being decommissioned
- Remove an unhealthy instance
- Remove an instance in a specific availability zone

Docs: https://kubeblocks.io/blog/take-specified-instances-offline

## Pre-scaling Checklist

- [ ] Sufficient node resources for new pods (CPU, memory, storage)
- [ ] StorageClass can provision new PVCs
- [ ] For scale-in: verify the cluster won't go below the minimum replica count for its topology
- [ ] For sharding: ensure data rebalancing time is acceptable for your SLA

## Documentation Links

| Resource | URL |
|----------|-----|
| MySQL horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/03-horizontal-scaling |
| PostgreSQL horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/03-horizontal-scaling |
| Redis horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-redis/04-operations/03-horizontal-scaling |
| MongoDB horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-mongodb/04-operations/03-horizontal-scaling |
| Kafka horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-kafka/04-operations/03-horizontal-scaling |
| Elasticsearch horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/03-horizontal-scaling |
| Milvus horizontal scaling | https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/03-horizontal-scaling |
| Decommission specific instance | https://kubeblocks.io/blog/take-specified-instances-offline |
| Operations API | https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations |
