# Workflow Recipes

## Table of Contents

- [Task to Endpoint Map](#task-to-endpoint-map)
- [Generate from Prompt or Reference Images](#generate-from-prompt-or-reference-images)
- [Generate from a Preset](#generate-from-a-preset)
- [Generate with Saved Characters](#generate-with-saved-characters)
- [Inspect Balance and History](#inspect-balance-and-history)
- [Recharge with WeChat or Stripe](#recharge-with-wechat-or-stripe)
- [Prefer These Conventions](#prefer-these-conventions)
- [Avoid These Mistakes](#avoid-these-mistakes)

## Task to Endpoint Map

| Task | Recommended sequence |
| --- | --- |
| Discover available presets or styles | `GET /api/catalog` |
| Estimate model cost | `GET /api/model-costs` |
| Resolve a user-provided model name | `GET /api/pricing-config` |
| Improve a vague prompt | `POST /api/enhance-prompt` |
| Generate from text or references | `POST /api/v2/generate-image` |
| Generate from a preset | `GET /api/catalog` -> `POST /api/v2/apply-preset` with source images |
| Create or manage characters | `/api/characters` |
| Generate a scene with saved characters | `/api/characters` -> optional `/api/enhance-prompt` -> `POST /api/v2/generate-for-character` |
| Review recent outputs | `GET /api/history` |
| Check credits | `POST /api/billing/balance` |
| List available recharge plans | `GET /api/v1/recharge/plans` |
| Create a WeChat recharge order | `GET /api/v1/recharge/plans` -> `POST /api/v1/recharge/wechat` |
| Create a Stripe recharge session | `GET /api/v1/recharge/plans` -> `POST /api/v1/recharge/stripe` |

## Generate from Prompt or Reference Images

Use this workflow for free-form generation without preset logic.

1. Decide whether the prompt needs refinement.
2. If needed, call `/api/enhance-prompt` with a `category` and the raw user prompt.
3. Optionally call `/api/model-costs` if the user cares about cost.
4. Call `/api/pricing-config` if the user supplied a model name and you need a valid `modelId`.
5. Call `/api/v2/generate-image`.
6. Return `imageUrl`, `promptUsed`, `model`, `remainingBalance`, and `transactionId`.

Example body:

```json
{
  "prompt": "cinematic portrait in warm sunset light",
  "referenceImageUrls": ["https://example.com/reference.jpg"],
  "resolution": "2K",
  "ratio": "Original",
  "modelId": "seedream45"
}
```

## Generate from a Preset

Use this workflow when the user wants a known template or style.

1. Call `/api/catalog`.
2. Choose a preset from the returned templates or styles.
3. Inspect the preset metadata, usage hints, and whether it is a `template` or `style`.
4. Add at least one `sourceImages` or `sourceImageUrls` entry.
5. Build `variableValues` with the exact placeholder names the preset expects.
6. Optionally call `/api/model-costs` before overriding `modelId`.
7. Call `/api/pricing-config` if the user supplied a model name and you need a valid `modelId`.
8. Call `/api/v2/apply-preset`.

Example body:

```json
{
  "presetId": "65f0c1d2e3f4a5b6c7d8e9f0",
  "sourceImageUrls": ["https://example.com/source.jpg"],
  "variableValues": {
    "Subject": "a traveler in a red coat",
    "Mood": "nostalgic and cinematic"
  },
  "resolution": "2K",
  "ratio": "3:4"
}
```

For template presets, the source images are treated as face-reference photos. For style presets, the first source image is the photo being transformed.

## Generate with Saved Characters

Use this workflow when character consistency matters across scenes.

1. List characters with `GET /api/characters`, or create one with `POST /api/characters`.
2. Collect the `id` values for each character you need.
3. Optionally refine the scene prompt with `/api/enhance-prompt`. When useful, pass simplified character descriptors in the `characters` array.
4. Call `/api/v2/generate-for-character`.
5. Return `imageUrl` and preserve `historyItem` if present.

Example create-character body:

```json
{
  "name": "Aki",
  "photoBase64": "data:image/jpeg;base64,...",
  "description": "Short black hair, silver jacket, calm expression"
}
```

Example generate-for-character body:

```json
{
  "characterIds": ["char_123", "char_456"],
  "prompt": "two friends walking through a neon-lit Tokyo alley at night",
  "resolution": "2K",
  "ratio": "16:9"
}
```

## Inspect Balance and History

Use this workflow before expensive jobs or when reconciling prior results.

1. Call `/api/billing/balance`.
2. If the user asks for prior generations, call `GET /api/history`.
3. When adding or repairing history manually, use `POST /api/history`.
4. When deleting history, prefer stored IDs and delete explicitly.

## Recharge with WeChat or Stripe

Use this workflow when the user needs to top up the project linked to a service key.

1. Call `GET /api/v1/recharge/plans`.
2. Choose the correct `planId` from `data.plans`.
3. If the user wants a WeChat QR code, call `POST /api/v1/recharge/wechat`.
4. If the user wants a Stripe-hosted checkout page, call `POST /api/v1/recharge/stripe`.
5. Return the payment artifact the client actually needs:
   - WeChat: `qrcodeImg`, `codeUrl`, `payUrl`, `orderId`, `unifpayOrderId`
   - Stripe: `checkoutUrl`, `qrcodeImg`, `sessionId`

Example WeChat body:

```json
{
  "planId": "698b7fead4c733c85f2a9c74"
}
```

Example Stripe body:

```json
{
  "planId": "698b7fead4c733c85f2a9c74",
  "successUrl": "https://your-app.com/payment/success",
  "cancelUrl": "https://your-app.com/payment/cancel"
}
```

## Prefer These Conventions

- Prefer `/api/catalog` over older template or style listing endpoints.
- Prefer `modelId` terminology on all v2 endpoints, including `/api/v2/generate-for-character`.
- Prefer remote image URLs for large reference images when they are already hosted.
- Prefer data URLs for local images or when the image must remain private to the current request.
- Prefer preserving the raw JSON response when debugging failed requests.
- Prefer `Authorization: Bearer <serviceKey>` for recharge endpoints, even though query and body fallbacks exist.
- Prefer the billing base URL for recharge calls and let `scripts/tuqu_request.py` choose it automatically.
- Prefer preserving `orderId`, `unifpayOrderId`, `checkoutUrl`, and `sessionId` in any app-level response mapping.

## Avoid These Mistakes

- Do not call `/api/v2/apply-preset` without first discovering a valid `presetId`.
- Do not expect `/api/v2/generate-for-character` or `/api/v2/generate-image` to enhance prompts for you.
- Do not send raw base64 without the `data:image/...;base64,` prefix to image fields that expect data URLs.
- Do not confuse the credential value with the auth mode. Even when the caller reuses the same role-specific service key across endpoints, the server still expects body `userKey`, header `x-api-key`, or bearer `serviceKey` depending on the route.
- Do not drop `transactionId` on successful generations; it is the easiest join key for later support work.
- Do not call `/api/v1/recharge/*` on `https://photo.tuqu.ai`; those endpoints live under `https://billing.tuqu.ai`.
- Do not send `x-api-key` to recharge endpoints.
- Do not confuse `planId` with `stripePriceId`; the client only sends `planId`.
- Do not assume WeChat supports every currency; unsupported ones return `CURRENCY_NOT_SUPPORTED`.
