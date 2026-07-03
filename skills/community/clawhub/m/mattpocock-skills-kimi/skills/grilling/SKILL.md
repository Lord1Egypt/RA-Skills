---
name: grilling
description: >
  Interview the user relentlessly about a plan or design until every branch of the
  decision tree is resolved. 当用户想要对齐需求、讨论计划、确认设计、
  stress-test a plan before building，或提到"对齐一下"、"帮我理清"、"想清楚"、
  "grill"、"讨论需求"、"设计确认"时触发。Ask questions one at a time, waiting for
  feedback on each before continuing. If a question can be answered by exploring the
  codebase, explore the codebase instead. 提供推荐答案但等待用户确认。
---

# Grilling — 需求对齐

> 原始理念来自 Matt Pocock。在 Kimi 生态中，此 skill 为 model-invoked，
> 自动在对齐场景触发。

## 核心原则

**没有人一开始就知道自己想要什么。** 软件开发最常见的失败模式是沟通偏差——你以为 AI 理解了，结果做出来才发现完全不是一回事。

修复方法是：**relentless interview**（ relentless 面试）。让 AI 反过来问你问题，直到设计的每个分支都被解析清楚。

## 工作方式

### 1. 逐分支遍历决策树

Walk down each branch of the design tree, **resolving dependencies between decisions one-by-one**.

不要一次问多个问题。一次只问一个，等用户回答后再继续。多个问题同时抛出会让人困惑。

### 2. 每个问题提供推荐答案

For each question, **provide your recommended answer** — 然后等待用户确认或调整。

推荐答案的作用是展示你理解的方向，而不是替用户做决定。

### 3. 能用代码回答的，用代码回答

If a question can be answered by exploring the codebase, **explore the codebase instead** of asking.

例如：用户说"这个功能是否已经在代码里实现了？" → 直接搜索代码，而不是问用户。

## 完成标准

Grilling 结束的标志：**决策树的所有分支都已解析，没有未解决的依赖**。

不要急于结束。如果你心中还有"这里可能还需要确认一下"的感觉，继续问。

## 触发场景（中文关键词）

以下关键词出现时，本 skill 应自动触发：

- "对齐一下需求"
- "帮我理清这个"
- "想清楚再动手"
- "讨论一下设计"
- "确认一下方案"
- "stress-test"
- "grill"
- "plan"
- "design"
- "方案"
- "设计"
- "需求"
- "计划"
- "思路"

## 关联技能

- 被 `grill-with-docs` 调用（有代码库时，对齐同时维护 `CONTEXT.md` + ADR）
- 被 `handoff` 前置（长会话需要交接时，先对齐再压缩）
- 被 `to-prd` 前置（对齐后合成 PRD）
