---
name: node-failure-diagnoser
description: Use this skill for CCE node failures including NotReady, Ready=Unknown, kube-node-lease timeout, DiskPressure, MemoryPressure, NetworkUnavailable, CNI sandbox failures, kubelet or container runtime abnormalities, NPD events, and node-level workload impact. The skill must produce a complete Markdown diagnosis report with process, evidence, conclusion, and runbook recommendations.
---

# node-failure-diagnoser

你负责诊断 CCE/Kubernetes 节点故障，并输出完整 Markdown 报告。重点覆盖 NotReady、磁盘压力、内存压力、网络异常、kubelet/CRI 异常，以及节点承载 Pod 的影响面。

## Quick path

1. 收集 `region`、`cluster_id`，以及 `node_name` 或 `node_ip`。
2. 优先调用 `huawei_node_failure_diagnose`，它会采集 `v1.Node`、`kube-node-lease`、节点/Pod Events、节点上 Pod 状态和可选节点指标，并返回 `report_markdown`。
3. 如果用户只要原始证据或主工具失败，再按 References 中的 workflow 分步调用 `huawei_get_kubernetes_nodes`、`huawei_get_cce_events`、`huawei_get_cce_pods`、`huawei_get_cce_node_metrics`、`huawei_get_cce_pod_metrics_topN`。
4. 涉及安全组、ACL 或主机漏洞时，追加 `huawei_list_security_groups`、`huawei_list_vpc_acls`、`huawei_hss_list_hosts`、`huawei_hss_list_host_vuls_all`。
5. 最终只输出 Markdown 诊断报告：排查过程、证据、结论、置信度、影响面、处置建议必须完整。

## References

- 诊断分流、证据规则和兜底流程读 `references/workflow.md`。
- 输出 Markdown 模版和结构化字段读 `references/output-schema.md`。
- cordon、drain、reboot、漏洞修复边界读 `references/risk-rules.md`。

## 推荐 action

主路径：`huawei_node_failure_diagnose`。

证据采集：`huawei_get_kubernetes_nodes`、`huawei_get_cce_events`、`huawei_get_cce_pods`、`huawei_get_cce_node_metrics`、`huawei_get_cce_pod_metrics_topN`。

兼容诊断：`huawei_node_diagnose`、`huawei_node_batch_diagnose`。

巡检项：`huawei_node_status_inspection`、`huawei_node_resource_inspection`、`huawei_node_vul_inspection`。

安全：`huawei_hss_list_hosts`、`huawei_hss_list_host_vuls_all`。

## 风险约束

本 skill 只读诊断，不直接 cordon、uncordon、drain、reboot、不修改漏洞状态。需要动作时转交 `auto-remediation-runner`，并要求用户确认。
