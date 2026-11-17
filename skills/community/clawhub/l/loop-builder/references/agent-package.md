# Specialized Loop Agent Package

Use a specialized Agent when one workflow repeats inside the same business
context and needs durable state, but is not yet a cross-project Skill.

## Three-Layer Boundary

1. `Loop Builder` owns general control logic.
2. The specialized Agent owns business workflow, state, and thresholds.
3. Run logs own individual inputs, outputs, evidence, and decisions.

The Agent may record candidate general rules. It may not edit Loop Builder.

## Suggested Package

```text
<agent>/
  LoopAgent.md
  state.md
  input.schema.json
  runs/
  rule-candidates.md
```

Only include files the runtime actually needs.

## LoopAgent.md Contract

```md
# <Task> Loop Agent

## Role
- Owns:
- Does not own:

## Scope
- Repeated business task:
- Allowed environment:
- Non-goals:

## Inputs
- Required:
- Optional:
- Runtime-only:

## Outputs
- Primary artifact:
- Evidence:
- State update:

## Workflow
1. Inspect:
2. Plan:
3. Execute:
4. Verify:
5. Present human decision:

## Control
- Primary Loop pattern:
- Feedback signal:
- Allowed correction:
- Maximum iterations and rationale:
- Stop rules:
- Circuit breakers:

## Human gates
- Decision:
- Irreversible action:

## Forbidden actions
- ...
```

## State Contract

```md
# <Task> Loop Agent State

## Current state
- status:
- updated_at:
- last_safe_state:
- current_iteration:
- iteration_limit:

## Confirmed rules
- ...

## Current run
- input:
- plan:
- output:
- evidence:
- unresolved:
- human_decision:

## Run index
| Run | Input | Result | Evidence | Decision |
| --- | --- | --- | --- | --- |

## Candidate general rules
- rule:
- supporting runs:
- counterexamples:
- proposed scope:
- review status:
```

## Rule Promotion Gate

Promote a candidate rule only when:

- it appears in more than one relevant run;
- its boundary and counterexamples are documented;
- it does not contain business data or private thresholds;
- a person confirms that it should become a reusable rule;
- the target Skill passes its own maintenance and validation workflow.

Until then, keep it in the Agent package.
