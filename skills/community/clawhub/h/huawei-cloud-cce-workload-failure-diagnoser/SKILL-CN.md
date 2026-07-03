---
name: workload-failure-diagnoser
description: Use this skill for CCE workload rollout failures such as release failed, rolling update stuck, replicas unavailable, Deployment new ReplicaSet not creating Pods, StatefulSet or DaemonSet update blocked, and probe-related readiness failures.
---

# workload-failure-diagnoser

你负责诊断 CCE 工作负载发布和副本可用性问题，覆盖 Deployment、StatefulSet、DaemonSet。先从控制器状态、版本归属和事件树建立证据，再把异常 Pod 交给已有 Pod 诊断逻辑下钻。

## 处理步骤

1. 收集 `region`、`cluster_id`、`namespace`、`kind`、`name`；`kind` 支持 `Deployment`、`StatefulSet`、`DaemonSet`。
2. 首选调用 `huawei_workload_rollout_diagnose`，它会采集 Workload、ReplicaSet、Pod 和 UID 清洗后的 Events，并输出 rollout 漏斗和 Top causes。
3. 如果只需要原始上下文或要核对证据，调用 `huawei_get_workload_rollout_context`。
4. 遇到 NewRS Pod 已创建但不 Ready 时，复用 `huawei_pod_failure_diagnose`、`huawei_get_pod_logs` 和 Pod 指标，不重复实现 CrashLoop/ImagePull/OOM/Pending 逻辑。
5. 如证据指向调度、节点压力或网络依赖，再转向 `node-failure-diagnoser` 或 `network-failure-diagnoser`。
6. 需要扩缩容、调整资源、删除重建、drain、重启等恢复动作时，只输出建议并转交 `auto-remediation-runner`。

## References

- 发布漏斗和版本锁定流程读 `references/workflow.md`。
- 输出结构按 `references/output-schema.md`。
- 风险边界读 `references/risk-rules.md`。

## 推荐 action

首选诊断：`huawei_workload_rollout_diagnose`。

只采集证据：`huawei_get_workload_rollout_context`。

Pod 下钻：`huawei_pod_failure_diagnose`、`huawei_get_pod_logs`、`huawei_get_cce_pod_metrics`、`huawei_get_cce_pod_metrics_topN`。

调度/存储/网络下钻：`huawei_get_cce_pvcs`、`huawei_get_cce_pvs`、`huawei_node_diagnose`、`huawei_network_diagnose`。

## 风险约束

本 skill 只做只读诊断。不扩缩容、不删除工作负载、不修改资源规格、不 cordon/drain/reboot 节点。所有需要确认的变更动作都交给 `auto-remediation-runner` 预览。
