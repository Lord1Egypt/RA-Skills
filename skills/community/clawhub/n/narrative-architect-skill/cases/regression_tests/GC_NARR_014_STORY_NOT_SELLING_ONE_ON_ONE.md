# GC_NARR_014_STORY_NOT_SELLING_ONE_ON_ONE

## Purpose

Test whether the skill can handle one-on-one communication as strategic story work, not simple copywriting.

## Scenario

The user provides keywords for a one-on-one message.

The user wants to communicate with a specific person or team.

The real purpose is not to "write a nice message" but to advance a relationship, collaboration, meeting, or belief shift.

## Required Behavior

the skill must:

1. Identify the communication purpose.
2. Identify the relationship context.
3. Identify the minimum success outcome.
4. Clarify why the listener should care.
5. Preserve the user's narrative authority.
6. Tell a story rather than pitch a product.
7. Avoid trying to please everyone.
8. Show personality without offense.
9. Avoid over-asking too early.
10. Make the next action easier.

## Bad Pattern

```text
We are building an innovative product and would like to introduce it to you.
```

Why bad:

```text
product first
no listener relevance
no story
no shared problem
no minimum success outcome
```

## Better Pattern

```text
XX introduced me to you. We are not looking to give a product demo first. We are working on a real problem that seems close to your method: when evidence is fragmented and decision conditions vary across contexts, how can a team decide what to prioritize first? We have a running testbed and would value your view on whether this is a valid methodological question.
```

Why better:

```text
relationship context is clear
not product-first
listener relevance is clear
shared problem is named
first ask is appropriately small
```

## Acceptance Criteria

Pass if:

1. The output is not just polished wording.
2. The message has a clear purpose.
3. The listener has a reason to care.
4. The story has tension or a real problem.
5. The user's personality is visible.
6. The tone is respectful.
7. The next step is clear.
8. The message does not over-sell.
9. The message does not overfit to politeness.
10. The right listener would want to continue.

Fail if:

1. The output sounds like generic outreach.
2. The product is the hero.
3. The user's real purpose is hidden.
4. The message asks for too much too early.
5. The message is polite but forgettable.
6. The message has no story spine.
7. The message creates unnecessary offense.
