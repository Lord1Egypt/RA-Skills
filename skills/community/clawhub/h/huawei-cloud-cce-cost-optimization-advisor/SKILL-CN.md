---
name: cost-optimization-advisor
description: Use this skill for Huawei Cloud CCE cost optimization analysis, including idle resources, oversized CPU or memory requests, low-utilization nodes, 24-hour and 7-day utilization trends, HPA recommendations, and node autoscaler policy optimization.
---

# cost-optimization-advisor

你负责分析 CCE 集群的成本优化机会。默认只做只读分析和配置建议，不直接修改 HPA、autoscaler、节点池或工作负载。

## 处理步骤

1. 收集 region、cluster_id、namespace 范围和业务排除规则；默认排除 `kube-system`。
2. 分别分析 24 小时和 7 天两个窗口的节点 CPU/内存使用率。
3. 标记低利用率节点：明显低于集群节点平均使用率，或集群平均 CPU/内存低于 30%。
4. 分析非 `kube-system` 工作负载的 request 与实际使用率差异，识别过量 request。
5. 检查节点池 autoscaling 信息，并用 `huawei_list_cce_hpas` 检查业务命名空间 HPA。
6. 如果需要 HPA，先用 `huawei_generate_cce_hpa_manifest` 或不带 `confirm=true` 的 `huawei_configure_cce_hpa` 生成预览；用户明确确认后才允许配置。
7. 输出优化建议、预计影响、风险和配置策略；需要真实配置时必须走确认流程。

## References

- 阈值、窗口和分析步骤读 `references/workflow.md`。
- 缩容、HPA/autoscaler 配置和安全边界读 `references/risk-rules.md`。
- 输出成本优化报告按 `references/output-schema.md`。

## 推荐 action

组合分析：优先使用 `huawei_analyze_cce_cost_optimization` 一次性完成资源清单、24h/7d 节点利用率、业务 Pod usage/request、HPA/autoscaler 状态和报告输出。

资源清单：`huawei_list_cce_nodes`、`huawei_list_cce_nodepools`、`huawei_get_cce_pods`、`huawei_get_cce_deployments`、`huawei_list_cce_hpas`。

指标分析：`huawei_get_cce_node_metrics_topN`、`huawei_get_cce_node_metrics`、`huawei_get_cce_pod_metrics_topN`、`huawei_get_cce_pod_metrics`、`huawei_get_aom_metrics`。

弹性策略：`huawei_generate_cce_hpa_manifest`、`huawei_configure_cce_hpa`。`huawei_configure_cce_hpa` 默认只返回预览，只有用户明确确认后才可以带 `confirm=true`。

图表：`huawei_generate_monitor_dashboard`。

## 风险约束

本 skill 不自动缩容、不修改 request、不自动安装或更新 HPA/autoscaler。可以生成 YAML、参数建议和执行计划；真实配置必须由用户明确确认后再调用带 `confirm=true` 的执行 action。
