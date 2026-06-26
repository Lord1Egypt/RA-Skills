---
name: kubeblocks-volume-expansion
metadata:
  version: "0.1.0"
description: Expand persistent volume storage for KubeBlocks database clusters via OpsRequest. Requires the StorageClass to support volume expansion (allowVolumeExpansion=true). Use when the user needs more disk space, wants to increase storage, expand volumes, or resize PVCs. NOT for changing CPU/memory (see vertical-scaling) or adding more replicas (see horizontal-scaling). Note that volume shrinking is not supported by Kubernetes.
---

# Volume Expansion: Increase Storage

## Overview

Volume expansion increases the persistent storage allocated to a KubeBlocks database cluster. This is an online operation — pods continue running while the underlying PVCs are resized.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/expand-the-storage-of-a-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

> **Important:** Volumes can only be **expanded**, never shrunk. Plan storage capacity carefully.

## Prerequisites

The StorageClass must support volume expansion. Check:

```bash
kubectl get sc
```

Look for `ALLOWVOLUMEEXPANSION = true` in the output. If it shows `false`, the StorageClass does not support expansion and must be reconfigured by a cluster administrator:

```bash
kubectl get sc <storage-class-name> -o jsonpath='{.allowVolumeExpansion}'
```

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Check current PVC sizes and StorageClass expansion support:

```bash
# Current PVC sizes
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>

# StorageClass supports expansion
kubectl get sc -o custom-columns='NAME:.metadata.name,EXPANSION:.allowVolumeExpansion'
```

## Workflow

```
- [ ] Step 1: Check current storage and StorageClass
- [ ] Step 2: Apply volume expansion OpsRequest
- [ ] Step 3: Monitor the operation
- [ ] Step 4: Verify new storage size
```

## Step 1: Check Current Storage and StorageClass

Check current PVC sizes:

```bash
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

Check the cluster spec for storage configuration:

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep -A 6 volumeClaimTemplates
```

Verify StorageClass supports expansion:

```bash
kubectl get sc -o custom-columns='NAME:.metadata.name,PROVISIONER:.provisioner,EXPANSION:.allowVolumeExpansion'
```

## Step 2: Apply Volume Expansion OpsRequest

### OpsRequest Template

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: VolumeExpansion
  volumeExpansion:
    - componentName: <component-name>
      volumeClaimTemplates:
        - name: <volume-name>
          storage: "<new-size>"
```

### Volume Name Reference

| Addon | Volume Name | Description |
|-------|-----------|-------------|
| MySQL | `data` | Data directory |
| PostgreSQL | `data` | Data directory |
| Redis | `data` | Data directory |
| MongoDB | `data` | Data directory |
| Kafka | `data` | Data logs |
| Kafka | `metadata` | Metadata directory |

### Example: Expand MySQL Data Volume to 50Gi

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: mysql
      volumeClaimTemplates:
        - name: data
          storage: "50Gi"
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: mysql
      volumeClaimTemplates:
        - name: data
          storage: "50Gi"
EOF
```

### Example: Expand PostgreSQL Data Volume to 100Gi

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: postgresql
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: postgresql
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
EOF
```

### Example: Expand Kafka Data and Metadata Volumes

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-kafka-cluster
  namespace: default
spec:
  clusterName: kafka-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: kafka-combine
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
        - name: metadata
          storage: "20Gi"
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: volumeexpand-kafka-cluster
  namespace: default
spec:
  clusterName: kafka-cluster
  type: VolumeExpansion
  volumeExpansion:
    - componentName: kafka-combine
      volumeClaimTemplates:
        - name: data
          storage: "100Gi"
        - name: metadata
          storage: "20Gi"
EOF
```

### Expand Multiple Components

```yaml
spec:
  volumeExpansion:
    - componentName: kafka-broker
      volumeClaimTemplates:
        - name: data
          storage: "200Gi"
    - componentName: kafka-controller
      volumeClaimTemplates:
        - name: data
          storage: "50Gi"
```

## Step 3: Monitor the Operation

Watch the OpsRequest:

```bash
kubectl get ops volumeexpand-<cluster-name> -n <namespace> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 1-5min | **If stuck >10min:** `kubectl describe ops volumeexpand-<cluster-name> -n <namespace>`

Expected progression: `Pending` → `Running` → `Succeed`.

Watch PVC resize:

```bash
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name> -w
```

## Step 4: Verify New Storage Size

After the OpsRequest succeeds, confirm PVC sizes:

```bash
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

Check the `CAPACITY` column reflects the new size.

Also verify from inside a pod:

```bash
kubectl exec -it <cluster-name>-<component>-0 -n <namespace> -- df -h /data
```

## Troubleshooting

**OpsRequest fails with "volume expansion not supported":**
- The StorageClass does not allow expansion. Check: `kubectl get sc <name> -o jsonpath='{.allowVolumeExpansion}'`
- Ask the cluster admin to enable it: `kubectl patch sc <name> -p '{"allowVolumeExpansion": true}'`

**PVC resize stuck in `FileSystemResizePending`:**
- Some storage providers require a pod restart to complete the filesystem resize. KubeBlocks handles this automatically, but it may take a few minutes.
- Check PVC conditions: `kubectl describe pvc <pvc-name> -n <namespace>`

**Cannot shrink volumes:**
- This is a Kubernetes limitation. Volumes can only be expanded, never shrunk.
- If smaller storage is needed, create a new cluster with the desired size and migrate data.

**Expansion for `log` or `metadata` volumes:**
- Some addons define additional volumes (e.g., Kafka's `metadata` volume). Use the correct volume name from the reference table above.

For complete volume name reference across all addons, additional OpsRequest examples (Redis, MongoDB, Elasticsearch, Milvus), and StorageClass expansion support by cloud provider, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
