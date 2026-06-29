# Addon Compatibility & Upgrade Order

## Addon Upgrade Order

**Mandatory sequence**: Cluster version upgrade first → Addon upgrade after cluster reaches target version

**Reason**: Addons must match the cluster K8s version. Upgrading addons before cluster risks incompatibility.

### Addon Categories

| Category | Upgrade Timing | Examples |
|----------|---------------|---------|
| Auto-upgraded during cluster upgrade | Cluster upgrade process handles addon upgrade automatically | Everest (storage CSI), CoreDNS, Metrics-server |
| Must upgrade AFTER cluster reaches target | Separate upgrade action after cluster upgrade completes | NGINX Ingress Controller (version constraints), Volcano |
| Must upgrade BEFORE cluster upgrade | Must be at compatible version before starting cluster upgrade | CCE Node Problem Detector (NPD ≥ 1.18.10 for v1.21+), Cloud Native Log Collector (≥ 1.3.0 for v1.21+) |
| No action needed | Already compatible with both current and target versions | Some addons |

### DaemonSet Plugin Resource Impact

DaemonSet plugins deploy one Pod per node. During upgrade, these Pods are recreated, consuming node resources.

| Plugin | DaemonSet Component | Resource Impact | Upgrade Strategy |
|-------|---------------------|-----------------|------------------|
| ICAgent | icagent | Default installed, mandatory for AOM/LTS | Auto-upgraded during cluster upgrade |
| Everest | everest-csi-driver | Default installed, storage CSI foundation | Auto-upgraded during cluster upgrade |
| Cloud Native Monitoring | node-exporter | Node-level metrics collection | Auto-upgraded |
| Cloud Native Log Collector | fluent-bit, cop-logs | Container/node log collection | Must be ≥ 1.3.0 before v1.21+ upgrade |
| NPD | node-problem-detector | Node health detection | Must be ≥ 1.18.10 before v1.21+ upgrade |
| CCE Key Management (DEW) | dew-provider, csi-secrets-store | Credential management | Auto-upgraded |
| AI Data Acceleration | csi-nodeplugin-fluid | Storage acceleration | Check compatibility before upgrade |
| CCE AI Suite (NVIDIA GPU) | nvidia-gpu-device-plugin | GPU device management | May affect new GPU node driver installation |
| CCE AI Suite (Ascend NPU) | huawei-npu-device-plugin | NPU device management | Check compatibility |
| NodeLocal DNSCache | node-local-dns-cache | DNS caching | Auto-upgraded |
| CCE Container Network Metrics | dolphin | Network metrics collection | Auto-upgraded |

**Resource planning**: During upgrade, DaemonSet Pods are recreated on each node. Ensure node resource headroom for:
- ICAgent: ~200m CPU / 300Mi memory
- Everest: ~100m CPU / 200Mi memory
- node-exporter: ~50m CPU / 50Mi memory
- fluent-bit: ~100m CPU / 100Mi memory

### NGINX Ingress Controller Version Constraints

Specific NGINX Ingress Controller versions have brief service interruption during upgrade:

| Version Range | Impact | Action |
|---------------|-------|--------|
| 2.1.x (patch < 32) | Service interruption during upgrade | Upgrade during low-traffic window |
| 2.2.x (patch < 41) | Service interruption during upgrade | Upgrade during low-traffic window |
| 2.4.x (patch < 4) | Service interruption during upgrade | Upgrade during low-traffic window |
| Other versions | Graceful upgrade (zero downtime) | No special window required |

**Newer versions support graceful upgrade** with ELB delete backend controller grace period.

### Addon Compatibility Check Commands

```bash
# List installed addons
hcloud CCE ListAddonInstances --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json

# Check addon template versions for target K8s version
hcloud CCE ListAddonTemplates --cluster_id=<cluster-id> --addon_template_name=<addon-name> --cli-region=<region> --cli-output=json
```

**Check**: For each addon, verify:
1. Current addon version supports current K8s version ✓
2. Target addon version supports target K8s version ✓
3. If only one supports both → addon will be auto-upgraded during cluster upgrade
4. If neither supports both → must upgrade addon BEFORE cluster upgrade (risk)

### Addon Upgrade Command

```bash
# Upgrade addon after cluster reaches target version
hcloud CCE UpdateAddonInstance \
  --cluster_id=<cluster-id> \
  --addon_id=<addon-id> \
  --body.version=<target-addon-version> \
  --cli-region=<region> \
  --cli-output=json

# Or include addon in cluster upgrade command
hcloud CCE UpgradeCluster \
  --cluster_id=<cluster-id> \
  --metadata.apiVersion=v3 \
  --metadata.kind=UpgradeTask \
  --spec.clusterUpgradeAction.targetVersion=<target-version> \
  --spec.clusterUpgradeAction.addons.1.addonTemplateName=<addon-name> \
  --spec.clusterUpgradeAction.addons.1.operation=patch \
  --spec.clusterUpgradeAction.addons.1.version=<target-addon-version> \
  --cli-region=<region> \
  --cli-output=json
```