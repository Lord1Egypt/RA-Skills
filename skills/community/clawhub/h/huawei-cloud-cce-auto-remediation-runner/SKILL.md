---
id: huawei-cloud-cce-auto-remediation-runner
name: huawei-cloud-cce-auto-remediation-runner
description: |
  Huawei Cloud CCE auto-remediation runner skill that converts remediation intent into preview-first, confirm-required, post-verify execution plans.
  Use this skill only when the user asks for a CCE remediation action or a diagnosis result needs a preview-first recovery plan, including Deployment rollback, restart/scale/resize, cordon/drain, reboot, isolation, traffic cutover, vulnerability status change, or cluster hibernate/awake.
  This skill performs MUTATION actions (drain, cordon, scale, restart, delete, reboot, hibernate) that require preview+confirm workflow. NEVER auto-add confirm=true.
  Trigger: "auto remediation", "自动恢复", "remediation action", "恢复动作", "node drain", "节点 drain", "node cordon", "节点 cordon", "scale workload", "扩缩容", "restart pod", "重启 Pod", "remediation preview", "恢复预览", "confirm remediation", "确认恢复"
tags: [cce, remediation, auto-heal, mutation]
---

# CCE Auto Remediation Runner

> **⚠️ Execution Method (Must Read): This skill executes remediation actions via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Tools section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill converts remediation intent into reviewable, confirmable, verifiable execution plans. It operates in **preview-first mode by default** — all mutation actions require preview without `confirm=true`, explicit user confirmation of action/object/risks, then execution with `confirm=true`, followed by read-only verification.

This skill is applicable to the following scenarios:

1. Remediation actions triggered by root-cause analysis conclusions (e.g., Deployment rollback for CrashLoop/ImagePull/CommandNotFound)
2. Node operations: cordon, uncordon, drain, reboot ECS
3. Workload operations: scale, resize, rollback, delete
4. Node pool operations: resize node pool
5. Cluster operations: hibernate, awake
6. Security operations: HSS vulnerability status change
7. Auto-remediation orchestration via `huawei_auto_remediation_run` for multi-step remediation plans
8. Traffic cutover: bind/unbind cluster EIP
9. ECS instance operations: start, stop

This skill does NOT handle the following:

1. Read-only diagnosis (use `huawei-cloud-cce-root-cause-analyzer` or domain-specific diagnoser skills)
2. Auto-executing remediation without preview and user confirmation
3. Guessing or fabricating remediation results without evidence
4. Batch or fuzzy-target remediation without explicit user confirmation per object

---

## Prerequisites

**Before using, you must run the environment check script to complete environment validation and dependency installation in one step:**

- Linux / macOS: `skill action=exec: bash skill://scripts/check_env.sh`
- Windows: `skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1`

> Windows Note: Do not use `&&` to chain commands (PowerShell 5.x does not support it). Use semicolons if you need to change directories first.

The script will check in sequence: Python >= 3.6 → install dependencies → validate SDK → validate credentials → validate service availability.
If the environment check fails, fix the issues before continuing with other actions.

**Environment Variables:**

| Variable | Required | Description |
|----------|----------|-------------|
| HW_ACCESS_KEY | Yes | Huawei Cloud AK |
| HW_SECRET_KEY | Yes | Huawei Cloud SK |
| HW_REGION_NAME | No | Default cn-north-4 |
| HW_PROJECT_ID | No | Project ID (automatically obtained via IAM API when not set) |
| HW_SECURITY_TOKEN | No | Required when using temporary AK/SK |
| HW_CLUSTER_ID | No | Default CCE cluster ID (can also be passed per action) |

**Security Constraints:**

1. Never persist credentials (AK/SK/Token/Certificate) to the filesystem
2. AK/SK exist only within the current request call stack; released after use
3. Only non-sensitive project IDs are cached in process memory (never written to disk)
4. All temporary certificate files must be deleted immediately after use
5. Never expose AK/SK in logs, responses, or error messages

**Do not output the values of the above environment variables.**

---

### IAM Permission Requirements

| API Action | Permission | Purpose |
|-----------|------------|---------|
| cce:cluster:get | Get cluster | View cluster details |
| cce:cluster:list | List clusters | List CCE clusters |
| cce:node:get | Get node | View node details |
| cce:node:list | List nodes | List cluster nodes |
| cce:node:update | Update node | Cordon/uncordon/drain nodes |
| cce:nodepool:update | Update node pool | Resize node pools |
| cce:nodepool:get | Get node pool | View node pool details |
| cce:nodepool:list | List node pools | List node pools |
| aom:*:get | Read AOM | Query AOM metrics and alarms |
| aom:alarmRule:list | List alarm rules | Query alarm rules for validation |
| aom:event:list | List events | Query AOM alarm events |

**Permission Failure Handling**:
1. When any command fails due to permission errors, display required permission list and policy JSON
2. Guide the user to create a custom policy in the IAM console and grant authorization
3. Pause execution and wait for user confirmation that permissions have been granted

---

## Core Tools

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`.

### Auto-Remediation Orchestration

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_auto_remediation_run` | region, cluster_id, strategy | Orchestrate multi-step remediation plan; strategy determines actions (rollback_previous_revision, scale_out, drain_and_replace, etc.) |

### Workload Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_rollback_cce_workload` | region, cluster_id, namespace, kind, name | Rollback Deployment/StatefulSet/DaemonSet to previous revision |
| `huawei_scale_cce_workload` | region, cluster_id, namespace, kind, name, replicas | Scale workload replicas |
| `huawei_resize_cce_workload` | region, cluster_id, namespace, kind, name | Resize workload resource limits |
| `huawei_delete_cce_workload` | region, cluster_id, namespace, kind, name | Delete a workload |

### Node Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_cce_node_cordon` | region, cluster_id, node_name | Mark node as unschedulable |
| `huawei_cce_node_uncordon` | region, cluster_id, node_name | Mark node as schedulable again |
| `huawei_cce_node_drain` | region, cluster_id, node_name | Evict all pods from node |
| `huawei_reboot_ecs` | region, ecs_id | Reboot the underlying ECS instance |

### Node Pool and Cluster Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_resize_cce_nodepool` | region, cluster_id, nodepool_id, target_count | Resize node pool to target count |
| `huawei_hibernate_cce_cluster` | region, cluster_id | Hibernate (sleep) the CCE cluster |
| `huawei_awake_cce_cluster` | region, cluster_id | Awake (wake) the CCE cluster |
| `huawei_delete_cce_cluster` | region, cluster_id | Delete the CCE cluster |
| `huawei_delete_cce_node` | region, cluster_id, node_name | Delete a node from the cluster |

### ECS Instance Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_start_ecs_instance` | region, ecs_id | Start ECS instance |
| `huawei_stop_ecs_instance` | region, ecs_id | Stop ECS instance |

### Elastic Scaling Policy

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_configure_cce_hpa` | region, cluster_id, namespace, kind, name, min_replicas, max_replicas | Configure HPA policy for workload |

### Network / Traffic Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_bind_cce_cluster_eip` | region, cluster_id, eip_id | Bind EIP to cluster for external access |
| `huawei_unbind_cce_cluster_eip` | region, cluster_id | Unbind EIP from cluster |
| `huawei_network_verify_pod_scheduling` | region, cluster_id, namespace | Verify pod scheduling network connectivity |

### Security Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_hss_change_vul_status` | region, vul_id, status | Change HSS vulnerability handling status |

### Verification (Read-Only) Actions

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_get_cce_pods` | region, cluster_id | List pods in cluster |
| `huawei_get_kubernetes_nodes` | region, cluster_id | List Kubernetes nodes in cluster |
| `huawei_get_cce_events` | region, cluster_id | List Kubernetes Events in cluster |
| `huawei_workload_rollout_diagnose` | region, cluster_id, namespace, kind, name | Diagnose workload rollout status |
| `huawei_root_cause_analyze` | region, cluster_id | Comprehensive root cause analysis (cross-skill: `huawei-cloud-cce-root-cause-analyzer`) |
| `huawei_dependency_impact_analyze` | region, cluster_id | Dependency impact analysis (cross-skill: `huawei-cloud-cce-root-cause-analyzer`) |
| `huawei_node_diagnose` | region, cluster_id | Node-level diagnosis |
| `huawei_workload_diagnose` | region, cluster_id | Workload status diagnosis |

---

## Parameter Reference

**Common Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| region | Yes | Huawei Cloud region, e.g., cn-north-4 |
| cluster_id | Yes* | CCE cluster ID |
| namespace | Yes* | Kubernetes namespace (required for workload actions) |
| kind | Yes* | Workload type: Deployment, StatefulSet, or DaemonSet |
| name | Yes* | Workload name or node name |
| node_name | Yes* | Node name (required for node actions) |
| nodepool_id | Yes* | Node pool ID (required for node pool resize) |
| ecs_id | Yes* | ECS instance ID (required for ECS actions) |
| replicas | Yes* | Target replica count (required for scale) |
| target_count | Yes* | Target node count (required for node pool resize) |
| strategy | Yes* | Remediation strategy (required for auto-remediation) |
| confirm | No | Set to `true` ONLY after explicit user confirmation |

*Required for specific actions as noted.

**Optional Parameters (passed via `--params` JSON):**

| Parameter | Description |
|-----------|-------------|
| ak | Override AK (uses HW_ACCESS_KEY by default) |
| sk | Override SK (uses HW_SECRET_KEY by default) |
| project_id | Override project ID (auto-obtained via IAM when not set) |
| min_replicas | HPA minimum replicas |
| max_replicas | HPA maximum replicas |
| vul_id | HSS vulnerability ID |
| status | HSS vulnerability handling status |
| eip_id | EIP ID for bind action |

---

## Output Format

### Remediation Preview (confirm=false)

```json
{
  "success": false,
  "requires_confirmation": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision",
  "diagnosis": {},
  "action_result": {},
  "preview": {
    "action": "huawei_rollback_cce_workload",
    "target": {
      "region": "cn-north-4",
      "cluster_id": "cluster-id",
      "namespace": "default",
      "kind": "Deployment",
      "name": "app-server"
    },
    "current_state": {},
    "expected_state": {},
    "impact_scope": {},
    "rollback_method": "Re-apply current revision"
  },
  "risk_level": "R2",
  "rollback_notes": [],
  "summary": "Remediation plan preview — requires user confirmation before execution"
}
```

### Remediation Execution (confirm=true)

```json
{
  "success": true,
  "requires_confirmation": false,
  "confirmation_received": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision",
  "action_result": {},
  "execution": {
    "action": "huawei_rollback_cce_workload",
    "timestamp": "...",
    "result": {}
  },
  "verification": [
    {
      "method": "huawei_get_cce_pods",
      "status": "healthy",
      "details": {}
    }
  ],
  "report_markdown": "# CCE Auto Remediation Execution Report...",
  "report_file": "optional"
}
```

### Full Auto-Remediation Orchestration Output

```json
{
  "success": false,
  "requires_confirmation": true,
  "remediation_trace_id": "ARR-...",
  "strategy": "rollback_previous_revision",
  "diagnosis": {},
  "action_result": {},
  "verification": {},
  "summary": "remediation plan or execution result",
  "action": "huawei_auto_remediation_run",
  "risk_level": "R2",
  "target": {
    "region": "cn-north-4",
    "cluster_id": "optional",
    "resource": "optional"
  },
  "preview": {},
  "requires_confirmation": true,
  "confirmation_received": false,
  "execution": {},
  "verification": [],
  "rollback_notes": [],
  "report_markdown": "# CCE Auto Remediation Execution Report...",
  "report_file": "optional"
}
```

---

## Verification

1. Run the environment check script to confirm dependencies and credentials are available
2. Use `huawei_cce_node_cordon` (without `confirm=true`) on a test node to verify preview mode returns `requires_confirmation: true`
3. After user confirmation, execute with `confirm=true` and verify node status with `huawei_get_kubernetes_nodes`
4. Use `huawei_rollback_cce_workload` preview mode to verify it shows current vs expected state
5. After rollback execution, verify workload health with `huawei_workload_rollout_diagnose`
6. Use `huawei_auto_remediation_run` preview mode to verify multi-step orchestration plan is shown before execution
7. Confirm that all R3 actions (drain, reboot, delete, hibernate) require explicit user confirmation
8. Verify that post-execution verification actions return healthy/expected status

---

## Best Practices

1. **Always preview first**: Never call any mutation action with `confirm=true` on the first invocation. Always preview without `confirm=true` first
2. **State the four essentials**: Before confirmation, restate the action, object, parameters, impact scope, and rollback plan to the user
3. **Prefer rollback for deployment failures**: If root cause is from `huawei-cloud-cce-root-cause-analyzer` and involves startup command, CrashLoop, probe, or image causing new version unavailability, prefer `huawei_auto_remediation_run` with `rollback_previous_revision` strategy
4. **Verify after execution**: Every execution must be followed by read-only verification (Pod status, Node status, Events, workload rollout diagnosis)
5. **Classify risk correctly**: Refer to `references/risk-rules.md` for R1/R2/R3 classification; apply appropriate confirmation requirements
6. **Never auto-add confirm**: Deployment rollback, scale, resize, resource modification, delete cluster/node/workload, drain, reboot, and HSS vulnerability status change must all be preview → user confirm → execute → verify
7. **Use auto-remediation orchestration for multi-step plans**: When remediation involves multiple actions, use `huawei_auto_remediation_run` to produce a complete execution report with diagnosis basis, action results, and verification results
8. **Cross-skill handoff for diagnosis**: When root cause analysis is needed before remediation, hand off to `huawei-cloud-cce-root-cause-analyzer`; this skill only executes confirmed remediation actions
9. **Document rollback notes**: Every execution plan must include rollback method — how to revert if the remediation causes unintended effects

---

## Reference Documents

- Workflow and action orchestration steps: `references/workflow.md`
- Risk classification and confirm=true rules: `references/risk-rules.md`
- Output execution record schema: `references/output-schema.md`
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

---

## Notes

1. This skill is a **MUTATION skill** — it performs write actions (drain, cordon, scale, restart, delete, reboot, hibernate, vulnerability status change). Preview+confirm workflow is mandatory
2. Do not output the values of HW_ACCESS_KEY, HW_SECRET_KEY, HW_SECURITY_TOKEN, or other environment variables
3. All scripts must be executed via `skill action=exec`; do not run them directly in a shell
4. NEVER auto-add `confirm=true`. User must explicitly confirm the specific action, object, and risks
5. The environment check script must be run before any remediation action
6. When using temporary AK/SK, HW_SECURITY_TOKEN must be set
7. After execution, must call read-only verification actions to confirm status
8. Cross-skill references: diagnosis → `huawei-cloud-cce-root-cause-analyzer`; domain-specific diagnosis → `huawei-cloud-cce-pod-failure-diagnoser`, `huawei-cloud-cce-node-failure-diagnoser`, `huawei-cloud-cce-network-failure-diagnoser`

---

## Common Pitfalls

1. **Auto-adding confirm=true** — The most critical pitfall. NEVER assume user intent implies confirmation. Always preview first, show results, and wait for explicit user confirmation
2. **Skipping preview for R2 actions** — Even medium-risk actions (scale, resize, cordon, rollback) require preview. No mutation action may skip the preview step
3. **Not verifying after execution** — Every R2/R3 execution must be followed by read-only verification (Pod/Node/Workload/Events status). Skipping verification leaves remediation unconfirmed
4. **Batch or fuzzy-target remediation** — R3 actions (drain, reboot, delete, hibernate) must have explicit, specific target objects. Never execute with vague or batch targets without per-object confirmation
5. **Not documenting rollback method** — Every remediation plan must state how to revert if the action causes unintended effects. Omitting rollback notes is a safety hazard
6. **Executing remediation without diagnosis** — Always confirm root cause via `huawei-cloud-cce-root-cause-analyzer` or domain diagnoser before remediation. Blind remediation without evidence is prohibited
7. **Confusing R2 and R3 risk levels** — R2 (runtime impact) requires preview+confirm; R3 (destructive) requires explicit per-object confirmation with additional verification. See `references/risk-rules.md`
8. **Not restating the plan to the user** — Before requesting confirmation, restate the action, target object, region, cluster_id, expected impact, and rollback plan. The user must confirm all four essentials