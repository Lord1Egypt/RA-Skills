---
name: huawei-cloud-cce-cost-optimization-advisor
description: |
  Huawei Cloud CCE cost optimization analysis skill. Identifies idle resources, oversized CPU/memory requests,
  low-utilization nodes, 24h/7d utilization trends, HPA recommendations, and node autoscaler policy optimization.
  Read-only analysis and configuration suggestions only — does not modify HPA, autoscaler, node pools, or workloads
  without explicit user confirmation.
  Trigger: user mentions "cost optimization", "成本优化", "cost advisor", "成本顾问", "resource waste", "资源浪费",
  "cost reduction", "成本降低", "billing analysis", "账单分析", "over-provisioned", "超配", "CCE cost", "idle nodes",
  "oversized request", "HPA recommendation", "autoscaler policy"
tags: [cce, cost-optimization, resource-utilization, hpa, autoscaler]
---

# Huawei Cloud CCE Cost Optimization Advisor

## Overview

Analyze CCE (Cloud Container Engine) cluster cost optimization opportunities. This skill performs read-only analysis and generates configuration suggestions — it does **not** directly modify HPA, autoscaler, node pools, or workload requests. All configuration changes require explicit user confirmation.

**Analysis scope**:

- 24-hour and 7-day node CPU/memory utilization trends
- Low-utilization node detection (below cluster average or below 30%)
- Oversized resource request detection (business workloads only)
- HPA and node autoscaler status review and recommendations
- Cost optimization report with execution plan

**Architecture**: Python SDK v3 → CCE API + AOM PromQL → Inventory + Metrics → Cost Analysis → Report

## Security Constraints

### Dangerous Operation Confirmation Mechanism

> **This skill enforces a strict read-only-by-default policy. All write operations require `confirm=true`.**

#### Operations Requiring Confirmation

| Tool | Operation Type | Risk Level | Description |
|------|---------------|------------|-------------|
| `huawei_configure_cce_hpa` | Create/Update HPA | 🟠 High | Creates or replaces a HorizontalPodAutoscaler |
| Node pool resize/scale-down | Scale | 🟠 High | Reduces node pool capacity |

**Write operations without `confirm=true` return a preview only**. The `huawei_configure_cce_hpa` tool returns a manifest preview and risk warning when called without `confirm=true`. Only after explicit user approval can it be called with `confirm=true` to apply the configuration.

#### Workflow

**Step 1: Preview Operation** — Call without `confirm=true`

```bash
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 \
  cluster_id=xxx \
  workload_name=my-deploy \
  namespace=default \
  min_replicas=1 \
  max_replicas=3 \
  target_cpu_utilization=60
```

Returns: HPA manifest preview, risk warning, confirmation hint

**Step 2: Confirm Execution** — Call with `confirm=true` after user approval

```bash
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 \
  cluster_id=xxx \
  workload_name=my-deploy \
  namespace=default \
  min_replicas=1 \
  max_replicas=3 \
  target_cpu_utilization=60 \
  confirm=true
```

### Prohibited Actions

- **No automatic node pool scale-down** — never delete nodes or shrink node pools automatically
- **No workload request modification** — never change CPU/memory requests directly
- **No automatic HPA installation/update** — never apply HPA without explicit user confirmation
- **No autoscaler enable/disable** — never toggle autoscaler without user approval

### Allowed Actions

- Read-only queries: nodes, node pools, pods, deployments, metrics, AOM PromQL
- Generate HPA YAML manifests, autoscaler parameter suggestions, and execution plans
- `huawei_configure_cce_hpa` without `confirm=true` returns preview only

### Credential Security

1. **No persistent credential storage** — AK/SK exists only during API calls
2. **No credential leakage** — never includes AK/SK in logs, responses, or errors
3. **Environment variable preferred** — `HW_ACCESS_KEY` / `HW_SECRET_KEY` / `HW_REGION_NAME`

---

## Prerequisites

### Python Environment

- Python 3.8+
- Install SDKs: `pip install huaweicloudsdkcce huaweicloudsdkcore huaweicloudsdkces`
- Optional for HPA operations: `pip install kubernetes`
- Optional for dashboard charts: `pip install matplotlib numpy`

### Environment Variables (Recommended)

```bash
export HW_ACCESS_KEY="your-access-key-id"
export HW_SECRET_KEY="your-secret-access-key"
export HW_REGION_NAME="cn-north-4"
```

### IAM Permission Policies

Ensure the IAM user has the minimum required permissions:

| Permission | Description |
|------------|-------------|
| `cce:cluster:list` | List clusters |
| `cce:cluster:get` | Get cluster details |
| `cce:node:list` | List nodes |
| `cce:node:get` | Get node details |
| `cce:nodepool:list` | List node pools |
| `cce:nodepool:get` | Get node pool details |
| `aom:*:get` | Read AOM metrics and PromQL data |

---

## Core Commands

### Recommended: Combined Analysis

| Tool | Function | Parameters |
|------|----------|------------|
| `huawei_analyze_cce_cost_optimization` | One-shot cost optimization analysis — inventory, 24h/7d node utilization, pod usage/request, HPA/autoscaler status, and report output | `region`, `cluster_id`, `exclude_namespaces`, `business_namespaces`, `short_hours`, `long_hours`, `top_n`, `output_dir` |

> **Prefer `huawei_analyze_cce_cost_optimization`** for comprehensive analysis. Only use individual tools below for supplementing details, reviewing specific metrics, or manually generating HPA YAML.

### Resource Inventory

| Tool | Function | Parameters |
|------|----------|------------|
| `huawei_list_cce_clusters` | List all CCE clusters in region | `region` |
| `huawei_list_cce_nodes` | List cluster nodes | `region`, `cluster_id` |
| `huawei_get_kubernetes_nodes` | Get Kubernetes node details (including allocatable resources) | `region`, `cluster_id` |
| `huawei_list_cce_nodepools` | List node pools with autoscaling info | `region`, `cluster_id` |
| `huawei_get_cce_pods` | Get pod list with labels, status, requests | `region`, `cluster_id` |
| `huawei_get_cce_deployments` | Get deployment list | `region`, `cluster_id` |
| `huawei_list_cce_hpas` | List HPA configurations (excludes kube-system by default) | `region`, `cluster_id` |

### Metrics Analysis

| Tool | Function | Parameters |
|------|----------|------------|
| `huawei_get_cce_node_metrics_topN` | Node CPU/memory/disk utilization Top N | `region`, `cluster_id`, `top_n`, `hours` |
| `huawei_get_cce_node_metrics` | Single node utilization time series | `region`, `cluster_id`, `node_ip`, `hours` |
| `huawei_get_cce_pod_metrics_topN` | Pod CPU/memory utilization Top N (supports custom PromQL) | `region`, `cluster_id`, `top_n`, `hours`, `cpu_query`, `memory_query` |
| `huawei_get_cce_pod_metrics` | Single pod utilization time series | `region`, `cluster_id`, `pod_name`, `namespace`, `hours` |
| `huawei_get_aom_metrics` | Generic AOM PromQL query | `region`, `aom_instance_id`, `query`, `hours` |

### Elasticity Policy

| Tool | Function | Risk Level | Requires Confirmation |
|------|----------|------------|----------------------|
| `huawei_generate_cce_hpa_manifest` | Generate `autoscaling/v2` HPA YAML (no cluster modification) | 🟢 Low | No |
| `huawei_configure_cce_hpa` | Create or replace HPA in cluster | 🟠 High | **Yes** (`confirm=true`) |

**HPA configuration workflow**:

1. Use `huawei_generate_cce_hpa_manifest` or `huawei_configure_cce_hpa` without `confirm=true` to generate a preview
2. Review the manifest with the user
3. Only after explicit user approval, call `huawei_configure_cce_hpa` with `confirm=true`

> **HPA recommendations must be based on request sizing**. If requests are clearly oversized, first recommend calibrating requests, then configure HPA.

### Dashboard

| Tool | Function | Parameters |
|------|----------|------------|
| `huawei_generate_monitor_dashboard` | Generate monitoring dashboard chart images | `region`, `cluster_id`, `metrics_type`, `hours` |

---

## Parameter Reference

### Common Parameters

All tools accept these common parameters for authentication and region:

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `region` | string | Yes | — | Huawei Cloud region code (e.g., `cn-north-4`) |
| `cluster_id` | string | Yes* | — | CCE cluster ID; not required for `huawei_list_cce_clusters` |
| `ak` | string | No | env `HW_ACCESS_KEY` | Access Key ID; environment variable preferred |
| `sk` | string | No | env `HW_SECRET_KEY` | Secret Access Key; environment variable preferred |
| `project_id` | string | No | auto | IAM project ID; auto-resolved from region if omitted |

\* `cluster_id` is not required for `huawei_list_cce_clusters` (lists all clusters in region).

### Combined Analysis Parameters (`huawei_analyze_cce_cost_optimization`)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `region` | string | Yes | — | Huawei Cloud region code |
| `cluster_id` | string | Yes | — | CCE cluster ID |
| `short_hours` | int | No | `24` | Short-window metrics duration in hours |
| `long_hours` | int | No | `168` (7d) | Long-window metrics duration in hours |
| `top_n` | int | No | `50` | Top N pods/nodes for oversized-request and utilization ranking |
| `exclude_namespaces` | string | No | `kube-system` | Comma-separated namespaces to exclude from analysis |
| `business_namespaces` | string | No | — | Comma-separated namespaces to treat as business workloads; if omitted, all non-excluded namespaces are analyzed |
| `output_dir` | string | No | — | Directory to write summary JSON and report markdown |
| `include_raw` | bool | No | `false` | Include raw metrics data in output |

### HPA Parameters (`huawei_generate_cce_hpa_manifest` / `huawei_configure_cce_hpa`)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `workload_name` | string | Yes | — | Target Deployment/StatefulSet name |
| `namespace` | string | Yes | — | Namespace of the target workload |
| `min_replicas` | int | Yes | — | Minimum replica count for HPA |
| `max_replicas` | int | Yes | — | Maximum replica count for HPA |
| `workload_type` | string | No | `deployment` | Workload kind: `deployment` or `statefulset` |
| `hpa_name` | string | No | auto | HPA object name; defaults to `<workload_name>-hpa` |
| `target_cpu_utilization` | int | No | `60` | Target average CPU utilization percentage |
| `target_memory_utilization` | int | No | — | Target average memory utilization percentage; omit to skip memory metric |
| `behavior` | object | No | — | HPA behavior policy (scaling rates, stabilization windows) |
| `confirm` | bool | No | `false` | **`huawei_configure_cce_hpa` only**: must be `true` to apply changes |

### Metrics Parameters (`huawei_get_cce_node_metrics_topN` / `huawei_get_cce_pod_metrics_topN`)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `top_n` | int | No | `10` | Number of top nodes/pods to return |
| `hours` | int | No | `1` | Metrics query time range in hours |
| `cpu_query` | string | No | auto | Custom PromQL for CPU; defaults to built-in query |
| `memory_query` | string | No | auto | Custom PromQL for memory; defaults to built-in query |
| `node_ip` | string | Yes* | — | Required for `huawei_get_cce_node_metrics` (single node) |
| `pod_name` | string | Yes* | — | Required for `huawei_get_cce_pod_metrics` (single pod) |
| `namespace` | string | Yes* | — | Required for `huawei_get_cce_pod_metrics` (single pod) |

\* Only required for single-entity metrics tools.

### Dashboard Parameters (`huawei_generate_monitor_dashboard`)

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `hours` | int | No | `1` | Monitoring data time range in hours |
| `top_n` | int | No | `10` | Top N pods for dashboard ranking |
| `namespace` | string | No | — | Filter by namespace |
| `label_selector` | string | No | — | Filter by label (e.g., `app=nginx`) |
| `output_file` | string | No | auto | Output HTML file path |
| `title` | string | No | auto | Dashboard title |

---

## Analysis Workflow

See [references/workflow.md](references/workflow.md) for detailed analysis steps, thresholds, and decision logic.

### Quick Summary

1. **Scope**: Confirm region, cluster_id, namespace range, and exclusion rules (default: exclude `kube-system`)
2. **Node utilization**: Analyze 24h and 7d windows for CPU/memory usage per node and cluster average
3. **Low-utilization detection**: Flag nodes below cluster average by 20 percentage points or below 60% of cluster average; cluster average below 30% signals overall over-provisioning
4. **Oversized requests**: Compare business workload request vs actual p95 usage; mark as `high` (p95 < 33% of request), `optimize` (p95 < 50%), or `observe` (short-window only)
5. **Elasticity review**: Check node pool autoscaling and HPA status; generate recommendations
6. **Output**: Summary, utilization tables, oversized request list, HPA/autoscaler recommendations, risks, and verification steps

---

## Risk Rules

See [references/risk-rules.md](references/risk-rules.md) for complete safety boundaries.

**Key constraints**:

- Auto-execution limited to R1 read-only queries only
- No automatic scale-down, request modification, or HPA/autoscaler changes
- Must reference both 24h and 7d windows before recommending scale-down
- Cost optimization suggestions must include rollback strategy and verification metrics
- Data gaps (missing metrics, missing requests, invisible HPA) must be flagged in the report

---

## Output Schema

See [references/output-schema.md](references/output-schema.md) for the complete JSON report structure.

All tools return JSON with:

- `status` / `success`: operation result
- `data`: analysis results, metrics, or configuration preview
- `message`: human-readable description
- `warning`: risk warning for write operations (preview mode only)
- `files`: paths to generated summary JSON and report markdown

---

## Supported Regions

| Region Code | Region Name |
|-------------|-------------|
| cn-north-4 | North China-Beijing 4 |
| cn-north-1 | North China-Beijing 1 |
| cn-east-3 | East China-Shanghai 1 |
| cn-south-1 | South China-Guangzhou |
| ap-southeast-1 | Asia-Pacific-Hong Kong |
| ap-southeast-2 | Asia Pacific-Bangkok |
| ap-southeast-3 | Asia Pacific-Singapore |

---

## Best Practices

1. **Run the combined analysis first** — use `huawei_analyze_cce_cost_optimization` for a complete picture before drilling into individual tools; avoid piecemeal queries that miss cross-resource dependencies.
2. **Always check both time windows** — rely on 7-day data for stable optimization decisions; use 24-hour data only for short-term fluctuation observation, never as the sole basis for scale-down recommendations.
3. **Exclude kube-system by default** — system workloads have fixed sizing requirements; analyzing them produces misleading oversized-request signals and wastes analysis capacity.
4. **Calibrate requests before configuring HPA** — HPA scales based on request percentages; if requests are oversized, HPA will trigger premature scaling. Fix requests first, then set HPA targets.
5. **Use environment variables for credentials** — prefer `HW_ACCESS_KEY` / `HW_SECRET_KEY` over passing AK/SK as parameters to avoid credential leakage in command history and logs.
6. **Review HPA preview before confirming** — always call `huawei_configure_cce_hpa` without `confirm=true` first; inspect the manifest YAML and risk warning with the user before applying.
7. **Include rollback strategy in every recommendation** — cost optimization changes can impact availability; every suggestion must specify how to revert and how to verify the change was safe.
8. **Flag data gaps explicitly** — if metrics are missing, requests are absent, or HPA status is invisible, report these as data gaps; do not infer optimization decisions from incomplete data.
9. **Set `top_n` appropriately** — use `top_n=50` for large clusters (100+ pods) to capture all significant outliers; reduce to `top_n=10` for focused analysis of specific namespaces.
10. **Save outputs to a persistent directory** — use `output_dir` to write the summary JSON and report markdown to a known location; this enables later review and comparison across multiple analysis runs.

---

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Missing AK/SK credentials | All tools return `"success": false` with credential error | Set `HW_ACCESS_KEY` and `HW_SECRET_KEY` environment variables before running |
| Wrong cluster ID | Empty or error results from cluster-specific tools | Run `huawei_list_cce_clusters` first to confirm the correct `cluster_id` for your region |
| Analyzing kube-system workloads | False oversized-request alerts on system DaemonSets | Set `exclude_namespaces=kube-system` (default) or add other system namespaces |
| Single-window scale-down decision | Node marked low-utilization in 24h only but stable in 7d | Always require both `short_hours=24` and `long_hours=168` before recommending scale-down |
| HPA on oversized requests | HPA triggers scaling at low actual usage because requests are inflated | First reduce CPU/memory requests to realistic values, then configure HPA with `target_cpu_utilization=60` |
| Missing AOM metrics | Empty utilization data, `data_gaps` flagged in report | Verify IAM has `aom:*:get` permission and AOM is enabled on the cluster |
| Applying HPA without preview | `huawei_configure_cce_hpa` called with `confirm=true` without review | Always call without `confirm=true` first, review manifest, then re-run with `confirm=true` |
| kubernetes SDK not installed | HPA tools fail with `"Kubernetes SDK not installed"` | Install with `pip install kubernetes` before using HPA listing or configuration tools |
| Large cluster with small `top_n` | Oversized-request pods missing from report | Increase `top_n` to 50 or higher for clusters with 100+ business pods |
| No output directory specified | Report files written to temporary location, may be lost | Set `output_dir` to a persistent path like `./cost-reports` |

---

## Output Format

All tools return JSON with status, success, data, message, warning, and iles fields. See [references/output-schema.md](references/output-schema.md) for the complete report structure.

## Verification

See [Verification Method](references/verification-method.md) for step-by-step verification.

## Cross-Skill References

| Skill | When to Use |
|-------|-------------|
| `huawei-cloud-cce-cluster-management` | Create/delete/hibernate clusters, manage node pools, manage addons, cordon/uncordon/drain nodes, create/delete individual nodes |

---

## Reference Documents

| Document | Path | Description |
|----------|------|-------------|
| Workflow | [references/workflow.md](references/workflow.md) | Detailed analysis workflow, thresholds, and decision logic |
| Risk Rules | [references/risk-rules.md](references/risk-rules.md) | Safety boundaries, prohibited actions, and confirmation requirements |
| Output Schema | [references/output-schema.md](references/output-schema.md) | Cost optimization report JSON structure |

---

## Notes

- Ensure AK/SK has correct IAM permissions (CCE read + AOM read)
- Default analysis excludes `kube-system` namespace
- HPA recommendations require request sizing to be reasonable first
- Node scale-down suggestions require both 24h and 7d data confirmation
- Cost optimization reports must include rollback strategy
- Data gaps must be explicitly flagged