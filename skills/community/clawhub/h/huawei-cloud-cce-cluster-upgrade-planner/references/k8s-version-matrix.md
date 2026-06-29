# CCE Kubernetes Version Upgrade Path Matrix

## Official Upgrade Path Table

Source: [CCE集群升级](https://support.huaweicloud.com/usermanual-cce/cce_10_0197.html)

 )

| Current Version | Supported Target Versions |
|---|---|
| v1.13 and below | Not supported |
| v1.15 | v1.19 |
| v1.17 | v1.19 |
| v1.19 | v1.21, v1.23 |
| v1.21 | v1.23 |
| v1.23 | v1.25, v1.27, v1.28 |
| v1.25 | v1.27, v1.28 |
| v1.27 | v1.28 |
| v1.28 | v1.29, v1.31 |
| v1.29 | v1.30, v1.31 |
| v1.30 | v1.31 |
| v1.31 | v1.32, v1.34 |
| v1.32 | v1.33, v1.34 |
| v1.33 | v1.34 |
| v1.34 | v1.35 |

## Upgrade Path Rules

### 1. No Skip-Version Upgrades

CCE does NOT support skipping intermediate versions. Must upgrade step by step through the upgrade path.

**Example**: v1.15 → v1.28 requires four sequential upgrades:
```
v1.15 → v1.19 → v1.23 → v1.27 → v1.28
```

Each intermediate upgrade requires a complete upgrade cycle (pre-check → upgrade → verify).

### 2. Patch Version Must Be Latest Before Major Version Upgrade

Before upgrading to a new major version, the current cluster patch version must be the latest available.

- Patch version upgrade: can jump directly to the latest patch (e.g., v1.23.5-r0 → v1.23.8-r0)
- Major version upgrade: must first upgrade to the latest patch of current version, then upgrade major version

**Example**: v1.23.5-r0 → v1.25
- Step 1: Upgrade patch → v1.23.8-r0 (latest patch)
- Step 2: Upgrade major → v1.25

### 3. Multi-Hop Upgrade Window Planning

For multi-hop upgrades (e.g., v1.21 → v1.28), the total upgrade window is the sum of each hop:

```
T_total = T_hop1 + T_hop2 + T_hop3 + T_hop4 + T_buffer_per_hop
```

Each hop should include its own buffer (20% of that hop's time) for unexpected issues.

## Maintenance Lifecycle

CCE follows Kubernetes community version lifecycle with at least 24 months of maintenance per version.

EOS (End of Service) versions cannot be upgraded directly and need migration strategy.

**Check**: Verify current version is NOT EOS before planning upgrade. See [CCE集群版本生命周期](https://support.huaweicloud.com/bulletin-cce/cce_bulletin_0043.html).

## Version-Specific Constraints

### v1.28+ Control Node IP Change

Upgrading to v1.28 or above creates new control nodes to replace old ones. Control node **IP addresses will change** after upgrade.

**Impact**: If applications connect to cluster via control node IP directly (not through cluster public/private address), they will fail after upgrade.

**Action**: Switch all direct IP connections to cluster unified address (public or private endpoint) BEFORE upgrade.

### v1.27+ Docker Runtime Deprecated

v1.27 and above recommend replacing Docker with Containerd as container runtime. v1.27+ clusters continue to support Docker but plan to remove Docker support in future.

**Action**: For v1.23/v1.25 → v1.27 upgrades, verify if business uses Docker-specific features, plan Containerd migration if needed.

### v1.25 PSP Removed

PodSecurityPolicy (PSP) is removed in v1.25. Must migrate to Pod Security Admission before upgrading to v1.25.

**Migration steps**:
1. Confirm cluster is at latest v1.23 patch version
2. Migrate PSP capabilities to Pod Security Admission (see [PSP配置](https://support.huaweicloud.com/usermanual-cce/cce_10_0466.html))
3. Verify migration works, then upgrade to v1.25

### v1.23→v1.21 Ingress Class Annotation

NGINX Ingress Controller v2.x (community v1.0+) requires explicit Ingress class annotation `kubernetes.io/ingress.class: nginx`. Without it, Ingress is ignored by the controller, causing service disruption.

**Action**: Before upgrading v1.21/v1.19 → v1.23, add the annotation to all Ingress resources, or verify the controller auto-detection is working.

### v1.19→v1.21 Exec Probe Timeout & Webhook SAN

v1.21 fixes the exec probe timeoutSeconds bug — timeout now actually enforced. Pods with exec probe timeouts > 1s may fail after upgrade.

v1.19+ kube-apiserver requires webhook certificates with Subject Alternative Names (SAN) field. Without SAN, webhook authentication fails.

**Action**: Check exec probe timeouts; check webhook certificate SAN configuration.

### v1.15→v1.19 Kubelet Label Compatibility

v1.19 kube-apiserver treats certain kubelet registration labels as illegal:
- `failure-domain.beta.kubernetes.io/is-baremetal` → use `node.kubernetes.io/baremetal`
- `kubernetes.io/availablezone` → use `failure-domain.beta.kubernetes.io/zone`

If node upgrade fails after control plane upgrade, nodes may stay NotReady. Avoid pausing upgrade between control plane and node phases.

**Action**: Do not use PauseUpgradeClusterTask between control plane and node upgrades for v1.15→v1.19.