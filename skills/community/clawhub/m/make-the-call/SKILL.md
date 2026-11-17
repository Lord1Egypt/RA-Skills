---
name: make-the-call
description: >
  Part of the Overpowered skill suite. Turn sufficient evidence into a clear decision when multiple viable options remain. Use when trade-offs matter and the agent must decide, recommend a cheap discriminating test, or explicitly defer because unresolved uncertainty makes commitment unsafe.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "1-knowledge-evidence-decision"
  version: "0.4.0"
---

# Overpowered / Make the Call

## Core rule

**Close a real choice with exactly one disposition: `DECIDE`, `TEST`, or `DEFER`. Do not hide behind “it depends.”**

This skill owns decision closure. It consumes evidence prepared by other skills; it does not recreate retrieval, reconciliation, precedent analysis, structured-data analysis, or assumption auditing.

## Decision protocol

1. **State the decision.** Write the actual choice in one sentence.
2. **Establish viable options.** Include only options that can genuinely meet the objective. Do not manufacture alternatives; if only one is viable, say so and decide proportionately.
3. **Derive criteria.** Ground each material criterion in the objective, constraints, risks, and success conditions. Record why it matters, supporting evidence, and how strongly it distinguishes the options. Do not invent weights or scores for cosmetic precision.
4. **Resolve material unknowns.** Route missing knowledge to `know-enough`, relevant history to `find-precedent`, structured evidence to `ask-the-data`, conflicts to `reconcile`, and hidden premises to `assumption-audit`.
5. **Account for commitment.** Compare the cost of being wrong, reversibility, cost of further analysis, and cost of delay. Cheap reversible choices deserve proportionate analysis.
6. **Test sensitivity.** Identify the assumptions and criteria that drive the winner. If a small plausible change reverses it, label the recommendation fragile.
7. **Evaluate information value.** Ask whether one realistic fact or cheap experiment could resolve the decision-driving uncertainty. Prefer that test when it costs less than committing under uncertainty.
8. **Choose exactly one disposition:**
   - `DECIDE` when evidence discriminates enough to commit.
   - `TEST` when a cheap bounded experiment can resolve the decisive uncertainty. State the hypothesis, measure, option-favoring threshold/results, and time/cost boundary.
   - `DEFER` when material uncertainty cannot be resolved cheaply now and guessing has unacceptable downside. State exactly what will make the decision ready.

## Output contract

```text
Decision
<one sentence>

Disposition
DECIDE | TEST | DEFER

Why
- <decisive criterion + evidence>

Trade-offs accepted
- ...

Uncertainty
- <remaining uncertainty, sensitivity, and whether it could flip the result>

Reversibility
<high / medium / low + consequence>

Next action
<commit, run the bounded test, or obtain the specific missing input>
```

Keep the response proportional; omit non-material sections for a trivial choice.

## Gotchas

- Do not end with “it depends” or an uncommitted pros/cons list.
- Do not invent numerical weights, scores, or criteria unsupported by the objective.
- Spend detail on discriminating evidence, not equal-length option summaries.
- Do not decide before obtaining material discoverable knowledge or reconciling decisive conflicts.
- Do not paralyze a cheap, reversible choice with research or committee-style analysis.
- Do not disguise a sensitivity-fragile recommendation as certain.
- Do not defer when a cheap discriminating test exists.
- Precedent informs a choice but is not normative authority.

## Composition

Typical minimal chains include `know-enough → make-the-call`, `ask-the-data → make-the-call`, or `reconcile → make-the-call`. Add `assumption-audit` only when hidden premises could change the result.

## Stop condition

Stop when one disposition is selected, its decisive evidence and sensitivity are explicit, and the next action is bounded and executable.
