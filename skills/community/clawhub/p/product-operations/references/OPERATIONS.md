# 操作与字段

## 制定运营计划

对应操作：`operation.plan`。必填：`product_name`、`goal`、`start_date`、`end_date`、`channels`。周期最长 91 天，渠道最多 6 个。可选：`budget`、`team_size`、`audience`、`notes`。

渠道值：`wechat`、`xiaohongshu`、`douyin`、`video`、`community`、`email`、`app`、`offline`、`other`。

## 复盘运营数据

对应操作：`operation.review`。必填：`campaign_name` 与 `metrics`。`metrics` 包含 `impressions`、`visits`、`leads`、`conversions`、`revenue`、`cost`；可增加 `target_conversions`、`previous_conversions`。漏斗数量必须满足曝光 ≥ 访问 ≥ 线索 ≥ 转化。

用户提供 CSV 或 XLSX 时，由 OpenClaw 在本机读取并映射上述字段，只向 API 提交汇总指标。平台工作台也支持上传 2 MB 以内、第一行为表头且第二行为汇总值的 CSV/XLSX。

## 获取运营检查清单

对应操作：`operation.checklist`。`scenario`：`product_launch`、`campaign`、`app_release`、`promotion`、`content`、`retention`。

`focus`：`complete`、`content`、`data`、`delivery`、`risk`。

## 导出运营结果

对应操作：`operation.export`。提交 `source_task_id`，来源必须是当前用户成功完成的 `operation.plan` 或 `operation.review` 任务。计划导出 CSV、XLSX、Markdown 和 ICS；复盘导出 CSV、XLSX 和 Markdown。
