# Done policies

This document defines the minimum completion policies for `local-coding-orchestrator`.

## Principle

A task is complete when its required objective checks pass.
A worker process exiting or claiming success is not sufficient.

## Check status vocabulary

Use a small fixed vocabulary for objective checks:
- `pending`
- `passed`
- `failed`
- `blocked`
- `not-required`

## Core checks

Common checks used across task types:
- `build`
- `tests`
- `review`
- `pr`
- `screenshot`
- `artifact`
- `repro`
- `docs`

Not every task needs every check.

## Policy by task type

### Feature

Minimum recommended checks:
- `build`
- `tests`
- `review`
- `pr` when requested
- `screenshot` when UI changed and screenshot proof is required

Completion guidance:
- all required checks must be `passed`
- optional checks may stay `not-required`
- any `failed` check blocks completion

### Bugfix

Minimum recommended checks:
- `repro` or equivalent defect evidence
- `tests`
- `review`
- `build` unless the environment is intentionally check-light

Completion guidance:
- defect scope should be evidenced
- fix should not introduce new lint/type/build failures

### Review-only

Minimum recommended checks:
- `artifact`
- `review`

Completion guidance:
- the review artifact exists
- findings are categorized clearly enough to act on

### Prototype

Minimum recommended checks:
- `artifact`
- `docs`
- `review` optional

Completion guidance:
- result is runnable or demonstrable
- operator knows how to launch or inspect it
- production hardening can remain deferred if declared

## Evaluation rule

A task may be marked `completed` only if:
1. every required check is `passed`, and
2. no required check is `pending`, `failed`, or `blocked`

If some required checks are still pending, the task is not complete even if the worker stopped.

## Suggested policy shape

A future evaluator can use a policy structure like:

```json
{
  "feature": {
    "required": ["build", "tests", "review"],
    "conditional": {
      "pr": "whenRequested",
      "screenshot": "whenUiChanged"
    }
  },
  "bugfix": {
    "required": ["tests", "review"],
    "conditional": {
      "build": "whenBuildable",
      "repro": "whenBugNeedsExplicitRepro"
    }
  }
}
```

## Recommended user-facing report shape

When reporting status, include:
- checks passed
- checks pending
- checks failed
- whether the current result is actionable
- what is needed to reach completion
