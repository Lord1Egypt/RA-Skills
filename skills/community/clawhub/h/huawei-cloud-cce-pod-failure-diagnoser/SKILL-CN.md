---
name: pod-failure-diagnoser
description: Use this skill for CCE Pod failures such as CrashLoopBackOff, ImagePullBackOff, OOMKilled, Pending, Evicted, restart storms, or workload unavailable.
---

# pod-failure-diagnoser

你负责诊断 CCE Pod 单资源故障，包括 CrashLoopBackOff、ImagePullBackOff、OOMKilled、Pending、Evicted 和频繁重启。先确认对象范围，再按 Kubernetes Pod status、container state、Events、previous/current logs、可选指标建立证据链。

## 处理步骤

1. 收集 `region`、`cluster_id`、`namespace`，尽量补齐 `pod_name`、`workload_name` 或 `labels`。
2. 首选调用 `huawei_pod_failure_diagnose`，让工具一次性拉取 Pod、Events、日志并输出 Top causes。
3. 如果用户只要原始信息，调用 `huawei_get_cce_pods` 查看 phase、reason、container state、last_state、restart_count、owner、node。
4. 对 CrashLoopBackOff、OOMKilled、频繁重启，查看 `previous=true` 的 `huawei_get_pod_logs`；对 ImagePullBackOff 通常没有容器日志，优先看 Events。
5. 对 Pending 优先看 FailedScheduling、FailedMount、FailedAttachVolume；必要时转 storage/node/autoscaling 方向继续诊断。
6. 对 OOMKilled 或 Evicted，可追加 `huawei_get_cce_pod_metrics` 或 TopN 指标验证内存、CPU、节点压力趋势。
7. 如果故障已经扩展到副本不满足、发布失败或 Service 不通，转交 workload/network/root-cause 相关 skill。

## References

- 状态分类和证据顺序读 `references/workflow.md`。
- 涉及恢复动作时读 `references/risk-rules.md`。
- 输出报告按 `references/output-schema.md`。

## 推荐 action

首选诊断：`huawei_pod_failure_diagnose`。

只读取证：`huawei_get_cce_pods`、`huawei_get_pod_logs`、`huawei_get_cce_events`、`huawei_get_cce_pod_metrics`。

综合诊断：`huawei_workload_diagnose`、`huawei_workload_diagnose_by_alarm`、`huawei_generate_diagnosis_report`。

## 风险约束

本 skill 不扩缩容、不删除工作负载、不重启节点。需要恢复动作时，把建议交给 `auto-remediation-runner`，默认先预览。
