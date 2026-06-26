# Recurring Payments - Google Pay

Use this file when checkout includes recurring billing or renewals.

## Scope Clarification

Google Pay improves initial payment entry, but recurring charges depend on backend and PSP contracts that differ from one-time checkout.

## Required Decisions

- Is Google Pay used for initial payment method capture only?
- Which PSP handles recurring billing lifecycle events?
- What is the renewal failure and dunning strategy?

## Recurring Flow Basics

1. Capture initial payment method through Google Pay flow.
2. Store reusable payment method reference via PSP.
3. Run renewals from backend scheduler or billing engine.
4. Reconcile renewals through webhook events.

## Validation Checklist

- Initial Google Pay checkout and first invoice succeed.
- Renewal charge succeeds without user interaction when expected.
- Failed renewal moves to retry and notification flow correctly.
- Cancel and reactivation behavior matches product policy.

## Common Pitfalls

- Assuming one-time payload behavior matches recurring contracts.
- Missing renewal reconciliation, causing false active state.
- Not testing expired funding source and payment method updates.
