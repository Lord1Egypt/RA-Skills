# LQS Skill Quickstart

> 定位：纯自然语言分析 Skill。
> 不要求执行器、不要求编码、不要求命令行、不要求内置抓取。

## 使用方式
- 输入一段自由文本需求，或一份 Google Doc 需求文档正文
- 先用 [.skill/prompts/01_parse_requirement.md](.skill/prompts/01_parse_requirement.md) 生成 `RequirementDraft`
- 再用 [.skill/prompts/04_resolve_spec.md](.skill/prompts/04_resolve_spec.md) 生成 `Spec`
- 再用 [.skill/prompts/05_render_artifacts.md](.skill/prompts/05_render_artifacts.md) 生成 `RenderPlan`
- 最后用 [.skill/prompts/06_preview_diff.md](.skill/prompts/06_preview_diff.md) 做 dry-run diff 预览

## 推荐输入
- 需求示例： [.skill/examples/free_text_input_example.md](.skill/examples/free_text_input_example.md)
- Google Doc 约定： [.skill/examples/google_doc_ingest_contract.md](.skill/examples/google_doc_ingest_contract.md)

## 推荐输出
- `RequirementDraft`
- `Spec`
- `RenderPlan`
- `Preview Diff`
- `ChangeReport`

## 每轮分析的必带结构
- `assumptions`：本轮做了哪些默认推断
- `evidence`：每条关键推断来自哪里
- `confidence`：整体置信度（high/medium/low）
- `ambiguities`：尚未完全确定、但已给出默认处理策略的点

## 逐轮变准（最小闭环）
1. 先保证主语义可落地（实体/动作/页面）
2. 把不确定项显式列入 `ambiguities`
3. 完成后回写一条新证据或修正一条旧假设到上下文
4. 下一轮优先处理上轮歧义项

## 注意
- 整个流程以 Prompt、Schema、Template 为主，不依赖仓库内命令执行器。
- migration 只生成预览与文件，不自动执行。
- 默认后台模块：Admin。
- 默认控制器基类：BackendBaseController。
