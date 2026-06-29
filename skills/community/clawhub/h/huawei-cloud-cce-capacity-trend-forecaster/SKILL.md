---
id: huawei-cloud-cce-capacity-trend-forecaster
name: huawei-cloud-cce-capacity-trend-forecaster
description: |
  Use when analyzing Huawei Cloud CCE periodic capacity trends, forecasting resource bottlenecks,
  simulating node/workload elasticity policies, generating capacity curve charts and reports,
  comparing recurring history records, or tuning HPA and node autoscaler configurations.
  Trigger: user mentions "capacity forecast", "容量预测", "capacity trend", "容量趋势",
  "resource trend", "资源趋势", "capacity planning", "容量规划", "capacity risk", "容量风险",
  "resource exhaustion", "资源耗尽", "HPA tuning", "node autoscaler", "capacity report",
  "capacity simulation"
tags: [cce, capacity, forecast, trend]
---

# Huawei Cloud CCE Capacity Trend Forecaster

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill analyzes CCE capacity trends over a user-selected period (1 hour to 1 month), forecasts resource bottlenecks, simulates elasticity policies, generates curve charts and reports, and compares recurring history records. The core principle is to treat capacity as a time-series problem: rising trends with high p95 signal risk, low utilization with conservative simulation signals cost optimization opportunity.

This skill has **read-only tools** (collection, analysis, simulation, report generation) and **preview tools** for HPA and autoscaler configuration. Applying configuration changes requires a two-step confirmation workflow with `confirm=true` and explicit user approval.

### Related Skills

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-metric-analyzer` | Query Pod/Node CPU/memory/disk metrics and anomaly detection |
| `huawei-cloud-cce-node-failure-diagnoser` | Node failure diagnosis (NotReady, resource pressure, NPD events) |
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod-level failure diagnosis (CrashLoopBackOff, ImagePullBackOff, etc.) |
| `huawei-cloud-cce-workload-failure-diagnoser` | Workload-level failure diagnosis |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (scale, reboot, drain) |
| `huawei-cloud-cce-cost-optimization-advisor` | Cost optimization recommendations |
| `huawei-cloud-cce-observability-context-builder` | Observability context enrichment |

### Capabilities

1. Collect node metrics, HPA status, nodepool autoscaling status, and business Deployment inventory
2. Calculate trend statistics (avg, min, max, p95, slope, trend direction) for CPU, memory, and disk
3. Predict bottleneck arrival time against configurable thresholds
4. Simulate recommended node counts and reducible nodes with headroom
5. Generate JSON/Markdown/HTML reports with embedded SVG curve charts
6. Store and compare recurring history records to track before-and-after effects
7. Preview and apply HPA configuration with two-step confirmation workflow
8. Recommend node autoscaler min/max bounds adjustments

### Typical Use Cases

- Run a 6-hour capacity trend analysis and identify rising CPU trends approaching bottleneck threshold
- Compare weekly capacity records to validate that a previous optimization reduced utilization
- Simulate node requirements with 60% CPU target and 15% headroom, then preview HPA adjustments
- Forecast when memory will reach 80% bottleneck threshold based on current slope
- Generate a monthly capacity report with curve charts for stakeholder review
- Check HPA coverage percentage and preview HPA manifest for uncovered Deployments

---

## Prerequisites

### Python Dependencies

The dispatcher script requires Python >= 3.6 and the following packages:

- `huaweicloudsdkcore`
- `huaweicloudsdkaom`
- `huaweicloudsdkcce`
- `huaweicloudsdkiam`

### Credential Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| HUAWEI_AK | Yes | Huawei Cloud Access Key |
| HUAWEI_SK | Yes | Huawei Cloud Secret Key |
| HUAWEI_REGION | No | Default region (overrides `region` param if set) |
| HUAWEI_PROJECT_ID | No | Project ID (auto-obtained via IAM API when not set) |
| HUAWEI_SECURITY_TOKEN | No | Required when using temporary AK/SK |

🚫 **Never expose or log AK/SK values.** Credentials exist only in the current request call stack and are released after each invocation. Do not write credentials to files, logs, or responses.

✅ **Use environment variables** `HUAWEI_AK` / `HUAWEI_SK` for authentication. The dispatcher reads them automatically.

**Security rules for credentials:**

1. **No persistent storage** — never write AK/SK, tokens, or certificates to disk files
2. **No long-term memory cache** — AK/SK exists only during the current API call and is released afterward
3. **Project ID memory cache only** — only non-sensitive project IDs may be cached in process memory (never written to disk)
4. **No log leakage** — never include AK/SK in logs, response output, or error messages
5. **Output desensitization** — output only capacity, trend, and simulation information; never expose authentication credentials

AK/SK may be provided in two ways:
- Via environment variables `HUAWEI_AK` / `HUAWEI_SK` (recommended)
- Via per-call parameters `ak` and `sk` (not recommended for production)

### IAM Permissions

| Permission | Description |
|------------|-------------|
| `cce:cluster:list` | Query CCE cluster metadata |
| `cce:node:list` | Query Kubernetes node inventory |
| `cce:nodepool:list` | Query CCE nodepool autoscaling status |
| `cce:deployment:list` | Query business Deployment inventory |
| `aom:metric:get` | Query AOM Prometheus metrics (CPU, memory, disk time series) |
| `cce:hpa:list` | Query HPA inventory and target references |
| `cce:hpa:configure` | Configure HPA (preview + confirm workflow) |

---

## Core Tools

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> [key=value ...]
```

### Two-Step Confirmation Workflow for Mutation Operations

> **Mutation operations (apply HPA configuration with `confirm=true`, change nodepool autoscaling bounds, resize node pools) require `confirm=true` to execute. Without `confirm`, the tool returns a preview and confirmation prompt only.**

**Step 1: Preview** — call without `confirm`:
```bash
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default deployment_name=<name> \
  min_replicas=2 max_replicas=10 target_cpu_percent=60
```

Returns: operation preview, target HPA, configuration fields, and confirmation example. No real modification is performed.

**Step 2: Confirm execution** — call again with `confirm=true`:
```bash
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default deployment_name=<name> \
  min_replicas=2 max_replicas=10 target_cpu_percent=60 \
  confirm=true
```

#### Operations Requiring Confirmation

| Tool | Operation | Risk Level | Description |
|------|-----------|-----------|-------------|
| `huawei_configure_cce_hpa` | Configure HPA | 🟠 High | Apply HPA configuration changes; preview without `confirm`, apply with `confirm=true` |
| Nodepool autoscaling changes | Modify bounds | 🟠 High | Change min/max nodes in nodepool autoscaler configuration |
| Node pool resize | Resize pool | 🔴 High | Add or remove nodes from a node pool |

#### Prohibited Actions

| Action | Description |
|--------|-------------|
| Automatic downsizing on single period | Do not treat a single period as enough evidence for aggressive downsizing; prefer at least two comparable records |
| Apply HPA without preview | Always preview first, then confirm only after explicit user approval |
| Skip rollback plan | For real changes, provide the exact reason, expected effect, rollback path, and validation checks |
| Modify workloads directly | Do not mutate Deployment replicas, node pools, or addons without explicit authorization |

### Capacity Trend Analysis (Read-Only)

| Action | Description | Required Params |
|--------|-------------|-----------------|
| `huawei_analyze_cce_capacity_trend` | Main analyzer: collect metrics, compute trends, simulate elasticity, generate reports with curve charts, store history records | `region`, `cluster_id` |

```bash
# Basic 6-hour analysis
python3 scripts/huawei-cloud.py huawei_analyze_cce_capacity_trend \
  region=cn-north-4 cluster_id=<cluster-id> hours=6

# Weekly analysis with custom targets and output directory
python3 scripts/huawei-cloud.py huawei_analyze_cce_capacity_trend \
  region=cn-north-4 cluster_id=<cluster-id> hours=168 \
  target_cpu_percent=60 target_memory_percent=70 \
  headroom_percent=15 bottleneck_percent=80 \
  output_dir=debug/capacity-trend/<cluster>

# Monthly analysis with business namespace scope and action note
python3 scripts/huawei-cloud.py huawei_analyze_cce_capacity_trend \
  region=cn-north-4 cluster_id=<cluster-id> hours=744 \
  business_namespaces=default,production \
  action_note="Scaled HPA max_replicas from 5 to 10 on 2026-05-28"

# Recurring run for comparison
python3 scripts/huawei-cloud.py huawei_analyze_cce_capacity_trend \
  region=cn-north-4 cluster_id=<cluster-id> hours=6 \
  output_dir=debug/capacity-trend/<cluster> \
  history_dir=debug/capacity-trend/<cluster>/history
```

### Inventory and Context (Read-Only)

| Action | Description | Required Params |
|--------|-------------|-----------------|
| `huawei_list_cce_clusters` | List CCE clusters in a region | `region` |
| `huawei_get_kubernetes_nodes` | Get Kubernetes node inventory for a cluster | `region`, `cluster_id` |
| `huawei_list_cce_nodepools` | List CCE nodepools with autoscaling status | `region`, `cluster_id` |
| `huawei_get_cce_deployments` | Get business Deployment inventory | `region`, `cluster_id` |
| `huawei_list_cce_hpas` | List HPA inventory and target references | `region`, `cluster_id` |

```bash
# List clusters
python3 scripts/huawei-cloud.py huawei_list_cce_clusters region=cn-north-4

# Get node inventory
python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes \
  region=cn-north-4 cluster_id=<cluster-id>

# List nodepools
python3 scripts/huawei-cloud.py huawei_list_cce_nodepools \
  region=cn-north-4 cluster_id=<cluster-id>

# Get deployments
python3 scripts/huawei-cloud.py huawei_get_cce_deployments \
  region=cn-north-4 cluster_id=<cluster-id>

# List HPA configurations
python3 scripts/huawei-cloud.py huawei_list_cce_hpas \
  region=cn-north-4 cluster_id=<cluster-id>
```

### Metrics (Read-Only)

| Action | Description | Required Params |
|--------|-------------|-----------------|
| `huawei_get_cce_node_metrics_topN` | Get Node CPU/memory/disk TopN | `region`, `cluster_id` |
| `huawei_get_aom_metrics` | Get AOM Prometheus metric time series | `region`, `cluster_id` |

```bash
# Node metrics TopN
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics_topN \
  region=cn-north-4 cluster_id=<cluster-id> top_n=10 hours=6

# AOM metrics
python3 scripts/huawei-cloud.py huawei_get_aom_metrics \
  region=cn-north-4 cluster_id=<cluster-id>
```

### HPA Configuration (Preview + Confirm)

| Action | Description | Risk Level | Requires `confirm` | Required Params |
|--------|-------------|-----------|--------------------|-----------------|
| `huawei_generate_cce_hpa_manifest` | Generate HPA manifest preview | 🟢 Low | No | `region`, `cluster_id`, `namespace`, `deployment_name`, `min_replicas`, `max_replicas`, `target_cpu_percent` |
| `huawei_configure_cce_hpa` | Preview or apply HPA configuration | 🟠 High | **Yes** for apply | `region`, `cluster_id`, `namespace`, `deployment_name`, `min_replicas`, `max_replicas`, `target_cpu_percent` |

```bash
# Generate HPA manifest preview (read-only)
python3 scripts/huawei-cloud.py huawei_generate_cce_hpa_manifest \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default deployment_name=<name> \
  min_replicas=2 max_replicas=10 target_cpu_percent=60

# Preview HPA configuration (no execution)
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default deployment_name=<name> \
  min_replicas=2 max_replicas=10 target_cpu_percent=60

# Confirm and apply HPA configuration
python3 scripts/huawei-cloud.py huawei_configure_cce_hpa \
  region=cn-north-4 cluster_id=<cluster-id> \
  namespace=default deployment_name=<name> \
  min_replicas=2 max_replicas=10 target_cpu_percent=60 \
  confirm=true
```

---

## Parameter Reference

### Capacity Trend Analysis Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | CCE cluster ID |
| `hours` | No | Analysis window in hours, clamped to 1-744 (default: 6) |
| `output_dir` | No | Directory to write reports, charts, and history records |
| `history_dir` | No | Override the default history folder for recurring comparison |
| `business_namespaces` | No | Comma-separated namespace allowlist for business Deployments |
| `exclude_namespaces` | No | Comma-separated namespace exclude list (default: `kube-system`) |
| `target_cpu_percent` | No | Simulation CPU target utilization (default: 60) |
| `target_memory_percent` | No | Simulation memory target utilization (default: 70) |
| `headroom_percent` | No | Simulation headroom percentage (default: 15) |
| `bottleneck_percent` | No | Bottleneck threshold percentage (default: 80) |
| `action_note` | No | Record an optimization action or operational event for before-and-after comparison |
| `ak` | No | Access Key ID; `HUAWEI_AK` environment variable preferred |
| `sk` | No | Secret Access Key; `HUAWEI_SK` environment variable preferred |
| `project_id` | No | Huawei Cloud project ID; auto-obtained via IAM API when not provided |

### HPA Configuration Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Huawei Cloud region |
| `cluster_id` | Yes | CCE cluster ID |
| `namespace` | Yes | Kubernetes namespace of the target Deployment |
| `deployment_name` | Yes | Target Deployment name |
| `min_replicas` | Yes | HPA minimum replica count |
| `max_replicas` | Yes | HPA maximum replica count |
| `target_cpu_percent` | No | HPA target CPU utilization percentage (default: 60) |
| `target_memory_percent` | No | HPA target memory utilization percentage |
| `confirm` | No | Must be explicitly set to `true` to apply HPA configuration; without it, returns preview only |

---

## Output Format

### Capacity Trend Report

Each analysis run writes the following files:

| File | Description |
|------|-------------|
| `capacity-trend-summary.json` | Full structured JSON output (see `references/output-schema.md`) |
| `capacity-trend-report.md` | Markdown report with trend statistics and recommendations |
| `capacity-trend-report.html` | HTML report with embedded SVG curve charts |
| `capacity-trend-chart.svg` | CPU/memory/disk trend curve chart |
| `capacity-simulation-chart.svg` | Simulation result curve chart |
| `history/capacity-trend-*.json` | Individual history record for recurring comparison |
| `capacity-trend-history.jsonl` | Append-only history log for cross-run comparison |

### Key Output Fields

| Field | Description |
|-------|-------------|
| `capacity_stats` | Per-resource trend statistics: avg, min, max, p95, latest, slope, trend direction, bottleneck prediction |
| `elasticity` | HPA coverage percentage, node autoscaler enabled status with min/max/current nodes |
| `simulation` | Recommended node counts, reducible nodes, capped sample percentage |
| `recommendations` | Prioritized optimization suggestions with area, reason, and configuration methods |
| `history_comparison` | Deltas between current and previous record when history is available |
| `data_gaps` | Missing metric data that prevents reliable trend conclusions |

See `references/output-schema.md` for the full JSON response schema.

---

## Verification

1. Run the dispatcher with a known region and cluster to confirm connectivity:
   ```bash
   python3 scripts/huawei-cloud.py huawei_analyze_cce_capacity_trend \
     region=cn-north-4 cluster_id=<cluster-id> hours=1
   ```
2. Verify that `capacity_stats` includes trend direction and bottleneck prediction for CPU, memory, and disk
3. Verify that `simulation.avg_recommended_nodes` and `max_recommended_nodes` are within autoscaler min/max bounds
4. Verify that `capacity-trend-report.html` contains embedded SVG charts
5. Run a second analysis and verify that `history_comparison` shows deltas from the first run
6. Test HPA preview workflow: call `huawei_configure_cce_hpa` without `confirm` and verify it returns a preview only
7. After a confirmed HPA change, run a new capacity analysis to compare before-and-after effects

---

## Best Practices

1. Always use `huawei_analyze_cce_capacity_trend` as the main action; it collects, analyzes, simulates, and generates reports in a single call
2. Accept windows from 1 hour to 1 month; common schedules are every 6 hours, daily, weekly, and monthly
3. Do not treat a single period as enough evidence for aggressive downsizing; prefer at least two comparable records before lowering baseline capacity
4. If the simulation recommends lower capacity but p95 or max utilization is close to the bottleneck threshold, keep headroom and propose observation instead
5. For real changes, provide the exact reason, expected effect, rollback path, and validation checks
6. Configuration execution must be user-approved and should be followed by a new capacity record to compare before-and-after effects
7. Use `action_note` to record optimization actions so the next cycle can compare their effects
8. If AOM metrics are unavailable, report the gap and do not invent trend conclusions
9. Always consider both workload elasticity (HPA) and node elasticity (nodepool autoscaling) when making recommendations

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/workflow.md` | Capacity trend workflow: scope, collection, trend analysis, elasticity awareness, recurring comparison, and output order |
| `references/simulation-rules.md` | Simulation rules: targets, node simulation formula, HPA advice, node autoscaler advice, and execution boundaries |
| `references/output-schema.md` | Output JSON schema for capacity trend analysis results |
| [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) | SDK reference |
| [Huawei Cloud API Explorer](https://support.huaweiicloud.com/apiexplorer/index.html) | API interactive explorer |

---

## Notes

1. This skill has **read-only tools** (analysis, simulation, report generation) and **preview tools** for HPA configuration — applying configuration changes requires `confirm=true` two-step confirmation
2. Do not treat a single period as enough evidence for aggressive downsizing; prefer at least two comparable records
3. If simulation recommends lower capacity but p95 is near bottleneck threshold, keep headroom and propose observation
4. Never expose or log AK/SK or environment variable values
5. All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls
6. Use `action_note` to record optimization events so subsequent runs can validate their effects
7. If remediation actions are needed (scale, reboot, drain), output recommendations only and hand off to `huawei-cloud-cce-auto-remediation-runner`

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Treating a single period as enough evidence for downsizing | Prefer at least two comparable records before lowering baseline capacity |
| Recommending lower capacity when p95 is near bottleneck threshold | Keep headroom and propose observation; low average does not override high p95 |
| Applying HPA configuration without preview step | Always call `huawei_configure_cce_hpa` without `confirm` first to preview; only add `confirm=true` after explicit user approval |
| Inventing trend conclusions when AOM metrics are unavailable | Report the data gap explicitly; do not fabricate trend analysis from incomplete data |
| Ignoring node elasticity when making workload elasticity recommendations | Always consider both HPA coverage and nodepool autoscaling together; workload scaling is constrained by node capacity |
| Not running a follow-up analysis after configuration changes | After any confirmed change, run a new capacity analysis and compare before-and-after effects using `action_note` |
| Using default simulation targets for latency-sensitive or bursty systems | Lower CPU/memory targets or increase headroom for systems with burst patterns or strict latency requirements |
| Skipping history comparison for recurring runs | Always compare the latest record with previous records to track utilization deltas and validate recommendations |