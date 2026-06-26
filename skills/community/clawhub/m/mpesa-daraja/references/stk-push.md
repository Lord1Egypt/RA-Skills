# STK Push / Lipa na M-Pesa Online

Use this reference when implementing, reviewing, or testing customer-initiated checkout through Daraja STK Push.

## Official Source Check

Before implementation or publishing skill updates, verify the current endpoint names, field names, result codes, and sandbox behavior against official Safaricom Daraja documentation:

- Daraja portal: https://developer.safaricom.co.ke/
- STK Push / Lipa na M-Pesa Online docs in the Daraja portal
- Safaricom developer release notes, notices, or portal announcements when available

Do not copy sensitive Daraja values, real phone numbers, receipt numbers, or production callback payloads from docs, dashboards, logs, or client systems into generated code.

## Implementation Shape

Prefer these boundaries:

- MpesaClient: Daraja session setup, STK authorization value, outbound request, response mapping.
- PaymentIntent or Payment: internal state and idempotency keys.
- PaymentService: creates intent, validates amount/order state, calls MpesaClient.
- CallbackRoute: validates callback shape, stores raw event safely, returns fast.
- ReconciliationJob: checks stale or ambiguous payments.

Keep HTTP calls injectable so tests can mock Daraja without touching external endpoints.

## Request Rules

- Generate timestamp as YYYYMMDDHHmmss.
- Generate the STK authorization value using Safaricom's current shortcode/private-value/timestamp formula.
- Use CustomerPayBillOnline for PayBill flows unless the product intentionally supports a different Daraja-supported transaction type.
- Normalize phone numbers only through a deliberate, tested formatter. Reject ambiguous or non-Kenyan MSISDN input.
- Require HTTPS callback URLs outside local tests.
- Treat MerchantRequestID and CheckoutRequestID as correlation identifiers, not proof of payment.

## Callback Rules

- Return HTTP 200 quickly after durable persistence.
- Deduplicate by CheckoutRequestID; also store MerchantRequestID and receipt number when present.
- Successful callbacks must not double-credit on retries.
- Failed callbacks may omit CallbackMetadata; do not assume it exists.
- Mask PhoneNumber and all sensitive Daraja values in logs.
- Map known ResultCodes into explicit internal states, but preserve unknown codes for manual review.

## State Mapping

Recommended internal states:

- pending: internal payment intent exists.
- prompt_sent: Daraja accepted the STK request.
- paid: successful callback with receipt metadata.
- failed: clear unsuccessful callback.
- cancelled: user cancellation, commonly ResultCode 1032.
- expired: timeout or no response after the product-defined window.
- manual_review: ambiguous response, unknown result, duplicate conflict, or reconciliation mismatch.
- reversed: confirmed reversal after operator-approved or compliant reversal flow.

## Review Checklist

- Sensitive settings are environment-backed and never committed.
- Production endpoint usage requires explicit opt-in.
- Daraja session caching respects expiry and handles 401 with one safe refresh retry.
- Checkout creation and callback processing are transactionally safe.
- Callback handler has shape validation, idempotency, masked logging, and durable event storage.
- Tests cover success, cancellation, timeout, duplicate callback, malformed callback, and Daraja outage.
