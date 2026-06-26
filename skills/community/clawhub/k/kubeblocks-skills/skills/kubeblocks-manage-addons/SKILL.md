---
name: kubeblocks-manage-addons
metadata:
  version: "0.1.0"
description: Install, uninstall, upgrade, and manage KubeBlocks database engine addons (MySQL, PostgreSQL, Redis, MongoDB, Kafka, Elasticsearch, Milvus, Qdrant, etc.). Use when the user wants to enable or disable a database engine, list available addons, or upgrade an addon version. NOT for creating database clusters (see kubeblocks-create-cluster or kubeblocks-addon-* skills) or installing the KubeBlocks operator itself (see kubeblocks-install).
---

# Manage KubeBlocks Addons

## Overview

Since KubeBlocks v0.8.0, database engine support is **decoupled from the core operator** and delivered as independent addons. Each addon provides ComponentDefinitions, configuration templates, and scripts for a specific database engine. You can install only the engines you need, keeping the cluster lightweight.

Official docs: https://kubeblocks.io/docs/preview/user_docs/references/install-addons
Supported addons list: https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons

## Prerequisites

- KubeBlocks operator is installed. If not, use the [install-kubeblocks](../kubeblocks-install/SKILL.md) skill first.
- Helm v3+ is available.
- `kubectl` has access to the target cluster.

## Workflow

```
- [ ] Step 1: Check currently installed addons
- [ ] Step 2: Add the KubeBlocks Helm repo
- [ ] Step 3: Install / Uninstall / Upgrade addons
- [ ] Step 4: Verify
```

## Default Auto-Installed Addons

When KubeBlocks is installed with default settings, these addons are auto-installed:

| Addon | Engine |
|---|---|
| `apecloud-mysql` | ApeCloud MySQL (HA MySQL with Raft consensus) |
| `mysql` | Community MySQL |
| `postgresql` | PostgreSQL |
| `redis` | Redis |
| `mongodb` | MongoDB |
| `kafka` | Apache Kafka |
| `etcd` | etcd |
| `qdrant` | Qdrant vector database |
| `rabbitmq` | RabbitMQ |

To skip auto-installation during KubeBlocks install, set `--set autoInstalledAddons="{}"`.

## Step 1: Check Currently Installed Addons

```bash
helm list -n kb-system | grep kb-addon
```

Example output:

```
kb-addon-mysql              kb-system   1   2024-12-01 10:00:00   deployed   mysql-1.0.2
kb-addon-postgresql         kb-system   1   2024-12-01 10:00:00   deployed   postgresql-1.0.2
kb-addon-redis              kb-system   1   2024-12-01 10:00:00   deployed   redis-1.0.2
```

You can also check the ComponentDefinitions registered by addons:

```bash
kubectl get componentdefinitions.apps.kubeblocks.io
```

## Step 2: Add the KubeBlocks Helm Repo

```bash
helm repo add kubeblocks https://apecloud.github.io/helm-charts
helm repo update
```

**China mainland users** — if GitHub Pages is slow or blocked, use the JiHuLab mirror:

```bash
helm repo add kubeblocks-addons https://jihulab.com/api/v4/projects/150246/packages/helm/stable
helm repo update
```

Then replace `kubeblocks/<addon-name>` with `kubeblocks-addons/<addon-name>` in all commands below.

## Step 3: Install / Uninstall / Upgrade Addons

### Search Available Addon Versions

```bash
helm search repo kubeblocks/<addon-name> --versions
```

Example:

```bash
helm search repo kubeblocks/elasticsearch --versions
```

### Install an Addon

```bash
helm install kb-addon-<name> kubeblocks/<name> \
  --namespace kb-system \
  --version <VERSION>
```

Example — install Elasticsearch addon v1.0.2:

```bash
helm install kb-addon-elasticsearch kubeblocks/elasticsearch \
  --namespace kb-system \
  --version 1.0.2
```

### Uninstall an Addon

**Important:** Delete all clusters using the addon before uninstalling.

```bash
# Check if any clusters use this addon
kubectl get cluster -A -o jsonpath='{range .items[*]}{.metadata.name}{"\t"}{.spec.componentSpecs[*].componentDef}{"\n"}{end}' | grep <addon-name>

# Uninstall
helm uninstall kb-addon-<name> --namespace kb-system
```

### Upgrade an Addon

```bash
helm upgrade kb-addon-<name> kubeblocks/<name> \
  --namespace kb-system \
  --version <NEW_VERSION>
```

## Version Compatibility

**Addon major version must match KubeBlocks major version.** Mismatched versions may cause unexpected errors.

| KubeBlocks Version | Required Addon Version |
|---|---|
| v1.0.x | v1.0.x (or 1.0.x without `v` prefix in Helm) |
| v0.9.x | v0.9.x |
| v0.8.x | v0.8.x |

Check your KubeBlocks version:

```bash
helm list -n kb-system | grep -w kubeblocks
```

## Custom Image Registry

If your cluster cannot pull from Docker Hub, specify a custom registry:

```bash
helm install kb-addon-<name> kubeblocks/<name> \
  --namespace kb-system \
  --version <VERSION> \
  --set image.registry=<your-registry>
```

**China mainland mirror:**

```bash
--set image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com
```

## Step 4: Verify

```bash
# Confirm the addon Helm release is deployed
helm list -n kb-system | grep kb-addon

# Check that ComponentDefinitions are registered
kubectl get componentdefinitions.apps.kubeblocks.io | grep <addon-name>

# Verify no errors in KubeBlocks operator logs
kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=50
```

## Common Addon Operations

### List All Available Addons

```bash
helm search repo kubeblocks/ | grep -v "^NAME"
```

### Bulk Install Multiple Addons

```bash
for addon in elasticsearch starrocks-ce milvus; do
  helm install kb-addon-${addon} kubeblocks/${addon} \
    --namespace kb-system \
    --version 1.0.2
done
```

### Bulk Uninstall All Addons

```bash
helm list -n kb-system | grep kb-addon | awk '{print $1}' | xargs -I {} helm -n kb-system uninstall {}
```

## Troubleshooting

**Addon install fails with "not found" error:**
- Run `helm repo update` to refresh the index.
- Verify the addon name: `helm search repo kubeblocks/ | grep <name>`

**Addon install succeeds but ComponentDefinition not found:**
- Check the KubeBlocks operator logs: `kubectl -n kb-system logs -l app.kubernetes.io/name=kubeblocks --tail=100`
- Ensure KubeBlocks `addonController.enabled` is `true` (default).

**Image pull errors in addon pods:**
- Switch to a custom registry: `--set image.registry=<registry>`
- For China, use: `--set image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com`

**Version mismatch warnings:**
- Confirm addon version matches KubeBlocks major version.
- Check: `helm list -n kb-system | grep kubeblocks` for the operator version.

## Reference

For a complete list of supported addons and their feature matrix, see [reference.md](references/reference.md).
