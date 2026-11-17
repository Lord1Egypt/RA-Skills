---
name: hold
description: Stop-and-recover gate that triggers ONLY on failures not anticipated in preflight's residual risk list. When triggered, stops all agent action, classifies the failure (new class, materialised risk, or invalidated plan), produces a structured report with evidence, offers exactly three options (fix-and-restart, continue-with-caution, abort), and waits for user selection. Explicitly NOT for routine errors or transient errors. Prevents blind retry loops on systemic issues while enabling graceful recovery.
license: MIT
---

# Hold

Stop when the plan is wrong. Don't improvise. This skill activates when something fails or deviates from the plan in a way that wasn't already flagged as a residual risk during preflight. Its job is to stop the agent, classify what happened, and present clear recovery options — never to auto-correct.

## When this runs

Precise trigger conditions:
- Something failed OR deviated from plan, AND
- The failure is NOT in preflight's residual risk list

Explicitly NOT for:
- Routine errors the plan already anticipated
- Transient errors (retry once, then escalate)
- The cheap test failing during preflight (that's preflight's job)

State why this distinction matters: a skill that stops on every error trains the user to ignore it.

## Procedure

### 1. Stop immediately

Do not retry. Do not try a workaround. Do not continue to the next step.

### 2. Classify the failure

Determine which of these three:
- New failure class: a type of error the plan did not consider
- Materialised residual risk: something preflight listed, now happening
- Invalidated plan: an assumption the plan rested on is false

### 3. Produce the report

Output exactly this template wrapped in a markdown code block. Make absolutely sure the closing fence is on its own line:

```markdown
## Hold - Unhandled Failure

### What happened
- Step: [where in the plan]
- Error: [exact message, no paraphrase]
- Classification: [new class / materialised risk / invalidated plan]

### Why this wasn't anticipated
[one sentence - honest, not defensive]

### Current state
- Completed: [what finished]
- In progress: [what was mid-flight]
- Side effects: [what was written, sent, or changed]

### Options

1. Fix and restart
   - Fix: [specific change]
   - Restart from: [step name]
   - Estimated additional cost: [range]

2. Continue with caution
   - Proceed despite the failure
   - Risk: [what could go wrong]
   - Only sensible if: [condition]

3. Abort
   - Stop the task
   - Cleanup needed: [list, or "none"]
   - What remains done: [list]

### Awaiting decision
Reply "1", "2", or "3".
```

### 4. Wait

Do not take any of the three options until the user chooses.

## Rules for this skill

- Only trigger on unhandled failures. Routine errors are not this skill's job.
- Always give three options, even if one is clearly wrong. The user decides.
- Never improvise a fix. Never retry "just once". The stop is the value.
- If the user picks option 1, run preflight again on the fixed path before restarting.

## Common mistakes

- Stopping on every error. This skill is for unhandled failures only - if preflight anticipated it, do not trigger hold.
- Skipping the classification step. "New class" vs "materialised risk" vs "invalidated plan" changes the recovery path.
- Improvising a workaround instead of stopping. The stop is the point.
- Triggering on the cheap test failing during preflight. That is preflight's domain, not hold's.
- Resuming without the user picking an option. The user decides.