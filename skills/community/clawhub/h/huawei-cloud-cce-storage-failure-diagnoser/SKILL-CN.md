---
name: storage-failure-diagnoser
description: Use this skill for CCE Kubernetes storage failures such as PVC Pending, provisioning failures, PV/PVC binding issues, EVS topology conflicts, VolumeAttachment attach failures, FailedMount, SFS/SFS Turbo NFS timeout, OBS 403 or credential errors, runtime IO errors, read-only filesystem, capacity or inode exhaustion, subPath mount deadlocks, and PVC Terminating protection. The skill must produce a complete Markdown diagnosis report with process, evidence, conclusion, confidence, and remediation guidance.
---

# storage-failure-diagnoser

你负责诊断 CCE/Kubernetes 存储故障，覆盖 PVC 供应、调度绑定、Attach/Mount、运行期 IO 和删除保护。默认产出一份完整 Markdown 报告，必须包含排查过程、证据、结论、置信度、建议动作和验证标准。

## Quick path

1. 收集 `region`、`cluster_id`，尽量补齐 `namespace`、`pvc_name`、`pod_name`、`failure_symptom`。
2. 首选调用 `huawei_storage_failure_diagnose`。它会采集 PVC/PV/StorageClass/Pod/Node/Event/VolumeAttachment、可选 Kubelet `/stats/summary`、Everest CSI 日志和云侧只读上下文，并返回 `report_markdown`。
3. 如果主工具失败或用户只要原始证据，按需调用 `huawei_get_cce_pvcs`、`huawei_get_cce_pvs`、`huawei_get_cce_storageclasses`、`huawei_get_cce_volumeattachments`、`huawei_get_cce_node_stats_summary`、`huawei_get_cce_everest_csi_logs`。
4. SFS/SFS Turbo 网络候选可追加 `huawei_list_security_groups`、`huawei_list_vpc_acls`；EVS 容量或 IO 候选可追加 `huawei_list_evs`、`huawei_get_evs_metrics`；OBS 凭证候选重点看 CSI 日志和事件。
5. 最终只输出 Markdown 诊断报告：排查过程、证据矩阵、结论、未确认风险和恢复验证标准必须完整。

## References

- 复用能力、缺口、分阶段诊断流水线读 `references/workflow.md`。
- 输出 Markdown 模板和结构化字段读 `references/output-schema.md`。
- 只读边界、数据一致性和高风险动作转交规则读 `references/risk-rules.md`。

## 推荐 action

主路径：`huawei_storage_failure_diagnose`。

Kubernetes 存储证据：`huawei_get_cce_pvcs`、`huawei_get_cce_pvs`、`huawei_get_cce_storageclasses`、`huawei_get_cce_volumeattachments`、`huawei_get_cce_node_stats_summary`、`huawei_get_cce_everest_csi_logs`、`huawei_get_cce_events`、`huawei_get_cce_pods`、`huawei_get_kubernetes_nodes`。

云侧补证：`huawei_list_evs`、`huawei_get_evs_metrics`、`huawei_list_sfs`、`huawei_list_sfs_turbo`、`huawei_list_security_groups`、`huawei_list_vpc_acls`。

交叉诊断：调度和节点资源问题可转 `node-failure-diagnoser`；Service/安全组/ACL 链路可转 `network-failure-diagnoser`；需要删除残留 Pod、迁移工作负载、扩容或修复云侧资源时转 `auto-remediation-runner`。

## 风险约束

本 skill 只读诊断，不删除 PVC/PV/Pod，不手工移除 finalizer，不 detach/attach EVS，不修改 StorageClass、安全组、ACL、IAM 委托或 Secret。需要恢复动作时只输出预案和验证标准，并转交 `auto-remediation-runner` 等待用户确认。
