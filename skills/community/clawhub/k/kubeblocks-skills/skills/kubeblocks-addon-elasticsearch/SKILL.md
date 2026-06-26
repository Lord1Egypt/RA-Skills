---
name: kubeblocks-addon-elasticsearch
metadata:
  version: "0.1.0"
description: Deploy and manage Elasticsearch clusters on KubeBlocks for full-text search, log analytics, and observability. Use when the user mentions Elasticsearch, ELK stack, search engine, log analytics, Kibana, full-text search, or explicitly wants to create an Elasticsearch cluster. Provides single-node (dev/test) and multi-node cluster creation with connection methods. No backup/restore support in KubeBlocks currently. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, volume expansion, etc.), use the corresponding operation skill.
---

# Deploy Elasticsearch on KubeBlocks

## Overview

Deploy Elasticsearch clusters on Kubernetes using KubeBlocks. Elasticsearch is a distributed, RESTful search engine for full-text search, log analytics, and observability. Supports single-node (dev/test) and multi-node topologies.

Official docs: https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/01-overview
Quickstart: https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/02-quickstart
Operations: https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/

**Note:** Backup and restore are not supported for Elasticsearch in KubeBlocks currently.

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The Elasticsearch addon must be enabled:

```bash
# Check if elasticsearch addon is installed
helm list -n kb-system | grep elasticsearch

# Install if missing
helm install kb-addon-elasticsearch kubeblocks/elasticsearch --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | Value | Components | Use Case |
|---|---|---|---|
| Single-node | (default) | elasticsearch | Dev/test, one node handles all roles |
| Multi-node | (default) | elasticsearch | Production, replicas > 1 |

Elasticsearch uses a single topology; the component name is `elasticsearch`. For single-node mode, set `replicas: 1` and configure `mode: "single-node"` in configs. For production, use `replicas: 3` or more.

## Supported Versions

| Major | serviceVersion Examples |
|---|---|
| 6.x | `6.8.23` |
| 7.x | `7.10.2`, `7.10.1`, `7.8.1`, `7.7.1` |
| 8.x | `8.15.5`, `8.8.2`, `8.1.3` |

List available versions: `kubectl get cmpv elasticsearch`

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (single-node or multi-node)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect and verify
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep elasticsearch
```

If not found:

```bash
helm install kb-addon-elasticsearch kubeblocks/elasticsearch --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Single-Node (Dev/Test)

One node handles all roles (master, data, ingest). Suitable for development:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: es-singlenode
  namespace: demo
spec:
  clusterDef: elasticsearch
  terminationPolicy: Delete
  componentSpecs:
    - name: elasticsearch
      serviceVersion: "8.8.2"
      replicas: 1
      configs:
        - name: es-cm
          variables:
            mode: "single-node"
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

### Multi-Node (Production)

Multiple replicas for high availability and shard distribution:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: es-cluster
  namespace: demo
spec:
  clusterDef: elasticsearch
  terminationPolicy: Delete
  componentSpecs:
    - name: elasticsearch
      serviceVersion: "8.8.2"
      replicas: 3
      resources:
        limits: {cpu: "1", memory: "2Gi"}
        requests: {cpu: "1", memory: "2Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
```

**Key points:**
- Do not set `mode: "single-node"` for multi-node clusters
- Use odd replica counts (3, 5) for master quorum
- Default ports: 9200 (HTTP), 9300 (transport)

### Apply with Dry-Run

Per [safety-patterns](../../references/safety-patterns.md), always dry-run before apply:

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

If dry-run succeeds:

```bash
kubectl apply -f cluster.yaml
```

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster <cluster-name> -w
```

**Success condition:** `STATUS` shows `Running`. Typical duration: 1–5 min. If not Running after 10 min, investigate:

```bash
kubectl describe cluster <cluster-name> -n demo
kubectl get events -n demo --sort-by='.lastTimestamp' | grep <cluster-name>
```

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## Step 5: Connect and Verify

### Port-Forward

```bash
kubectl -n demo port-forward svc/<cluster-name>-elasticsearch-http 9200:9200
```

### Health Check

```bash
curl -s http://localhost:9200/_cluster/health?pretty
```

Expected: `"status" : "green"` or `"yellow"` (yellow is acceptable for single-node).

### Cluster Info

```bash
curl -s http://localhost:9200
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod not starting:**
```bash
kubectl -n demo logs <elasticsearch-pod>
kubectl -n demo describe pod <elasticsearch-pod>
```

**Out of memory:**
- Increase `resources.limits.memory` and `resources.requests.memory`
- Elasticsearch typically needs at least 2Gi for production

**Single-node cluster in yellow:**
- Normal for single-node; replicas cannot be allocated. Use multi-node for green status.

## Day-2 Operations

**Note:** Backup and restore are not supported for Elasticsearch in KubeBlocks currently.

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-elasticsearch/04-operations/) |

## Safety Patterns

Follow [safety-patterns.md](../../references/safety-patterns.md) for dry-run before apply, status confirmation after watch, and pre-deletion checklist.
