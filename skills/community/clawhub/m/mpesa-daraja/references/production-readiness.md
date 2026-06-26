# Production Readiness

Use this reference for launch reviews, client handoff, production-access preparation, or audits of a Daraja integration.

## Hard Gates

- Fresh user approval is required before calling production endpoints or triggering payment prompts, payouts, reversals, or customer-facing payment activity.
- Real sensitive Daraja values must live in protected deployment settings, not in repository files.
- Callback URLs must be public HTTPS endpoints owned by the deployment.
- Fulfillment must be idempotent and coupled to confirmed payment state transitions.
- Operators need a manual reconciliation path before production traffic.

## Security

- Mask phone numbers, sensitive Daraja values, receipt numbers, and raw callback payloads in logs.
- Protect callback endpoints with rate limits, request size limits, and structured payload validation.
- Keep raw callback persistence access-controlled and retention-limited.
- Separate sandbox and production settings.
- Add a deny-by-default guard so tests cannot accidentally hit production.

## Reliability

- Cache Daraja authorization sessions until shortly before expiry.
- Retry only safe transient failures, such as timeouts, 429, and 5xx, according to a bounded policy.
- Do not blindly retry validation errors or duplicate callbacks.
- Alert on callback failures, stuck prompt_sent payments, repeated Daraja errors, and reconciliation mismatches.
- Store enough correlation data to investigate without storing sensitive raw values in logs.

## Data Model

Recommended uniqueness constraints:

- CheckoutRequestID
- MerchantRequestID
- MpesaReceiptNumber when present
- Internal order/payment intent ID

Recommended audit fields:

- internal payment ID
- Daraja request IDs
- normalized state
- masked phone number
- amount and currency
- callback received timestamp
- reconciliation status
- operator/manual-review notes

## Launch Checklist

- Official Daraja docs checked for current endpoints and fields.
- Sandbox happy path and failure path tested.
- Duplicate callback test passes.
- Timeout/cancellation path tested.
- Production config cannot be enabled in local/test by accident.
- .env.example contains placeholders only.
- Logs reviewed for sensitive-value and personal-data leakage.
- Run scripts/scan_skill_safety.py on skill examples and project fixtures before sharing code.
