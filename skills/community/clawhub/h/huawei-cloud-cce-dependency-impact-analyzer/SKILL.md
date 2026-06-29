---
id: huawei-cloud-cce-dependency-impact-analyzer
name: huawei-cloud-cce-dependency-impact-analyzer
description: |
  Huawei Cloud CCE service topology dependency impact analysis skill that traces Service/Ingress/Pod/Node propagation paths and upstream/downstream blast radius.
  Use this skill when a CCE incident needs service topology impact analysis, including Service/Ingress/Pod/Node propagation paths, upstream/downstream blast radius, affected entrypoints, and a complete Markdown impact report with evidence and confidence limits.
  Trigger: "dependency impact", "依赖影响", "dependency analysis", "依赖分析", "cascade failure", "级联故障", "blast radius", "爆炸半径", "service topology", "服务拓扑", "propagation path", "传播路径", "upstream downstream impact", "上下游影响", "dependency mapping", "依赖映射"
tags: [cce, dependency, impact, cascade]
---

# CCE Dependency Impact Analyzer

> **⚠️ Execution Method (Must Read): This skill executes diagnosis via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Tools section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill analyzes Kubernetes service topology to determine fault propagation paths and upstream/downstream dependency impact. It collects Pod, Service, Ingress, and Node snapshots, maps Service selectors to target Pods, identifies Ingress external entrypoints, and produces a complete Markdown report with propagation paths, evidence tables, impact scoring, and confidence limitations.

This skill is applicable to the following scenarios:

1. Service unavailability requiring upstream/downstream dependency tracing (Service → Ingress → Pod → Node)
2. Determining blast radius when a workload becomes unhealthy
3. Identifying which external entrypoints (Ingress rules) are affected by Pod failures
4. Mapping cluster-internal traffic paths (Service DNS → Pod) and external traffic paths (Ingress → Service → Pod)
5. Assessing impact severity by combining Pod readiness, Service exposure, Ingress exposure, and propagation path count
6. Producing structured impact reports with topology evidence, confidence limits, and remediation handoff

This skill does NOT handle the following:

1. Executing any remediation actions (scale, delete, restart, cordon, drain, traffic change)
2. Root cause analysis of why Pods are unhealthy (use `huawei-cloud-cce-root-cause-analyzer`)
3. Change correlation analysis (use `huawei-cloud-cce-change-impact-analyzer`)
4. Creating, modifying, or deleting CCE resources

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

**Permission Failure Handling**:
1. When any command fails due to permission errors, display required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation

---

## Core Tools

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`.

**Primary Analysis Action:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_dependency_impact_analyze` | region, cluster_id | Primary action: collects Pod/Service/Ingress/Node snapshots, maps Service selectors and Ingress backends, computes propagation paths and impact scoring, produces a complete Markdown impact report |

**Supporting Discovery Actions:**

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_get_cce_pods` | region, cluster_id | List Pods in the cluster |
| `huawei_get_cce_services` | region, cluster_id | List Services in the cluster |
| `huawei_get_cce_ingresses` | region, cluster_id | List Ingresses in the cluster |
| `huawei_get_kubernetes_nodes` | region, cluster_id | List Kubernetes Nodes in the cluster |

**Cross-Skill Diagnosis Actions:**

| Action | Required Parameters | Cross-Skill Reference | Description |
|--------|---------------------|----------------------|-------------|
| `huawei_workload_rollout_diagnose` | region, cluster_id, namespace, kind, name | `huawei-cloud-cce-workload-failure-diagnoser` | Diagnose workload rollout failures |
| `huawei_network_failure_diagnose` | region, cluster_id | `huawei-cloud-cce-network-failure-diagnoser` | Network connectivity diagnosis |
| `huawei_change_impact_analyze` | region, cluster_id | `huawei-cloud-cce-change-impact-analyzer` | Change-impact correlation analysis |

---

## Parameter Reference

**Common Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| region | Yes | Huawei Cloud region, e.g., cn-north-4 |
| cluster_id | Yes | CCE cluster ID |
| namespace | No | Kubernetes namespace (narrows scope) |
| target_name | No | Target workload/app/service name for scope narrowing |
| label_selector | No | Label selector for target Pod matching |

**Optional Parameters (passed via `--params` JSON):**

| Parameter | Description |
|-----------|-------------|
| ak | Override AK (uses HW_ACCESS_KEY by default) |
| sk | Override SK (uses HW_SECRET_KEY by default) |
| project_id | Override project ID (auto-obtained via IAM when not set) |
| hours | Metric/query time range in hours (default 1) |

---

## Workflow

1. **Scope**: Confirm region, cluster_id, namespace, target_name/workload_name/app_name/name, or label_selector
2. **Snapshot**: Collect Pods, Services, Ingresses, and Nodes from current cluster state via `huawei_dependency_impact_analyze`
3. **Target matching**: Find target Pods by label selector first, then by Pod name prefix, ownerReference, or label value matching target name
4. **Upstream mapping**: Find Services whose selectors match target Pod labels; find Ingress rules/default backends that point to those Services
5. **Propagation paths**: Model external traffic as Ingress → Service → Pods and cluster traffic as Service DNS → Pods
6. **Impact scoring**: Combine target Pod readiness, Service exposure, Ingress exposure, and propagation path count to determine risk level
7. **Evidence and limits**: Output Pod health, Service selector, Ingress backend, path table, Mermaid topology, and confidence limitations
8. **Handoff**: If target is unhealthy, pass root cause to `huawei-cloud-cce-root-cause-analyzer`; if remediation is needed, pass action to `huawei-cloud-cce-auto-remediation-runner`; if change correlation is needed, pass to `huawei-cloud-cce-change-impact-analyzer`

---

## Output Format

See `references/output-schema.md` for the complete output schema.

```json
{
  "success": true,
  "analysis_trace_id": "DIA-...",
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "default",
    "target_name": "api",
    "match_reason": "target_name=api"
  },
  "summary": {
    "risk_level": "High | Medium | Low | Unknown",
    "risk_score": 88,
    "risk_reason": "target pods unavailable and exposed by Service/Ingress",
    "pod_health": {
      "total": 2,
      "ready": 0,
      "unready": 2,
      "availability": "unavailable"
    },
    "service_count": 1,
    "ingress_count": 1,
    "path_count": 2
  },
  "target": {
    "pods": [],
    "services": [],
    "ingresses": []
  },
  "propagation_paths": [],
  "report_markdown": "# CCE Dependency Impact Analysis Report...",
  "report_file": "optional"
}
```

---

## Verification

1. Run the environment check script to confirm dependencies and credentials are available
2. Use `huawei_dependency_impact_analyze` on a known healthy cluster to verify it returns `success: true` with correct topology mapping
3. Verify that Service selectors correctly match Pod labels in the propagation paths
4. Verify that Ingress backends correctly point to Services in the propagation paths
5. Confirm that Pod health counts (total/ready/unready) match actual cluster state
6. Verify that `risk_level` and `risk_score` align with Pod readiness and Service/Ingress exposure
7. Confirm that confidence limitations are explicitly stated for inferred dependencies

---

## Best Practices

1. Always start with `huawei_dependency_impact_analyze` for comprehensive topology analysis; use individual discovery actions only for supplementary evidence
2. For service unavailability, trace Service selector → Ingress backend → Pod Ready → Node distribution propagation paths
3. Treat downstream consumers as inferred unless backed by APM, service mesh, access logs, or explicit dependency metadata
4. Static Kubernetes topology can prove possible propagation paths, not real request volume or business criticality
5. Clearly label inferred dependencies with confidence limitations
6. If impact appears to stem from recent changes, hand off to `huawei-cloud-cce-change-impact-analyzer`
7. If target Pods are unhealthy and root cause is needed, hand off to `huawei-cloud-cce-root-cause-analyzer`
8. If remediation is needed, hand off to `huawei-cloud-cce-auto-remediation-runner` with preview-first confirmation

---

## Reference Documents

- Workflow pipeline and scoring rules: `references/workflow.md`
- Output structure specification: `references/output-schema.md`
- Read-only boundaries and handoff rules: `references/risk-rules.md`
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

---

## Notes

1. This skill is read-only topology analysis and report generation only; no write, scale, delete, cordon, drain, reboot, or traffic change operations
2. Do not output the values of HW_ACCESS_KEY, HW_SECRET_KEY, HW_SECURITY_TOKEN, or other environment variables
3. All scripts must be executed via `skill action=exec`; do not run them directly in a shell
4. Any remediation action must be handed off to `huawei-cloud-cce-auto-remediation-runner`; this skill never executes remediation
5. The environment check script must be run before any analysis action
6. When using temporary AK/SK, HW_SECURITY_TOKEN must be set

---

## Common Pitfalls

1. **Treating inferred dependencies as confirmed** — Downstream consumers inferred from Kubernetes topology are not proven by real traffic data. Always label inferred paths with confidence limitations
2. **Skipping environment check** — The environment check must be run first; missing dependencies or invalid credentials will cause analysis failures
3. **Concluding impact from topology alone** — Static topology shows possible propagation paths, not actual request volume or business criticality. Correlate with AOM metrics or APM data when available
4. **Not handing off to huawei-cloud-cce-root-cause-analyzer** — When target Pods are unhealthy, this skill identifies impact scope but not root cause. Hand off to `huawei-cloud-cce-root-cause-analyzer` for deeper diagnosis
5. **Attempting remediation from this skill** — All recovery actions must be handed off to `huawei-cloud-cce-auto-remediation-runner` with preview-first confirmation; this skill never executes mutations
6. **Ignoring change correlation** — If impact appears linked to recent deployments, config updates, or policy changes, use `huawei-cloud-cce-change-impact-analyzer` to build the "change before failure" causal chain
7. **Assuming single-direction propagation** — Dependency impact can propagate bidirectionally (upstream failure affects downstream, downstream back-pressure affects upstream); analyze both directions
8. **Missing kube-system dependencies** — CoreDNS, kube-proxy, and Ingress controller dependencies affect all services; include them in blast radius analysis