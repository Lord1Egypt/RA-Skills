---
id: huawei-cloud-cce-observability-context-builder
name: huawei-cloud-cce-observability-context-builder
description: Use this skill when the user wants to collect AOM alarms, metrics, LTS logs, Pod logs, or Kubernetes events and build a comprehensive observability context package before handing off to diagnosis skills. Trigger: user mentions observability context, "可观测性上下文", context builder, "上下文构建", metric+log+event, "指标+日志+事件", comprehensive observability, "综合可观测", diagnosis context, "诊断上下文"
tags: [cce, observability, context, alarms]
---

# Huawei Cloud CCE Observability Context Builder

> **⚠️ Execution Method (Must Read): This skill executes actions via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Tools section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill consolidates scattered fault signals into a structured, diagnosable context package. It first collects the time window, cluster, namespace, workload, Pod, node, and alarm scope, then gathers evidence by type (alarms, events, metrics, logs), merges signals along a timeline, and identifies gaps and the appropriate next diagnostic skill for hand-off. **This skill is strictly read-only — it never executes remediation actions.**

**Architecture**: `python3 scripts/huawei-cloud.py` dispatcher → Huawei Cloud Python SDK + AOM/LTS API → alarms, metrics, logs, events aggregation

**Related Skills**:
- `huawei-cloud-cce-pod-failure-diagnoser` - Pod CrashLoopBackOff, ImagePullBackOff, OOMKilled diagnosis
- `huawei-cloud-cce-node-failure-diagnoser` - Node health, resource pressure, NPD events diagnosis
- `huawei-cloud-cce-network-failure-diagnoser` - Network connectivity, DNS, ELB diagnosis
- `huawei-cloud-cce-storage-failure-diagnoser` - PVC/PV mount, storage provisioning diagnosis
- `huawei-cloud-cce-root-cause-analyzer` - Cross-domain root cause analysis and reports
- `huawei-cloud-cce-auto-remediation-runner` - Remediation actions (scale, drain, rollback, etc.)
- `huawei-cloud-cce-alarm-correlation-engine` - Alarm deduplication and correlation
- `huawei-cloud-cce-metric-analyzer` - Deep metric trend analysis
- `huawei-cloud-cce-log-analyzer` - Deep log pattern analysis

**Capabilities**:
- Collect active and history AOM alarms, deduplicate and group by severity (`huawei_list_aom_alarms`, `huawei_analyze_aom_alarms`)
- Retrieve Kubernetes Events grouped by object and reason (`huawei_get_cce_events`)
- Query Pod and Node TopN metrics for resource peaks and anomalies (`huawei_get_cce_pod_metrics_topN`, `huawei_get_cce_node_metrics_topN`)
- Query AOM and LTS logs for deep log evidence (`huawei_query_aom_logs`, `huawei_get_recent_logs`)
- Fetch Pod-side container logs (`huawei_get_pod_logs`)
- Get AOM metrics and instance list (`huawei_get_aom_metrics`, `huawei_list_aom_instances`)
- Generate monitor dashboards from collected data (`huawei_generate_monitor_dashboard`)
- Merge signals along a timeline, mark gaps, and recommend the next diagnostic skill

**Typical Use Cases**:

- "Collect all observability data for cluster xyz in the last hour"
- "Build a context package for a Pod crash incident"
- "Gather alarms, events, and metrics before diagnosis"
- "I see multiple alarms, consolidate them into a diagnosis context"
- "Show me the full observability picture: alarms + metrics + logs + events"
- "What's happening in namespace prod over the last 30 minutes?"

## Prerequisites

### 1. Python Dependencies

- Python 3.8+ with `huaweicloudsdkcce`, `huaweicloudsdkcore`, `huaweicloudsdkaom`, `huaweicloudsdklts` packages
- Run environment check before first use (see Verification section)

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - Never expose AK/SK values in code, conversation, or commands
  - Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - Prefer IAM users over root account for cloud operations
  - Enable MFA for sensitive operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**Important Security Notes**:

- Never commit credentials to version control
- Use IAM users with minimal required permissions
- Rotate AK/SK regularly

### 3. IAM Permission Requirements

| API Action                  | Permission         | Purpose                               |
| --------------------------- | ------------------ | ------------------------------------- |
| `cce:cluster:get`           | Get cluster        | View CCE cluster details              |
| `cce:cluster:createCert`    | Create certificate | Obtain kubeconfig for kubectl access  |
| `aom:alarm:list`            | List alarms        | Query AOM active/history alarms      |
| `aom:alarm:analyze`         | Analyze alarms     | Deduplicate and group alarms          |
| `aom:metricsData:get`       | Get metrics data   | Query Pod/node CPU/memory metrics     |
| `aom:instance:list`         | List AOM instances | Discover AOM Prom instance            |
| `aom:logData:get`           | Get log data       | Query AOM/LTS log data               |
| `lts:log:list`              | List LTS logs      | Query LTS log streams                 |
| `cce:event:list`            | List events        | Query Kubernetes Events               |

**Permission Failure Handling**:

1. When any command fails due to IAM permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console and grant authorization
3. Pause execution and wait for user confirmation that permissions have been granted

## Core Tools

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`.

### Alarm Collection

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_list_aom_alarms` | region, cluster_id | Collect active + history AOM alarms for the cluster |
| `huawei_analyze_aom_alarms` | region, cluster_id | Deduplicate alarms and group by severity level |

### Event and Metric Collection

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_get_cce_events` | region, cluster_id | Retrieve Kubernetes Events grouped by object and reason |
| `huawei_get_cce_pod_metrics_topN` | region, cluster_id, namespace | TopN Pod metrics (CPU/memory) for anomaly detection |
| `huawei_get_cce_node_metrics_topN` | region, cluster_id | TopN Node metrics for resource pressure detection |
| `huawei_get_aom_metrics` | region, cluster_id, namespace | Query AOM metrics for specific resources |
| `huawei_list_aom_instances` | region | Discover AOM Prom instance for metrics queries |

### Log Collection

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_query_aom_logs` | region, cluster_id, namespace | Query AOM structured log data |
| `huawei_get_recent_logs` | region, cluster_id, namespace | Get recent log entries (LTS) |
| `huawei_get_pod_logs` | region, cluster_id, pod_name, namespace | Fetch Pod container logs (previous or current) |

### Visualization

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_generate_monitor_dashboard` | region, cluster_id | Generate monitoring dashboard from collected data |

## Parameter Reference

### Common Parameters

| Parameter    | Required | Description          | Default         |
| ------------ | -------- | -------------------- | --------------- |
| `region`     | Yes      | Huawei Cloud region  | `HUAWEI_REGION` |
| `cluster_id` | Yes      | CCE cluster ID       | N/A             |
| `namespace`  | No       | Kubernetes namespace | N/A             |
| `ak`         | Optional | Override AK          | `HUAWEI_AK`     |
| `sk`         | Optional | Override SK          | `HUAWEI_SK`     |
| `project_id` | Optional | Project ID           | Auto from IAM   |

### Alarm Collection Parameters

| Parameter    | Required | Description                    | Default  |
| ------------ | -------- | ------------------------------ | -------- |
| `alarm_id`   | No       | Specific alarm ID to query     | N/A      |
| `alarm_level`| No       | Alarm severity filter          | All      |
| `hours`      | No       | History lookback window (hours)| 1        |

### Log Collection Parameters

| Parameter    | Required | Description                     | Default  |
| ------------ | -------- | ------------------------------- | -------- |
| `pod_name`   | Yes*     | Pod name (for `huawei_get_pod_logs`) | N/A |
| `container`  | No       | Container name                  | First    |
| `previous`   | No       | Fetch previous (crashed) logs   | `false`  |
| `tail_lines` | No       | Number of log tail lines        | 100      |

### Metric Collection Parameters

| Parameter    | Required | Description                     | Default  |
| ------------ | -------- | ------------------------------- | -------- |
| `top_n`      | No       | Number of top results           | 10       |
| `hours`      | No       | Metrics lookback window (hours) | 1        |

*Required for specific actions as noted.

## Workflow

1. **Record scope**: Capture fault time, `region`, `cluster_id`, `namespace`, `workload`, `pod`, `node`, and `alarm_id` provided by the user
2. **Set time window**: If time is unclear, default to the last 1 hour and note this assumption in the output
3. **Collect alarms**: Call `huawei_list_aom_alarms` to collect active + history alarms, then use `huawei_analyze_aom_alarms` for deduplication and severity grouping
4. **Collect events**: Call `huawei_get_cce_events` to retrieve Kubernetes Events grouped by involved object and reason
5. **Collect metrics**: Call Pod/Node TopN metrics tools to find resource peaks, abnormal nodes, and abnormal Pods
6. **Collect logs**: When log evidence is needed, prefer `huawei_query_aom_logs`, then supplement with Pod-side logs from `huawei_get_recent_logs` or `huawei_get_pod_logs`
7. **Merge and output**: Merge signals along a timeline, output the anomaly summary, missing information (gaps), and recommended diagnostic skill for hand-off

For the complete evidence-gathering workflow, see `references/workflow.md`.

## Output Format

See `references/output-schema.md` for the complete JSON response structure.

**Context Package Output**:

```json
{
  "summary": "one paragraph context summary",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "optional",
    "namespace": "optional",
    "workload": "optional",
    "time_window": "optional"
  },
  "signals": {
    "alarms": [],
    "events": [],
    "metrics": [],
    "logs": []
  },
  "timeline": [],
  "gaps": [],
  "next_skill": "huawei-cloud-cce-pod-failure-diagnoser | huawei-cloud-cce-node-failure-diagnoser | huawei-cloud-cce-network-failure-diagnoser | huawei-cloud-cce-root-cause-analyzer"
}
```

**Key output fields**:
- `summary` — one paragraph summarizing the collected observability context
- `scope` — region, cluster, namespace, workload, and time window
- `signals` — collected evidence grouped by type (alarms, events, metrics, logs)
- `timeline` — merged signal timeline showing event chronology
- `gaps` — missing data that could improve diagnosis
- `next_skill` — recommended diagnostic skill for hand-off based on signal analysis

## Risk Rules

This skill is **strictly read-only observability** — no mutations allowed.

- Allow automatic R1 read-only queries: alarms, metrics, logs, events, inventory, read-only report generation
- Prohibit any action requiring `confirm=true` — no mutations allowed
- Never persist AK/SK, tokens, certificates, or kubeconfig
- Log output must be sanitized. When suspected secrets are found, describe the hit location only — never copy the original text
- Charts and reports must only be generated from authorized query results

For complete risk classification, see `references/risk-rules.md`.

## Verification

1. Run `python3 scripts/huawei-cloud.py huawei_list_aom_alarms region=cn-north-4 cluster_id=<cluster-id>` to verify alarm query connectivity
2. Run `python3 scripts/huawei-cloud.py huawei_get_cce_events region=cn-north-4 cluster_id=<cluster-id> limit=10` to verify Event query works
3. Run `python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN region=cn-north-4 cluster_id=<cluster-id> namespace=default top_n=5` to verify metrics TopN
4. Run a full context build on a healthy namespace and confirm the output contains valid `scope`, `signals`, `timeline`, `gaps`, and `next_skill` fields
5. Verify that no mutation actions are suggested in the output — all actions should be read-only or hand-offs to diagnosis skills

## Best Practices

1. **Always start with alarms**: Check active + history alarms first using `huawei_list_aom_alarms` and `huawei_analyze_aom_alarms` — alarms provide the most direct fault signals
2. **Define scope early**: Record region, cluster_id, namespace, workload, pod, node, and time window before collecting any data. If the time window is unclear, default to the last 1 hour and note the assumption
3. **Use TopN for quick anomaly detection**: `huawei_get_cce_pod_metrics_topN` and `huawei_get_cce_node_metrics_topN` efficiently highlight resource peaks without scanning all resources
4. **Prefer AOM logs first, then supplement with Pod logs**: `huawei_query_aom_logs` provides structured log data; use `huawei_get_pod_logs` or `huawei_get_recent_logs` for Pod-side container log details
5. **Merge signals along a timeline**: Chronological merging of alarms, events, metrics, and logs reveals causal chains that individual data types cannot
6. **Mark gaps explicitly**: Always identify missing data in the `gaps` field — this guides the next diagnostic skill on what additional evidence to collect
7. **Never suggest mutation actions**: This skill is read-only. For scaling, deletion, restart, drain, or vulnerability state changes, hand off to `huawei-cloud-cce-auto-remediation-runner`
8. **Recommend the correct next skill**: Based on signal analysis, recommend the most specific diagnoser — Pod failures → `huawei-cloud-cce-pod-failure-diagnoser`, node issues → `huawei-cloud-cce-node-failure-diagnoser`, network → `huawei-cloud-cce-network-failure-diagnoser`, cross-domain → `huawei-cloud-cce-root-cause-analyzer`

## Reference Documents

| Document                                | Description                                    |
| --------------------------------------- | ---------------------------------------------- |
| [Workflow](references/workflow.md)      | Evidence-gathering workflow and step sequence   |
| [Risk Rules](references/risk-rules.md)  | Safety constraints and risk classification     |
| [Output Schema](references/output-schema.md) | JSON response format for context package |

## Notes

1. This skill is **strictly read-only** — it never executes remediation actions. For mutation actions, hand off to `huawei-cloud-cce-auto-remediation-runner`
2. All actions are R1 (read-only) — no `confirm=true` is ever needed
3. Log excerpts are **sanitized** — suspected passwords, tokens, AK/SK, and Authorization headers are redacted in output
4. AK/SK must **never** be hardcoded — use environment variables only
5. The Python dispatcher script (`scripts/huawei-cloud.py`) is the **only execution method** — do not use hcloud CLI or direct API calls
6. The `next_skill` field in the output uses `huawei-cloud-cce-*` naming for cross-skill hand-off
7. When alarm correlation is needed before context building, consider using `huawei-cloud-cce-alarm-correlation-engine`

## Common Pitfalls

| Pitfall                                    | Symptom                                  | Quick Fix                                        |
| ------------------------------------------ | ---------------------------------------- | ------------------------------------------------ |
| Missing `cluster_id`                       | All actions fail immediately             | Provide `cluster_id` from cluster list            |
| No time window specified                   | Broad, noisy results                     | Default to last 1 hour; note assumption in output |
| Skipping alarm collection                  | Missing critical fault signals           | Always start with `huawei_list_aom_alarms`        |
| Not merging signals on timeline            | Isolated data points, no causal chain    | Chronologically merge alarms, events, metrics     |
| Suggesting mutation actions                | Unsafe recommendations                   | All mutations → `huawei-cloud-cce-auto-remediation-runner` |
| Not marking data gaps                      | Diagnosis skill lacks direction           | Always populate the `gaps` field                  |
| Querying all namespaces                    | Slow response, too many results          | Scope with `namespace` and `workload`             |
| AOM Prom instance not found                | Metrics queries return empty             | Verify with `huawei_list_aom_instances` first     |