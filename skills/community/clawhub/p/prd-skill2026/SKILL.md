---
name: product-prd-writer
description: >-
  Generate product requirement documents (PRD) with a complete structure for product design and requirement writing.
  Use when the user asks for PRD, 产品需求文档, 产品需求, 需求文档, or product requirements.
---

# Product PRD Writer

## Instructions
When activated, help the user design and write a PRD in Chinese.

### 1) Intake & Clarify
First, read the user’s prompt and extract any given information:
- 产品/业务背景与问题
- 目标与成功标准
- 用户角色与使用场景
- 范围（做/不做）、约束、时间线
- 现有系统/数据、依赖、风险

If key information is missing, ask up to 6 clarifying questions. Prefer questions that unlock multiple PRD sections at once, such as:
- 产品阶段：新建还是改版？当前处于哪个阶段（0->1 / MVP / 增长迭代）？
- 目标用户是谁？核心场景是什么？（至少给出 1-3 个典型场景）
- 成功标准/KPI是什么？如何量化？
- 本次要做的范围与不做的范围分别是什么？
- 关键约束是什么？（技术/合规/平台/成本/进度）
- 交付节奏：期望里程碑与上线时间？

If the user cannot answer, proceed with “明确假设”并在 PRD 中标注 “待确认”字段。

### 2) PRD Structure (generate a full doc)
Always output a complete PRD with the following sections (use Markdown and Chinese headings):

1. 摘要（1 段话 + 目标）
2. 背景与问题定义（现状、痛点、为什么现在做）
3. 目标与成功标准（KPI、指标口径、达成方式）
4. 非目标（不做什么）
5. 目标用户与使用场景（角色、旅程/场景）
6. 需求概览（按优先级/模块做总览）
7. 功能需求（逐条列出，可表格化）
8. 非功能需求（性能、安全、可用性、合规、可维护性等）
9. 交互/原型要点（用文字描述关键流程与交互状态）
10. 数据埋点与分析（事件、字段、用于衡量 KPI 的逻辑）
11. 权限与流程（如适用）
12. 验收标准（可测试、可核查）
13. 里程碑与发布计划
14. 依赖、风险与对策
15. 开放问题与待确认清单（与“假设”对应）

### 3) Requirement Detailing Rules
For every functional requirement, use this minimum schema:
- 编号：FR-xxx
- 标题：一句话描述“用户能做什么”
- 优先级：P0 / P1 / P2（默认 P1）
- 用户价值：为哪个用户解决什么问题
- 前置条件：触发需要满足的条件（如登录/权限/状态）
- 业务规则：关键规则、边界与例外
- 交互要点：关键页面/组件/状态（成功/失败/加载/空状态）
- 数据与埋点：相关事件与关键字段（若适用）
- 验收标准：至少 3 条，优先使用 Given / When / Then

For non-functional requirements, use:
- 编号：NFR-xxx
- 指标目标：如响应时间、可用性、并发、安全等（可量化则量化）
- 验证方式：如何测试/如何验收
- 风险与替代：无法达到时的处理方案

### 4) Prototype & Interaction (text-only)
Since the agent cannot assume access to design tools, describe:
- 核心页面/流程图（用步骤化文字）
- 关键交互状态（加载/空/错误/重试/权限不足）
- 关键字段与表单校验规则（如适用）

If the user provides wireframe or screenshots text, integrate them; otherwise propose a sensible baseline flow and mark “待确认”.

### 5) Reverse Review (quality gate)
Before finalizing, do a quick consistency check:
- 每个目标/成功标准都能追溯到具体需求或埋点事件
- “非目标”不会与“功能需求”冲突
- 需求条目足够可测试（有验收标准/边界条件）
- 优先级合理（P0 必须覆盖 MVP 必需）
- 风险/依赖覆盖至少：数据、权限、合规、性能、上线回滚

### 6) Output Format Preferences
Default to:
- 直接给出 PRD 终稿（不只给大纲）
- 保持可读性：使用表格用于“需求概览”和“依赖清单”
- 不要输出与 PRD 无关的冗长背景

### What to Ask the User Next
If the PRD 已足够推进，给出下一步建议（最多 3 条），例如：
- 需要补齐的输入
- 立即可做的原型/评审活动
- 需求拆分与排期建议

## Example
用户输入（示例）：
“帮我做一个 PRD：一键补贴申请，面向新用户，减少申请流程。”

Skill 输出（示例摘要）：
1) 摘要：...
2) 背景与问题定义：...
3) 目标与成功标准：...
4) 功能需求：FR-001（P0）...

