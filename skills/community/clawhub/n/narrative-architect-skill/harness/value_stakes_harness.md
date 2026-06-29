# Value & Stakes Harness

## Purpose

Value & Stakes Harness checks whether the narrative has a meaningful value at risk.

A text may be clear and well-written but still weak if the audience cannot see what matters.

This harness ensures that the skill does not produce empty explanation, decorative storytelling, or inflated drama.

## What It Checks

The harness checks:

1. What value is being pursued?
2. What value is at risk?
3. What happens if the protagonist fails?
4. What improves if the protagonist succeeds?
5. Is the cost specific enough?
6. Is the urgency real or exaggerated?
7. Does the value shift match the evidence?

## Checkpoints

### 1. Value Sought

Identify the desired value.

Examples:

```text
trust
clarity
speed
safety
accuracy
control
adoption
credibility
decision confidence
```

### 2. Value at Risk

Identify what can be lost.

Examples:

```text
wrong decisions
wasted effort
reputational damage
misunderstanding
unsafe use
loss of trust
unreviewable output
```

### 3. Cost of Failure

The cost should be concrete.

Weak:

```text
This may cause problems.
```

Better:

```text
Wrong information may enter a report, email, medical note, financial analysis, or customer-facing document before anyone catches it.
```

### 4. Opportunity if Success

The positive outcome should also be concrete.

Weak:

```text
This improves quality.
```

Better:

```text
The team can review the output, catch errors earlier, and improve the process over time.
```

### 5. Stakes Proportionality

The language must match the actual stakes.

Do not inflate:

```text
This guarantees safety.
This changes the future of work.
This eliminates error.
```

Use bounded language:

```text
This reduces risk.
This makes errors easier to catch.
This makes output more reviewable.
```

## Failure Modes

Fail if:

1. The text says "important" but never explains the cost.
2. The stakes are generic.
3. The success state is vague.
4. The failure state is exaggerated.
5. The tone is dramatic but the evidence is weak.
6. The output relies on abstract benefits such as "efficiency" or "innovation" without concrete consequence.
7. The audience cannot answer: "What could go wrong if we ignore this?"

## Severity

```text
hard_fail:
 - no value at risk
 - inflated stakes beyond evidence
 - success/failure not distinguishable

soft_fail:
 - vague cost
 - weak urgency
 - generic benefit language
```

## Rewrite Rule

If Value & Stakes Harness fails, rewrite by answering:

```text
What is the protagonist trying to protect or gain?
What specific bad outcome is being avoided?
What specific better state becomes possible?
```

Then replace vague value words with concrete consequences.

## Output Instruction

Do not expose the stakes analysis unless the user asks for critique.
For normal output, silently use this harness to sharpen the draft.
