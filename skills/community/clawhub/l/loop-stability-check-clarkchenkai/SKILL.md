---
name: loop-stability-check
description: |
  Loop Stability Check — Workflow Stability Skill for Detecting Loops, Drift, and Retry Waste. Use it when the user needs a
  disciplined protocol and fixed output contract for this kind of task rather
  than a generic answer.
license: MIT
metadata:
  author: clarkchenkai
  version: "1.0.0"
  language: en
---

# Loop Stability Check — Workflow Stability Skill for Detecting Loops, Drift, and Retry Waste

Use this skill when the task matches the protocol below.

## Activation Triggers

- repeated retries with no improvement
- oscillation between multiple outputs or states
- planning loops that never cash out into execution
- human-bot ping-pong with no stable owner
- cases where repetition is happening but convergence is not

## Core Protocol

### Step 1: Define the intended loop objective

A loop cannot be judged as stable if nobody states what it is supposed to converge toward.

### Step 2: Observe the repeated behavior

Look at retries, state changes, tool calls, or handoff cycles instead of reasoning from theory alone.

### Step 3: Classify the instability

Name the pattern: dead retry, oscillation, drift, amplification, or feedback starvation.

### Step 4: Locate the feedback failure

Ask which signal is missing, delayed, noisy, or being ignored.

### Step 5: Add guardrails and intervention

Recommend retry caps, state locks, escalation triggers, ownership boundaries, or full halts where needed.

## Output Contract

Always end with this six-part structure:

```markdown
## Loop Objective
[...]

## Observed Behavior
[...]

## Stability Risks
[...]

## Likely Failure Mode
[...]

## Guardrails
[...]

## Recommended Intervention
[...]
```

## Response Style

- Describe the loop behavior concretely.
- Prefer named failure modes over generic ‘this seems buggy.’
- Recommend the smallest guardrail that restores convergence.
- Stop the loop when the right action is halt, not another cycle.

## Boundaries

- It does not optimize creativity by forcing every open-ended workflow into rigid convergence.
- It does not confuse ‘more steps’ with ‘more learning.’
- It does not permit repeated motion to substitute for explicit ownership and escalation.
