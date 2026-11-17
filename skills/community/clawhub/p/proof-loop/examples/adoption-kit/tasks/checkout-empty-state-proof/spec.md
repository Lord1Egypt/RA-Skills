# Task: checkout-empty-state-proof

## Task Statement

Fix a checkout empty state so returning customers get a useful recovery action while new empty carts keep the existing continue-shopping path.

## Acceptance Criteria

**AC1:** Returning empty-cart customers see the saved-cart recovery action.
- Verify: inspect the recorded browser check in `raw/returning-empty-cart.txt`.

**AC2:** Brand-new empty carts still show the continue-shopping action.
- Verify: inspect the recorded browser check in `raw/new-empty-cart.txt`.

**AC3:** Existing checkout regression checks remain green.
- Verify: inspect the recorded regression command in `raw/checkout-regression.txt`.

## Constraints

- Do not change payment, totals, or cart persistence logic.
- Do not broaden this task into checkout redesign.

## Non-Goals

- No new checkout analytics.
- No new recommendation engine.
- No visual redesign beyond the empty-state copy and action choice.

## Verification Approach

A fresh verifier reads the evidence logs, confirms each AC has direct proof, and runs `bin/proof-loop check` against this task folder.
