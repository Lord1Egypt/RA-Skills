# Renderer: Zero AI Background

## Purpose

Explain AI-related concepts to people with no AI technical background.

This renderer must preserve accuracy without using insider vocabulary as the entry point.

## Audience Assumption

The audience:
- may have used ChatGPT or heard of AI
- does not understand models, prompts, agents, guardrails, evaluation, or runtime
- cares about practical reliability
- may distrust technical jargon
- understands ordinary work risks, checklists, quality control, and accountability

## Language Rules

1. Start from a familiar risk or scene.
2. Avoid insider terms in the first sentence.
3. Introduce technical terms only after the problem is clear.
4. Use at most one analogy in short outputs.
5. Do not list too many components.
6. Prefer continuous prose over bullet points.
7. Do not expose internal system workflow.
8. Avoid AI-style phrases:
 - 核心是
 - 本质上
 - 不是……而是……
 - 只做一件事
 - 从 A 到 B
 - 打造闭环
 - 赋能
 - 底层逻辑
9. Use concrete verbs:
 - 检查
 - 拦住
 - 发现
 - 改正
 - 记录
 - 复盘
10. Keep confidence bounded.
 Do not say "guarantee", "zero risk", or "always correct".

## Recommended Structure

For short explanations:

```text
risk scene
→ why ordinary AI output is not enough
→ what the mechanism does
→ why it matters
```

## Forbidden Structure

```text
definition
→ technical contrast
→ component list
→ slogan
```

## Example Topic: Harness Engineering

Bad opening:
"Harness engineering is not another prompt layer."

Good opening:
"AI can write a fluent answer, but it can also hide mistakes that are hard to spot."

## Output Style

Tone:

* concrete
* calm
* credible
* non-technical
* not childish

Sentence length:

* medium
* varied

Technical term budget:

* 1-2 terms maximum
* every term must be explained immediately
