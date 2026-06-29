# Verification Method - CCE Node Failure Diagnoser Skill

## Overview

This document defines the verification steps for the CCE Node Failure Diagnoser skill. Verification is divided into five levels: environment setup, configuration verification, connectivity verification, primary diagnosis, and fallback workflow.

## Level 1: Environment Setup

### 1.1 Python Installation

| Item | Command | Success Criteria |
|------|---------|-----------------|
| Python installed | `python3 --version` | Returns version >= 3.6 |
| pip installed | `pip3 --version` | Returns pip version |

If Python is not installed, download and install from the official Python release page.

### 1.2 Python SDK Packages

```bash
pip3 install huaweicloudsdkcore huaweicloudsdkcce huaweicloudsdkaom huaweicloudsdkhss huaweicloudsdkvpc huaweicloudsdkecs huaweicloudsdkces huaweicloudsdkevs huaweicloudsdkeip huaweicloudsdkelb huawei-cloudsdkiam kubernetes
```

Expected: All packages installed without errors.

### 1.3 Dispatcher Script

| Item | Command | Success Criteria |
|------|---------|-----------------|
| Script exists | Check `scripts/huawei-cloud.py` in skill directory | File exists and is readable |

## Level 2: Configuration Verification

### 2.1 Credential Configuration

| Item | Method | Success Criteria |
|------|--------|-----------------|
| Credentials configured | Environment variables `HUAWEI_AK`, `HUAWEI_SK`, `HUAWEI_REGION` | Variables set with valid values |

🚫 **Never use** `echo $HUAWEI_AK` or `echo $HUAWEI_SK` to check credentials.

✅ **Correct**: Verify via a read-only action that requires authentication.

### 2.2 IAM Permission Check

Verify that the IAM user has the required permissions listed in [IAM Permission Policies](iam-policies.md).

## Level 3: Connectivity Verification

### 3.1 List CCE Nodes

```bash
python3 scripts/huawei-cloud.py huawei_list_cce_nodes region=cn-north-4 cluster_id=<cluster_id>
```

Expected: Returns list of CCE cluster nodes with names, IDs, and status.

### 3.2 Get Kubernetes Nodes

```bash
python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes region=cn-north-4 cluster_id=<cluster_id>
```

Expected: Returns v1.Node list with Ready status and conditions.

### 3.3 Get CCE Events

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_events region=cn-north-4 cluster_id=<cluster_id>
```

Expected: Returns Kubernetes events for the cluster.

## Level 4: Primary Diagnosis Verification

### 4.1 Diagnose a Healthy Node

```bash
python3 scripts/huawei-cloud.py huawei_node_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  node_name=<healthy-node-name> lease_timeout_seconds=40 \
  event_limit=500 hours=1 include_metrics=true
```

Expected: `success=true`, `root_category=Healthy`, `confidence=High`, `report_markdown` contains all required sections.

### 4.2 Verify Report Markdown Sections

Check that `report_markdown` contains:

| # | Section | Required Content |
|---|---------|-----------------|
| 1 | `# Kubernetes Node Automated Diagnosis Report` | Title |
| 2 | `## 1. Diagnosis Overview` | Node, conclusion, confidence, blast radius |
| 3 | `## 2. Node Status Health` | Conditions, pressure status, kubelet status |
| 4 | `## 3. Key Investigation` | Liveness triage, events, pod symptoms, metrics |
| 5 | `## 4. Diagnosis Conclusion` | Root cause, confidence, unconfirmed risks |
| 6 | `## 5. Remediation Recommendations` | Suggestions and verification steps |

### 4.3 Diagnose a NotReady Node (if available)

```bash
python3 scripts/huawei-cloud.py huawei_node_failure_diagnose \
  region=cn-north-4 cluster_id=<cluster_id> \
  node_name=<notready-node-name> lease_timeout_seconds=40 \
  event_limit=500 hours=1 include_metrics=true
```

Expected: `success=true`, `root_category` indicates actual root cause, `confidence` and `evidence` populated, `report_markdown` contains complete diagnosis.

### 4.4 Verify Node Conditions Match CCE Console

Compare node conditions (Ready, MemoryPressure, DiskPressure) in the output with the CCE console display for the same node.

## Level 5: Fallback Workflow Verification

### 5.1 Manual Evidence Collection

```bash
python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_get_cce_events region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_get_cce_pods region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics region=cn-north-4 cluster_id=<cluster_id> node_ip=<node_ip>
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN region=cn-north-4 cluster_id=<cluster_id>
```

Expected: All actions return valid results.

### 5.2 Inspection Actions

```bash
python3 scripts/huawei-cloud.py huawei_node_status_inspection region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_node_resource_inspection region=cn-north-4 cluster_id=<cluster_id>
python3 scripts/huawei-cloud.py huawei_node_vul_inspection region=cn-north-4 cluster_id=<cluster_id>
```

Expected: All inspection actions return valid results.

### 5.3 Security Correlation Actions

```bash
python3 scripts/huawei-cloud.py huawei_list_security_groups region=cn-north-4
python3 scripts/huawei-cloud.py huawei_list_vpc_acls region=cn-north-4
python3 scripts/huawei-cloud.py huawei_hss_list_hosts region=cn-north-4
python3 scripts/huawei-cloud.py huawei_hss_list_host_vuls_all region=cn-north-4 host_id=<host_id>
```

Expected: Security group, ACL, and HSS data returned.

## Verification Checklist

| # | Check Item | Command | Status |
|---|-----------|---------|--------|
| 1 | Python >= 3.6 installed | `python3 --version` | ☐ |
| 2 | SDK packages installed | `pip3 list | grep huaweicloudsdk` | ☐ |
| 3 | Dispatcher script exists | Check `scripts/huawei-cloud.py` | ☐ |
| 4 | Credentials configured | Environment variables set | ☐ |
| 5 | IAM permissions granted | Check IAM console | ☐ |
| 6 | List CCE nodes | `python3 scripts/huawei-cloud.py huawei_list_cce_nodes region=<r> cluster_id=<id>` | ☐ |
| 7 | Get Kubernetes nodes | `python3 scripts/huawei-cloud.py huawei_get_kubernetes_nodes region=<r> cluster_id=<id>` | ☐ |
| 8 | Get CCE events | `python3 scripts/huawei-cloud.py huawei_get_cce_events region=<r> cluster_id=<id>` | ☐ |
| 9 | Diagnose healthy node | `python3 scripts/huawei-cloud.py huawei_node_failure_diagnose region=<r> cluster_id=<id> node_name=<n>` | ☐ |
| 10 | Verify report sections | Check `report_markdown` has all 5 required sections | ☐ |
| 11 | Verify node conditions | Compare output with CCE console | ☐ |
| 12 | Node metrics query | `python3 scripts/huawei-cloud.py huawei_get_cce_node_metrics region=<r> cluster_id=<id> node_ip=<ip>` | ☐ |
| 13 | Pod metrics query | `python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN region=<r> cluster_id=<id>` | ☐ |
| 14 | Node status inspection | `python3 scripts/huawei-cloud.py huawei_node_status_inspection region=<r> cluster_id=<id>` | ☐ |
| 15 | Security groups list | `python3 scripts/huawei-cloud.py huawei_list_security_groups region=<r>` | ☐ |
| 16 | HSS hosts list | `python3 scripts/huawei-cloud.py huawei_hss_list_hosts region=<r>` | ☐ |