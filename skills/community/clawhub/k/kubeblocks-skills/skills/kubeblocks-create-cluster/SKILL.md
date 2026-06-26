---
name: kubeblocks-create-cluster
metadata:
  version: "0.1.0"
description: Create a database cluster on KubeBlocks using the generic Cluster CR template. Supports all addons (MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, etc.) with various topologies. Use when the user wants to deploy, create, provision, or launch a new database cluster — especially for engines without a dedicated addon-* skill. For MySQL, PostgreSQL, Redis, MongoDB, or Kafka, prefer the engine-specific addon skill (kubeblocks-addon-mysql, kubeblocks-addon-postgresql, kubeblocks-addon-redis, kubeblocks-addon-mongodb, kubeblocks-addon-kafka) which provides topology guidance and tuned defaults. NOT for managing existing clusters (see Day-2 operation skills).
---

# Create a Database Cluster on KubeBlocks

## Overview

KubeBlocks uses the `Cluster` CR (Custom Resource) to declaratively create and manage database clusters. A single YAML template works across all supported addons — MySQL, PostgreSQL, Redis, MongoDB, Kafka, and more.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/create-and-connect-a-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Prerequisites

- A running Kubernetes cluster with KubeBlocks installed. If not, use:
  - [create-local-k8s-cluster](../kubeblocks-create-local-k8s-cluster/SKILL.md) to create a local cluster
  - [install-kubeblocks](../kubeblocks-install/SKILL.md) to install KubeBlocks
- The target addon must be installed (check with `helm list -n kb-system | grep kb-addon`)

## Workflow

```
- [ ] Step 1: Determine addon and topology
- [ ] Step 2: Apply Cluster CR
- [ ] Step 3: Verify cluster is running
- [ ] Step 4: Connect to the cluster
```

## Step 1: Determine Addon and Topology

Ask the user which database engine they need. Use the table below to select the correct `clusterDef`, `topology`, and `componentSpecs` values.

### Common Addon Quick Reference

| Addon | clusterDef | Topology | Component Name | Default Port | serviceVersion |
|-------|-----------|----------|----------------|-------------|----------------|
| MySQL (ApeCloud) | apecloud-mysql | apecloud-mysql | mysql | 3306 | 8.0.30 |
| MySQL (Community) | mysql | mysql-replication | mysql | 3306 | 8.0.33 |
| PostgreSQL | postgresql | postgresql | postgresql | 5432 | 14.8.0 |
| Redis | redis | redis-cluster | redis | 6379 | 7.2.4 |
| MongoDB | mongodb | mongodb-replicaset | mongodb | 27017 | 6.0.16 |
| Kafka | kafka | kafka-combined | kafka-combine | 9092 | 3.7.2 |

> **Note:** Topologies and versions may change across addon releases. Run `kubectl get clusterdefinitions` and `kubectl get componentversions` to see what is available in your environment.

If the user needs **detailed topology options or advanced configurations** for a specific addon, refer them to the addon-specific skills (e.g., kubeblocks-addon-mysql, kubeblocks-addon-postgresql, kubeblocks-addon-redis, kubeblocks-addon-mongodb, kubeblocks-addon-kafka) when available.

## Step 2: Apply Cluster CR

### Universal Cluster Template

Replace the placeholder values according to the addon table above:

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: <cluster-name>
  namespace: <namespace>
spec:
  clusterDef: <addon>
  topology: <topology>
  terminationPolicy: Delete
  componentSpecs:
    - name: <component>
      serviceVersion: "<version>"
      replicas: <N>
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Example: Create a MySQL Cluster (3 replicas)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: mysql-cluster
  namespace: default
spec:
  clusterDef: apecloud-mysql
  topology: apecloud-mysql
  terminationPolicy: Delete
  componentSpecs:
    - name: mysql
      serviceVersion: "8.0.30"
      replicas: 3
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Example: Create a PostgreSQL Cluster (2 replicas)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: pg-cluster
  namespace: default
spec:
  clusterDef: postgresql
  topology: postgresql
  terminationPolicy: Delete
  componentSpecs:
    - name: postgresql
      serviceVersion: "14.8.0"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Example: Create a Redis Cluster (2 shards)

```yaml
apiVersion: apps.kubeblocks.io/v1
kind: Cluster
metadata:
  name: redis-cluster
  namespace: default
spec:
  clusterDef: redis
  topology: redis-cluster
  terminationPolicy: Delete
  componentSpecs:
    - name: redis
      serviceVersion: "7.2.4"
      replicas: 2
      resources:
        limits:
          cpu: "0.5"
          memory: "0.5Gi"
        requests:
          cpu: "0.5"
          memory: "0.5Gi"
      volumeClaimTemplates:
        - name: data
          spec:
            accessModes: [ReadWriteOnce]
            resources:
              requests:
                storage: 20Gi
```

### Apply the YAML

Save the YAML to a file (e.g., `cluster.yaml`) and apply.

Before applying, validate with dry-run:

```bash
kubectl apply -f cluster.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f cluster.yaml
```

Or apply inline. Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
# paste YAML here
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
# paste YAML here
EOF
```

## Step 3: Verify Cluster Is Running

Watch the cluster status until it becomes `Running`:

```bash
kubectl get cluster <cluster-name> -n <namespace> -w
```

> **Success condition:** `.status.phase` = `Running` | **Typical:** 1-5min | **If stuck >10min:** `kubectl describe cluster <cluster-name> -n <namespace>`

Check all pods are Ready:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

Expected output (MySQL 3-replica example):

```
NAME                    READY   STATUS    RESTARTS   AGE
mysql-cluster-mysql-0   4/4     Running   0          2m
mysql-cluster-mysql-1   4/4     Running   0          90s
mysql-cluster-mysql-2   4/4     Running   0          60s
```

If pods are not Running, check events:

```bash
kubectl describe cluster <cluster-name> -n <namespace>
kubectl get events -n <namespace> --sort-by='.lastTimestamp' | grep <cluster-name>
```

## Step 4: Connect to the Cluster

### Get Connection Credentials

KubeBlocks auto-generates a Secret with the connection credentials:

```bash
kubectl get secret <cluster-name>-conn-credential -n <namespace> -o jsonpath='{.data.username}' | base64 -d
kubectl get secret <cluster-name>-conn-credential -n <namespace> -o jsonpath='{.data.password}' | base64 -d
```

### Port-Forward for Local Access

```bash
# MySQL
kubectl port-forward svc/<cluster-name>-mysql -n <namespace> 3306:3306

# PostgreSQL
kubectl port-forward svc/<cluster-name>-postgresql -n <namespace> 5432:5432

# Redis
kubectl port-forward svc/<cluster-name>-redis -n <namespace> 6379:6379

# MongoDB
kubectl port-forward svc/<cluster-name>-mongodb -n <namespace> 27017:27017
```

## Decision Tree

```
User wants to create a cluster
├── Which addon?
│   ├── MySQL       → clusterDef: apecloud-mysql or mysql
│   ├── PostgreSQL  → clusterDef: postgresql
│   ├── Redis       → clusterDef: redis
│   ├── MongoDB     → clusterDef: mongodb
│   ├── Kafka       → clusterDef: kafka
│   └── Other       → kubectl get clusterdefinitions
├── How many replicas?
│   ├── Dev/test    → 1 replica, terminationPolicy: Delete
│   └── Production  → 3+ replicas, terminationPolicy: DoNotTerminate
└── Resource sizing?
    ├── Dev/test    → 0.5 CPU, 0.5Gi memory, 20Gi storage
    └── Production  → 2+ CPU, 4Gi+ memory, 100Gi+ storage
```

## terminationPolicy

| Policy | Behavior | Recommended For |
|--------|----------|-----------------|
| `DoNotTerminate` | Blocks deletion; must patch to change | Production |
| `Delete` | Deletes cluster and PVCs, retains backups | Dev / test |
| `WipeOut` | Deletes everything including backups | Disposable environments |

> **Important:** For production clusters, always use `DoNotTerminate` to prevent accidental deletion.

## Troubleshooting

**Cluster stuck in `Creating` or `Updating`:**
- Check if the addon is installed: `helm list -n kb-system | grep kb-addon`
- Check pod events: `kubectl describe pod <pod-name> -n <namespace>`
- Check resource availability: `kubectl describe nodes`

**Image pull errors:**
- Verify image registry. If in China, ensure the addon uses the Aliyun mirror registry.

**Insufficient resources:**
- Reduce `resources.requests` or add more nodes to the cluster.

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).

## Reference

For detailed Cluster CR field descriptions and more addon examples, see [reference.md](references/reference.md).
