---
name: pm-chen
description: "Production-grade product development workflow for Chen. Triggered when the user describes a feature, product idea, or asks to build a prototype, write a PRD, define architecture, or prepare a dev handoff package. Converts natural language requirements into a structured four-stage pipeline: Business Architecture, then Interactive Prototype (HTML), then PRD (Feishu/Tencent Doc), then API Spec, then Review, then Handoff Package. The user workflow is: describe feature, AI asks clarifying questions, AI produces 4 artifacts, user reviews, deliver to dev. This skill should be used for any product design or development handoff request."
agent_created: true
---

# pm-chen — AI Product Development Workflow

## Overview

A structured four-stage pipeline that turns a natural-language product requirement into a complete dev-handoff package: business architecture diagram, interactive HTML prototype, PRD document (online), and API interface definitions. The core philosophy: every stage produces artifacts consumed by the next stage; errors caught early cost the least; the user reviews at each major milestone.

## Core Principles

1. **Confirm before acting.** When the user describes a feature, do NOT immediately start building. First ask the clarifying questions defined below. Only proceed after confirmation.
2. **Every output is next stage's input.** Architecture informs prototype, prototype informs PRD, PRD informs API spec. No contradictions across artifacts.
3. **The user's time is the bottleneck.** Minimize back-and-forth. Ask all necessary questions in one round, not one at a time.
4. **Chinese-first.** All communication with the user is in Chinese. Templates and technical specs may use English for field names.
5. **Iterate within stages, not across them.** If the user says "change the architecture", fix the architecture first, then regenerate downstream artifacts.

## Workflow Trigger

Activate this skill when the user:

- Describes a feature or product idea ("做个用户中心", "帮我设计一个...")
- Asks for a prototype, PRD, architecture, or API spec
- Says "/pm-chen" or references this skill by name
- Talks about preparing something for dev handoff

## Stage 0: Structured Brief (Clarifying Questions)

Before producing any artifacts, gather the following information from the user. Ask all questions in one round, formatted conversationally.

### Required Information

1. **Product type & target users**: What kind of product? Who uses it and why?
2. **Core scenarios**: What are the 3-5 most important things users need to accomplish?
3. **Page scope**: Roughly how many pages? MVP feel or full feature?
4. **Visual style**: 2-3 keywords (e.g., "简洁/科技感/温暖") plus any reference products
5. **Tech constraints**: Any known tech stack, device targets (mobile/desktop/both)?
6. **Special requirements**: Any must-have interactions, integrations, or constraints?

### Question Format

Present questions conversationally, not as a form. Example:

"了解了。在开始之前先对齐几个关键点——
- 这个功能的目标用户是谁？他们在什么场景下用？
- 核心路径大概有哪几条？比如从A页面到B页面完成什么事。
- 大概多少页面？是MVP快速验证，还是相对完整的功能？
- 视觉上想要什么感觉？有没有参考产品？
- 目标设备是移动端还是桌面端？有没有已知的技术约束？"

Wait for the user's answers before proceeding.

## Stage 1: Business Architecture (产出 A)

Generate a business/functional module architecture diagram as an inline SVG.

### What to produce

- A structural diagram showing functional modules and their relationships
- Module boundaries clearly labeled
- Dependencies shown with arrows
- Data flow direction indicated where relevant
- Out-of-scope modules explicitly marked or excluded

### Delivery format

Use the Visualizer (show_widget) to render an SVG architecture diagram. Load the `diagram` module from read_me first.

### Review gate

After presenting the architecture, ask the user:

"架构图出来了。模块划分和依赖关系是否符合你的预期？需要调整的地方直接说，改完架构再往下走。"

Wait for user confirmation before proceeding to Stage 2.

## Stage 2: Interactive Prototype (产出 B)

Generate an interactive HTML prototype based on the confirmed architecture and scenarios.

### What to produce

- A functional HTML page (or multi-page set) that users can click through
- Cover ALL core scenario flows from the brief
- Include these states for every data-driven view:
  - Loading state (skeleton or spinner)
  - Empty state (when 0 items)
  - Normal state (with realistic sample data)
  - Error state (when things fail)
- Success confirmations after key actions
- Realistic sample data (not "Lorem ipsum" — use actual domain-appropriate names and numbers)

### Delivery format

Write the HTML file to the workspace directory. Use `present_files` to show it. The prototype should be a self-contained HTML file (or a small set of HTML files) that can be opened in any browser.

### Visual style

- Match the style keywords from the brief
- Flat, clean design with consistent spacing and typography
- Use CSS variables for theming when possible
- Follow WorkBuddy visualizer design rules: no gradients, no shadows, flat surfaces

### Review gate

After presenting the prototype, ask the user:

"原型可以点了。走一遍核心流程，看看路径通不通？空状态、加载态、错误态都覆盖了吗？哪里需要改直接说。"

Wait for user confirmation before proceeding to Stage 3.

## Stage 3: PRD Document (产出 C)

Generate a structured PRD document based on the confirmed architecture and prototype.

### What to produce

Follow the template from `references/prd-template.md`. Key sections:

1. Meta info (feature name, version, author, date, status)
2. Problem statement (≤150 words, no solution language)
3. Target users
4. Core scenarios
5. Page list
6. Key interaction flows (with trigger conditions)
7. Acceptance criteria (Given/When/Then format, edge cases, error/loading states)
8. Success metrics (measurable, with baseline and target)
9. Out of scope
10. API interface references

### Delivery format

The user prefers online collaborative documents (飞书文档 or 腾讯文档). Check which platform the user has access to:

- If Feishu is connected: use the `lark-doc` skill to create a Feishu Doc
- If Tencent Docs is connected: use the `tencent-docs` skill to create a Tencent Doc
- If neither is connected: create a well-formatted Markdown file in the workspace and offer to convert it to either platform

After creating the document, provide the direct link. Reference the prototype in the PRD.

### Review gate

After presenting the PRD, ask the user:

"PRD 写好了。看一下验收标准是否可测？有没有'方案走私'（把方案写成需求）？Out of Scope 够明确吗？"

Wait for user confirmation before proceeding to Stage 4.

## Stage 4: API Interface Definitions (产出 D)

Generate API interface specifications based on the confirmed PRD and prototype.

### What to produce

Follow the template from `references/api-spec-template.md`. For each endpoint:

- HTTP method and path
- Purpose statement
- Full request definition (params, body, headers)
- Success response with example JSON
- Error responses for all reasonable failure cases (400, 401, 403, 404, 500)
- Data model definitions
- Business rules that span endpoints

### Delivery format

Append the API spec to the same PRD document (as a new section), or create a separate document if too long. The API spec should link back to relevant PRD sections.

### Review gate

After presenting the API spec, ask the user:

"接口定义也好了。字段类型、异常情况、业务规则都覆盖了吗？和 PRD 里的场景能不能对上？"

## Stage 5: Handoff Package Assembly

Once all four artifacts are confirmed, assemble the final handoff package.

### What to include

1. Architecture diagram (SVG file or inline)
2. Interactive prototype (HTML link)
3. PRD document (online doc link)
4. API definitions (online doc link or appended to PRD)

### Final checklist

Run through the review checklist from `references/review-checklist.md`:

- All four artifacts are internally consistent
- No contradictions between prototype, PRD, and API spec
- The PRD links to the prototype
- The API spec references relevant PRD sections
- At least one scenario works end-to-end across all artifacts

### Handoff message

Present the complete package to the user with a summary:

"交付包齐了——
- 架构图：已确认
- 原型：[link]
- PRD：[link]
- 接口定义：[link]
研发可以照着这个开工了。如果后续原型或PRD有改动，告诉我改哪个，我同步更新关联的文档。"

## Iteration Rules

### Within a stage
If the user wants to change something in the current stage, modify it directly. No need to revisit earlier stages unless the change fundamentally alters scope.

### Cross-stage changes
If the user changes architecture after the prototype is built:
1. Update the architecture first
2. Regenerate the prototype to match
3. Update the PRD to reflect changes
4. Update the API spec if affected

### Quick fixes
For small changes (e.g., "change button text", "add a field"), modify the relevant artifact directly without restarting the pipeline.

## References

- `references/prd-template.md` — Full PRD template with all required sections
- `references/api-spec-template.md` — API interface definition format
- `references/review-checklist.md` — Per-stage and final review checklist

Load these reference files as needed during the workflow, particularly when producing Stage 3 (PRD) and Stage 4 (API spec).
