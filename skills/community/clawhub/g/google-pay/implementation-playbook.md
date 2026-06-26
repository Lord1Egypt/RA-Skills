# Implementation Playbook - Google Pay

Use this file to choose a path and avoid mixing incompatible patterns.

## Path A: Web Checkout

1. Confirm browser and region support for Google Pay.
2. Render Google Pay button only after capability checks pass.
3. Build payment data request with server-trusted totals.
4. Use gateway tokenization for most implementations.
5. Submit payment payload to backend or PSP for authorization.
6. Return deterministic success and failure states to checkout UI.

## Path B: Android Checkout

1. Configure Google Pay API client and merchant context.
2. Build request with exact amount and currency.
3. Handle callback and token forwarding safely.
4. Keep capture and settlement logic in backend or PSP.
5. Show fallback methods when Google Pay is unavailable.

## Path C: PSP-Mediated Integration

1. Confirm PSP supports Google Pay in target country and currency.
2. Align token format expectations between client and PSP API.
3. Enforce idempotency keys for authorization and capture calls.
4. Validate webhook handling for async state transitions.
5. Document rollback strategy for elevated declines or PSP outages.

## Data Integrity Rules

- Currency and amount precision must match backend contracts.
- Checkout session ids must map to order ids one-to-one.
- Retries must preserve idempotency key per logical payment attempt.

## Completion Criteria

- Selected path is explicit.
- Prerequisites are validated.
- Validation checklist is complete for target environment.
- Incident and rollback path is documented.
