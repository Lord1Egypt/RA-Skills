# Planning Strategies

Match strategy to the dominant uncertainty, not to the task's topic. A migration and an essay both use Iterative if the real unknown is "what does good look like".

## Strategy Templates

### Sequential
```
1. A (blocks B)
2. B (blocks C)
3. C (final output)
```
Use when: each step needs the previous step's output.
The trap: natural order ≠ safe order. Within dependency constraints, front-load the step most likely to invalidate the plan (ordering rule → SKILL.md, Core Rules). Backup → transform → validate → deploy, never deploy-then-validate.

### Parallel
```
Contract: agree interfaces FIRST
Track 1: A1 → A2 → A3
Track 2: B1 → B2 → B3
Merge: named step with its own check
```
Use when: components are truly independent.
Precondition: interface agreement before splitting — schema, API signature, or section outline. Parallel dies at the merge: two tracks each "five minutes from done" that do not compose. The merge is a plan step with its own observable check, never "combine results".

### Iterative
```
Cycle 1: Draft → Feedback → Revise
Cycle 2: Draft → Feedback → Revise
Cycle 3: cap
```
Use when: acceptance is subjective (writing, design, tone) and cannot be specified upfront.
Cap at 3 cycles. Not converging by cycle 3 means the acceptance criteria are the problem, not the draft — stop and renegotiate criteria instead of producing a fourth draft. Each cycle needs a named direction change; a cycle without one is polishing, and polishing is done outside the plan.

### Spike-First
```
1. Spike: ONE yes/no question, timeboxed
2. Decide: continue, pivot, or kill
3. Execute: full plan only if spike said yes
```
Use when: estimate range ratio >3x (→ SKILL.md, Core Rules), or a step has no attachable check (→ `decomposition.md`, Done-Checks).
A spike has exactly one question with a yes/no answer. Timebox expires without an answer → the question was too big: split it, do not extend the timebox. Spike output is a decision, not code — declare the code disposable upfront, or the spike quietly becomes the untested implementation.

### Checkpoint
```
1. Milestone A → checkpoint (human can still change X)
2. Milestone B → checkpoint (human can still change Y)
3. Final delivery
```
Use when: >1 day duration, or the human's picture of "done" may drift from yours mid-flight.
Place checkpoints at irreversibility boundaries, not time intervals: the checkpoint before the deploy is worth ten status updates after safe steps. Each checkpoint states what is still changeable; a checkpoint where nothing is decidable is a status update — cut it.

## Strategy Selection

| Task characteristic | Strategy |
|---------------------|----------|
| Clear steps with real dependencies | Sequential |
| Independent components, interfaces agreeable upfront | Parallel |
| Subjective acceptance (writing, design) | Iterative |
| Feasibility unknown | Spike-First |
| >1 day duration | Checkpoint |
| High stakes and novel | Checkpoint + Iterative |
| Anything else / unsure | Sequential, riskiest step first |

## Strategy Combinations

Complex tasks layer strategies; the combination is chosen at plan time, not improvised:

- **Feature development:** Spike-First (kill bad approach early) → Sequential (API → logic → UI) → Checkpoint after each layer.
- **Content creation:** Iterative per section, Checkpoint between sections — feedback on section 1 changes sections 2-5 cheaply.
- **Migration:** Sequential (rollback script → backup → transform → validate → deploy) + Checkpoint before the irreversible step.

## Minimum Viable Plan

| Risk level | Include |
|------------|---------|
| Low | Steps only |
| Medium | Steps + outputs + estimate range |
| High | Steps + outputs + risks + rollback + checkpoints |
| Unknown | Treat as High until the first checkpoint proves otherwise |

## Adapting Strategy

Strategy verdicts live in the outcome log (`outcomes.md`), one line per type in the Current Defaults block:

```
code/refactor: Parallel → ⚠️ merge conflicts twice; default now Sequential
writing/docs: Iterative → ✅ converges in 2 cycles
migration/schema: Checkpoint → ✅ never skip the pre-deploy checkpoint
```

A strategy failure entry without a why ("didn't work") teaches nothing and does not count as evidence for switching.
