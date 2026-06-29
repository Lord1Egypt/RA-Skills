# Workflow

## 1. Gateway Phase

Perform dual routing first; do not directly enter HPA or CA details.

Semantic intent:

- Matches Pod, workload, Deployment, StatefulSet, replica, instance: `Target=WORKLOAD`.
- Matches Node, node, ECS, virtual machine, server, host: `Target=NODE`.
- Ambiguous descriptions such as "Why isn't autoscaling working": `Target=UNKNOWN`.

Capability discovery:

- `Has_HPA`: `huawei_list_cce_hpas` returns HPA total count or target-scope-matched HPA.
- `Has_CA`: `huawei_list_cce_addons` identifies CCE elastic engine/Cluster Autoscaler, or `huawei_list_cce_nodepools` shows a node pool with autoscaling enabled.

Routing matrix:

| Target | Has_HPA / Has_CA | Route |
| --- | --- | --- |
| WORKLOAD | Any | A: Workload autoscaling diagnosis |
| NODE | Any | B: Node autoscaling diagnosis |
| UNKNOWN | True / False | A: Workload autoscaling diagnosis |
| UNKNOWN | False / True | B: Node autoscaling diagnosis |
| UNKNOWN | True / True | C: Dual-layer cascade diagnosis |
| Any | False / False | BLOCKED: No autoscaling capability configured |

## 2. Path A: Pod-Layer HPA Closed Loop

Goal: Explain why replica count did not increase from N to N+1.

Check sequence:

1. Does HPA exist and does its scaleTargetRef point to the correct Deployment/StatefulSet?
2. HPA status: `currentReplicas`, `desiredReplicas`, `minReplicas`, `maxReplicas`, conditions.
3. HPA Events: `FailedGetResourceMetric`, `FailedComputeMetricsReplicas`, `FailedGetScale`, `Selector`, `missing request`.
4. Metric condition: Are current CPU/memory or custom metrics above the target threshold; if the ratio falls within HPA tolerance, flag as "condition not met".
5. Resource requests: CPU/Memory utilization-type HPA must check whether target Pod containers have corresponding `resources.requests`.
6. Metric components: Are metrics-server, AOM, Prometheus, or custom/external metrics pipelines visible.
7. Upper limit and cooldown: `maxReplicas`, `ScalingLimited`, behavior/stabilization/cooldown-related Events.

Typical root causes:

- HPA not configured or HPA not matching the target workload.
- Missing CPU/Memory request; HPA cannot calculate utilization.
- Metric missing or metrics/AOM/Prometheus pipeline broken.
- Current metric below threshold, or within default ~10% tolerance.
- `maxReplicas` reached.
- scaleTargetRef, selector, or labels mismatch.

## 3. Path B: Node-Layer CA Closed Loop

Goal: Explain why node count did not increase from M to M+1, or why scale-down was blocked by protection policies.

**Priority prerequisite step: Analyze CA component Pod logs.**

CA components (CCE cluster elastic engine/Cluster Autoscaler) run as Pods in the `kube-system` namespace. Their standard output logs are the **most direct, highest-confidence** evidence source for node scaling issues. Prioritize retrieving CA Pod logs before investigation:

- Locate Pods in `kube-system` with names containing `autoscaler`/`cce-elastic`/`elastic-engine` via `huawei_get_cce_pods`.
- Retrieve logs using `huawei_get_pod_logs` (`tail_lines=200`).
- Search for key signals in logs (`huawei_autoscaling_diagnose` primary tool executes this step automatically).

**CA Log Key Signal Quick Reference:**

| Signal | Meaning | Severity |
| --- | --- | --- |
| `No expansion options` | CA has no available expansion options, usually because node pool specs/AZ/subnet do not meet the schedulable Pod requirements | critical |
| `max node group size reached` | Node group has reached max_nodes limit | critical |
| `Scale-up: final scale-up plan is empty` | Final expansion plan is empty; all node groups were skipped | critical |
| `Quota exceeded` / `quota limit` | Cloud resource (ECS/EVS/EIP) quota insufficient | critical |
| `subnet ip exhausted` / `no available ip` | VPC subnet available IP exhausted | critical |
| `iam` / `permission denied` / `agency` / `forbidden` | IAM agency or permission abnormality | critical |
| `Failed to refresh` / `cannot connect` | CA cannot connect to cloud API or control plane | high |
| `skipping node group` | CA skipped a node group; the log will state the reason | high |
| `pod ... is unschedulable` | CA identified an unschedulable Pod | info |
| `ScaleDown: no candidates` | No candidate nodes for scale-down | info |
| `node ... is not suitable for removal` | Node does not meet scale-down conditions | high |
| `not safe to evict` / `safe-to-evict=false` | PDB or annotation protection blocking eviction | high |

Scale-up check sequence:

1. **Prioritize CA Pod log review**: The primary tool `huawei_autoscaling_diagnose` automatically retrieves and analyzes them. For manual fallback, prioritize this step — CA logs often directly expose the root cause.
2. Is CCE cluster elastic engine/Cluster Autoscaler installed, and is the version below 1.13.8?
3. Are node pools/scaling groups autoscaling-enabled with min/max configured?
4. Do Pending Pods exist, especially `FailedScheduling` with `Insufficient cpu/memory/pods/ephemeral-storage`?
5. Has the node pool reached `max_nodes`?
6. Is Pending caused by affinity, anti-affinity, nodeSelector, or taint/toleration mismatch? This may not be solvable by simply adding nodes.
7. Cloud resource signals: VPC subnet IP exhaustion, ECS/EVS/EIP quota insufficient, IAM agency permission abnormality (CA logs usually contain explicit error messages).

Scale-down check sequence:

1. **Prioritize CA Pod log review**: Scale-down signals such as `not suitable for removal`, `not safe to evict`, `no candidates` are explicitly recorded in CA logs.
2. Are node requests below the scale-down threshold and continuously meeting the cooldown window?
3. Does PodDisruptionBudget disallow eviction?
4. Do Pods have `cluster-autoscaler.kubernetes.io/safe-to-evict=false` annotation?
5. Are there kube-system non-DaemonSet Pods or non-controller-managed Pods on the node?

## 4. Path C: Dual-Layer Cascade

Trace chronologically:

1. Run Path A first; determine whether HPA has increased target replicas or made workload desired replicas greater than ready replicas.
2. If HPA did not scale up, converge the conclusion to Pod-layer blocking; do not continue attributing the issue to nodes.
3. If HPA has scaled up and new Pods are Pending, treat those Pending Pods as input for Path B and check why CA did not add nodes (**including CA Pod log analysis**).
4. If HPA scaling cannot be proven and there are no Pending Pods, report as "insufficient cascade evidence" and list the historical HPA Events, Deployment revisions, or metric timelines that need to be collected.
5. In cascade scenarios, CA Pod logs simultaneously contain CA-side scheduling attempt records and cloud API call errors, which can serve as key supplementary evidence for the HPA→CA linkage.

## 5. Manual Fallback Tool Sequence

When `huawei_autoscaling_diagnose` is unavailable or fails:

1. `huawei_list_cce_hpas`
2. `huawei_list_cce_addons`
3. `huawei_list_cce_nodepools`
4. `huawei_get_cce_deployments` / `huawei_list_cce_statefulsets`
5. `huawei_get_cce_pods` (**also retrieve `namespace=kube-system` to locate CA component Pods**)
6. **`huawei_get_pod_logs`**: Locate Pods in `kube-system` with names containing `autoscaler`/`cce-elastic`/`elastic-engine`, retrieve their logs (`tail_lines=200`). Search for signals such as `NoExpansionOptions`, `QuotaExceeded`, `subnet`, `permission denied`, `skipping node group`, `max node group size`, `scale up plan empty`, `not suitable for removal`, `safe-to-evict` — this step is often **the most critical step for confirming CA-side root causes**.
7. `huawei_get_cce_events`
8. `huawei_get_cce_pod_metrics_topN` / `huawei_get_cce_node_metrics_topN`
9. If needed, use `huawei_get_aom_metrics` for custom PromQL queries.