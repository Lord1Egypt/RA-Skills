---
name: kubeblocks-addon-qdrant
metadata:
  version: "0.1.0"
description: Deploy and manage Qdrant vector database clusters on KubeBlocks for vector search, similarity search, and embedding storage. Use when the user mentions Qdrant, vector database, vector search, similarity search, embedding, RAG, or explicitly wants to create a Qdrant cluster. Provides cluster creation, connection via REST API, and Day-2 operations. For generic cluster creation across all engines, see kubeblocks-create-cluster. For Day-2 operations (scaling, etc.), use the corresponding operation skill.
---

# Deploy Qdrant on KubeBlocks

## Overview

Deploy Qdrant vector database clusters on Kubernetes using KubeBlocks. Qdrant is a high-performance vector similarity search engine optimized for AI-driven applications such as semantic search, RAG, and recommendation systems. Multiple replicas form a distributed cluster with data sharding.

Official docs: https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/01-overview
Quickstart: https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/02-quickstart

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed (see [install-kubeblocks](../kubeblocks-install/SKILL.md))
- The Qdrant addon must be enabled:

```bash
# Check if qdrant addon is installed
helm list -n kb-system | grep qdrant

# Install if missing
helm install kb-addon-qdrant kubeblocks/qdrant --namespace kb-system --version 1.0.0
```

## Topology

| Topology | Value | Component | Use Case |
|---|---|---|---|
| Cluster | `cluster` | qdrant | Single topology, distributed with data sharding |

## Supported Versions

| Version | serviceVersion |
|---|---|
| 1.5 | `1.5.0` |
| 1.7 | `1.7.3` |
| 1.8 | `1.8.1`, `1.8.4` |
| 1.10 | `1.10.0` |
| 1.13 | `1.13.4` |
| 1.15 | `1.15.4` |

List available versions: `kubectl get cmpv qdrant`

## Workflow

```
- [ ] Step 1: Ensure addon is installed
- [ ] Step 2: Create namespace
- [ ] Step 3: Create cluster (dry-run then apply)
- [ ] Step 4: Wait for cluster to be ready
- [ ] Step 5: Connect via REST API
```

## Step 1: Ensure Addon Is Installed

```bash
helm list -n kb-system | grep qdrant
```

If not found:

```bash
helm install kb-addon-qdrant kubeblocks/qdrant --namespace kb-system --version 1.0.0
```

## Step 2: Create Namespace

```bash
kubectl create namespace demo --dry-run=client -o yaml | kubectl apply -f -
```

## Step 3: Create Cluster

Default ports: 6333 (HTTP REST API), 6334 (gRPC). Recommended replicas: 3, 5, or 7.

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: qdrant-cluster
  namespace: demo
spec:
  clusterDef: qdrant
  topology: cluster
  terminationPolicy: Delete
  componentSpecs:
    - name: qdrant
      serviceVersion: "1.10.0"
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

**Dry-run before apply:**

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

If dry-run succeeds:

```bash
kubectl apply -f cluster.yaml
```

## Step 4: Wait for Cluster Ready

```bash
kubectl -n demo get cluster qdrant-cluster -w
```

**Success condition:** `STATUS` shows `Running`. Typical duration: 1–2 minutes. Investigate after 10 min if still Creating.

Check pods:

```bash
kubectl -n demo get pods -l app.kubernetes.io/instance=qdrant-cluster
```

## Step 5: Connect via REST API

Port 6333 exposes the HTTP REST API. Use port-forward or the headless service:

```bash
# Port-forward to a pod
kubectl -n demo port-forward qdrant-cluster-qdrant-0 6333:6333
```

```bash
# Health check
curl http://localhost:6333/health
```

```bash
# List collections
curl http://localhost:6333/collections
```

Internal service: `qdrant-cluster-qdrant-qdrant.demo.svc.cluster.local:6333` (REST), `:6334` (gRPC).

## Backup

KubeBlocks supports full backup via HTTP API `snapshot` for all collections. See:
https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/02-create-full-backup

## Troubleshooting

**Cluster stuck in Creating:**
```bash
kubectl -n demo describe cluster qdrant-cluster
kubectl -n demo get events --sort-by='.lastTimestamp'
```

**Pod not starting:**
```bash
kubectl -n demo logs qdrant-cluster-qdrant-0
kubectl -n demo describe pod qdrant-cluster-qdrant-0
```

**Connection refused:** Ensure port-forward is running or use the internal service from within the cluster.

## Day-2 Operations

| Operation | Skill | External Docs |
|---|---|---|
| Stop / Start / Restart | [cluster-lifecycle](../kubeblocks-cluster-lifecycle/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/01-stop-start-restart) |
| Scale CPU / Memory | [vertical-scaling](../kubeblocks-vertical-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| Add / Remove replicas | [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| Expand storage | [volume-expansion](../kubeblocks-volume-expansion/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| Upgrade engine version | [minor-version-upgrade](../kubeblocks-minor-version-upgrade/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| Expose externally | [expose-service](../kubeblocks-expose-service/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/04-operations/) |
| Backup | [backup](../kubeblocks-backup/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/02-create-full-backup) |
| Restore | [restore](../kubeblocks-restore/SKILL.md) | [Docs](https://kubeblocks.io/docs/preview/kubeblocks-for-qdrant/05-backup-restore/) |

## Safety Patterns

Follow [safety-patterns](../../references/safety-patterns.md): dry-run before apply, confirm success condition after watch, pre-deletion checklist before delete.
