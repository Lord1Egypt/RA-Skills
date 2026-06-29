# Upgrade Workflow

## 7-Step Assessment Process

### Step 1: Collect Cluster Current State

Query cluster details to establish baseline:

```bash
# Get cluster version, node count, addon list, node pool info
hcloud CCE ShowCluster --cluster_id=<cluster-id> --detail=true --cli-region=<region> --cli-output=json

hcloud CCE ListAddonInstances --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ListNodePools --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
hcloud CCE ListNodes --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
```

**Extract from ShowCluster response**:
- `spec.version` — current K8s version (e.g., v1.23.5-r0)
- `status.phase` — cluster status (must be Available)
- `metadata.annotations.totalNodesNumber` — total node count
- `metadata.annotations.activeNodesNumber` — active node count
- `metadata.annotations.installedAddonInstances` — addon list with name, version, status

### Step 2: Determine Upgrade Path

```bash
# Get all upgrade paths
hcloud CCE ListClusterUpgradePaths --cli-region=<region> --cli-output=json
```

**Upgrade path rules** (see [k8s-version-matrix.md](k8s-version-matrix.md)):
1. Find current version in the upgrade path table
2. Check if target version is in the "支持升级到的Kubernetes版本号" column
3. If not listed, must upgrade through intermediate versions step by step
4. Patch version must be upgraded to latest before major version upgrade

**Example**: v1.21.7-r0 → v1.28
- v1.21 → v1.23 (intermediate)
- v1.23 → v1.25 (intermediate)
- v1.25 → v1.27 (intermediate)
- v1.27 → v1.28 (target)
- Each step requires a full upgrade cycle (pre-check → upgrade → verify)

### Step 3: Pre-Upgrade Check

```bash
# Create upgrade workflow (triggers pre-check automatically)
hcloud CCE CreateUpgradeWorkFlow \
  --cluster_id=<cluster-id> \
  --apiVersion=v3 \
  --kind=WorkFlowTask \
  --spec.targetVersion=<target-version> \
  --spec.clusterVersion=<current-version> \
  --cli-region=<region> \
  --cli-output=json

# Or check upgrade info directly
hcloud CCE ShowClusterUpgradeInfo --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json
```

**Pre-check covers 76 items** (see [pre-upgrade-checklist.md](pre-upgrade-checklist.md)):
- Node status, OS, kubelet, disk, CPU, memory, DNS, clock sync
- Addon status and version compatibility
- Helm template deprecated API scan
- K8s deprecated resource scan (audit logs)
- Security group ICMP rules
- Node pool state, node pool configuration consistency
- CoreDNS configuration consistency
- Container runtime (Docker vs Containerd) check
- Network component health (NetworkManager, ENI)
- GPU/NPU plugin compatibility
- And more...

**If pre-check fails**: fix the reported issues before proceeding with upgrade.

### Step 4: Addon Compatibility Assessment

For each installed addon:
1. Check if addon supports both current and target K8s versions
2. If addon only supports one version, it will be upgraded during cluster upgrade (auto) or needs separate upgrade action
3. Verify addon upgrade won not break business functionality

```bash
# List addon template versions for target K8s
hcloud CCE ListAddonTemplates --cluster_id=<cluster-id> --addon_template_name=<addon-name> --cli-region=<region> --cli-output=json
```

**Addon upgrade order** (see [addon-compatibility.md](addon-compatibility.md)):
- Everest (storage CSI) — must upgrade before or during cluster upgrade
- CoreDNS — upgrade after cluster reaches target version
- Metrics-server — upgrade after cluster
- NGINX Ingress Controller — upgrade after cluster (check version constraints)
- DaemonSet plugins (ICAgent, node-exporter, fluent-bit, NPD) — upgrade during cluster upgrade (auto)

### Step 5: Upgrade Window Estimation

Calculate upgrade window based on:
- Node count and batch strategy
- Addon count and upgrade time per addon
- Verification time
- Buffer for unexpected issues

See [upgrade-window-estimation.md](upgrade-window-estimation.md) for formula and examples.

### Step 6: Generate Upgrade Plan (Execution Preview)

Generate specific hcloud CLI commands for each phase:

**Phase 1 — Control Plane Upgrade**:
```bash
hcloud CCE UpgradeCluster \
  --cluster_id=<cluster-id> \
  --metadata.apiVersion=v3 \
  --metadata.kind=UpgradeTask \
  --spec.clusterUpgradeAction.targetVersion=<target-version> \
  --spec.clusterUpgradeAction.strategy.type=inPlaceRollingUpdate \
  --spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.userDefinedStep=20 \
  --spec.clusterUpgradeAction.strategy.inPlaceRollingUpdate.scope=Cluster \
  --spec.clusterUpgradeAction.addons.1.addonTemplateName=coredns \
  --spec.clusterUpgradeAction.addons.1.operation=patch \
  --spec.clusterUpgradeAction.addons.1.version=<target-addon-version> \
  --cli-region=<region> \
  --cli-output=json
```

**Phase 2 — Node Pool Upgrade**:
```bash
hcloud CCE UpgradeNodePool \
  --cluster_id=<cluster-id> \
  --nodepool_id=<nodepool-id> \
  --cli-region=<region> \
  --cli-output=json
```

**Phase 3 — Addon Upgrade** (for addons that need separate upgrade):
```bash
hcloud CCE UpdateAddonInstance \
  --cluster_id=<cluster-id> \
  --addon_id=<addon-id> \
  --body.version=<target-addon-version> \
  --cli-region=<region> \
  --cli-output=json
```

> **⚠️ Execution Preview**: These commands are for review only. Do NOT execute without user confirming with explicit approval.

### Step 7: Rollback Strategy & Post-Upgrade Verification

**Rollback options**:
- Use backup data (etcd auto-backup during upgrade, CBR/EVS manual backup before upgrade)
- PauseUpgradeClusterTask to pause upgrade and investigate issues
- Cancel upgrade workflow (UpgradeWorkFlowUpdate with phase=Cancel)
- For v1.28+: control node IPs change, plan connectivity update

**Post-upgrade verification**:
```bash
# Check cluster status
hcloud CCE ShowCluster --cluster_id=<cluster-id> --detail=true --cli-region=<region> --cli-output=json

# Check node status (all should be Ready)
hcloud CCE ListNodes --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json

# Check addon status
hcloud CCE ListAddonInstances --cluster_id=<cluster-id> --cli-region=<region> --cli-output=json

# Check upgrade workflow completion
hcloud CCE ShowUpgradeWorkFlow --cluster_id=<cluster-id> --upgrade_workflow_id=<workflow-id> --cli-region=<region> --cli-output=json
```

**Post-upgrade verification items**:
1. Cluster status.phase = Available
2. All nodes Ready, no NotReady nodes
3. All addons status = running
4. Business workload health (Pod status, Service connectivity)
5. New node scheduling works (create test Pod on new node)
6. CoreDNS resolution works (nslookup test)
7. Ingress/ELB routing works (curl test on external endpoint)