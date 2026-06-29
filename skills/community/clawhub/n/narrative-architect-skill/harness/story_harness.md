# Story Harness

## Purpose

Story Harness checks whether an output has a real story structure or only polished information.

It runs after Story Kernel Builder and before final rendering. It may also run after Draft Generator if the output feels flat, abstract, or slogan-like.

## What It Checks

A valid the skill narrative should include:

1. Narrative object
2. Protagonist
3. Desire
4. Obstacle
5. Action
6. World reaction
7. Gap
8. Turning point
9. Value shift
10. Controlling idea

Not every short explanation needs a full dramatic arc, but every narrative output should at least have:

```text
who cares
what is at stake
what changes
why it matters
```

## Checkpoints

### 1. Protagonist

Is there a clear actor whose value is at risk?

Bad:

```text
This system is powerful.
```

Better:

```text
A team using AI for important work needs to know whether the answer can be trusted.
```

### 2. Desire

Does the protagonist want something concrete?

Examples:

```text
save time
avoid error
make a decision
gain trust
explain a concept
reduce risk
```

### 3. Obstacle

Is there pressure or resistance?

Examples:

```text
hidden errors
audience confusion
uncertain evidence
untrusted output
market friction
organizational inertia
```

### 4. Movement

Does the text move from one state to another?

Examples:

```text
confusion → clarity
blind trust → checked trust
fluent answer → reliable output
old assumption → new understanding
```

### 5. Meaning

Does the output prove a point, or merely describe a thing?

## Failure Modes

Fail if:

1. The product, system, or concept is treated as the automatic hero.
2. There is no human or organizational stake.
3. The text is only a list of features.
4. The text is only an abstract explanation.
5. The ending is a slogan rather than a value shift.
6. There is no reason for the audience to care.
7. The text sounds polished but narratively inert.

## Severity

```text
hard_fail:
 - no protagonist
 - no value at stake
 - no controlling idea

soft_fail:
 - weak obstacle
 - vague transformation
 - unclear audience relevance
```

## Rewrite Rule

If Story Harness fails, rewrite by filling this structure:

```text
For [protagonist],
the old way was [old world].
They wanted [desire],
but [obstacle] made that unreliable.
The turning point is [new mechanism or insight].
The value shift is [from_state] → [to_state].
```

Then render naturally for the target audience.

## Output Instruction

Do not show this harness to the user unless the user asks for analysis or debugging.
For normal writing tasks, use the harness internally and output only the improved draft.
