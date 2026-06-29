# Lightest Sufficient Chain Policy

## Purpose

This policy prevents the skill from over-processing simple tasks.

The skill should not use the same heavy runtime chain for every request.

## Core Rule

```text
Use the lightest chain that can produce a good result.
```

A chain is sufficient if it protects:

```text
user intent
claim boundary
audience fit
relationship context when relevant
narrative authority when relevant
surface naturalness
```

## Why This Matters

Over-processing causes:

```text
short messages becoming essays
introductions becoming proposals
explanations becoming over-dramatic
user intent being replaced by the skill's framework
too many internal concepts leaking into output
slow iteration when user only wants a quick fix
```

## Chain Weight Levels

### Level 1: Micro

Use for:

```text
one-line message
quick reply
minor rewrite
short phrase
```

Required checks:

```text
purpose
tone
next action if relevant
surface naturalness
```

### Level 2: Light

Use for:

```text
short explanation
brief intro
short follow-up
simple audience adaptation
```

Required checks:

```text
claim boundary
audience fit
surface naturalness
```

### Level 3: Medium

Use for:

```text
one-on-one strategy
expert explanation
collaboration message
customer message
investor intro
```

Required checks:

```text
conversation purpose
recipient motivation
claim boundary
narrative authority
audience fit
outcome
surface naturalness
```

### Level 4: Heavy

Use for:

```text
public narrative
article
speech
brand story
pitch
long-form strategic communication
```

Required checks:

```text
story kernel
narrative authority
value stakes
action-reaction-gap
controlling idea
affective arc
narrative entropy
claim boundary
source fidelity
surface naturalness
```

## Escalation Rule

Start light if possible.

Escalate only when:

```text
the task is high-stakes
the user asks for strategy
the output fails
the user is dissatisfied
the relationship context is complex
the source material is complex
the message must persuade, not just inform
```

## De-escalation Rule

If the output feels too heavy, reduce chain weight.

Signs of over-processing:

```text
too much setup
too many paragraphs
too many concepts
too formal
sounds like a proposal
sounds like a framework rather than a message
```

## User Frame Preservation

If the user provides a preferred frame, preserve it.

Do not replace the user's structure just because a deeper chain could produce a more complete narrative.

Improve within the frame:

```text
sharpen
compress
clarify
strengthen tension
control claims
make next action clearer
```

## Final Rule

the skill should be powerful when needed and invisible when not needed.
