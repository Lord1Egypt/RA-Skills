# Pre-Upgrade Checklist (76 Items)

Source: [升级前检查项](https://support.huaweicloud.com/usermanual-cce/cce_10_0549.html)

CCE automatically runs these 76 pre-check items before allowing upgrade. If any item fails, upgrade is blocked until fixed.

## Checklist Categories

### Node Health (Items 1, 21, 22, 25, 41, 44, 51, 52)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 1 | 节点限制检查 | Node availability, OS compatibility, unexpected node pool labels, K8s node name consistency with ECS | Fix node state, remove unexpected labels |
| 21 | 节点Ready检查 | All cluster nodes must be Ready | Drain/fix NotReady nodes before upgrade |
| 22 | 节点journald检查 | journald service must be running normally | Restart journald: `systemctl restart systemd-journald` |
| 25 | 节点挂载点检查 | No inaccessible mount points on nodes | Remove stale mount points |
| 41 | 节点sock文件挂载检查 | Pods mounting docker/containerd.sock directly will break during runtime restart | Remove sock mounts from Pod specs, or accept Pod restart |
| 44 | 节点paas用户登录权限检查 | paas user must have login permission | Restore paas user permissions |
| 51 | 节点命令行检查 | Upgrade-required commands must exist on node | Ensure standard system tools available |
| 52 | 节点交换区检查 | Swap must be disabled on nodes | Disable swap: `swapoff -a` |

### Node Resources (Items 11, 12, 16, 19, 49, 62, 67, 69)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 11 | 节点CPU使用率检查 | Node CPU usage must be < 90% | Reduce workload or add nodes |
| 12 | 节点磁盘检查 | Key data disk usage meets requirements; /tmp has ≥500MB free | Clean disk space, remove unused images |
| 16 | 节点内存检查 | Node memory usage must be < 90% | Reduce workload or add nodes |
| 19 | 节点CPU数量检查 | Control node CPU cores must be > 2 | Upgrade control node flavor |
| 49 | 节点Sudo检查 | sudo command and related files must be normal | Fix sudo configuration |
| 62 | 集群镜像数量检查 | Node image count should not exceed 1000 (Docker slow start risk) | Clean unused images: `docker image prune` |
| 67 | 节点镜像层数量检查 | Image layers should not exceed 5000 | Clean unused images |
| 69 | 轮转证书文件数量检查 | Certificate files on node should not exceed 1000 (slow upgrade risk) | Remove unnecessary certificates |

### Node Configuration (Items 15, 17, 34, 35, 36, 37, 39, 40, 50)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 15 | 节点Kubelet检查 | kubelet service must be running normally | Restart kubelet if needed |
| 17 | 节点时钟同步检查 | ntpd or chronyd must be running normally | Install/configure chronyd |
| 34 | 节点NetworkManager检查 | NetworkManager must be running normally | Restart NetworkManager |
| 35 | 节点ID文件检查 | Node ID file content must match expected format | Fix ID file |
| 36 | 节点配置一致性检查 (v1.19+) | K8s component config files should not be manually modified (v1.19+ upgrade) | Use CCE config management instead of direct file edits |
| 37 | 节点配置文件检查 | Key component config files must exist | Restore missing config files |
| 39 | 节点关键目录文件权限检查 | Root directory permissions must be correct | Fix permissions: `chmod 755 /` |
| 40 | 节点关键命令检查 | Upgrade-required commands must execute normally | Ensure standard system commands work |
| 50 | 节点系统参数检查 | Node sysctl parameters must match expected values | Reset sysctl to CCE defaults |

### Node Network & DNS (Items 13, 14)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 13 | 节点DNS检查 | Node DNS must resolve OBS addresses | Fix DNS configuration |
| 14 | 节点OBS访问检查 | Node must access OBS (upgrade package storage) | Fix network/firewall rules |

### Upgrade Control (Items 2, 46, 68)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 2 | 升级管控检查 | Cluster must not be under upgrade control | Wait for current control period to end |
| 46 | 历史升级记录检查 | Original cluster version must meet upgrade path conditions | Follow correct upgrade path sequence |
| 68 | 集群滚动升级条件检查 | Cluster must satisfy rolling upgrade conditions | Fix blocking conditions |

### Addon & Plugin (Items 3, 27, 28, 47, 48, 53, 54, 63)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 3 | 插件检查 | Addon status must be normal; addon must support target K8s version | Fix addon status; upgrade incompatible addons |
| 27 | everest插件版本限制检查 | Everest plugin version compatibility | Upgrade Everest to compatible version |
| 28 | cce-hpa-controller插件限制检查 | HPA controller target version compatibility | Upgrade HPA controller |
| 47 | CCE AI套件(NVIDIA GPU)插件检查 | GPU plugin may affect new GPU node driver installation | Verify GPU plugin compatibility |
| 48 | 增强型CPU管理策略检查 | Source and target version must support enhanced CPU management | Disable if target version doesn't support |
| 53 | NGINX Ingress控制器插件升级检查 | Ingress controller upgrade path compatibility | Upgrade Ingress controller version |
| 54 | 云原生监控插件升级检查 | Prometheus plugin 3.9.0 migration: grafana switch must be enabled | Enable grafana switch before upgrade |
| 63 | OpenKruise插件兼容性检查 | OpenKruise plugin compatibility with target K8s | Upgrade OpenKruise to compatible version |

### K8s Resources & API (Items 4, 8, 9, 33, 75)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 4 | Helm模板检查 | HelmRelease must not contain target-version deprecated APIs | Update Helm templates to use non-deprecated APIs |
| 8 | K8s废弃资源检查 | Cluster must not have resources from deprecated API versions | Migrate resources to new API versions |
| 9 | 兼容性风险检查 | Version compatibility differences (not applicable for patch upgrades) | Review version-specific changes in this document |
| 33 | K8s废弃API检查 | Audit logs (past 24h) must not show calls to deprecated APIs | Migrate API calls to non-deprecated versions |
| 75 | 插件配置一致性校验 | Addon ConfigMap must match Helm Release records (manual edits will be overwritten) | Use CCE addon management API instead of direct ConfigMap edits |

### Node Pool & Scheduling (Items 5, 26, 72)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 5 | 节点池检查 | Node pool status must be normal | Fix node pool issues |
| 26 | K8s节点污点检查 | Nodes must not have taints needed by upgrade process | Remove conflicting taints |
| 72 | 集群与节点池配置管理检查 | ENI network component nic-max-above-warm-target must not exceed maximum | Adjust ENI warm target configuration |

### Security & Network (Items 6, 42, 58, 70, 71, 74, 76)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 6 | 安全组检查 | ICMP rule from control node security group must not be deleted | Restore ICMP security group rule |
| 42 | HTTPS ELB证书一致性检查 | HTTPS ELB certificate must not be modified outside CCE | Manage certificates through CCE only |
| 58 | ELB监听器访问控制检查 | ELB listener access control configuration must be correct | Fix ELB access control configuration |
| 70 | Ingress与ELB配置一致性检查 | Ingress config must match ELB config (no manual ELB edits) | Manage ELB through CCE Ingress only |
| 71 | 集群网络组件NetworkPolicy开关检查 | NetworkPolicy switch must match default (manual changes will be reset) | Use CCE network management API |
| 74 | VPC容器预留网段升级检查 | VPC container CIDR reservation switch should be enabled | Enable VPC container CIDR reservation |
| 76 | Secret落盘加密特性兼容性检查 | Target version must support Secret encryption-at-rest if enabled | Disable Secret encryption if target version doesn't support |

### Control Plane (Items 31, 32, 59, 73)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 31 | 用户节点组件健康检查 | Container runtime and network components must be healthy | Fix component issues |
| 32 | 控制节点组件健康检查 | K8s, runtime, network components on control nodes must be healthy | Fix control plane component issues |
| 59 | 控制节点子网配额检查 | Subnet must have enough remaining IPs for rolling upgrade | Request subnet IP quota increase |
| 73 | 控制节点时区检查 | Control node timezone must match cluster timezone | Align timezone settings |

### Special Checks (Items 7, 10, 23, 24, 29, 30, 38, 43, 45, 55, 56, 57, 60, 61, 64, 65, 66)

| # | Check Item | Description | Fix |
|---|------------|-------------|-----|
| 7 | 残留待迁移节点检查 | Nodes requiring migration must be handled first | Complete node migration before upgrade |
| 10 | 节点CCE Agent版本检查 | cce-agent must be latest version | Upgrade cce-agent |
| 23 | 节点干扰ContainerdSock检查 | Interfering containerd.sock file exists (affects EulerOS runtime startup) | Remove interfering sock file |
| 24 | 内部错误检查 | Internal error in pre-check process | Contact support |
| 29 | 增强型CPU管理策略检查 | Current and target version must support enhanced CPU management | Adjust CPU management policy |
| 30 | 用户节点组件健康检查 | User node runtime and network components healthy | Fix unhealthy components |
| 38 | CoreDNS配置一致性检查 | CoreDNS Corefile must match Helm Release (manual edits overwritten during addon upgrade) | Manage CoreDNS through CCE addon API |
| 43 | 节点挂载检查 | Node mount configuration issues | Fix mount issues |
| 45 | ELB IPv4私网地址检查 | LoadBalancer Service ELB must have IPv4 private IP | Fix ELB IP configuration |
| 55 | Containerd Pod重启风险检查 | Containerd upgrade may restart business Pods on containerd nodes | Accept Pod restart risk or plan for it |
| 56 | CCE AI套件(NVIDIA GPU)关键参数检查 | GPU plugin parameters must not be invasively modified | Restore GPU plugin default parameters |
| 57 | GPU/NPU Pod重建风险检查 | kubelet restart during upgrade may rebuild GPU/NPU Pods | Plan for GPU/NPU Pod rebuild |
| 60 | 节点运行时检查 | Docker runtime warning for v1.27+ upgrade (CCE plans to remove Docker support) | Plan Containerd migration |
| 61 | 节点池运行时检查 | Node pool Docker runtime warning for v1.27+ | Migrate to Containerd |
| 64 | Secret落盘加密特性兼容性检查 | Secret encryption-at-rest compatibility with target version | Disable if target doesn't support |
| 65 | Ubuntu内核与GPU驱动兼容性提醒 | Ubuntu kernel 5.15.0-113-generic requires NVIDIA driver ≥535.161.08 | Upgrade GPU driver or change kernel |
| 66 | 排水任务检查 | Unfinished drain tasks will trigger Pod eviction after upgrade | Complete all pending drain tasks |

## Version-Specific Breaking Changes

### All Upgrade Paths

- Check for **deprecated APIs** across all versions (see Deprecated API tables in official docs)
- Verify Helm templates don't use deprecated API versions

### v1.28 → v1.29/v1.31

- **nf_conntrack_max override**: kube-proxy may set nf_conntrack_max lower than node sysctl. High-traffic nodes (gateways) may be affected.
- **Fix**: Use node pool kube-proxy config `conntrack-min` instead of direct sysctl modification.

### v1.23/v1.25 → v1.27

- **Docker runtime deprecated**: Recommend Containerd migration for v1.27+ clusters.
- **CCE warning**: Docker runtime will be removed in future versions.

### v1.23 → v1.25

- **PodSecurityPolicy removed**: Must migrate PSP → Pod Security Admission before v1.25 upgrade.
- **Migration**: (1) Confirm v1.23 latest patch; (2) Migrate PSP to PSA; (3) Verify migration works; (4) Upgrade to v1.25.

### v1.21/v1.19 → v1.23

- **NGINX Ingress class annotation**: Ingress without `kubernetes.io/ingress.class: nginx` annotation ignored by v2.x controller.
- **Fix**: Add class annotation to all Ingress resources, or verify auto-detection.

### v1.19 → v1.21

- **exec probe timeoutSeconds enforced**: Previously ignored, now enforced. Default 1s. Pods with >1s exec probe may fail.
- **Webhook SAN required**: v1.19+ apiserver requires SAN in webhook certificates. CommonName-only certificates fail.

### v1.15 → v1.19

- **Kubelet label incompatibility**: v1.19 apiserver rejects v1.15 kubelet labels (`failure-domain.beta.kubernetes.io/is-baremetal`, `kubernetes.io/availablezone`). Nodes may become NotReady.
- **Docker fs change**: v1.19 switches Docker storage driver fs from xfs to ext4. Java apps may have import order changes.
- **Webhook SAN**: Same as v1.21 — webhook certificates need SAN.
- **PSP auto-creation**: v1.17.17+ auto-creates PSP restricting insecure configs (sysctl net.core.somaxconn). Need to reference PSP for access.
- **QosClass change**: v1.16+ kubelet counts initContainers in QosClass calculation. Pods may change QosClass after upgrade.