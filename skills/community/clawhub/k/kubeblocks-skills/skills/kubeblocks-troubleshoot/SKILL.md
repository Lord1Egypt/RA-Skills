---
name: kubeblocks-troubleshoot
metadata:
  version: "0.1.0"
description: "Diagnostic guide for KubeBlocks-managed database clusters. Use when the user reports troubleshoot, debug, diagnose, not working, error, failed, stuck, CrashLoopBackOff, cluster exception, or similar problems with their database cluster. This skill guides the agent through diagnostic steps — it does NOT perform actions."
---

# Troubleshoot KubeBlocks Clusters

## Overview

This skill helps diagnose and fix common issues with KubeBlocks-managed database clusters. Follow the diagnostic flowchart and sections below to systematically identify root causes. **This skill guides the agent through diagnostic steps; it does not perform actions.**

## Quick Diagnostic Flowchart

```
User reports cluster problem
│
├─ Is the KubeBlocks operator healthy?
│  └─ kubectl -n kb-system get pods
│     ├─ Pods not Running → Operator Issues (Section 5)
│     └─ Pods Running → continue
│
├─ Is the cluster in an abnormal state?
│  └─ kubectl get cluster <name> -n <ns>
│     ├─ Phase: Creating/Updating/Abnormal/Deleting → Cluster Status Issues (Section 1)
│     └─ Phase: Running → continue
│
├─ Is there a failed OpsRequest?
│  └─ kubectl get opsrequest -n <ns>
│     ├─ Failed/Running (stuck) → OpsRequest Failures (Section 3)
│     └─ Succeeded → continue
│
└─ Are pods crashing?
   └─ kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster>
      ├─ CrashLoopBackOff/ImagePullBackOff/Pending → Pod Issues (Section 2)
      └─ All Running → check pod logs and events for application errors
```

## 1. Cluster Status Issues

### Cluster stuck in `Creating`

| Cause | How to verify | Action |
|-------|---------------|--------|
| Addon not installed | `kubectl get addon` | Install the required addon (e.g. `kbcli addon enable mysql`) |
| Insufficient resources | `kubectl describe pod <pending-pod>` → Events | Increase node resources or reduce cluster requests |
| Image pull errors | `kubectl describe pod` → ImagePullBackOff | Fix registry access, image name, or imagePullSecrets |

### Cluster stuck in `Updating`

1. Check if all pods are `Running`: `kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster>`
2. Check pod logs for errors: `kubectl logs <pod> -c <container>`
3. Verify pod roles: `kubectl get po <pod> -L kubeblocks.io/role`
4. Check for failed OpsRequest: `kubectl get opsrequest -n <ns>` and `kubectl describe opsrequest <name>`
5. Ensure container image in `status.containerStatuses` matches `spec.containers.image`; mismatches can block updates

### Cluster in `Abnormal`

Usually caused by pod failures or storage issues. Check pod status and events (see Pod Issues below), then `kubectl describe cluster <name> -n <ns>` for conditions.

### Cluster stuck in `Deleting`

If KubeBlocks logs show `has no pods to running the pre-terminate action`, the cluster cannot run the pre-terminate lifecycle. To skip:

```bash
kubectl annotate component <COMPONENT_NAME> -n <ns> apps.kubeblocks.io/skip-pre-terminate-action=true
```

## 2. Pod Issues

### CrashLoopBackOff

1. **Check logs**: `kubectl logs <pod> -c <container> --previous`
2. **Describe pod**: `kubectl describe pod <pod> -n <ns>` (check Events)
3. **Common causes**: Wrong config, bad credentials, storage mount failure, OOM, database init failure

### ImagePullBackOff

1. **Describe pod**: `kubectl describe pod <pod>` → Events show pull error
2. **Common causes**: Private registry without `imagePullSecrets`, wrong image name/tag, network/registry unreachable

### Pending

1. **Describe pod**: `kubectl describe pod <pod>` → Events
2. **Common causes**: Insufficient CPU/memory, no nodes matching nodeSelector/affinity, PVC pending (StorageClass or capacity)

## 3. OpsRequest Failures

### How to check failed OpsRequest

```bash
kubectl get opsrequest -n <namespace>
kubectl describe opsrequest <ops-name> -n <namespace>
```

Check `status.conditions` and Events for failure reason.

### Common OpsRequest failure reasons

- Resource constraints (scaling beyond available capacity)
- Preconditions not met (e.g. cluster not Running)
- Timeout or step failure during the operation

### How to cancel a stuck OpsRequest

Only `VerticalScaling` and `HorizontalScaling` OpsRequests in `Running` state can be cancelled:

```bash
kubectl patch opsrequest <OPSREQUEST_NAME> -n <ns> -p '{"spec":{"cancel":true}}' --type=merge
```

## 4. Operator Issues

### KubeBlocks operator pod not running

```bash
kubectl -n kb-system get pods
kubectl -n kb-system describe pod <kubeblocks-pod>
```

### CRD version mismatch

If installing on K8s ≤ 1.23, you may see `unknown field "x-kubernetes-validations"`. Apply CRDs with `--validate=false` (see official docs).

### Check operator logs

```bash
kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100 -f
# or
kubectl -n kb-system logs deployments/kubeblocks -f
```

### ComponentDefinition status Unavailable

If `kubectl get componentdefinition` shows `Unavailable` (e.g. "immutable fields can't be updated"):

```bash
kubectl annotate componentdefinition <NAME> apps.kubeblocks.io/skip-immutable-check=true
```

## 5. Useful Commands Reference

| Purpose | Command |
|---------|---------|
| Operator health | `kubectl -n kb-system get pods` |
| Cluster status | `kubectl get cluster -A` |
| Cluster details | `kubectl describe cluster <name> -n <ns>` |
| OpsRequest status | `kubectl get opsrequest -n <ns>` |
| Pod status | `kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster>` |
| Pod logs | `kubectl logs <pod> -c <container> -n <ns>` |
| Pod events | `kubectl describe pod <pod> -n <ns>` |
| Operator logs | `kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100` |
| Cluster resources | `kubectl get cmp,its,po -l app.kubernetes.io/instance=<cluster> -n <ns>` |
| Generate report | `kbcli report cluster <name> --with-logs --mask` |

## 6. Official Troubleshooting Docs

| Resource | URL |
|----------|-----|
| FAQs (cluster exception) | https://kubeblocks.io/docs/preview/user_docs/troubleshooting/handle-a-cluster-exception |
| Known Issues | https://kubeblocks.io/docs/preview/user_docs/troubleshooting/known-issues |
| Full doc index | https://kubeblocks.io/llms-full.txt |

### Known issues to check

- **PostgreSQL password with special chars** (v0.9.4 and before, v1.0.0): Upgrade to v1.0.1-beta.6+ or set `symbolCharacters` in `passwordConfig` to avoid YAML parsing errors.
- **Excessive secrets** (KubeBlocks v1.0.0 on K8s ≤ 1.24): Upgrade to v1.0.1-beta.3+.
