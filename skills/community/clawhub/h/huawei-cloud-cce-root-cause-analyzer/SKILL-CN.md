---
name: root-cause-analyzer
description: Use this skill when a Huawei Cloud CCE incident spans alarms, workload rollout, Pod events/logs, recent changes, service topology, nodes, network, or metrics, and the user needs a complete Markdown root-cause report with investigation steps, evidence chain, impact scope, Top3 causes, confidence, and remediation handoff.
---

# root-cause-analyzer

你负责把多域证据收敛成根因结论。默认输出完整 Markdown 报告，包含排查过程、时间线、证据链、影响面、Top3 根因、置信度、反证和恢复交接。

## 处理步骤

1. 明确故障现象、时间窗口、影响业务和已知对象。
2. 首选调用 `huawei_root_cause_analyze`，让脚本汇聚工作负载发布诊断、依赖影响面、近期变更和 AOM 告警。
3. 对启动命令、镜像、探针、CrashLoop、ReplicaSet 创建失败等发布类故障，重点看 `huawei_workload_rollout_diagnose` 的 Top cause 和 Pod 事件/日志。
4. 对服务不可用，调用 `huawei_dependency_impact_analyze` 判断 Service/Ingress/Pod/Node 传播路径和影响面。
5. 对疑似发布、配置、网络、安全策略或节点变更，调用 `huawei_change_impact_analyze` 补充变更时间线和证据。
6. 生成 Top3 根因，逐条附证据、反证、影响面和置信度。
7. 恢复动作只作为建议，交给 `auto-remediation-runner` 做预览、确认和执行后验证。

## References

- 证据链和根因排序读 `references/workflow.md`。
- 风险边界读 `references/risk-rules.md`。
- 报告结构按 `references/output-schema.md`。

## 推荐 action

首选综合：`huawei_root_cause_analyze`。

工作负载：`huawei_workload_rollout_diagnose`、`huawei_workload_diagnose`、`huawei_pod_failure_diagnose`。

影响面：`huawei_dependency_impact_analyze`。

变更：`huawei_change_impact_analyze`。

网络/节点：`huawei_network_diagnose`、`huawei_network_failure_diagnose`、`huawei_node_diagnose`、`huawei_node_failure_diagnose`。

报告：`huawei_generate_diagnosis_report`、`huawei_generate_monitor_dashboard`。

告警：`huawei_analyze_aom_alarms`。

## 风险约束

本 skill 输出根因和建议，不执行变更。任何需要 `confirm=true` 的动作都必须转交 `auto-remediation-runner`。
