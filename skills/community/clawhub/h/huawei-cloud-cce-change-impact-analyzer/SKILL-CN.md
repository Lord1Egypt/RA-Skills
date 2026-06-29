---
name: change-impact-analyzer
description: Use this skill when a Huawei Cloud CCE incident may be caused by recent changes, including workload releases, ConfigMap/Secret updates, Service/Ingress/Gateway route changes, NetworkPolicy/RBAC/security policy changes, node taints or infrastructure changes, and the user needs a complete Markdown report with timeline, evidence, blast radius, risk score, and conclusion.
---

# change-impact-analyzer

你负责把“故障发生前后有哪些变更”变成可证明的诱因分析。默认输出一份完整 Markdown 报告，包含排查过程、核心变更时间线、证据矩阵、爆炸半径、Top 风险预警、结论和数据缺口。

## 四阶段流水线

1. **Scope & Ingestion**：确认 `region`、`cluster_id`、`namespace` 或全集群范围、目标对象和时间窗口；生成 `Analysis-Trace-ID`；并行采集审计日志、K8s 历史事件、AOM active+history 告警、当前资源拓扑快照。
2. **Filtering & Categorization**：对审计写操作做语义降噪，过滤 HPA 副本变更、controller 写入、Token/Lease/Status 等干扰；保留镜像、环境变量、CoreDNS、Service/Ingress、NetworkPolicy、RBAC、Node taint 等核心变更。
3. **Impact & Blast Radius Modeling**：把核心变更映射到当前 Pod、Service、Ingress、Node、ConfigMap/Secret、Security Group/VPC ACL 快照，推断影响面和传播路径。
4. **Synthesis & Reporting**：按变更敏感度、拓扑波及范围、安全边界跨度、故障时间邻近度、事件/告警相关性评分，输出 Markdown 报告。

## 推荐 action

首选：`huawei_change_impact_analyze`。它会返回结构化字段和 `report_markdown`，可用 `output_file` 写出 `.md` 文件。

常用参数：

- `region`、`cluster_id`：必填。
- `hours` 或 `start_time`/`end_time`：分析窗口，默认过去 1 小时。
- `namespace`、`target_name`、`workload_name`、`app_name`：收敛目标范围，但不要因此忽略 kube-system/CoreDNS 等全集群变更。
- `fault_time` 或 `incident_time`：故障时间点，用于时间邻近度打分。
- `log_group_id`/`log_stream_id` 或日志组/流名称：审计日志自动发现失败时手工指定。
- `include_audit`、`include_k8s_events`、`include_aom`、`include_snapshots`：按需关闭某类采集。
- `top_n`：报告中最高风险预警数量，默认 3。

## 处理原则

- 先找变更，再找影响，再与告警/事件/故障时间对齐；不要只因为对象发生过更新就直接判定根因。
- CoreDNS、kube-proxy、网络插件、Ingress 控制器等基础配置变更即使发生在 `kube-system`，也必须纳入业务故障分析。
- Deployment 仅 HPA 调整 `replicas` 通常视为噪声；镜像、启动参数、探针、资源规格、环境变量、ConfigMap/Secret 引用变化视为核心变更。
- NetworkPolicy/RBAC 变更要重点关联连接超时、403、DNS 异常、跨命名空间访问失败。
- Node taint、cordon/drain、节点池扩缩容、集群升级等基础设施变更需要结合 Pod Pending、Evicted、NotReady 和节点事件判断。

## References

- 具体流水线和评分规则读 `references/workflow.md`。
- 可复用能力、当前缺口和建议补齐的原子能力读 `references/capability-map.md`。
- 输出字段和 Markdown 模板读 `references/output-schema.md`。
- 只读边界和恢复动作交接读 `references/risk-rules.md`。

## 风险约束

本 skill 只做只读分析和报告生成。不修改工作负载、不回滚、不改 ConfigMap/Secret、不调整安全组/ACL/NetworkPolicy/RBAC、不 cordon/drain/reboot 节点。任何恢复动作都必须转交 `auto-remediation-runner` 预览并由用户确认。
