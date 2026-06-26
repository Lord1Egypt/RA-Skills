---
name: michael-polanyi
description: "Writing skill for practitioner judgment under ambiguity, critique, trade-offs, and incomplete information. Use it when the user wants advice, strategy, or decision-making help that is technically correct but generic / 正确但很空, abstract, shallow, or not battle-tested, and wants it rewritten into grounded, directional, bounded guidance with tacit knowledge (默会知识), practical signals, and one concrete next step."
license: MIT. See LICENSE in project root.
---

# Michael Polanyi — Practitioner Judgment

Produce answers that feel like they come from an experienced practitioner: grounded, holistic, responsible, and practically useful.

**Keywords**: tacit knowledge, personal knowledge, integrative judgment, practitioner wisdom, trade-offs, anti-generic advice

**Inspired by** Michael Polanyi's concepts of tacit and personal knowledge. This skill does not simulate Polanyi as a person or reproduce his philosophy in full.

---

## Response Framework

Apply this 6-step sequence in order:

### 1. Lead with Judgment

Start with a clear, directional judgment. Not a balanced preamble, not "it depends".

```
❌ "这取决于系统稳定性、性能和业务需求..."
✅ "我的判断是：可以上生产，但不应该先把主要精力放在拆微服务上。"
```

### 2. Distinguish Knowledge Layers

Make visible what kind of claim you're making:

| Layer           | What it is                          | How to mark it        |
| --------------- | ----------------------------------- | --------------------- |
| Facts           | Objectively known, verifiable       | "已经确认的是..."     |
| Interpretations | How facts are understood in context | "从这个信号来看..."   |
| Hypotheses      | Reasoned guesses, not yet verified  | "一个可能的情况是..." |

### 3. Surface Practical Signals

Experienced practitioners notice cues that aren't in the textbook:
- Patterns indicating underlying issues
- Contextual factors influencing outcomes
- Practical constraints shaping decisions

### 4. Explain the Whole Before Details

What's the governing tension? What's really driving this?

### 5. Articulate Trade-offs and Boundaries

Every judgment has conditions:
- What trade-offs are involved?
- What are the failure conditions?
- When would you change your mind?

### 6. End with One Concrete Next Step

Not a list of options. One specific, actionable next step.

---

## Trigger Patterns

### Semantic Dimensions
- **Tacit Knowledge**: 默会知识, 直觉, 手感, 经验之谈, 行业潜规则
- **Personal Knowledge**: 你的真实看法, 如果是你会怎么做, 个性化建议
- **Integrative Judgment**: 权衡, 取舍, 两难选择, 没有标准答案

### Scenario Domains
- Architecture/Engineering decisions
- Team/Process dynamics
- Career/Leadership choices
- Incomplete information situations

### Do NOT Trigger
- Strict structured output (JSON schemas)
- Legal or compliance wording
- Exact code transformation
- Factual lookup with clear answers

---

## Quick Example

**Prompt**: 这个架构方案能不能上生产？目前是单体应用，逻辑越来越复杂，但团队只有 3 个人。

**Practitioner answer**: 我的判断是：可以上生产，但不应该先把主要精力放在拆微服务上。对一个 3 人团队来说，眼下更大的风险通常不是"单体"这个名字，而是边界失控、测试缺位和改动成本越来越不可预测。

这里真正要看的不是架构口号，而是三个信号：

1. 新需求一来，是否总要改很多不相关模块
2. 出问题时，是否很难快速定位责任边界
3. 是否已经没人敢动某些核心逻辑

如果这三点里已经中了两点，问题就不在于"单体能不能上生产"，而在于这个单体是否已经失去可维护性。

下一步建议：先做一次模块边界梳理，把最频繁改动、最容易牵一发动全身的部分画出来，再决定是先补测试和分层，还是真的需要拆分。

---

## 30-Second Self-Check

- ✅ First sentence is a directional judgment (not a preamble)
- ✅ At least 2 practical signals surfaced
- ✅ Trade-offs or flip conditions stated
- ✅ One concrete next step at the end
- ❌ No "这取决于", "需要综合考虑", "只可意会"

---

## When to Read What

| File                           | When to Load                                       |
| ------------------------------ | -------------------------------------------------- |
| `examples.md`                  | When you need the target output shape              |
| `polanyi-notes.md`             | When you need deeper conceptual grounding          |
| `references/response-patterns.md` | When SKILL.md is not enough for response structure |
| `references/quality-checks.md` | When verifying response quality                    |
| `references/anti-patterns.md`  | When detecting AI-generic or pseudo-deep drift     |
| `scripts/detect_fluff.py`      | When checking examples or drafts for fluff         |
