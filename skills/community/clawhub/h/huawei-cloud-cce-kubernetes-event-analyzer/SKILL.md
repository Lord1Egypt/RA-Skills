---
id: huawei-cloud-cce-kubernetes-event-analyzer
name: huawei-cloud-cce-kubernetes-event-analyzer
description: Use this skill when the user wants to query and analyze Kubernetes events in Huawei Cloud CCE clusters. Trigger: user mentions Kubernetes events, "Kubernetes 事件", CCE events, "CCE 事件", event analysis, "事件分析", "FailedScheduling", "FailedMount", event query, "事件查询", cluster events, "集群事件"
tags: [cce, kubernetes, events, observability, analysis]
---

# Kubernetes Event Analyzer

## Overview

Analyze Kubernetes events in Huawei Cloud CCE clusters to find warning events, anomalies, and failure patterns. Queries events via K8s API or LTS log streams, applies client-side filtering, groups patterns, and hands off to diagnosis skills for remediation.

**Architecture**: MCP Tool → CCE K8s API / LTS Log Streams → Events → Client-side Filter & Group → Pattern Summary → Diagnosis Handoff

**Standard workflow**:
```
1. Identify region, cluster_id, and optional namespace from user query
2. Fetch events using huawei_get_cce_events (K8s API) or huawei_query_k8s_events_from_lts (LTS)
3. Apply client-side filters (type, reason, involved_object, time window)
4. Group and aggregate by reason, namespace, or pattern
5. Summarize top reasons, repeated patterns, and affected resources
6. Hand off to diagnosis skill if specific failures identified
```

**Related Skills** (handoff targets):
- Pod failures -> `huawei-cloud-cce-pod-failure-diagnoser`
- Workload rollout issues -> `huawei-cloud-cce-workload-failure-diagnoser`
- Node issues -> `huawei-cloud-cce-node-failure-diagnoser`
- Storage issues -> `huawei-cloud-cce-storage-failure-diagnoser`
- Service/Network issues -> `huawei-cloud-cce-network-failure-diagnoser`
- Action requested -> `huawei-cloud-cce-auto-remediation-runner`

## Prerequisites

### 1. Python Dependencies

- Python 3.8+ with `huaweicloudsdkcce`, `huaweicloudsdkcore`, `kubernetes` packages
- Run environment check before first use (see Verification section)

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - ✅ Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - ✅ Prefer IAM users over root account for cloud operations
  - ✅ Enable MFA for sensitive operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**⚠️ Important Security Notes**:

- Never commit credentials to version control
- Use IAM users with minimal required permissions
- Enable MFA for sensitive operations
- Rotate AK/SK regularly

### 3. IAM Permission Requirements

| API Action | Permission | Purpose |
|------------|-----------|---------|
| `cce:cluster:get` | Get cluster | View CCE cluster details |
| `cce:cluster:createCert` | Create certificate | Obtain kubeconfig for kubectl access |
| `cce:node:list` | List nodes | Query CCE cluster nodes |
| `lte:logStream:list` | List LTS log streams | Discover LTS log streams for event queries |
| `lte:logs:search` | Search LTS logs | Query K8s events from LTS log streams |

**Permission Failure Handling**:

1. When any command fails due to IAM permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console and grant authorization
3. Pause execution and wait for user confirmation that permissions have been granted

## Security Constraints

### Read-Only Skill

> **This skill is strictly read-only.** It only queries Kubernetes events and lists related resources. No modifications are made to the cluster.

- **No write operations**: Never modify, delete, or create any Kubernetes resources
- **Redact sensitive data**: Do not expose node names, pod names, or workload names that could identify production systems. Use redacted or fictional examples in summaries
- **Hand off remediation**: If event analysis reveals a clear remediation path, provide evidence and hand off to the appropriate diagnosis or remediation skill instead of executing recovery actions here
- **Time-bounded queries**: Keep event queries time-bounded. Prefer recent windows (1-24 hours) to avoid overwhelming results
- **Redirect action requests**: If the user asks to take action based on event findings, redirect to `huawei-cloud-cce-auto-remediation-runner` with the evidence summarized

## Tools

| Tool | Purpose | Required Parameters | Optional Parameters |
|------|---------|---------------------|---------------------|
| `huawei_get_cce_events` | Query CCE Kubernetes events via K8s API Server | `region`, `cluster_id` | `namespace`, `limit` |
| `huawei_query_k8s_events_from_lts` | Query K8s events from LTS log streams (Event→LTS LogConfig required) | `region`, `cluster_id`, `start_time`, `end_time` | `keywords` |

## Scenario Routing

| User Intent | Reference Document |
|---|---|
| Full event query workflow (5-step) | [references/workflow.md](references/workflow.md) |
| Event pattern recognition table | [references/workflow.md](references/workflow.md) |
| Time-window analysis guidance | [references/workflow.md](references/workflow.md) |
| Risk constraints & guardrails | [references/risk-rules.md](references/risk-rules.md) |
| Output schema (query & analysis) | [references/output-schema.md](references/output-schema.md) |

## Core Commands

### Step 1: Query Events via K8s API (huawei_get_cce_events)

Fetches raw Kubernetes events from the cluster API Server. All filtering beyond `namespace` and `limit` is done client-side after fetching.

```bash
# Query all events in a cluster
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id>

# Query events in a specific namespace
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  namespace=default

# Limit event count
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  limit=100
```

**Supported API filters**: `namespace`, `limit` (default 500)

**Unsupported filters (apply client-side)**: `event_type`, `reason`, `involved_object_kind`, `involved_object_name`, `hours`, `start_time`, `end_time`

### Step 2: Query Events via LTS (huawei_query_k8s_events_from_lts)

Queries K8s events collected to LTS via Event→LTS LogConfig. Requires a LogConfig with event collection enabled and pointing to LTS output.

```bash
# Query events from LTS in a time window
python3 scripts/huawei-cloud.py huawei_query_k8s_events_from_lts \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  start_time="2026-05-30 06:00:00" \
  end_time="2026-05-30 08:00:00"

# Query with keyword filter
python3 scripts/huawei-cloud.py huawei_query_k8s_events_from_lts \
  region=cn-north-4 \
  cluster_id=<cluster-id> \
  start_time="2026-05-30 00:00:00" \
  end_time="2026-05-30 23:59:59" \
  keywords=FailedScheduling
```

**LTS time format**: `YYYY-MM-DD HH:MM:SS`

**Fallback**: If no Event→LTS LogConfig is found with events enabled, returns an error. Use `huawei_get_cce_events` instead.

### Step 3: Apply Client-Side Filters

After fetching events, apply filters based on user needs:

- `type == "Warning"` — warning events only
- `reason` — specific patterns (FailedScheduling, ImagePullBackOff, FailedMount, etc.)
- `involved_object.kind` + `involved_object.name` — specific resources
- `namespace` — namespace-specific analysis
- `first_timestamp` / `last_timestamp` — time-window analysis

### Step 4: Group and Aggregate

- Group by `reason` to find top event patterns
- Group by `namespace` to find high-noise namespaces
- Flag events with `count > 1` as repeated patterns
- Calculate `warning_count` vs `normal_count` for quick health signal

### Step 5: Summarize and Hand Off

Summarize findings with counts, timestamps, and affected objects. If events point to specific failures, hand off to the appropriate diagnosis skill with evidence.

## Parameter Reference

### Common Parameters

| Parameter | Required/Optional | Description | Default |
|-----------|-------------------|-------------|---------|
| `region` | Required | Huawei Cloud region | `HUAWEI_REGION` |
| `cluster_id` | Required | CCE cluster ID | N/A |
| `namespace` | Optional | Kubernetes namespace filter | N/A (all namespaces) |
| `ak` | Optional | Override AK | `HUAWEI_AK` |
| `sk` | Optional | Override SK | `HUAWEI_SK` |
| `project_id` | Optional | Project ID | Auto from IAM |

### `huawei_get_cce_events` Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region | `HUAWEI_REGION` |
| `cluster_id` | Yes | CCE cluster ID | N/A |
| `namespace` | No | Kubernetes namespace filter | N/A (all namespaces) |
| `limit` | No | Maximum number of events to return | 500 |

### `huawei_query_k8s_events_from_lts` Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region | `HUAWEI_REGION` |
| `cluster_id` | Yes | CCE cluster ID | N/A |
| `start_time` | Yes | Query start time (YYYY-MM-DD HH:MM:SS) | N/A |
| `end_time` | Yes | Query end time (YYYY-MM-DD HH:MM:SS) | N/A |
| `keywords` | No | Keyword filter for LTS search | N/A |

## Event Pattern Quick Reference

| Pattern | Likely Cause | Handoff Target |
|---------|-------------|---------------|
| `ImagePullBackOff` repeated | Wrong image or pull secret missing | `huawei-cloud-cce-pod-failure-diagnoser` |
| `FailedScheduling` + `insufficient` | Resource pressure or node not ready | `huawei-cloud-cce-workload-failure-diagnoser` |
| `FailedMount` | Volume attach or PVC issue | `huawei-cloud-cce-storage-failure-diagnoser` |
| `Evicted` pods | Budget disruption or node pressure | `huawei-cloud-cce-pod-failure-diagnoser` |
| `NodeNotReady` | Node agent or network issue | `huawei-cloud-cce-node-failure-diagnoser` |
| `Unhealthy` + Readiness probe | Application issue or startup failure | `huawei-cloud-cce-pod-failure-diagnoser` |
| `FailedCreatePodSandBox` | CNI or network issue | `huawei-cloud-cce-network-failure-diagnoser` |
| `OOMKilled` | Memory limit exceeded | `huawei-cloud-cce-pod-failure-diagnoser` |

## Output Format

### From huawei_get_cce_events (K8s API)

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID |
| `namespace` | Kubernetes namespace filter (if applied) |
| `total_fetched` | Number of events returned by the API |
| `events` | Raw event list (apply filters client-side) |
| `warning_count` | Number of Warning events (calculated) |
| `top_reasons` | Top event reasons with counts (calculated) |
| `repeated_patterns` | Events with count > 1 grouped by reason |
| `namespace_breakdown` | Event counts by namespace |
| `next_steps` | Suggested follow-up query or diagnosis skill |

### From huawei_query_k8s_events_from_lts (LTS)

| Field | Description |
|------|-------------|
| `region` | Huawei Cloud region |
| `cluster_id` | CCE cluster ID |
| `log_group_id` | LTS log group ID |
| `log_stream_id` | LTS log stream ID |
| `keywords` | Keywords used for filtering |
| `event_count` | Number of events returned |
| `events` | Parsed event list with normalized structure |
| `time_range` | Start/end time of the query |
| `log_config` | LogConfig info (name, events enabled, etc.) |

## Verification

1. Run environment check script
2. Query CCE events with huawei_get_cce_events
3. Verify event filtering and pattern grouping
4. Confirm handoff to diagnosis skills works correctly

## Best Practices

1. **Start with K8s API** — use `huawei_get_cce_events` for quick queries; fall back to LTS only when time-range precision is needed
2. **Filter Warning first** — Warning events are the primary signal; filter `type == "Warning"` before deep analysis
3. **Group by reason** — event reason grouping reveals systemic issues faster than per-event analysis
4. **Time-bound queries** — prefer recent windows (1-24 hours) to avoid overwhelming results
5. **Hand off, don't remediate** — this skill is read-only; always hand off to diagnosis skills with evidence
6. **Redact sensitive names** — use generic labels in summaries; do not expose production pod/node/workload names

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Missing `cluster_id` | Action fails immediately | Provide `cluster_id` from `huawei_get_cce_clusters` |
| No Event→LTS LogConfig configured | LTS query returns error | Use `huawei_get_cce_events` (K8s API) instead |
| Unbounded time query | Overwhelming results, slow response | Always provide `start_time`/`end_time` or limit scope to 1-24 hours |
| LTS time format mismatch | LTS query fails or returns no results | Use exact format `YYYY-MM-DD HH:MM:SS` for `start_time` and `end_time` |
| Large namespace scan with no filter | Too many events, hard to analyze | Narrow with `namespace` or client-side filters (`type`, `reason`) |
| Permission denied on kubeconfig | Cannot access cluster | Verify `cce:cluster:createCert` IAM permission |
| LTS permission denied | Cannot query LTS log streams | Verify `lte:logStream:list` and `lte:logs:search` IAM permissions |
| Ignoring `count > 1` events | Missing systemic patterns | Always group by `reason` and flag repeated events first |

## Notes

- This skill does **not** modify, delete, or create any Kubernetes or LTS resources — all actions are **read-only**
- Event summaries must **redact** production pod/node/workload names; use generic labels in public outputs
- AK/SK must **never** be hardcoded — use environment variables only
- The Python dispatcher script (`scripts/huawei-cloud.py`) is the **only execution method** — do not use hcloud CLI or direct API calls for event queries
- For LTS queries, the cluster must have an **Event→LTS LogConfig** configured; otherwise fall back to K8s API
- Hand off remediation requests to `huawei-cloud-cce-auto-remediation-runner` with evidence summarized — this skill never executes recovery actions
- All event data is **point-in-time** — K8s API events have a retention limit; use LTS for historical analysis beyond the API retention window

## Reference Documents

| Document | Description |
|----------|-------------|
| [workflow.md](references/workflow.md) | Full event query workflow, pattern recognition, time-window analysis, aggregation guidance, LTS vs K8s API selection guide |
| [risk-rules.md](references/risk-rules.md) | Read-only constraints, data redaction rules, handoff policies, guardrails |
| [output-schema.md](references/output-schema.md) | Event query summary, analysis summary, and per-event detail schema |