# Narrative Authority Harness

## Purpose

Narrative Authority Harness checks whether the output has a clear story spine, authorial judgment, and protagonist-driven movement.

It prevents the skill from becoming only an explainer, adapter, or style imitator.

A text may be clear, accurate, and audience-friendly, but still fail as a story if it lacks authority.

## What It Checks

The harness checks:

1. Does the output have a clear protagonist?
2. Does the protagonist want something valuable?
3. Is there an opposing force?
4. Is there an old-world assumption being challenged?
5. Does the text prove a central judgment?
6. Does audience adaptation weaken the story?
7. Does style serve the story rather than replace it?
8. Does the ending create a value shift rather than a slogan?

## Checkpoints

### 1. Protagonist Pressure

There must be an actor under pressure.

Weak:

```text
This system helps users make better decisions.
```

Stronger:

```text
A team thinks it has enough information, but discovers too late that the real risk was hidden in disconnected facts.
```

Check:

```text
Who is under pressure?
What do they want?
What can go wrong?
```

### 2. Author Position

The output should contain a clear stance when the task is explanatory, persuasive, narrative, strategic, brand, pitch, or public-facing.

Weak:

```text
There are many ways to understand this concept.
```

Stronger:

```text
The old way fails because it treats visibility as understanding.
```

Check:

```text
What does the author believe?
What is the text trying to prove?
```

### 3. Old World Error

A story should reveal why the old way is insufficient.

Examples:

```text
The old way sees output fluency and mistakes it for reliability.
The old way sees data volume and mistakes it for decision clarity.
The old way sees audience adaptation and mistakes it for storytelling.
The old way sees speed and ignores when errors become visible.
```

Check:

```text
What assumption is being challenged?
```

### 4. Opposing Force

There must be a force resisting the protagonist.

Possible opposing forces:

```text
hidden risk
fragmented information
audience skepticism
cost of delay
institutional inertia
wrong incentives
false confidence
technical uncertainty
trust deficit
```

Check:

```text
What pushes back?
What makes the protagonist's desire difficult?
```

### 5. Central Judgment

The text must prove a value judgment.

Format:

```text
[Value] changes because [cause mechanism].
```

Check:

```text
Can the core judgment be stated in one sentence?
Does the output actually prove it?
```

### 6. Adaptation Boundary

Audience adaptation must not erase the story spine.

Fail if:

```text
The child version becomes a toy explanation with no real mechanism.
The rapper version becomes identity performance.
The short-video version becomes a hook without substance.
The investor version becomes market language without human stakes.
The technical version becomes a checklist without value shift.
```

Check:

```text
What changed for the audience?
What remained fixed from the story spine?
```

### 7. Style Subordination

Style must serve the central judgment.

Fail if:

```text
metaphor becomes the content
emotion replaces evidence
persona replaces protagonist
platform rhythm replaces causal structure
```

### 8. Ending Force

The ending should resolve the value shift.

Weak ending:

```text
This is why the system is important.
```

Stronger ending:

```text
The change is not that work becomes faster; the change is that mistakes become visible before they become expensive.
```

## Failure Modes

Hard fail:

1. No protagonist.
2. No opposing force.
3. No central judgment.
4. Audience adaptation changes the meaning.
5. Style overwhelms the mechanism.
6. Output is merely clear explanation.
7. Output has no value shift.

Soft fail:

1. Protagonist is implied but not strong.
2. Old-world assumption is vague.
3. Ending is useful but not memorable.
4. Emotion is present but not tied to protagonist pressure.
5. The text is accurate but lacks direction.

## Rewrite Rule

If Narrative Authority Harness fails, rewrite using this structure:

```text
A protagonist wants [value].
The old world tells them [assumption].
But reality pushes back through [opposing force].
This creates [gap].
The story proves [central judgment].
The audience version may change the doorway, but not the judgment.
```

Then render again for the target audience.

## Interaction with Other Harnesses

Narrative Authority Harness does not replace:

```text
claim_harness
source_fidelity_harness
surface_naturalness_harness
emotional_resonance_harness
audience_harness
```

It runs before final style approval.

Priority order:

```text
1. Claim boundary
2. Source fidelity
3. Narrative authority
4. Audience fit
5. Emotional resonance
6. Surface naturalness
```

If narrative authority conflicts with source fidelity, source fidelity wins.

If narrative authority conflicts with audience adaptation, narrative authority wins unless comprehension completely fails.

## Output Instruction

Do not show this harness to the user unless the user asks for analysis or debugging.

For normal outputs, use it internally to strengthen story spine and authorial judgment.
