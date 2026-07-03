# Common Pitfalls & Solutions

This document contains detailed troubleshooting guides for common issues encountered when using the CCE Pod Failure Diagnoser skill.

## Pitfall 1: Missing Targeting Parameter

**Symptom**: Diagnosis returns `no_matching_abnormal_pods` or empty Pod list

**Root Cause**: No targeting parameter (`pod_name`, `workload_name`, or `labels`) was provided, or the parameters do not match any Pods in the namespace

**Solution**: Always provide at least one targeting parameter:

```bash
# With pod_name
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=my-app-xxx

# With workload_name
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --workload_name=my-app

# With labels
python3 scripts/huawei-cloud.py huawei_pod_failure_diagnose --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --labels="app=my-app"
```

## Pitfall 2: Wrong Namespace

**Symptom**: No Pods found or diagnosis shows `no_matching_abnormal_pods`

**Root Cause**: The specified namespace does not contain the target Pods, or the namespace name is incorrect

**Solution**: Verify namespace with Pod list first:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Check all namespaces if unsure:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=<correct-namespace>
```

## Pitfall 3: ImagePullBackOff — Requesting Container Logs

**Symptom**: Container logs return empty, error, or "container not found"

**Root Cause**: ImagePullBackOff means the container image has not been pulled; no container exists to produce logs

**Solution**: Use Events instead of logs for ImagePullBackOff:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_events --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

Focus on events with reason `Failed`, `BackOff`, or `Pulling` related to the image.

## Pitfall 4: OOMKilled — Not Checking Previous Logs

**Symptom**: Current logs show only application startup output, no crash evidence

**Root Cause**: After OOMKilled, the container restarts and current logs show the new startup attempt; the crash evidence is in the previous container logs

**Solution**: Always request `previous=true` logs for OOMKilled:

```bash
python3 scripts/huawei-cloud.py huawei_get_pod_logs --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name> --container=<container> --previous=true
```

## Pitfall 5: Pending — Ignoring FailedScheduling Events

**Symptom**: Diagnosis misses the scheduling root cause; Pod shown as Pending without clear reason

**Root Cause**: FailedScheduling events contain the critical scheduler message explaining why no node was selected

**Solution**: Focus on Events with FailedScheduling, FailedMount, FailedAttachVolume reasons:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_events --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

If FailedMount/FailedAttachVolume is found, escalate to storage diagnosis. If node resource/affinity issues are found, consider `huawei-cloud-cce-node-failure-diagnoser`.

## Pitfall 6: Evicted — Missing Node Pressure Evidence

**Symptom**: Eviction cause unclear; diagnosis lacks node-level context

**Root Cause**: Eviction is triggered by node pressure conditions (MemoryPressure, DiskPressure); Pod-level data alone is insufficient

**Solution**: Check node conditions and Pod metrics:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --pod_name=<pod-name>

python3 scripts/huawei-cloud.py huawei_get_cce_pod_metrics_topN --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default --metric_type=memory --top_n=10
```

If node-level pressure is confirmed, escalate to `huawei-cloud-cce-node-failure-diagnoser`.

## Pitfall 7: Cluster ID Incorrect

**Symptom**: API returns 404, empty results, or cluster not found

**Root Cause**: The `cluster_id` parameter does not match an existing CCE cluster

**Solution**: Verify cluster ID from the cluster list:

```bash
python3 scripts/huawei-cloud.py huawei_get_cce_pods --region=cn-north-4 --cluster_id=<cluster-id> --namespace=default
```

If the cluster_id is wrong, find the correct ID from the CCE cluster management console or API.

## Pitfall 8: Credential Permission Denied

**Symptom**: API returns 403 Forbidden

**Root Cause**: The IAM user lacks required CCE Pod/Event/Log permissions

**Solution**: Verify IAM permissions for the required actions (see IAM Permission Requirements in SKILL.md). Create custom IAM policies with:

- `cce:pod:get`, `cce:pod:list`
- `cce:event:list`
- `cce:pod:log`
- `cce:pod:metrics`

Guide the user to create policies in the IAM console and grant authorization.

## Pitfall 9: Metrics API Unavailable

**Symptom**: Pod metrics query fails or returns empty

**Root Cause**: The metrics-server addon is not installed in the CCE cluster

**Solution**: Ensure metrics-server addon is installed:

```bash
# Check addon availability
hcloud CCE ShowAddonInstance --cluster_id=<cluster-id> --addon_id=metrics-server
```

If not installed, install via CCE console or hcloud CLI.

## Pitfall 10: Frequent Restart False Positive

**Symptom**: Diagnosis reports FrequentRestart for a Pod with normal restart behavior

**Root Cause**: The restart threshold is too low for the application context; some applications naturally restart occasionally

**Solution**: Consider context-specific thresholds:
- Normal: 0-2 restarts in 10 minutes
- Suspicious: 3-5 restarts in 10 minutes
- Concerning: >5 restarts in 10 minutes

Verify with `restart_count` and last termination reason before flagging as FrequentRestart.

## Error Code Reference

| Error Code          | HTTP Status | Description                  | Recommended Action                    |
| ------------------- | ----------- | ---------------------------- | ------------------------------------- |
| `CCE.001`           | 400         | Invalid parameter            | Check parameter format and rules      |
| `CCE.002`           | 404         | Cluster not found            | Verify cluster_id                     |
| `CCE.003`           | 400         | Cluster status unavailable   | Check cluster status                  |
| `CCE.004`           | 403         | Permission denied            | Check IAM policies                    |
| `CCE.006`           | 401         | Authentication failed        | Check AK/SK credentials               |
| `CCE.007`           | 429         | Too many requests            | Add delay, reduce request rate        |
| `MetricsNotAvailable` | N/A       | Metrics API not installed    | Install metrics-server addon          |
| `NoMatchingPods`    | 200         | No Pods match criteria       | Adjust targeting parameters           |