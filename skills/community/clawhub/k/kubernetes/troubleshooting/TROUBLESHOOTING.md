# TROUBLESHOOTING.md — Debugging Knowledge Base

> Log debugging knowledge, root causes, and solutions. Build institutional memory.

---

## Last Updated: 2026-02-24

---

## Template: Add New Entry

```
## Problem: <title>

### Symptoms
- <observable symptom 1>
- <observable symptom 2>

### Root Cause
<technical cause>

### Fix
<solution steps>

### Prevention
<how to prevent recurrence>

### Related Skills
- skill:cluster-ops:health-check
- skill:observability:alert-triage
```

---

## Common Problem Patterns

### Cluster Issues

| Problem | Quick Check | Skill |
|---------|-------------|-------|
| Node Not Ready | `kubectl get nodes` | cluster-ops:health-check |
| API Server Down | `kubectl cluster-info` | cluster-ops:health-check |
| Pod CrashLoopBackOff | `kubectl describe pod <name>` | dev-experience:debug-pod |
| etcd Issues | `kubectl exec -n kube-system etcd-0 -- etcdctl` | cluster-ops:etcd-backup |

### GitOps Issues

| Problem | Quick Check | Skill |
|---------|-------------|-------|
| Sync Failure | `argocd app get <app>` | gitops:argocd-app-sync |
| Drift Detected | `argocd app diff <app>` | gitops:drift-detect |
| Helm Upgrade Failed | `helm list -A` | gitops:helm-diff |

### Security Issues

| Problem | Quick Check | Skill |
|---------|-------------|-------|
| RBAC Misconfiguration | `kubectl auth can-i` | security:rbac-audit |
| Vulnerable Image | `trivy image <image>` | security:image-scan |
| Secret Exposed | Check pod logs/env | security:secret-rotation |

---

## Diagnostic Commands

### Quick Cluster Health
```bash
kubectl get nodes -o wide
kubectl get pods -A -o wide
kubectl get events -A --sort-by='.lastTimestamp'
```

### OpenShift Specific
```bash
oc get nodes -o wide
oc get co
oc status
```

### Logs & Metrics
```bash
kubectl logs <pod> -n <ns> --tail=100
kubectl top nodes
kubectl top pods -A
```

---

## Escalation Matrix

| Issue Type | First Agent | Escalation |
|------------|-------------|------------|
| Node issues | Atlas (cluster-ops) | @human |
| Deployment | Flow (gitops) | @human |
| Security | Shield (security) | @human IMMEDIATE |
| Performance | Pulse (observability) | @Atlas |
| Developer | Desk (dev-experience) | @Flow |

---

## Investigation Workflow

1. **Observe** — Gather symptoms, check status
2. **Hypothesize** — Form theory of cause
3. **Investigate** — Run diagnostic commands
4. **Verify** — Confirm root cause
5. **Fix** — Apply solution (requires approval if production)
6. **Document** — Log to TROUBLESHOOTING.md
7. **Prevent** — Add automation/guardrails

---

## Never Do Without Human Approval

- Delete any resource
- Modify RBAC
- Change cluster-wide policies
- Rollback production deployment
- Modify secrets
- Scale beyond limits
- Apply unknown YAML
- Execute ad-hoc scripts on production
