---
name: kubeblocks-cluster-lifecycle
metadata:
  version: "0.1.0"
description: "Manage KubeBlocks cluster lifecycle: stop, start, and restart database clusters via OpsRequest. Stopping terminates pods while retaining PVCs for cost savings. Use when the user wants to stop, start, restart, pause, resume, or shut down a database cluster temporarily. NOT for deleting a cluster permanently (see delete-cluster) or for scaling operations (see vertical-scaling, horizontal-scaling)."
---

# Manage Cluster Lifecycle: Stop, Start, Restart

## Overview

KubeBlocks supports stopping, starting, and restarting database clusters through `OpsRequest` CRs. Stopping a cluster terminates all pods while retaining PVCs, allowing cost savings when the cluster is not in use.

Official docs: https://kubeblocks.io/docs/preview/user_docs/maintenance/stop-start-a-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Workflow

```
- [ ] Step 1: Check current cluster status
- [ ] Step 2: Apply the lifecycle operation (Stop / Start / Restart)
- [ ] Step 3: Verify the operation
```

## Step 1: Check Current Cluster Status

```bash
kubectl get cluster <cluster-name> -n <namespace>
```

| Status | Meaning |
|--------|---------|
| `Running` | Cluster is healthy and serving traffic. Can be stopped or restarted. |
| `Stopped` | Cluster pods are terminated, PVCs retained. Can be started. |
| `Updating` | An operation is in progress. Wait for it to complete. |

## Step 2: Apply the Lifecycle Operation

### Stop a Cluster

Stops all pods in the cluster. PVCs are retained so data is preserved.

**OpsRequest method:**

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

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Stop
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

Apply:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: stop-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Stop
EOF
```

**Alternative — kubectl patch method:**

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":true}]}}'
```

> Replace `<component-name>` with the component name for the addon (e.g., `mysql`, `postgresql`, `redis`, `mongodb`, `kafka-combine`).

### Start a Cluster

Recreates pods from the retained PVCs, restoring the cluster to its previous state.

**OpsRequest method:**

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

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: start-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Start
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

Apply:

```bash
kubectl apply -f - <<'EOF'
apiVersion: apps.kubeblocks.io/v1beta1
kind: OpsRequest
metadata:
  name: start-<cluster-name>
  namespace: <namespace>
spec:
  clusterName: <cluster-name>
  type: Start
EOF
```

**Alternative — kubectl patch method:**

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"componentSpecs":[{"name":"<component-name>","stop":false}]}}'
```

### Restart a Cluster

Performs a rolling restart of specified components. Pods are restarted one at a time to maintain availability.

**OpsRequest method:**

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

Before applying, validate with dry-run:

```bash
kubectl apply -f - --dry-run=server <<'EOF'
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
EOF
```

If dry-run reports errors, fix the YAML before proceeding.

Apply:

```bash
kubectl apply -f - <<'EOF'
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
EOF
```

> **Note:** The `componentName` depends on the addon. Common values:
> - MySQL: `mysql`
> - PostgreSQL: `postgresql`
> - Redis: `redis`
> - MongoDB: `mongodb`
> - Kafka: `kafka-combine` (combined topology) or `kafka-broker` / `kafka-controller` (separated topology)

You can restart multiple components by adding more entries to the `restart` list.

## Step 3: Verify the Operation

### Monitor the OpsRequest

```bash
kubectl get ops -n <namespace> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 1-3min | **If stuck >5min:** `kubectl describe ops <ops-name> -n <namespace>`

Expected progression: `Pending` → `Running` → `Succeed`.

### Check Cluster Status

```bash
kubectl get cluster <cluster-name> -n <namespace> -w
```

> **Success condition:** Stop: `.status.phase` = `Stopped` | Start/Restart: `.status.phase` = `Running` | **Typical:** 1-3min | **If stuck >5min:** `kubectl describe cluster <cluster-name> -n <namespace>`

- After **Stop**: status changes to `Stopped`, all pods terminated.
- After **Start**: status changes to `Running`, all pods recreated.
- After **Restart**: status briefly shows `Updating`, then returns to `Running`.

### Check Pods

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

- After **Stop**: no pods found.
- After **Start** / **Restart**: all pods in `Running` state.

## Troubleshooting

**OpsRequest stuck in `Running`:**
- Check OpsRequest events: `kubectl describe ops <ops-name> -n <namespace>`
- Check KubeBlocks controller logs: `kubectl logs -n kb-system -l app.kubernetes.io/name=kubeblocks --tail=50`

**Start fails after Stop:**
- Ensure PVCs still exist: `kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>`
- If PVCs were manually deleted, the cluster cannot be started and must be recreated.

**Restart takes too long:**
- Rolling restart is sequential. For large clusters, it processes one pod at a time.
- Check if pods are stuck: `kubectl describe pod <pod-name> -n <namespace>`

## Additional Resources

For component names by engine, kubectl patch alternatives, cluster status transitions, and cost-saving patterns, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
