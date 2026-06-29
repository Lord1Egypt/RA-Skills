# Audience Visibility Policy

## Purpose

Decide whether the audience diagnosis should be shown to the user.

## Default Rule

Audience diagnosis is internal by default.

Only show audience framing when:
1. The user explicitly asks why a text is hard to understand.
2. The user asks for audience-specific writing.
3. The output would be confusing without clarifying who it is for.
4. The user is testing the writing skill or renderer.
5. The task involves explaining a technical concept to a non-technical audience.

## Visibility Modes

### hidden

Use when the user only asks for final copy.

Output:
- final text only

Do not show:
- Story Kernel
- ontology mapping
- audience diagnosis
- affective arc (emotional temperature, emotion path)
- harness checklist
- internal workflow

### visible_brief

Use when the user asks for audience adaptation or when the target audience materially changes the explanation.

Output format:

"This version is for: [audience]."

Then provide final text.

### visible_full

Use only when the user asks for analysis, critique, architecture design, or debugging.

Output:
1. Audience type
2. Prior knowledge
3. Likely confusion
4. Entry point
5. Forbidden terms
6. Language strategy
7. Final text

## Rule

If the user says:
- "普通人"
- "完全没有 AI 知识"
- "非专业听众"
- "客户第一次听"
- "投资人但不懂技术"
- "媒体"
- "小白"

Then the system must run Audience Cognition Mapper before drafting.

## Failure Mode

Do not begin with concepts that only make sense to insiders.

Bad:
"Harness engineering is not another prompt layer."

Reason:
This assumes the audience already understands models and prompts.

Better:
"AI can give impressive answers, but it can also make mistakes that are hard to spot."

Reason:
This starts from a human problem the audience can understand.
