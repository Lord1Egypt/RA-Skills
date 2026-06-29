# Narrative Authority Mapper

## Purpose

Narrative Authority Mapper defines the story's authority before audience adaptation and style rendering.

the skill should not merely ask:

```text
How can this audience understand the material?
```

It must first ask:

```text
What truth should the audience be led to see?
What value judgment must the story prove?
Whose struggle gives the story force?
What must not be diluted when adapting to audience or platform?
```

Narrative authority is the spine of the story.

Audience adaptation changes the doorway.
Narrative authority protects the destination.

## Core Principle

```text
A story is not built by pleasing the audience.
A story is built by leading the audience through pressure, conflict, discovery, and value change.
```

the skill must preserve the story's central judgment across all renderings.

## Required Output

Before Audience Cognition Mapping, internally produce:

```yaml
narrative_authority:
 story_owner:
 protagonist:
 author_position:
 central_judgment:
 old_world_error:
 opposing_force:
 non_negotiable_truth:
 desired_audience_shift:
 dilution_risks:
 adaptation_boundary:
```

## Field Definitions

### story_owner

Who owns the story's perspective?

This is not always the user, company, product, or system.

Possible story owners:

```text
founder
customer
doctor
patient
operator
engineer
investor
teacher
student
organization
market actor
public audience
misunderstood idea
```

The story owner is the perspective from which the truth is revealed.

### protagonist

Who is under pressure?

The protagonist should be the actor whose value is at risk.

Do not default to:

```text
the product
the company
the platform
the technology
the author
```

Unless that entity truly experiences pressure, conflict, or transformation.

### author_position

What does the author believe?

The output must not be neutral when the task requires persuasion, narrative, pitch, brand, or opinion.

Examples:

```text
The old way is wasteful.
The audience is asking the wrong question.
The real risk is hidden, not visible.
The product is not the hero; the user's changed action is the hero.
The system matters because it changes when mistakes are discovered.
```

Author position should be clear but bounded by evidence.

### central_judgment

What value judgment should the story prove?

Format:

```text
[Value] changes because [cause mechanism].
```

Examples:

```text
Trust becomes possible when claims are tested against real consequences.
Speed becomes valuable only when errors can be caught before they spread.
A complex idea becomes understandable when the audience first feels the problem it solves.
A product becomes credible when its value is shown through conflict, not adjectives.
```

### old_world_error

What does the old world get wrong?

Examples:

```text
It assumes more information creates better decisions.
It assumes a fluent answer is a reliable answer.
It assumes a good product will naturally find adoption.
It assumes explanation is enough to create belief.
It assumes audience adaptation means changing style.
```

### opposing_force

What force resists the protagonist?

Examples:

```text
uncertainty
hidden risk
institutional inertia
fragmented information
trust deficit
wrong assumptions
audience skepticism
operational friction
cost of delay
social pressure
market complexity
```

Opposing force must be specific enough to create tension.

### non_negotiable_truth

What cannot be softened away when adapting to a specific audience?

Examples:

```text
The output must not imply guaranteed success.
The story must preserve the real risk.
The product must not become the protagonist if the user is the true protagonist.
The analogy must not erase the actual mechanism.
The platform style must not make the claim less accurate.
```

### desired_audience_shift

What should the audience believe or feel differently after the story?

Format:

```text
Before:
[old belief]

After:
[new belief]
```

Example:

```text
Before:
This is just a technical tool.

After:
This is a way to change when risk becomes visible.
```

### dilution_risks

How might the story get weakened?

Common risks:

```text
over-explaining
over-adapting to audience
turning story into product description
turning judgment into slogan
making the tone too safe
using too many analogies
performing a persona
hiding conflict to sound friendly
```

### adaptation_boundary

What can change and what must stay fixed?

Example:

```yaml
can_change:
 - metaphor
 - opening scene
 - vocabulary
 - rhythm
 - emotional temperature

must_not_change:
 - protagonist
 - value at stake
 - central judgment
 - claim boundary
 - actual mechanism
```

## Runtime Placement

Narrative Authority Mapper should run after Story Kernel Builder and before Audience Cognition Mapper.

Recommended chain:

```text
Parse Material
→ Extract Claim Boundary
→ Build Story Kernel
→ Map Narrative Authority
→ Identify Value / Stakes
→ Build Action-Reaction-Gap
→ Build Controlling Idea
→ Map Audience Cognition
→ Map Affective Arc
→ Render
→ Harness
```

## Decision Rules

### Rule 1: Authority before adaptation

Before adapting to an audience, decide what the story must prove.

Bad:

```text
How do I explain this to teenagers?
```

Better:

```text
What truth must teenagers understand, and what doorway lets them enter without weakening that truth?
```

### Rule 2: Do not make the audience the author

Audience needs shape the doorway.
They do not define the story's truth.

### Rule 3: Style cannot replace judgment

A poetic version, ironic version, business version, child version, or short-video version must still prove the same core judgment.

### Rule 4: Persona is not performance

When writing for a persona or platform, use the audience's real situation, not stereotypes.

Bad:

```text
Add slang to sound like the audience.
```

Better:

```text
Find the pressure, risk, and workflow the audience actually recognizes.
```

### Rule 5: Conflict must remain visible

If the text becomes too polite, too explanatory, or too smooth, restore the opposing force.

A story without opposition becomes a brochure.

## Failure Modes

Narrative authority is weak if:

1. The text only explains what something is.
2. The text adapts too much to the audience and loses its central judgment.
3. The protagonist disappears.
4. The story has no opposing force.
5. The old world is not challenged.
6. The ending is a slogan instead of a value shift.
7. Style becomes the main event.
8. The output feels helpful but not necessary.
9. The audience understands the words but does not feel led anywhere.

## Rewrite Rule

If narrative authority is weak, rebuild using:

```text
This story is about [protagonist],
who wants [value],
but is blocked by [opposing force].
The old world believes [old assumption].
The story proves [central judgment].
No matter the audience, the output must preserve [non-negotiable truth].
```

Then render for the target audience.

## Final Rule

the skill is not trying to please the audience.

the skill is trying to lead the audience toward a sharper understanding of a value under pressure.
