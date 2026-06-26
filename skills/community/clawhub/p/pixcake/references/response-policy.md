# Response Policy

## Success Language

- 项目创建成功：说“已创建项目”
- 图片导入成功：说“已提交导入”或“已导入到目标项目”
- 预设应用成功：说“已应用预设 `<name>`”
- 导出成功：说“已提交导出任务”或“导出任务已创建”

## Export Language

`batch_export_images` 返回成功时，只能表达为：

- 已提交导出任务
- 已开始导出
- 导出任务已创建

不要说：

- 已经导出完成
- 图片已经在桌面上了

## Export Status Language

`get_task_status` 返回成功时：

- 如果任务还在处理中，说“导出任务处理中”或“当前进度为 `<x>`”
- 如果任务已完成，才说“导出任务已完成”
- 如果任务失败，直接说明任务失败，并带上最关键的失败信息

不要在没有 `get_task_status` 结果时，把导出任务说成已完成。

## Preset Matching Language

- 高匹配直执行时，明确告诉用户使用了哪个预设
- 需要用户选择时，直接给 2 到 4 个候选，不要丢开放式大问题

## Out-Of-Scope Language

统一表达为：

- 当前 PixCake skill 未暴露该能力
- 当前版本仅支持项目管理、预设修图和导出

## Version Mismatch Language

出现兼容性问题时，优先表达为：

- 当前 PixCake 客户端版本可能过旧，或客户端与当前 skill 包版本不匹配
- 请升级到支持 Skills 的 PixCake 客户端 `9.0.0` 或更高版本后重试
- 如升级后仍无法处理，请联系工作人员或客服支持

## Failure Language

- 返回失败工具名和最可能缺失的上下文
- 给用户一个可执行的下一步
- 不只贴原始报错
- 不编造成功结果
