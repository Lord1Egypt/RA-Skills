# Controlling Idea

## Purpose

This file defines the controlling idea requirement for the skill.

A controlling idea is the central value judgment proven by the narrative structure.

It is not a topic.
It is not a title.
It is not a slogan.
It is not a mood.
It is not a tagline.

A controlling idea states:

```text
what value changes
and why it changes.
```

## Required Formula

the skill should express the controlling idea as:

```text
[Value] changes because [cause mechanism].
```

Examples:

Weak:

```text
AI can improve work.
```

Strong:

```text
AI becomes usable in serious work only when its output can be checked, bounded, and reviewed before it enters real decisions.
```

Weak:

```text
Good storytelling matters.
```

Strong:

```text
A complex idea becomes persuasive only when the audience can see what value is at risk and why the old way fails.
```

Weak:

```text
The product is powerful.
```

Strong:

```text
A product becomes credible only when its value is shown through a real conflict, not merely claimed through adjectives.
```

## Value + Cause

A valid controlling idea must contain two parts:

### Value Statement

What value changes?

Examples:

```text
trust is earned
clarity is restored
risk is reduced
confidence becomes justified
speed becomes controllable
adoption becomes possible
```

### Causal Statement

Why does it change?

Examples:

```text
because hidden errors are checked before delivery
because the real obstacle is exposed
because the audience enters through a familiar problem
because the system turns one-off output into a repeatable process
because the protagonist learns that the old assumption was wrong
```

## Runtime Requirement

Before final drafting, the skill must internally produce:

```yaml
controlling_idea:
 value_statement:
 causal_statement:
 full_sentence:
 evidence_path:
```

`evidence_path` explains how the output proves the controlling idea through structure.

## Structure as Proof

the skill should not simply state the controlling idea.
It should prove it through sequence:

```text
old belief
→ action based on that belief
→ resistance from reality
→ gap
→ new understanding
→ value shift
```

If the text states a thesis but the sequence does not prove it, the output is weak.

## Controlling Idea vs Theme

Theme is broad:

```text
trust
risk
technology
growth
storytelling
```

Controlling idea is specific:

```text
Trust grows when claims are tested against real-world consequences.
```

Theme names the territory.
Controlling idea makes a judgment about that territory.

## Claim Boundary

The controlling idea must not overclaim.

Avoid:

```text
This guarantees trust.
This solves all reliability problems.
This makes failure impossible.
```

Prefer:

```text
This makes the output easier to check.
This reduces a specific risk.
This gives the team a way to review and improve.
```

## Failure Modes

Fail if:

1. The output has only a topic.
2. The conclusion is a slogan.
3. The controlling idea lacks cause.
4. The stated idea is not proven by the text.
5. The idea is more dramatic than the evidence allows.
6. The value shift is unclear.
7. The audience cannot repeat the point in one sentence.

## Rewrite Rule

If the controlling idea is weak, ask:

```text
What value changes?
What causes that change?
What evidence or sequence shows it?
```

Then rewrite the output so the structure proves the idea.

## Final Rule

No persuasion without a controlling idea.
the skill must know what value it is proving before it decides how beautifully to say it.
