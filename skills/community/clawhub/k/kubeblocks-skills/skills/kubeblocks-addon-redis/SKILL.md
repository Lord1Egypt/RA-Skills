---
name: kubeblocks-addon-redis
metadata:
  version: "0.1.0"
description: Deploy and manage Redis clusters on KubeBlocks with topology selection guidance. Supports standalone (dev/test), replication with Sentinel (HA), and Redis Cluster sharding (horizontal scaling) topologies. Use when the user mentions Redis, cache, in-memory store, or explicitly wants to create a Redis cluster. Provides topology comparison, best-practice defaults, and connection methods. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, backup, etc.), use the corresponding operation skill.
---

# Deploy Redis on KubeBlocks

## Overview

Deploy Redis on Kubernetes using KubeBlocks. Three topologies are available: standalone for development, replication with Sentinel for HA, and Redis Cluster for horizontal sharding.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/create-and-connect-a-redis-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The Redis addon must be enabled:

```bash
# Check if redis addon is installed
helm list -n kb-system | grep redis

# Install if missing
helm install kb-addon-redis kubeblocks/redis --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | clusterDef | topology | Components | Use Case |
|---|---|---|---|---|
| Standalone | `redis` | `standalone` | redis (1 replica) | Dev/test, no HA needed |
| Replication | `redis` | `replication` | redis (2+) + redis-sentinel (3) | Production HA |
| Sharding | N/A | N/A | Uses `spec.shardings` with componentDef `redis-cluster-7` | Horizontal scaling |

**Important:** The sharding topology uses `spec.shardings` instead of `spec.componentSpecs`. This is a fundamentally different spec structure.

## Supported Versions

| Version | serviceVersion |
|---|---|
| Redis 7.0 | `7.0.6` |
| Redis 7.2 | `7.2.4` |

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to Redis
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep redis
```

If not found:

```bash
helm install kb-addon-redis kubeblocks/redis --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Standalone

Simplest setup, single Redis instance. Good for development:

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

### Replication with Sentinel

Production-ready HA setup. Sentinel monitors the primary and performs automatic failover:

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

**Key points:**
- The `redis` component has 2+ replicas (1 primary + replicas, managed by Sentinel)
- The `redis-sentinel` component needs 3 replicas for quorum

### Redis Cluster (Sharding)

For horizontal scaling with data sharding. **This topology uses `spec.shardings` instead of `spec.componentSpecs`:**

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

**Key points:**
- Uses `spec.shardings` — NOT `spec.componentSpecs`
- `shards: 3` creates 3 shards (minimum recommended)
- Each shard has `replicas: 2` (1 primary + 1 replica per shard)
- Uses `componentDef: redis-cluster-7` (not `clusterDef`)
- Does NOT set `clusterDef` or `topology` at the cluster level

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster <cluster-name> -w
```

Wait until `STATUS` shows `Running`.

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## Step 5: Connect to Redis

### Get Credentials

```bash
# Secret name format: <cluster>-redis-account-default
kubectl -n demo get secret redis-standalone-redis-account-default -o jsonpath='{.data.password}' | base64 -d
```

### Connect via kubectl exec

```bash
# Standalone / Replication
kubectl -n demo exec -it redis-standalone-redis-0 -- redis-cli

# Redis Cluster (use -c flag for cluster mode)
kubectl -n demo exec -it redis-cluster-shard-ckvks-0 -- redis-cli -c
```

### Connect via Port-Forward

```bash
kubectl -n demo port-forward svc/redis-standalone-redis 6379:6379
# Then from another terminal:
redis-cli -h 127.0.0.1 -p 6379
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Sentinel failover issues:**
```bash
kubectl -n demo exec -it redis-replication-redis-sentinel-0 -- redis-cli -p 26379 SENTINEL masters
```

**Redis Cluster slots not assigned:**
```bash
kubectl -n demo exec -it <any-shard-pod> -- redis-cli -c CLUSTER INFO
```

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/stop-start-restart-a-redis-cluster) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/scale-for-a-redis-cluster) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/scale-for-a-redis-cluster) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/expand-volume-of-a-redis-cluster) |
| Change parameters | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/configuration/configure-cluster-parameters) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/cluster-management/expose-redis) |
| Backup | [backup](../kubeblocks-backup/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/backup-and-restore/backup) |
| Restore | [restore](../kubeblocks-restore/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-redis/backup-and-restore/restore) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.

## Next Steps

- For full YAML examples of all topologies, see [reference.md](references/reference.md)
