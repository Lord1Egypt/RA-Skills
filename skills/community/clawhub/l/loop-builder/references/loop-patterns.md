# Loop Pattern Reference

Use this reference after the task and evidence gates pass. Select one primary
pattern. Add a secondary pattern only when it solves a distinct control problem.

## Pattern Matrix

| Pattern | Best for | Main feedback | Primary risk |
| --- | --- | --- | --- |
| Retry Loop | transient or localized failure | success/failure plus error class | repeating the same ineffective action |
| Plan-Execute-Verify | multi-step change with objective checks | tests, lint, build, diff, screenshots | expanding scope while repairing |
| Explore-Narrow | ambiguous search or discovery | ranked evidence and elimination | endless collection |
| Human-in-the-Loop | judgment or irreversible decisions | explicit human decision | pretending approval is optional |
| Lifecycle Loop | long-lived assets and recurring review | trend, drift, or review delta | automation without a meaningful change signal |

## Retry Loop

Choose Retry when:

- the action is stable;
- failure may be transient or narrowly diagnosable;
- each retry can change one relevant variable;
- retry cost is bounded.

Minimum cycle:

```text
attempt -> observe error class -> choose one bounded adjustment -> retry
```

Stop on success, repeated error class without new evidence, maximum cost,
permission failure, or an unsafe workaround request.

Do not use Retry for ambiguous goals, subjective quality, broad refactors, or
tasks where the evaluator cannot distinguish improvement.

## Plan-Execute-Verify

Choose this pattern when:

- the goal can be decomposed;
- the environment exposes objective checks;
- changes can be kept small and reversible;
- verification can guide the next plan.

Minimum cycle:

```text
inspect -> plan one work package -> execute -> verify -> compare -> continue/stop
```

Bind every planned step to a verification method. If verification does not
cover the changed behavior, stop and revise the plan instead of declaring
success.

## Explore-Narrow

Choose this pattern when the task begins with uncertainty:

```text
define criteria -> collect bounded candidates -> compare evidence
-> remove weak options -> inspect the strongest remaining option
```

Set collection limits before searching. Stop when one candidate satisfies the
decision criteria, when new candidates no longer change the ranking, or when
missing evidence requires human input.

## Human-in-the-Loop

Choose this pattern whenever the system can prepare evidence but a person must
own the decision.

Minimum cycle:

```text
prepare -> verify -> present decision packet -> wait
-> record decision -> execute only the approved action
```

Approval must identify the action and target. General workflow approval does not
authorize publishing, payments, deletion, permission changes, or production
writes.

## Lifecycle Loop

Choose this pattern for an artifact that is expected to evolve:

```text
capture baseline -> observe a new signal -> compare drift
-> propose an update -> review -> version the accepted change
```

Define the review trigger. A calendar alone is not sufficient if no meaningful
signal can change the artifact.

## Composition Rules

- Use `Plan-Execute-Verify + Human-in-the-Loop` for code changes that lead to a
  release or production action.
- Use `Explore-Narrow + Human-in-the-Loop` for research that ends in a strategic
  or editorial decision.
- Use `Lifecycle + Plan-Execute-Verify` for maintaining reusable Skills or
  operating procedures.
- Use Retry only inside a bounded step. Do not make it the outer pattern for an
  ambiguous project.
- Keep one primary pattern so the state machine and stopping rule remain clear.

## Tool Boundary

A Loop design may name tool classes and verification commands that are already
known. Mark unknown paths, capabilities, credentials, and commands as runtime
inputs. Never invent an executable command to make the template appear
complete.
