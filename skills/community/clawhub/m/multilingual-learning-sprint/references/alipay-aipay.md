# Alipay AI Pay Integration Notes

Use this reference only when the user asks to monetize the learning sprint, connect Alipay AI Pay, connect JD ClawTip A2A payment, build a paid API, or prepare launch materials.

## Current Platform Boundary

Official Alipay AI Pay public pages describe AI pay-per-use around HTTP payment negotiation. The overview lists payable AI objects such as AI skills, MCP services, and APIs, but the service registration page currently exposes Restful and callback service types and says Skill service type will be expanded later.

Sources:

- Official overview: https://aipay.alipay.com/docs/overview.html
- Official call-pay flow: https://aipay.alipay.com/callpay
- Official npm package: `@alipay/alipay-aipay@1.3.1`

Therefore:

- A ClawHub instruction-only Skill cannot itself enforce Alipay payment.
- For paid launch today, wrap the learning service as a Restful API and register that service with Alipay AI Pay.
- Keep the ClawHub skill as discovery, onboarding, and usage workflow, or make it call the paid API only after payment validation exists.

## Official Tooling

Install the official Alipay AI Pay Skill/tooling when doing a real integration:

```bash
npx -y @alipay/alipay-aipay@latest install
```

The package includes integration flows, onboarding flows, sandbox helpers, and code examples for pay-per-use.

## Restful Paid Wrapper Shape

Recommended paid resource endpoints:

| Endpoint | Purpose |
|---|---|
| `POST /v1/language-sprint/placement` | Paid placement report and plan |
| `POST /v1/language-sprint/lesson` | Paid daily lesson generation |
| `POST /v1/language-sprint/quiz` | Paid review quiz and score |
| `GET /v1/language-sprint/resource/:id` | Fetch paid generated resource |

The endpoint should:

1. Check whether the request includes a valid `Payment-Proof` header.
2. If missing, create a local order, sign a payment request, return HTTP 402, and set `Payment-Needed`.
3. If present, parse `Payment-Proof`, call `alipay.aipay.agent.payment.verify`, and confirm the proof is active.
4. Verify local order, amount, resource id, and idempotency before generating or releasing the resource.
5. Generate the lesson, quiz, or plan.
6. Call `alipay.aipay.agent.fulfillment.confirm`.
7. Return the resource and set `Payment-Validation`.

## JD ClawTip / A2A Path

JD ClawTip public CLI behavior checked on 2026-07-21 with `@clawtip/clawtip-cli@1.0.4` and the official developer guide supplied by JD ClawTip.

Production backend:

```text
https://language-sprint-clawtip.pages.dev
```

This Cloudflare Worker creates ClawTip orders, stores them in Workers KV, keeps `CLAWTIP_PAY_TO` and `CLAWTIP_SM4_KEY` as Cloudflare Secrets, and releases the language resource only after decrypting a `payCredential` with `payStatus=SUCCESS`.

Core commands:

```bash
clawtip create-token --token <user_token>
clawtip check-register
clawtip pay --order-no <orderNo> --indicator <indicator> --skill-version 1.0.4
```

`indicator` is not shown on the ClawTip wallet page. It is computed from the skill slug:

```text
slug: multilingual-learning-sprint
indicator: md5(slug) = 223739d6eb9b80249e86507fbb1827fb
skill-id: multilingual-learning-sprint
```

The payer-side CLI expects order files under:

```text
Windows: %USERPROFILE%\openclaw\skills\orders\<indicator>\<orderNo>.json
macOS/Linux: ~/.openclaw/skills/orders/<indicator>/<orderNo>.json
```

Order JSON fields observed from the official CLI:

```json
{
  "skill-id": "multilingual-learning-sprint",
  "order_no": "LS_PLACEMENT_DEMO",
  "amount": 50,
  "pay_to": "merchant_or_wallet_pay_to",
  "question": "Paid language placement test and sprint plan",
  "description": "Generate a CEFR-style diagnostic and 7/14/30-day language sprint plan.",
  "slug": "multilingual-learning-sprint",
  "resource_url": "https://example.com/api/language-sprint/placement",
  "encrypted_data": "SM4_ECB_PKCS5PADDING_BASE64",
  "skillId": "multilingual-learning-sprint",
  "orderNo": "LS_PLACEMENT_DEMO",
  "payTo": "merchant_or_wallet_pay_to",
  "encryptedData": "SM4_ECB_PKCS5PADDING_BASE64",
  "resourceUrl": "https://example.com/api/language-sprint/placement"
}
```

The official developer guide requires `encrypted_data` to be an SM4-encrypted JSON string containing `orderNo`, `amount` in fen, and `payTo`, encrypted with the SM4 key paired to that `payTo`.

For local OpenClaw/Codex delivery, use `CLAWTIP_PAYMENT_VERIFY_MODE=order-file`: the server writes the order file before returning 402, `clawtip pay` writes `payCredential` back to that file after payment, and the follow-up API request must pass `X-Language-Sprint-Order-No` plus `X-ClawTip-Pay-Credential`.

Do not claim hosted live ClawTip collection is complete until a real `pay_to`, matching `CLAWTIP_SM4_KEY`, user token registration, and either order-file or merchant-endpoint payment credential verification are configured.

Key protocol pieces from the official Node pay-per-use example:

- Request header from the client or agent: `Payment-Proof`.
- Response header when payment is required: `Payment-Needed`.
- Response header after successful validation and fulfillment: `Payment-Validation`.
- Payment verification API: `alipay.aipay.agent.payment.verify`.
- Fulfillment confirmation API: `alipay.aipay.agent.fulfillment.confirm`.

## Payment-Needed Payload Fields

The official example encodes a JSON object with a `protocol` section and a `method` section as base64url.

Typical `protocol` fields:

```json
{
  "out_trade_no": "ORDER_...",
  "amount": "0.01",
  "currency": "CNY",
  "resource_id": "/v1/language-sprint/lesson",
  "pay_before": "2026-07-20T18:30:00+08:00",
  "seller_signature": "...",
  "seller_sign_type": "RSA2",
  "seller_unique_id": "2088..."
}
```

Typical `method` fields:

```json
{
  "seller_name": "merchant name",
  "seller_id": "2088...",
  "seller_app_id": "2021...",
  "goods_name": "Multilingual Learning Sprint daily lesson",
  "seller_unique_id_key": "seller_id",
  "service_id": "real_service_id"
}
```

Use a real `service_id` in production. The official sandbox demo uses `api_mock_service_id` only for sandbox debugging.

## Launch Checklist

- Alipay merchant account is available and authorized.
- Product signing for AI pay-per-use is complete.
- Open platform app exists and keys are configured.
- Restful service is registered with name, description, pricing, endpoint, and service id.
- Endpoint is reachable over HTTPS.
- Database stores orders, resource ids, payment state, and fulfillment state.
- Payment verification checks amount, currency, `out_trade_no`, `trade_no`, active status, and resource id.
- Fulfillment confirmation is sent before returning successful delivery.
- Logs redact private keys, bearer tokens, `Payment-Proof`, and full signatures.
- Refund, support, and abuse controls are documented.

## Suggested Product Copy

Service name: Multilingual Learning Sprint API

Goods names:

- Language placement test and sprint plan
- Personalized daily language lesson
- Spaced review quiz and progress report

Pricing suggestion for early testing:

- Placement and plan: CNY 0.99 to 2.99 per report
- Daily lesson: CNY 0.19 to 0.99 per generated lesson
- Quiz and progress report: CNY 0.09 to 0.49 per run

Actual pricing should be adjusted for model cost, payment fee, refund policy, and target market.
