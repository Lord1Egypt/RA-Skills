# Cluster Lifecycle Reference

## OpsRequest API Reference

Full API docs: https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations

### Stop OpsRequest

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Stop
```

### Start OpsRequest

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: start-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Start
```

### Restart OpsRequest

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: restart-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Restart
  restart:
    - componentName: <component-name>
```

Restart supports multiple components in a single OpsRequest:

```yaml
  restart:
    - componentName: mysql
    - componentName: proxy
```

## Component Names by Engine

| Engine | Component Names |
|--------|----------------|
| MySQL (semi-sync) | `mysql` |
| MySQL (MGR) | `mysql` |
| MySQL (orchestrator) | `mysql`, `orchestrator` |
| MySQL (with ProxySQL) | `mysql`, `proxysql` |
| PostgreSQL | `postgresql` |
| Redis (standalone) | `redis` |
| Redis (replication) | `redis`, `redis-sentinel` |
| Redis (cluster/sharding) | `redis-shard` |
| MongoDB (replicaset) | `mongodb` |
| MongoDB (sharding) | `mongos`, `configsvr`, `shard` |
| Kafka (combined) | `kafka-combine` |
| Kafka (separated) | `kafka-broker`, `kafka-controller` |
| Elasticsearch | `elasticsearch` |
| Milvus (standalone) | `milvus` |
| Milvus (cluster) | `milvus-proxy`, `milvus-mixcoord`, `milvus-datanode`, `milvus-indexnode`, `milvus-querynode` |

## kubectl Patch Alternative

### Stop via patch

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge \
  -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":true}]}}'
```

### Start via patch

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge \
  -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":false}]}}'
```

### Stop specific components only

You can stop individual components by setting `stop: true` on specific componentSpecs. This is useful for stopping proxy or monitoring components while keeping the database running.

## Cluster Status Transitions

```
Running ──Stop──→ Stopping ──→ Stopped
Stopped ──Start─→ Starting ──→ Running
Running ──Restart→ Updating ──→ Running
```

### Status Meanings

| Status | Description |
|--------|-------------|
| `Running` | All components healthy and serving |
| `Stopped` | All pods terminated, PVCs retained |
| `Stopping` | Stop in progress, pods being terminated |
| `Starting` | Start in progress, pods being created |
| `Updating` | Restart in progress, rolling restart active |
| `Failed` | Operation failed, check events |

## Behavior Details

### Stop behavior
- All pods in the cluster are terminated (scaled to 0 replicas)
- PVCs are retained — no data loss
- Services are retained but have no endpoints
- Cluster status changes to `Stopped`
- Cost savings: no compute charges while stopped (only storage charges remain)

### Start behavior
- Pods are recreated from the same PVC data
- Data is preserved exactly as it was before stop
- Replication and HA are re-established automatically
- Cluster returns to `Running` once all pods are ready

### Restart behavior
- Performs a rolling restart: one pod at a time
- For HA clusters: secondary pods restart first, then primary
- Automatic switchover occurs before restarting the primary to minimize downtime
- No data loss
- Useful after static parameter changes that require a restart

## Common Patterns

### Cost-saving: stop dev/test clusters on schedule

Combine with a CronJob or external scheduler:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-dev-cluster-nightly
  namespace: dev
spec:
  clusterName: dev-mysql
  type: Stop
EOF
```

### Restart after static parameter change

After modifying a static parameter (e.g., `innodb_buffer_pool_size` for MySQL), a restart is required:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: restart-after-reconfig
  namespace: default
spec:
  clusterName: mysql-cluster
  type: Restart
  restart:
    - componentName: mysql
EOF
```

## Documentation Links

| Resource | URL |
|----------|-----|
| MySQL lifecycle | https://kubeblocks.io/docs/preview/kubeblocks-for-mysql/04-operations/01-stop_start_restart |
| PostgreSQL lifecycle | https://kubeblocks.io/docs/preview/kubeblocks-for-postgresql/04-operations/01-stop-start-restart |
| Redis lifecycle | https://kubeblocks.io/docs/preview/kubeblocks-for-redis/04-operations/01-stop-start-restart |
| MongoDB lifecycle | https://kubeblocks.io/docs/preview/kubeblocks-for-mongodb/04-operations/01-stop-start-restart |
| Kafka lifecycle | https://kubeblocks.io/docs/preview/kubeblocks-for-kafka/04-operations/01-stop-start-restart |
| Operations API | https://kubeblocks.io/docs/preview/user_docs/references/api-reference/operations |
