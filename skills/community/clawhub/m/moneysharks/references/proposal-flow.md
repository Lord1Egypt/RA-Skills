# Approval-Gated Proposal Flow

## Goal
Use real Aster market/account data to generate execution-ready proposals without directly submitting live orders.

## Flow
1. Fetch real market data.
2. Fetch real account, positions, and orders.
3. Reconcile current exposure.
4. Compute signal, confluence, leverage, and size.
5. Run risk checks.
6. Build a proposal.
7. Emit `PENDING_APPROVAL`.
8. Wait for operator approval before any external order submission layer is invoked.

## Required fields in proposal
- symbol
- side
- quantity
- entry reference price
- leverage
- stop loss
- take profit
- confidence
- confluence count
- rationale
- current exposure
- available margin
