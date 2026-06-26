# Template Library Architecture

模板能力分 4 层，不要再把它混成一坨硬编码：

## 1. Provider

模板来源。

例子：
- `islide`
- 后续更多公开模板库
- 私有模板库

Provider 只负责说明“模板从哪里来”，不直接参与渲染。

## 2. Family

模板家族。

例子：
- `board_evidence`
- `proposal_consulting`
- `research_editorial`
- `hero_dark_launch`
- `editorial_campaign`
- `training_manual`
- `clean_report`

Family 决定：
- 适用场景
- 封面语法
- 常见页型
- 默认配色倾向
- 版式节奏

## 3. Page Recipe

页面级语法。

例子：
- `agenda_grid`
- `decision_close`
- `training_concept_map`
- `audience_story`
- `process_map`

Page recipe 决定某类 section 应该落成什么结构，而不是只说“这一页好看”。
每个 page recipe 至少要能回答：
- 这页的结论是什么
- 这页的支撑证据是什么
- 这页的主视觉承担什么角色
- 这页在异步阅读时是否也成立

## 4. Rendering

导出器的责任只是把已选中的 page recipe 渲染出来。

导出器不该自己重新决定：
- 用哪个模板库
- 用哪个 family
- 用什么配色

这些应该在 design stage 的 template selection 阶段完成。

## Public Contract

公开 skill 层只需要约束这些概念边界：

- 当前选择的是哪个 provider
- 当前选择的是哪个 family
- 当前页面集合采用了哪些 page recipe
- 每个 page recipe 对应的结论 / 证据 / 视觉职责是否明确
- deck 是否产出了可检查的 template selection artifact

## Rule

- 新增模板库时，优先补全 provider 和 family catalog，不要先改导出器。
- 新页型先写成 recipe，再决定是否需要新增渲染器。
- 如果只是“换一个模板名字”，但没有 page recipe 差异，这不算真正新增模板能力。
- 不要让整份 deck 退化成同一种 recipe 的重复堆叠。
