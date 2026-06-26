# Reference Guide

This skill implements deterministic, attention-style memory routing for OpenClaw.

## Goal

Convert a large memory store into a compact working-memory packet tuned to the current step role:

- planner
- executor
- critic
- responder

## Memory philosophy

This skill is not plain RAG.

Instead of:

1. retrieve flat top-k chunks
2. paste raw history into context

it does:

1. gather deterministic candidates from scope matches, FTS recall, durable memory, and recent fallback
2. assign each candidate to one block: `task_scoped`, `session_scoped`, `durable_global`, or `recent_fallback`
3. score and select the best blocks
4. score memories only inside those selected blocks
5. compose a compact working-memory packet
6. write back learnings and retire stale memory when needed

## Memory types

- `episode` - concrete event, observation, tool result, failure, or action
- `summary` - compressed task or session state
- `reflection` - lesson, warning, diagnosis, or postmortem
- `procedure` - reusable steps for future tasks
- `preference` - durable user or system preference or hard constraint

## Abstraction levels

- `0` - raw or immediate
- `1` - session-level
- `2` - task-level
- `3` - long-term or durable

## Current role routing table

- `planner` -> `preference`, `procedure`, `summary`
- `executor` -> `preference`, `procedure`, `episode`, `reflection`
- `critic` -> `reflection`, `preference`, `summary`
- `responder` -> `preference`, `summary`, `procedure`

Key update:

- `executor` now reads `preference` memory as well as `procedure` memory so durable output constraints survive into execution.

## Recommended writing rules

### `episode`

Use when:

- a tool produced an important result
- a tool failed in a reusable way
- a concrete observation should remain inspectable later

Avoid when:

- the content is temporary scratch work
- the same signal is already captured by a better `summary`

### `summary`

Use when:

- several raw events can be compressed into one stable note
- a task or session reached a durable state worth reusing

### `reflection`

Use when:

- a failure pattern matters
- a lesson should affect future behavior
- a warning should surface as a pitfall next time
- a support/contradiction relationship should influence later ranking

### `procedure`

Use when:

- the steps are reusable
- the workflow has worked or is strongly grounded
- the agent should follow these steps first next time

### `preference`

Use when:

- the user expresses a stable preference
- the environment has a durable rule or hard constraint
- the rule should persist into planning, execution, or response composition

## Two-stage routing logic

### Stage A: block routing

The router first scores four coarse blocks:

- `task_scoped`
- `session_scoped`
- `durable_global`
- `recent_fallback`

Block scoring considers:

- scope bias
- role compatibility
- lexical overlap with goal
- unresolved-question overlap
- recent-failure overlap
- freshness

### Stage B: memory ranking inside selected blocks

The router then ranks memories only inside the selected blocks.

Row scoring uses these signals:

- role match
- lexical overlap with goal, constraints, failures, and open questions
- task match
- session match
- importance
- confidence
- success score
- freshness
- graph support
- graph contradiction
- selected block score

The exact numeric weights live in:

`scripts/memory_router.py`

## Graph semantics

Graph edges are not cosmetic. They influence ranking.

### `supports`

Use `supports` when later evidence validates a memory.

Practical effect:

- helps a validated memory win borderline ranking decisions
- especially useful when two candidate procedures are similarly relevant but only one has supporting evidence

### `contradicts`

Use `contradicts` when a newer memory invalidates an older one.

Current behavior:

- contradiction is treated directionally
- the **target** of the contradiction edge is penalized
- the newer memory asserting the contradiction is not penalized just for being the source of the edge

This is important because otherwise both memories get dragged down and stale memory can remain too competitive.

## Packet design

The packet is the only thing the downstream reasoning step should need.

Current field mapping:

- `preference` -> `hard_constraints`
- `procedure` -> `procedures_to_follow`
- `reflection` -> `pitfalls_to_avoid`
- `summary` / `episode` -> `relevant_facts`

Current caps:

- `selected_memory_ids` -> 5
- `hard_constraints` -> 4
- `relevant_facts` -> 3
- `procedures_to_follow` -> 3
- `pitfalls_to_avoid` -> 3
- `open_questions` -> 5

Why this matters:

- lower token noise
- clearer packet semantics
- less chance of stuffing the next step with redundant memories

## Replacement and refresh policy

Use replacement or refresh whenever:

- a new memory supersedes an old one
- an old preference is explicitly changed
- a procedure is proven wrong
- a summary is outdated after better evidence appears

Recommended lifecycle:

1. mark stale memory inactive
2. set `replaced_by_memory_id`
3. persist a retirement reason
4. add a `contradicts` edge when replacement semantics exist
5. keep the new memory active

If replacement is clear, prefer retiring the stale memory instead of leaving both active and contradictory.

## Suggested integration points in an agent graph

Read before:

- planning
- execution after a failure
- critique or review
- final response composition

Write after:

- important tool result
- major failure
- task completion
- preference discovery
- procedure discovery

Refresh after:

- contradictions
- explicit corrections
- updated durable rules

## Current validated behavior

The optimized skill is expected to satisfy all of these behaviors:

- planner packet reuses durable preference memory
- executor packet preserves both hard constraints and reusable procedures
- reflection can generate reusable procedure memory
- replacement retires stale memory and records forward links
- newer contradictory memory outranks stale contradicted memory
- graph-supported procedure can outrank a slightly stronger but unsupported competitor
- packet output remains compact under dense memory conditions
