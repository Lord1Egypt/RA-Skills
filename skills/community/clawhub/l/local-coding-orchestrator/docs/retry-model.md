# Retry model

This document defines the retry strategy for `local-coding-orchestrator`.

## Principle

Retries should preserve learning.
Do not blindly rerun the same prompt unless the failure was purely mechanical.

## Retry classes

### Mechanical retry

Use mechanical retry when the problem was operational rather than conceptual.

Examples:
- shell startup glitch
- transient CLI failure
- workdir mismatch
- temporary permissions issue
- install or process launch hiccup

Behavior:
- keep task intent the same
- fix the execution condition
- preserve accepted scope
- rerun with minimal prompt changes

### Semantic retry

Use semantic retry when the worker misunderstood the task or optimized for the wrong thing.

Examples:
- solved the wrong requirement
- changed the wrong files
- overbuilt instead of making the narrow fix
- ignored required context or definitions
- skipped expected validation or tests

Behavior:
- explain what went wrong
- preserve the valid parts of the prior attempt
- explicitly redirect scope
- restate acceptance focus
- write a new retry brief for the next attempt

## Minimum retry brief fields

A retry brief should include:
- retry reason
- what to preserve
- what to change
- extra context
- acceptance focus

## Task updates

When generating a retry brief for a new attempt, the orchestrator should:
- increment the attempt counter
- update the prompt artifact path
- preserve task history and prior evidence

## Suggested sequence

1. classify failure as mechanical or semantic
2. collect evidence
3. generate retry brief
4. transition task into `retrying`
5. relaunch the worker
6. transition back into `running`
