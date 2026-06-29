# Workflow

## Reusable Capabilities and Gaps

- Available reusable tools: `huawei_get_kubernetes_nodes` for Node Ready/pressure conditions, `huawei_get_cce_events` for Kubernetes Events, `huawei_get_cce_pods` for Pod phase/reason/lastState, `huawei_get_cce_node_metrics` and `huawei_get_cce_pod_metrics_topN` for AOM metrics, `huawei_node_diagnose`/`huawei_node_batch_diagnose` for node monitoring, NPD, and workload summary.
- The external huawei-cloud skill also emphasizes the CCE node, Pod, Event, monitoring, inspection, and diagnosis report tool family; these read-only tools and the "list tasks first, then output complete report" output pattern can be directly reused.
- Original gaps: missing `kube-node-lease` renewal evidence, missing full Node condition timestamps, missing pod symptom aggregation per node, missing a deterministic action to synthesize NotReady/pressure/CNI/kubelet evidence into a Markdown report.
- Filled by the primary tool: `huawei_node_failure_diagnose` outputs structured evidence and `report_markdown` in one invocation.

## Main Flow

1. Input must include `region`, `cluster_id`, and either `node_name` or `node_ip`.
2. Call `huawei_node_failure_diagnose` with defaults: `lease_timeout_seconds=40`, `event_limit=500`, `hours=1`, `include_metrics=true`.
3. If the primary tool returns `report_markdown`, use that Markdown as the final report body. You may only add clarifications the user requests; do not discard evidence tables.
4. If the primary tool fails, follow the manual fallback workflow below.

## 1. Control Plane Liveness Triage

Collect:

- `v1.Node.status.conditions` for `Ready`, `MemoryPressure`, `DiskPressure`, `PIDPressure`, `NetworkUnavailable`.
- `kube-node-lease/<node_name>` `spec.renewTime`; calculate the difference between current time and renewTime.

Determine:

- **Case A**: `Ready=Unknown` and Lease renewal delay exceeds 40 seconds. Inference: control plane disconnected from the node. If there is no stronger evidence such as `SystemOOM`, `EvictionThresholdMet`, `FailedCreatePodSandBox/CNI`, or `ContainerRuntimeNotReady`, the conclusion should read "control plane disconnected from node (network link or Kubelet/CRI heartbeat interrupted, requires node-side verification)" — do not prematurely attribute to kubelet or network alone.
- **Case B**: `Ready=False` and Lease is renewing normally. Inference: kubelet is alive and actively reporting node or infrastructure unhealthy.
- **Case C**: `Ready=True`. Inference: basic communication is normal; continue investigating local resource pressure, CNI, and workload symptoms.
- **Case D**: Other combinations. Mark as insufficient evidence; continue narrowing with Event, Pod, and node local logs.

## 2. Node Event Timeline Retrospection

Filter Events where `involvedObject.kind=Node` and `involvedObject.name=<node_name>`, sorted by `lastTimestamp/eventTime/firstTimestamp` descending.

Strong signals:

- `SystemOOM`: strong memory pressure evidence.
- `EvictionThresholdMet` with message containing `imagefs`, `nodefs`, `DiskPressure`, `ephemeral-storage`: strong disk pressure evidence.
- `KubeletSetupFailed`, `ContainerRuntimeNotReady`, `PLEG`, runtime not ready: strong kubelet/CRI abnormality evidence.
- `NodeNotReady`: NotReady result evidence; root cause must still be identified.

## 3. Workload Symptom Drill-Down

Query all Pods where `spec.nodeName=<node_name>`, and aggregate `phase`, `reason`, `message`, container `state`, and `lastState`.

Determine:

- **Disk pressure**: Multiple Pods `phase=Failed`, `reason=Evicted`, message mentions `DiskPressure`, `nodefs`, `imagefs`, or `ephemeral-storage`.
- **Memory pressure**: Business Pod `lastState.terminated.reason=OOMKilled`, especially exit code `137`; if `SystemOOM` is also present, confidence is high.
- **Network abnormality**: New Pods stuck in `ContainerCreating`; corresponding Pod Events have `FailedCreatePodSandBox`, message contains `CNI`, `network plugin returns error`, `timeout waiting for DHCP`, etc.
- **kubelet/CRI abnormality**: Many Pods become `Unknown`/`NodeLost`, or `kube-system` core DaemonSets (kube-proxy, CNI plugin, CSI plugin, etc.) are abnormal, frequently restarting, or `Unhealthy`.

## 4. Metrics and Cloud-Side Supplementary Evidence

- Use `huawei_get_cce_node_metrics` to verify CPU, memory, disk trends; do not treat single-point peaks as root cause directly.
- Use `huawei_get_cce_pod_metrics_topN node_ip=<node_ip>` to find high-memory/high-CPU Pods on the node.
- When NotReady or network hypothesis is strong, additionally check security groups, network ACLs, and Master-Node communication paths.
- When kernel vulnerabilities or reboot-required issues are involved, additionally check HSS host and vulnerability lists, but do not execute repairs in this skill.

## 5. Conclusion Synthesis

Priority is evidence strength, not fixed order:

1. Strong Event + Pod symptom agreement: high confidence; can directly categorize as memory, disk, network, or kubelet/CRI.
2. `Ready=Unknown` + Lease timeout: high confidence for "node disconnected" itself; usually only medium-low confidence for underlying root cause, unless independent strong evidence exists.
3. Pressure condition `Unknown` with reason `NodeStatusUnknown`: only means kubelet stopped reporting; does not equate to MemoryPressure/DiskPressure being normal or abnormal; report should label as "indeterminate" and note missing independent evidence.
4. Only NotReady or only metric anomaly: medium-low confidence; requires local log verification.

Conclusions must include: root cause category, confidence level, key evidence, impact radius, unconfirmed risks, and next-step verification.