# Verification Method - CCE Network Failure Diagnoser

## Overview

This document defines the verification steps for the CCE network failure diagnoser skill. Verification is divided into three levels: environment verification, configuration verification, and diagnosis verification.

## Level 1: Environment Verification

### 1.1 Python Environment

| Item | Command | Success Criteria |
|------|---------|------------------|
| Python installed | `python3 --version` | Returns Python version >= 3.6 |
| Environment check passed | `skill action=exec: bash skill://scripts/check_env.sh` | All checks pass (Python, dependencies, SDK, credentials, service) |

### 1.2 Dependency Installation

The environment check script automatically installs required dependencies. If it fails, manually install:

```bash
pip install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkvpc huaweicloudsdkelb huaweicloudsdkeip huaweicloudsdkces huaweicloudsdkecs huaweicloudsdkevs huaweicloudsdkiam
```

### 1.3 SDK Validation

```bash
python3 -c "from huaweicloudsdkcore.auth.credentials import BasicCredentials; print('SDK OK')"
```

Expected: `SDK OK` printed without error.

## Level 2: Configuration Verification

### 2.1 Credential Configuration

| Item | Method | Success Criteria |
|------|--------|------------------|
| AK/SK configured | Environment variables set | `HW_ACCESS_KEY` and `HW_SECRET_KEY` present (values NOT displayed) |
| Region configured | `HW_REGION_NAME` set | Region ID present (e.g., `cn-north-4`) |
| Cluster ID configured | `HW_CCE_CLUSTER_ID` set | Cluster ID present |

✅ **Correct**: Verify credentials by running the environment check script
❌ **Incorrect**: Do NOT use `echo $HW_ACCESS_KEY` or `echo $HW_SECRET_KEY` to check credential values

### 2.2 Service Connectivity

```bash
python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes region=cn-north-4 cluster_id=<cluster-id>
```

Expected: Returns JSON with node list (may be empty if cluster has no nodes).

## Level 3: Diagnosis Verification

### 3.1 Basic Diagnosis (Known-Healthy Cluster)

```bash
python3 scripts/huawei-cloud.py huawei_network_failure_diagnose region=cn-north-4 cluster_id=<cluster-id> namespace=default
```

Expected: Returns JSON with:
- `success: true`
- `confidence` value present
- `findings` array (may be empty for healthy cluster)
- `report_markdown` containing all required sections

### 3.2 Report Structure Validation

Verify `report_markdown` contains all required headings:

1. `# CCE Network Failure Automated Diagnosis Report`
2. `## 1. Diagnosis Overview`
3. `## 2. Investigation Process`
4. `## 3. Link Topology`
5. `## 4. Key Object Snapshot`
6. `## 5. Evidence Matrix`
7. `## 6. Diagnosis Conclusion`
8. `## 7. Recommended Actions and Verification Criteria`

### 3.3 Pipeline Pruning Validation

When node-level issues are present, verify:
- `pipeline_pruned` is set to `true`
- Upper-layer findings are not present (correctly pruned)
- Node-level findings reference the infrastructure issue

### 3.4 Cross-Reference with Console Data

Cross-reference diagnosis findings with Huawei Cloud console data:

| Finding Type | Console Verification |
|-------------|---------------------|
| `ELBBackendUnhealthy` | ELB console → Load balancer → Backend health status |
| `NetworkPolicyBlocked` | CCE console → NetworkPolicy details |
| `NodeUnhealthy` | CCE console → Node status |
| `SecurityGroup blocking` | VPC console → Security group rules |

### 3.5 Individual Action Verification

```bash
# Verify K8s evidence actions
python3 scripts/huawei-cloud.py huawei_get_cce_services region=cn-north-4 cluster_id=<cluster-id> namespace=default
python3 scripts/huawei-cloud.py huawei_get_cce_pods region=cn-north-4 cluster_id=<cluster-id> namespace=default

# Verify cloud network evidence actions
python3 scripts/huawei-cloud.py huawei_list_elb region=cn-north-4
python3 scripts/huawei-cloud.py huawei_list_security_groups region=cn-north-4
```

Expected: Each action returns valid JSON with relevant resource data.

## Verification Checklist

| # | Check Item | Command / Method | Status |
|---|-----------|-------------------|--------|
| 1 | Python >= 3.6 | `python3 --version` | ☐ |
| 2 | Environment check passed | `skill action=exec: bash skill://scripts/check_env.sh` | ☐ |
| 3 | AK/SK configured | Environment variables present (values NOT displayed) | ☐ |
| 4 | Cluster ID configured | `HW_CCE_CLUSTER_ID` present | ☐ |
| 5 | SDK validated | `python3 -c "from huaweicloudsdkcore.auth.credentials import BasicCredentials; print('SDK OK')"` | ☐ |
| 6 | Service connectivity | `huawei_get_kubernetes_nodes` returns valid data | ☐ |
| 7 | Diagnosis returns structured JSON | `huawei_network_failure_diagnose` returns success | ☐ |
| 8 | Report has all required sections | `report_markdown` has 7 required headings | ☐ |
| 9 | `confidence` and `severity` in all findings | All findings have numeric confidence and severity | ☐ |
| 10 | `pipeline_pruned` correct | Pruning flag matches node-level issues | ☐ |