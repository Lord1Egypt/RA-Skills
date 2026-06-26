---
name: kubeblocks-addon-milvus
metadata:
  version: "0.1.0"
description: Deploy and manage Milvus vector database clusters on KubeBlocks for AI/ML workloads. Supports embedding similarity search, standalone (dev/test) and cluster (production) topologies. Use when the user mentions Milvus, vector database, AI embeddings, similarity search, or explicitly wants to create a Milvus cluster. Provides topology comparison, connection methods, and Day-2 operations. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, expose, etc.), use the corresponding operation skill.
---

# Deploy Milvus on KubeBlocks

## Overview

Deploy Milvus vector database clusters on Kubernetes using KubeBlocks. Milvus powers embedding similarity search and AI applications. Supports standalone mode (single node, dev/test) and cluster mode (distributed, production) with etcd, MinIO, and optional Pulsar/Kafka for log storage.

Official docs: https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/01-overview
Quickstart: https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/02-quickstart

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The Milvus addon must be enabled:

```bash
# Check if milvus addon is installed
helm list -n kb-system | grep milvus

# Install if missing
helm install kb-addon-milvus kubeblocks/milvus --namespace kb-system --version 1.0.0
```

## Available Topologies

| Topology | Value | Components | Use Case |
|---|---|---|---|
| Standalone | `standalone` | milvus + etcd + minio | Dev/test, single node |
| Cluster | `cluster` | milvus-proxy, milvus-mixcoord, milvus-datanode, milvus-indexnode, milvus-querynode + etcd + minio (+ pulsar/kafka) | Production, distributed |

Default ports: 19530 (gRPC), 9091 (metrics).

## Supported Versions

| Version | serviceVersion |
|---|---|
| Milvus 2.3 | `v2.3.2` |
| Milvus 2.5 | `v2.5.13` |

List available: `kubectl get cmpv milvus`

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (choose topology)
- [ ] Step 4: Dry-run, then apply
- [ ] Step 5: Watch until Running, verify success
- [ ] Step 6: Connect and verify
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep milvus
```

If not found:

```bash
helm install kb-addon-milvus kubeblocks/milvus --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

### Standalone (Dev/Test)

Single-node deployment with etcd and MinIO co-located. Suitable for development and testing:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: milvus-standalone
  namespace: demo
spec:
  clusterDef: milvus
  topology: standalone
  terminationPolicy: Delete
  componentSpecs:
    - name: etcd
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: minio
      replicas: 1
      resources:
        limits: {cpu: "0.5", memory: "0.5Gi"}
        requests: {cpu: "0.5", memory: "0.5Gi"}
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources: {requests: {storage: 20Gi}}
    - name: milvus
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

### Cluster (Production)

Distributed deployment with proxy, mixcoord, datanode, indexnode, querynode. Requires pre-created etcd, minio, and optionally Pulsar/Kafka clusters. See [cluster topology docs](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/03-topologies/02-cluster) for full setup.

Key components: `milvus-proxy` (access), `milvus-mixcoord` (coordination), `milvus-datanode`, `milvus-indexnode`, `milvus-querynode` (compute), plus `etcd`, `minio`. Cluster mode uses `serviceRef` to reference external etcd, minio, and pulsar/kafka clusters.

## Step 4: Dry-Run and Apply

Before applying, run server-side dry-run to catch RBAC, webhook, or schema errors:

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

If dry-run succeeds, apply:

```bash
kubectl apply -f cluster.yaml
```

## Step 5: Wait for Cluster Ready

```bash
kubectl -n demo get cluster <cluster-name> -w
```

**Success condition:** `STATUS` shows `Running`. Typical duration: 2–5 min. Investigate after 10 min if still Creating/Updating (see [safety-patterns](../../references/safety-patterns.md)).

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=<cluster-name>
```

## Step 6: Connect

### Port-Forward (Standalone)

```bash
kubectl port-forward pod/<cluster-name>-milvus-0 -n demo 19530:19530
```

Connect via `localhost:19530` (gRPC). For cluster mode, port-forward to the proxy pod.

### Verify with Python

```python
from pymilvus import connections
connections.connect(host="localhost", port=19530)
```

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster <cluster-name>
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Milvus pod not starting:**
```bash
kubectl -n demo logs <milvus-pod>
```

**etcd or minio dependency issues:**
- Ensure etcd and minio pods are Running before milvus starts
- Check component order in `componentSpecs`

**Out of memory:**
- Increase `resources.limits.memory` for milvus component
- For cluster mode, scale datanode/indexnode/querynode resources

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/01-stop-start-restart) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/02-vertical-scaling) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/03-horizontal-scaling) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-milvus/04-operations/) |

## Safety Patterns

Follow [safety-patterns](../../references/safety-patterns.md): dry-run before apply, confirm success condition after watch, pre-deletion checklist before delete.
