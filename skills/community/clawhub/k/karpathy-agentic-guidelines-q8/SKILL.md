---
name: karpathy-agentic-guidelines-q8
description: Compact q8 Karpathy-inspired agentic coding guidance. Use when you need bounded autonomy, verification discipline, and context control without loading the full skill.
---

# Karpathy Agentic Guidelines - Q8 Compact

## Overview

Use agents for generation and iteration.
Keep human authority over intent, truth, review, and release.

This quantized variant keeps only the highest-signal operating rules in `SKILL.md`.
Load references only when the task is exploratory enough to need them.

## When to Use

Use when:
- the task is large enough that agent loops are useful
- assumptions could silently drift
- success criteria are clearer than the implementation path
- you care about keeping the result understandable
- the work involves delegation, verification, or bounded autonomy

Do not use when:
- the task is trivial
- there is no meaningful verification surface yet
- the real problem is missing product direction, not execution discipline

For exploratory optimization or research-like loops, also load:
- [research-loop.md](references/research-loop.md)

## Core Rules

### 1. Program in Outcomes

Prefer:
- success criteria
- invariants
- boundaries
- explicit non-goals

Do not over-specify the path unless the path itself matters.

### 2. Make Assumptions Explicit

Require the agent to:
- surface assumptions that matter
- name unclear inputs
- call out conflicting evidence
- push back when the requested shape looks riskier than a simpler one

Silent assumption choice is one of the main failure modes.

### 3. Keep a Human Review Surface Open

Agents generate.
Humans discriminate.

Review the actual changed files and check that every changed line traces back to the request.
Do not treat "it ran" as sufficient proof.

### 4. Pick the Lightest Viable Mode

Choose the smallest execution mode that preserves clarity:
- `direct execution` for small, obvious, low-risk work
- `declarative plan` when success is clear but the path should stay flexible
- `task-sliced plan` when multiple files or checkpoints matter
- `supervised delegation` when tasks can be isolated cleanly

Do not default to either maximum ceremony or maximum autonomy.

### 4.5. Use Defaults, Not Menus

When multiple paths could work:
- pick one default
- say why it is the default
- keep alternatives as escape hatches

For example:
- `direct execution` is the default for small, obvious bugfixes
- `task-sliced plan` is the default for research loops or multi-surface work

### 5. Bias Toward Simple Construction

Prefer:
- direct code
- local reasoning
- fewer moving parts
- the naive correct version first

Do not invent extra helper layers, config surfaces, or abstractions without need.

### 6. Treat Unrelated Edits as Regressions

Do not allow:
- unrelated refactors
- style churn
- comment churn
- orthogonal deletions

Clean up only what your requested change made unnecessary.

### 7. Anchor the Loop

Use:
- failing tests
- reproducible bug cases
- browser or runtime checks
- explicit output contracts
- diff constraints

If the loop has no anchor, it will drift.

### 8. Control Autonomy

Use bounded autonomy:
- scoped tasks
- explicit authority boundaries
- visible verification
- clear escalation points

Do not let any session become a hidden planning authority, hidden truth source, or hidden release gate.

## Authority Map

- the agent may:
  - generate code
  - run bounded checks
  - iterate toward declared success criteria
  - surface tradeoffs and simplifications
- the supervising human or controller keeps authority over:
  - intent
  - canon or source-of-truth decisions
  - approval and release
  - architectural fallback choices
  - final judgment when signals conflict

If a delegated session starts acting sovereign, pull authority back.

## Verification Surfaces

Do not collapse all verification into "tests passed".

Check:
- behavior verification
- scope verification
- truth alignment
- runtime or materialized-state verification when relevant

## Quick Reference

Before starting:
- define success criteria
- define boundaries and non-goals
- surface risky assumptions

While executing:
- keep steps small and reviewable
- prefer the naive correct version first
- verify after each meaningful change

For research-like loops:
- use `task-sliced plan`
- call the evaluator the `frozen harness` and `fixed measuring stick`
- say `do not modify` the evaluator during candidate runs
- measure and record the baseline current version before iterating
- log each attempt and end with `keep`, `discard`, or `escalate`

Before calling it done:
- run the checks
- inspect the diff
- verify code/config/docs/runtime alignment when relevant
- explain the resulting shape
- state residual risks honestly

## Common Mistakes

### Mistake: Over-directing the implementation
Fix:
- describe the target behavior and constraints, not every keystroke

### Mistake: Letting the model choose assumptions silently
Fix:
- require explicit assumptions for anything non-trivial or high-risk

### Mistake: Accepting a large diff because tests passed
Fix:
- review for conceptual correctness and scope discipline

### Mistake: Moving fast but understanding less
Fix:
- require concise post-change explanations and file accountability
