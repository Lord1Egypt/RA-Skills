# Loop Templates

Copy only the sections needed for the selected artifact.

## Loop State

```md
# <Task> Loop State

## Goal
- target:
- non-goals:
- success signal:

## Inputs
- required:
- runtime:
- assumptions:

## State
- status:
- current_iteration:
- maximum_iterations:
- last_safe_state:
- remaining_budget:

## Work packages
- [ ] <bounded step> - verification: <check>

## Run log
| Iteration | Change | Feedback | Delta | Decision |
| --- | --- | --- | --- | --- |

## Stop rules
- success:
- no progress:
- repeated failure:
- cost:
- risk:

## Human gates
- decision:
- action:
- evidence packet:

## Forbidden actions
- ...

## Retrospective
- useful evidence:
- wasted iteration:
- reusable rule:
- unresolved:
```

## Planner Prompt

```md
Act as the Planner for <task>.

Read:
- goal and non-goals;
- current state;
- latest evidence;
- allowed and forbidden actions;
- remaining budget.

Produce exactly one bounded work package:
- objective;
- files or systems in scope;
- expected evidence;
- verification method;
- rollback or recovery;
- human gate, if any.

Stop instead of planning when required evidence is missing, scope would expand,
or a circuit breaker is active. Do not execute the work.
```

## Read-Only Scout Prompt

```md
Inspect <scope> without changing external or local state.

Return:
- relevant structure;
- current behavior;
- exact evidence paths;
- constraints;
- unknowns that change the plan;
- smallest useful next work package.

Do not implement, publish, commit, or infer missing facts.
```

## Maker Prompt

```md
Execute only the confirmed work package for <task>.

Rules:
- preserve unrelated work;
- keep changes small and reversible;
- do not weaken checks;
- record files or systems changed;
- stop on missing permission, expanded scope, or unsafe recovery.

Return:
- outcome;
- changes;
- evidence produced;
- verification still required;
- any human decision.
```

## Checker Prompt

```md
Independently verify the latest work package.

Compare the result with:
- success signal;
- confirmed scope;
- acceptance checks;
- forbidden actions.

Return:
- pass / partial / fail / blocked;
- evidence;
- remaining gap;
- regression risk;
- recommended next check.

Do not repair the result.
```

## Evaluator Prompt

```md
Evaluate whether another iteration is justified.

Inputs:
- prior and current feedback;
- iteration count and limit;
- remaining budget;
- active circuit breakers;
- unresolved human gates.

Return:
- continue / stop-success / stop-no-progress / stop-risk / wait-for-human;
- evidence delta;
- next permitted correction, if continuing;
- rationale.
```

## Human Decision Packet

```md
## Decision required
- Exact decision:
- Proposed action:
- Target:
- Why now:
- Evidence:
- Risk:
- Recovery:
- Alternatives:
- What happens if deferred:
```

## Failure Report

```md
# <Task> Loop Failure Report

## Outcome
- final state:
- circuit breaker:
- last safe state:

## Evidence
- observed:
- expected:
- gap:

## Attempts
| Iteration | Action | Result | New evidence |
| --- | --- | --- | --- |

## Root-cause assessment
- confirmed:
- suspected:
- unknown:

## Recovery options
1. <option> - impact / cost / approval

## Reuse note
- project rule:
- template improvement:
- Skill candidate:
```

## PR or Change Summary

```md
## Context
<problem and evidence>

## Change
<bounded implementation>

## Verification
<checks and results>

## Risk
<known limits and recovery>

## Human decision
<merge, release, or rollout gate>
```

## Pre-Confirmation Response

```md
## Status
- Current stage: WAITING_FOR_LOGIC_CONFIRMATION
- Stop reason: waiting for workflow approval
- Resume condition: approve or revise the card below

## Intake summary
- Original request:
- Recognized scenario:
- Confirmed evidence:
- Remaining assumptions:

## Task card
| Field | Content |
| --- | --- |
| Goal | |
| Inputs | |
| Success signal | |
| Allowed actions | |
| Forbidden actions | |
| Human gates | |

## Loop fit
- Conclusion:
- Reason:
- Non-automatable part:

## Artifact selection
- Artifact:
- Why:
- Why not a heavier artifact:

## Workflow confirmation
- Pattern:
- Phases:
- Feedback:
- Iteration limit:
- Stop rules:
- Final deliverables:
```
