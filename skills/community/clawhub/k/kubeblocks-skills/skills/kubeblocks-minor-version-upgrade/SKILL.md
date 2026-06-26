---
name: kubeblocks-minor-version-upgrade
metadata:
  version: "0.1.0"
description: Upgrade the database engine minor version for KubeBlocks clusters via OpsRequest. Performs a rolling upgrade with minimal downtime. Use when the user wants to upgrade, update, or patch the database engine version (e.g. MySQL 8.0.33 to 8.0.35, PostgreSQL 14.7 to 14.10). NOT for upgrading the KubeBlocks operator itself (see KubeBlocks official upgrade docs) or for major version upgrades (e.g. MySQL 5.7 to 8.0, which requires data migration).
---

# Minor Version Upgrade

## Overview

KubeBlocks supports upgrading the database engine's minor version (e.g., MySQL 8.0.33 → 8.0.35, PostgreSQL 16.1 → 16.2). The upgrade performs a rolling update: secondary pods restart first, then a switchover promotes a secondary to primary, and finally the original primary restarts — minimizing downtime.

Official docs: https://kubeblocks.io/docs/preview/user_docs/handle-an-exception/upgrade-database-engine

## Pre-Check

Before proceeding, verify the cluster is healthy and no other operation is running:

```bash
# Cluster must be Running
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.status.phase}'

# No pending OpsRequests
kubectl get opsrequest -n <namespace> -l app.kubernetes.io/instance=<cluster-name> --field-selector=status.phase!=Succeed
```

If the cluster is not `Running` or has a pending OpsRequest, wait for it to complete before proceeding.

Check current version and available upgrade targets:

```bash
# Current version
kubectl get cluster <cluster-name> -n <namespace> -o jsonpath='{.spec.componentSpecs[*].serviceVersion}'

# Available versions
kubectl get cmpv
```

## Workflow

```
- [ ] Step 1: Check current version
- [ ] Step 2: List available versions
- [ ] Step 3: Update serviceVersion in Cluster CR
- [ ] Step 4: Verify upgrade
```

## Step 1: Check Current Version

```bash
kubectl get cluster <cluster> -n <ns> -o jsonpath='{.spec.componentSpecs[*].serviceVersion}'
```

Or check from the running pods:

```bash
kubectl get cluster <cluster> -n <ns> -o yaml | grep serviceVersion
```

## Step 2: List Available Versions

List available component versions for the addon:

```bash
kubectl get cmpv
```

Example output:

```
NAME                        VERSIONS                          AGE
apecloud-mysql              8.0.30, 8.0.33, 8.0.35           10d
postgresql                  14.11.0, 15.7.0, 16.4.0          10d
redis                       7.0.6, 7.2.4                      10d
mongodb                     6.0.5, 7.0.12                     10d
```

For detailed information about a specific version:

```bash
kubectl get cmpv <addon-name> -o yaml
```

This shows the exact image tags, compatibility rules, and supported version transitions.

## Step 3: Update serviceVersion

Edit the Cluster CR to set the new `serviceVersion`:

```bash
kubectl edit cluster <cluster> -n <ns>
```

Change the `serviceVersion` field in the relevant component spec:

```yaml
spec:
  componentSpecs:
  - name: <component>
    serviceVersion: "8.0.35"    # new version
    # ... rest of component spec
```

Or patch it directly. Before patching, validate with dry-run:

```bash
kubectl patch cluster <cluster> -n <ns> --type merge -p '
{
  "spec": {
    "componentSpecs": [
      {
        "name": "<component>",
        "serviceVersion": "<new-version>"
      }
    ]
  }
}' --dry-run=server
```

If dry-run reports errors, fix the patch before proceeding.

```bash
kubectl patch cluster <cluster> -n <ns> --type merge -p '
{
  "spec": {
    "componentSpecs": [
      {
        "name": "<component>",
        "serviceVersion": "<new-version>"
      }
    ]
  }
}'
```

## Step 4: Verify Upgrade

### Watch Rolling Upgrade Progress

```bash
kubectl get pods -n <ns> -l app.kubernetes.io/instance=<cluster> -w
```

> **Success condition:** All pods `.status.phase` = `Running` | **Typical:** 5-15min for rolling upgrade | **If stuck >20min:** `kubectl describe pod <pod> -n <ns>`

The rolling upgrade follows this sequence:
1. **Secondary pods** restart first with the new version
2. A **switchover** promotes an upgraded secondary to primary
3. The **original primary** (now secondary) restarts with the new version

This order matters: by upgrading secondaries first, the cluster maintains a working primary throughout the process. If a secondary fails to start on the new version, the primary is still on the old (known-good) version and the cluster remains fully operational — you can investigate and roll back without any write downtime. Upgrading the primary last also ensures the switchover only happens once, minimizing the brief write interruption to a single event.

Ref: https://kubeblocks.io/blog/in-place-updates

### Confirm New Version

```bash
# Check cluster spec
kubectl get cluster <cluster> -n <ns> -o jsonpath='{.spec.componentSpecs[*].serviceVersion}'

# Verify from the database itself
# MySQL
kubectl exec -it <pod> -n <ns> -- mysql -u root -p -e "SELECT VERSION();"

# PostgreSQL
kubectl exec -it <pod> -n <ns> -- psql -U postgres -c "SELECT version();"

# Redis
kubectl exec -it <pod> -n <ns> -- redis-cli INFO server | grep redis_version

# MongoDB
kubectl exec -it <pod> -n <ns> -- mongosh --eval "db.version()"
```

## Important Notes

- Only **minor version** upgrades are supported through this method (e.g., 8.0.33 → 8.0.35). Major version upgrades require migration.
- Always **backup before upgrading**: use the [backup](../kubeblocks-backup/SKILL.md) skill to create a full backup first.
- Check the `ComponentVersion` CR for supported upgrade paths — not all version transitions may be allowed.
- The rolling upgrade process ensures **zero downtime** for read traffic and only brief interruption for write traffic during switchover.

## Troubleshooting

**Upgrade stuck or pods in CrashLoopBackOff:**
- Check pod events: `kubectl describe pod <pod> -n <ns>`
- Check logs: `kubectl logs <pod> -n <ns>`
- The new version may be incompatible; check ComponentVersion for valid transitions

**Version not available:**
- Ensure the addon is installed with a version that includes the target engine version
- Update the addon: `helm upgrade kb-addon-<addon> kubeblocks/<addon> -n kb-system --version <addon-version>`

**Rollback:**
- Set `serviceVersion` back to the previous version to trigger a rollback
- This follows the same rolling restart process

For general agent safety conventions (dry-run, status confirmation, production protection), see [safety-patterns.md](../../references/safety-patterns.md).
