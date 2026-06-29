# Workflow

1. Record the fault time, region, cluster_id, namespace, workload, pod, and node provided by the user.
2. If the time is unclear, default to the last 1 hour and note this assumption in the output.
3. Call `huawei_list_aom_alarms` to collect active + history alarms, then use `huawei_analyze_aom_alarms` for deduplication and severity grouping.
4. Call `huawei_get_cce_events` to retrieve Kubernetes Events, grouped by involved object and reason.
5. Call Pod/Node TopN metrics tools to find resource peaks, abnormal nodes, and abnormal Pods.
6. When log evidence is needed, prefer `huawei_query_aom_logs`, then supplement with Pod-side logs from `huawei_get_recent_logs` or `huawei_get_pod_logs`.
7. Output the evidence timeline, anomaly summary, missing information, and recommended diagnostic skill for hand-off.