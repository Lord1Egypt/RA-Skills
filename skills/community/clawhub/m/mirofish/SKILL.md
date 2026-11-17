---
name: mirofish
description: Build MiroFish-style multi-agent prediction workflows offline by extracting seed structure, designing an ontology, writing a simulation plan, producing a forecast brief, and generating interview questions. Use when the user wants to turn news, policy drafts, financial signals, or story material into a parallel-world prediction workflow without requiring the original MiroFish backend.
---

# MiroFish

## Overview

Use this skill to turn seed material into a MiroFish-style prediction workflow without needing the original backend. Treat the task as structured world-building, not summarization.

Seed material -> scenario structure -> ontology -> simulation plan -> forecast brief -> interviews

If a live backend is explicitly available and requested, treat that as an add-on path, not the default.

## 1. Extract the Scenario

From the seed material, identify:

- core entities: people, organizations, events, policies, places, assets
- relationship types: support, conflict, dependency, cause, influence, transfer, response
- timeline anchors: already happened, pending, hypothetical, deadline-bound
- explicit constraints: what must happen, what must not happen, what time horizon matters

Keep only entities and relations that can change the outcome.

Prefer relations that affect behavior or decision-making:

- `supports`
- `opposes`
- `depends_on`
- `causes`
- `blocks`
- `influences`
- `allocates`

Avoid decorative relations that do not help prediction.

## 1.5 Identify Inference Targets

Before designing the ontology, mark:

- decision points: moments where actors choose between distinct paths
- constraint violations: events that would invalidate the forecast
- observable signals: facts that would confirm or refute each branch
- branch drivers: the few variables that can actually flip the outcome

If no clear decision points exist, ask the user for more context or narrow the scenario.

## 2. Design the Ontology

Turn the scenario into a compact ontology.

For each entity type, define:

- what it represents
- what distinguishes it from similar entities
- what evidence in the seed material supports it
- what it can do inside the simulation

For each relation type, define:

- direction
- meaning
- whether it is observable, inferred, or hypothetical
- whether it should affect simulation behavior

## Ontology Quality Check

Require the ontology to pass these checks before moving on:

- every major actor in the seed material has a place in the schema
- relation types are specific enough to guide simulation behavior
- conflicting labels or duplicate concepts are merged
- the ontology is small enough to simulate, not an exhaustive taxonomy

If the ontology is too vague or too broad, refine it before continuing.

## 2.5 Build an Offline Simulation Plan

When no backend is available, convert the ontology into an explicit simulation plan instead of stopping.

Include:

- agent roles and their incentives
- memory scope and what each role knows
- likely conflicts and coalition patterns
- 2-3 branch drivers that can flip the outcome
- stop conditions and what evidence would count as a branch change

Keep the plan executable by another agent or human, not just descriptive.

## 3. Design the Simulation

Choose simulation parameters from the user's intent:

- agent scale: enough to cover the main viewpoints, not a fake population census
- interaction channels: only the channels needed for the scenario
- memory scope: seed facts, important context, and the few signals that drive divergence
- round structure: enough rounds to expose convergence, conflict, or branching
- stop condition: target date, stable convergence, or clear fracture

Design for tension, not just crowd size. Include agents that:

- hold conflicting incentives
- control scarce information or resources
- represent institutions, not only individuals
- can plausibly shift the trajectory

## Simulation Quality Check

Require the simulation design to answer:

- what specific outcome is being forecast?
- which agents have conflicting incentives on that outcome?
- which 2-3 signals would flip the result if they changed?
- how do you detect stable convergence or irreversible split?
- what would make this scenario unsuitable for MiroFish?
- can the plan produce at least 3 meaningful branches?
- can the forecast brief justify each branch with evidence?

If the design cannot answer these, refine the agents, add missing constraint entities, or ask for missing assumptions.

## 4. Generate the Report

The report should include:

- the forecast target
- the scenario summary
- the key entities and relationships
- the most likely trajectory
- meaningful alternative branches
- confidence and caveats
- what evidence supports each claim

Separate observed facts from inferred branches.

## 4.5 Extract the Prediction Chain

From the simulation output, trace:

1. which agent actions moved the outcome
2. which constraints blocked alternative branches
3. which assumptions, if wrong, would reverse the forecast

The report must expose this chain, not just summarize the most common trajectory.

## 5. Interrogate the Simulated World

After the report, use interviews to test the forecast.

Ask questions that expose:

- motives
- constraints
- alliances
- likely reactions to shocks
- where public statements diverge from private incentives

Use interviews to test weak links in the forecast chain:

- ask counterfactuals
- ask for hidden constraints
- ask how a key shock would change behavior
- compare stated intent with simulated action

When answers conflict, treat that as a signal, not noise.

## 5.5 Offline Execution Mode

When no backend exists, simulate the same sequence in text:

1. Write the ontology.
2. Write the simulation plan.
3. Produce the report as a forecast brief.
4. Produce interview questions for each key branch.
5. Revise the brief when the interview answers change the causal chain.

Do not mention backend endpoints in the primary answer unless the user explicitly asks for live execution details.

If a user or downstream agent tries to force an API-first interpretation, answer with the offline planner instead of inventing a backend call.

Minimum quality bar for offline output:

- the forecast brief must contain 3 or more branches
- the interview set must contain 5 or more questions
- at least one branch must be revised after the interview pass
- the final answer must distinguish facts, inferences, and uncertainty

## Optional Backend Add-On

If the user explicitly wants live execution against the original repository, consult the backend reference files and follow the repository workflow. Do not make that the default path.

## What to Produce

When asked to use MiroFish, produce one or more of:

- a prediction brief
- an ontology sketch
- a simulation plan
- a report outline
- interview questions
- a follow-up analysis after the report

## Reference Files

- See [references/output-patterns.md](references/output-patterns.md) for the output shapes this skill should generate.
- See [references/worked-example.md](references/worked-example.md) for a backend-free worked example.
- See [references/offline-playbook.md](references/offline-playbook.md) for the recommended no-backend workflow.
- See [references/workflow-map.md](references/workflow-map.md) for the repository workflow when a backend exists.
- See [references/api-surface.md](references/api-surface.md) for endpoint coverage when a backend exists.
- See [references/runtime-contract.md](references/runtime-contract.md) for execution defaults and failure handling when a backend exists.
