# Value and Stakes

## Purpose

This file defines how the skill identifies value and stakes before writing.

A story becomes meaningful only when something valuable can be gained, lost, protected, damaged, restored, or transformed.

No value, no story.
No risk, no drama.
No stakes, no reason to listen.

## Core Definition

Value is what matters.

Stakes are what may be gained or lost if the protagonist succeeds or fails.

the skill must identify both before generating narrative output.

## Types of Value

Value may be:

```text
trust
time
money
safety
reputation
clarity
control
freedom
growth
belonging
truth
survival
status
learning
credibility
decision confidence
```

For professional and technical materials, value is often not emotional on the surface. It may appear as:

```text
fewer mistakes
faster judgment
lower uncertainty
better coordination
more reliable output
less wasted effort
clearer accountability
```

the skill should translate abstract value into concrete consequence.

## Stakes Questions

Before writing, answer:

1. What does the protagonist want to gain?
2. What may be lost if the attempt fails?
3. What is the cost of delay?
4. What is the cost of misunderstanding?
5. What becomes possible if the protagonist succeeds?
6. What becomes worse if nothing changes?
7. Is the risk reversible or irreversible?

## Concrete Stakes Rule

Weak stakes are vague:

```text
This matters because it improves efficiency.
```

Stronger stakes are concrete:

```text
If the team cannot catch hidden errors before delivery, AI output may enter real work with wrong facts, false certainty, or distorted source material.
```

the skill should avoid vague stakes unless the source material does not support more detail.

## Positive and Negative Value

Value shifts can move in several directions:

```text
negative → positive
positive → negative
false positive → real negative
apparent failure → real gain
confusion → clarity
confidence → doubt
doubt → justified trust
```

the skill should identify the polarity of the value shift.

## Stakes Threshold

If stakes are weak, the output should be explanatory, not dramatic.
If stakes are strong, the output may use narrative tension.

Decision rule:

```text
low stakes → clear explanation
medium stakes → structured narrative
high stakes → full story arc with conflict and transformation
```

## Professional Context Rule

In professional writing, do not exaggerate stakes.

Avoid:

```text
This changes everything.
This guarantees success.
This eliminates all risk.
This is the future of the industry.
```

Prefer:

```text
This reduces a specific failure mode.
This makes judgment more reviewable.
This helps expose risk earlier.
This turns one-off output into a more controllable process.
```

## Runtime Fields

the skill should internally produce:

```yaml
value_stakes:
 value_sought:
 value_at_risk:
 cost_of_failure:
 opportunity_if_success:
 urgency:
 reversibility:
 value_shift:
 stakes_level: low | medium | high
```

## Failure Modes

Fail if:

1. The text says something matters but does not explain why.
2. The text uses high emotional language without real cost.
3. Success and failure lead to almost the same outcome.
4. The protagonist has no meaningful risk.
5. Stakes are inflated beyond the source material.

## Final Rule

Every the skill output should make the value clear.
If the audience cannot answer "what is at stake?", the narrative has failed.
