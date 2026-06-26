---
name: kubeblocks-delete-cluster
metadata:
  version: "0.1.0"
description: Safely delete a KubeBlocks database cluster with pre-deletion checks for backups, PVCs, and dependent resources. Use when the user wants to remove, delete, destroy, tear down, or clean up a database cluster. NOT for stopping a cluster temporarily (see kubeblocks-cluster-lifecycle) or uninstalling the KubeBlocks operator (see kubeblocks-install skill).
---

# Delete a KubeBlocks Database Cluster

## Overview

Safely remove a KubeBlocks-managed database cluster. This skill covers pre-deletion checks, handling the `terminationPolicy`, and cleaning up residual resources.

Official docs: https://kubeblocks.io/docs/preview/user_docs/kubeblocks-for-mysql/cluster-management/delete-mysql-cluster
Full doc index: https://kubeblocks.io/llms-full.txt

## Workflow

```
- [ ] Step 1: Pre-deletion checklist
- [ ] Step 2: Handle terminationPolicy
- [ ] Step 3: Delete the cluster
- [ ] Step 4: Verify deletion
- [ ] Step 5: Clean up residual resources (optional)
```

## Step 1: Pre-Deletion Checklist

Before deleting, confirm the following with the user:

### 1a: Identify the Cluster

```bash
kubectl get cluster -n <namespace>
```

### 1b: Check terminationPolicy

```bash
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.spec.terminationPolicy}'
```

| Policy | What Happens on Delete |
|--------|----------------------|
| `DoNotTerminate` | **Deletion is blocked.** Must patch before deleting. |
| `Delete` | Deletes pods and PVCs. Retains backups. |
| `WipeOut` | Deletes everything including backups. |

### 1c: Check for Existing Backups

```bash
kubectl get backup -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

If backups exist and the policy is `WipeOut`, **warn the user** that all backups will also be deleted.

### 1d: Check for Dependent Resources

```bash
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

Cancel any running OpsRequests before deleting:

```bash
kubectl delete opsrequest <ops-name> -n <namespace>
```

## Step 2: Handle terminationPolicy

If the current policy is `DoNotTerminate`, the cluster **cannot be deleted** until it is changed. Patch it:

```bash
kubectl patch cluster <cluster-name> -n <namespace> \
  --type merge -p '{"spec":{"terminationPolicy":"Delete"}}'
```

> **Warning:** Confirm with the user before changing from `DoNotTerminate`. This policy exists to protect production clusters from accidental deletion.

To also delete backups, use `WipeOut` instead of `Delete`.

## Step 3: Delete the Cluster

```bash
kubectl delete cluster <cluster-name> -n <namespace>
```

This may take a minute as KubeBlocks gracefully shuts down database instances and cleans up resources.

## Step 4: Verify Deletion

Confirm the cluster is gone:

```bash
kubectl get cluster <cluster-name> -n <namespace>
```

Expected output:

```
Error from server (NotFound): clusters.apps.kubeblocks.io "<cluster-name>" not found
```

Confirm pods are terminated:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

Expected: no resources found.

## Step 5: Clean Up Residual Resources (Optional)

### PVCs

If the `terminationPolicy` was `DoNotTerminate` (before patching) or if PVCs remain for any reason:

```bash
kubectl get pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

To delete them:

```bash
kubectl delete pvc -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

> **Caution:** Deleting PVCs permanently destroys data. Make sure backups exist if the data might be needed.

### Secrets

Connection credential secrets may remain:

```bash
kubectl get secret -n <namespace> | grep <cluster-name>
```

To delete them:

```bash
kubectl delete secret -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

### ConfigMaps

```bash
kubectl get configmap -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

To delete them:

```bash
kubectl delete configmap -n <namespace> -l app.kubernetes.io/instance=<cluster-name>
```

## Troubleshooting

**Cluster deletion hangs (stuck in `Deleting`):**
- Check for finalizers: `kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.metadata.finalizers}'`
- Check KubeBlocks controller logs: `kubectl logs -n kb-system -l app.kubernetes.io/name=kubeblocks --tail=50`

**`terminationPolicy` is `DoNotTerminate` and user forgot the policy:**
- The `kubectl delete` command will return an error. Patch the policy first (Step 2).

**PVCs remain after deletion:**
- This is expected if `terminationPolicy` was `DoNotTerminate`. Clean them up in Step 5.

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
