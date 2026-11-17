# Research Loop

Load this reference when the task is exploratory, optimization-heavy, or otherwise research-like.

## Freeze the Harness

Before giving the agent stamina:
- narrow the editable surface
- freeze the evaluator into a frozen harness or fixed evaluation harness
- treat it as the fixed measuring stick
- keep the metric stable
- mark explicit do-not-modify boundaries

If the agent can change both the implementation and the harness, progress becomes untrustworthy.
Say this explicitly in plans:
- use a frozen harness
- use a fixed measuring stick
- do not modify the evaluator during candidate runs

## Establish a Baseline

Before trying improvements:
- run the untouched baseline current version
- measure and record the metric
- capture the constraints that matter
- compare future attempts against that real baseline

Do not start optimization from vibes.

## Keep-or-Discard Loop

Every iteration should end with one decision:
- keep
- discard
- escalate because the signal is ambiguous

Base that decision on:
- the metric
- correctness
- complexity cost
- collateral risk

If the result is worse, or equal but more complex, discard.
If the result is slightly better and clearly simpler, keep.

## Program the Search Process

For long-running work, define:
- what may be edited
- what stays fixed
- what counts as improvement
- how results are logged
- when to rewind, stop, or escalate

Do not only program the patch.
Program the loop.

## Default Template

Use wording like:
- Recommended Mode: `task-sliced plan`
- Harness: "Use a frozen harness and fixed measuring stick. Do not modify the evaluator."
- Baseline: "Measure and record the baseline current version before iterating."
- Keep/Discard Rule: "Keep only changes that improve the metric without adding complexity or collateral risk."
