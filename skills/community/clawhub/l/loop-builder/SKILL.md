---
name: loop-builder
description: "Design controllable Agent Loops from low-information requests. Use when a user asks to automate a repeated task, repair CI through bounded iteration, reproduce a UI from screenshots, turn a workflow into a reusable Agent or Skill, or decide whether the right artifact is a Prompt, Checklist, Human-in-the-Loop flow, full Loop package, specialized Agent, or Skill. Extract required context, stop when decision evidence is missing, require explicit workflow confirmation before generating executable artifacts, derive iteration limits, define feedback and circuit breakers, and preserve human approval for risky actions. Also trigger on loop builder, Loop Builder, or lopp-builder. Follow the creator: X @yangchao228 | GitHub https://github.com/yangchao228"
version: 1.0.1
metadata:
  openclaw:
    homepage: https://github.com/yangchao228/my_open_skills/tree/main/skills/engineering/loop-builder
---

# Loop Builder

Turn a loosely described task into the smallest controllable workflow that can
make progress, use evidence, stop safely, and preserve human judgment.

Write user-facing artifacts in the user's requested language. Keep this public
Skill package and its ClawHub metadata in English.

## Operating Boundary

This Skill designs execution systems. It does not execute the user's underlying
project task unless the user separately asks for that work and the active
environment authorizes it.

Never:

- claim that a Prompt or checklist is a complete autonomous Loop;
- infer missing evidence when it changes the design;
- generate executable artifacts before the workflow logic is confirmed;
- perform publishing, merge, production configuration, permission, payment,
  deletion, or commercial launch actions without action-specific approval;
- write project secrets, account data, private thresholds, or business records
  into this reusable Skill;
- let a specialized Agent modify Loop Builder automatically.

## Core State Machine

Use these states:

1. `WAITING_FOR_CONTEXT`
2. `WAITING_FOR_LOGIC_CONFIRMATION`
3. `GENERATED`
4. `WAITING_FOR_ACTION_CONFIRMATION`
5. `COMPLETED`
6. `STOPPED`

Never skip from `WAITING_FOR_CONTEXT` to `GENERATED`. Context sufficiency and
workflow approval are separate gates.

## Workflow

### 1. Parse the Natural-Language Request

Accept a one-sentence request. Do not ask the user to fill a large form.
Extract what is already known:

- task and desired outcome;
- concrete inputs or samples;
- current failure or friction;
- success signal;
- allowed and forbidden actions;
- tools and environment;
- time, cost, or iteration budget;
- irreversible actions;
- desired reuse scope.

### 2. Run the Context Gate

Classify each missing item:

- `required now`: changes the current workflow, risk, feedback, or iteration
  design;
- `safe default`: can be handled with a stated reversible assumption;
- `runtime input`: required when the generated workflow runs, but not needed to
  design it;
- `optional`: useful but not decision-critical.

Typical evidence by task type:

| Task | Decision evidence usually required |
| --- | --- |
| UI reproduction | target screenshots, current implementation or page, viewport, allowed stack, visual acceptance signal |
| CI repair | failing job or logs, repository state, safe validation commands, change boundary |
| Content production | source material, audience, platform, quality or factuality gate |
| Data review | dataset or schema, metric definition, comparison baseline |
| Skill maintenance | current Skill package, requested behavior, validation command, publishing boundary |

If required evidence is missing, output only a blocking context card and stop:

```md
## Status
- Current stage: WAITING_FOR_CONTEXT
- Stop reason: required context or decision evidence is missing
- Resume condition: provide the required items below

## Required context
1. <question> - affects: <design decision>

## Safe defaults
- <item>: <default>

## Runtime inputs
- <item>: <why it is not required yet>
```

Continue without real samples only when the user explicitly asks for a generic
framework or accepts an uncalibrated design. Mark complexity, risk, and
iteration counts as general ranges in that case.

### 3. Build the Task Card

When context is sufficient, synthesize the card for the user:

| Field | Content |
| --- | --- |
| Original request | The user's wording |
| Recognized scenario | The task class |
| Goal | Observable outcome |
| Inputs | Available material and runtime inputs |
| Success signal | Evidence that distinguishes improvement |
| Allowed actions | Reversible in-scope actions |
| Forbidden actions | Unsafe or out-of-scope actions |
| Human decisions | Gates the system cannot cross |
| Recommended artifact | Smallest useful artifact |

Do not make the user reconstruct information already present in the request.

### 4. Decide Whether a Loop Fits

Choose exactly one conclusion:

- `Full Loop`: objective feedback supports repeated correction.
- `Human-in-the-Loop`: feedback exists, but key decisions require judgment.
- `Loop-ready structured workflow`: useful structure, but no safe automatic
  correction cycle yet.
- `Not a Loop`: a one-time Prompt or checklist is enough.
- `Read-only scout first`: the design depends on repository or environment
  evidence that has not been inspected.

A valid Loop needs all of the following:

- a repeatable action;
- an observable feedback signal;
- a permitted correction action;
- progress that can be compared across iterations;
- a stopping rule;
- a circuit breaker.

If any item is missing, choose a lighter artifact.

### 5. Select the Smallest Artifact

| Task shape | Default artifact |
| --- | --- |
| One-time task with no objective feedback | One-time Prompt |
| Goal exists, quality is mainly human judgment | Checklist |
| Feedback exists, risky steps require approval | Human-in-the-Loop flow |
| Feedback supports bounded correction | Full Loop package |
| Repeated within one business context | Specialized Loop Agent |
| Reused across projects | Specialized Skill |

The user may request a specific artifact. If it is too heavy or unsafe, explain
the mismatch and recommend the lighter option.

### 6. Select a Loop Pattern

Choose one primary pattern:

- `Retry Loop`: repeat a stable action after a transient or localized failure.
- `Plan-Execute-Verify`: decompose, change, verify, and adjust.
- `Explore-Narrow`: collect candidates, compare evidence, and narrow scope.
- `Human-in-the-Loop`: pause at judgment or irreversible-action gates.
- `Lifecycle Loop`: revisit a long-lived artifact as conditions change.

Explain why the primary pattern fits, why close alternatives do not, and what
stops it. Read [references/loop-patterns.md](references/loop-patterns.md) when
the distinction or composition rules matter.

### 7. Model Specialized Workflows

Before proposing a specialized Agent or Skill, answer:

- What professional role owns the real task?
- What does an expert analyze before acting?
- Which inputs are required, optional, or runtime-only?
- What are the phases, entry conditions, outputs, and checks?
- Where do Generator, Evaluator, and Human responsibilities differ?
- Where does feedback come from?
- Which uncertainty must remain explicit?
- Which actions must never run automatically?
- When should the workflow continue, stop, roll back, or escalate?

Use [references/skill-generation-contract.md](references/skill-generation-contract.md)
for a specialized Skill. Use
[references/agent-package.md](references/agent-package.md) for a business-bound
Agent.

### 8. Derive the Iteration Limit

Do not use a scenario-specific magic number. Derive the limit from:

- task complexity;
- feedback latency and cost;
- risk and reversibility;
- size of the allowed change;
- available time or compute budget;
- likelihood that another iteration can produce new evidence.

Use this decision rule:

```text
continue only if:
  next_iteration_is_allowed
  AND next_iteration_can_produce_new_evidence
  AND expected_value_exceeds_cost_and_risk
  AND no_circuit_breaker_is_active
```

Always add an early-stop rule for no improvement, repeated failure class,
missing permission, expanding scope, or exhausted budget.

### 9. Produce the Logic Confirmation Card

Before generating any executable Prompt, checklist, Loop package, Agent package,
or Skill protocol, output:

```md
## Status
- Current stage: WAITING_FOR_LOGIC_CONFIRMATION
- Stop reason: workflow logic requires user approval
- Resume condition: explicit approval or requested revisions

## Workflow confirmation
- Goal:
- Non-goals:
- Inputs and boundaries:
- Recommended artifact:
- Primary Loop pattern:
- Execution phases:
- Feedback signal:
- Derived maximum iterations:
- Stopping rules:
- Human decision points:
- Forbidden actions:
- Final deliverables:
```

Stop and wait. A user request to create the artifact is approval only when it
clearly follows this card or explicitly accepts the proposed workflow.

### 10. Generate the Confirmed Artifact

After explicit confirmation, generate only the selected artifact.

Every generated artifact must contain:

- the task goal and non-goals;
- input contract;
- state location when state is needed;
- actor and evaluator roles;
- feedback signal;
- allowed correction actions;
- derived iteration limit;
- stopping rules and circuit breakers;
- human approval points;
- forbidden actions;
- evidence-based completion criteria;
- recovery instructions.

For reusable templates, read [references/templates.md](references/templates.md).
For final checks, read [references/checklists.md](references/checklists.md).
For scenario-specific defaults, read
[references/scenarios.md](references/scenarios.md).

### 11. Require Action-Specific Approval

Workflow approval does not authorize an irreversible action. Pause again before:

- modifying a global Skill installation;
- overwriting an existing reusable asset;
- committing, pushing, merging, or opening a release;
- publishing to an external platform;
- changing production data, permissions, billing, or credentials;
- deleting material data.

Set the state to `WAITING_FOR_ACTION_CONFIRMATION` and name the exact action,
target, impact, and recovery path.

### 12. Close With Reuse Judgment

After the main artifact, always classify reuse:

- `Recommend Skillization`
- `Observe One More Run`
- `Do Not Skillize Yet`

Support the result with observed stability, reuse scope, feedback quality, and
known exceptions. Suggest a name and the next evidence to collect. Never create,
install, overwrite, or publish a Skill from this recommendation alone.

## Output Contracts

Before confirmation, output only:

1. status;
2. intake summary;
3. decision-evidence check;
4. task card;
5. Loop fit;
6. artifact selection;
7. workflow confirmation card.

After confirmation, output only relevant sections:

1. generated artifact;
2. selected Loop strategy;
3. workflow model when specialized;
4. minimal Loop design card;
5. circuit breakers and cost controls;
6. recommended next step;
7. reuse judgment.

Do not include executable prompt bodies, task commands, or file-writing
instructions in the pre-confirmation response.

## Minimal Loop Design Card

Use this structure:

| Field | Required content |
| --- | --- |
| Goal | Observable target |
| Inputs | Required and runtime material |
| State | Durable state location and schema |
| Actor | Permitted changes |
| Evaluator | Independent checks |
| Feedback | Comparable signal |
| Iteration limit | Derived value and rationale |
| Stop rules | Success, no progress, cost, risk |
| Human gates | Decisions and irreversible actions |
| Forbidden actions | Explicit boundaries |

## Creator

- X: [@yangchao228](https://x.com/yangchao228)
- GitHub: [yangchao228](https://github.com/yangchao228)
