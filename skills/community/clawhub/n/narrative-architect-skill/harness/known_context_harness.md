# Known Context Harness

## Purpose

Known Context Harness checks whether the skill used available project context before asking clarifying questions.

It prevents over-clarification and blank-slate behavior.

## Checkpoints

1. Did the user reference a known project or internal system?
2. Is there relevant context in current conversation, memory, workspace, or project files?
3. Did the skill attempt recovery before asking?
4. Is there enough context to produce a safe draft?
5. Are unknowns marked instead of blocking?
6. Does the output preserve known exclusions?
7. Does the output language match the user request?

## Known Entity Detection

Treat the following as possible known entities:

```text
project names
skill names
product names
internal systems
previously discussed architectures
workspace directories
repo names
domain-specific initiatives
```

## Sufficient Context Test

A known project has sufficient context if at least four of the following are known:

```text
one-line description
target user
core problem
main use cases
what it is not
core architecture
public positioning
safe claim boundary
```

If sufficient, do not ask basic questions. Produce a draft.

## Known Exclusions

If prior context says the project is not something, preserve that boundary.

Examples:

```text
not a CRM
not a marketplace
not a supplier promotion platform
not an automatic clinical decision system
not a generic encyclopedia
not a product catalog
```

## Bad Pattern

```text
I don't have context. What is this product? Who is it for? What problem does it solve?
```

Bad when context exists.

## Good Pattern

```text
I'll draft this based on the available context. I'm treating it as [known positioning]. I'll mark unknown installation and license details as placeholders.
```

## Failure Modes

Hard fail:

1. Asks basic questions about known project.
2. Ignores project memory.
3. Treats retrieval failure as final.
4. Does not produce artifact when enough context exists.
5. Uses wrong language.

Soft fail:

1. Draft omits important known boundary.
2. Unknowns are not marked clearly.
3. Context is used but public positioning is too internal.

## Rewrite Rule

If failed:

```text
Recover known context.
Summarize assumptions in one sentence.
Generate artifact.
Mark unknowns as TBD.
Ask only one follow-up if truly necessary.
```

## Final Rule

A memory-enabled skill must not behave like it has never met the project before.
