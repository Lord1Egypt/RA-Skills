# Kimi Work Adapter

用于 Kimi Work 或同类支持文件读取、网页搜索、长文档处理和任务规划的宿主。核心判断仍由 `SKILL.md`、`references/` 和 `schemas/` 控制；本文件只处理宿主能力接线。

## Capability Map

| 能力 | 路线 |
| --- | --- |
| 文件读取 | 用宿主文件解析能力定位页码、幻灯片、隐藏页、工作表、隐藏工作表、公式错误值、Excel 批注/notes、段落、备注、页眉页脚和脚注 |
| 网页搜索 | 只用于核验公开来源、公司官网、财报、公告、政策和新闻日期 |
| 文件输出 | 用户明确要求后创建副本、批注稿或修订建议表 |
| 任务规划 | 只给 10/30/60 分钟修复路线，不创建自动发送任务 |

## File Handling

读取文件后先输出判定，再输出定位。无法读取图片、图表底层数据、隐藏页、批注、Excel notes、页眉页脚、脚注、尾注或隐藏工作表时，在 `未核验项` 写明。

调用本地预筛脚本时，将用户当前请求传给 `--context-text`，必要前文传给 `--conversation-text`；脚本推断出的对象、目标、截止和材料阶段要再与长对话、文件首页及结尾动作交叉核验。

每条问题保留两层归因：`error_family/error_type`。Kimi Work 可展开长上下文，但首屏仍先给判定、上下文、权重依据和必须改。

需要生成修订版时：

1. 先给风险清单。
2. 等用户确认改法。
3. 创建新文件副本。
4. 文件名加 `_presend_fix` 或日期后缀。
5. 保留原文件。

## Search Handling

只有用户要求核验来源、公开事实或“帮我补来源”时才搜索。搜索材料只当来源候选，不能自动替换用户文件里的口径。

需要标注：

- 来源名称。
- 发布时间或覆盖周期。
- 链接。
- 和原文件口径的差异。

无法确认时写 `待核验`。

搜索结果进入报告前必须标注口径差异；如果公开来源和用户材料周期、地区、样本或指标定义不一致，只能写成 `source_stale_or_misaligned` 或待核验，不能直接补成确定来源。

## Structured Output

需要交给表格、日志或后续 Agent 时，输出 `inspection.json`：

- 遵守 `schemas/presend-inspection.schema.json`。
- `context_basis.context_signals` 记录收件人、目标动作、截止时间或材料阶段来源。
- `context_basis.risk_weighting` 解释为什么某类风险排在前面。
- `must_fix` 每项带 `error_family/error_type`、`context_reason`、发现依据和修法。
- `additional_findings` 保留首屏以外的完整问题，`finding_overflow` 回显遗漏阻断数和位置。

## Forbidden Host Actions

| 用户要求 | 处理 |
| --- | --- |
| 直接发给老板或客户 | 给发送话术草稿，不发送 |
| 自动替用户承诺时间、价格、资源 | 改成待确认或需审批 |
| 覆盖原文件 | 创建副本前先确认 |
| 隐藏风险让材料显得更顺 | 保留风险，压缩表达 |
| 用搜索结果强行补齐内部数据 | 只列公开来源候选和口径差异 |
