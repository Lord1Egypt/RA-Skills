---
name: autoscaling-diagnoser
description: Use this skill for Huawei Cloud CCE autoscaling failures, including HPA not increasing Pod replicas, Cluster Autoscaler or CCE elastic engine not adding or removing nodes, missing metrics, missing CPU or memory requests, maxReplicas or max_nodes limits, Pending Pods, scheduling constraints, subnet IP exhaustion, ECS quota, IAM agency permission issues, and HPA-to-CA cascade diagnosis. The skill must output a complete Markdown diagnosis report with process, evidence, conclusion, confidence, and recommendations.
---

# autoscaling-diagnoser

你负责诊断 CCE 自动弹性链路故障，并最终输出完整 Markdown 报告。重点区分两层闭环：HPA 是否把工作负载副本数从 N 调到 N+1，以及 CCE 集群弹性引擎/Cluster Autoscaler 是否在资源不足 Pending Pod 出现后把节点数从 M 调到 M+1。

## Quick Path

1. 收集 `region`、`cluster_id`，尽量补齐 `namespace`、`workload_name`、`workload_type` 和用户原始问题 `question`。
2. 首选调用 `huawei_autoscaling_diagnose`。它会执行意图识别、HPA/CA 能力发现、路径 A/B/C 路由、证据采集，并返回 `report_markdown`。
3. 最终面向客户只输出 Markdown 报告主体；报告必须包含排查过程、关键证据、根因结论、置信度、数据缺口和下一步建议。
4. 若主工具失败，再按 `references/workflow.md` 手工调用原子工具兜底，不要跳过 Gateway 路由。

## References

- 路由矩阵、路径 A/B/C 诊断树和人工兜底读 `references/workflow.md`。
- 主工具返回字段和 Markdown 模版读 `references/output-schema.md`。
- 可复用脚本能力、当前缺口和后续原子能力清单读 `references/capability-map.md`。
- 变更动作边界读 `references/risk-rules.md`。

## 推荐 Action

主路径：`huawei_autoscaling_diagnose`。

只读补证：`huawei_list_cce_hpas`、`huawei_list_cce_addons`、`huawei_list_cce_nodepools`、`huawei_get_cce_pods`、`huawei_get_cce_deployments`、`huawei_list_cce_statefulsets`、`huawei_get_cce_events`、`huawei_get_cce_pod_metrics_topN`、`huawei_get_cce_node_metrics_topN`、`huawei_get_aom_metrics`。

关联下钻：Pod 运行时异常转 `pod-failure-diagnoser`；工作负载 rollout 异常转 `workload-failure-diagnoser`；节点 NotReady/压力转 `node-failure-diagnoser`；资源治理和趋势优化转 `capacity-trend-forecaster` 或 `cost-optimization-advisor`。

## 风险约束

本 skill 默认只读诊断。不直接创建/修改 HPA，不扩缩工作负载，不修改节点池 min/max，不安装/升级插件，不扩容子网，不申请配额。需要整改时只给预览、YAML 或执行计划，并转交 `auto-remediation-runner` 或人工变更流程，真实执行必须由客户明确授权。
