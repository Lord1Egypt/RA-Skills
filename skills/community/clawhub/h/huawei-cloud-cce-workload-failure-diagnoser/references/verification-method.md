# Verification Method

## Step 1: Environment Check

Run the environment check script before any diagnosis action:

- Linux / macOS: `skill action=exec: bash skill://scripts/check_env.sh`
- Windows: `skill action=exec: powershell -ExecutionPolicy Bypass -File skill://scripts/check_env.ps1`

Verify that the script completes without errors:
- Python >= 3.6 installed
- Dependencies installed (huaweicloudsdkcore, huaweicloudsdkcce, kubernetes, etc.)
- SDK validation passed
- Credentials validated (HW_ACCESS_KEY, HW_SECRET_KEY)
- Service availability confirmed

## Step 2: Healthy Workload Baseline

Use a known healthy Deployment to verify that `huawei_workload_rollout_diagnose` returns `status: healthy`:

```bash
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_workload_rollout_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"Deployment","name":"<healthy-deployment>"}'
```

Expected output:
- `summary.status` = `"healthy"`
- `generation_check.observed` = `true`
- All funnel layers = `"pass"`
- `top_causes` list is empty or low-confidence

## Step 3: Failing Workload Diagnosis

Use a known failing workload to verify Top causes are accurately identified:

```bash
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_workload_rollout_diagnose --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"Deployment","name":"<failing-deployment>"}'
```

Expected output:
- `summary.status` = one of the failure statuses (`rollout_blocked`, `replicas_unavailable`, `probe_failure`, etc.)
- `top_causes` contains at least one ranked cause with evidence
- `funnel` identifies the first failing layer
- `events.filtered_count` > 0

## Step 4: Context Collection Consistency

Compare `huawei_get_workload_rollout_context` raw data with `huawei_workload_rollout_diagnose` output for consistency:

```bash
skill action=exec: python3 scripts/huawei-cloud.py --action huawei_get_workload_rollout_context --params '{"region":"cn-north-4","cluster_id":"<cluster-id>","namespace":"default","kind":"Deployment","name":"api"}'
```

Verify:
- `workload` object matches the workload status in diagnosis output
- `replicasets` list is present for Deployment kind
- `pods` list contains Pods matching the workload selector
- `events` list matches the UID-filtered events in diagnosis output

## Step 5: UID-Filtered Event Verification

Verify that UID-filtered Events match only workload-related objects (not all namespace Warning events):

1. Check that `events.filter.after_count` is significantly less than `events.filter.before_count`
2. Verify that all events in `events.timeline` have `involvedObject.uid` belonging to the Workload, ReplicaSet, or Pod UIDs
3. Verify `events.filter.events_without_involved_uid` = 0

## Step 6: Cross-Domain Handoff Verification

When diagnosis output contains `handoff` entries, verify that:

1. Each `handoff[].skill` uses the `huawei-cloud-cce-` prefix convention
2. The handoff reason is specific and actionable (not generic)
3. The handoff direction is consistent with the Top Cause type

## Step 7: Credential Security Verification

Verify that no credential values appear in any output:

1. Check that `HW_ACCESS_KEY`, `HW_SECRET_KEY`, `HW_SECURITY_TOKEN` values are never present in output JSON
2. Check that no temporary certificate files remain after execution
3. Verify that `warnings` does not contain credential-related information