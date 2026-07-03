---
id: huawei-cloud-cce-workload-failure-diagnoser
name: huawei-cloud-cce-workload-failure-diagnoser
description: |
  Huawei Cloud CCE workload failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose Deployment/StatefulSet/DaemonSet rollout failures, (2) analyze workload replica shortages and update rollback issues, (3) diagnose probe-related readiness failures (startup, liveness, readiness), (4) identify ReplicaSet creation blocked by quota, admission, or webhook rejection, (5) detect control-plane-not-observed issues (observedGeneration lag), (6) check workload status, events and metrics comprehensively.
  Trigger: user mentions "workload failure", "工作负载故障", "Deployment rollback", "Deployment 回滚", "rollout stuck", "发布失败", "replica unavailable", "副本不可用", "workload diagnosis", "工作负载诊断", "workload unavailable", "负载异常", "Service unreachable", "Service 不通", "probe failure", "探针失败", "ReplicaSet blocked", "ReplicaSet 阻塞", "observedGeneration lag", "控制面未观测"
tags: [cce, workload, diagnosis, rollout]
---

# Huawei Cloud CCE Workload Failure Diagnoser

> **⚠️ Execution Method (Must Read): This skill executes diagnosis via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Commands section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill diagnoses CCE workload rollout failures, replica availability issues, and probe-related readiness failures for Deployment, StatefulSet, and DaemonSet workloads. It builds evidence from controller state, version ownership, and event trees, then drills down into abnormal Pods using Pod diagnosis logic.

**Architecture**: Python SDK dispatcher (`scripts/huawei-cloud.py`) → Huawei Cloud CCE API / Kubernetes API → Workload + ReplicaSet + Pod + Event data → Rollout funnel analysis → Top causes ranking → Handoff recommendations

**Related Skills**:
- `huawei-cloud-cce-pod-failure-diagnoser` - Pod-level failure diagnosis (CrashLoop, ImagePull, OOM, Pending, etc.) for drill-down from workload diagnosis
- `huawei-cloud-cce-node-failure-diagnoser` - Node-level failure diagnosis (NotReady, DiskPressure, MemoryPressure, etc.) for scheduling/node pressure handoff
- `huawei-cloud-cce-root-cause-analyzer` - Multi-domain root cause analysis converging workload, alarm, change, and dependency evidence
- `huawei-cloud-cce-auto-remediation-runner` - Remediation execution (rollback, scale, resize, cordon, drain, reboot) with preview-confirm-verify workflow
- `huawei-cloud-cce-alarm-correlation-engine` - AOM alarm correlation, deduplication, and severity grouping for alarm-related evidence
- `huawei-cloud-cce-cce-workload-manager` - CCE workload lifecycle management (create, query, scale, update, delete)

**Capabilities**:
- Diagnose Deployment/StatefulSet/DaemonSet rollout failures (rollout stuck, rollback issues)
- Analyze workload replica shortages (unavailable replicas, updated replicas below expected)
- Diagnose probe failures (startup, liveness, readiness probe failures causing Pod not Ready)
- Identify ReplicaSet creation blocked by quota, admission, or webhook rejection
- Detect control-plane-not-observed issues (observedGeneration lagging behind generation)
- Collect workload rollout context (Workload, ReplicaSet, Pod, and UID-filtered Events)
- Drill down into Pod-level failures for abnormal Pods
- Cross-domain handoff to node, network, storage, and root-cause skills

**Typical Use Cases**:

- "My Deployment rollout is stuck, diagnose the failure"
- "Replicas are unavailable, find the root cause"
- "Pods are Running but not Ready, check probe failures"
- "New ReplicaSet has zero replicas, check quota or admission blocking"
- "Deployment observedGeneration is lagging, check control plane pressure"
- "Collect workload rollout context for manual analysis"
- "Drill down into Pod-level failures from workload diagnosis"
- "Check PVC/PV for storage-related workload issues"
- "Hand off to node or network diagnosis for cross-domain failures"

## Prerequisites

### 1. Python Requirements (MANDATORY)

- Python >= 3.6 installed
- Run the environment check script before any diagnosis action

**Environment Check**:

- Linux / macOS: `skill action=exec: bash skill://scripts/check_env.sh`
- Windows: `skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1`

> Windows Note: Do not use `&&` to chain commands (PowerShell 5.x does not support it). Use semicolons if you need to change directories first.

The script will check in sequence: Python >= 3.6 → install dependencies → validate SDK → validate credentials → validate service availability.
If the environment check fails, fix the issues before continuing with other actions.

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HW_ACCESS_KEY` or `echo $HW_SECRET_KEY` to check credentials
  - ✅ Use environment variables: `HW_ACCESS_KEY`, `HW_SECRET_KEY`, `HW_REGION_NAME`
  - ✅ Prefer IAM users over root account for cloud operations
  - ✅ Enable MFA for sensitive operations
  - ✅ Never persist credentials (AK/SK/Token/Certificate) to the filesystem
  - ✅ All temporary certificate files must be deleted immediately after use

**Configuration Method** (Environment Variables Only):

```bash
export HW_ACCESS_KEY=<your-ak>
export HW_SECRET_KEY=<your-sk>
export HW_REGION_NAME=cn-north-4
export HW_PROJECT_ID=<your-project-id>
```

**Optional for temporary AK/SK**:
```bash
export HW_SECURITY_TOKEN=<your-security-token>
```

**⚠️ Important Security Notes**:

- AK/SK exist only within the current request call stack; released after use
- Only non-sensitive project IDs are cached in process memory (never written to disk)
- Never commit credentials to version control
- Use IAM users with minimal required permissions
- Rotate AK/SK regularly
- Do not output the values of environment variables

### 3. IAM Permission Requirements

| API Action                        | Permission          | Purpose                                    |
| --------------------------------- | ------------------- | ------------------------------------------ |
| `cce:cluster:get`                 | Get cluster         | Obtain CCE cluster details and kubeconfig  |
| `cce:cluster:createCert`          | Create certificate  | Obtain CCE cluster kubeconfig for API access |
| `cce:node:list`                   | List nodes          | Query cluster node information             |
| `cce:workload:get`                | Get workload        | Read Deployment/StatefulSet/DaemonSet status |
| `cce:pod:list`                    | List pods           | Query Pod status and container state       |
| `cce:event:list`                  | List events         | Query Kubernetes Events for diagnosis      |
| `aom:metric:get`                  | Get metrics         | Query Pod/Node CPU/memory metrics          |

**Permission Failure Handling**:

1. When any action fails due to IAM permission errors, verify the permissions listed above
2. Guide the user to create a custom policy in the IAM console for Huawei Cloud permissions
3. Pause execution and wait for user confirmation that permissions have been granted

## Core Commands

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`:

```bash
python3 scripts/huawei-cloud.py --action <action_name> --params '<json_params>'
```

### 1. Primary Diagnosis

See [Workflow](references/workflow.md) for detailed evidence collection and diagnosis flow.

```bash
# Diagnose Deployment rollout failure
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_workload_rollout_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"Deployment","name":"api"}'

# Diagnose StatefulSet rollout failure
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_workload_rollout_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"StatefulSet","name":"my-db"}'

# Diagnose DaemonSet rollout failure
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_workload_rollout_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"DaemonSet","name":"log-agent"}'
```

### 2. Context Collection (Evidence Only)

```bash
# Collect raw workload rollout context without diagnosis ranking
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_workload_rollout_context --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"Deployment","name":"api"}'
```

### 3. Pod-Level Drill-Down

```bash
# Diagnose Pod-level failures (CrashLoop, ImagePull, OOM, Pending, etc.)
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_pod_failure_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# List Pods in the cluster
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_pods --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# Retrieve container logs for a specific Pod
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_pod_logs --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","pod_name":"<pod-name>"}'
```

### 4. Supporting Evidence

```bash
# List Kubernetes Events in the cluster
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_events --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# Get CPU/memory metrics for a specific Pod
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_pod_metrics --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","pod_name":"<pod-name>"}'

# Get top-N Pod metrics by resource usage
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_pod_metrics_topN --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'
```

### 5. Cross-Domain Drill-Down

```bash
# List PVCs for storage-related issues
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_pvcs --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# List PVs for storage-related issues
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_cce_pvs --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# Diagnose node-level failures (scheduling, pressure)
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_node_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'

# Diagnose network-level failures (Service, Ingress connectivity)
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_network_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>"}'
```

## Parameter Reference

### Common Parameters

| Parameter    | Required | Description                              | Default        |
| ------------ | -------- | ---------------------------------------- | -------------- |
| `region`     | Yes      | Huawei Cloud region, e.g., cn-north-4    | `HW_REGION_NAME` |
| `cluster_id` | Yes      | CCE cluster ID                           | `HW_CLUSTER_ID` |
| `namespace`  | Yes*     | Kubernetes namespace                     | N/A            |
| `kind`       | Yes*     | Workload type: Deployment, StatefulSet, or DaemonSet | N/A |
| `name`       | Yes*     | Workload name                            | N/A            |

*Required only for `huawei_workload_rollout_diagnose` and `huawei_get_workload_rollout_context`.

### Workload-Specific Parameters

| Parameter     | Required | Description                              | Constraints         |
| ------------- | -------- | ---------------------------------------- | ------------------- |
| `kind`        | Yes      | Workload type                            | `Deployment`, `StatefulSet`, or `DaemonSet` only |
| `name`        | Yes      | Workload name                            | Must reference existing workload in the namespace |

### Optional Parameters (passed via `--params` JSON)

| Parameter        | Description                                           | Default |
| ---------------- | ----------------------------------------------------- | ------- |
| `ak`             | Override AK (uses `HW_ACCESS_KEY` by default)         | env var |
| `sk`             | Override SK (uses `HW_SECRET_KEY` by default)         | env var |
| `project_id`     | Override project ID (auto-obtained via IAM when not set) | env var |
| `label_selector` | Pod label selector for filtering                      | None    |
| `hours`          | Metric query time range in hours                      | 1       |
| `top_n`          | Number of top results for metrics                     | 10      |

### Supported Regions

| Region Name                    | Region ID        |
| ------------------------------ | ---------------- |
| North China - Beijing 4        | `cn-north-4`     |
| North China - Beijing 1        | `cn-north-1`     |
| East China - Shanghai 1        | `cn-east-3`      |
| East China - Shanghai 2        | `cn-east-2`      |
| South China - Guangzhou        | `cn-south-1`     |
| Southwest China - Guiyang 1    | `cn-southwest-2` |
| Asia Pacific - Bangkok         | `ap-southeast-2` |
| Asia Pacific - Singapore       | `ap-southeast-1` |
| Asia Pacific - Hong Kong       | `ap-southeast-3` |
| Europe - Paris                 | `eu-west-0`      |

## Output Format

See [Output Schema](references/output-schema.md) for detailed response format examples.

### Primary Diagnosis: `huawei_workload_rollout_diagnose`

```json
{
  "success": true,
  "action": "workload_rollout_diagnose",
  "target": {
    "namespace": "default",
    "kind": "Deployment",
    "name": "api"
  },
  "selector": {
    "value": "app=api",
    "source": "matchLabels"
  },
  "summary": {
    "status": "control_plane_not_observed | new_version_not_created | rollout_blocked | replicas_unavailable | probe_failure | healthy",
    "headline": "human-readable diagnosis; may note when old-version replicas remain available",
    "expected_replicas": 3,
    "ready_replicas": 1,
    "available_replicas": 1,
    "top_cause": "ProbeFailure | ContainerCommandNotFound | CrashLoopOrAppExit | ..."
  },
  "generation_check": {
    "generation": 5,
    "observed_generation": 5,
    "observed": true
  },
  "workload": {
    "kind": "Deployment",
    "uid": "workload-uid",
    "desired_replicas": 3,
    "updated_replicas": 3,
    "ready_replicas": 1,
    "available_replicas": 1,
    "conditions": []
  },
  "version": {
    "strategy": "DeploymentReplicaSet",
    "new_rs": {},
    "old_rs": []
  },
  "funnel": [
    {"layer": "workload_current", "expected": 3, "actual": 3, "status": "pass"},
    {"layer": "new_pods_ready", "expected": 3, "actual": 1, "status": "fail"}
  ],
  "events": {
    "filtered_count": 5,
    "timeline": [],
    "filter": {
      "uid_count": 6,
      "before_count": 40,
      "after_count": 5,
      "events_without_involved_uid": 0
    }
  },
  "pod_diagnosis": {
    "diagnosed_pods": 1,
    "pods": []
  },
  "top_causes": [
    {
      "rank": 1,
      "type": "ProbeFailure",
      "title": "New version Pods are Running but probe checks fail or Pods are not Ready",
      "confidence": 0.88,
      "evidence": [],
      "recommendation": []
    }
  ],
  "handoff": [
    {
      "skill": "huawei-cloud-cce-pod-failure-diagnoser",
      "reason": "Probe failure requires Pod logs and health check configuration analysis"
    }
  ],
  "warnings": []
}
```

### Context-Only: `huawei_get_workload_rollout_context`

```json
{
  "success": true,
  "action": "get_workload_rollout_context",
  "workload": {},
  "replicasets": [],
  "pods": [],
  "events": [],
  "event_filter": {},
  "warnings": []
}
```

### Summary Status Values

| Status                       | Description                                               |
| ---------------------------- | --------------------------------------------------------- |
| `healthy`                    | All replicas ready and available; rollout complete         |
| `control_plane_not_observed` | `observedGeneration < generation`; controller lagging      |
| `new_version_not_created`    | New ReplicaSet has zero current replicas or no owned Pods  |
| `rollout_blocked`            | Rollout funnel layer fails; replicas below expected        |
| `replicas_unavailable`       | Updated/ready/available replicas below desired count       |
| `probe_failure`              | Pod Running but not Ready; Unhealthy probe events present  |

### Top Cause Types

| Top Cause Type              | Description                                               |
| --------------------------- | --------------------------------------------------------- |
| `ProbeFailure`              | Startup/liveness/readiness probe failing                  |
| `ContainerCommandNotFound`  | Executable not found in container `$PATH`                 |
| `CrashLoopOrAppExit`        | Container crashing or exiting unexpectedly                 |
| `ImagePullBackOff`          | Container image cannot be pulled                          |
| `OOMKilled`                 | Container killed by OOM                                   |
| `QuotaOrAdmissionRejected`  | ReplicaSet creation blocked by quota/admission/webhook    |
| `SchedulingFailure`         | Pod Pending due to FailedScheduling                       |
| `StorageMountFailure`       | Pod FailedMount/FailedAttachVolume                        |

## Verification

See [Verification Method](references/verification-method.md) for step-by-step verification.

## Best Practices

1. **Always start with primary diagnosis** — Use `huawei_workload_rollout_diagnose` before collecting raw context; it provides the rollout funnel and ranked Top causes
2. **Drill down from workload layer** — Identify which funnel layer first fails before drilling into Pod-level diagnosis; do not skip the workload layer
3. **Use Pod diagnosis for drill-down** — When NewRS Pods exist but are not Ready, use `huawei_pod_failure_diagnose` and `huawei_get_pod_logs` for deeper analysis
4. **Only use UID-filtered Events** — Only accept Events whose `involvedObject.uid` belongs to Workload, ReplicaSet, or Pod objects; do not treat all namespace Warning events as relevant
5. **Check generation before Pod analysis** — If `observedGeneration < generation`, diagnose control-plane pressure before looking at Pods
6. **Distinguish old vs new version replicas** — A Deployment with old ReplicaSet replicas still available is not "healthy"; the funnel tracks new-version readiness specifically
7. **Cite specific evidence** — Always cite specific objects, events, log segments, or API fields in diagnosis output; never present guesses as conclusions
8. **Write "insufficient evidence" when lacking** — When evidence is insufficient, write "insufficient evidence" explicitly; never fabricate diagnosis results
9. **Hand off cross-domain failures** — When evidence points to scheduling/node pressure, hand off to `huawei-cloud-cce-node-failure-diagnoser`; for Service/Ingress/ELB issues, hand off to `huawei-cloud-cce-network-failure-diagnoser`
10. **Remediation as recommendations only** — All remediation actions (scale, resize, delete, cordon/drain/reboot) must be output as recommendations and handed off to `huawei-cloud-cce-auto-remediation-runner`

## Reference Documents

| Document                                                  | Description                              |
| --------------------------------------------------------- | ---------------------------------------- |
| [Workflow](references/workflow.md)                        | Evidence collection order, failure rules, and diagnosis flow |
| [Output Schema](references/output-schema.md)              | Response format specification for primary and context actions |
| [Risk Rules](references/risk-rules.md)                    | Allowed/not-allowed operations and handoff mapping |
| [Verification Method](references/verification-method.md)  | Step-by-step verification procedures     |
| [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html) | Official CCE documentation |
| [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html) | CCE API reference |

## Notes

- **This skill is read-only diagnosis only** — no write, scale, delete, cordon, drain, or reboot operations
- **Do not output credential values** — never expose `HW_ACCESS_KEY`, `HW_SECRET_KEY`, `HW_SECURITY_TOKEN` values in logs, responses, or error messages
- **All scripts must be executed via `skill action=exec`** — do not run them directly in a shell
- **Do not call remediation actions** — `huawei_scale_cce_workload`, `huawei_resize_cce_workload`, `huawei_delete_cce_workload` are out of scope
- **Do not add `confirm=true`** — this skill never confirms remediation actions; it only outputs recommendations
- **Run environment check first** — the check script must be executed before any diagnosis action
- **Temporary AK/SK requires `HW_SECURITY_TOKEN`** — set this environment variable when using temporary credentials
- **Cross-skill handoff uses prefixed names** — handoff targets use `huawei-cloud-cce-` prefix convention (e.g., `huawei-cloud-cce-pod-failure-diagnoser`)

## Common Pitfalls

| Pitfall                                                | Symptom                                           | Quick Fix                                                    |
| ------------------------------------------------------ | ------------------------------------------------- | ------------------------------------------------------------ |
| Treating all namespace Warning events as evidence      | False-positive diagnosis with irrelevant events   | Only use UID-filtered events whose `involvedObject.uid` belongs to Workload/RS/Pod |
| Skipping generation check                              | Misdiagnosing Pod failures when controller is lagging | If `observedGeneration < generation`, diagnose control-plane pressure first |
| Confusing old-version replicas with health             | Declaring workload "healthy" when old RS still active | The rollout funnel tracks new-version readiness specifically |
| Diagnosing Pod failures directly without funnel        | Missing the workload-layer root cause             | Start from workload layer; identify which funnel layer first fails |
| Attempting remediation from this skill                 | Unauthorized scale/delete/cordon/drain actions    | All changes must be handed off to `huawei-cloud-cce-auto-remediation-runner` |
| Ignoring ReplicaSetCreateBlocked subtype               | Missing quota/admission/webhook rejection evidence | Check FailedCreate events mentioning quota, LimitRange, admission, webhook, forbidden |
| Using unfiltered namespace events                      | Too many irrelevant Warning events in diagnosis   | Apply UID-based event filtering per workflow step 5          |
| Not running environment check script first             | SDK import errors or credential failures          | Run `check_env.sh` / `check_env.ps1` before any action       |
| Hardcoding cluster_id instead of environment variable  | Wrong cluster or repeated manual entry            | Use `HW_CLUSTER_ID` env var or pass `cluster_id` per action  |
| Confusing Deployment RS vs StatefulSet version model   | Wrong version analysis for StatefulSet/DaemonSet  | Deployment uses ReplicaSet revision; StatefulSet/DaemonSet use workload itself |