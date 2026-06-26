# Infini Troubleshooting

Use this file first when the user reports an error.

## Language-Aware Documentation

Choose the troubleshooting links in the same language as the user whenever possible.

## Official Links

- Chinese error code doc: `https://developer.infini.money/docs/zh/8-errorcodes`
- English error code doc: `https://developer.infini.money/docs/en/8-errorcodes`
- Chinese authentication doc: `https://developer.infini.money/docs/zh/4-authorization`
- English authentication doc: `https://developer.infini.money/docs/en/4-authorization`
- Chinese API doc: `https://developer.infini.money/docs/zh/6-api-ducumentation`
- English API doc: `https://developer.infini.money/docs/en/6-api-ducumentation`
- Chinese webhook doc: `https://developer.infini.money/docs/zh/7-webhook`
- English webhook doc: `https://developer.infini.money/docs/en/7-webhook`

## How To Diagnose

1. Identify the current step.
2. Check whether the issue matches one of the known cases below.
3. Give the known fix first if there is a match.
4. Only ask for extra details if the known cases do not solve it.

## Known Cases

### 40001 Invalid parameter

Meaning in simple words:

- one or more request fields are missing, empty, or formatted incorrectly

Check:

- required body fields are present
- amount and currency values are valid
- the request body matches the API example

### 40002 Invalid signature

Meaning in simple words:

- the server could not verify the signature

Check:

- `Date` header is present
- `Date` value is close to the current server time
- `Authorization` header format is correct
- `Digest` exists when the request has a body
- `secret_key` is correct
- the signed content matches the real request exactly
- the path in the signing string really matches `/v1/acquiring/order`

### 401 Unauthorized

Meaning in simple words:

- the API key is wrong, missing, disabled, or being used in the wrong environment

Check:

- sandbox keys are used with sandbox base URL
- production keys are used with production base URL
- `key_id` and `secret_key` were copied correctly

### 40901 Order not found

Meaning in simple words:

- the order ID does not exist in the current environment

Check:

- order ID is correct
- sandbox order is being queried in sandbox, not production

### 40902 Order status error

Meaning in simple words:

- the current order state does not allow the action being attempted

Check:

- whether the order is already completed, expired, or still processing

### 40906 Duplicate or repeated request case

Meaning in simple words:

- the same request may have been sent again with conflicting data

Check:

- whether the same merchant order number is being reused
- whether retries send the exact same payload

## Webhook-Specific Checks

If the webhook does not work:

- first test with `https://webhook.cool`
- confirm the webhook URL is publicly reachable
- confirm the callback handler reads the raw request body if signature verification depends on it
- confirm `X-Webhook-Timestamp`, `X-Webhook-Event-Id`, and `X-Webhook-Signature` are read correctly
- confirm the verification string uses `{timestamp}.{event_id}.{payload_body}`
- confirm the server clock is correct

## Sandbox Test Checks

If sandbox order creation works but the full flow does not:

- confirm the returned `checkout_url` opens correctly
- confirm the user completed the test payment, not just opened the page
- confirm the user has test tokens in the sandbox flow
- confirm the payment was actually completed in sandbox
- confirm your webhook endpoint received the callback
- confirm your backend updated the order after receiving a valid webhook
