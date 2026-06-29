# Affective Arc Mapper

## Purpose

Affective Arc Mapper decides the emotional path of the audience before rendering.

Audience adaptation is not only cognitive. For general audiences, the text must create an emotional reason to care before explaining the mechanism.

the skill should not just answer "will the audience understand?" but also "what should the audience feel as they move through this explanation?"

## Required Fields

```yaml
affective_arc:
 initial_emotion:
 emotional_trigger:
 tension:
 recognition:
 relief_or_resolution:
 final_emotion:
 emotional_temperature: 0-5
```

## Emotion Types

### Possible Initial Emotions

- unease — something feels off but the audience cannot name it yet
- curiosity — a gap between what is assumed and what might be true
- surprise — a counterintuitive fact that challenges a common belief
- frustration — a known pain that has been tolerated too long
- recognition — "yes, I have felt this too"
- worry — a risk the audience may face
- disbelief — "that cannot be right" before the explanation unfolds
- anger — a preventable wrong that continues to happen
- hope — a possibility that was dismissed but may be real

### Possible Final Emotions

- clarity — the confusion is resolved
- relief — a risk is shown to be manageable
- justified trust — not blind faith, but confidence with evidence
- urgency — "this matters and cannot wait"
- confidence — equipped with new understanding
- respect — for the complexity of the problem or the elegance of the solution
- cautious optimism — hope bounded by realism

## Emotional Temperature Scale

Scale: 0–5

| Level | Use Case | Description |
|---|---|---|
| 0 | Technical documentation, regulatory submission, formal report | No emotional shaping. Pure clarity. |
| 1 | Technical team explanation, internal briefing | Light problem-framing. Minimal affective lift. |
| 2 | Business executive, investor, professional audience | Stakes made visible. Risk and consequence felt. |
| 3 | General public, media, customer | Problem felt before mechanism explained. |
| 4 | Brand story, thought leadership, keynote | Full affective arc. Recognition → tension → resolution. |
| 5 | Urgent warning, ethical imperative, societal stakes | Strong emotional entry. Must be earned by real stakes. |

Level 5 requires a hard check: is the emotion justified by real stakes? If not, downgrade.

## Audience Rules

### General Audience

Use emotional entry before conceptual definition.

Pattern:

```text
felt risk
→ recognizable scene
→ hidden problem
→ mechanism
→ emotional resolution
```

### Technical Audience

Use mechanism first. Emotional intensity should stay low (0–1).

Pattern:

```text
problem statement
→ mechanism
→ consequence
```

### Investor Audience

Use expensive failure or missed opportunity as emotional trigger.

Pattern:

```text
cost of the old way
→ why the old way persists
→ mechanism that changes the equation
→ new possibility
```

### Customer Audience

Use operational pain or avoided loss as emotional trigger.

Pattern:

```text
daily friction
→ why the friction is structural, not personal
→ how the mechanism removes it
→ what the day looks like after
```

## Boundaries

Emotion must come from real stakes.

Do not use:

- fearmongering — inflating danger beyond evidence
- melodrama — "this changes everything"
- shame — making the audience feel stupid
- exaggerated catastrophe — "if we don't act, disaster"
- unsupported danger — risk that is implied but never demonstrated
- sentimental language — vague appeals to emotion without mechanism

If the source material does not support emotional weight, lower the temperature. A calm explanation at temperature 1 is better than forced emotion at temperature 4.

## Visibility Rule

Affective Arc is internal by default.

Do not show in final output:
- affective_arc label or YAML
- emotional temperature
- emotion path (e.g., "unease → recognition → relief")
- any affective arc metadata

The only exception: the user explicitly asks for debugging, analysis, or skill testing.

This applies regardless of audience type. Even when the emotional temperature is high, the emotional path shapes the output—it does not appear in the output.

## Runtime Rule

Before rendering for general audience, ask:

1. What should the audience feel first?
2. What hidden risk or contradiction creates that feeling?
3. What recognition should happen in the middle?
4. What relief or conviction should the ending create?

## Relationship to Other Layers

- Affective Arc maps the emotional path → not a separate layer, but a shaping force
- Claim Boundary still applies: emotion cannot upgrade confidence
- Story Kernel still applies: the gap creates the emotional energy
- Controlling Idea still applies: the resolution must prove the idea
- Style Wrapper still applies: tone and register follow the temperature setting

## Failure Modes

1. **Emotional entry without mechanism.** The audience feels something but learns nothing.
2. **Mechanism without emotional entry.** The audience understands but does not care.
3. **Forced emotion.** The stakes don't justify the temperature chosen.
4. **Emotion overriding facts.** A dramatic claim replaces a bounded one.
5. **Flat arc.** No movement from initial emotion to final emotion.
6. **Wrong initial emotion.** Starting from anger when the audience feels curiosity, or vice versa.

## Protagonist-Bound Emotion Rule

Emotion should come from the protagonist's pressure, not from decorative language.

Bad:

```text
Add excitement, fear, humor, or drama to make the audience feel something.
```

Better:

```text
Show what the protagonist risks, misunderstands, discovers, or almost loses.
Let the audience feel through that pressure.
```

## Emotion Source Rule

For every affective arc, identify the source of emotion:

```yaml
emotion_source:
 protagonist_pressure:
 value_at_risk:
 opposing_force:
 discovery:
 value_shift:
```

## Audience vs Protagonist Emotion

Audience emotion is a response to protagonist pressure.

The system should not only ask:

```text
What should the audience feel?
```

It must ask first:

```text
What happens to the protagonist that makes this feeling justified?
```

## Emotion Validity Test

Fail if emotion is created mainly by:

```text
dramatic adjectives
platform language
persona performance
sentimental phrasing
exaggerated danger
```

Emotion is valid only when it is grounded in stakes, conflict, discovery, or value shift.

## Entropy and Emotion

Emotion often rises when entropy rises.

But not all surprise is emotional.

the skill should link emotional movement to meaningful entropy.

Good:

```text
The audience expects X.
The story reveals Y.
This creates recognition, unease, relief, or urgency.
```

Bad:

```text
Add emotional language to make the output stronger.
```

## Emotional Entropy Rule

For general audiences:

```text
slight unease
→ recognition
→ clear mechanism
→ relief or cautious optimism
```

For strategic audiences:

```text
frustration
→ reframing
→ possibility
→ focused action
```

For technical audiences:

```text
curiosity
→ structural clarity
→ controlled confidence
```

For one-on-one collaboration:

```text
relevance
→ shared problem
→ intellectual interest
→ low-friction next step
```
