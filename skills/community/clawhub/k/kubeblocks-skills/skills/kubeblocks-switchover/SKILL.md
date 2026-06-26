---
name: kubeblocks-switchover
metadata:
  version: "0.1.0"
description: Perform planned primary-secondary switchover for KubeBlocks database clusters via OpsRequest. Promotes a replica to primary with minimal downtime. Use when the user wants to promote a replica, switch primary, change leader, perform a planned failover, or do maintenance on the current primary node. NOT for unplanned failover recovery (handled automatically by HA middleware like Patroni, Orchestrator, or Sentinel) or restarting all pods (see kubeblocks-cluster-lifecycle).
---

# Switchover Primary-Secondary

## Overview

A switchover is a **planned** operation that promotes a secondary replica to primary and demotes the current primary to secondary. This is useful for maintenance, load rebalancing, or pre-failover testing.

Switchover is only available for addons with primary/secondary replication roles:
- MySQL / ApeCloud MySQL
- PostgreSQL
- Redis (replication mode)
- MongoDB (replica set)

Official docs: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/switchover

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Verify the cluster has 2+ replicas and check current roles:

```bash
kubectl get pods -n <namespace> -l app.kubernetes.io/instance=<cluster-name> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Switchover requires at least 2 replicas. If only 1 replica exists, scale out first (see [horizontal-scaling](../kubeblocks-horizontal-scaling/SKILL.md)).

## Workflow

```
- [ ] Step 1: Check current roles
- [ ] Step 2: Perform switchover via OpsRequest
- [ ] Step 3: Verify new roles
```

## Step 1: Check Current Roles

Identify which pod is the current primary:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Example output:

```
mycluster-mysql-0    primary
mycluster-mysql-1    secondary
mycluster-mysql-2    secondary
```

## Step 2: Perform Switchover

### Switchover via OpsRequest

```yaml
apiVersion: operations.kubeblocks.io/v1alpha1
kind: OpsRequest
metadata:
  name: <cluster>-switchover
  namespace: <ns>
spec:
  clusterName: <cluster>
  type: Switchover
  switchover:
  - componentName: <component>
    instanceName: <current-primary-pod>
```

- `componentName`: the component name from the Cluster spec (e.g. `mysql`, `postgresql`)
- `instanceName`: the pod name of the **current primary** that should be demoted

Before applying, validate with dry-run:

```bash
kubectl apply -f switchover-ops.yaml --dry-run=server
```

If dry-run reports errors, fix the YAML before proceeding.

Apply it:

```bash
kubectl apply -f switchover-ops.yaml
kubectl get ops <cluster>-switchover -n <ns> -w
```

> **Success condition:** `.status.phase` = `Succeed` | **Typical:** 1-3min | **If stuck >5min:** `kubectl describe ops <cluster>-switchover -n <ns>`

Status will progress: `Pending` → `Running` → `Succeed`

## Step 3: Verify New Roles

After the OpsRequest succeeds, confirm the roles have changed:

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> \
  -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.metadata.labels.kubeblocks\.io/role}{"\n"}{end}'
```

Expected: a different pod should now have the `primary` role.

Also verify replication health:

```bash
# MySQL: check replication status
kubectl exec -it <new-secondary-pod> -n <ns> -- mysql -u root -p -e "SHOW REPLICA STATUS\G"

# PostgreSQL: check replication
kubectl exec -it <primary-pod> -n <ns> -- psql -U postgres -c "SELECT * FROM pg_stat_replication;"
```

## Important Notes

- Switchover is a **planned** operation, not a failover. The current primary must be healthy and reachable.
- During switchover, there is a brief period where writes are unavailable (typically seconds).
- Client connections to the primary service are automatically re-routed after switchover completes.
- KubeBlocks uses the HA proxy or service endpoint to ensure clients connect to the new primary.

### Switchover vs Failover

A **switchover** is initiated by the operator (you) when both primary and secondaries are healthy — for example, before node maintenance, to rebalance load, or to test your HA setup. Because the current primary is still running, it can gracefully finish in-flight transactions and hand off leadership cleanly, resulting in minimal downtime (seconds).

A **failover** happens automatically when the primary crashes or becomes unreachable. HA middleware (Patroni for PostgreSQL, Orchestrator for MySQL, Sentinel for Redis, or the built-in MongoDB election) detects the failure and promotes a secondary without human intervention. You typically don't need to trigger a failover manually — the HA stack handles it.

### Best Practice: Backup Before Switchover

While switchover is designed to be safe, creating a backup beforehand provides an extra safety net — especially if your application is sensitive to replication lag or you're performing switchover as part of a larger maintenance window.

## Troubleshooting

**Switchover OpsRequest fails:**
- Ensure the cluster has more than one replica
- Verify the current primary pod name is correct
- Check that all pods are in Running state before switchover

**Roles not updated after switchover:**
- Wait a few seconds for label propagation
- Check OpsRequest events: `kubectl describe ops <name> -n <ns>`

**Replication lag after switchover:**
- The new secondary (former primary) may need time to catch up
- Monitor with: `kubectl exec -it <pod> -n <ns> -- <db-specific-replication-check>`

## Additional Reference

For per-engine switchover behaviors, HA middleware details (Orchestrator, Patroni, Sentinel), and complete replication health check commands for MySQL/PostgreSQL/Redis/MongoDB, see [reference.md](references/reference.md).

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
