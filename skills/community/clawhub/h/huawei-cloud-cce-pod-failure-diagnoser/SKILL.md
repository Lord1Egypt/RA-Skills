---
id: huawei-cloud-cce-pod-failure-diagnoser
name: huawei-cloud-cce-pod-failure-diagnoser
description: |
  Huawei Cloud CCE Pod failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose Pod CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending, Evicted failures, (2) analyze Pod restart storms, (3) check Pod logs and events, (4) view Pod metrics and resource usage.
  Trigger: user mentions "Pod failure", "Pod 故障", "CrashLoopBackOff", "ImagePullBackOff", "OOMKilled", "Pod Pending", "Pod Evicted", "Pod 重启", "容器异常", "Pod 诊断", "Pod crash", "Pod 无法启动", "Pod 状态异常"
tags: [cce, pod-diagnosis, kubernetes, fault-diagnosis]
---

# Huawei Cloud CCE Pod Failure Diagnoser

## Overview

This skill diagnoses single-resource Pod failures in Huawei Cloud CCE clusters, including CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending, Evicted, and frequent restart storms. It confirms scope, then builds an evidence chain through Kubernetes Pod status, container state, Events, previous/current logs, and optional metrics.

**Architecture**: `python3 scripts/huawei-cloud.py` dispatcher → Huawei Cloud Python SDK + Kubernetes client → Pod status, Events, logs, metrics

**Related Skills**:
- `huawei-cloud-cce-workload-failure-diagnoser` - Workload rollout, stuck rolling updates, unavailable replicas
- `huawei-cloud-cce-node-failure-diagnoser` - Node health, resource pressure, NPD events
- `huawei-cloud-cce-network-failure-diagnoser` - Network connectivity, DNS, ELB diagnosis
- `huawei-cloud-cce-storage-failure-diagnoser` - PVC/PV mount, storage provisioning failures
- `huawei-cloud-cce-root-cause-analyzer` - Cross-domain root cause analysis and reports
- `huawei-cloud-cce-auto-remediation-runner` - Remediation actions (scale, resize, drain, etc.)

**Capabilities**:
- One-shot Pod failure diagnosis with top causes (`huawei_pod_failure_diagnose`)
- Read Pod phase, reason, container state, last state, restart count, owner, node (`huawei_get_cce_pods`)
- Fetch Pod current and previous container logs (`huawei_get_pod_logs`)
- Query Kubernetes Events for a namespace or cluster (`huawei_get_cce_events`)
- View Pod CPU/memory metrics and TopN metrics (`huawei_get_cce_pod_metrics`, `huawei_get_cce_pod_metrics_topN`)
- Comprehensive workload diagnosis (`huawei_workload_diagnose`, `huawei_workload_diagnose_by_alarm`)
- Generate structured diagnosis report (`huawei_generate_diagnosis_report`)

**Typical Use Cases**:

- "My Pod is in CrashLoopBackOff, find the root cause"
- "Pod keeps restarting, check previous logs"
- "Pod stuck in Pending, why can't it schedule?"
- "ImagePullBackOff error, check events and registry access"
- "Pod was OOMKilled, show memory metrics"
- "Pod was Evicted, check node pressure"
- "List all abnormal Pods in a namespace"
- "Show Pod resource usage for the last hour"

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

| API Action                        | Permission          | Purpose                                    |
| --------------------------------- | ------------------- | ------------------------------------------ |
| `cce:cluster:get`                 | Get cluster         | View CCE cluster details                   |
| `cce:cluster:createCert`          | Create certificate  | Obtain kubeconfig for kubectl access       |
| `cce:node:list`                   | List nodes          | Query CCE cluster nodes                    |
| `aom:instance:list`               | List AOM instances  | Discover AOM Prom instance for metrics     |
| `aom:metricsData:get`             | Get metrics data    | Query Pod/node CPU/memory metrics          |

**Permission Failure Handling**:

1. When any command fails due to IAM permission errors, display the required permission list
2. Guide the user to create a custom policy in the IAM console and grant authorization
3. Pause execution and wait for user confirmation that permissions have been granted

## Core Commands/Tools

All commands use the Python dispatcher script: `python3 scripts/huawei-cloud.py <action> <key=value>...`

### 1. Primary Diagnosis — `huawei_pod_failure_diagnose`

One-shot action that fetches Pod status, Events, logs, and optional metrics, then outputs top causes.

```bash
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster-id> namespace=default \
  pod_name=my-app-xxx workload_name=my-app \
  include_logs=true include_metrics=false \
  tail_lines=80 hours=1 max_pods=20 event_limit=500
```

**Parameters**:
- `pod_name` or `workload_name` or `labels` — at least one targeting parameter recommended
- `include_logs=true` — fetch previous and current container logs (default: true)
- `include_metrics=true` — fetch Pod CPU/memory metrics (default: false)
- `tail_lines` — number of log tail lines (default: 80)
- `hours` — metrics lookback window in hours (default: 1)
- `max_pods` — max Pods to analyze per workload (default: 20)

### 2. Read-Only Evidence — Raw Data Retrieval

```bash
# List Pods with phase, reason, container state, restart count, node
python3 scripts/huawei-cloud.py huawei_get_cce_pods \
  region=cn-north-4 cluster_id=<cluster-id> namespace=default labels=app=my-app

# Fetch Pod logs (previous=true for CrashLoopBackOff/OOMKilled)
python3 scripts/huawei-cloud.py huawei_get_pod_logs \
  region=cn-north-4 cluster_id=<cluster-id> pod_name=my-app-xxx \
  namespace=default container=app previous=true tail_lines=100

# Query Kubernetes Events
python3 scripts/huawei-cloud.py huawei_get_cce_events \
  region=cn-north-4 cluster_id=<cluster-id> namespace=default limit=500

# View Pod CPU/memory metrics
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics \
  region=cn-north-4 cluster_id=<cluster-id> pod_name=my-app-xxx \
  namespace=default hours=1

# TopN Pod metrics by CPU or memory
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN \
  region=cn-north-4 cluster_id=<cluster-id> namespace=default \
  top_n=10 hours=1
```

### 3. Comprehensive Diagnosis — Workload-Level

```bash
# Workload-level diagnosis (Pods + rollout + metrics)
python3 scripts/huawei-cloud.py huawei_workload_diagnose \
  region=cn-north-4 cluster_id=<cluster-id> \
  workload_name=my-app namespace=default hours=6

# Workload diagnosis triggered by alarm
python3 scripts/huawei-cloud.py huawei_workload_diagnose_by_alarm \
  region=cn-north-4 cluster_id=<cluster-id> \
  alarm_info=<alarm-json> hours=6

# Generate structured diagnosis report
python3 scripts/huawei-cloud.py huawei_generate_diagnosis_report \
  region=cn-north-4 cluster_id=<cluster-id>
```

## Parameter Reference

### Common Parameters

| Parameter      | Required/Optional | Description          | Default         |
| -------------- | ----------------- | -------------------- | --------------- |
| `region`       | Required          | Huawei Cloud region  | `HUAWEI_REGION` |
| `cluster_id`   | Required          | CCE cluster ID       | N/A             |
| `namespace`    | Recommended       | Kubernetes namespace | `default`       |
| `ak`           | Optional          | Override AK          | `HUAWEI_AK`     |
| `sk`           | Optional          | Override SK          | `HUAWEI_SK`     |
| `project_id`   | Optional          | Project ID           | Auto from IAM   |

### `huawei_pod_failure_diagnose` Parameters

| Parameter         | Required | Description                | Default  |
| ----------------- | -------- | -------------------------- | -------- |
| `pod_name`        | No*      | Target Pod name            | N/A      |
| `workload_name`   | No*      | Target workload name       | N/A      |
| `labels`          | No*      | Label selector (e.g. app=web) | N/A   |
| `include_logs`    | No       | Fetch previous+current logs | `true`  |
| `include_metrics` | No       | Fetch Pod metrics          | `false`  |
| `tail_lines`      | No       | Log tail line count        | 80       |
| `hours`           | No       | Metrics lookback hours     | 1        |
| `max_pods`        | No       | Max Pods per workload      | 20       |
| `event_limit`     | No       | Max Events fetched         | 500      |

*At least one of `pod_name`, `workload_name`, or `labels` should be provided for targeted diagnosis.

### `huawei_get_pod_logs` Parameters

| Parameter    | Required | Description                | Default  |
| ------------ | -------- | -------------------------- | -------- |
| `pod_name`   | Yes      | Pod name                   | N/A      |
| `namespace`  | No       | Namespace                  | `default`|
| `container`  | No       | Container name             | First    |
| `previous`   | No       | Previous (crashed) logs    | `false`  |
| `tail_lines` | No       | Number of tail lines       | 100      |

## Output Format

See [Output Schema](references/output-schema.md) for the complete JSON response structure.

**Key output fields**:
- `success` — boolean, true if diagnosis completed
- `summary.diagnosis_status` — `abnormal`, `no_known_failure_detected`, or `no_matching_abnormal_pods`
- `pods[].issues[].type` — failure type: CrashLoopBackOff, ImagePullBackOff, OOMKilled, PendingScheduling, PendingStorage, Evicted, FrequentRestart, PodNotReady
- `pods[].issues[].confidence` — confidence score (0-1)
- `top_causes` — ranked top causes with evidence and recommendations
- `recommended_actions` — read-only next checks; mutation actions deferred to `huawei-cloud-cce-auto-remediation-runner`

## Verification

1. Run `python3 scripts/huawei-cloud.py huawei_get_cce_pods region=cn-north-4 cluster_id=<cluster-id>` to verify cluster connectivity
2. Run `python3 scripts/huawei-cloud.py huawei_get_cce_events region=cn-north-4 cluster_id=<cluster-id> limit=10` to verify Event query works
3. Run `python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose region=cn-north-4 cluster_id=<cluster-id> namespace=default` on a healthy namespace and confirm `diagnosis_status=no_known_failure_detected`

## Best Practices

1. **Use `huawei_pod_failure_diagnose` as first choice** — it aggregates Pod status, Events, logs, and metrics in one call
2. **Check previous logs for CrashLoopBackOff/OOMKilled** — set `previous=true` to see the last crashed container output
3. **Prioritize Events for ImagePullBackOff** — container logs typically don't exist for image pull failures; read Events first
4. **Escalate to related skills** — Pending scheduling → node/autoscaling skills; Pending storage → storage diagnosis; workload-level → huawei-cloud-cce-workload-failure-diagnoser
5. **Scope with namespace** — always provide `namespace` to reduce result noise
6. **Sanitize output** — the dispatcher automatically sanitizes logs; never copy raw passwords, tokens, or AK/SK from log excerpts

## Reference Documents

| Document                                | Description                              |
| --------------------------------------- | ---------------------------------------- |
| [Workflow](references/workflow.md)      | Failure classification and evidence order |
| [Risk Rules](references/risk-rules.md)  | Safety constraints for diagnostic actions |
| [Output Schema](references/output-schema.md) | JSON response format for pod_failure_diagnose |

## Notes

- This skill does **not** scale, delete, or restart workloads or nodes — mutation actions must be handed off to `huawei-cloud-cce-auto-remediation-runner`
- All diagnostic actions are **read-only** — no side effects on cluster state
- Log excerpts are **sanitized** — suspected passwords, tokens, AK/SK, and Authorization headers are redacted in output
- AK/SK must **never** be hardcoded — use environment variables only
- The Python dispatcher script (`scripts/huawei-cloud.py`) is the **only execution method** — do not use hcloud CLI or direct API calls for Pod diagnosis
- For Pending Pods with FailedScheduling, consider switching to `huawei-cloud-cce-node-failure-diagnoser` or `huawei-cloud-cce-autoscaling-diagnoser`

## Common Pitfalls

| Pitfall                                    | Symptom                               | Quick Fix                                    |
| ------------------------------------------ | ------------------------------------- | -------------------------------------------- |
| Missing `cluster_id`                       | Action fails immediately              | Provide `cluster_id` from `huawei_get_cce_clusters` |
| Pod name not found                         | `no_matching_abnormal_pods` result    | Use `workload_name` or `labels` instead      |
| ImagePullBackOff logs requested            | Empty or error log response           | Read Events first; ImagePullBackOff has no container logs |
| Previous logs not checked                  | Missing crash root cause              | Set `previous=true` for CrashLoopBackOff/OOMKilled |
| Large namespace scan                       | Slow response, too many Pods          | Narrow with `workload_name`, `labels`, or `pod_name` |
| Permission denied on kubeconfig            | Cannot access cluster                 | Verify `cce:cluster:createCert` IAM permission |
| Metrics not available                      | `include_metrics=true` returns empty  | Ensure AOM Prom instance exists; check `aom:instance:list` |