---
id: huawei-cloud-cce-root-cause-analyzer
name: huawei-cloud-cce-root-cause-analyzer
description: |
  Huawei Cloud CCE cross-domain root cause analysis skill using Python SDK dispatcher.
  Use this skill when a CCE incident spans alarms, workload rollout, Pod events/logs, recent changes, service topology, nodes, network, or metrics, and the user needs a complete Markdown root-cause report with investigation steps, evidence chain, impact scope, Top3 causes, confidence, and remediation handoff.
  Trigger: user mentions "root cause analysis", "根因分析", "multiple failures", "多类告警", "cross-resource diagnosis", "跨资源诊断", "comprehensive diagnosis", "综合诊断", "RCA", "故障定位", "impact scope", "影响面分析", "change correlation", "变更关联"
tags: [cce, root-cause-analysis, cross-domain-diagnosis, kubernetes, fault-diagnosis]
---

# CCE Root Cause Analysis

> **⚠️ Execution Method (Must Read): This skill executes diagnosis via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Tools section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill converges multi-domain evidence into root cause conclusions for CCE incidents. It orchestrates workload rollout diagnosis, dependency impact analysis, change impact analysis, AOM alarm analysis, and cross-domain drill-down (network, node) to produce a complete Markdown report with investigation steps, timeline, evidence chain, impact scope, Top3 root causes, confidence, counter-evidence, and remediation handoff.

This skill is applicable to the following scenarios:

1. Cross-resource incidents involving multiple failure domains (workload + dependency + change + alarm)
2. Root cause analysis when alarms span multiple CCE resources and the user needs comprehensive diagnosis
3. Correlating recent changes (deployments, config updates, network/security policy changes, node changes) with observed failures
4. Dependency impact propagation analysis (Service → Ingress → Pod → Node chain)
5. Workload rollout failures requiring evidence funnel (generation → ReplicaSet → Pod Ready → events → logs → command/args → probes → image)
6. Producing structured Top3 root cause reports with evidence, counter-evidence, and confidence scores

This skill does NOT handle the following:

1. Executing any remediation actions (scale, delete, drain, reboot, vulnerability state modification, cluster sleep/wake)
2. Making root cause conclusions from a single alarm without timeline or evidence chain
3. Creating, modifying, or deleting CCE resources
4. Guessing or fabricating diagnosis results without evidence

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
| cce:node:list | List nodes | List cluster nodes |
| aom:*:get | Read AOM | Query AOM metrics and alarms |
| aom:event:list | List events | Query AOM alarm events |
| aom:alarmRule:list | List alarm rules | Query alarm rules |

**Permission Failure Handling**:
1. When any command fails due to permission errors, display required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation

---

## Core Tools

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`:

**Primary Comprehensive Diagnosis:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_root_cause_analyze` | region, cluster_id | Primary comprehensive action: orchestrates workload rollout diagnosis, dependency impact, change impact, and AOM alarms into a unified root cause report with Top3 causes |

**Workload Domain Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_workload_rollout_diagnose` | region, cluster_id, namespace, kind, name | Diagnose Deployment/StatefulSet/DaemonSet rollout failures with funnel and Top causes |
| `huawei_workload_diagnose` | region, cluster_id | General workload status diagnosis |
| `huawei_workload_diagnose_by_alarm` | region, cluster_id | Workload diagnosis triggered by AOM alarm correlation |
| `huawei_pod_failure_diagnose` | region, cluster_id | Pod-level failure diagnosis (CrashLoop, ImagePull, OOM, Pending, etc.) |

**Dependency and Impact Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_dependency_impact_analyze` | region, cluster_id | Analyze Service/Ingress/Pod/Node propagation paths and impact scope for service unavailability |

**Change Impact Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_change_impact_analyze` | region, cluster_id | Correlate recent changes (deployment, config, network, security policy, node changes) with observed failures via audit log and AOM alarm timeline |

**Network and Node Domain Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_network_diagnose` | region, cluster_id | General network connectivity diagnosis |
| `huawei_network_diagnose_by_alarm` | region, cluster_id | Network diagnosis triggered by AOM alarm correlation |
| `huawei_network_failure_diagnose` | region, cluster_id | Network failure diagnosis (Service, Ingress connectivity) |
| `huawei_node_diagnose` | region, cluster_id | Node-level diagnosis (scheduling, pressure) |
| `huawei_node_failure_diagnose` | region, cluster_id | Node failure diagnosis |
| `huawei_node_batch_diagnose` | region, cluster_id | Batch node diagnosis for multi-node issues |

**Alarm and Report Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_analyze_aom_alarms` | region, cluster_id | Analyze AOM alarm patterns and correlation across resources |
| `huawei_generate_diagnosis_report` | region, cluster_id | Generate structured Markdown diagnosis report |
| `huawei_generate_monitor_dashboard` | region, cluster_id | Generate monitoring dashboard for ongoing observation |

**Supporting Evidence Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_get_cce_events` | region, cluster_id | List Kubernetes Events in the cluster |

---

## Parameter Reference

**Common Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| region | Yes | Huawei Cloud region, e.g., cn-north-4 |
| cluster_id | Yes | CCE cluster ID |
| namespace | Yes* | Kubernetes namespace (required for workload-specific actions) |
| kind | Yes* | Workload type: Deployment, StatefulSet, or DaemonSet |
| name | Yes* | Workload name |

*Required only for `huawei_workload_rollout_diagnose`.

**Optional Parameters (passed via `--params` JSON):**

| Parameter | Description |
|-----------|-------------|
| ak | Override AK (uses HW_ACCESS_KEY by default) |
| sk | Override SK (uses HW_SECRET_KEY by default) |
| project_id | Override project ID (auto-obtained via IAM when not set) |
| target_name | Optional workload/app/service name for scope narrowing |
| hours | Metric/query time range in hours (default 1) |
| top_n | Number of top results for ranking (default 3) |

---

## Output Format

### Primary Comprehensive: `huawei_root_cause_analyze`

```json
{
  "success": true,
  "analysis_trace_id": "RCA-...",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "optional",
    "target_name": "optional workload/app/service"
  },
  "summary": {
    "top_cause": {},
    "cause_count": 3,
    "data_sources": {
      "rollout": true,
      "dependency": true,
      "change": true,
      "alarms": true
    }
  },
  "top_causes": [
    {
      "rank": 1,
      "type": "ContainerCommandNotFound",
      "title": "New version container startup command or entry file does not exist",
      "domain": "workload",
      "confidence": 0.94,
      "evidence": [],
      "counter_evidence": [],
      "recommendation": [],
      "remediation_hint": {
        "skill": "huawei-cloud-cce-auto-remediation-runner",
        "action": "huawei_auto_remediation_run",
        "strategy": "rollback_previous_revision",
        "requires_confirmation": true
      }
    }
  ],
  "report_markdown": "# CCE Comprehensive Root Cause Analysis Report...",
  "report_file": "optional"
}
```

### Supporting Domain Outputs

Each domain action (`huawei_workload_rollout_diagnose`, `huawei_dependency_impact_analyze`, `huawei_change_impact_analyze`, `huawei_analyze_aom_alarms`) produces its own structured JSON output. See individual skill documentation for domain-specific schemas.

---

## Verification

1. Run the environment check script to confirm dependencies and credentials are available
2. Use `huawei_root_cause_analyze` on a known healthy cluster to verify it returns `success: true` with zero or low-confidence causes
3. Use `huawei_root_cause_analyze` on a cluster with known multi-domain failures to verify Top3 causes are accurately identified
4. Compare `huawei_root_cause_analyze` summary with individual domain action outputs for consistency
5. Verify that evidence chains reference specific objects, events, and API fields (not generic statements)
6. Verify that counter-evidence is present for each top cause candidate
7. Confirm that low-confidence conclusions are clearly labeled with required supplementary data

---

## Best Practices

1. Always start with `huawei_root_cause_analyze` for comprehensive diagnosis; drill down into individual domain actions only when specific evidence requires deeper analysis
2. For workload rollout failures, prioritize the rollout funnel: generation/observedGeneration → ReplicaSet → Pod Ready → Events → Logs → command/args → probes → image
3. For service unavailability, use `huawei_dependency_impact_analyze` to trace Service selector → Ingress backend → Pod Ready → Node distribution propagation paths
4. For suspected change-induced failures, use `huawei_change_impact_analyze` to build "change occurred before failure" causal chain with audit logs, K8s historical events, and AOM alarms
5. Never conclude root cause from a single alarm alone; always provide timeline or evidence chain
6. Record supporting evidence, counter-evidence, data gaps, and remediation handoff for each root cause candidate
7. Sort root causes by impact scope, timeline alignment, evidence strength, and recoverability
8. Clearly label low-confidence conclusions with required supplementary data
9. All remediation actions must be output as recommendations only and handed off to `huawei-cloud-cce-auto-remediation-runner`

---

## Reference Documents

- Evidence chain and root cause ranking workflow: `references/workflow.md`
- Output structure specification: `references/output-schema.md`
- Risk boundaries and handoff rules: `references/risk-rules.md`
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

---

## Notes

1. This skill is read-only diagnosis and report generation only; no write, scale, delete, cordon, drain, reboot, vulnerability state modification, or cluster sleep/wake operations
2. Do not output the values of HW_ACCESS_KEY, HW_SECRET_KEY, HW_SECURITY_TOKEN, or other environment variables
3. All scripts must be executed via `skill action=exec`; do not run them directly in a shell
4. Any action requiring `confirm=true` must be handed off to `huawei-cloud-cce-auto-remediation-runner`; this skill never executes remediation
5. The environment check script must be run before any diagnosis action
6. When using temporary AK/SK, HW_SECURITY_TOKEN must be set

---

## Common Pitfalls

1. **Concluding root cause from a single alarm** — Always require timeline or evidence chain; a single alarm without temporal correlation is insufficient evidence
2. **Skipping `huawei_root_cause_analyze` and drilling into individual domains first** — Always start with comprehensive analysis; individual domain drill-down is for supplementary evidence only
3. **Ignoring counter-evidence** — Each root cause candidate must include counter-evidence and data gaps; omitting these leads to false confidence
4. **Not building a fault timeline** — Establish user-perceived time, alarm trigger time, Kubernetes event time, and change time before ranking causes
5. **Attempting remediation actions from this skill** — All changes must be handed off to `huawei-cloud-cce-auto-remediation-runner`; this skill only outputs recommendations
6. **Failing to label low-confidence conclusions** — When evidence is insufficient, write "insufficient evidence" explicitly; never present guesses as conclusions
7. **Not correlating changes with failures** — When a recent deployment, config, network, or security policy change exists, use `huawei_change_impact_analyze` to verify the "change before failure" causal chain
8. **Treating dependency propagation as single-direction** — Dependency impact can propagate bidirectionally (upstream failure affects downstream, and downstream back-pressure affects upstream); analyze both directions