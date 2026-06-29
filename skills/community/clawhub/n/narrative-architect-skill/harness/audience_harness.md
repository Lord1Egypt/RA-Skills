# Audience Harness

## Purpose

Audience Harness checks whether the output is appropriate for the target audience.

Audience adaptation is not simply changing tone. It is rebuilding the path from the audience's current understanding to the intended understanding.

This harness prevents the skill from producing text that is technically correct but hard to understand, or simple but insulting.

## What It Checks

The harness checks:

1. Who is the audience?
2. What can they already understand?
3. What terms are likely unfamiliar?
4. What do they care about?
5. What may they misunderstand?
6. What entry point should the explanation use?
7. Does the language respect the audience?
8. Does the output answer their practical question?

## Audience Types

Possible audience labels:

```text
zero_ai_background
general_public
customer_first_touch
investor_nontechnical
business_executive
technical_team
expert_reader
internal_team
media
student
```

## Checkpoints

### 1. Entry Point Fit

The first sentence should match the audience's entry point.

For zero-AI-background audience:

Bad:

```text
Harness engineering is a model-runtime constraint layer.
```

Better:

```text
AI can give a fluent answer, but it can also make mistakes that are hard to notice.
```

For technical audience:

Acceptable:

```text
Harness engineering adds checkable control points between model generation and task execution.
```

### 2. Terminology Budget

For non-technical audiences, limit technical terms.

Rules:

```text
zero_ai_background: 0-2 technical terms, explained immediately
general_public: 2-4 terms, explained in context
technical_team: technical terms allowed if precise
```

### 3. Respect Rule

Do not treat simple explanation as childish explanation.

Avoid:

```text
像小朋友一样理解
很简单哦
不用懂技术
```

Prefer:

```text
A clearer entry point is...
The practical issue is...
A useful way to understand it is...
```

### 3a. Child Audience Rule

When the audience is children:

- use one central analogy only — do not stack game metaphors;
- keep the real-world object lightly visible — the child should sense there is a real product behind the story;
- avoid stacking multiple game metaphors — "like a game" is acceptable as one entry, not as three consecutive game references;
- do not over-promise magical speed or guaranteed success — "两分钟" must be qualified, not presented as magic;
- explain through: risk → map → path → trying-before-spending — this sequence is concrete and respects the child's intelligence;
- simple does not mean childish — the language can be clear without being babyish.

Fail if:
- the real mechanism is replaced by a game metaphor rather than explained through it;
- the output promises "always works" or "super fast" without qualification;
- the tone talks down to the child;
- multiple game references stack into a genre performance rather than an explanation.

### 4. Practical Question

The output should answer the question the audience actually has.

Examples:

```text
Why should I care?
What can go wrong?
How does this help me decide?
Why is the old way not enough?
```

### 5. Trust Barrier

The output should address the likely reason the audience may not believe or care.

Examples:

```text
sounds like jargon
sounds too magical
sounds like marketing
sounds too technical
sounds too vague
```

## Failure Modes

Fail if:

1. The first sentence assumes insider knowledge.
2. The output is technically correct but inaccessible.
3. The explanation uses too many abstract nouns.
4. The text simplifies by removing the real mechanism.
5. The audience is treated as unintelligent.
6. The draft uses a metaphor but never explains the mechanism.
7. The output does not answer why the audience should care.
8. Style increases cognitive burden.

## Severity

```text
hard_fail:
 - wrong audience entry point
 - major unexplained terminology
 - audience cannot understand the main value

soft_fail:
 - slightly too abstract
 - too many framework words
 - analogy overused
```

## Rewrite Rule

If Audience Harness fails, rewrite using:

```text
audience:
What do they already understand?

entry point:
What familiar risk, pain, or scene should open the explanation?

mechanism:
What is the simplest accurate explanation?

value:
Why does it matter to this audience?
```

Then produce a continuous final text unless the user asks for analysis.

## Output Instruction

Do not show audience mapping by default.
Show brief audience framing only when:

1. the user asks for audience-specific output;
2. the user says the previous version was hard to understand;
3. the user is testing the skill;
4. audience choice materially changes the explanation.
