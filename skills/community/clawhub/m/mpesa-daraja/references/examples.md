# M-Pesa Daraja Examples

## OpenClaw Usage Examples

Use these as realistic prompts for another OpenClaw/Codex session:

- "Use $mpesa-daraja to add sandbox STK Push checkout to my FastAPI app. Keep all sensitive settings in env vars and add tests for Daraja session setup, authorization value generation, outbound request shape, and callback idempotency."
- "Use $mpesa-daraja to review this M-Pesa callback route. Focus on duplicate callbacks, leaked phone numbers in logs, missing shape validation, and unsafe production endpoint usage."
- "Use $mpesa-daraja to create a Django model and service layer for tracking M-Pesa payments from pending to paid/failed/reversed."
- "Use $mpesa-daraja to draft a client implementation plan for Paybill C2B validation and confirmation callbacks."
- "Use $mpesa-daraja to generate QA test cases for STK Push before we request production access."

## Minimal STK Push Architecture

Recommended components:

- MpesaClient: handles Daraja session setup, STK authorization value generation, and Daraja HTTP requests.
- PaymentService: creates internal payment intent records and calls MpesaClient.
- CallbackController: receives Daraja callbacks, validates payload shape, persists raw event, and invokes reconciliation.
- PaymentRepository: enforces idempotency with unique CheckoutRequestID/MerchantRequestID/TransactionID constraints.
- ReconciliationJob: checks pending/unclear payments using transaction status or internal review queues.

State flow:

    order_created -> payment_pending -> stk_prompt_sent -> paid
                                          |-> failed
                                          |-> cancelled
                                          |-> expired
                                          |-> manual_review
    paid -> reversed

## Environment Variables

Use placeholders in examples:

    MPESA_ENV=sandbox
    MPESA_CONSUMER_KEY=replace-me
    MPESA_PRIVATE_APP_VALUE=replace-me
    MPESA_SHORTCODE=174379
    MPESA_STK_AUTH_VALUE=replace-me
    MPESA_CALLBACK_URL=https://example.test/api/mpesa/stk-callback
    MPESA_INITIATOR_NAME=replace-me
    MPESA_PROTECTED_OPERATOR_VALUE=replace-me

Do not commit real values.

## Python STK Authorization Value Example

    import base64
    from datetime import datetime, timezone


    def daraja_timestamp() -> str:
        return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")


    def stk_authorization_value(shortcode: str, private_value: str, timestamp: str) -> str:
        raw = f"{shortcode}{private_value}{timestamp}".encode("utf-8")
        return base64.b64encode(raw).decode("utf-8")

## STK Push Request Shape

    {
      "BusinessShortCode": "174379",
      "Password": "base64-shortcode-private-value-timestamp",
      "Timestamp": "20260520101630",
      "TransactionType": "CustomerPayBillOnline",
      "Amount": 100,
      "PartyA": "254708374149",
      "PartyB": "174379",
      "PhoneNumber": "254708374149",
      "CallBackURL": "https://example.test/api/mpesa/stk-callback",
      "AccountReference": "ORDER-1001",
      "TransactionDesc": "Order payment"
    }

## Successful Callback Shape

    {
      "Body": {
        "stkCallback": {
          "MerchantRequestID": "29115-34620561-1",
          "CheckoutRequestID": "ws_CO_20052026101630000000",
          "ResultCode": 0,
          "ResultDesc": "The service request is processed successfully.",
          "CallbackMetadata": {
            "Item": [
              { "Name": "Amount", "Value": 100 },
              { "Name": "MpesaReceiptNumber", "Value": "TEK7X12345" },
              { "Name": "TransactionDate", "Value": 20260520101701 },
              { "Name": "PhoneNumber", "Value": 254708374149 }
            ]
          }
        }
      }
    }

## Failed Callback Shape

    {
      "Body": {
        "stkCallback": {
          "MerchantRequestID": "29115-34620561-2",
          "CheckoutRequestID": "ws_CO_20052026102030000000",
          "ResultCode": 1032,
          "ResultDesc": "Request cancelled by user"
        }
      }
    }
