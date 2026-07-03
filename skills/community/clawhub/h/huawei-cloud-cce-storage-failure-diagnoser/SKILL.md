---
id: huawei-cloud-cce-storage-failure-diagnoser
name: huawei-cloud-cce-storage-failure-diagnoser
description: |
  Huawei Cloud CCE Storage failure diagnosis skill using Python SDK dispatcher.
  Use this skill when the user wants to: (1) diagnose PVC Pending, volume mount failures, (2) analyze EVS disk issues, (3) diagnose storage class and CSI driver errors, (4) check PV/PVC binding status and storage capacity.
  Trigger: user mentions "storage failure", "存储故障", "PVC Pending", "PVC 挂载失败", "volume mount error", "卷挂载错误", "EVS disk", "云硬盘", "PV failure", "PV 异常", "CSI driver error", "CSI 驱动异常", "存储诊断", "FailedMount", "FailedAttachVolume"
tags: [cce, storage-diagnosis, evs, pvc, fault-diagnosis]
---

# Huawei Cloud CCE Storage Failure Diagnoser

> **Execution Method (Must Read): This skill executes queries via the local Python dispatcher script. Using hcloud, kubectl, or other CLI tools or direct API calls is prohibited.**
>
> - The dispatcher script is located at `scripts/huawei-cloud.py` within the skill directory
> - All scripts and environment check scripts are inside the skill package. **You must use `skill action=exec` to execute them. Do not run them directly in a shell.**
> - **Do not attempt hcloud, kubectl, curl IAM, or any other CLI/API methods. This skill does not depend on those tools.**
> - **All paths are relative to the skill directory, which is the directory where this SKILL.md is located.**

## Overview

This skill diagnoses CCE/Kubernetes storage failures across PVC provisioning, scheduling/binding, attach/mount, runtime I/O, capacity, permission, and teardown stages. It uses the local Python dispatcher (`scripts/huawei-cloud.py`) to call the Huawei Cloud Python SDK and Kubernetes client APIs, collecting PVC/PV/StorageClass/Pod/Node/Event/VolumeAttachment evidence, Everest CSI logs, Kubelet `/stats/summary`, and cloud-side storage information. It produces a complete Markdown diagnosis report with process, evidence, conclusion, confidence, and remediation guidance.

### Related Skills

| Skill | Purpose |
|-------|---------|
| `huawei-cloud-cce-node-failure-diagnoser` | Node-level failure diagnosis (scheduling, node resource issues) |
| `huawei-cloud-cce-network-failure-diagnoser` | Network failure diagnosis (Service/security group/ACL chain) |
| `huawei-cloud-cce-pod-failure-diagnoser` | Pod-level failure diagnosis |
| `huawei-cloud-cce-auto-remediation-runner` | Execute remediation actions (delete residual Pods, migrate workloads, expand storage, fix cloud resources) |
| `huawei-cloud-cce-metric-analyzer` | Metric trend analysis |
| `huawei-cloud-cce-observability-context-builder` | Observability context enrichment |

### Capabilities

1. One-shot storage failure diagnosis with structured evidence and Markdown report (`huawei_storage_failure_diagnose`)
2. PVC/PV/StorageClass/VolumeAttachment collection (`huawei_get_cce_pvcs`, `huawei_get_cce_pvs`, `huawei_get_cce_storageclasses`, `huawei_get_cce_volumeattachments`)
3. Node Kubelet `/stats/summary` proxy-read for capacity and inode analysis (`huawei_get_cce_node_stats_summary`)
4. Everest CSI driver/controller log retrieval with auto-sanitization (`huawei_get_cce_everest_csi_logs`)
5. Cloud-side EVS/SFS/SFS Turbo supplementary evidence (`huawei_list_evs`, `huawei_get_evs_metrics`, `huawei_list_sfs`, `huawei_list_sfs_turbo`)
6. Network supplementary evidence for SFS/NFS (`huawei_list_security_groups`, `huawei_list_vpc_acls`)
7. Pod, Node, and Event Kubernetes evidence (`huawei_get_cce_pods`, `huawei_get_kubernetes_nodes`, `huawei_get_cce_events`)

### Typical Use Cases

- Diagnose a PVC stuck in `Pending` state
- Investigate Pod stuck in `ContainerCreating` with `FailedMount` or `FailedAttachVolume` events
- Analyze EVS disk attach failures, residual attachment locks, or per-node disk count limits
- Troubleshoot SFS/SFS Turbo NFS mount timeouts or network data-plane blocking
- Resolve OBS bucket access 403 errors, IAM delegation or AK/SK credential failures
- Diagnose runtime read-only filesystem, capacity or inode exhaustion
- Investigate ConfigMap/Secret subPath mount deadlocks
- Resolve PVC stuck in `Terminating` due to protection finalizers
- Check StorageClass provisioning or CSI driver errors

### What This Skill Does NOT Handle

1. Creating, modifying, or deleting PVC/PV/Pod resources
2. Removing finalizers or force-detaching EVS disks
3. Modifying StorageClass, IAM delegations, AK/SK Secrets, security groups, or ACLs
4. Executing `kubectl exec`, node SSH, packet capture, stress tests, or `fsck`
5. Any write operations on the data plane or control plane

---

## Prerequisites

### Python Dependencies

The dispatcher script requires Python >= 3.6 and the following packages:

- `huaweicloudsdkcore`
- `huaweicloudsdkcce`
- `huaweicloudsdkevs`
- `huaweicloudsdksfs`
- `huaweicloudsdkvpc`
- `huaweicloudsdkiam`
- `huaweicloudsdkces`
- `kubernetes`

Run environment check before first use (see Verification section). The venv is auto-created by `check_env`; on Linux/macOS use `.venv/bin/python3`, on Windows use `.venv/Scripts/python3.exe`.

### Credential Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| HW_ACCESS_KEY | Yes | Huawei Cloud Access Key |
| HW_SECRET_KEY | Yes | Huawei Cloud Secret Key |
| HW_REGION_NAME | No | Default region (overrides `region` param if set); default cn-north-4 |
| HW_PROJECT_ID | No | Project ID (auto-obtained via IAM API when not set) |
| HW_SECURITY_TOKEN | No | Required when using temporary AK/SK |

**Security constraints:**

1. Never persist AK/SK/Token/Certificate to disk or long-term memory
2. AK/SK exists only in the current request call stack and is released on completion
3. Only non-sensitive project IDs may be cached in process memory (never written to disk)
4. All temporary certificate files must be deleted immediately after use
5. Never leak AK/SK or other sensitive information in logs, responses, or errors
6. Never send authentication information to any third-party server

**Do not output the values of the above environment variables.**

### IAM Permissions

This skill requires read-only IAM permissions for CCE, EVS, SFS, OBS, VPC, and CES services. Minimum required permissions:

| Service | Permission | Purpose |
|---------|-----------|---------|
| CCE | `cce:cluster:get`, `cce:node:get` | Read cluster and node info |
| CCE | `cce:pod:get`, `cce:pvc:get` | Read Pod and PVC status |
| EVS | `evs:disk:list`, `evs:disk:get` | Read EVS disk details |
| EVS | `evs:cloudvolume:list` | List cloud volumes |
| VPC | `vpc:securityGroup:get`, `vpc:firewall:get` | Read security groups and ACLs |
| SFS | `sfs:share:get`, `sfs:share:list` | Read SFS/SFS Turbo shares |

If a permission check fails, verify AK/SK configuration, confirm the user has the required read-only permissions, and check that the IAM policy is active (policies typically take effect within 5-10 minutes).

---

## Core Tools

All actions are invoked via the dispatcher script:

```bash
python3 scripts/huawei-cloud.py <action> region=<region> cluster_id=<cluster_id> [key=value ...]
```

### Primary Diagnosis Action

```bash
python3 scripts/huawei-cloud.py huawei_storage_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  namespace=default pvc_name=<pvc_name> \
  include_stats=true include_logs=true include_cloud=false
```

Returns structured evidence + `report_markdown` (complete Markdown diagnosis report).

**Recommended defaults:** `include_stats=true`, `include_logs=true`, `include_cloud=false`. Set `include_cloud=true` when you need EVS/SFS/SFS Turbo and security group/ACL supplementary evidence.

### Kubernetes Evidence Actions

| Action | Required Params | Optional Params | Description |
|--------|----------------|-----------------|-------------|
| `huawei_get_cce_pvcs` | `region`, `cluster_id` | `namespace`, `pvc_name` | List PVCs |
| `huawei_get_cce_pvs` | `region`, `cluster_id` | `pv_name` | List PVs |
| `huawei_get_cce_storageclasses` | `region`, `cluster_id` | - | List StorageClasses with provisioner, parameters, volumeBindingMode |
| `huawei_get_cce_volumeattachments` | `region`, `cluster_id` | - | List VolumeAttachments with attached status, attachError, detachError |
| `huawei_get_cce_node_stats_summary` | `region`, `cluster_id` | - | Proxy-read node `/stats/summary`; parse PVC usedBytes/capacityBytes and inode |
| `huawei_get_cce_everest_csi_logs` | `region`, `cluster_id` | - | Read Everest CSI driver/controller logs (auto-sanitized) |
| `huawei_get_cce_events` | `region`, `cluster_id` | - | List cluster events |
| `huawei_get_cce_pods` | `region`, `cluster_id` | `namespace`, `pod_name` | List Pods |
| `huawei_get_kubernetes_nodes` | `region`, `cluster_id` | - | List Kubernetes nodes with labels, taints, conditions |

### Cloud Supplementary Evidence Actions

| Action | Required Params | Optional Params | Description |
|--------|----------------|-----------------|-------------|
| `huawei_list_evs` | `region` | `disk_id`, `availability_zone` | List EVS disks |
| `huawei_get_evs_metrics` | `region`, `disk_id` | - | Get EVS disk I/O metrics |
| `huawei_list_sfs` | `region` | - | List SFS file systems |
| `huawei_list_sfs_turbo` | `region` | - | List SFS Turbo file systems |
| `huawei_list_security_groups` | `region` | - | List VPC security groups (for SFS/NFS network analysis) |
| `huawei_list_vpc_acls` | `region` | - | List VPC network ACLs (for SFS/NFS network analysis) |

---

## Parameter Reference

### `huawei_storage_failure_diagnose`

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region (e.g., `cn-north-4`) |
| `cluster_id` | Yes | - | CCE cluster ID |
| `namespace` | No | - | Kubernetes namespace (recommended for PVC Pending/Terminating/capacity issues) |
| `pvc_name` | No | - | Specific PVC name |
| `pod_name` | No | - | Specific Pod name (recommended for Pod Pending/ContainerCreating/IO anomalies) |
| `failure_symptom` | No | - | Symptom description, e.g., "PVC Pending", "FailedMount mount.nfs timeout", "OBS 403", "Read-only file system", "PVC Terminating" |
| `include_stats` | No | true | Include node `/stats/summary` for capacity/inode analysis |
| `include_logs` | No | true | Include Everest CSI driver/controller logs |
| `include_cloud` | No | false | Include EVS/SFS/SFS Turbo and security group/ACL cloud-side evidence |

### Common Parameters (All Actions)

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `region` | Yes | - | Huawei Cloud region |
| `cluster_id` | Yes* | - | CCE cluster ID (required for CCE/K8s actions; not required for pure cloud actions) |
| `ak` | No | env HW_ACCESS_KEY | Huawei Cloud AK |
| `sk` | No | env HW_SECRET_KEY | Huawei Cloud SK |
| `project_id` | No | auto-obtained | Project ID (auto-obtained via IAM API when not set) |

*Required for CCE/Kubernetes actions. Not required for pure cloud-side actions like `huawei_list_evs`, `huawei_list_security_groups`.

---

## Output Format

The primary action `huawei_storage_failure_diagnose` returns structured JSON with an embedded `report_markdown`. See `references/output-schema.md` for the full JSON response schema.

```json
{
  "success": true,
  "action": "huawei_storage_failure_diagnose",
  "region": "cn-north-4",
  "cluster_id": "cluster-id",
  "namespace": "default",
  "conclusion": "high signal conclusion",
  "confidence": "High",
  "findings": [
    {
      "stage": "Mount stage failure",
      "type": "EVSNodeAttachLimitExceeded",
      "title": "VolumeAttachment attached=false; error indicates ECS per-node disk count limit reached",
      "confidence": 0.94,
      "severity": "critical",
      "evidence": [],
      "recommendation": []
    }
  ],
  "top_causes": [],
  "snapshot": {},
  "report_markdown": "# CCE Storage Failure Automated Diagnosis Report\n..."
}
```

### Required Markdown Report Sections

When `report_markdown` is present, use it as the final report body. You may add clarifications the user requests, but do not discard evidence tables.

The `report_markdown` must contain these headings:

- `# CCE Storage Failure Automated Diagnosis Report`
- `## 1. Diagnosis Overview`
- `## 2. Investigation Process`
- `## 3. Key Object Relationships`
- `## 4. Evidence Matrix`
- `## 5. Diagnosis Conclusion`
- `## 6. Recommended Actions and Verification Standards`
- `## 7. Data Gaps and Manual Confirmation`

### Finding Types

Common `type` values in findings:

| Type | Description |
|------|-------------|
| `NormalWaitForFirstConsumer` | PVC Pending with WaitForFirstConsumer; normal behavior awaiting Pod scheduling |
| `EVSQuotaExceeded` | EVS cloud disk quota exceeded |
| `SFSSubnetIPInsufficient` | SFS/SFS Turbo subnet available IP or mount target allocation failure |
| `OBSBucketNameInvalid` | OBS bucket name conflict or invalid naming |
| `EVSAvailabilityZoneSchedulingConflict` | EVS single-AZ affinity prevents Pod scheduling to storage AZ |
| `LocalPVNodeOffline` | Local PV host node down/offline |
| `VolumeAttachmentNotCreated` | K8s control plane has not issued attach instruction |
| `EVSNodeAttachLimitExceeded` | ECS per-node attached disk count limit reached |
| `EVSResidualAttachmentLock` | EVS residual node occupancy or underlying lock not released |
| `EVSAttachFailed` | EVS attach failure (general) |
| `HostKernelMountFailed` | Cloud-side attached but host kernel/filesystem mount failed |
| `SFSNfsNetworkBlocked` | SFS/SFS Turbo NFS mount timeout due to network data-plane blocking |
| `OBSCredentialInvalid` | OBS IAM delegation changed, AK/SK Secret invalid, or bucket permission error |
| `StoragePermissionDenied` | Permission denied / forbidden / access denied (general) |
| `PVCCapacityExhausted` | PVC capacity usage > 95% |
| `PVCInodeExhausted` | PVC inode usage > 95% |
| `ReadOnlyFilesystemProtection` | Linux read-only filesystem protection triggered |
| `ConfigMapSecretSubPathDeadlock` | ConfigMap/Secret subPath mount point deadlock |
| `PVCProtectionBlocked` | PVC Terminating with kubernetes.io/pvc-protection finalizer |
| `StorageIOError` | Runtime storage I/O errors |

---

## Verification

### Environment Check

Before first use, run the environment check script to install dependencies and validate credentials:

- Linux/macOS: `skill action=exec: bash skill://scripts/check_env.sh`
- Windows: `skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1`

The script checks: Python >= 3.6, install dependencies, validate SDK, validate credentials, validate service availability.

### Diagnosis Verification

1. Run environment check and confirm all checks pass
2. Execute `huawei_storage_failure_diagnose` with a known region and cluster_id:
   ```bash
   python3 scripts/huawei-cloud.py huawei_storage_failure_diagnose \
     region=cn-north-4 cluster_id=<cluster_id> include_stats=true include_logs=true
   ```
3. Verify the returned JSON contains `success=true`, `findings` array, and `report_markdown`
4. Check that the Markdown report contains all required sections (see `references/output-schema.md`)
5. Compare diagnosis conclusions against known failure patterns

---

## Best Practices

1. Always call `huawei_storage_failure_diagnose` first; use individual tools only as fallback or for raw evidence
2. Provide `namespace` and `pvc_name`/`pod_name` when possible to narrow diagnosis scope
3. Set `include_cloud=true` only when you need cloud-side (EVS/SFS/OBS) supplementary evidence
4. For NFS/SFS mount timeouts, always supplement with security group and VPC ACL checks
5. For OBS 403 errors, focus on Everest CSI logs and event messages rather than cloud-side queries
6. Conclusion confidence is ranked by evidence strength, not by stage priority
7. Never write guesses as conclusions; output evidence gaps explicitly
8. For any remediation actions, only output proposed plan and verification standards, then hand off to `huawei-cloud-cce-auto-remediation-runner` for user confirmation

---

## Reference Documents

| Document | Description |
|----------|-------------|
| `references/workflow.md` | Diagnosis triage flow, reusable capabilities, and stage-by-stage pipeline |
| `references/output-schema.md` | Output JSON schema and required Markdown report sections |
| `references/risk-rules.md` | Risk boundary rules: allowed read actions, prohibited write actions, and high-risk handoff |
| [Huawei Cloud Python SDK Documentation](https://doc.huihua.com/api/sdk/python.html) | SDK reference |
| [Huawei Cloud API Explorer](https://support.huaweicloud.com/apiexplorer/index.html) | API interactive explorer |

---

## Notes

1. This skill is **read-only diagnosis only** — it never deletes PVC/PV/Pod, patches finalizers, force-detaches/attaches EVS, or modifies any StorageClass/IAM/Secret/SecurityGroup/ACL
2. Never expose or log AK/SK or environment variable values
3. All actions are executed via `python3 scripts/huawei-cloud.py <action>`; do not use hcloud CLI, kubectl, or direct API calls
4. PVC Terminating: never directly suggest removing `kubernetes.io/pvc-protection` finalizer; must first prove no Pod references and no business data risk
5. EVS residual mount or read-only filesystem scenarios: never suggest force-unmount, force-attach, or direct restart of database-class workloads before confirming filesystem consistency
6. ConfigMap/Secret `resourceVersion` has no natural update timestamp; use `managedFields.time`, Pod timestamps, and FailedMount events as circumstantial evidence only
7. Cross-diagnosis handoff: scheduling/node resource issues -> `huawei-cloud-cce-node-failure-diagnoser`; Service/security group/ACL chain -> `huawei-cloud-cce-network-failure-diagnoser`; remediation actions -> `huawei-cloud-cce-auto-remediation-runner`

---

## Common Pitfalls

| Pitfall | Correct Approach |
|---------|-----------------|
| Treating `WaitForFirstConsumer` PVC Pending as a failure | A PVC in Pending state with `WaitForFirstConsumer` volumeBindingMode and no associated Pod is normal behavior, not a failure |
| Diagnosing scheduling failures without AZ context | EVS disks are single-AZ; always check PV `nodeAffinity` and node AZ labels before concluding scheduling issues |
| Confusing mount vs. attach | `attached=true` in VolumeAttachment means cloud-side attach succeeded; `FailedMount` events indicate host-side kernel/filesystem mount failure, not cloud attach failure |
| Overlooking CSI logs for OBS issues | OBS 403 and credential errors are best identified in Everest CSI logs, not in Kubernetes events alone |
| Premature finalizer removal | Removing `kubernetes.io/pvc-protection` without verifying no Pod references can cause data loss |
| Guessing without evidence | When no clear finding matches, output the evidence gap rather than fabricating a conclusion |
| Skipping environment check | Always run the environment check script before first diagnosis execution |