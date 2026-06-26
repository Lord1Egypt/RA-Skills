---
name: <skill-name>
description: "<描述：通过多轮对话收集需求后再行动。包含触发关键词。>"
license: Apache-2.0
metadata:
  author: <作者>
  version: "<major.minor.patch>"
  pattern: "inversion"
  interaction: "multi-turn"
---

# <Skill 名称> (Inversion)

<!--
Inversion 模式：Agent 先采访用户再行动。
分阶段提问，显式门控（"DO NOT start building until all phases are complete"）。

核心思路：
- 分 Phase 提问，收集完整需求
- 每个 Phase 有明确的完成条件
- 所有 Phase 完成后才进入 Synthesis（生成）阶段
- 防止 agent 在信息不足时就开始行动
-->

一句话概述：通过结构化采访收集完整需求，然后生成 <输出类型>。

## Architecture

```
User Request
    ↓
Phase 1: <领域1> 提问 → 收集答案
    ↓ (gate: all required answers collected)
Phase 2: <领域2> 提问 → 收集答案
    ↓ (gate: all required answers collected)
Phase N: <领域N> 提问 → 收集答案
    ↓ (gate: ALL phases complete)
Synthesis: 生成输出
```

## Instructions

**CRITICAL RULE**: DO NOT start building/generating until ALL phases are complete.
If the user tries to skip ahead, remind them which phase is pending.

### Phase 1: <领域名称>

**Goal**: Understand <what this phase collects>

Ask the following questions (adapt wording to context):

1. <问题1>
2. <问题2>
3. <问题3>

**Completion gate**:
- [ ] <条件1 已满足>
- [ ] <条件2 已满足>

**If user is unsure**: Offer these defaults: <defaults>

### Phase 2: <领域名称>

**Goal**: Understand <what this phase collects>

Ask the following questions:

1. <问题1>
2. <问题2>
3. <问题3>

**Completion gate**:
- [ ] <条件1 已满足>
- [ ] <条件2 已满足>

<!-- 按需添加更多 Phase -->

### Phase N: Confirmation

**Goal**: Confirm all collected information before proceeding

```
Present a summary of all collected answers:

Phase 1 (<领域1>):
  - <var>: <collected value>

Phase 2 (<领域2>):
  - <var>: <collected value>

Ask: "Is this correct? Should I proceed with generation?"
```

**Completion gate**:
- [ ] User explicitly confirms

### Synthesis

**Precondition**: ALL phases above are complete and confirmed.

```
1. Compile all collected variables
2. [If combined with Generator] Load template from assets/
3. Generate output using collected context
4. Present output for review
```

## Phase Design Guidelines

<!-- 给 Skill 作者的指导 -->

- 每个 Phase 聚焦一个领域，不要混杂
- 问题按依赖关系排序（前面的答案可能影响后面的问题）
- 必须提供 "unsure" 的默认值选项
- Phase 数量建议 2-4 个，太多会让用户疲劳
- 最后一个 Phase 总是 Confirmation

## Directory Structure

```
<skill-name>/
├── SKILL.md                    # 主文件：Phase 定义 + 门控规则
├── references/                 # 领域知识（辅助提问）
│   └── <domain-context>.md     # 帮助 agent 提出更好问题的背景知识
└── assets/                     # 输出模板（如果结合 Generator）
    └── <output-template>.md
```

## Anti-Patterns

| Pattern | Problem |
|---|---|
| 信息不全就开始行动 | 输出质量差，需要反复修改 |
| 一次问太多问题（>5个） | 用户认知过载 |
| 没有完成门控 | Agent 可能跳过关键问题 |
| 不提供默认值 | 用户不确定时被卡住 |
| Phase 之间有循环依赖 | 无法线性推进 |
| 不做最终确认 | 误解需求后浪费大量工作 |
