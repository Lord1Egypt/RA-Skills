---
id: huawei-cloud-cce-network-failure-diagnoser
name: huawei-cloud-cce-network-failure-diagnoser
description: |
  Huawei Cloud CCE Network failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose CCE network connectivity issues, Service/Ingress failures, (2) analyze ELB configuration, VPC/Subnet issues, (3) diagnose DNS resolution failures, (4) check network policies and security group rules.
  Trigger: user mentions "network failure", "网络故障", "Service unreachable", "Service 不通", "Ingress 502", "Ingress 504", "ELB error", "ELB 异常", "DNS failure", "DNS 解析失败", "network diagnosis", "网络诊断", "VPC", "subnet", "子网", "安全组", "网络策略"
tags: [cce, network-diagnosis, elb, vpc, fault-diagnosis]
---

# Huawei Cloud CCE Network Failure Diagnoser

> **⚠️ Execution Method (Must Read): This skill executes diagnosis via local Python scripts using a dispatcher pattern. Using hcloud, openstack, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is `scripts/huawei-cloud.py`, invoked as `python3 scripts/huawei-cloud.py <action> <key=value params>`
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - For action details and parameters, refer to `references/workflow.md`, `references/risk-rules.md`, and `references/output-schema.md`
> - **Do not attempt hcloud, openstack, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill diagnoses CCE (Cloud Container Engine) network failures by performing a layered, read-only diagnosis across the full network stack — from node infrastructure, DNS, Service/EndpointSlice, NetworkPolicy, Ingress to cloud-side ELB/EIP/NAT/VPC security policies. It produces a complete Markdown diagnosis report that must include the investigation process, evidence, conclusions, confidence levels, and verification criteria.

**Use this skill when:**

1. CCE Service connectivity is broken (Service unreachable, intermittent, or flapping)
2. DNS/CoreDNS resolution failures (NXDOMAIN, timeout)
3. Ingress 502/504 errors or ELB backend health issues
4. NetworkPolicy blocking traffic between Pods
5. VPC/Subnet/Security Group/ACL configuration affecting cluster networking
6. EIP/NAT gateway affecting external access from the cluster

**This skill does NOT handle:**

1. Creating, modifying, or deleting any resources
2. Binding/unbinding EIP or modifying security groups/ACLs/ELB listeners
3. Scaling workloads or restarting components
4. Pod-level or Node-level root causes (cross-reference to `huawei-cloud-cce-pod-failure-diagnoser`, `huawei-cloud-cce-node-failure-diagnoser`, `huawei-cloud-cce-workload-failure-diagnoser`)

---

## Prerequisites

**You must run the environment check script first to complete environment validation and dependency installation in one step:**

- Linux / macOS: `skill action=exec: bash skill://scripts/check_env.sh`
- Windows: `skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1`

> Windows note: Do not use `&&` to chain commands (PowerShell 5.x does not support it); use semicolons if you need to change directories first.

The script will check in order: Python >= 3.6 → install dependencies → validate SDK → validate credentials → validate service availability. If the environment check fails, fix the issues before proceeding.

**Environment Variables:**

| Variable | Required | Description |
|----------|----------|-------------|
| HW_ACCESS_KEY | Yes | Huawei Cloud AK (Access Key) |
| HW_SECRET_KEY | Yes | Huawei Cloud SK (Secret Key) |
| HW_REGION_NAME | No | Default cn-north-4 |
| HW_PROJECT_ID | No | Project ID (automatically obtained via IAM API when not set) |
| HW_SECURITY_TOKEN | No | Required when using temporary AK/SK |
| HW_CCE_CLUSTER_ID | Yes | CCE cluster ID for diagnosis target |
| KUBECONFIG | No | Kubernetes config; auto-obtained from CCE API if not set |

**Security Constraints:**

1. Never persist AK/SK/Token/Certificate to filesystem
2. AK/SK exists only in the current call stack; released after call ends
3. Only non-sensitive project IDs may be cached in process memory (never written to disk)
4. All temporary certificate files must be deleted immediately after use
5. Never leak AK/SK in logs, responses, or error messages
6. Never send credentials to any third-party server

**Do not output the values of environment variables.**

---

### IAM Permission Requirements

| API Action | Permission | Purpose |
|-----------|------------|---------|
| cce:cluster:get | Get cluster | View cluster details |
| cce:cluster:list | List clusters | List CCE clusters |
| cce:node:list | List nodes | List cluster nodes |
| vpc:vpc:list | List VPCs | Query VPC details |
| vpc:subnet:list | List subnets | Query subnet details |
| elb:loadbalancer:list | List ELBs | Query ELB details |
| elb:listener:list | List listeners | Query ELB listeners |
| aom:*:get | Read AOM | Query AOM metrics and alarms |

**Permission Failure Handling**:
1. When any command fails due to permission errors, display required permission list
2. Guide the user to create a custom policy in the IAM console
3. Pause execution and wait for user confirmation

---

## Core Tools

All actions are invoked via the Python dispatcher script:

```
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> namespace=<namespace> [other_params...]
```

**Execution via skill:**

- Linux / macOS: `skill action=exec: skill://.venv/bin/python3 skill://scripts/huawei-cloud.py <action> <params>`
- Windows: `skill action=exec: skill://.venv/Scripts/python3.exe skill://scripts/huawei-cloud.py <action> <params>`

### Primary Diagnosis Action

| Action | Description |
|--------|-------------|
| `huawei_network_failure_diagnose` | One-shot diagnosis: collects K8s and cloud-side read-only snapshots, returns structured findings + `report_markdown` |

### Kubernetes Evidence Actions

| Action | Description |
|--------|-------------|
| `huawei_get_cce_services` | List Services in a namespace |
| `huawei_get_cce_ingresses` | List Ingresses in a namespace |
| `huawei_get_cce_pods` | List Pods in a namespace |
| `huawei_get_kubernetes_nodes` | List cluster Nodes |
| `huawei_get_cce_events` | List cluster Events |
| `huawei_get_pod_logs` | Retrieve Pod container logs |

### Cloud Network Evidence Actions

| Action | Description |
|--------|-------------|
| `huawei_get_elb_backend_status` | Read ELB pool/member/health monitor/load balancer status |
| `huawei_get_elb_metrics` | Retrieve ELB monitoring metrics |
| `huawei_list_elb` | List ELB load balancers |
| `huawei_list_elb_listeners` | List ELB listeners |
| `huawei_list_eip` | List EIP addresses |
| `huawei_get_eip_metrics` | Retrieve EIP monitoring metrics |
| `huawei_list_nat` | List NAT gateways |
| `huawei_get_nat_gateway_metrics` | Retrieve NAT gateway metrics |
| `huawei_list_security_groups` | List VPC security groups |
| `huawei_list_vpc_acls` | List VPC ACLs |

### Legacy Compatibility Actions

| Action | Description |
|--------|-------------|
| `huawei_network_diagnose` | Legacy comprehensive network diagnosis |
| `huawei_network_diagnose_by_alarm` | Diagnosis triggered by alarm correlation |
| `huawei_network_verify_pod_scheduling` | Verify Pod scheduling constraints (read-only) |

---

## Parameter Reference

### Required Parameters

| Parameter | Description |
|-----------|-------------|
| `region` | Huawei Cloud region, e.g., `cn-north-4` |
| `cluster_id` | CCE cluster ID |
| `namespace` | Kubernetes namespace |

### Optional Parameters (provide as many as possible for accurate diagnosis)

| Parameter | Description |
|-----------|-------------|
| `failure_symptom` | Symptom description: `domain_unresolvable`, `in_cluster_service_unreachable`, `service_intermittent`, `external_access_failed`, `ingress_502_504` |
| `target_kind` | Resource type: Pod, Service, Ingress, etc. |
| `target_name` | Resource name |
| `service_name` | Target Service name |
| `ingress_name` | Target Ingress name |
| `source_pod` | Source Pod name or label |
| `destination_pod` | Destination Pod name or label |
| `domain` | Domain name for DNS diagnosis |
| `elb_id` | ELB load balancer ID |

---

## Output Format

`huawei_network_failure_diagnose` returns structured JSON with an embedded `report_markdown`:

```json
{
  "success": true,
  "action": "huawei_network_failure_diagnose",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "namespace": "default",
  "conclusion": "high signal conclusion",
  "confidence": "High",
  "pipeline_pruned": false,
  "findings": [
    {
      "stage": "Stage 3: East-West Routing and Policy Layer",
      "type": "NetworkPolicyBlocked",
      "title": "NetworkPolicy selects target Pod but does not allow source Pod labels or target port",
      "confidence": 1.0,
      "severity": "critical",
      "evidence": [],
      "recommendation": [],
      "prune": false
    }
  ],
  "top_causes": [],
  "snapshot": {
    "inputs": {},
    "nodes": [],
    "pods": [],
    "services": [],
    "ingresses": [],
    "endpoint_slices": [],
    "network_policies": [],
    "events": [],
    "logs": {},
    "cloud": {
      "elb_ids": [],
      "elbs": {},
      "eips": {},
      "nat": {},
      "security_groups": {},
      "vpc_acls": {}
    }
  },
  "report_markdown": "# CCE Network Failure Automated Diagnosis Report\n..."
}
```

### Markdown Report Sections

The `report_markdown` must contain the following headings:

1. **Diagnosis Overview** — target, symptom, conclusion, confidence, collection time, pruned stages
2. **Investigation Process** — per-stage status (checked, abnormal, pruned/skipped)
3. **Link Topology** — DNS path, east-west path, or north-south path based on failure type
4. **Key Object Snapshot** — Service, EndpointSlice, Backend Pods, Ingress, NetworkPolicy, Cloud ELB
5. **Evidence Matrix** — stage, type, confidence, evidence summary
6. **Diagnosis Conclusion** — top root causes (max 3), each backed by evidence
7. **Recommended Actions and Verification Criteria** — read-only verification steps or change suggestions to hand off to `huawei-cloud-cce-auto-remediation-runner`

### Finding Types

Common `type` values in findings:

| Type | Description |
|------|-------------|
| `NodeUnhealthy` | Node Ready=False or Ready=Unknown |
| `NodePressure` | Memory/Disk/PID/Network pressure on node |
| `PodDNSConfigMissing` | Pod dnsPolicy=None with no dnsConfig |
| `KubeDnsNoEndpoint` | kube-dns EndpointSlice has 0 ready endpoints |
| `CoreDNSRestarting` | CoreDNS pods showing OOMKilled/LivenessProbe failures |
| `CoreDNSNxDomain` | CoreDNS logs showing NXDOMAIN responses |
| `CoreDNSUpstreamTimeout` | CoreDNS logs showing upstream i/o timeout |
| `NetworkPolicyBlocked` | NetworkPolicy blocks source Pod traffic (confidence 100%) |
| `ServiceNoReadyEndpoint` | Service has 0 ready endpoints in EndpointSlice |
| `ServiceSelectorMismatch` | Service selector matches no Pods |
| `ReadinessFlapping` | Backend Pod readiness probe flapping |
| `BackendOverloaded` | Application logs show OOM/connection pool exhausted |
| `LoadBalancerProvisioningFailed` | LoadBalancer Ingress status empty with CCM errors |
| `ELBBackendUnhealthy` | ELB member unhealthy while K8s backend Pod is Ready |
| `IngressUpstreamError` | Ingress controller logs show 502/504 |

---

## Verification

1. Run the environment check script to confirm dependencies and credentials are available
2. Execute `huawei_network_failure_diagnose` with a known-healthy cluster and verify the report structure
3. Cross-reference findings with Huawei Cloud console data (ELB health, security groups, VPC ACLs)
4. Verify `pipeline_pruned` flag is set correctly when node-level issues prune upper layers
5. Confirm that `confidence` and `severity` values are present in all findings

---

## Best Practices

1. Always provide `failure_symptom` to direct the diagnosis pipeline to the relevant stage (DNS, east-west, or north-south)
2. Provide as many optional parameters as possible (`service_name`, `ingress_name`, `source_pod`, `destination_pod`, `domain`) for more precise diagnosis
3. Start with `huawei_network_failure_diagnose` for one-shot comprehensive diagnosis; use individual actions only for targeted follow-up queries
4. When evidence is insufficient, state "evidence insufficient" explicitly — never present guesses as conclusions
5. For north-south (external access) issues, always supplement with `huawei_get_elb_backend_status` and `huawei_list_security_groups` to check cloud-side configuration
6. When node-level issues are found, note that upper-layer diagnosis may be pruned; cross-reference with `huawei-cloud-cce-node-failure-diagnoser`

---

## Reference Documents

- Diagnosis workflow, reuse priorities, and layered pipeline: `references/workflow.md`
- Risk rules and action boundaries: `references/risk-rules.md`
- Output schema and finding type reference: `references/output-schema.md`

---

## Notes

1. This skill is strictly read-only; it never modifies Service, Ingress, NetworkPolicy, CoreDNS ConfigMap, security groups, ACLs, ELB listeners/backends, EIP bindings, or NAT rules
2. Never execute `kubectl exec`, packet capture, stress testing, or active traffic injection unless the user explicitly requests and acknowledges the risk
3. `huawei_network_verify_pod_scheduling` is for verification only; it does not replace scaling actions
4. Any network change suggestion must describe impact scope, rollback method, and verification criteria, and be handed off to `huawei-cloud-cce-auto-remediation-runner` for preview
5. Do not output the values of environment variables such as HW_ACCESS_KEY, HW_SECRET_KEY, HW_SECURITY_TOKEN
6. All scripts must be executed via `skill action=exec`; do not run them directly in a shell

---

## Common Pitfalls

1. **Missing cluster_id**: The `cluster_id` parameter is required for all CCE actions. If the user only provides a cluster name, query `huawei_list_cce_clusters` first to resolve the ID
2. **Wrong failure_symptom**: Using a wrong symptom category (e.g., `ingress_502_504` for an in-cluster issue) may misdirect the pipeline. Always confirm the symptom type with the user
3. **Ignoring node-level root cause**: If nodes are NotReady, upper-layer diagnosis may be pruned. Do not skip the node-layer check even when the symptom appears to be Service/DNS-level
4. **Confusing K8s-side and cloud-side**: ELB backend unhealthy does not always mean the K8s Pod is unhealthy — check both `huawei_get_elb_backend_status` and `huawei_get_cce_pods` together
5. **Over-interpreting insufficient evidence**: When EndpointSlice has 0 ready endpoints, it could be selector mismatch, readiness flapping, or Pod crash. Do not jump to conclusions without checking Pod events and logs
6. **Not checking NetworkPolicy for east-west issues**: NetworkPolicy blocking has 100% confidence when confirmed, but is easily overlooked. Always check NetworkPolicy in the target namespace