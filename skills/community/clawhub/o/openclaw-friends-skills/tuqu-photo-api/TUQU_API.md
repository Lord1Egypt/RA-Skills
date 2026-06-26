# Tuqu API Notes

This file holds the API-specific guidance that used to live in `SKILL.md`. The main skill now
drives supported tasks through `scripts/tuqu_request.py`; use this file when you need the host,
auth, endpoint, payload, or failure semantics behind those helper commands.

For exact field-level request and response schemas, read
[references/endpoints.md](./references/endpoints.md). For task-oriented API flows, read
[references/workflows.md](./references/workflows.md).

## Hosts and Auth

`https://photo.tuqu.ai` serves photo, catalog, prompt, character, history, pricing, and balance
workloads. `https://billing.tuqu.ai` serves recharge flows.

`serviceKey` and `userKey` refer to the same credential value. The difference is where the server
expects to receive it:

| Paths | Host | Auth |
| --- | --- | --- |
| `/api/v2/generate-image` | photo | body `userKey` |
| `/api/v2/apply-preset` | photo | body `userKey` |
| `/api/v2/generate-for-character` | photo | body `userKey` |
| `/api/billing/balance` | photo | body `userKey` |
| `/api/characters` | photo | header `x-api-key` |
| `/api/history` | photo | header `x-api-key` |
| `/api/enhance-prompt` | photo | none |
| `/api/catalog` | photo | none |
| `/api/model-costs` | photo | none |
| `/api/pricing-config` | photo | none |
| `/api/v1/recharge/plans` | billing | `Authorization: Bearer <serviceKey>` |
| `/api/v1/recharge/wechat` | billing | `Authorization: Bearer <serviceKey>` |
| `/api/v1/recharge/stripe` | billing | `Authorization: Bearer <serviceKey>` |

The helper maps `--service-key` into the correct auth mode automatically for the supported paths.

## Capability Map

Use these API families for each task:

1. Discover presets, styles, and template variables: `/api/catalog`
2. Improve a vague prompt: `/api/enhance-prompt`
3. Generate directly from text or reference images: `/api/v2/generate-image`
4. Apply a known template or style preset: `/api/v2/apply-preset`
5. Create, update, list, or delete persistent characters: `/api/characters`
6. Generate scenes with saved characters: `/api/v2/generate-for-character`
7. Review or maintain prior outputs: `/api/history`
8. Check remaining balance: `/api/billing/balance`
9. Inspect pricing data or resolve a model name: `/api/model-costs`, `/api/pricing-config`
10. Top up a project balance: `/api/v1/recharge/plans`, `/api/v1/recharge/wechat`, `/api/v1/recharge/stripe`

## Request Rules

- Send JSON with `Content-Type: application/json`.
- Send image data as full data URLs such as `data:image/jpeg;base64,...`.
- Treat `/api/catalog` as the source of truth for `presetId`, preset type, and variable names.
- For `/api/v2/apply-preset`, send at least one `sourceImages` or `sourceImageUrls` entry.
- For `/api/v2/generate-image`, provide at least one of `prompt`, `referenceImages`, or
  `referenceImageUrls`.
- Use `/api/model-costs` before overriding `modelId` on cost-sensitive jobs.
- Use `/api/pricing-config` before accepting a user-supplied model name. Normalize candidate names
  by lowercasing and stripping non-alphanumeric characters before comparing.
- Use `ratio: "Original"` only when at least one reference image is present, because the server
  measures the first reference image.
- Preserve important output fields when the API returns them:
  `imageUrl`, `promptUsed`, `model`, `remainingBalance`, `transactionId`, `historyItem`,
  `orderId`, `unifpayOrderId`, `checkoutUrl`, `sessionId`, `qrcodeImg`, `codeUrl`, and `payUrl`.

## Common Flow Semantics

### Generate from prompt or references

1. Optionally enhance the prompt with `/api/enhance-prompt`.
2. Optionally inspect `/api/model-costs` or `/api/pricing-config`.
3. Call `/api/v2/generate-image`.

### Generate from a preset

1. Call `/api/catalog`.
2. Choose a valid `presetId`.
3. Confirm whether the preset is a `template` or a `style`.
4. Supply at least one source image.
5. Fill `variableValues` with only the placeholders defined by the preset.
6. Call `/api/v2/apply-preset`.

### Generate with saved characters

1. Use `/api/characters` to create or look up characters.
2. Optionally refine the scene prompt with `/api/enhance-prompt`.
3. Call `/api/v2/generate-for-character`.

### Inspect history and balance

1. Call `/api/billing/balance` before expensive jobs when the user asks about credits.
2. Call `/api/history` when the user needs recent generations or audit data.

### Recharge

1. Call `/api/v1/recharge/plans` to list valid `planId` values.
2. Use `/api/v1/recharge/wechat` for QR-based payment.
3. Use `/api/v1/recharge/stripe` for hosted checkout.

## Failure Recovery

- `INSUFFICIENT_BALANCE`: stop and report the remaining balance if the response includes it.
- `INVALID_REQUEST`: compare the payload against the endpoint schema and call out the missing or
  malformed field explicitly.
- `NOT_FOUND` on `/api/v2/apply-preset`: refresh `/api/catalog`; the `presetId` is wrong or no
  longer active.
- `UNAUTHORIZED`: verify both the host and the auth mode expected by the route.
- Recharge `UNAUTHORIZED`: verify the service key is still active and is being sent to the billing
  host.
- `PAYMENT_NOT_CONFIGURED`: report which payment channel is missing at the project or global config
  layer.
- `CURRENCY_NOT_SUPPORTED`: explain that WeChat only supports direct `CNY` or `JPY`, plus `USD`
  through project FX conversion.
- `GENERATION_FAILED`: surface whether the response says the request was refunded.
