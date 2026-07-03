---
name: grill-with-docs
description: >
  A relentless interview to sharpen a plan or design, which also creates docs
  (CONTEXT.md and ADRs) as we go. 当用户在有代码库的项目中说"对齐需求"、"讨论方案"、
  "设计功能"、"确认设计"，或任何触发 grilling 的场景，且当前目录有代码文件时触发。
  在对齐过程中同步维护 CONTEXT.md 和 ADR，建立共享语言。与 grill-me 的区别：
  grill-me 无代码库（纯对话），grill-with-docs 有代码库（对话 + 文档维护）。
---

# Grill With Docs — 有代码库的对齐

> 原始理念来自 Matt Pocock。在 Kimi 生态中，此 skill 为 model-invoked，
> 在有代码库时自动替代 `grilling`。

## 与 grill-me 的区别

| | `grill-me` | `grill-with-docs` |
|---|---|---|
| 代码库 | 无 | 有 |
| 保存文件 | 否 | 是（`CONTEXT.md` + ADR） |
| 领域建模 | 无 | 有（同步维护术语表） |
| 使用场景 | 任何计划/设计 | 在代码库上的计划/设计 |

## 核心原则

**对话中产生的每一个术语决策，都立即写入 `CONTEXT.md`。** 不要等会话结束，不要批量。当场写。

## 工作方式

### 1. 检测代码库

如果当前目录存在以下信号，判定为"有代码库"：
- `package.json` / `Cargo.toml` / `go.mod` / `pyproject.toml` 等
- `src/` / `lib/` / `app/` 目录
- `.git/` 目录
- 已存在的 `CONTEXT.md` 或 `CONTEXT-MAP.md`

### 2. 调用 grilling 循环

运行 `grilling` skill 的 relentless interview：
- 一次一个问题
- 提供推荐答案
- 等待用户确认
- 遍历决策树的所有分支

### 3. 同步维护 CONTEXT.md

在 grilling 过程中，每当一个术语被确定：
- 立即读取 `CONTEXT.md`（如果存在）
- 添加新术语到对应分组
- 更新定义和关系
- 如果 `CONTEXT.md` 不存在，创建它

**规则**：
- 只包含领域术语，不包含实现细节
- 定义一行搞定：是什么，不是做什么
- 关系用 bold 术语名

### 4. 同步创建 ADR

在 grilling 过程中，每当遇到需要记录的架构决策：
- 检查是否满足 ADR 三条件（难逆转、没有上下文会惊讶、有真实权衡）
- 如果满足，询问用户是否记录
- 创建到 `docs/adr/000X-xxx.md`

### 5. 与代码交叉验证

当用户描述某个行为时，检查代码是否一致。如果发现矛盾：
- 指出矛盾
- 询问用户哪个是对的（代码还是描述）
- 如果描述是对的，标记代码需要更新；如果代码是对的，更新描述

### 6. 完成标准

- 决策树的所有分支已解析
- `CONTEXT.md` 已更新（如果产生了新术语）
- ADR 已创建（如果需要）

## 触发场景（中文关键词）

- 在有代码库的项目中触发 `grilling` 的所有场景
- "在这个项目里"
- "在代码里"
- "当前目录"
- "这个项目"
- "代码库"

## 关联技能

- 调用 `grilling`（底层面试循环）
- 调用 `domain-modeling`（同步维护术语和 ADR）
- 前置：`codebase-design`（设计模块时确定术语边界）
- 后置：`to-prd`（对齐后合成 PRD）
- 后置：`handoff`（长会话后压缩上下文）
