# Prompt Patterns

Use these patterns as flexible shapes, not rigid templates. Keep the output proportional to the task.

## 1. Simple Coding Task Pattern

Use for small scripts, utilities, or focused coding requests.

Recommended shape:
- role
- goal
- constraints
- output requirements

Example structure:

```text
你是一名经验丰富的 [语言/领域] 工程师。

目标：
[用户要完成的事]

约束条件：
- [技术约束]
- [环境约束]
- [依赖限制]

输出要求：
- 提供完整可运行代码
- 简要说明关键实现思路
- 若有潜在边界情况，一并说明
```

## 2. Prototype / Product Idea Pattern

Use for landing pages, SaaS prototypes, MVP ideas, and PRD-like requests.

Recommended shape:
- role
- target audience
- objective
- required modules or sections
- output format

Example structure:

```text
你现在是一位资深产品经理兼 UX 设计顾问。

背景：
[用户场景和目标用户]

目标：
[要设计的页面 / 原型 / MVP]

请完成以下任务：
1. 明确页面/产品核心目标
2. 拆解关键模块
3. 说明每个模块的作用
4. 给出建议的信息层级与交互重点

输出格式：
- 先给整体方案概述
- 再分模块说明
- 最后补充设计建议或注意事项
```

## 3. Complex Multi-step Task Pattern

Use for larger tasks that need structure, sequencing, and success criteria.

Recommended shape:
- role
- context
- goal
- task breakdown
- constraints
- acceptance criteria
- output format

Example structure:

```text
你是一位擅长系统设计与任务拆解的高级顾问。

背景：
[上下文]

目标：
[最终目标]

请按以下要求执行：
1. 先拆解任务阶段
2. 识别关键风险与依赖
3. 为每个阶段给出具体产出
4. 若存在多种可行路径，说明推荐方案及理由

约束条件：
- [限制 1]
- [限制 2]

验收标准：
- [成功标准 1]
- [成功标准 2]

输出格式：
- 使用清晰的小节
- 先总后分
- 最后给出建议的下一步行动
```

## 4. Assumptions Section Pattern

When using assumptions, keep them outside the prompt body in the assistant response.

Good pattern:

```markdown
**已做如下假设：**
- 面向个人用户
- Web 端优先
- 默认使用 Python 实现
```

## 5. Prompt Summary Pattern

Keep the summary minimal.

Default rule:
- use 2 bullets
- use 3 only for clearly complex tasks
- each bullet should be one short sentence
- say what the prompt did, not why it did it

Strong examples:
- 限定了时间范围。
- 限定了文献来源和真实性要求。
- 补了输出结构和选题建议模块。

Avoid:
- very long bullets
- textbook-style prompt theory
- phrases like `是为了`
- repeating obvious parts of the user's own request
- explaining every section of the prompt
