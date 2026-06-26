# Approval Execution Layer

This layer applies only in `approval` mode (or `live` with `require_human_approval_for_live_orders=true`).

In `autonomous_live` mode, this entire layer is bypassed — orders go directly to `scripts/live_execution_adapter.py`.

## Flow (approval / live with approval)

1. Generate decision.
2. Run confluence, leverage, sizing, and risk checks.
3. Build an order proposal.
4. Present proposal to user and require explicit approval.
5. Only after approval: hand off to the live execution adapter.
6. Journal before and after approval.

## Rules

- Do not submit live orders without approval when approval is required.
- Mask credentials in all output.
- Treat the adapter as a gate, not as the exchange client.
- Keep journaling before and after approval.

## In `autonomous_live` mode

- This layer is **not used**.
- The agent proceeds directly from risk checks → `scripts/live_execution_adapter.py` → journal.
- No proposal is generated. No user confirmation is requested.
- This is intentional: the user gave blanket consent at onboarding.

## Suggested approval payload (when approval mode is active)

- symbol
- side
- quantity
- leverage
- stop loss
- take profit
- rationale
- confidence
- confluence count
