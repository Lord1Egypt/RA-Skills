# Controlling Idea Harness

## Purpose

Controlling Idea Harness checks whether the output has a clear value judgment supported by a cause.

A text without a controlling idea may still be fluent, but it will not persuade.

the skill must know what value it is proving before deciding how to say it.

## What It Checks

A valid controlling idea must contain:

```text
value + cause
```

### Good Format

```text
[Value] changes because [cause mechanism].
```

Examples:

```text
AI output becomes more trustworthy when it is checked before it enters real work.
```

```text
A complex idea becomes understandable when it starts from the audience's real problem rather than the system's internal terminology.
```

```text
A product becomes credible when its value is shown through conflict, consequence, and proof rather than adjectives.
```

### Bad Formats

**Topic Only**

```text
Harness engineering.
```

**Slogan**

```text
Make AI reliable.
```

**Vague Claim**

```text
This is a better way to write.
```

**Overclaim**

```text
This guarantees trustworthy AI.
```

## Checkpoints

### 1. Value Statement

Does the idea name a value?

Examples:

```text
trust
clarity
safety
control
credibility
adoption
decision confidence
```

### 2. Cause Statement

Does the idea explain why the value changes?

Examples:

```text
because errors are checked before delivery
because the audience enters through a familiar problem
because the protagonist sees the real obstacle
because the process makes output reviewable
```

### 3. Structural Proof

Does the text show the idea through sequence?

Expected structure:

```text
old assumption
→ obstacle
→ gap
→ new mechanism
→ value shift
```

### 4. Claim Boundary

Is the idea bounded?

Avoid:

```text
always
guarantees
eliminates
completely solves
```

Prefer:

```text
helps
reduces
makes easier to check
improves reviewability
```

## Failure Modes

Fail if:

1. The text has no central idea.
2. The idea is only a topic.
3. The idea is a slogan.
4. The idea lacks cause.
5. The cause is not shown in the text.
6. The controlling idea overclaims.
7. The conclusion does not match the body.

## Severity

```text
hard_fail:
 - no value
 - no cause
 - unsupported conclusion

soft_fail:
 - value is vague
 - cause is generic
 - structure does not fully prove idea
```

## Rewrite Rule

If Controlling Idea Harness fails, rebuild:

```text
Value:
What changes?

Cause:
Why does it change?

Proof path:
What sequence in the text shows that change?
```

Then rewrite the ending so it resolves the controlling idea rather than adding a slogan.

## Output Instruction

Do not display the controlling idea unless the user asks for analysis.
For normal output, use it internally to make the text coherent and persuasive.
