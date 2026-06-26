---
name: kubeblocks-upgrade
metadata:
  version: "0.1.0"
description: Upgrade the KubeBlocks operator itself via Helm. Covers update operator, upgrade to v1.0, update kubeblocks version, and CRD updates. Use when the user wants to upgrade KubeBlocks, update the operator, or upgrade to a new KubeBlocks release. NOT for upgrading database engine versions (see minor-version-upgrade).
---

# Upgrade KubeBlocks Operator

## Overview

This skill covers upgrading the KubeBlocks operator (the controller that manages database clusters). The upgrade is done via `helm upgrade` on the kubeblocks chart. **Running database clusters are not affected** — they keep running during the operator upgrade. After upgrading the operator, addons may need to be upgraded separately.

Official docs: [Upgrade to v1.0.x](https://kubeblocks.io/docs/preview/user_docs/upgrade/upgrade-to-v10x), [Upgrade to v0.9.x](https://kubeblocks.io/docs/preview/user_docs/upgrade/upgrade-to-v09-version)

## Workflow

```
- [ ] Step 1: Check current version
- [ ] Step 2: Pre-upgrade checklist
- [ ] Step 3: Update CRDs
- [ ] Step 4: Helm upgrade
- [ ] Step 5: Verify operator pods
- [ ] Step 6: Upgrade addons (optional)
```

## Step 1: Check Current Version

```bash
helm list -n kb-system | grep kubeblocks
```

Or with kbcli: `kbcli version`

**Upgrade paths:**
| Current | Target v1.0.x | Target v0.9.x |
|---------|---------------|---------------|
| v1.0.x  | ✅ Direct     | N/A           |
| v0.9.x  | ❌ Not supported | ✅ Direct  |
| v0.8.x  | ❌ Upgrade to v0.9.x first | ✅ Direct (extra steps) |
| v0.7.x or earlier | ❌ Upgrade to v0.8 first | ❌ Upgrade to v0.8 first |

## Step 2: Pre-Upgrade Checklist

- **Backup important clusters** using the [backup](../kubeblocks-backup/SKILL.md) skill
- **Read release notes** for the target version: https://kubeblocks.io/docs/preview/user_docs/release_notes
- For **v0.8 → v0.9** or **v0.9 → v1.0**: follow the version-specific docs; major jumps require intermediate steps

## Step 3: Update CRDs

CRDs are separate from the Helm chart. Update them before the helm upgrade:

```bash
# Replace {VERSION} with target version, e.g. v1.0.2
kubectl replace -f https://github.com/apecloud/kubeblocks/releases/download/{VERSION}/kubeblocks_crds.yaml
```

For **v0.9.x same-minor upgrade** (e.g. v0.9.1 → v0.9.5), you can skip CRD update and use `--set crd.enabled=false` in Step 4 for faster deployment.

## Step 4: Helm Upgrade

### 4a: Update Helm Repo

```bash
helm repo add kubeblocks https://apecloud.github.io/helm-charts
helm repo update kubeblocks
```

### 4b: Upgrade

**Global network (docker.io):**

```bash
helm -n kb-system upgrade kubeblocks kubeblocks/kubeblocks --version {VERSION}
```

**China mainland network:**

```bash
helm -n kb-system upgrade kubeblocks kubeblocks/kubeblocks --version {VERSION} \
  --set image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set dataProtection.image.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com \
  --set addonChartsImage.registry=apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com
```

**v0.9.x same-minor (faster):** add `--set crd.enabled=false`

**v0.8 → v0.9:** requires `--set admissionWebhooks.enabled=true --set admissionWebhooks.ignoreReplicasCheck=true` and pre-steps (annotate addons, delete incompatible OpsDefinitions). See [upgrade-to-v09-version](https://kubeblocks.io/docs/preview/user_docs/upgrade/upgrade-to-v09-version).

## Step 5: Verify Operator Pods

```bash
kubectl -n kb-system get pods
```

Expected: `kubeblocks` and `kubeblocks-dataprotection` pods in `Running` state. Typical: 1–3 min. If stuck >5 min: `kubectl -n kb-system describe pods` and `kubectl -n kb-system logs deployment/kubeblocks`.

## Step 6: Upgrade Addons (Optional)

Addon upgrade may restart clusters. Since v1.0.0, existing clusters are generally not affected by addon upgrade, but test in non-production first.

**Upgrade all addons with KubeBlocks:**

```bash
helm -n kb-system upgrade kubeblocks kubeblocks/kubeblocks --version {VERSION} --set upgradeAddons=true
```

**Upgrade specific addon:** see [install-addons](https://kubeblocks.io/docs/preview/user_docs/references/install-addons#upgrade-addons). For migrating clusters to a new addon version, see [migrate-clusters-to-new-addon](https://kubeblocks.io/docs/preview/user_docs/upgrade/migrate-clusters-to-new-addon).

## Troubleshooting

**CRD replace fails:** For K8s <= 1.23, try `kubectl create -f ... || kubectl replace -f ...`. Add `--validate=false` if x-kubernetes-validations errors occur.

**Image pull errors:** Switch to China mirror registry (Step 4b). Verify: `helm get values kubeblocks -n kb-system`.

**Pods not Running:** Check `kubectl -n kb-system logs deployment/kubeblocks` and [GitHub Issues](https://github.com/apecloud/kubeblocks/issues).

## Safety Patterns

For dry-run before apply, status confirmation, and production cluster protection, see [safety-patterns.md](../../references/safety-patterns.md).
