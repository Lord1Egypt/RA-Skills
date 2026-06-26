---
name: kubeblocks-vertical-scaling
metadata:
  version: "0.1.0"
description: Scale CPU and memory resources for KubeBlocks database clusters via OpsRequest (vertical scaling). Supports in-place updates when the feature gate is enabled. Use when the user wants to change, increase, decrease, resize, or adjust CPU or memory resources of a database cluster. NOT for adding/removing replicas or shards (see horizontal-scaling) or expanding disk storage (see volume-expansion).
---

# Vertical Scaling: Change CPU and Memory

## Overview

Vertical scaling adjusts the CPU and memory resources allocated to a KubeBlocks database cluster. KubeBlocks performs rolling updates — secondary/replica pods are updated first, then the primary, to minimize downtime.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/scale-a-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Check current resource allocations:

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep -A 4 resources
```

## Workflow

```
- [ ] Step 1: Check current resources
- [ ] Step 2: Apply vertical scaling OpsRequest
- [ ] Step 3: Monitor the operation
- [ ] Step 4: Verify new resources
```

## Step 1: Check Current Resources

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep -A 8 resources
```

Or inspect a specific pod:

```bash
kubectl get pod <cluster-name>-<component>-0 -n <namespace> -o jsonpath='{.spec.containers[0].resources}' | jq .
```

## Step 2: Apply Vertical Scaling OpsRequest

### OpsRequest Template

```yaml
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: verticalscaling-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: VerticalScaling
  verticalScaling:
    - componentName: <component-name>
      requests:
        cpu: "<new-cpu-request>"
        memory: "<new-memory-request>"
      limits:
        cpu: "<new-cpu-limit>"
        memory: "<new-memory-limit>"
```

### Example: Scale MySQL to 2 CPU / 4Gi Memory

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: verticalscaling-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: VerticalScaling
  verticalScaling:
    - componentName: mysql
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: verticalscaling-mysql-cluster
  namespace: default
spec:
  clusterName: mysql-cluster
  type: VerticalScaling
  verticalScaling:
    - componentName: mysql
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
EOF
```

### Example: Scale PostgreSQL to 1 CPU / 2Gi Memory

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: verticalscaling-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: VerticalScaling
  verticalScaling:
    - componentName: postgresql
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "1"
        memory: "2Gi"
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: verticalscaling-pg-cluster
  namespace: default
spec:
  clusterName: pg-cluster
  type: VerticalScaling
  verticalScaling:
    - componentName: postgresql
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "1"
        memory: "2Gi"
EOF
```

> **Component name reference:**
> - MySQL: `mysql`
> - PostgreSQL: `postgresql`
> - Redis: `redis`
> - MongoDB: `mongodb`
> - Kafka: `kafka-combine` (combined) or `kafka-broker` / `kafka-controller` (separated)

### Scale Multiple Components

For clusters with multiple components, add entries to the `verticalScaling` list:

```yaml
spec:
  verticalScaling:
    - componentName: kafka-broker
      requests:
        cpu: "2"
        memory: "4Gi"
      limits:
        cpu: "2"
        memory: "4Gi"
    - componentName: kafka-controller
      requests:
        cpu: "1"
        memory: "2Gi"
      limits:
        cpu: "1"
        memory: "2Gi"
```

## Step 3: Monitor the Operation

Watch the OpsRequest status:

```bash
kubectl get ops verticalscaling-<cluster-name> -n <namespace> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 1-5min | **If stuck >10min:** `kubectl describe ops verticalscaling-<cluster-name> -n <namespace>`

Expected progression: `Pending` → `Running` → `Succeed`.

Watch the cluster status:

```bash
kubectl get cluster <cluster-name> -n <namespace> -w
```

> **Success condition:** `.status.phase` = `Running` | **Typical:** 1-5min | **If stuck >10min:** `kubectl describe cluster <cluster-name> -n <namespace>`

The cluster status will transition: `Running` → `Updating` → `Running`.

Watch pods being rolling-restarted:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name> -w
```

> **Success condition:** `.status.phase` = `Running` | **Typical:** 1-5min | **If stuck >10min:** `kubectl describe pod <pod-name> -n <namespace>`

> **Rolling update order:** KubeBlocks updates secondary/replica pods first, then the primary pod. This minimizes downtime by ensuring at least one instance is always serving.

## Step 4: Verify New Resources

After the OpsRequest succeeds:

```bash
kubectl get cluster <cluster-name> -n <namespace> -o yaml | grep -A 8 resources
```

Or check a pod directly:

```bash
kubectl get pod <cluster-name>-<component>-0 -n <namespace> -o jsonpath='{.spec.containers[0].resources}' | jq .
```

## Troubleshooting

**OpsRequest fails or is rejected:**
- Check events: `kubectl describe ops <ops-name> -n <namespace>`
- Ensure the cluster is in `Running` state before scaling.
- Ensure requested resources do not exceed node capacity: `kubectl describe nodes`

**Pods stuck in `Pending` after scaling:**
- The node may lack sufficient resources. Check: `kubectl describe pod <pod-name> -n <namespace>`
- Consider adding more nodes or reducing the resource request.

**Scaling takes too long:**
- Rolling updates are sequential. Each pod must be fully ready before the next is updated.
- For large clusters, this is expected behavior.

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
