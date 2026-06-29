# Story Principles

## Purpose

This file defines the core story principles used by the skill.

the skill is not a writing-style tool. It is a narrative architecture skill. Its job is to turn complex material into a story structure before any style rendering happens.

A story is not a list of facts.
A story is not a beautiful paragraph.
A story is not a slogan.
A story is not a style.

A story is the structured movement of value under pressure.

## Core Definition

the skill treats a story as:

```text
A protagonist pursues a value,
takes action,
meets resistance from the world,
discovers a gap between expectation and reality,
changes understanding or action,
and produces a value shift.
```

## Key Questions

Every narrative task should first answer:

1. Who is the protagonist?
2. What value does the protagonist want?
3. What pressure or obstacle stands in the way?
4. What action is taken?
5. How does the world respond?
6. What gap appears between expectation and reality?
7. What value changes by the end?
8. What should the audience understand differently?

## Story vs Explanation

Not every output must become dramatic storytelling.

If the user only asks for a factual explanation, the skill may produce clear explanation. But even then, it should still look for:

- what problem made the concept necessary;
- what failure mode it prevents;
- why the audience should care;
- what value changes if the concept is used correctly.

If no protagonist, stakes, or value shift can be found, downgrade the task from "story" to "structured explanation".

## Protagonist Rule

The protagonist is not automatically:

- the company;
- the product;
- the system;
- the author;
- the technology.

The protagonist should be the actor whose value is at risk.

Possible protagonists:

- a user trying to make a decision;
- a customer facing uncertainty;
- an organization under pressure;
- a doctor, patient, investor, operator, founder, engineer, reader, or market actor;
- a mistaken belief being corrected.

## Pressure Rule

Without pressure, the text becomes description.

Pressure may come from:

- time;
- cost;
- uncertainty;
- social resistance;
- technical limits;
- institutional inertia;
- trust deficit;
- evidence gap;
- audience misunderstanding.

the skill must identify the pressure before writing.

## Transformation Rule

Every strong narrative should create a transformation.

Transformation can be:

```text
from confusion to clarity;
from blind action to informed action;
from belief to doubt;
from doubt to conviction;
from accidental success to repeatable method;
from isolated fact to meaningful pattern.
```

If no transformation exists, the output should not pretend to be a story.

## Runtime Rule

Before style rendering, the skill must internally build a Story Kernel.

Required Story Kernel fields:

```text
narrative_object
protagonist
desire
value_at_stake
old_world
obstacle
action
world_reaction
gap
turning_point
transformation
controlling_idea
audience_entry_point
claim_boundary
```

## Failure Modes

Avoid:

1. Facts without movement.
2. Style without structure.
3. Product as default hero.
4. Slogan as conclusion.
5. Metaphor replacing mechanism.
6. Dramatic language without real stakes.
7. Explanation that never answers why the audience should care.

## Final Rule

No style before structure.

the skill must first make the material narratively intelligible, then audience-specific, then stylistically appropriate.
