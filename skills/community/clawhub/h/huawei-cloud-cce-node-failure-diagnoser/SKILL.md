---
id: huawei-cloud-cce-node-failure-diagnoser
name: huawei-cloud-cce-node-failure-diagnoser
description: |
  Huawei Cloud CCE Node failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose CCE node NotReady, node resource pressure, node failure events, (2) analyze node disk/memory/CPU pressure, (3) check node status and conditions, (4) view node metrics and events.
  Trigger: user mentions "node failure", "节点故障", "NodeNotReady", "节点 NotReady", "node pressure", "节点压力", "node disk pressure", "磁盘压力", "node eviction", "节点驱逐", "节点异常", "节点诊断", "CCE node", "CCE 节点", "节点状态"
tags: [cce, node-diagnosis, kubernetes, fault-diagnosis]
---

# Huawei Cloud CCE Node Failure Diagnoser

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill diagnoses CCE/Kubernetes node failures and produces a complete Markdown diagnosis report. It uses the local Python dispatcher (`scripts/huawei-cloud.py`) to call the Huawei Cloud Python SDK and Kubernetes client APIs, collecting node status, kube-node-lease evidence, events, pod symptoms, and AOM metrics.

The skill covers: node NotReady, disk/memory/CPU pressure, network abnormalities, kubelet/CRI failures, NPD events, and workload impact on the affected node.

### Related Skills

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod-level failure diagnosis |
| `huawei-cloud-cce-network-failure-diagnoser` | Network failure diagnosis |
| `huawei-cloud-cce-storage-failure-diagnoser` | Storage failure diagnosis |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (cordon, drain, reboot) |
| `huawei-cloud-cce-metric-analyzer` | Metric trend analysis |
| `huawei-cloud-cce-observability-context-builder` | Observability context enrichment |

### Capabilities

1. One-shot node failure diagnosis with structured evidence and Markdown report (`huawei_node_failure_diagnose`)
2. Kubernetes node status and conditions collection (`huawei_get_kubernetes_nodes`)
3. Node/Pod event timeline retrieval (`huawei_get_cce_events`)
4. Pod phase/reason/state aggregation per node (`huawei_get_cce_pods`)
5. Node and Pod AOM metric queries (`huawei_get_cce_node_metrics`, `huawei_get_cce_pod_metrics_topN`)
6. Node inspection items (status, resource, vulnerability) (`huawei_node_status_inspection`, `huawei_node_resource_inspection`, `huawei_node_vul_inspection`)
7. Security group and HSS vulnerability correlation (`huawei_list_security_groups`, `huawei_hss_list_hosts`, `huawei_hss_list_host_vuls_all`)

### Typical Use Cases

- Diagnose a CCE node that transitioned to NotReady state
- Investigate node disk or memory pressure conditions
- Analyze kubelet or container runtime failures on a node
- Check node network connectivity issues (CNI sandbox failures)
- Assess pod impact when a node becomes unhealthy
- Review NPD events and node-level security findings

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

### IAM Permissions

| Permission | Service | Required For |
|------------|---------|---------------|
| CCE cluster/node read | CCE | `huawei_list_cce_nodes`, `huawei_get_cce_nodes`, `huawei_node_diagnose` |
| Kubernetes API read | CCE (kubeconfig) | `huawei_get_kubernetes_nodes`, `huawei_node_failure_diagnose` |
| AOM metrics read | AOM | `huawei_get_cce_node_metrics`, `huawei_get_cce_pod_metrics_topN` |
| CES alarm read | CES | `huawei_get_cce_events` |
| HSS host/vul read | HSS | `huawei_hss_list_hosts`, `huawei_hss_list_host_vuls_all` |
| VPC/SG read | VPC | `huawei_list_security_groups`, `huawei_list_vpc_acls` |

---

## Core Tools

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### Primary Diagnosis Action

```bash
python3 scripts/huawei-cloud.py huawei_node_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  node_name=<node_name> lease_timeout_seconds=40 \
  event_limit=500 hours=1 include_metrics=true
```

Returns structured evidence + `report_markdown` (complete Markdown diagnosis report).

### Evidence Collection Actions

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_get_kubernetes_nodes` | `region`, `cluster_id` | Query v1.Node Ready/conditions status |
| `huawei_get_cce_events` | `region`, `cluster_id` | Retrieve Kubernetes events |
| `huawei_get_cce_pods` | `region`, `cluster_id` | List Pod phase/reason/lastState |
| `huawei_get_cce_node_metrics` | `region`, `cluster_id`, `node_ip` | Query node CPU/memory/disk metrics |
| `huawei_get_cce_node_metrics_topN` | `region`, `cluster_id` | Top-N node metrics |
| `huawei_get_cce_pod_metrics_topN` | `region`, `cluster_id` | Top-N pod metrics (supports `node_ip` filter) |

### Inspection Actions

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_node_status_inspection` | `region`, `cluster_id` | Node status health inspection |
| `huawei_node_resource_inspection` | `region`, `cluster_id` | Node resource utilization inspection |
| `huawei_node_vul_inspection` | `region`, `cluster_id` | Node vulnerability inspection |

### Security Correlation Actions

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_list_security_groups` | `region` | List VPC security groups |
| `huawei_list_vpc_acls` | `region` | List VPC network ACLs |
| `huawei_hss_list_hosts` | `region` | List HSS host security status |
| `huawei_hss_list_host_vuls_all` | `region`, `host_id` | List all vulnerabilities for a host |

---

## Parameter Reference

### `huawei_node_failure_diagnose`

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | - | CCE cluster ID |
| `node_name` | No* | - | Target node name (one of node_name or node_ip required) |
| `node_ip` | No* | - | Target node internal IP (one of node_name or node_ip required) |
| `lease_timeout_seconds` | No | 40 | Kube-node-lease stale threshold in seconds |
| `event_limit` | No | 500 | Maximum events to retrieve |
| `hours` | No | 1 | Metric lookback window in hours |
| `include_metrics` | No | true | Whether to include AOM metrics |

*At least one of `node_name` or `node_ip` must be provided. If both are omitted, the action returns an error.

### Common Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `region` | Yes | Huawei Cloud region |
| `cluster_id` | Yes (most actions) | CCE cluster ID |
| `node_ip` | Required for `huawei_get_cce_node_metrics` | Node internal IP |
| `top_n` | No | Number of top results (default 10) |
| `hours` | No | Metric lookback hours (default 1) |

---

## Output Format

The primary action `huawei_node_failure_diagnose` returns structured evidence and a Markdown report. See `references/output-schema.md` for the full JSON response schema.

Key output fields:

| Field | Description |
|-------|-------------|
| `success` | Whether the diagnosis completed successfully |
| `node` | Node name, IP, Ready status, conditions |
| `lease` | kube-node-lease renew time, stale status, delay seconds |
| `liveness` | Control plane liveness case (A/B/C/D) and conclusion |
| `root_category` | Root cause category (ControlPlaneDisconnected, MemoryPressure, DiskPressure, Network, Kubelet, NotReady, Healthy) |
| `confidence` | Confidence level (High/Medium/Low) |
| `evidence` | List of evidence items with category, severity, signal, source, detail |
| `pod_summary` | Pod phase counts and symptomatic pod list |
| `health_items` | Node health check items with status |
| `report_markdown` | Complete Markdown diagnosis report (use as final output) |

When `report_markdown` is present, use it as the final report body. You may add clarifications the user requests, but do not discard evidence tables.

---

## Verification

1. Run the dispatcher with a known cluster and node to confirm connectivity:
   ```bash
   python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes region=cn-north-4 cluster_id=<cluster_id>
   ```
2. Execute `huawei_node_failure_diagnose` on a healthy node; expect `root_category=Healthy` and `confidence=High`
3. Verify `report_markdown` contains all required sections (see `references/output-schema.md`)
4. Compare node conditions in the output with the CCE console

---

## Best Practices

1. Always call `huawei_node_failure_diagnose` first; use manual fallback actions only if the primary action fails
2. When `Ready=Unknown` and lease is stale, conclude "control plane disconnected from node" rather than prematurely attributing to kubelet or network alone
3. When pressure conditions are `Unknown` with `NodeStatusUnknown` reason, label them "indeterminate" — do not mark as "normal"
4. Correlate Event signals with Pod symptoms before forming conclusions; evidence strength determines confidence level
5. Include security group and HSS checks only when network or vulnerability hypotheses are strong
6. Do not single-point metric peaks as root cause; validate with trend data

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/workflow.md` | Diagnosis triage flow, evidence rules, and fallback workflow |
| `references/output-schema.md` | Output JSON schema and required Markdown report sections |
| `references/risk-rules.md` | Risk boundary rules: allowed read actions, prohibited write actions |
| [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) | SDK reference |
| [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) | API interactive explorer |

---

## Notes

1. This skill is **read-only diagnosis only** — it does not cordon, uncordon, drain, reboot, or modify vulnerability status
2. When remediation actions are needed, hand off to `huawei-cloud-cce-auto-remediation-runner` and require user confirmation
3. Never expose or log AK/SK or environment variable values
4. All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI or direct API calls
5. If the primary action `huawei_node_failure_diagnose` fails, follow the manual fallback workflow in `references/workflow.md`

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Concluding "kubelet failure" when `Ready=Unknown` + lease stale | Conclude "control plane disconnected from node (network or kubelet/CRI heartbeat interrupted, requires node-side verification)" |
| Marking `Unknown` pressure conditions as "normal" | Label as "indeterminate — no independent evidence available" |
| Using a single metric spike as root cause | Validate with trend data over time; use `hours` parameter for lookback |
| Skipping event/pod correlation | Always cross-reference Event signals with Pod symptoms before forming conclusions |
| Executing cordon/drain/reboot directly | This skill does not perform write actions; hand off to `huawei-cloud-cce-auto-remediation-runner` |
| Ignoring CNI sandbox failures in Pod events | `FailedCreatePodSandBox` + CNI error patterns are strong network abnormality evidence |
| Not checking kube-node-lease when node is NotReady | Lease staleness is critical evidence for control plane connectivity |