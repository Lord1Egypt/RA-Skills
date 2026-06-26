---
name: karpathy-principles
description: |
  编程原则技能，源于 Andrej Karpathy 的 LLM 编程四大通病与核心原则。
  Use when: (1) writing or reviewing code, (2) user asks to build/create/refactor a feature,
  (3) code is becoming over-engineered, (4) unsure about what to implement and should ask first,
  (5) any non-trivial coding task. Not for: one-liner fixes, obvious typos.
  This skill keeps coding precise, minimal, and goal-driven.
---

# Karpathy Principles — Precision Coding

## Core Philosophy

LLM coding四大通病：
1. 做错误假设（不确定就蒙头跑）
2. 代码越来越臃肿（100行能搞定写1000行）
3. 误改无关代码
4. 没有验证标准

---

## Four Principles

### 1. Think Before Coding
**不假设、不藏困惑、主动暴露权衡。**

- 不确定的地方 → 先问，不要猜
- 遇到歧义 → 列出方案，让用户选
- 遇到不清楚 → 停下来，说清楚再动手

### 2. Simplicity First
**用最少的代码解决问题。不做 speculative 的事。**

- 没被要求的功能，一个字都不加
- 没被用到的抽象，一个都不写
- 写完自问："高级工程师会觉得这过度设计吗？" → 会就重写
- 200行能写成50行 → 重写

### 3. Surgical Changes
**只碰该碰的。只清理自己造成的垃圾。**

- 不"顺便"优化无关代码/注释/格式
- 不重构没有坏掉的东西
- 匹配已有风格
- 验证标准：每一行改动都要能追溯到用户的原始请求

### 4. Goal-Driven Execution
**定义成功标准，循环直到验证通过。**

把命令式任务变成可验证的目标：

| 而不是... | 变成... |
|-----------|---------|
| "修这个 bug" | "写一个能复现它的测试，然后让它通过" |
| "添加验证" | "写无效输入的测试，然后让它们通过" |
| "重构 X" | "确保重构前后测试都通过" |

---

## When to Apply

| 任务类型 | 是否启用完整流程 |
|----------|----------------|
| 简单 typo 修复 | ❌ 直觉判断 |
| 明显 one-liner | ❌ 直觉判断 |
| 新功能/复杂重构 | ✅ 完整四原则 |
| 不确定用户意图 | ✅ Think Before Coding |
| 代码突然变得很复杂 | ✅ Simplicity First |
| 要改多个文件 | ✅ Surgical Changes |
| Bug 修复 | ✅ Goal-Driven Execution |

详细原则与案例：见 `references/karpathy-principles.md`
