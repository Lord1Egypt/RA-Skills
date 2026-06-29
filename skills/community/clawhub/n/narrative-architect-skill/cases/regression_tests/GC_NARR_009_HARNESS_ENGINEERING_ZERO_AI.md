# GC_NARR_009_HARNESS_ENGINEERING_ZERO_AI

## Task

Explain "harness engineering" in around 300 Chinese characters.

## Target Audience

完全没有 AI 技术背景，但需要理解为什么 AI 不能直接拿来做重要工作的人。

## Required Behavior

The system must:
1. Identify audience as zero_ai_background.
2. Use risk-first or scene-first entry.
3. Avoid opening with "prompt", "model", "runtime", or "workflow".
4. Avoid exposing Story Kernel.
5. Avoid bullet list.
6. Use at most one analogy.
7. Explain why harness matters.
8. Avoid overclaiming.

## Bad Output Pattern

```text
Harness engineering 不是给模型再写一层提示词，而是在模型和真实任务之间加一套可检查的约束。
```

Why bad:

* assumes the audience understands model and prompt
* begins with insider contrast
* too abstract for zero-AI audience

## Good Output Pattern

```text
AI can give a fluent answer, but it can also make mistakes that are hard to notice: using the wrong fact, sounding too certain, or changing the meaning of source material.
```

Why good:

* starts from visible risk
* does not require AI knowledge
* creates a reason to care

## Golden Output

AI 可以写出很顺的答案，但它也会犯一些不容易马上看出来的错：把不确定的事说得很肯定，漏掉关键条件，或者把原始材料的意思改偏。Harness engineering 做的，就是在 AI 的结果真正被使用前，加上一套检查机制。

它有点像飞机起飞前的检查单。检查单不会替飞行员开飞机，但会提醒哪些关键步骤不能漏。放在 AI 里，harness 负责检查事实有没有越界、语气有没有误导、重要信息有没有被改写。它的价值不是让 AI 更会说，而是让 AI 在重要工作里更可靠、更容易复盘，也更容易持续改进。
