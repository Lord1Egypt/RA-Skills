# Attraction Filter Mapper

## Purpose

Attraction Filter Mapper identifies who the story is meant to attract, who it does not need to attract, and how the user's personality should remain visible without creating unnecessary offense.

the skill should not optimize every message for universal approval.

The goal is not:
"Everyone should like this."

The goal is:
"The right listener should feel this story is for them."

## Required Output

Internally produce:

```yaml
attraction_filter:
 ideal_listener:
 non_target_listener:
 love_trigger:
 personality_signal:
 acceptable_polarization:
 forbidden_polarization:
 repulsion_boundary:
 story_magnet:
```

## Field Definitions

### ideal_listener

Who should be attracted by this story?

Examples:

```text
a method-driven academic
a risk-aware founder
a buyer tired of shallow pitches
an investor looking for system-level change
a doctor who sees adoption friction
an operator who has felt the pain
a technical leader who cares about controllability
```

### non_target_listener

Who does not need to be convinced?

Examples:

```text
people seeking only surface marketing
people uninterested in the problem
listeners who need guaranteed certainty
listeners looking for immediate transactional benefit
people who dislike complexity
```

Do not insult non-target listeners. Simply do not over-adapt to them.

### love_trigger

Why would the ideal listener love the story?

Examples:

```text
It names a problem they have felt but could not articulate.
It gives them a new frame.
It respects their intelligence.
It shows a real-world testbed.
It reveals a hidden structure.
It offers a way to act.
It makes them feel early to something important.
```

### personality_signal

What part of the user's personality should remain visible?

Examples:

```text
sharpness
restraint
curiosity
ambition
skepticism
discipline
intellectual honesty
boldness
humor
taste
```

### acceptable_polarization

What kind of selectivity is acceptable?

Examples:

```text
Some listeners may find the story too technical.
Some may not care because they do not feel the problem.
Some may disagree with the worldview.
Some may not be ready for the level of ambition.
```

### forbidden_polarization

What must be avoided?

Examples:

```text
making the listener feel stupid
mocking existing practitioners
implying everyone else is backward
creating moral superiority
using contempt as energy
turning a structural critique into personal attack
```

### repulsion_boundary

What expression would create unnecessary dislike?

Examples:

```text
too much self-praise
too many superlatives
too much urgency
too much insider language
overstating novelty
sounding like a pitch
sounding like a lecture
```

### story_magnet

The phrase or frame that pulls the right listener in.

Examples:

```text
This is not a product demo. It is a real-world testbed for a method.
The real issue is not lack of data, but when hidden risk becomes visible.
We are not asking you to buy the system. We are inviting you to examine the problem with us.
```

## Runtime Rule

Attraction Filter runs after Conversation Purpose Mapper and before rendering.

It determines what should be intensified and what should be softened.

## Failure Modes

Fail if:

1. The output tries to be liked by everyone.
2. The message loses the user's personality.
3. The story has no magnet for the right listener.
4. The tone becomes over-safe.
5. The tone becomes arrogant or hostile.
6. The text confuses selectivity with superiority.
7. The output is acceptable but not attractive.

## Final Rule

A good the skill output should not merely be clear.

It should make the right listener feel:
"This is exactly the kind of problem I care about."
