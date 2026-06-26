# Infini API Notes

Use this file when the user needs exact technical details.

## Language-Aware Documentation

Choose document links based on the user's interaction language.

- Chinese docs base: `https://developer.infini.money/docs/zh`
- English docs base: `https://developer.infini.money/docs/en`
- English overview: `https://developer.infini.money/docs/en/1-overview`

## Base URLs

- Sandbox: `https://openapi-sandbox.infini.money`
- Production: `https://openapi.infini.money`

## API Key Page

- Sandbox key page: `https://business-sandbox.infini.money/developer`

## Authentication

Docs:

- Chinese: `https://developer.infini.money/docs/zh/4-authorization`
- English: `https://developer.infini.money/docs/en/4-authorization`

Required request headers:

- `Date`
- `Authorization`
- `Digest` when the request has a body

Plain-language explanation:

- `Date`: the request time
- `Digest`: the fingerprint of the request body
- `Authorization`: the signed proof that the request was created by your server

Signing method:

- HMAC-SHA256

Clock requirement:

- the request timestamp should stay within about 300 seconds of server time

## Basic Hosted Checkout Flow

Docs:

- Chinese: `https://developer.infini.money/docs/zh/3-checkout-mode`
- English: `https://developer.infini.money/docs/en/3-checkout-mode`
- Chinese API doc: `https://developer.infini.money/docs/zh/6-api-ducumentation`
- English API doc: `https://developer.infini.money/docs/en/6-api-ducumentation`

Core flow:

1. Create order with `POST /v1/acquiring/order`
2. Read the returned `checkout_url`
3. Send the user to that URL
4. Receive webhook events
5. Verify the webhook signature

## Confirmed Create-Order Fields

From the current official create-order example, the confirmed request body fields are:

- `amount`
- `currency`
- `client_reference`
- `description`
- `expires_at`

Do not treat `redirect_url` as a confirmed official field.
Do not treat `notify_url` as a confirmed official field in the create-order request unless the current official docs explicitly show it.

## Environment Variables

When explaining `.env`, keep it simple:

- a `.env` file is a text file for storing private values
- common beginner example:

```env
INF_KEY_ID=your_key_id
INF_SECRET_KEY=your_secret_key
```

- tell the user to place the file in the project root
- tell the user not to commit the real `secret_key`

When showing code, explain where these values are read from before continuing.

## Code Stitching Guidance

When moving from signing code to create-order code:

- tell beginners to keep both parts in the same file first
- explain that the second snippet depends on values from the first snippet
- explicitly point out reused variables such as `body`, `date`, `digest`, and `authorization`

## Common Webhook Events

- `order.processing`
- `order.completed`
- `order.expired`
- `order.late_payment`

## Webhook Verification

Docs:

- Chinese auth doc: `https://developer.infini.money/docs/zh/4-authorization`
- English auth doc: `https://developer.infini.money/docs/en/4-authorization`
- Chinese webhook doc: `https://developer.infini.money/docs/zh/7-webhook`
- English webhook doc: `https://developer.infini.money/docs/en/7-webhook`

Important headers:

- `X-Webhook-Timestamp`
- `X-Webhook-Event-Id`
- `X-Webhook-Signature`

Verification string format:

- `{timestamp}.{event_id}.{payload_body}`

Plain-language verification flow:

1. get the timestamp header
2. get the event id header
3. keep the raw request body unchanged
4. join them with dots
5. sign the result with `secret_key`
6. compare with the received signature header

## Guidance Style For Code

When providing code:

- ask for the user's language first
- match the explanation language to the user's language
- output only `Node.js` or only `Python`, never both in the same step unless the user asks
- prefer short runnable snippets over long framework-specific scaffolding
- explain where the user should place `key_id` and `secret_key` in plain language
- if webhook setup is discussed, explain it separately from the create-order body unless the current official docs explicitly connect them
