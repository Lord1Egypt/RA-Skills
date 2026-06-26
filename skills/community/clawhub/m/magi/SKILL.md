---
name: magi
description: Autonomous behavioral research loop that optimizes agent behavior through correction tracking and multi-perspective (MAGI) verification.
version: 1.8.0
metadata:
  openclaw:
    emoji: "🧬"
    autonomous: false
---

# Self-Improving

Autonomous behavioral research loop with multi-perspective process verification.

## Architecture

```
SKILL.md         # Policy — human edits
memory.md        # State — agent edits
experiments.md   # Log — append-only
corrections.md   # Data — append-only
```

**Constraints:** Three files are writable, each with a specific access mode:
- `memory.md` — **edit** (add, modify, or delete rules)
- `corrections.md` — **append-only** (new entries at end, never modify or delete existing)
- `experiments.md` — **append-only** (new entries at end, never modify or delete existing)

SKILL.md is read-only to the agent — only the user edits policy.
The metric definition is the fixed evaluation harness — do not redefine it.
Do not infer from silence. The dataset is explicit corrections only.

## The Metric

**Correction rate** — how often the user corrects the agent. Lower is better.
A **correction** is any explicit user statement that the agent's output was wrong,
unwanted, or should have been different. User edits count. Ambiguous signals don't.

The agent is both subject and evaluator — no external measurement function.
This dual role can create self-reinforcing loops: the agent may interpret
reduced corrections as success when it has actually drifted from user intent
in ways the user hasn't noticed yet. Compensate: require strong, unambiguous
signals. Be conservative. When in doubt, ask the user rather than self-affirm.

## The Experiment Loop

Event-driven, asynchronous — APPLY and MEASURE resolve in different cycles.
Rules in Applied are concurrent independent experiments.

**Baseline:** First cycle: log starting state (zero rules) in experiments.md.

**Mode:** If `autonomous: false` (default), pause and ask the user for confirmation
before APPLY (step 4) and MEASURE (step 5). If `autonomous: true`, continue the
loop without interrupting the user's workflow.

If out of ideas, re-read corrections.md, combine near-misses, try the opposite
of what failed.

```
ON CORRECTION or SELF-REFLECTION (after completing work or receiving feedback):

1. LOG — Append to corrections.md: YYYY-MM-DD | wrong → wanted.

2. HYPOTHESIZE — What rule prevents this class of correction?
   Trace: observation → generalization → scope → rule.

3. VERIFY — Audit reasoning chain through the MAGI Check.
   2/3 lenses on Steps 2–4 → proceed. Fails → discard.

4. APPLY — Write rule to memory.md Applied section.

5. MEASURE (next encounter) — outcome verification, not process verification.
   Absence of correction is a weak signal; the user may not have encountered
   the relevant scenario. Only count repeated non-correction across multiple
   relevant encounters as strong evidence.
   - User does NOT correct → KEEP. Move to Rules. Log "keep".
   - User corrects same class → FAILED. Delete from Applied. Log "revert".
   - 14 days untested → TIMEOUT. Delete from Applied. Log "discard".

Log = append one row to experiments.md at resolution (not at APPLY).
If VERIFY fails at step 3, log immediately as "discard".
```

Revert = delete the rule. Rules are independent lines — surgical deletion,
not full-file restore. Immediate harm → delete, log "crash", move on.

**Drift guard:** If 3 consecutive experiments end in revert, discard, or crash,
pause the loop and surface the pattern to the user regardless of autonomous mode.
Consecutive failures suggest the agent is misreading the user's intent.
Conversely, if 5 consecutive rules are kept without any user-initiated correction
triggering the cycle, surface the current rule set for user review — a long
streak of self-confirmed successes in a self-evaluating system is as suspect
as a streak of failures.

### Search (when stuck)

Self-reflection alone cannot generate novel reasoning once committed to an answer.

- Re-read corrections.md for unexploited patterns
- Combine near-miss rules that individually failed
- Try the opposite of a recently failed hypothesis
- Look for corrections recurring despite existing rules

## The MAGI Check

Audit the **reasoning chain** — each step, not just the conclusion.
Process verification outperforms outcome verification.

Single agent with three lenses has conformity bias — all lenses share the
model's blind spots and cannot surface errors the model itself cannot recognize.
The 2/3 vote is a structured reasoning discipline, not independent verification.
In a single-agent setting, conformity bias can make self-debate worse than no
debate: the check becomes rubber-stamping rather than verification. Compensate:
actively seek reasons each step FAILS, and treat unanimous agreement with the
same scrutiny as disagreement. The value of the check lies in evaluating each
reasoning step independently — catching errors where they originate, not in
the number of perspectives applied.

### Chain to Audit

```
Step 1. Observation — "User said X" — accurately captured? (factual check)
Step 2. Generalization — "User prefers Y" — follows from observation?
Step 3. Scope — "Applies to Z" — justified, or situational?
Step 4. Rule — "Do Y in Z" — faithfully encodes the generalization?
```

### Three Lenses (Steps 2–4)

**MELCHIOR (Scientist):** Logically valid? Overfitting to one incident?
**BALTHASAR (Mother):** Serves the user? Lasting preference or one-time ask?
**CASPAR (Woman):** Worth the complexity? Simpler alternative exists?

Dissent: MELCHIOR → more evidence. BALTHASAR → clarify with user. CASPAR → simplify.
2/3 on all steps → commit. Override confirmed rule → 3/3. This tiered threshold
mirrors the principle that verification stringency should scale with decision
stakes — routine additions require less consensus than overturning established rules.

## Memory Format

memory.md: single file the agent edits. Cap: 50 lines.

```
## Rules (verified, kept)
- [rule]: [rationale] (kept: YYYY-MM-DD, used: Nx)

## Applied (awaiting measurement)
- [rule]: [rationale] (applied: YYYY-MM-DD)
```

Unused 30 days → remove. Conflicts: specific > general > most recent > ask user.

## Corrections & Experiment Log

corrections.md: `YYYY-MM-DD | wrong → wanted`. Keep last 30.

experiments.md: `date | hypothesis | magi | rules_count | outcome | status`

Example:
```
2026-03-25 | — | — | 0 | baseline | keep
2026-03-25 | use tabs | 3/3 | 1 | no correction | keep
2026-03-26 | increase verbosity | 1/3 | 1 | MELCHIOR: overfitting | discard
2026-03-27 | formal tone | 2/3 | 2 | corrected again | revert
```

`rules_count` = complexity metric. `status`: keep, discard, revert, crash.

## Triggers

| Signal | Action |
|--------|--------|
| User corrects | Log + full cycle |
| Repeated correction | Flag failure, escalate |
| "Always / Never X" | Full cycle, high confidence |
| Task succeeds | Note signal only |
| After multi-step work | Self-reflect, cycle if concrete |

NOT triggers: silence, one-time instructions, hypotheticals, third-party info.

## Security & Simplicity

Never store: credentials, financial data, health info, third-party info.
"What do you know?" → show memory.md. "Forget X" → remove, confirm.
The best memory.md is the smallest one that minimizes correction rate.
Fewer rules = always better.

## Setup Note

After `clawhub install magi`, the skill lives at `./skills/magi/`.
The agent needs write access to this directory — it edits `memory.md`
and appends to `experiments.md` and `corrections.md` during operation.

By default the agent pauses for user approval before applying or reverting
rules. To allow autonomous operation, set `autonomous: true` in the frontmatter.
