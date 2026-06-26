---
name: mpesa-daraja
description: Advisory reference for Safaricom M-Pesa Daraja integration planning, reviews, sandbox testing, callbacks, reconciliation, and production-readiness. It provides implementation guidance only and does not require external account access to use.
version: 1.2.2
---

# M-Pesa Daraja

This is an advisory/reference skill. It does not call Safaricom APIs, initiate payments, or require external account access to install or use.

## Operating Rules

- Treat this as payment-integration guidance, not permission to move money.
- Default to Daraja sandbox endpoints and placeholder configuration unless the user explicitly asks for production guidance.
- Never store sensitive Daraja values, callback payloads with phone numbers, or transaction IDs in committed files.
- Ask before calling any live/production endpoint or sending any request that could trigger a payment prompt, payout, reversal, or customer-facing callback.
- Prefer environment variables and protected deployment settings over \`.env\` files in shared repos. If \`.env.example\` is needed, use placeholder values only.
- Make callbacks idempotent: verify request shape, persist raw event safely, deduplicate by CheckoutRequestID/ConversationID/TransactionID, then process business state transitions.

## Workflow

1. Identify the payment flow:
   - **STK Push / Lipa na M-Pesa Online** for customer-initiated checkout.
   - **C2B** for paybill/till customer payments with validation and confirmation callbacks.
   - **B2C** for business payouts to customers or agents.
   - **Transaction Status / Reversal** for reconciliation and recovery.
2. Confirm runtime context: language/framework, sandbox vs production, callback URL availability, persistence layer, and compliance constraints.
3. Design the integration around these boundaries:
   - Daraja session setup and caching
   - request authorization value generation
   - outbound Daraja client
   - callback receiver
   - idempotency/reconciliation
   - observability without leaking personal or payment data
4. Use \`references/examples.md\` when the user asks for sample OpenClaw prompts, implementation examples, or architecture snippets.
5. Use \`references/test-cases.md\` when the user asks for QA scenarios, unit tests, integration tests, sandbox tests, or production-readiness checks.
6. Use \`references/stk-push.md\` for STK Push/Lipa na M-Pesa Online implementation details.
7. Use \`references/api-endpoints.md\` when the user needs current Daraja endpoint names, versions, or flow coverage.
8. Use \`references/production-readiness.md\` before production-readiness reviews, client handoff, or launch checklists.
9. Use \`references/maintenance.md\` before updating or publishing this skill. Always check official Safaricom/Daraja sources for API changes, update the version, and run validation before pushing to ClawHub.

## Implementation Guidance

- Keep Daraja client code small and injectable so app tests can mock HTTP calls.
- Follow Safaricom's current STK authorization formula with timestamp format \`YYYYMMDDHHmmss\`.
- Cache Daraja authorization sessions until shortly before expiry.
- Expose public HTTPS callback URLs in sandbox using a stable tunnel or deployed test environment; avoid local-only callback URLs.
- Return fast from callbacks after durable persistence; do heavier fulfillment asynchronously when possible.
- Log correlation IDs, response codes, and internal order IDs. Mask phone numbers, names, and all sensitive Daraja values.
- Model payment state explicitly, for example: \`pending\`, \`prompt_sent\`, \`paid\`, \`failed\`, \`cancelled\`, \`expired\`, \`reversed\`, \`manual_review\`.

## Common OpenClaw Requests

- "Use $mpesa-daraja to add STK Push checkout to this Django app."
- "Use $mpesa-daraja to write sandbox test cases for our M-Pesa checkout."
- "Use $mpesa-daraja to review this Daraja callback handler for idempotency and sensitive-data leakage."
- "Use $mpesa-daraja to create an OpenClaw automation that drafts M-Pesa reconciliation reports without touching production APIs."

## Deliverables To Prefer

- For implementation: client module, callback route, typed request/response models, masked logging, tests, and \`.env.example\`.
- For review: findings ordered by payment risk, security risk, idempotency/reconciliation risk, then code quality.
- For planning: flow diagram in text, endpoint list, configuration list, callback contract, test plan, and production checklist.
- For troubleshooting: exact failing step, expected Daraja response, likely causes, and the smallest safe verification step.
