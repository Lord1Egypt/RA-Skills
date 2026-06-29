---
id: huawei-cloud-cce-ops-report-generator
name: huawei-cloud-cce-ops-report-generator
description: |
  Use when generating consolidated CCE operations reports that combine daily inspection,
  capacity trend, availability risk, cost optimization, and on-call context into weekly,
  monthly, SLA, capacity, or stability reports with Markdown and HTML output.
  Trigger: user mentions "ops report", "运维报告", "report generation", "报告生成",
  "cluster report", "集群报告", "weekly report", "月度报告", "SLA report", "capacity report",
  "stability report", "operations summary", "运营总结", "consolidated report", "综合报告",
  "CCE reporting", "oncall report", "值班报告"
tags: [cce, ops-report, report, dashboard]
---

# Huawei Cloud CCE Ops Report Generator

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill generates consolidated operations reports for Huawei Cloud CCE clusters. It aggregates outputs from daily inspection, capacity trend forecasting, availability risk scanning, cost optimization analysis, and optional on-call context into structured reports (weekly, monthly, SLA, capacity, stability). Default behavior is read-only analysis and report generation.

**Architecture**: Python dispatcher (`scripts/huawei-cloud.py`) → `huawei_generate_ops_report` → aggregates from `huawei-cloud-cce-daily-cluster-inspector`, `huawei-cloud-cce-capacity-trend-forecaster`, `huawei-cloud-cce-availability-risk-scanner`, `huawei-cloud-cce-cost-optimization-advisor`, on-call context → Markdown + HTML + JSON reports

### Related Skills

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-daily-cluster-inspector` | Daily health inspection and risk summarization |
| `huawei-cloud-cce-capacity-trend-forecaster` | Capacity trend analysis, bottleneck forecasting, HPA simulation |
| `huawei-cloud-cce-availability-risk-scanner` | Availability risk scanning (single replicas, PDB, AZ distribution) |
| `huawei-cloud-cce-cost-optimization-advisor` | Cost optimization analysis (idle resources, oversized requests) |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions when user authorizes |

### Capabilities

1. One-shot consolidated ops report generation (`huawei_generate_ops_report`)
2. Five report types: `weekly`, `monthly`, `sla`, `capacity`, `stability`
3. Aggregated summaries from inspection, capacity, availability, cost, and on-call sources
4. Prioritized cross-source recommendations with risk levels
5. Markdown and HTML output with trend charts when capacity data is available
6. Optional raw payload traceability (`include_raw=true`)
7. Graceful degradation: reports continue even if individual sources fail, marking data gaps clearly

### Typical Use Cases

- "Generate a weekly ops report for my CCE cluster"
- "Create a monthly operations summary with capacity and availability findings"
- "Produce an SLA report combining inspection and on-call data"
- "Consolidate capacity trends and cost optimization into a stability report"
- "Generate a report with on-call context from last week's incidents"
- "Export a consolidated ops report in HTML with charts"

---

## Prerequisites

### Python Dependencies

The dispatcher script requires Python >= 3.6 and the following packages:

- `huaweicloudsdkcore`
- `huaweicloudsdkcce`
- `huaweicloudsdkaom`
- `huaweicloudsdkhss`
- `huaweicloudsdkvpc`
- `huaweicloudsdkecs`
- `huaweicloudsdkces`
- `huaweicloudsdkevs`
- `huaweicloudsdkeip`
- `huaweicloudsdkelb`
- `huaweicloudsdkiam`
- `kubernetes`
- `matplotlib`
- `numpy`

Install: `pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom huaweicloudsdkhss huaweicloudsdkvpc huaweicloudsdkecs huaweicloudsdkces huaweicloudsdkevs huaweicloudsdkeip huaweicloudsdkelb huaweicloudsdkiam kubernetes matplotlib numpy`

### Credential Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `HUAWEI_AK` | Yes | Huawei Cloud Access Key |
| `HUAWEI_SK` | Yes | Huawei Cloud Secret Key |
| `HUAWEI_REGION` | No | Default region (overrides `region` param if set) |
| `HUAWEI_PROJECT_ID` | No | Project ID (auto-obtained via IAM API when not set) |
| `HUAWEI_SECURITY_TOKEN` | No | Required when using temporary AK/SK |

🚫 **Never expose or log AK/SK values.** Credentials exist only in the current request call stack and are released after each invocation. Do not write credentials to files, logs, or responses.

✅ **Use environment variables** `HUAWEI_AK` / `HUAWEI_SK` for authentication. The dispatcher reads them automatically.

### IAM Permission Requirements

This skill aggregates data from multiple sub-skills. It requires all permissions needed by:

| Sub-Skill | Required Permissions |
|-----------|---------------------|
| `huawei-cloud-cce-daily-cluster-inspector` | CCE cluster/node/workload/event read, AOM alarm read |
| `huawei-cloud-cce-capacity-trend-forecaster` | CCE cluster/node/nodepool/Deployment/HPA read, AOM metrics read |
| `huawei-cloud-cce-availability-risk-scanner` | CCE cluster/node/workload/PDB/Service/Ingress read, AOM metrics read |
| `huawei-cloud-cce-cost-optimization-advisor` | CCE cluster/node/nodepool/Deployment/HPA/Pod read, AOM metrics read |

---

## Core Commands

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### 1. Primary Action: Generate Ops Report

The primary action aggregates all sub-skill outputs into a consolidated report:

```bash
python3 scripts/huawei-cloud.py huawei_generate_ops_report \
  region=cn-north-4 cluster_id=<cluster_id> \
  report_type=weekly \
  output_dir=./output
```

Returns: consolidated summary, cross-source recommendations, data gaps, and output files (Markdown, HTML, JSON, optional SVG charts).

### 2. Supporting Context Actions

For follow-up deep dives after report generation:

| Action | Source Skill | Description |
|--------|-------------|-------------|
| `huawei_cce_auto_inspection` | `huawei-cloud-cce-daily-cluster-inspector` | Full daily health inspection |
| `huawei_analyze_cce_capacity_trend` | `huawei-cloud-cce-capacity-trend-forecaster` | Capacity trend analysis with simulation |
| `huawei_scan_cce_availability_risk` | `huawei-cloud-cce-availability-risk-scanner` | Availability risk scan with remediation plan |
| `huawei_analyze_cce_cost_optimization` | `huawei-cloud-cce-cost-optimization-advisor` | Cost optimization analysis |

---

## Parameter Reference

### `huawei_generate_ops_report` (Primary Action)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | - | CCE cluster ID |
| `report_type` | No | `weekly` | Report type: `weekly`, `monthly`, `sla`, `capacity`, `stability` |
| `hours` | No | Auto (by type) | Analysis window in hours (overrides default for report type) |
| `short_hours` | No | 24 | Short-period lookback for cost analysis |
| `long_hours` | No | 168 | Long-period lookback for cost analysis |
| `exclude_namespaces` | No | `kube-system` | Comma-separated namespaces excluded from business analysis |
| `business_namespaces` | No | - | Comma-separated namespace allowlist for business Deployments |
| `gateway_keywords` | No | `nginx,gateway,ingress,proxy,kong,apisix,traefik` | Keywords for identifying gateway-class workloads |
| `output_dir` | No | - | Directory to persist Markdown, HTML, JSON reports and charts |
| `include_raw` | No | `false` | Include raw source payloads for traceability |
| `oncall_report_path` | No | - | Path to on-call report file for incident context |
| `oncall_summary` | No | - | Inline on-call summary text for incident context |

### Default Hours by Report Type

| Report Type | Default Hours |
|-------------|---------------|
| `weekly` | 168 |
| `monthly` | 744 |
| `sla` | 168 |
| `capacity` | 168 |
| `stability` | 168 |

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

---

## Output Format

See `references/output-schema.md` for the complete JSON response schema.

### Output Files

When `output_dir` is specified, the following files are generated:

| File | Description |
|------|-------------|
| `ops-<type>-summary.json` | Full structured JSON output with summaries, recommendations, and sources |
| `ops-<type>-report.md` | Markdown report with cross-source analysis and recommendations |
| `ops-<type>-report.html` | HTML report with embedded SVG trend charts |
| `ops-capacity-trend.svg` | Capacity trend curve chart (when capacity data available) |
| `ops-capacity-simulation.svg` | Capacity simulation chart (when simulation data available) |
| `ops-<type>-raw.json` | Raw source payloads (when `include_raw=true`) |

### Key Output Fields

| Field | Description |
|-------|-------------|
| `scope` | Report scope: region, cluster_id, excluded namespaces, gateway keywords |
| `report` | Report metadata: type, hours, short_hours, long_hours |
| `summary.daily_cluster_inspector` | Health status and anomaly count |
| `summary.capacity_trend_forecaster` | CPU/memory averages, trend direction, simulation status |
| `summary.availability_risk_scanner` | Risk level and issue count |
| `summary.cost_optimization_advisor` | Underutilized nodes and oversized requests count |
| `summary.oncall_copilot` | On-call context status, source, and summary |
| `recommendations` | Prioritized cross-source recommendation list with source and risk level |
| `data_gaps` | List of sources that failed or had missing data |
| `sources` | Per-source success status and file paths |
| `files` | Output file paths for all generated artifacts |

---

## Workflow

1. Collect `region`, `cluster_id`, report type, time window, namespace scope, and output directory from user
2. Execute `huawei_generate_ops_report` — it aggregates from all five sources internally
3. Review generated Markdown report first, then HTML report for charts and visualization
4. For high-risk findings, trace back to source sections:
   - Daily anomalies → `huawei-cloud-cce-daily-cluster-inspector`
   - Risk level and issue categories → `huawei-cloud-cce-availability-risk-scanner`
   - Oversized requests / low utilization → `huawei-cloud-cce-cost-optimization-advisor`
   - Trend slope / bottleneck projection → `huawei-cloud-cce-capacity-trend-forecaster`
5. If customer asks for remediation, switch to explicit change workflow and require authorization — hand off to `huawei-cloud-cce-auto-remediation-runner`

### Data Gap Handling

- If a source report fails, the aggregate report continues and marks that source as degraded
- If on-call input is missing, mark as a context gap instead of failing the report
- Preserve source file pointers and optional raw payloads (`include_raw=true`) for auditability

---

## Verification

1. Run a weekly report with a known cluster:
   ```bash
   python3 scripts/huawei-cloud.py huawei_generate_ops_report \
     region=cn-north-4 cluster_id=<cluster-id> \
     report_type=weekly output_dir=./output
   ```
2. Verify `success=true` and all four source summaries are present
3. Check that `recommendations` lists cross-source items with `[source][risk_level]` prefixes
4. Verify `data_gaps` is empty when all sources succeed
5. Confirm `ops-weekly-report.md` and `ops-weekly-report.html` are generated in output_dir
6. Test with `include_raw=true` and verify `ops-weekly-raw.json` contains source payloads
7. Test with `oncall_summary="Test incident"` and verify on-call context appears in summary

---

## Best Practices

1. Always use `huawei_generate_ops_report` as the primary action; it aggregates all sources in one call
2. Choose report type matching the reporting cycle: `weekly` for weekly reviews, `monthly` for monthly summaries, `sla` for SLA tracking, `capacity` for capacity planning, `stability` for stability assessment
3. Use `output_dir` to persist reports for audit and stakeholder review
4. For traceability, use `include_raw=true` to preserve source payloads
5. If on-call context is available, pass it via `oncall_report_path` or `oncall_summary` to enrich the report
6. For high-risk findings, trace back to the relevant sub-skill for detailed remediation plans
7. Do NOT execute write actions (HPA apply, scale, node pool resize, workload mutation) unless the user explicitly authorizes remediation — hand off to `huawei-cloud-cce-auto-remediation-runner`

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/workflow.md` | Detailed execution process, scope validation, and data gap handling |
| `references/output-schema.md` | Complete JSON response schema for report output |

---

## Notes

- **Read-only by design** — this skill does NOT modify workloads, HPA, node pools, or cluster configuration
- **Remediation hand-off** — all mutation suggestions are handed off to `huawei-cloud-cce-auto-remediation-runner` with user authorization
- **Never expose or log AK/SK or environment variable values**
- **All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls**
- **Data gaps** — the report continues generation even when individual sources fail; gaps are clearly marked
- **On-call optional** — when on-call context is unavailable, the report still generates with a marked context gap

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Assuming report fails when one source fails | The report continues with degraded sources; data gaps are explicitly listed |
| Skipping on-call context entirely when unavailable | Mark as a context gap; the report still provides value from other sources |
| Executing remediation directly from report findings | All remediation requires explicit user authorization; hand off to `huawei-cloud-cce-auto-remediation-runner` |
| Not using `output_dir` for persistent reports | Always specify `output_dir` for audit traceability and stakeholder access |
| Treating recommendations as action items without risk context | Each recommendation includes `[source][risk_level]` prefix; prioritize by risk level |
| Ignoring `include_raw` for compliance requirements | Use `include_raw=true` when audit traceability of source data is required |
| Using wrong `report_type` for the reporting cycle | Match report type to cycle: weekly=168h, monthly=744h, sla/capacity/stability=168h by default |