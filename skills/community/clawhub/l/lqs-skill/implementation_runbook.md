# LQS Skill 实施 Runbook（纯自然语言版）

说明：本 Runbook 面向 Prompt / Template / Schema 驱动的 Skill 流程，核心是“上下文完备 + 渐进式推断精度提升”，不依赖仓库内命令执行器。

## 0) 核心原则（必须遵守）
1. 不引入执行器，不要求编码，不要求命令行流程。
2. 所有推断都要显式给出：`assumptions`、`evidence`、`confidence`。
3. 允许不确定，但必须沉淀到 `ambiguities`，并在下一轮收敛。
4. 每次需求处理后，至少回写一条“可复用模式”到上下文或 patterns。
5. 默认先求稳，再求全：先覆盖主语义，再补细节分支。

---

## 阶段 1：准备（上下文对齐）
输入：
- .skill/context.json
- 目标需求文本或文档正文

输出：
- 需求原文（脱敏）
- 本轮分析范围声明（本轮覆盖/暂不覆盖）

通过标准：
- 不包含数据库凭证
- 明确边界：是“后台 CRUD”，还是“含权限/工作流/跨模块”

## 阶段 2：需求解析（RequirementDraft）
执行：
- 使用 prompts/01_parse_requirement.md
- 输出 RequirementDraft（符合 schemas/requirement_draft.schema.json）

额外要求：
- 同时输出：`assumptions[]`、`evidence[]`、`confidence`、`ambiguities[]`

通过标准：
- 至少识别 1 个实体
- 至少识别 4 个基础动作（list/view/create/update/delete 可合并）
- 每个关键推断都有证据来源（用户原文/项目上下文/历史模式）

## 阶段 3：项目模式挖掘（ProjectPatternProfile）
执行：
- 使用 prompts/02_mine_patterns.md
- 扫描 Admin 控制器 + Admin views 样本

输出：
- ProjectPatternProfile

额外要求：
- 给高频模式标记置信度（高/中/低）
- 标记例外场景（exceptions）

通过标准：
- 明确 query_contract 与 response_contract
- 明确控制器与视图骨架
- 有“模式适用范围”和“已知例外”

## 阶段 4：模板资产化（TemplatePack）
执行：
- 使用 prompts/03_build_templates.md
- 更新 templates/template_pack.blueprint.json

输出：
- TemplatePack（controller/model/view/migration）

通过标准：
- 每个模板具备 placeholder 清单与适配条件
- 每个模板都注明“何时不该套用”

## 阶段 5：生成规格（Spec）
执行：
- 使用 prompts/04_resolve_spec.md
- 产出 Spec（符合 schemas/spec.schema.json）

额外要求：
- 输出 `assumptions`、`evidence`、`confidence`、`ambiguities`

通过标准：
- 默认 module=Admin
- 默认 base_controller=BackendBaseController
- migration 前缀=typecho_
- 对低置信度字段给出“待确认项”

补充产物：
- 示例：.skill/examples/article.spec.json

## 阶段 6：预览（RenderPlan + Diff）
执行：
- 使用 prompts/05_render_artifacts.md 输出 RenderPlan
- 依据 RenderPlan 渲染目标文件文本
- 使用 prompts/06_preview_diff.md 输出 unified diff（默认 dry-run）

通过标准：
- 显示新增/修改/覆盖类别
- 给出冲突风险提示
- 标记“基于假设的变更块”

补充产物：
- Schema：.skill/schemas/render_plan.schema.json
- 示例：.skill/examples/article.render_plan.json

## 阶段 7：确认与沉淀（关键增量）
执行：
- 用户确认后（approve/edit/reject），记录本轮结论
- 将“被验证正确/错误的推断”回写上下文

输出：
- 变更清单
- 未覆盖项提示
- 迭代记忆（本轮新增模式、修正点、剩余歧义）

通过标准：
- 仅写入批准文件
- 完整记录目标路径
- 形成下轮可复用证据

---

## 迭代精度策略（每轮必须做）
1. 本轮新增证据 >= 1 条。
2. 本轮歧义项减少或更具体（即使未归零）。
3. 本轮“低置信度推断”数量不高于上一轮，或解释更充分。
4. 如果遇到新类型需求，将其归类并更新 context/patterns 的边界说明。
