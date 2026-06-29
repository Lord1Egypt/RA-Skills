---
id: huawei-cloud-cce-autoscaling-diagnoser
name: huawei-cloud-cce-autoscaling-diagnoser
description: |
  Huawei Cloud CCE autoscaling failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose CCE autoscaling failures across HPA not increasing Pod replicas, CCE elastic engine or Cluster Autoscaler not adding/removing nodes, missing metrics, missing CPU/memory requests, maxReplicas or max_nodes limits, Pending Pods, scheduling constraints, subnet IP exhaustion, ECS quota, or IAM agency permission issues, (2) perform HPA-to-CA cascade diagnosis linking workload-level and node-level scaling failures, (3) analyze CA Pod logs for Cluster Autoscaler signals (NoExpansionOptions, MaxNodeGroupSizeReached, QuotaExceeded, SubnetIPExhausted, IAM denied), (4) generate a complete Markdown diagnosis report with process, evidence, conclusion, confidence, and recommendations.
  Trigger: user mentions "autoscaling diagnosis", "弹性伸缩诊断", "HPA diagnosis", "HPA 诊断", "scaling failure", "伸缩失败", "HPA not scaling", "HPA 不伸缩", "replica scaling", "副本伸缩", "autoscaling issue", "伸缩问题"
tags: [cce, autoscaling, hpa, diagnosis]
---

# Huawei Cloud CCE Autoscaling Diagnoser

> **⚠️ Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill diagnoses CCE autoscaling link failures across two closed-loop layers: (1) whether HPA increases workload replica count from N to N+1, and (2) whether CCE elastic engine / Cluster Autoscaler increases node count from M to M+1 after resource-insufficient Pending Pods appear. It outputs a complete Markdown diagnosis report with process, evidence, root cause conclusion, confidence, data gaps, and recommendations.

**Architecture**: Python dispatcher (`scripts/huawei-cloud.py`) → Huawei Cloud Python SDK + Kubernetes client → HPA/CA/Addon/NodePool/Pod/Events/Metrics → Gateway intent routing → Path A/B/C diagnosis → Structured evidence + Markdown report

**Related Skills**:

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod runtime failure diagnosis (CrashLoopBackOff, OOMKilled, Pending) |
| `huawei-cloud-cce-node-failure-diagnoser` | Node-level failure diagnosis (NotReady, disk/memory pressure) |
| `huawei-cloud-cce-workload-failure-diagnoser` | Workload rollout failure diagnosis |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (HPA config, nodepool resize) |
| `huawei-cloud-cce-root-cause-analyzer` | Cross-resource root cause correlation |
| `huawei-cloud-cce-alarm-correlation-engine` | Alarm correlation and diagnosis triggering |
| `huawei-cloud-cce-capacity-trend-forecaster` | Capacity trend and HPA coverage analysis |
| `huawei-cloud-cce-cost-optimization-advisor` | Resource governance and cost optimization |

**Capabilities**:

1. One-shot autoscaling diagnosis with Gateway intent routing, capability discovery, and Path A/B/C evidence collection (`huawei_autoscaling_diagnose`)
2. HPA object inspection: spec, currentReplicas, desiredReplicas, minReplicas, maxReplicas, conditions, metrics (`huawei_list_cce_hpas`)
3. CCE addon and nodepool autoscaling discovery (`huawei_list_cce_addons`, `huawei_list_cce_nodepools`)
4. CA Pod log analysis: automatic discovery of kube-system autoscaler Pods, log retrieval, and 16 diagnostic signal pattern matching
5. Pending Pod and scheduling constraint analysis (`huawei_get_cce_pods`, `huawei_get_cce_events`)
6. AOM/Prometheus custom metric evidence (`huawei_get_aom_metrics`)
7. Complete Markdown report generation with evidence, conclusion, confidence, and recommendations

**Typical Use Cases**:

- "HPA is not scaling my Deployment, what's wrong?"
- "Why isn't the Cluster Autoscaler adding nodes when Pods are Pending?"
- "My workload replicas aren't increasing despite high CPU usage"
- "Diagnose why autoscaling is not working in my CCE cluster"
- "HPA shows desiredReplicas equals currentReplicas, why no scaling?"
- "Pods are Pending with Insufficient cpu/memory but no new nodes appear"
- "Check if autoscaling is properly configured for my workload"
- "Analyze CA logs for node scaling failure signals"

## Prerequisites

### 1. Python Requirements (MANDATORY)

- Python >= 3.6 installed
- Required packages: `huaweicloudsdkcore`, `huaweicloudsdkcce`, `huaweicloudsdkaom`, `kubernetes`
- Verify: `python3 --version`
- Install packages: `pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom kubernetes`

### 2. Credential Configuration

- Valid Huawei Cloud credentials (AK/SK mode)
- **Security Rules**:
  - 🚫 Never expose AK/SK values in code, conversation, or commands
  - 🚫 Never use `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials
  - 🚫 Never write credentials to files, logs, or responses
  - ✅ Use environment variables: `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION`
  - ✅ Credentials exist only in the current request call stack and are released after each invocation
  - ✅ Prefer IAM users over root account for cloud operations

**Configuration Method** (Environment Variables Only):

```bash
export HUAWEI_AK=<your-ak>
export HUAWEI_SK=<your-sk>
export HUAWEI_REGION=cn-north-4
```

**Additional Variables**:

| Variable | Required | Description |
|----------|----------|-------------|
| `HUAWEI_AK` | Yes | Huawei Cloud Access Key |
| `HUAWEI_SK` | Yes | Huawei Cloud Secret Key |
| `HUAWEI_REGION` | No | Default region (overrides `region` param if set) |
| `HUAWEI_PROJECT_ID` | No | Project ID (auto-obtained via IAM API when not set) |
| `HUAWEI_SECURITY_TOKEN` | No | Required when using temporary AK/SK |

### 3. IAM Permission Requirements

| API Action | Service | Purpose |
|------------|---------|---------|
| CCE cluster read | CCE | `huawei_list_cce_clusters`, `huawei_list_cce_nodepools` |
| CCE addon read | CCE | `huawei_list_cce_addons`, `huawei_get_cce_addon_detail` |
| CCE HPA read | CCE (kubeconfig) | `huawei_list_cce_hpas` |
| CCE workload read | CCE (kubeconfig) | `huawei_get_cce_deployments`, `huawei_list_cce_statefulsets` |
| CCE Pod read | CCE (kubeconfig) | `huawei_get_cce_pods` |
| CCE Pod logs | CCE (kubeconfig) | `huawei_get_pod_logs` |
| CCE Events read | CCE (kubeconfig) | `huawei_get_cce_events` |
| AOM metrics read | AOM | `huawei_get_aom_metrics`, `huawei_get_cce_pod_metrics_topN`, `huawei_get_cce_node_metrics_topN` |

**Permission Failure Handling**:

1. When any action fails due to IAM permission errors, display the required permission list
2. Guide the user to create custom policies in the IAM console for Huawei Cloud permissions
3. Pause execution and wait for user confirmation that permissions have been granted
4. Retry the failed action

## Core Commands

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### 1. Primary Diagnosis Action

```bash
python3 scripts/huawei-cloud.py huawei_autoscaling_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  namespace=default workload_name=my-app workload_type=Deployment \
  question="Why isn't HPA scaling my workload?"
```

Returns structured evidence + `report_markdown` (complete Markdown diagnosis report). When `report_markdown` is present, use it as the final report body. You may add clarifications the user requests, but do not discard evidence tables.

### 2. Evidence Collection Actions (Read-Only)

| Action | Required Params | Description |
|--------|----------------|-------------|
| `huawei_list_cce_hpas` | `region`, `cluster_id` | List HPA specs, current/desired replicas, conditions, metrics |
| `huawei_list_cce_addons` | `region`, `cluster_id` | Identify CCE elastic engine, metrics/AOM/Prometheus addons |
| `huawei_get_cce_addon_detail` | `region`, `cluster_id`, `addon_id` | Get addon detail (version, status) |
| `huawei_list_cce_nodepools` | `region`, `cluster_id` | List nodepools: autoscaling enable, min/max, current node count |
| `huawei_get_cce_pods` | `region`, `cluster_id` | List Pod phase, owner, container state, resources.requests/limits, annotations |
| `huawei_get_cce_deployments` | `region`, `cluster_id` | Read Deployment desired/current/ready replicas |
| `huawei_list_cce_statefulsets` | `region`, `cluster_id` | Read StatefulSet desired/current/ready replicas |
| `huawei_get_cce_events` | `region`, `cluster_id` | Read HPA, Pod, Scheduler events (FailedScheduling, FailedGetResourceMetric) |
| `huawei_get_cce_pod_metrics_topN` | `region`, `cluster_id` | Pod resource metric ranking |
| `huawei_get_cce_node_metrics_topN` | `region`, `cluster_id` | Node resource metric ranking |
| `huawei_get_aom_metrics` | `region`, `cluster_id` | AOM/Prometheus custom metric queries |

### 3. CA Pod Log Analysis (Manual Fallback)

```bash
# Step 1: Locate CA component Pods in kube-system
python3 scripts/huawei-cloud.py huawei_get_cce_pods \
  region=cn-north-4 cluster_id=<cluster_id> namespace=kube-system

# Step 2: Retrieve CA Pod logs (find pods with names containing autoscaler/cce-elastic/elastic-engine)
python3 scripts/huawei-cloud.py huawei_get_pod_logs \
  region=cn-north-4 cluster_id=<cluster_id> namespace=kube-system \
  pod_name=cce-cluster-autoscaler-abc123 container=autoscaler tail_lines=200
```

**CA Log Signal Quick Reference**:

| Signal | Meaning | Severity |
|--------|---------|----------|
| `No expansion options` | No available expansion options for node pool specs/AZ/subnet | critical |
| `max node group size reached` | Node group reached max_nodes limit | critical |
| `Scale-up: final scale-up plan is empty` | All node groups skipped in expansion plan | critical |
| `Quota exceeded` / `quota limit` | Cloud resource (ECS/EVS/EIP) quota insufficient | critical |
| `subnet ip exhausted` / `no available ip` | VPC subnet available IP exhausted | critical |
| `iam` / `permission denied` / `agency` / `forbidden` | IAM agency or permission abnormality | critical |
| `Failed to refresh` / `cannot connect` | CA cannot connect to cloud API or control plane | high |
| `skipping node group` | CA skipped a node group (reason in log) | high |
| `pod ... is unschedulable` | CA identified an unschedulable Pod | info |
| `ScaleDown: no candidates` | No candidate nodes for scale-down | info |
| `node ... is not suitable for removal` | Node does not meet scale-down conditions | high |
| `not safe to evict` / `safe-to-evict=false` | PDB or annotation protection blocking eviction | high |

## Parameter Reference

### `huawei_autoscaling_diagnose` (Primary Action)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | - | CCE cluster ID |
| `namespace` | No | - | Target namespace (narrows scope) |
| `workload_name` | No | - | Target workload name (Deployment/StatefulSet) |
| `workload_type` | No | - | Workload type (`Deployment` or `StatefulSet`) |
| `question` | No | - | User's original question (improves intent routing) |

### Common Parameters

| Parameter | Required | Description | Default |
|-----------|----------|-------------|---------|
| `region` | Yes | Huawei Cloud region | - |
| `cluster_id` | Yes (most actions) | CCE cluster ID | - |
| `namespace` | Action-dependent | Kubernetes namespace | - |
| `workload_name` | Action-dependent | Deployment/StatefulSet name | - |
| `pod_name` | Required for logs | Pod name | - |
| `container` | Required for logs | Container name | - |
| `tail_lines` | No | Log tail lines count | 200 |
| `top_n` | No | Number of top results for metrics | 10 |

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

## Output Format

The primary action `huawei_autoscaling_diagnose` returns structured evidence and a Markdown report. See [Output Schema](references/output-schema.md) for the full JSON response schema.

Key output fields:

| Field | Description |
|-------|-------------|
| `success` | Whether the diagnosis completed successfully |
| `intent.target` | Routing target: `WORKLOAD`, `NODE`, or `UNKNOWN` |
| `intent.scale_direction` | Scale direction: `scale_up`, `scale_down`, or `unknown` |
| `route` | Diagnosis path: `A`, `B`, `C`, or `BLOCKED` |
| `discovery` | Has_HPA, Has_CA, metric addon detected, nodepool autoscaling enabled |
| `issues` | List of diagnosed issues with code, severity, layer, evidence, recommendation |
| `evidence` | List of evidence items with layer, source, summary |
| `data_gaps` | Data collection failures or unconfirmed items |
| `conclusion` | Root cause conclusion summary |
| `confidence` | Confidence level (`High`, `Medium`, `Low`) |
| `report_markdown` | Complete Markdown diagnosis report (use as final output) |

Required Markdown report sections:

1. `# CCE Autoscaling Automated Diagnosis Report`
2. `## 1. Diagnosis Overview`: region, cluster, intent, scale direction, route, conclusion, confidence
3. `## 2. Capability Discovery & Routing`: Has_HPA, Has_CA, metric link, routing basis
4. `## 3. Investigation Process`: Gateway, Path A/B/C actual execution steps
5. `## 4. Key Evidence`: HPA status, nodepool/addon, Pending Pod, FailedScheduling evidence
6. `## 5. Issues & Root Cause Convergence`: issues ranked by severity with evidence and recommendations
7. `## 6. Next-Step Recommendations`: read-only verification and remediation suggestions only
8. `## 7. Data Gaps`: collection failures and items that could not be confirmed

## Verification

See [Verification Method](references/verification-method.md) for step-by-step verification.

## Best Practices

1. **Primary action first**: Always call `huawei_autoscaling_diagnose` first; use manual fallback only if the primary action fails
2. **Gateway routing**: Do not skip the Gateway phase — intent routing and capability discovery determine the correct Path A/B/C
3. **CA logs are critical**: CA Pod logs are the highest-confidence evidence source for node scaling failures; the primary tool automatically collects them, but manual fallback must prioritize this step
4. **Cascade diagnosis**: When HPA has scaled but new Pods are Pending, trace from HPA → CA as a cascade (Path C), not as separate isolated issues
5. **Metric prerequisites**: CPU/memory utilization-based HPA requires corresponding `resources.requests` on Pod containers; missing requests are a common critical root cause
6. **Read-only boundary**: This skill is read-only diagnosis; never create/modify HPA, scale workloads, modify nodepool min/max, install/upgrade addons, expand subnets, or apply for quota
7. **Hand off remediation**: When remediation is needed, hand off to `huawei-cloud-cce-auto-remediation-runner` and require user confirmation
8. **Log sanitization**: Never copy raw passwords, tokens, AK/SK, or Authorization headers from CA logs into output

## Reference Documents

| Document | Description |
|----------|-------------|
| [Workflow](references/workflow.md) | Gateway routing, Path A/B/C diagnosis trees, manual fallback tool sequence |
| [Output Schema](references/output-schema.md) | JSON response schema and required Markdown report sections |
| [Capability Map](references/capability-map.md) | Reusable tool capabilities, current gaps, and recommended atomic tool additions |
| [Risk Rules](references/risk-rules.md) | Allowed read actions, prohibited write actions, mutation boundary rules |

## Notes

- **Read-only by design** — this skill does NOT create/modify HPA, scale workloads, modify nodepool min/max, install/upgrade addons, expand subnets, or apply for quota
- **One-call preferred** — `huawei_autoscaling_diagnose` is the primary tool; raw queries are for targeted evidence when the user requests specific information or when the primary tool fails
- **Log sanitization** — only sanitized tail excerpts are included; raw secrets, tokens, and credentials must never appear in output
- **Gateway routing mandatory** — do not skip intent identification and capability discovery before entering Path A/B/C
- **CA Pod log analysis** — the primary tool automatically discovers and analyzes CA component Pod logs; manual fallback must prioritize this step
- **Cross-skill handoff** — when diagnosis reveals issues beyond autoscaling scope (Pod runtime failure, workload rollout failure, node NotReady), escalate to the appropriate skill

## Common Pitfalls

| Pitfall | Symptom | Quick Fix |
|---------|---------|-----------|
| Skipping Gateway routing | Diagnosis enters wrong path or misses capability | Always run intent + capability discovery before Path A/B/C |
| Missing CPU/Memory request | HPA cannot calculate utilization; `FailedGetResourceMetric` | Check `resources.requests` on all target Pod containers |
| Ignoring CA Pod logs | CA root cause remains unknown | Prioritize CA Pod log retrieval (kube-system autoscaler Pods) |
| Treating tolerance as failure | HPA not scaling when metrics within ~10% tolerance | Verify current metric ratio vs target threshold and tolerance window |
| Isolated HPA/CA analysis | Missing HPA→CA cascade linkage | Use Path C when both HPA and CA are present and intent is UNKNOWN |
| Wrong cluster_id | API returns 404 or empty results | Verify cluster ID via `huawei_list_cce_clusters` |
| Credential permission denied | API returns 403 | Check IAM permissions for CCE HPA/Pod/Event/Addon access |
| Not checking maxReplicas | HPA stuck at max replicas with `ScalingLimited` condition | Compare `currentReplicas` vs `maxReplicas` in HPA status |
| Not checking nodepool max_nodes | CA not expanding despite Pending Pods | Check `max_nodes` vs current node count in nodepool |
| Metrics API unavailable | HPA shows `FailedGetResourceMetric` | Ensure metrics-server or AOM addon is installed in cluster |