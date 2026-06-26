# Decision Rules for Self-Improvement

Use this reference to decide whether a new issue should become:
- a simple learning entry
- an experiment with binary evals
- a promoted operating rule

---

## Option 1 — Log only

Use **log only** when:
- the issue happened once
- root cause is still unclear
- there is not enough evidence yet to turn it into a rule
- the lesson is useful, but not broadly reusable yet

Typical output:
- `learning`
- `error`
- `feature`

Examples:
- one-off API outage
- first-time tool glitch with unclear cause
- user preference that does not affect system-wide ops

---

## Option 2 — Run an experiment

Use an **experiment** when:
- the same failure happened 2+ times
- a new guardrail/SOP/checklist/schema change is being proposed
- you can define 3-5 binary evals
- you want evidence that the change helped before promoting it broadly

Typical output:
- `experiment`
- baseline + mutation + binary evals + keep/discard decision

Examples:
- Mission Control summaries repeatedly missing links/details
- deploy closeout repeatedly confusing code-ready with live
- repeated missing receipts or incomplete proof bundles
- repeated front-end / operator-surface mismatch after backend fixes

---

## Option 3 — Promote immediately

Use **promote immediately** when:
- the rule is already obviously correct and low-risk
- the issue is severe enough that waiting would be irresponsible
- the required change is a principle or ownership rule, not an uncertain optimization
- operator review already confirms the new rule should become standard

Typical output:
- promotion into `AGENTS.md`, `TOOLS.md`, `SOUL.md`, or `docs/ops/*.md`

Examples:
- deployment owner must be explicit
- code-ready is not the same as live
- missing receipt cannot be treated as delivered
- summary without proof links is not operator-complete

---

## Promote after experiment

Use **experiment first, then promote** when:
- the rule sounds plausible but may add friction
- you are not sure whether the added checklist/schema field actually reduces errors
- the change could create process overhead without improving truth quality

Examples:
- adding new summary schema fields
- adding new receipt requirements
- adding extra verification steps to handoff or QA lanes

---

## Anti-patterns

Do **not** run an experiment when:
- there is no clear repeated failure
- the evals would be vague or subjective
- the issue is really just missing execution, not missing learning
- the fix requires immediate owner action, not more analysis

Do **not** promote immediately when:
- the rule is still based on one anecdote
- the change is likely to create bureaucracy without proof of benefit
- the actual failure surface is still unclear

---

## Quick decision tree

1. Did this happen only once?
- Yes → log only
- No → continue

2. Is the new rule obviously necessary and low-risk?
- Yes → promote immediately
- No → continue

3. Can you define 3-5 binary evals for the proposed change?
- Yes → run an experiment
- No → log only until the failure is clearer

4. Did the experiment materially improve the failure pattern?
- Yes → keep and consider promotion
- No → discard or partial_keep

---

## One-line heuristic

**Single incident = log. Repeated pattern = experiment. Clear principle/ownership rule = promote.**
