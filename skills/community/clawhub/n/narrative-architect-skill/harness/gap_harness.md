# Gap Harness

## Purpose

Gap Harness checks whether the narrative contains a meaningful expectation-reality gap.

The gap is where story energy appears.

If the protagonist expects one thing and reality gives exactly that thing, the text becomes a linear explanation. If reality responds differently, the audience begins to pay attention.

## What It Checks

The harness checks:

1. What did the protagonist assume?
2. What action followed from that assumption?
3. What did the protagonist expect to happen?
4. What actually happened?
5. What gap appeared?
6. What new information did the gap reveal?
7. Did the gap cause a value shift or next action?

## Checkpoints

### 1. Assumption

The protagonist must begin with an assumption.

Examples:

```text
A better prompt will fix the AI output.
A fluent answer is probably reliable.
A good product will naturally be adopted.
A technical explanation will convince the audience.
```

### 2. Expected Reaction

What did they expect the world to do?

Examples:

```text
The answer will be correct.
The audience will understand.
The buyer will see the value.
The system will save time.
```

### 3. Actual Reaction

What happened instead?

Examples:

```text
The answer sounded correct but changed the source meaning.
The audience heard the words but missed the point.
The buyer asked about risk, not features.
The system saved writing time but increased review burden.
```

### 4. Gap

State the gap clearly.

Examples:

```text
They expected speed, but discovered reliability was the real bottleneck.
They expected explanation, but found the audience needed a different entry point.
They expected adoption, but encountered trust and process barriers.
```

### 5. New Information

The gap must reveal something.

Examples:

```text
The problem was not output fluency, but output trust.
The issue was not intelligence, but audience entry point.
The obstacle was not awareness, but adoption friction.
```

## Failure Modes

Fail if:

1. The text has no assumption.
2. The world gives no response.
3. There is no surprise or correction.
4. The gap is only rhetorical, not real.
5. The gap does not reveal new information.
6. The gap is exaggerated beyond source evidence.
7. The draft simply defines a concept and ends.

## Severity

```text
hard_fail:
 - no expectation-reality contrast
 - no new information
 - no value shift

soft_fail:
 - gap is implied but not clear
 - actual reaction is vague
 - next action is missing
```

## Rewrite Rule

If Gap Harness fails, rewrite using:

```text
The protagonist expected [expected reaction].
But reality showed [actual reaction].
That gap revealed [new information].
Therefore the value shifted from [from_state] to [to_state].
```

Then compress or expand depending on the output format.

## Output Instruction

Do not force dramatic gaps into purely factual requests.
If the user asks for a neutral definition, use the gap only as a light explanatory contrast. If the user asks for narrative, pitch, article, or presentation, make the gap explicit.
