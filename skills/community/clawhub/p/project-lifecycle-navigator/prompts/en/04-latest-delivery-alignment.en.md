# Latest Delivery Alignment Review

Use this mode to review one active delivery boundary without repeating a whole-repository audit.

## Inputs

Inspect the current target and acceptance criteria, active task or Work Order, latest handoff, affected source and tests, current diff or commit, verification configuration, and evidence produced for this delivery.

## Review Rules

1. Keep the review read-only.
2. State the exact commit, branch, dirty state, and delivery boundary when available.
3. Compare each completion claim with observable acceptance and evidence.
4. Run or inspect only the regression surface needed to validate the delivery unless a broader risk justifies expansion.
5. Distinguish implemented, partial, verified, unverified, unusable, documentation-conflict, and not-executed.
6. Treat Developer Complete as a handoff state, not Accepted.
7. Preserve the current target; route target changes to Owner-led rebaseline.

## Output

- Delivery reviewed
- Current target and acceptance slice
- Evidence inspected or executed, including final exits
- Claim-by-claim alignment table
- Regressions or user-visible gaps
- Documentation or governance conflicts
- Decision: Ready for Independent Acceptance, Needs Fix, Blocked, or Cannot Confirm
- Bounded next action and required Owner decisions

Do not sign final QA acceptance in this mode.
