# KubeBlocks Installation Reference

Detailed options, configurations, and procedures for KubeBlocks installation.

Source: https://kubeblocks.io/docs/preview/user_docs/references/kubeblocks_options

## Helm Chart Options

To view all available options for a specific version:

```bash
helm show values kubeblocks/kubeblocks --version {VERSION}
```

### KubeBlocks Core Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `image.registry` | KubeBlocks image registry | `apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com` |
| `image.repository` | KubeBlocks image repository | `apecloud/kubeblocks` |
| `image.pullPolicy` | Image pull policy | `IfNotPresent` |
| `image.tag` | Image tag (defaults to chart appVersion) | `""` |
| `image.imagePullSecrets` | Image pull secrets | `[]` |
| `replicaCount` | Replica count | `1` |

### Data Protection Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `dataProtection.enabled` | Enable data protection controllers | `true` |
| `dataProtection.image.registry` | Data protection image registry | `""` (uses `image.registry`) |
| `dataProtection.image.repository` | Data protection image repository | `apecloud/kubeblocks-dataprotection` |
| `dataProtection.enableBackupEncryption` | Enable backup encryption | `false` |
| `dataProtection.gcFrequencySeconds` | Garbage collection frequency | `3600` |

### Addon Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `addonController.enabled` | Enable Addon controller (requires `cluster-admin` ClusterRole) | `true` |
| `addonChartsImage.registry` | Addon charts image registry | `""` (uses `image.registry`) |
| `addonChartsImage.repository` | Addon charts image repository | `apecloud/kubeblocks-charts` |
| `autoInstalledAddons` | Addons to auto-install | `["apecloud-mysql","etcd","kafka","mongodb","mysql","postgresql","qdrant","redis","rabbitmq"]` |
| `keepAddons` | Keep Addon CRs when uninstalling | `true` |

### Feature Gates

| Parameter | Description | Default |
|-----------|-------------|---------|
| `featureGates.inPlacePodVerticalScaling.enabled` | Enable in-place Pod vertical scaling | `false` |

### Controller Options

| Parameter | Description | Default |
|-----------|-------------|---------|
| `controllers.apps.enabled` | Enable apps controller | `true` |
| `controllers.workloads.enabled` | Enable workloads controller | `true` |
| `controllers.operations.enabled` | Enable operations controller | `true` |
| `controllers.experimental.enabled` | Enable experimental controller | `false` |

## Image Registry Reference

### Global (default for non-China environments)

```
registry: docker.io
namespace: apecloud
```

Example full image: `docker.io/apecloud/kubeblocks:{VERSION}`

### China Mainland Mirror

```
registry: apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com
namespace: apecloud
```

Example full image: `apecloud-registry.cn-zhangjiakou.cr.aliyuncs.com/apecloud/kubeblocks:{VERSION}`

### Alternative Helm Repository for China

If GitHub Pages is slow, use the JiHuLab mirror for addon charts:

```bash
helm repo add kubeblocks-addons https://jihulab.com/api/v4/projects/150246/packages/helm/stable
```

## Managing Addons

After KubeBlocks is installed, some addons are auto-installed by default. To manage addons:

### List Installed Addons

```bash
helm list -n kb-system | grep kb-addon
```

### Install an Additional Addon

```bash
# View available versions
helm search repo kubeblocks/{addon-name} --versions

# Install
helm install kb-addon-{addon-name} kubeblocks/{addon-name} \
  --namespace kb-system --create-namespace \
  --version {ADDON_VERSION}
```

Addon version must match KubeBlocks major version (e.g., KubeBlocks v1.0.x with Addon v1.0.x).

### Uninstall an Addon

```bash
helm uninstall kb-addon-{addon-name} --namespace kb-system
```

## Detailed Uninstall Procedure

### Step 1: Delete All Clusters and Backups

```bash
kubectl get cluster -A
kubectl get backup -A

kubectl delete cluster <name> -n <namespace>
kubectl delete backup <name> -n <namespace>
```

### Step 2: Uninstall All Addons

```bash
helm list -n kb-system | grep kb-addon | awk '{print $1}' | xargs -I {} helm -n kb-system uninstall {}
```

### Step 3: Clean Up Remaining Resources

Some resources are kept due to Helm resource policy. Remove them:

```bash
kubectl delete componentdefinitions.apps.kubeblocks.io --all
kubectl delete parametersdefinitions.parameters.kubeblocks.io --all
kubectl get configmap -n kb-system | grep configuration | awk '{print $1}' | xargs -I {} kubectl delete -n kb-system cm {}
kubectl get configmap -n kb-system | grep template | awk '{print $1}' | xargs -I {} kubectl delete -n kb-system cm {}
kubectl delete addon.extensions.kubeblocks.io --all
```

### Step 4: Uninstall KubeBlocks

```bash
helm uninstall kubeblocks --namespace kb-system
```

### Step 5: Remove CRDs

```bash
kubectl get crd -o name | grep kubeblocks.io | xargs kubectl delete
```

### Step 6: Verify Clean Removal

```bash
kubectl get crd | grep kubeblocks.io | awk '{print $1}' | while read crd; do
  echo "Processing CRD: $crd"
  kubectl get "$crd" -o json | jq '.items[] | select(.metadata.finalizers != null) | .metadata.name' -r | while read resource; do
    echo "Custom Resource left: $resource in CRD: $crd"
  done
done
```

The output should be empty if everything is cleaned up.

## Upgrading KubeBlocks

```bash
# Update Helm repo
helm repo update

# Upgrade KubeBlocks
helm upgrade kubeblocks kubeblocks/kubeblocks \
  --namespace kb-system \
  --version {NEW_VERSION}
```

For major version upgrades (e.g., v0.9.x to v1.0.x), refer to:
https://kubeblocks.io/docs/preview/user_docs/upgrade/upgrade-to-v10x

## Creating a Local Test Cluster

If the user has no Kubernetes cluster, use the [create-local-k8s-cluster](../../kubeblocks-create-local-k8s-cluster/SKILL.md) skill to create one with Kind, Minikube, or k3d.

## Version Compatibility Matrix

| KubeBlocks | Addon Version | kbcli Version | Min K8s |
|------------|---------------|---------------|---------|
| v1.0.x     | v1.0.x        | v1.0.x        | v1.21   |
| v0.9.x     | v0.9.x        | v0.9.x        | v1.21   |
| v0.8.x     | v0.8.x        | v0.8.x        | v1.21   |

Mismatched major versions between KubeBlocks, addons, and kbcli may cause unexpected errors.

## Documentation Links

- Installation: https://kubeblocks.io/docs/preview/user_docs/overview/install-kubeblocks
- Options Reference: https://kubeblocks.io/docs/preview/user_docs/references/kubeblocks_options
- Addons Management: https://kubeblocks.io/docs/preview/user_docs/references/install-addons
- Install kbcli: https://kubeblocks.io/docs/preview/user_docs/references/install-kbcli
- Local K8s Cluster: https://kubeblocks.io/docs/preview/user_docs/references/prepare-a-local-k8s-cluster
- Supported Addons: https://kubeblocks.io/docs/preview/user_docs/overview/supported-addons
- Full Doc Index: https://kubeblocks.io/llms-full.txt
- KubeBlocks GitHub: https://github.com/apecloud/kubeblocks
- KubeBlocks Releases: https://github.com/apecloud/kubeblocks/releases
