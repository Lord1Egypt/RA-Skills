# Decision Guide

Use this guide when deciding whether to transform, clarify, or bypass.

## 1. Transform

Choose **transform** when the user wants a stronger prompt for a task that an AI could continue working on.

Common signals:
- 写一个脚本 / 页面 / 接口 / 工具
- 设计一个原型 / MVP / PRD 草稿
- 规划一个复杂任务或多步骤流程
- 需要特定输出格式、约束条件、角色或验收标准

Examples:
- `@prt 帮我写一个 Python 脚本，批量重命名文件`
- `@prompt 帮我设计一个面向独立开发者的 SaaS 登录页原型`
- `@prt 帮我整理一个 AI 自动运营工作流`

## 2. Clarify

Choose **clarify** when a missing detail would meaningfully change the prompt.

Ask only 1 to 3 questions.

But do not treat `1 to 3` as a target. Ask the fewest questions that unblock the task.

High-impact missing details often include:
- target platform: web / mobile / desktop / backend / script
- target deliverable: code / prototype / PRD / task plan
- user or audience: who it is for
- technical stack: only when the stack materially changes the solution
- scope: especially for broad requests such as admin systems or full products

Examples:
- `@prompt 帮我做一个电商后台`
- `@prt 帮我设计一个管理系统`
- `@prompt 帮我做一个 AI 产品`

## 3. Transform with Assumptions

Use assumptions when the gaps are modest and common defaults are reasonable.

Good assumption cases:
- the request is narrow enough that a default does not distort the result
- the user likely wants speed over interrogation
- the assumptions can be stated in 1 to 3 short bullets

Example:
- `@prt 帮我做一个记账 App`

Reasonable assumptions might be:
- 面向个人用户
- 移动端优先
- 核心功能包括记账、分类、统计

## 4. Bypass

Choose **bypass** when the prefix is present but the content is not really a prompt-writing task.

Typical bypass cases:
- greetings
- weather
- jokes
- casual remarks
- simple factual questions
- low-value requests that do not benefit from prompt engineering

Examples:
- `@prt 今天天气怎么样？`
- `@prt 哈哈`
- `@prompt 你是谁`

On bypass:
- answer naturally
- do not output the prompt template
- do not force prompt-logic explanations
- avoid internal terms like `旁路`
- prefer direct user-facing wording
- for greetings, usually just reply with the greeting itself
- if needed, use a very short bridge such as `这个我直接回你：`

## 5. Conflict Handling

If the user asks for mutually conflicting goals, do not quietly smooth it over.

Examples:
- "极简实现" and "企业级完整系统"
- "只要几十行" and "包含完整权限、审计、报表、工作流"

In these cases:
- point out the tension briefly
- ask the user which side to prioritize

## 6. Post-generation Follow-up Rule

After generating a prompt, reset back to normal conversation unless the user explicitly keeps working on that prompt.

Important rules:
- `@prt` / `@prompt` affects only that one user turn.
- Do not assume the generated prompt's subject becomes the next default topic.
- If a later non-prefixed reply such as `做2` or `继续优化` could refer to multiple things, ask one short clarification question.
- If recent context shows the user is testing or discussing the skill itself, prefer that interpretation over the content of the generated prompt.

Bad pattern:
- user tests the skill with a paper-search prompt
- assistant generates a good prompt
- user says `做2`
- assistant wrongly continues the paper topic instead of checking whether `2` refers to the earlier skill discussion

Preferred recovery:
- `你是指继续做 skill 优化，还是继续优化刚刚那条 Prompt？`

## 7. Post-output Restraint Rule

After a successful prompt transformation, do not eagerly append a long tail of suggestions, branching plans, or numbered menus.

Good behavior:
- end cleanly after the required output contract
- optionally add one short closing sentence if it truly helps
- wait for the user to decide the next step

Bad behavior:
- adding `1 / 2 / 3` options by default
- proposing multiple future paths when the user did not ask
- turning a finished prompt delivery into a new round of sales-like prompting

Reason:
- excessive endings create ambiguity for short follow-ups like `做2`
- they also make the interaction feel more verbose and less product-like

## 8. Simplicity Rule

Do not inflate a small request into a giant enterprise template.

If the task is simple:
- use fewer sections
- keep the prompt compact
- keep the logic notes short

If the task is large:
- use more structure
- surface constraints and acceptance criteria clearly
