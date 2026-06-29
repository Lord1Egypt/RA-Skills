---
name: dependency-impact-analyzer
description: Use this skill when a Huawei Cloud CCE incident needs service topology impact analysis, including Service/Ingress/Pod/Node propagation paths, upstream/downstream blast radius, affected entrypoints, and a complete Markdown impact report with evidence and confidence limits.
---

# dependency-impact-analyzer

你负责基于 Kubernetes 服务拓扑判断故障传播路径和上下游影响。默认输出完整 Markdown 报告，包含排查过程、拓扑证据、传播路径、影响面结论和能力缺口。

## 处理步骤

1. 明确 `region`、`cluster_id`、`namespace`、目标工作负载/服务名或 `label_selector`。
2. 首选调用 `huawei_dependency_impact_analyze`，采集 Pod、Service、Ingress、Node 当前快照。
3. 用 Service selector 识别目标 Pod 的上游服务，用 Ingress backend 识别外部入口。
4. 根据 Pod Ready 状态、Service/Ingress 数量和传播路径给出影响等级。
5. 输出影响面、传播路径、证据表和置信度限制。
6. 如果影响面来自近期变更，转交 `change-impact-analyzer`；如果需要恢复，转交 `auto-remediation-runner`。

## 推荐 action

首选：`huawei_dependency_impact_analyze`。

补充查询：`huawei_get_cce_pods`、`huawei_get_cce_services`、`huawei_get_cce_ingresses`、`huawei_get_kubernetes_nodes`。

相关诊断：`huawei_workload_rollout_diagnose`、`huawei_network_failure_diagnose`、`huawei_change_impact_analyze`。

## References

- 具体流水线读 `references/workflow.md`。
- 输出结构读 `references/output-schema.md`。
- 只读边界和置信度限制读 `references/risk-rules.md`。

## 风险约束

本 skill 只做只读拓扑分析和报告生成。不修改 Service、Ingress、Deployment、NetworkPolicy、ELB 或节点状态。恢复动作必须交给 `auto-remediation-runner` 预览并确认。
