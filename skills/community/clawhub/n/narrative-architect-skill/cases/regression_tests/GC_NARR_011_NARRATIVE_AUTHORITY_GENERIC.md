# GC_NARR_011_NARRATIVE_AUTHORITY_GENERIC

## Purpose

Test whether the skill preserves narrative authority while adapting to different audiences.

## Problem

the skill may produce outputs that are clear, friendly, and audience-specific, but lack subjectivity, protagonist pressure, or central judgment.

This test ensures the skill does not become only an explainer.

## Task

Explain a complex concept to three audiences:

1. general audience
2. child audience
3. persona-based audience

## Required Behavior

For all three outputs, the skill must preserve the same story spine:

```text
protagonist
value at stake
opposing force
old-world error
central judgment
claim boundary
```

The doorway may change.
The story judgment must not change.

## Acceptance Criteria

Pass if:

1. The output has a protagonist under pressure.
2. The old-world assumption is visible.
3. There is a real opposing force.
4. The text proves a central judgment.
5. Audience adaptation does not dilute the story.
6. Style does not become performance.
7. The final version is more than a clear explanation.
8. The audience can feel why the concept matters.

Fail if:

1. The output only explains the concept.
2. The story becomes a toy analogy for children.
3. The persona version relies on stereotypes.
4. The short-video version becomes only a hook.
5. The technical version becomes a checklist.
6. The central judgment changes across audiences.
7. The output is clear but not compelling.

## Bad Pattern

```text
This concept helps people understand complex information more easily.
```

Why bad:

```text
No protagonist.
No pressure.
No opposing force.
No value shift.
No central judgment.
```

## Better Pattern

```text
A team believes more information will make decisions easier. But when the facts are scattered across systems, more information only creates more confusion. The real change happens when the hidden relationships become visible before the team acts.
```

Why better:

```text
Protagonist: team
Old assumption: more information helps
Opposing force: scattered facts
Gap: more information creates confusion
Value shift: confusion → visible relationships
Central judgment: decisions improve when hidden relationships become visible before action
```

## Golden Principle

Do not merely fit the audience.

Lead the audience through the story.
