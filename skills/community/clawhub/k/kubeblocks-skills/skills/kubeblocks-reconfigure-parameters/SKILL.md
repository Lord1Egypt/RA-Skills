---
name: kubeblocks-reconfigure-parameters
metadata:
  version: "0.1.0"
description: Modify database configuration parameters for KubeBlocks clusters via OpsRequest. Supports dynamic parameters (applied without restart) and static parameters (require pod restart). Use when the user wants to change, tune, modify, optimize, or adjust database settings, config, or parameters (e.g. max_connections, innodb_buffer_pool_size, shared_buffers). NOT for changing cluster resource limits (see vertical-scaling) or managing database user accounts (see manage-accounts).
---

# Reconfigure Database Parameters

## Overview

KubeBlocks allows modifying database configuration parameters through the `OpsRequest` CR with `type: Reconfiguring`. Parameters are categorized as:

- **Dynamic**: Applied immediately without restart (e.g. `max_connections` for MySQL)
- **Static**: Requires a rolling restart of pods to take effect (e.g. `innodb_buffer_pool_size` for MySQL)

KubeBlocks automatically determines whether a restart is needed based on the parameter type.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/configuration/configure-cluster-parameters

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Check current parameter values via the relevant ConfigMap:

```bash
kubectl get configmap -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Workflow

```
- [ ] Step 1: Identify the parameter to change
- [ ] Step 2: Create Reconfiguring OpsRequest
- [ ] Step 3: Verify the change
```

## Step 1: Identify the Parameter

Check current configuration values:

```bash
# List config templates for the cluster
kubectl get configurations -n <ns> -l app.kubernetes.io/instance=<cluster>
```

For a reference of common parameters per addon, see [reference.md](references/reference.md).

## Step 2: Create Reconfiguring OpsRequest

### Single Parameter Change

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-reconfigure
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Reconfiguring
  reconfigures:
  - componentName: <component>
    parameters:
    - key: max_connections
      value: "500"
```

### Multiple Parameters

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-reconfigure
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Reconfiguring
  reconfigures:
  - componentName: <component>
    parameters:
    - key: max_connections
      value: "500"
    - key: innodb_buffer_pool_size
      value: "2147483648"
```

Before applying, validate with dry-run:

```bash
kubectl apply -f reconfigure-ops.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f reconfigure-ops.yaml
```

## Step 3: Verify the Change

### Watch OpsRequest Status

```bash
kubectl get ops <cluster>-reconfigure -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 2-8min | **If stuck >15min:** `kubectl describe ops <cluster>-reconfigure -n <ns>`

Status progression:
- `Pending` → `Running` → `Succeed` (dynamic parameters)
- `Pending` → `Running` → `Restarting` → `Succeed` (static parameters, triggers rolling restart)

### Verify Parameter Value

Connect to the database and check:

```bash
# MySQL
kubectl exec -it <pod> -n <ns> -- mysql -u root -p -e "SHOW VARIABLES LIKE 'max_connections';"

# PostgreSQL
kubectl exec -it <pod> -n <ns> -- psql -U postgres -c "SHOW max_connections;"

# Redis
kubectl exec -it <pod> -n <ns> -- redis-cli CONFIG GET maxmemory
```

## Dynamic vs Static Parameters

| Behavior | Dynamic | Static |
|----------|---------|--------|
| Restart required | No | Yes (rolling restart) |
| Downtime | None | Brief per-pod during rolling restart |
| Effect | Immediate | After pod restart |

KubeBlocks handles the restart automatically for static parameters. Secondary pods restart first, then a switchover occurs, and the original primary restarts last — minimizing downtime.

## Troubleshooting

**OpsRequest fails with validation error:**
- Check that the parameter key exists for the addon
- Verify the value is within the allowed range
- Ensure the component name is correct: `kubectl get cluster <cluster> -n <ns> -o jsonpath='{.spec.componentSpecs[*].name}'`

**Rolling restart takes too long:**
- Static parameter changes trigger sequential pod restarts
- Check pod status: `kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> -w`

## Additional Reference

For a list of common tunable parameters per database addon, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
