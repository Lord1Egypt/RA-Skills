# Verification Method - CCE Pod Failure Diagnoser Skill

## Overview

This document defines the verification steps for the CCE Pod Failure Diagnoser skill. Verification is divided into four levels: installation verification, configuration verification, read-only operation verification, and diagnosis workflow verification.

## Level 1: Installation Verification

### 1.1 Python Installation

| Item              | Command               | Success Criteria                          |
| ----------------- | --------------------- | ----------------------------------------- |
| Python 3 installed| `python3 --version`   | Returns Python version >= 3.8             |

### 1.2 Script Availability

| Item                  | Command                                        | Success Criteria                          |
| --------------------- | ----------------------------------------------- | ----------------------------------------- |
| huawei-cloud.py exists| `ls scripts/huawei-cloud.py`                    | File found in scripts directory           |

## Level 2: Configuration Verification

### 2.1 Credential Configuration

| Item                    | Command                | Success Criteria                        |
| ----------------------- | ---------------------- | --------------------------------------- |
| Credentials configured  | Environment variables  | `HUAWEI_AK`/`HUAWEI_SK` or `HW_ACCESS_KEY`/`HW_SECRET_KEY` set; pass `region=...` or `--region=...` explicitly |

Never use `echo $HUAWEI_AK`, `echo $HUAWEI_SK`, `echo $HW_ACCESS_KEY`, or `echo $HW_SECRET_KEY` to check credentials.

### 2.2 API Connectivity Test

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Expected: Returns Pod list (HTTP 200).

## Level 3: Read-Only Operation Verification

### 3.1 List Pods

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Expected: Returns Pod status list with phase, reason, container states, restart counts.

### 3.2 Get Pod Events

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_events --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Expected: Returns Events list with reason, message, timestamps.

### 3.3 Get Pod Logs

```bash
python3 scripts/huawei-cloud.py huawei_get_pod_logs --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name> --container=<container-name>
```

Expected: Returns sanitized log excerpt.

### 3.4 Get Pod Previous Logs

```bash
python3 scripts/huawei-cloud.py huawei_get_pod_logs --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name> --container=<container-name> --previous=true
```

Expected: Returns sanitized previous container log excerpt (may be empty if Pod has not restarted).

### 3.5 Get Pod Metrics

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name>
```

Expected: Returns Pod CPU/memory usage metrics.

## Level 4: Diagnosis Workflow Verification

### 4.1 One-Call Diagnosis (Pod Name)

```bash
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name> --include_logs=true --include_metrics=false
```

Expected: Returns diagnosis JSON with `summary.diagnosis_status`, `pods[].issues`, `top_causes`, and `recommended_actions`.

### 4.2 One-Call Diagnosis (Workload Name)

```bash
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --workload_name=<deployment-name> --include_logs=true --include_metrics=false
```

Expected: Returns diagnosis for all Pods of the specified workload.

### 4.3 Verify Output Schema

Check that the diagnosis output conforms to the schema defined in [Output Schema](output-schema.md):

- `success` field present (boolean)
- `summary.diagnosis_status` present (string)
- `top_causes` array present (at least one entry for abnormal status)
- `recommended_actions` array present
- `next_skill` field present (string or null)

### 4.4 Verify No Mutation

After running diagnosis commands, verify that no cluster state changes occurred:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Expected: Pod count and status unchanged from before diagnosis.

## Verification Checklist

| #  | Check Item                | Command                                             | Status |
| -- | ------------------------- | --------------------------------------------------- | ------ |
| 1  | Python 3 >= 3.8           | `python3 --version`                                 | ☐      |
| 2  | Script available          | `ls scripts/huawei-cloud.py`                        | ☐      |
| 3  | Credentials configured    | Environment variables set                           | ☐      |
| 4  | API connectivity          | `python3 scripts/huawei-cloud.py huawei_get_cce_pods ...` | ☐ |
| 5  | List Pods                 | `python3 scripts/huawei-cloud.py huawei_get_cce_pods ...` | ☐ |
| 6  | Get Events                | `python3 scripts/huawei-cloud.py huawei_get_cce_events ...` | ☐ |
| 7  | Get current logs          | `python3 scripts/huawei-cloud.py huawei_get_pod_logs ...` | ☐ |
| 8  | Get previous logs         | `python3 scripts/huawei-cloud.py huawei_get_pod_logs ... --previous=true` | ☐ |
| 9  | Get Pod metrics           | `python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics ...` | ☐ |
| 10 | One-call diagnosis (Pod)  | `python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose ... --pod_name=<name>` | ☐ |
| 11 | One-call diagnosis (Workload) | `python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose ... --workload_name=<name>` | ☐ |
| 12 | Output schema valid       | Check JSON fields match output-schema.md            | ☐      |
| 13 | No mutation occurred      | Pod count/status unchanged                          | ☐      |
