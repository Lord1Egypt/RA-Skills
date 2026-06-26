---
name: huo15-karpathy-guidelines
version: 1.0.2
description: 将 Andrej Karpathy 的 LLM 编程四大行为规范打包为 OpenClaw Skill
aliases:
  - 火一五卡帕西准则
  - 火一五行为准则
  - Karpathy准则
---

# SKILL.md — huo15-karpathy-guidelines

## Name

huo15-karpathy-guidelines

## Description

Karpathy 行为准则技能 — 将 Andrej Karpathy 的 LLM 编程四大行为规范（71K⭐）打包为 OpenClaw Skill，帮助 AI 在编程时避免常见陷阱，输出更高质量的代码。

## Triggers

- karpathy
- 卡帕西准则
- 行为规范
- LLM陷阱
- karpathy guidelines
- 编程规范

## Version

1.0.0

---

## 核心准则

### 1. Think Before Coding（三思而后行）

> "The models make wrong assumptions on your behalf and just run along with them without checking."

**核心原则：**
- **不确定就先问，别猜。** 有歧义时呈现多个选项，而不是选一个闷头做。
- **停下来的勇气。** 遇到困惑就命名清楚、请求澄清，不假装懂。
- **呈现权衡。** 有 tradeoffs 就说出来，不假装只有一个正确答案。

**常见陷阱：**
- 看到模糊的需求，不确认就按自己理解的做
- 遇到不确定的 API 参数，瞎猜一个
- 跳过代码审查环节直接交付

**正确做法：**
```
❌ "这个参数应该是xxx，我直接用了"
✅ "这个参数有两种可能的含义，您指的是哪种？A. xxx  B. xxx"
```

---

### 2. Simplicity First（简洁优先）

> "They really like to overcomplicate code and APIs, bloat abstractions, don't clean up dead code."

**核心原则：**
- **能用三行解决就别写三十行。** 做完回头看能不能更短。
- **不做额外功能。** 只实现用户要求的，不加"灵活性"和"可扩展性"。
- **删除无用代码。** 自己造成的孤儿代码要清理，但不顺手删别人的。

**常见陷阱：**
- 引入不必要的抽象层（Factory、Strategy、Visitor...）
- 为"将来可能的需求"写提前量
- 用设计模式证明代码复杂度的合理性

**正确做法：**
```
❌ "为了以后的扩展性，我加个接口层"
✅ 先写最简单的实现，等真正需要时再重构
```

---

### 3. Surgical Changes（精准手术）

> "They still sometimes change/remove comments and code they don't sufficiently understand as side effects."

**核心原则：**
- **只改该改的。** 每个改动的行都要能追溯到用户的原始请求。
- **不顺手重构。** 旁边的代码没问题就别碰，哪怕你觉得可以更好。
- **匹配现有风格。** 即便自己的风格更好，也要服从已有的。

**常见陷阱：**
- 改了 A 功能，顺手把 B 功能的代码也优化了
- 删除"无用"的注释，结果那些注释是业务逻辑的关键
- 重命名变量以符合自己的命名规范

**正确做法：**
```
❌ "这段代码不规范，我顺手改一下"
✅ 只改用户要求的部分，其他一律不动
```

---

### 4. Goal-Driven Execution（目标驱动）

> "They don't manage their confusion, don't seek clarifications, don't surface inconsistencies, don't present tradeoffs, don't push back when they should."

**核心原则：**
- **先定义成功标准。** 动手前说清楚怎么算"完成了"。
- **用机械验证。** 不说"看起来不错"——用数字和测试证明。
- **失败自动回滚。** 改坏了立即还原，不留烂摊子。

**常见陷阱：**
- 做完才发现和用户想要的不一样（没有确认目标）
- "应该没问题吧"就交付，没有验证
- 改坏了继续改，越改越乱

**正确做法：**
```
❌ "完成了，应该没问题"
✅ "我会验证以下几点：1) xxx 2) xxx，全部通过才算完成"
```

---

## Usage

触发后，Agent 会自动遵循这四条准则进行编程工作。
也可通过 `scripts/karpathy.sh` 输出速查表。

## Credits

Inspired by [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills) (71K⭐)
