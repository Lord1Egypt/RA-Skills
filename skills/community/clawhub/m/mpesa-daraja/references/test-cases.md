# M-Pesa Daraja Test Cases

## Unit Tests

- Daraja session client builds the correct authorization header from placeholder app settings.
- Daraja session client never logs sensitive app values or session strings.
- STK authorization value generation follows Safaricom's current shortcode/private-value/timestamp formula.
- Timestamp uses Daraja format YYYYMMDDHHmmss and is generated in a consistent timezone.
- STK request rejects non-positive amount values.
- STK request rejects invalid MSISDN format; normalize local 07xx numbers to 2547xx only when the product explicitly allows it.
- STK request uses PartyB equal to the configured shortcode.
- STK request requires an HTTPS callback URL outside local unit tests.
- Daraja client maps network timeout to retryable internal error.
- Daraja client maps Daraja ResponseCode/ResultCode into explicit internal states.
- Callback parser extracts Amount, MpesaReceiptNumber, TransactionDate, and PhoneNumber from CallbackMetadata when ResultCode is 0.
- Callback parser handles failed callbacks that do not include CallbackMetadata.
- Callback parser rejects payloads missing Body.stkCallback.
- Callback handler masks phone numbers in logs.
- Callback handler is idempotent for duplicate CheckoutRequestID.

## Integration Tests With HTTP Mocking

- Daraja session endpoint returns a session string and expiry; client caches it and reuses it before expiry.
- Daraja session refresh happens when cached session data is near expiry.
- STK Push request sends the expected Authorization header.
- STK Push request includes BusinessShortCode, Password, Timestamp, TransactionType, Amount, PartyA, PartyB, PhoneNumber, CallBackURL, AccountReference, and TransactionDesc.
- Daraja 401 causes one session refresh and one retry, then fails cleanly if still unauthorized.
- Daraja 429 or 5xx is retried according to the app's retry policy.
- Daraja validation error is not retried.
- Callback route persists raw callback once and returns HTTP 200 quickly.
- Duplicate successful callback does not double-credit an order.
- Failed callback changes payment state to failed/cancelled/expired according to ResultCode mapping.

## Sandbox End-to-End Tests

- Start checkout for a sandbox order and verify a MerchantRequestID and CheckoutRequestID are stored.
- Simulate a successful callback and verify order/payment state becomes paid.
- Simulate user cancellation ResultCode 1032 and verify state becomes cancelled.
- Simulate timeout/expiry and verify state becomes expired or manual_review.
- Verify reconciliation job can find stale prompt_sent payments.
- Verify public callback URL is reachable over HTTPS from outside the local machine.
- Verify logs contain internal order IDs and Daraja request IDs but no sensitive Daraja values or full phone number.

## Production Readiness Checks

- Production base URL is gated by explicit environment configuration and cannot be enabled accidentally in tests.
- All real sensitive values are loaded from protected deployment settings, not committed files.
- Callback endpoint has rate limiting or upstream protection appropriate for the deployment.
- Database has uniqueness constraints for CheckoutRequestID, MerchantRequestID, and MpesaReceiptNumber where applicable.
- Payment fulfillment is idempotent and transactionally coupled to payment-state changes.
- Reversal and refund processes require explicit operator approval unless the user has built a compliant automated workflow.
- Monitoring alerts on repeated Daraja failures, callback failures, and stuck pending payments.
- Manual reconciliation path exists for ambiguous states.

## Example Pytest Names

- test_stk_authorization_value_uses_shortcode_private_value_timestamp
- test_stk_request_requires_https_callback_url
- test_daraja_client_masks_sensitive_values_in_logs
- test_success_callback_extracts_receipt_and_amount
- test_failed_callback_without_metadata_is_handled
- test_duplicate_callback_does_not_double_credit_order
- test_unauthorized_response_refreshes_session_once
- test_production_endpoint_requires_explicit_opt_in
