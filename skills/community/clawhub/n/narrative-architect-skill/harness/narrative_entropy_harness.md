# Narrative Entropy Harness

## Purpose

Narrative Entropy Harness checks whether the output has the right balance of predictability and surprise.

It prevents two common failures:

1. clear but boring;
2. exciting but confusing.

## What It Checks

1. Does the output give the audience familiar ground?
2. Does it contain at least one meaningful turn?
3. Is the surprise understandable?
4. Is cognitive load controlled?
5. Are there too many metaphors or concepts?
6. Does the entropy rhythm support the controlling idea?
7. Does the ending resolve the tension?

## Checkpoints

### 1. Familiar Ground

The audience should know where they are.

Bad:

```text
This is an ontology-driven multi-agent simulation system.
```

Better:

```text
A company can spend months entering a new market before realizing it chose the wrong path.
```

### 2. Meaningful Turn

The text should create one strong shift.

Examples:

```text
It is not lack of data. It is disconnected data.
It is not that AI writes badly. It is that it can sound right while being wrong.
It is not just faster decision-making. It is earlier error exposure.
```

### 3. Cognitive Load

Fail if the output contains too many unfamiliar terms before grounding.

High-risk clusters:

```text
ontology + simulation + multi-agent + payment curve + KOL + world model
regulation + procurement + reimbursement + channel + evidence + pricing
```

If needed, introduce them in layers.

### 4. Entropy Rhythm

Preferred rhythm:

```text
low → medium → high → low
```

Example:

```text
familiar scene
→ hidden problem
→ surprising reframing
→ clear mechanism
→ memorable resolution
```

### 5. No Random Surprise

High-entropy information must reveal meaning.

Fail if surprise is only:

```text
dramatic language
big claim
unexpected metaphor
unsupported contrast
```

### 6. Resolution

The ending should reduce entropy again.

Good endings:

```text
The value is not speed. It is making the wrong path visible before money is spent.
You do not need to trust AI blindly. You need to trust the checks around it.
The point is not more information. It is the moment information becomes usable.
```

## Failure Modes

Hard fail:

1. The output is predictable from beginning to end.
2. The output has no turn.
3. The output introduces too many new concepts at once.
4. The output is emotionally intense but structurally unclear.
5. The surprise contradicts source fidelity.
6. The ending adds a slogan instead of resolving the turn.

Soft fail:

1. The turn is present but weak.
2. The opening is too abstract.
3. Too many metaphors.
4. The final line is correct but not memorable.
5. The audience may understand but not feel discovery.

## Rewrite Rule

If entropy is too low:

```text
Find the old assumption.
Reveal why it is incomplete.
Turn the explanation around that discovery.
```

If entropy is too high:

```text
Remove extra metaphors.
Reduce the number of claims.
Return to one protagonist, one pressure, one turn.
```

## Final Rule

Good the skill output should make the audience feel:

```text
I can follow this.
And I did not expect that turn.
```
