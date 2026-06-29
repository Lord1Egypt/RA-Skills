# Facet Patterns

Use this as guidance, not as a fixed role list. The current task decides the split.

## Artifact True Job Examples

The true job of an artifact is what it must accomplish, not how it works. When the type is unclear, ask: "What would make this a complete success, and what would cause it to fail?"


- Prompt or delegation instruction: describe the goal, objective resources, constraints, decision boundaries, and acceptance criteria — not the implementation steps.
- Deployment plan: be executable by the operator and risk-aware of failure modes.
- Design: serve the user comfortably, maintain visual coherence, and be feasible to build within the given system.
- Code: be correct, maintainable, integrated with the surrounding system, and produce the right user-visible behavior.
- Health or lifestyle routine: be safe, produce measurable outcomes, and fit the user's actual schedule and environment.
- Strategy or plan: balance ambition against operational realism and produce a clear decision path.
- Research or analysis: surface accurate, relevant findings and indicate their reliability and limitations.

## Facet Selection Logic

Pick facets that protect different ways the result could fail:

- intent failure: wrong goal, wrong artifact, wrong audience
- resource failure: missing facts, wrong assumptions, unavailable inputs
- execution failure: cannot be implemented, tested, delivered, or operated
- experience failure: confusing, uncomfortable, unpleasant, or hard to adopt
- quality failure: mediocre result, weak polish, shallow reasoning
- safety failure: harmful, insecure, unhealthy, or misleading

**User/customer perspective check (mandatory):** after selecting facets, confirm that at least one facet directly represents the person who will actually use, receive, or be affected by the artifact. Technical-correctness and operational-realism facets appear naturally; the user/customer perspective is the one most commonly dropped. If no selected facet speaks for the end user or customer, either redefine one or add a facet before proceeding.

## Common Patterns

Prompt or delegation instruction:

- goal clarity
- objective resources
- execution boundary

Code or automation:

- correctness
- integration risk
- operator or user-facing behavior

Design or user experience:

- user comfort
- visual or interaction excellence
- implementation feasibility

Plan or strategy:

- ambition and upside
- operational realism
- decision clarity

Health, habit, or home routine:

- comfort and adherence
- measurable health or safety
- practical schedule or environment fit

## Anti-Patterns

Avoid:

- three reviewers all judging "quality"
- named personas that do not map to real success conditions
- roles selected because they are familiar rather than useful
- adding a third subagent when two facets already cover the target tension
- selecting subagents to prove the skill was used instead of improving the artifact
- no facet representing the user or customer — technical and operational facets dominate naturally; the user perspective must be checked for explicitly

