# Dissatisfaction Recovery Policy

## Purpose

This policy defines how the skill should respond when the user is dissatisfied with an output.

User dissatisfaction is not noise. It is signal.

the skill should use dissatisfaction to identify whether the failure is in:

```text
communication context
relationship context
conversation purpose
recipient motivation
narrative authority
audience entry point
emotional arc
style
source fidelity
surface naturalness
```

## Core Rule

Do not automatically ask many follow-up questions.

If the user provides clear correction, reroute and rewrite.

If the user provides vague dissatisfaction, diagnose first and ask at most one high-leverage question.

## Dissatisfaction Types

### 1. Clear Context Correction

Examples:

```text
不是冷邮件，是朋友介绍。
不是给投资人，是给学者。
不是正式邮件，是微信消息。
不是销售，是方法论交流。
不是让对方买，是让对方愿意共同探讨。
```

Action:

```text
Do not ask follow-up.
Rerun relevant mappers.
Rewrite.
```

Required rerun:

```text
communication_context_mapper
conversation_purpose_mapper
recipient_context_mapper if available
narrative_authority_mapper
```

### 2. Missing Content

Examples:

```text
需要解释一下架构。
需要加上我们已经在三个国家运行。
需要更强调合作方向。
需要说明不是产品介绍。
```

Action:

```text
Do not ask follow-up.
Add missing content.
Run claim/source fidelity checks.
Rewrite.
```

### 3. Tone Complaint

Examples:

```text
太像冷邮件。
太销售。
太学术。
太 AI。
太平。
不够有主体性。
```

Action:

```text
Diagnose the likely failure.
Rewrite once.
Only ask if multiple interpretations remain.
```

### 4. Vague Dissatisfaction

Examples:

```text
不对。
不够好。
不像。
没有感觉。
还是差点意思。
```

Action:

First respond with a brief diagnosis:

```text
我判断问题可能在三处：关系语境、主张强度、情绪入口。
```

Then ask one high-leverage question:

```text
你更想修哪一处：关系不对、目的不清、主张不够强，还是情绪不够？
```

Do not ask a long questionnaire.

### 5. Strategic Reframe

Examples:

```text
我不是想见一面，而是要形成合作。
我不是推销产品，而是讲一个故事。
我想让合适的人爱上这个故事。
```

Action:

```text
Treat as a top-level repositioning.
Update story_not_selling principle.
Rerun conversation purpose, attraction filter, and narrative authority.
```

## Rewrite Priority

When user is dissatisfied, revise in this order:

```text
1. Communication purpose
2. Relationship context
3. Narrative authority
4. Audience entry point
5. Emotional arc
6. Style
7. Surface polish
```

Do not start from word-level edits unless the user asks for word-level edits.

## Follow-Up Question Rule

Ask a follow-up only if:

1. The user's goal is ambiguous.
2. The desired next action is unclear.
3. Multiple relationship contexts are possible.
4. A factual claim needs confirmation.
5. The output may create reputational risk.

Ask only one question at a time.

Preferred question:

```text
这次沟通你希望对方做出的最小动作是什么：回复、见面、给建议、介绍资源、共同设计课题，还是形成初步合作意向？
```

## Final Rule

When the user says an output is wrong, the skill should not defend the draft.

It should identify which layer failed and rebuild from that layer.
