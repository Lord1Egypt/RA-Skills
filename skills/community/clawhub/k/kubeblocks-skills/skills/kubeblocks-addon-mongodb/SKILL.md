---
name: kubeblocks-addon-mongodb
metadata:
  version: "0.1.0"
description: Deploy and manage MongoDB clusters on KubeBlocks with topology selection guidance. Supports ReplicaSet (HA) and Sharding (mongos + config servers + shards) topologies. Use when the user mentions MongoDB, Mongo, document database, or explicitly wants to create a MongoDB cluster. Provides topology comparison, best-practice defaults, and connection methods. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, backup, etc.), use the corresponding operation skill.
---

# Deploy MongoDB on KubeBlocks

## Overview

Deploy MongoDB clusters on Kubernetes using KubeBlocks. Supports ReplicaSet for HA and Sharding for horizontal scaling with mongos routers and config servers.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/create-and-connect-a-mongodb-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The MongoDB addon must be enabled:

```bash
# Check if mongodb addon is installed
helm list -n kb-system | grep mongodb

# Install if missing
helm install kb-addon-mongodb kubeblocks/mongodb --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | topology value | Components | Use Case |
|---|---|---|---|
| ReplicaSet | `replicaset` | mongodb (3 replicas) | Standard HA, most common |
| Sharding | `sharding` | shard (N) + config-server + mongos | Horizontal scaling, large datasets |

## Supported Versions

MongoDB 4.0 through 7.0 are supported. Common serviceVersion values:

| Version | serviceVersion |
|---|---|
| MongoDB 4.0 | `4.0` |
| MongoDB 4.2 | `4.2` |
| MongoDB 4.4 | `4.4` |
| MongoDB 5.0 | `5.0` |
| MongoDB 6.0 | `6.0` |
| MongoDB 7.0 | `7.0.12` |

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect to MongoDB
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep mongodb
```

If not found:

```bash
helm install kb-addon-mongodb kubeblocks/mongodb --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### ReplicaSet (Recommended)

Standard HA setup with automatic primary election:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mongo-cluster
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

Apply:

```bash
kubectl apply -f mongo-cluster.yaml
```

**Key points:**
- 3 replicas is the minimum for a proper ReplicaSet (allows majority voting)
- MongoDB automatically elects a primary among the replicas

### Sharding

For horizontal scaling across multiple shards. Uses both `spec.shardings` (for shard data) and `spec.componentSpecs` (for config-server and mongos):

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

**Key points:**
- Shards use `spec.shardings` (each shard is a ReplicaSet)
- Config-server and mongos use `spec.componentSpecs`
- `shards: 2` creates 2 shards (each with 3 replicas)
- Connect to `mongos` for data operations (port 27017)
- Config-server stores sharding metadata

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster <cluster-name> -w
```

Wait until `STATUS` shows `Running`. Sharded clusters take longer (3-5 minutes).

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## Step 5: Connect to MongoDB

### Get Credentials

```bash
# Secret name format: <cluster>-mongodb-account-root
kubectl -n demo get secret mongo-cluster-mongodb-account-root -o jsonpath='{.data.password}' | base64 -d
```

### Connect via kubectl exec

```bash
# ReplicaSet
kubectl -n demo exec -it mongo-cluster-mongodb-0 -- mongosh --username root --authenticationDatabase admin

# Sharded cluster (connect via mongos)
kubectl -n demo exec -it mongo-sharded-mongos-0 -- mongosh --username root --authenticationDatabase admin
```

### Connect via Port-Forward

```bash
# ReplicaSet
kubectl -n demo port-forward svc/mongo-cluster-mongodb 27017:27017

# Sharded (via mongos)
kubectl -n demo port-forward svc/mongo-sharded-mongos 27017:27017

# Then from another terminal:
mongosh mongodb://root:<password>@127.0.0.1:27017/admin
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**ReplicaSet not forming:**
```bash
kubectl -n demo exec -it mongo-cluster-mongodb-0 -- mongosh --eval "rs.status()"
```

**Sharding status:**
```bash
kubectl -n demo exec -it mongo-sharded-mongos-0 -- mongosh --eval "sh.status()"
```

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/stop-start-restart-a-mongodb-cluster) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/scale-for-a-mongodb-cluster) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/scale-for-a-mongodb-cluster) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/cluster-management/expand-volume-of-a-mongodb-cluster) |
| Change parameters | [reconfigure-parameters](../kubeblocks-reconfigure-parameters/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/configuration/configure-cluster-parameters) |
| Backup | [backup](../kubeblocks-backup/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/backup-and-restore/backup) |
| Restore | [restore](../kubeblocks-restore/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mongodb/backup-and-restore/restore) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.

## Next Steps

- For detailed sharding YAML examples, see [reference.md](references/reference.md)
