---
name: daily-cluster-inspector
description: Use this skill for daily Huawei Cloud CCE health checks, quick checks, cluster inspections, heartbeat summaries, and continuous operations reports.
---

# daily-cluster-inspector

你负责做周期性、低风险的 CCE 巡检。优先快检，发现异常后再深度诊断，避免每次巡检都执行重型检查。

## 处理步骤

1. 收集 region、cluster_id、巡检范围和报告期望。
2. 优先调用 `huawei_cce_quick_check` 或 `huawei_cce_auto_inspection`。
3. 正常时输出简短健康摘要。
4. 异常时调用深度诊断或并行巡检，并按 Pod、Node、Event、AOM、ELB 分组。
5. 需要报告时调用导出报告 action。

## References

- 快检与深检分流读 `references/workflow.md`。
- 巡检只读边界读 `references/risk-rules.md`。
- 巡检摘要按 `references/output-schema.md`。

## 推荐 action

快检：`huawei_cce_quick_check`、`huawei_cce_auto_inspection`。

深检：`huawei_cce_deep_diagnosis`、`huawei_cce_cluster_inspection_parallel`、`huawei_pod_status_inspection`、`huawei_node_status_inspection`、`huawei_aom_alarm_inspection`。

报告：`huawei_export_inspection_report`。

## 风险约束

本 skill 只做巡检和报告，不执行修复动作。发现风险后输出建议并转交对应诊断或自愈 skill。

