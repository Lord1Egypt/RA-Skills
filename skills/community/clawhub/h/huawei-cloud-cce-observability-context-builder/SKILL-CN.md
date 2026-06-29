---
name: observability-context-builder
description: Use this skill when a Huawei Cloud CCE issue needs observability context from AOM alarms, metrics, LTS logs, Pod logs, or Kubernetes events before diagnosis.
---

# observability-context-builder

你负责把零散的故障信号整理成可诊断的上下文。先收集时间窗口、集群、命名空间、工作负载、Pod、节点和告警，再按证据类型输出，不直接执行恢复动作。

## 处理步骤

1. 明确时间窗口和对象范围：region、cluster_id、namespace、workload、pod、node、alarm_id。
2. 先查 active + history 告警，优先使用 `huawei_list_aom_alarms` 或 `huawei_analyze_aom_alarms`。
3. 拉取 Kubernetes Events、Pod 日志、AOM 指标 TopN，必要时查询 AOM/LTS 日志。
4. 把信号按时间线归并，标记缺口和下一步需要的诊断 skill。
5. 输出上下文包，不给出需要 `confirm=true` 的动作。

## References

- 需要完整取证步骤时读 `references/workflow.md`。
- 不确定是否可以调用某个动作时读 `references/risk-rules.md`。
- 输出报告前按 `references/output-schema.md` 组织字段。

## 推荐 action

优先：`huawei_list_aom_alarms`、`huawei_analyze_aom_alarms`、`huawei_get_cce_events`、`huawei_get_cce_pod_metrics_topN`、`huawei_get_cce_node_metrics_topN`。

日志：`huawei_query_aom_logs`、`huawei_get_recent_logs`、`huawei_get_pod_logs`。

图表：`huawei_generate_monitor_dashboard`。

## 风险约束

本 skill 只做只读观测。遇到扩缩容、删除、重启、drain、漏洞状态变更等需求，转交 `auto-remediation-runner` 并保持预览优先。

