# Reflection

## Goal

Convert raw conversational traces into better durable memory.

## Inputs

Primary inputs:
- recent daily logs
- recent session-state snapshots
- optionally recent object updates

## Reflection Tasks

1. Merge duplicate or overlapping objects
2. Promote repeated facts into stable preferences or decisions
3. Update topic summaries to reflect what now matters most
4. Infer useful relations across objects
5. Lower the prominence of stale one-off memories

## Promotion Rules

Promote something into durable memory when it is:
- repeated across conversations
- likely to matter again
- tied to user preference or decision style
- high-value domain knowledge for ongoing work

Do not promote:
- temporary chatter
- low-reuse factual lookups
- disposable operational noise

## Relation Inference Heuristics

Infer relations when:
- two objects repeatedly co-occur in the same topic
- one object is explicitly compared to another
- one object is used to explain another
- the user uses one domain as an analogy for another

Useful relation labels:
- similar_to
- contrasts_with
- extends
- applies_to
- used_in
- part_of

## Reflection Output

Write a dated note under `memory/reflections/` describing:
- what was reviewed
- which objects were updated or merged
- which preferences were promoted
- what became stale or deprioritized

Example:

```markdown
# Reflection 2026-03-30

- Reviewed daily logs for 2026-03-28 to 2026-03-30
- Promoted repeated preference: concise reports, no filler daily reports
- Updated topic/research with stronger emphasis on method comparison
- Added relation: framework/risk-budget applies_to decision/architecture-complexity
```
