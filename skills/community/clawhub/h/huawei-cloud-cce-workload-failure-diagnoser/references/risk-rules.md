# Risk Rules

## Allowed

- Read Workload, ReplicaSet, Pod, Event, PVC, PV, metric, log, node, and network diagnostic data.
- Generate diagnosis summaries, evidence timelines, Top causes, and handoff recommendations.
- Suggest remediation options only as proposals.

## Not Allowed

- Do not call `huawei_scale_cce_workload`, `huawei_resize_cce_workload`, or `huawei_delete_cce_workload`.
- Do not cordon, uncordon, drain, reboot, delete nodes, or resize node pools.
- Do not add `confirm=true` to any action.
- Do not treat all namespace Warning events as evidence; only use UID-filtered events.
- Do not fabricate diagnosis results without evidence.
- Do not modify, scale, delete, or recreate any workload resource.

## Handoff

| Diagnosis Direction                  | Target Skill                              | Reason                                          |
| ------------------------------------ | ----------------------------------------- | ------------------------------------------------ |
| Workload resource changes            | `huawei-cloud-cce-auto-remediation-runner`| Scale/resize/delete/rollback actions             |
| Node pressure or scheduling failures | `huawei-cloud-cce-node-failure-diagnoser` | NotReady/DiskPressure/MemoryPressure/Scheduling  |
| Service, Ingress, ELB, or dependency reachability | `huawei-cloud-cce-network-failure-diagnoser`  | Service/Ingress connectivity issues              |
| Storage mount or PVC/PV issues       | `huawei-cloud-cce-storage-failure-diagnoser`               | FailedMount/FailedAttachVolume/PVC Pending       |
| Multi-domain uncertainty             | `huawei-cloud-cce-root-cause-analyzer`    | Cross-domain evidence convergence                |
| Pod-level failures                   | `huawei-cloud-cce-pod-failure-diagnoser`  | CrashLoop/ImagePull/OOM/Pending/Probe drill-down |
| Alarm correlation evidence           | `huawei-cloud-cce-alarm-correlation-engine`| AOM alarm dedup and severity grouping           |

## Risk Level

This skill operates at **R1** (read-only observation only). All write, scale, delete, cordon, drain, and reboot operations are prohibited and must be handed off to `huawei-cloud-cce-auto-remediation-runner`.