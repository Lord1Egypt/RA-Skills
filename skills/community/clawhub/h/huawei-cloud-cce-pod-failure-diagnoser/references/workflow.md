# Workflow

## Evidence Order

1. Scope: confirm `region`, `cluster_id`, `namespace`, and one of `pod_name`, `workload_name`, or `labels`.
2. Pod snapshot: read phase/status, reason/message, node, owner references, QoS, conditions, container states, last states, restart counts, image and resource requests/limits.
3. Events: correlate Pod events by involved object; preserve reason, message, count, and last timestamp.
4. Logs: for CrashLoopBackOff, OOMKilled, and frequent restarts, inspect `previous=true` first, then current logs. ImagePullBackOff normally has no container log.
5. Metrics: for OOMKilled/Evicted/resource suspicion, fetch Pod metrics and optionally TopN Pod/node metrics for the fault window.
6. Output: classify failure type, cite evidence, rank Top3 causes, list read-only next checks, and hand off any mutation to `huawei-cloud-cce-auto-remediation-runner`.

## Failure Rules

### CrashLoopBackOff

- Signals: waiting reason `CrashLoopBackOff`, BackOff restarting events, high `restart_count`, terminated last state.
- Evidence: previous logs, exit code, last termination reason, liveness/startup probe events, ConfigMap/Secret changes.
- Common causes: application crash, missing config, bad command/args, failed dependency, probe too aggressive, resource shortage during startup.

### ImagePullBackOff / ErrImagePull

- Signals: waiting reason `ImagePullBackOff` or `ErrImagePull`, events with failed pull/back-off pulling image.
- Evidence: image string, imagePullSecrets, event message, repository/tag/auth/network hints.
- Common causes: wrong image/tag, missing secret, SWR/registry permission, repository deleted, node egress or DNS issue, registry rate limit.

### OOMKilled

- Signals: last terminated reason `OOMKilled`, exit code 137, restart after memory spike.
- Evidence: last state, memory limit/request, Pod memory metrics, node memory pressure, business traffic or batch job timing.
- Common causes: memory limit too low, memory leak, cache growth, sudden traffic, JVM/runtime memory settings inconsistent with container limit.

### Pending

- Signals: phase `Pending`, `PodScheduled=False`, FailedScheduling, FailedMount, FailedAttachVolume, FailedCreatePodSandBox.
- Evidence: scheduler event message, node allocatable resources, taints/tolerations, affinity/nodeSelector, namespace quota, PVC/PV state.
- Common causes: insufficient resources, strict affinity, missing toleration, quota, PVC pending, mount timeout, CNI/sandbox creation issue.

### Evicted

- Signals: Pod reason/message contains `Evicted`, phase `Failed`, eviction events.
- Evidence: eviction message, node pressure condition, QoS class, requests/limits, ephemeral-storage usage.
- Common causes: MemoryPressure, DiskPressure, ephemeral-storage exhaustion, node NotReady, planned node maintenance.