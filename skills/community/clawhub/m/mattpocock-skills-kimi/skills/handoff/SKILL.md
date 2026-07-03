---
name: handoff
description: >
  Compact the current conversation into a handoff document so another agent or fresh
  session can continue the work. 当用户说"会话太长了"、"换一个新会话"、"交接一下"、
  "handoff"、"上下文满了"、"新开一个对话继续"，或在 grilling 对齐后需要分会话实现时触发。
  将当前进展、决策、待办项压缩为 markdown 文件，保存到当前 workspace。包含建议的后续
  skill 列表。不重复 PRD/ADR/issue 等已有内容，只引用路径。
---

# Handoff — 跨会话交接

> 原始理念来自 Matt Pocock。在 Kimi 生态中，此 skill 为 model-invoked，
> 在需要跨会话接力时自动触发。

## 何时触发

以下场景出现时，本 skill 应自动触发：

- 用户说"会话太长了"
- 用户说"换一个新会话继续"
- 用户说"交接一下"
- 用户说"handoff"
- 用户说"上下文快满了"
- 用户说"新开一个对话"
-  grilling 对齐后需要进入多会话实现阶段
- 当前会话 token 接近上下文上限（~120k tokens）

## 核心原则

**不要丢掉已完成的思考。** 会话的上下文是昂贵的，但已经做出的决策和探索是沉没成本。交接文档的价值是：让新会话**不重新问一遍已经问过的问题**。

## 工作方式

### 1. 提取关键信息

从当前会话中提取以下内容：

- **已完成的决策**：哪些分支已经解析，结论是什么
- **未完成的待办**：哪些分支还在讨论，需要什么信息
- **关键约束**：时间、资源、技术栈限制
- **已发现的坑**：已经排除的选项、已知风险
- **相关文件/文档**：PRD、ADR、Issue、代码路径（只引用，不复制）

### 2. 不重复已有内容

**Do NOT duplicate** 已经存在于其他文件中的内容：

- PRD → 引用路径或 URL
- ADR → 引用路径
- Issue → 引用编号
- 代码 diff → 引用 commit SHA 或文件路径
- 原型代码 → 引用路径

交接文档只补充**会话中产生的、但尚未写入任何文件**的信息。

### 3. 建议后续 skill

在文档末尾加入 **Suggested Skills** 部分，推荐下一个会话应该调用的 skill：

```markdown
## Suggested Skills

- `/grilling` — 如果有未解析的分支需要继续对齐
- `/domain-modeling` — 如果讨论中产生了新的领域术语
- `/tdd` — 如果下一个会话开始实现代码
- `/diagnosing-bugs` — 如果交接的是 Bug 修复上下文
- `/to-prd` — 如果需求已经对齐，需要合成 PRD
- `/implement` — 如果 PRD 已有，直接开始实现
```

### 4. 脱敏处理

Redact any sensitive information:
- API keys, tokens, passwords
- 个人身份信息（PII）
- 内部机密信息

### 5. 保存到当前 workspace

将交接文档保存到当前 workspace 目录下：

```
<workspace>/handoff-<timestamp>.md
```

例如：`handoff-20260616-143022.md`

**不要保存到系统 temp 目录。** 在 Kimi Work 中，workspace 是持久化的；temp 目录可能丢失。

### 6. 告知用户文件路径

保存后，明确告诉用户：

> 交接文档已保存到 `<workspace>/handoff-20260616-143022.md`
> 请在新会话中引用此文件，我会继续推进工作。

## 文档格式

```markdown
# Handoff — <简短主题>

## 会话背景
<当前在做什么，为什么交接>

## 已完成决策
- <决策 1：结论>
- <决策 2：结论>

## 未完成待办
- <待办 1：需要什么信息>
- <待办 2：需要什么信息>

## 关键约束
- <约束 1>

## 已知风险/已排除选项
- <坑 1>

## 相关文件
- PRD: `<path>`
- ADR: `<path>`
- Issue: `#<number>`
- 原型: `<path>`

## Suggested Skills
- <skill 1> — <为什么推荐>
- <skill 2> — <为什么推荐>
```

## 触发场景（中文关键词）

- "会话太长了"
- "换一个新会话"
- "交接一下"
- "handoff"
- "上下文满了"
- "新开一个对话"
- "继续"（在 grilling 对齐后）
- "分几步做"
- "多会话"

## 关联技能

- 前置：`grilling`（对齐后常常需要分会话实现）
- 后置：`grilling` / `tdd` / `diagnosing-bugs` / `to-prd` / `implement`（新会话根据上下文选择）
