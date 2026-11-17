# Risk — Irreversibility, Rollback, Blast Radius

The risk decision is the plan's payload (SKILL.md, Core Rules). This file is how to make it: find the riskiest assumption, classify irreversibility, size the blast radius, and design rollbacks that actually roll back.

## The Riskiest Assumption

- Definition: the assumption whose failure invalidates the most downstream steps. Find it mechanically: for each assumption ask "if this is false, which steps survive?" — fewest survivors wins.
- It gets tested as early as dependencies allow (SKILL.md, Core Rules), with the cheapest test that could falsify it — a curl against the real API beats a full client implementation.
- Pre-mortem, one line at plan time: "It is a month later and this failed — write the most likely cause." If the answer is not already a tested assumption or a named risk in the plan, add it as one.

## Irreversibility Taxonomy

| Class | Definition | Examples |
|---|---|---|
| Irreversible | No path back to the prior state | Sent email/message, published release or post, deleted data with no backup, executed payment, exposed secret, third parties already acted on your output |
| Recoverable-at-cost | A good state is reachable; the cost is real | Dropped table with last night's backup (lose a day of writes), force-push inside the reflog window, deleted resource that can be re-created but re-configured by hand |
| Reversible | Undo restores the prior state | Git-tracked edits, config change with the old value recorded, feature-flagged change with the flag off |

- Column decision: recoverable-at-cost counts as "plan needed", not "reversible" (SKILL.md, The Planning Decision) — and the plan names the recovery cost explicitly.
- Recovery windows decay: reflog expiry, backup rotation, trash retention. Record the window next to the rollback line ("restorable until Friday's backup rotation") — a rollback with an expired window has silently changed class to irreversible.

## Blast Radius

| Radius | If the step fails | Forces |
|---|---|---|
| Self | Retry; nobody notices | Nothing extra |
| User | Rework, apology, trust cost | L2; announce deviations |
| Third parties | External side effects you do not control | L2 + human validation — sending anything external (email, publish, payment, customer-visible data change) sits here |

Reputation makes things irreversible that look recoverable: a wrong email can be corrected but not unsent. When classifying, ask what the *recipient* can undo, not what you can.

## Rollback Design

- The rollback is a plan step with its own check, ordered before the irreversible step (SKILL.md, Plan Format). A rollback never tested is a hope, not a rollback.
- Design it for mid-step failure, not only full completion: what state exists if the step dies halfway? The partial-state rollback is the one that gets used.
- No rollback exists → say so in the plan line and name the mitigation: "Irreversible steps: 4 — rollback: none; mitigation: dry-run against staging copy in step 2."

## Mitigation Ladder

Cheapest-first conversions of irreversible → recoverable; pick the cheapest that actually converts the class:

1. Dry-run flag (`--dry-run`, `--check`, print-only mode)
2. Run against a copy or staging environment
3. Backup + **verify the restore** before touching the original
4. Feature flag / canary subset — limit exposure to a revocable slice
5. Human checkpoint immediately before the step

A checkpoint alone converts nothing — it only guarantees a witness. It belongs at the end of the ladder, on top of a real conversion, not instead of one.
