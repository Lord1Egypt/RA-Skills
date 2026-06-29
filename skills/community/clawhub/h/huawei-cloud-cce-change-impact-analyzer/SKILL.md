---
id: huawei-cloud-cce-change-impact-analyzer
name: huawei-cloud-cce-change-impact-analyzer
description: |
  Huawei Cloud CCE change impact analysis skill that converts "what changed before the incident" into provable causal attribution.
  Use this skill when a CCE incident may be caused by recent changes, including workload releases, ConfigMap/Secret updates, Service/Ingress/Gateway route changes, NetworkPolicy/RBAC/security policy changes, node taints or infrastructure changes, and the user needs a complete Markdown report with timeline, evidence matrix, blast radius, risk score, and conclusion.
  Trigger: "change impact analysis", "变更影响分析", "change risk", "变更风险", "deployment impact", "发布影响", "config change", "配置变更", "network policy change", "网络策略变更", "node taint change", "节点污点变更", "blast radius", "爆炸半径", "recent changes", "近期变更", "audit log correlation", "审计日志关联"
tags: [cce, change-impact, risk-assessment, preview]
---

# CCE Change Impact Analyzer

> **⚠️ Execution Method (Must Read): This skill executes diagnosis via local Python scripts using the `scripts/huawei-cloud.py` dispatcher. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - All actions are dispatched through `scripts/huawei-cloud.py` with `--action <action_name>` and `--params <json_params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them; do not run them directly in a shell**
> - For action names and parameters, see the Core Tools section below
> - **Do not attempt hcloud, kubectl, curl IAM, or other CLI/API methods. This skill does not depend on these tools**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md resides**

## Overview

This skill turns "what changed before the incident" into provable causal attribution. It ingests audit logs, K8s historical events, AOM active+history alarms, and current resource topology snapshots; filters noise; maps core changes to blast radius; scores risk by sensitivity, topology scope, security boundary span, temporal proximity to fault, and event/alarm correlation; then outputs a complete Markdown report with investigation steps, core change timeline, evidence matrix, blast radius, Top N risk alerts, conclusion, and data gaps.

This skill is applicable to the following scenarios:

1. Incidents where recent workload releases, config updates, or network/security policy changes may be the cause
2. CoreDNS, kube-proxy, or cluster plugin configuration changes causing business-wide failures
3. Node taint, cordon/drain, node pool resize, or cluster upgrade triggering Pod Pending, Evicted, or NotReady
4. NetworkPolicy/RBAC changes causing connection timeouts, 403 errors, DNS anomalies, or cross-namespace access failures
5. Service/Ingress/Gateway route changes causing traffic routing failures
6. Correlating audit trail changes with observed failures and alarm timelines

This skill does NOT handle the following:

1. Executing any remediation actions (rollback, scale, delete, drain, reboot, modify NetworkPolicy/RBAC/Security Group/VPC ACL)
2. Making causal conclusions from object updates alone without temporal or response-signal correlation
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
| cce:nodepool:list | List node pools | List node pools |
| aom:*:get | Read AOM | Query AOM metrics and alarms |
| aom:alarmRule:list | List alarm rules | Query alarm rules |
| aom:event:list | List events | Query AOM alarm events |

**Permission Failure Handling**:
1. When any command fails due to permission errors, display required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation

---

## Core Tools

All actions are dispatched through `scripts/huawei-cloud.py` using `skill action=exec`.

### Primary Change Impact Analysis

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_change_impact_analyze` | region, cluster_id | Primary comprehensive action: orchestrates audit log ingestion, K8s event correlation, AOM alarm correlation, resource snapshot collection, noise filtering, blast radius modeling, and risk scoring into a unified change impact report with Top N risk alerts |

### Audit and Event Collection

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_query_cce_audit_logs` | region, cluster_id | Query CCE Kubernetes audit logs for create/update/patch/delete operations with actor, verb, resource, namespace, name, requestURI, statusCode |
| `huawei_query_k8s_events_from_lts` | region, cluster_id | Query historical K8s Events from LTS (overcomes the K8s API short event window) |
| `huawei_get_cce_events` | region, cluster_id | List current Kubernetes Events when LTS is unavailable |

### Alarm Correlation

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_analyze_aom_alarms` | region, cluster_id | Analyze AOM active + history alarm patterns and correlation across resources |

### Domain Drill-Down (Read-Only)

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_workload_rollout_diagnose` | region, cluster_id, namespace, kind, name | Drill down when changes point to Deployment/StatefulSet/DaemonSet rollout failures (cross-skill: `huawei-cloud-cce-workload-failure-diagnoser`) |
| `huawei_network_failure_diagnose` | region, cluster_id | Drill down when changes point to Service/Ingress/NetworkPolicy/ELB connectivity failures (cross-skill: `huawei-cloud-cce-network-failure-diagnoser`) |
| `huawei_node_failure_diagnose` | region, cluster_id | Drill down when changes point to Node taint, NotReady, scheduling, or resource pressure (cross-skill: `huawei-cloud-cce-node-failure-diagnoser`) |

### Current Topology Snapshots

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_get_cce_pods` | region, cluster_id | List current Pod status for blast radius modeling |
| `huawei_get_cce_deployments` | region, cluster_id | List current Deployment status |
| `huawei_get_cce_services` | region, cluster_id | List current Service selector/ports for impact mapping |
| `huawei_get_cce_ingresses` | region, cluster_id | List current Ingress rules/backends for impact mapping |
| `huawei_get_kubernetes_nodes` | region, cluster_id | List current Node status for taint/impact mapping |
| `huawei_list_cce_configmaps` | region, cluster_id | List current ConfigMap objects (identify CoreDNS, kube-proxy, business configs) |
| `huawei_list_cce_secrets` | region, cluster_id | List current Secret objects |
| `huawei_list_cce_nodepools` | region, cluster_id | List current NodePool status for infrastructure change context |

### Cloud Network Snapshots

| Action | Required Parameters | Description |
|--------|---------------------|-------------|
| `huawei_list_security_groups` | region | List current Security Group rules for cloud network context |
| `huawei_list_vpc_acls` | region | List current VPC ACL rules for cloud network context |

---

## Parameter Reference

**Common Parameters:**

| Parameter | Required | Description |
|-----------|----------|-------------|
| region | Yes | Huawei Cloud region, e.g., cn-north-4 |
| cluster_id | Yes | CCE cluster ID |

**Optional Parameters (passed via `--params` JSON):**

| Parameter | Description |
|-----------|-------------|
| hours | Analysis window in hours (default 1) |
| start_time | Analysis window start (YYYY-MM-DD HH:MM:SS), alternative to hours |
| end_time | Analysis window end (YYYY-MM-DD HH:MM:SS), alternative to hours |
| namespace | Narrow scope to a namespace, but do not exclude kube-system/CoreDNS global changes |
| target_name | Target object name for scope narrowing |
| workload_name | Workload name for scope narrowing |
| app_name | Application name for scope narrowing |
| fault_time | Incident time point for temporal proximity scoring |
| incident_time | Alternative to fault_time |
| log_group_id | Audit log group ID (manual fallback when auto-discovery fails) |
| log_stream_id | Audit log stream ID (manual fallback when auto-discovery fails) |
| include_audit | Enable/disable audit log collection (default true) |
| include_k8s_events | Enable/disable K8s event collection (default true) |
| include_aom | Enable/disable AOM alarm collection (default true) |
| include_snapshots | Enable/disable resource snapshot collection (default true) |
| top_n | Number of top risk alerts in report (default 3) |
| output_file | Path to write the Markdown report file |
| ak | Override AK (uses HW_ACCESS_KEY by default) |
| sk | Override SK (uses HW_SECRET_KEY by default) |
| project_id | Override project ID (auto-obtained via IAM when not set) |

---

## Output Format

### Primary: `huawei_change_impact_analyze`

Returns structured JSON with embedded `report_markdown`. See `references/output-schema.md` for full schema.

```json
{
  "success": true,
  "analysis_trace_id": "CIA-yyyymmddHHMMSS-xxxxxxxx",
  "analysis_window": {
    "start_time": "YYYY-MM-DD HH:MM:SS",
    "end_time": "YYYY-MM-DD HH:MM:SS",
    "hours": 1
  },
  "scope": {
    "region": "cn-north-4",
    "cluster_id": "cluster-id",
    "namespace": "optional",
    "target_name": "optional"
  },
  "summary": {
    "core_change_count": 3,
    "top_risk_count": 3,
    "data_sources": {
      "CCE Audit Logs": "success",
      "K8s Historical Events": "success",
      "AOM Alarms": "success",
      "Current Resource Snapshots": "success"
    }
  },
  "top_changes": [
    {
      "time": "YYYY-MM-DD HH:MM:SS",
      "verb": "patch",
      "resource": "configmaps",
      "namespace": "kube-system",
      "name": "coredns",
      "object_key": "kube-system/coredns",
      "category": "global_config_change",
      "title": "Cluster core configuration change",
      "actor": "user or serviceAccount",
      "semantic_fields": ["data", "Corefile"],
      "blast_radius": "cluster-wide",
      "impacted_entities": {
        "pods": [],
        "services": ["kube-system/kube-dns"],
        "ingresses": [],
        "nodes": ["node-a"]
      },
      "risk_score": 96,
      "risk_level": "Critical",
      "confidence": "high",
      "risk_reasons": [],
      "evidence": []
    }
  ],
  "changes": [],
  "report_markdown": "# CCE Change Impact Analysis Report\n...",
  "report_file": "/optional/path/report.md",
  "capture_metadata": {}
}
```

---

## Verification

1. Run the environment check script to confirm dependencies and credentials are available
2. Use `huawei_change_impact_analyze` on a known stable cluster to verify it returns `success: true` with zero or low-confidence core changes
3. Use `huawei_change_impact_analyze` on a cluster with known recent changes to verify Top N risk alerts are accurately identified
4. Verify that noise filtering correctly excludes HPA replica-only updates, controller status writes, Lease/Token/status subresource writes
5. Verify that CoreDNS/kube-proxy/kube-system changes are always included regardless of namespace scope
6. Verify that blast radius mapping correctly traces Service selector → Pod → Ingress → Node propagation
7. Confirm that low-confidence conclusions are clearly labeled with data gaps

---

## Best Practices

1. Always start with `huawei_change_impact_analyze` for comprehensive change correlation; drill down into domain diagnoser actions only when specific evidence requires deeper analysis
2. Find changes first, then map impact, then align with alarms/events/fault time — do not conclude root cause from object updates alone
3. CoreDNS, kube-proxy, network plugin, and Ingress controller config changes in `kube-system` must always be included in business fault analysis regardless of target namespace scope
4. Deployment HPA-only `replicas` adjustments are noise; image, startup args, probe, resource spec, environment variable, and ConfigMap/Secret reference changes are core changes
5. NetworkPolicy/RBAC changes must be correlated with connection timeouts, 403, DNS anomalies, and cross-namespace access failures
6. Node taint, cordon/drain, node pool resize, and cluster upgrade changes must be correlated with Pod Pending, Evicted, NotReady, and node events
7. All remediation actions must be output as recommendations only and handed off to `huawei-cloud-cce-auto-remediation-runner`
8. Clearly label low-confidence conclusions with required supplementary data; never present speculation as fact

---

## Reference Documents

- Four-stage pipeline and risk scoring rules: `references/workflow.md`
- Reusable capabilities, gaps, and suggested atomic actions: `references/capability-map.md`
- Output field specification and Markdown template: `references/output-schema.md`
- Read-only boundaries and remediation handoff rules: `references/risk-rules.md`
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)

---

## Notes

1. This skill is read-only analysis and report generation only; no modification of workloads, rollback, ConfigMap/Secret changes, Security Group/ACL/NetworkPolicy/RBAC adjustments, or node cordon/drain/reboot operations
2. Do not output the values of HW_ACCESS_KEY, HW_SECRET_KEY, HW_SECURITY_TOKEN, or other environment variables
3. All scripts must be executed via `skill action=exec`; do not run them directly in a shell
4. Any remediation action must be handed off to `huawei-cloud-cce-auto-remediation-runner`; this skill never executes remediation
5. The environment check script must be run before any analysis action
6. When using temporary AK/SK, HW_SECURITY_TOKEN must be set
7. Cross-skill references: remediation → `huawei-cloud-cce-auto-remediation-runner`; comprehensive root cause → `huawei-cloud-cce-root-cause-analyzer`; workload diagnosis → `huawei-cloud-cce-workload-failure-diagnoser`; network diagnosis → `huawei-cloud-cce-network-failure-diagnoser`; node diagnosis → `huawei-cloud-cce-node-failure-diagnoser`

---

## Common Pitfalls

1. **Concluding root cause from object updates alone** — Always require temporal proximity, event/alarm response, and topology impact evidence; an object update without correlation is insufficient evidence
2. **Excluding kube-system changes when scoped to a namespace** — CoreDNS, kube-proxy, and cluster plugin changes are global even when the target namespace is different; always include them
3. **Treating HPA replica updates as core changes** — HPA-only `replicas` modifications are noise; only image, probe, resource, env, config reference changes are core
4. **Not correlating NetworkPolicy/RBAC with connectivity symptoms** — NetworkPolicy/RBAC changes must be cross-referenced with connection timeout, 403, DNS anomaly, and cross-namespace access failure events
5. **Attempting remediation actions from this skill** — All changes must be handed off to `huawei-cloud-cce-auto-remediation-runner`; this skill only outputs recommendations
6. **Failing to label low-confidence conclusions** — When evidence is insufficient, write "insufficient evidence" explicitly with data gaps; never present guesses as conclusions
7. **Ignoring controller and platform noise** — Lease, Token, status subresource, Node status patch, scheduler binding, and CCE platform-managed RBAC updates must all be filtered out; they are control-plane closed-loop operations, not user changes
8. **Not building a fault timeline** — Establish user-perceived fault time, alarm trigger time, Kubernetes event time, and change time before scoring risk