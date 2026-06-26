# Safety Patterns for Agent Operations

This document defines the safety conventions that all KubeBlocks skills should follow. When writing or updating a skill, reference this document instead of duplicating the rules.

## 1. Dry-Run Before Apply

Every `kubectl apply` of a Cluster, OpsRequest, Backup, or any other KubeBlocks CR should be preceded by a server-side dry-run. This catches RBAC issues, webhook rejections, quota violations, and schema errors before any real change occurs.

```bash
kubectl apply -f <yaml-file-or-stdin> --dry-run=server
```

If the dry-run reports errors, fix the YAML before proceeding. Only after a clean dry-run should the agent run the actual `kubectl apply`.

For `kubectl delete`, dry-run is not applicable — use the pre-deletion checklist instead (see section 3).

## 2. Status Confirmation After Apply

After applying a change, confirm the operation reached its expected end-state. Use `kubectl get <resource> -w` to watch status transitions.

Each watch step should have three things clearly defined:

- **Success condition**: the specific `.status.phase` value that means "done"
- **Typical duration**: how long this normally takes
- **Timeout threshold**: how long to wait before suspecting a problem and running `kubectl describe`

### Status Condition Quick Reference

| Resource | Success Condition | Typical Duration | Timeout / Investigate After |
|---|---|---|---|
| Cluster (create/restore) | `.status.phase` = `Running` | 1-5 min | 10 min |
| Cluster (stop) | `.status.phase` = `Stopped` | 1-3 min | 5 min |
| Cluster (start/restart) | `.status.phase` = `Running` | 1-3 min | 5 min |
| OpsRequest (general) | `.status.phase` = `Succeed` | 1-5 min | 10 min |
| OpsRequest (reconfigure, static params) | `.status.phase` = `Succeed` (may pass through `Restarting`) | 2-8 min | 15 min |
| Backup (full) | `.status.phase` = `Completed` | Varies by data size | 30 min |
| Backup (continuous) | `.status.phase` = `Running` (stays running) | 1 min to start | 5 min |

### When Timeout Is Reached

If the resource has not reached its success condition within the timeout threshold:

```bash
# For Cluster
kubectl describe cluster <name> -n <ns>
kubectl get events -n <ns> --sort-by='.lastTimestamp' | grep <name>

# For OpsRequest
kubectl describe ops <name> -n <ns>

# For Backup
kubectl describe backup <name> -n <ns>

# For Pods
kubectl describe pod <pod-name> -n <ns>
kubectl logs <pod-name> -n <ns> --tail=50
```

Report the findings to the user rather than continuing blindly.

## 3. Pre-Deletion Checklist

Before deleting any cluster, list what will be affected and get explicit confirmation from the user:

1. Show the cluster's `terminationPolicy`:
   ```bash
   kubectl get cluster <name> -n <ns> -o jsonpath='{.spec.terminationPolicy}'
   ```
2. If `WipeOut`, warn that backups will also be deleted
3. List existing backups:
   ```bash
   kubectl get backup -n <ns> -l app.kubernetes.io/instance=<name>
   ```
4. List running OpsRequests (must be cancelled first):
   ```bash
   kubectl get opsrequest -n <ns> -l app.kubernetes.io/instance=<name>
   ```
5. Ask the user to confirm before proceeding

## 4. Production Cluster Protection

If a cluster has `terminationPolicy: DoNotTerminate`, treat it as a production cluster:

- **Any destructive operation** (delete, scale-in, stop) should trigger a warning and explicit confirmation
- **Changing terminationPolicy** requires the agent to explain the implications before patching
- Recommend creating a backup before any risky operation (switchover, upgrade, reconfigure)

## 5. Pre-Check Before Day-2 Operations

Before executing any Day-2 operation, verify the cluster is in a healthy state:

```bash
# Cluster must be Running (not Updating, Creating, or Stopped)
kubectl get cluster <name> -n <ns> -o jsonpath='{.status.phase}'

# No pending OpsRequests (only one OpsRequest can run at a time)
kubectl get opsrequest -n <ns> -l app.kubernetes.io/instance=<name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, inform the user and wait rather than stacking operations.
