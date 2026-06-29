---
id: huawei-cloud-cce-availability-risk-scanner
name: huawei-cloud-cce-availability-risk-scanner
description: |
  Huawei Cloud CCE availability risk scanning skill using Python SDK dispatcher for read-only cluster risk assessment.
  Use this skill when the user wants to: (1) scan CCE clusters for availability risks including single replicas, missing PodDisruptionBudgets, unhealthy probes, unreasonable affinity or nodepool pinning, (2) assess master HA and utilization, node and workload AZ balance, gateway workload distribution, and core addon anti-affinity, (3) detect resource request/limit overcommit and capacity illusions, (4) produce risk-rated reports with remediation plans and YAML suggestions, (5) check control-plane visibility, node AZ distribution, nodepool distribution, and Pod spread.
  Trigger: user mentions "availability risk", "可用性风险", "availability scanner", "可用性扫描", "cluster inspection", "集群巡检", "risk assessment", "风险评估", "single point of failure", "单点故障", "availability gap", "可用性缺口", "PDB missing", "单副本", "AZ imbalance", "AZ 不均衡", "gateway concentration", "网关集中", "resource overcommit", "资源超配", "health probe missing", "探针缺失"
tags: [cce, availability, risk-scanner, inspection]
---

# Huawei Cloud CCE Availability Risk Scanner

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill scans Huawei Cloud CCE clusters for availability risks. It performs read-only checks, produces risk-rated reports, and generates remediation plans with YAML suggestions. It does NOT directly modify workloads, PDBs, affinity rules, probes, node pools, or cluster configuration.

**Architecture**: Python dispatcher (`scripts/huawei-cloud.py`) → Huawei Cloud Python SDK + Kubernetes client → Nodes, Pods, Deployments, StatefulSets, DaemonSets, PDBs, Services, Ingresses, Events, Metrics → Risk classification → Remediation plan → Reports

**Related Skills**:

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod-level failure diagnosis (CrashLoopBackOff, OOMKilled, Pending) |
| `huawei-cloud-cce-node-failure-diagnoser` | Node-level failure diagnosis (NotReady, pressure) |
| `huawei-cloud-cce-network-failure-diagnoser` | Network failure diagnosis (Service, DNS, Ingress, ELB) |
| `huawei-cloud-cce-root-cause-analyzer` | Cross-resource root cause correlation |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (scale, PDB, affinity, probes) |
| `huawei-cloud-cce-cce-workload-manager` | Workload lifecycle management (Deployment/StatefulSet operations) |

**Capabilities**:

1. One-shot availability risk scan with automated inventory collection and risk classification (`huawei_scan_cce_availability_risk`)
2. Control-plane visibility and master HA assessment (node count, AZ distribution, CPU/memory metrics)
3. Node AZ distribution and nodepool distribution analysis
4. Workload risk detection: single replicas, missing PDBs, Pod AZ/node concentration, missing health probes, hard affinity, anti-affinity gaps, topology spread gaps
5. Gateway workload identification and distribution assessment (nginx, gateway, ingress, proxy, kong, apisix, traefik)
6. Core addon anti-affinity and distribution checks (CoreDNS, nginx-ingress, ingress-nginx)
7. Resource request/limit overcommit detection and cluster capacity illusion identification
8. Risk-rated reports with severity classification, remediation suggestions, and authorized execution plans

**Typical Use Cases**:

- "Scan my CCE cluster for availability risks"
- "Check if my cluster has single points of failure"
- "Assess master HA and node AZ distribution"
- "Find workloads missing PodDisruptionBudgets"
- "Identify gateway workloads concentrated on a single node or AZ"
- "Detect resource overcommit and capacity illusions"
- "Check health probe coverage for my Deployments"
- "Assess workload affinity and topology spread"
- "Review core addon (CoreDNS, nginx-ingress) anti-affinity"
- "Generate an availability risk report with remediation plan"

## Prerequisites

### 1. Python Requirements (MANDATORY)

- Python >= 3.6 installed
- Required packages: `huaweicloudsdkcore`, `huaweicloudsdkcce`, `huaweicloudsdkaom`, `huaweicloudsdkhss`, `huaweicloudsdkvpc`, `huaweicloudsdkecs`, `huaweicloudsdkces`, `huaweicloudsdkevs`, `huaweicloudsdkeip`, `huaweicloudsdkelb`, `huaweicloudsdkiam`, `kubernetes`
- Verify: `python3 --version`
- Install packages: `pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom huaweicloudsdkhss huaweicloudsdkvpc huaweicloudsdkecs huaweicloudsdkces huaweicloudsdkevs huaweicloudsdkeip huaweicloudsdkelb huaweicloudsdkiam kubernetes`

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - 🚫 Never write credentials to files, logs, or responses
  - ✅ Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - ✅ Credentials exist only in the current request call stack and are released after each invocation
  - ✅ Prefer IAM users over root account for cloud operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**Additional Variables**:

| Variable | Required | Description |
|----------|----------|-------------|
| `HUAWEI_AK` | Yes | Huawei Cloud Access Key |
| `HUAWEI_SK` | Yes | Huawei Cloud Secret Key |
| `HUAWEI_REGION` | No | Default region (overrides `region` param if set) |
| `HUAWEI_PROJECT_ID` | No | Project ID (auto-obtained via IAM API when not set) |
| `HUAWEI_SECURITY_TOKEN` | No | Required when using temporary AK/SK |

### 3. IAM Permission Requirements

| API Action | Service | Purpose |
|------------|---------|---------|
| CCE cluster read | CCE | `huawei_list_cce_clusters` |
| CCE node read | CCE | `huawei_get_kubernetes_nodes`, `huawei_get_cce_nodes` |
| CCE workload read | CCE | `huawei_get_cce_pods`, `huawei_get_cce_deployments` |
| CCE nodepool read | CCE | `huawei_list_cce_nodepools` |
| CCE addon read | CCE | `huawei_list_cce_addons` |
| AOM metrics read | AOM | `huawei_get_cce_node_metrics`, `huawei_get_cce_node_metrics_topN`, `huawei_get_aom_metrics` |
| Kubernetes API read | CCE (kubeconfig) | `huawei_get_cce_pods`, `huawei_get_cce_deployments`, `huawei_list_cce_statefulsets`, `huawei_list_cce_daemonsets` |

**Permission Failure Handling**:

1. When any action fails due to permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation that permissions have been granted
4. Retry the failed action

## Core Commands

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### 1. Primary Scan Action (One-Call)

The primary scan command that collects all availability risk data in a single call and outputs a risk-rated report.

```bash
python3 scripts/huawei-cloud.py huawei_scan_cce_availability_risk \
  region=cn-north-4 cluster_id=<cluster_id> \
  exclude_namespaces=kube-system \
  gateway_keywords=nginx,gateway,ingress,proxy,kong,apisix,traefik \
  metrics_hours=24 \
  output_dir=./output
```

Returns: risk-rated issues, severity classification, inventory summary, data gaps, remediation suggestions, and optionally `availability-risk-summary.json` and `availability-risk-report.md` files.

### 2. Inventory Collection Actions

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_get_kubernetes_nodes` | `region`, `cluster_id` | Query v1.Node Ready/conditions/AZ distribution |
| `huawei_get_cce_pods` | `region`, `cluster_id` | List Pod phase/reason/state/node/AZ |
| `huawei_get_cce_deployments` | `region`, `cluster_id` | List Deployments with replicas/PDB/affinity |
| `huawei_get_cce_services` | `region`, `cluster_id` | List Services for workload correlation |
| `huawei_get_cce_ingresses` | `region`, `cluster_id` | List Ingresses for gateway identification |
| `huawei_list_cce_nodepools` | `region`, `cluster_id` | List node pools with AZ distribution |
| `huawei_list_cce_daemonsets` | `region`, `cluster_id` | List DaemonSets for probe/affinity check |
| `huawei_list_cce_statefulsets` | `region`, `cluster_id` | List StatefulSets for PDB/single-replica check |
| `huawei_get_cce_node_metrics_topN` | `region`, `cluster_id` | Top-N node CPU/memory metrics |
| `huawei_get_aom_metrics` | `region` | AOM metric data for master/node trends |
| `huawei_list_cce_clusters` | `region` | List CCE clusters (for cluster selection) |

### 3. Supplementary Query Actions

For targeted evidence when the user requests specific information:

```bash
# Node AZ distribution detail
python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes \
  region=cn-north-4 cluster_id=<cluster_id>

# Pod distribution across AZs
python3 scripts/huawei-cloud.py huawei_get_cce_pods \
  region=cn-north-4 cluster_id=<cluster_id> namespace=default

# Deployment detail with PDB and affinity
python3 scripts/huawei-cloud.py huawei_get_cce_deployments \
  region=cn-north-4 cluster_id=<cluster_id> namespace=default

# Node pool AZ distribution
python3 scripts/huawei-cloud.py huawei_list_cce_nodepools \
  region=cn-north-4 cluster_id=<cluster_id>

# Node metrics trend
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics_topN \
  region=cn-north-4 cluster_id=<cluster_id> top_n=10
```

## Parameter Reference

### `huawei_scan_cce_availability_risk` (Primary Action)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | - | CCE cluster ID |
| `exclude_namespaces` | No | `kube-system` | Namespaces excluded from business risk scanning; core addons still checked |
| `gateway_keywords` | No | `nginx,gateway,ingress,proxy,kong,apisix,traefik` | Keywords for identifying gateway-class workloads |
| `metrics_hours` | No | 24 | Lookback window for master/node CPU/memory trend metrics |
| `output_dir` | No | - | Directory for `availability-risk-summary.json` and `availability-risk-report.md` output |

### Common Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region | - |
| `cluster_id` | Yes (most actions) | CCE cluster ID | - |
| `namespace` | Context-dependent | Kubernetes namespace | - |
| `top_n` | No | Number of top results | 10 |
| `metrics_hours` | No | Metric lookback hours | 24 |

### Common Region IDs

| Region Name | Region ID |
|-------------|-----------|
| North China - Beijing 4 | `cn-north-4` |
| North China - Beijing 1 | `cn-north-1` |
| East China - Shanghai 1 | `cn-east-3` |
| East China - Shanghai 2 | `cn-east-2` |
| South China - Guangzhou | `cn-south-1` |
| South China - Shenzhen | `cn-south-4` |
| Southwest China - Guiyang 1 | `cn-southwest-2` |
| Asia Pacific - Bangkok | `ap-southeast-2` |
| Asia Pacific - Singapore | `ap-southeast-1` |
| Asia Pacific - Hong Kong | `ap-southeast-3` |
| Europe - Paris | `eu-west-0` |

## Output Format

The primary action `huawei_scan_cce_availability_risk` returns structured risk data. See [Output Schema](references/output-schema.md) for the full JSON response schema.

**Key Output Fields**:

| Field | Description |
|-------|-------------|
| `success` | Whether the scan completed successfully |
| `scope` | Scan scope (region, cluster_id, excluded namespaces, gateway keywords) |
| `inventory` | Collected resource counts (nodes, workloads, pods, PDBs, services, ingresses) and AZ distribution |
| `cluster.control_plane` | Master HA status, visible node count, zone distribution, metrics |
| `cluster.resources` | CPU/memory request/limit allocatable ratios, missing request containers count |
| `issues[]` | Risk issues with severity, category, resource, message, recommendation |
| `summary.risk_level` | Overall risk level: critical, high, medium, low |
| `summary.issue_count` | Total issues with severity breakdown |
| `recommendations` | Remediation recommendations list |
| `remediation_plan` | Authorized execution plan items |
| `data_gaps` | Data gaps when control-plane or metrics are unavailable |
| `files` | Optional output file paths (summary JSON, report Markdown, raw inventory) |

**Issue Severity Levels**:

| Severity | Criteria |
|----------|----------|
| `critical` | Single replica gateway, no master HA, single-AZ concentration of all Ready nodes |
| `high` | Multi-replica workload missing PDB, Pod concentration on single node/AZ, missing health probes |
| `medium` | Missing resource requests, memory overcommit ratio > 2x, core addon single replica |
| `low` | CPU overcommit ratio > 4x (may be intentional burst), minor affinity gaps |

**Issue Categories**:

| Category | Description |
|----------|-------------|
| `single-replica` | Workload or gateway running with < 2 replicas |
| `pdb` | Multi-replica workload missing PodDisruptionBudget |
| `health-check` | Workload missing readinessProbe or livenessProbe |
| `affinity` | Hard affinity pinning to single AZ/node/nodepool, missing anti-affinity |
| `az-distribution` | Nodes or Pods concentrated in a single AZ |
| `gateway` | Gateway workload risk (concentration, missing PDB, missing probes) |
| `resources` | Missing requests, overcommit, or capacity illusion |

## Verification

See [Verification Method](references/verification-method.md) for step-by-step verification.

## Best Practices

1. **Primary action first**: Always call `huawei_scan_cce_availability_risk` first; use manual inventory queries only if the primary scan fails or the user requests specific detail
2. **Control-plane data gap**: When CCE managed control plane does not expose master nodes, mark it as a data gap in the report — do NOT assume master HA
3. **Core addon awareness**: Even when `kube-system` is in `exclude_namespaces`, CoreDNS, nginx-ingress, and ingress-nginx are still individually identified and checked
4. **Gateway identification**: Use `gateway_keywords` to identify gateway-class workloads; adjust keywords for custom gateway implementations
5. **Remediation authorization**: All real remediation (scaling replicas, creating PDB, modifying probes, adjusting affinity, migrating nodes, resizing node pools) requires explicit user authorization before execution
6. **Remediation hand-off**: When remediation is needed, hand off to `huawei-cloud-cce-auto-remediation-runner` with proper safeguards and user confirmation
7. **Read-only boundary**: This skill does NOT scale replicas, create PDBs, modify probes, adjust affinity, migrate nodes, or resize node pools — it only generates remediation plans and YAML suggestions
8. **Resource overcommit interpretation**: CPU overcommit ratio > 4x is marked as low risk (may be intentional burst); memory overcommit ratio > 2x is marked as medium risk (OOM and bin-packing risk)

## Reference Documents

| Document | Description |
|----------|-------------|
| [Workflow](references/workflow.md) | Scan workflow, evidence collection steps, and risk classification rules |
| [Risk Rules](references/risk-rules.md) | Safety constraints, mutation boundaries, and authorization requirements |
| [Output Schema](references/output-schema.md) | Complete JSON response format for scan results |
| [Verification Method](references/verification-method.md) | Step-by-step verification for skill setup and scan execution |
| [Common Pitfalls](references/common-pitfalls.md) | Troubleshooting guides for scan pitfalls |

## Notes

- **Read-only by design** — this skill does NOT modify workloads, PDBs, probes, affinity, node pools, or cluster configuration
- **Remediation hand-off** — all mutation suggestions are handed off to `huawei-cloud-cce-auto-remediation-runner` with `requires_confirmation: true`
- **Never expose or log AK/SK or environment variable values**
- **All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls**
- **Data gaps** — when CCE managed control plane does not expose master nodes, the scan marks this as a data gap and recommends verifying in the CCE console/API
- **Gateway keywords** — default keywords cover common gateway implementations; custom gateways can be added via `gateway_keywords` parameter
- **`kube-system` exclusion** — business risk scanning excludes `kube-system` by default, but core addons (CoreDNS, nginx-ingress, ingress-nginx) are still individually checked for anti-affinity and distribution risks

## Common Pitfalls

See [Common Pitfalls & Solutions](references/common-pitfalls.md) for detailed troubleshooting guides.

**Quick Reference**:

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Assuming master HA | Report concludes "master HA OK" with no visible master nodes | Mark as data gap; recommend CCE console/API verification |
| Skipping PDB check | Missing PDB for multi-replica gateway not flagged | Include gateway keywords and check PDB for all multi-replica workloads |
| Ignoring gateway concentration | All gateway Pods on one node/AZ | Use `gateway_keywords` and check Pod distribution across nodes/AZs |
| Treating CPU overcommit as critical | CPU limit/request ratio > 4x flagged as critical | Mark as low risk; confirm whether intentional burst design |
| Missing resource requests | Containers with no CPU/memory requests not flagged | Always check request/limit presence; mark missing requests as medium risk |
| Excluding core addons | `kube-system` excluded removes CoreDNS from checks | Core addons are individually identified regardless of namespace exclusion |
| Wrong cluster_id | API returns 404 or empty results | Verify cluster ID via `huawei_list_cce_clusters` |
| Credential permission denied | API returns 403 | Check IAM permissions for CCE node/workload/metrics access |
| Metrics API unavailable | Node/Pod metrics query fails | Ensure metrics-server addon is installed in cluster |