# Loop Checklists

## Fit Check

- [ ] The target is observable.
- [ ] At least one feedback signal distinguishes improvement.
- [ ] A permitted correction action can respond to that signal.
- [ ] Progress can be compared across iterations.
- [ ] State persists across iterations when needed.
- [ ] The maximum iteration count is derived from cost, risk, and evidence.
- [ ] Success, no-progress, cost, and risk stops are explicit.
- [ ] Irreversible actions have human gates.
- [ ] The workflow is lighter than the problem it solves.

If any of the first four items fail, choose a Prompt, checklist, or read-only
scout instead of a full Loop.

## Minimum Acceptance Card

```md
## Acceptance
- Goal:
- Evidence:
- Verification method:
- Remaining gap:
- Human decision required:
- Final state: pass / partial / stopped / blocked
```

Never convert `partial`, `stopped`, or `blocked` into `pass`.

## Circuit Breakers

Stop when any condition is true:

- the same failure class repeats without new evidence;
- the feedback signal does not improve for the agreed window;
- required context, permission, or credentials are missing;
- scope expands beyond the confirmed task;
- the evaluator cannot verify the latest change;
- cost, time, compute, or retry budget is exhausted;
- a proposed workaround weakens safety or validation;
- a change becomes difficult to recover;
- an irreversible action lacks exact approval.

Report:

```md
## Circuit breaker
- Trigger:
- Evidence:
- Last safe state:
- Actions attempted:
- Recovery options:
- Decision needed:
```

## Cost Controls

- Prefer read-only inspection before mutation.
- Change one meaningful variable per iteration.
- Reuse durable state instead of rediscovering context.
- Run the narrowest relevant verification first.
- Escalate to broader verification only when risk requires it.
- Stop speculative branches after they stop changing the decision.
- Keep expensive generation or external writes behind explicit gates.

## Retrospective

- Did the feedback signal predict real quality?
- Which iteration created new evidence?
- Which iteration repeated work?
- Was the limit too high or too low?
- Did a human gate occur at the correct moment?
- What failure should become a circuit breaker?
- What stable rule belongs in a project document, template, Agent, or Skill?
- What remains business-specific and must not be generalized?

## Human-Control Check

- [ ] The person retains decisions over goals and risky actions.
- [ ] Evidence is visible enough to challenge the system.
- [ ] Automation reduces repetitive work without hiding uncertainty.
- [ ] Durable artifacts remain portable and inspectable.
- [ ] The workflow can be stopped without losing the last safe state.
