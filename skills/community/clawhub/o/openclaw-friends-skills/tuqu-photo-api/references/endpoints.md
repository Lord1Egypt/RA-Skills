# Endpoint Reference

## Table of Contents

- [Base URLs](#base-urls)
- [Auth Matrix](#auth-matrix)
- [Shared Response and Error Shapes](#shared-response-and-error-shapes)
- [`/api/v2/generate-image`](#apiv2generate-image)
- [`/api/v2/apply-preset`](#apiv2apply-preset)
- [`/api/v2/generate-for-character`](#apiv2generate-for-character)
- [`/api/enhance-prompt`](#apienhance-prompt)
- [`/api/catalog`](#apicatalog)
- [`/api/model-costs`](#apimodel-costs)
- [`/api/pricing-config`](#apipricing-config)
- [`/api/characters`](#apicharacters)
- [`/api/history`](#apihistory)
- [`/api/billing/balance`](#apibillingbalance)
- [`/api/v1/recharge/plans`](#apiv1rechargeplans)
- [`/api/v1/recharge/wechat`](#apiv1rechargewechat)
- [`/api/v1/recharge/stripe`](#apiv1rechargestripe)

## Base URLs

| API family | Base URL |
| --- | --- |
| Photo, catalog, history, and balance | `https://photo.tuqu.ai` |
| Recharge and hosted payment flows | `https://billing.tuqu.ai` |

`serviceKey` and `userKey` are the same credential. Recharge endpoints prefer `Authorization: Bearer <serviceKey>`.

## Auth Matrix

| Endpoint | Method | Auth | Notes |
| --- | --- | --- | --- |
| `/api/v2/generate-image` | `POST` | body `userKey` | At least one of `prompt`, `referenceImages`, or `referenceImageUrls` is required |
| `/api/v2/apply-preset` | `POST` | body `userKey` | Requires `presetId` from `/api/catalog` and at least one source image |
| `/api/v2/generate-for-character` | `POST` | body `userKey` | No automatic prompt enhancement; returns `404` before billing when characters are missing |
| `/api/enhance-prompt` | `POST` | none | Returns text only |
| `/api/catalog` | `GET` | none | Public preset and usage discovery |
| `/api/model-costs` | `GET` | none | Public model pricing map |
| `/api/pricing-config` | `GET` | none | Public model and resolution coefficients for resolving `modelId` values |
| `/api/characters` | `GET/POST/PUT/DELETE` | `x-api-key` header or `Authorization: Bearer` | Persistent character store |
| `/api/history` | `GET/POST/DELETE` | `x-api-key` header or `Authorization: Bearer` | Recent generations and manual history entries |
| `/api/billing/balance` | `POST` | body `userKey` | Returns remaining token balance |
| `/api/v1/recharge/plans` | `GET` | `Authorization: Bearer <serviceKey>` or `serviceKey` query | Hosted on the billing base URL |
| `/api/v1/recharge/wechat` | `POST` | `Authorization: Bearer <serviceKey>` or body `serviceKey` | Hosted on the billing base URL |
| `/api/v1/recharge/stripe` | `POST` | `Authorization: Bearer <serviceKey>` or body `serviceKey` | Hosted on the billing base URL |

## Shared Response and Error Shapes

Common API errors:

- `INVALID_REQUEST`: Missing or invalid parameters
- `UNAUTHORIZED`: Missing or invalid credential
- `NOT_FOUND`: Missing resource such as a preset or history item
- `INSUFFICIENT_BALANCE`: Not enough tokens for the operation
- `GENERATION_FAILED`: Generation failed and may include refund information
- `PAYMENT_NOT_CONFIGURED`: Project or global payment config is missing for the requested channel
- `CURRENCY_NOT_SUPPORTED`: Recharge plan currency cannot be processed by the selected payment channel
- `INTERNAL_ERROR`: Unexpected server error

Photo and catalog success responses usually follow this pattern:

```json
{
  "success": true,
  "data": {
    "...": "endpoint-specific fields"
  }
}
```

Photo and catalog error responses usually follow this pattern:

```json
{
  "success": false,
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Human-readable explanation"
  }
}
```

Recharge endpoints use the same success wrapper but return top-level `code` and `message` on failure:

```json
{
  "success": false,
  "code": "UNAUTHORIZED",
  "message": "Invalid or inactive service key"
}
```

## `/api/v2/generate-image`

- Method: `POST`
- Auth: body `userKey`
- Purpose: direct image generation from text, reference images, or both

Request body:

```json
{
  "userKey": "required",
  "prompt": "optional when reference images are provided",
  "referenceImages": ["optional data URL base64 images"],
  "referenceImageUrls": ["optional remote image URLs"],
  "resolution": "optional: 1K | 2K | 4K",
  "ratio": "optional, default 3:4, may be Original",
  "modelId": "optional, default seedream45"
}
```

Notes:

- Provide at least one of `prompt`, `referenceImages`, or `referenceImageUrls`.
- `ratio: "Original"` measures the first reference image.
- The endpoint does not enhance prompts automatically.

Success fields:

- `imageUrl`
- `promptUsed`
- `model`
- `referenceImageCount`
- `remainingBalance`
- `transactionId`

## `/api/v2/apply-preset`

- Method: `POST`
- Auth: body `userKey`
- Purpose: apply a template or style preset from the catalog to user-provided source images

Request body:

```json
{
  "userKey": "required",
  "presetId": "required",
  "sourceImages": ["optional data URL base64 images"],
  "sourceImageUrls": ["optional remote image URLs"],
  "variableValues": {
    "Optional Placeholder": "value"
  },
  "resolution": "optional: 1K | 2K | 4K",
  "ratio": "optional, default 3:4, may be Original",
  "modelId": "optional"
}
```

Notes:

- `presetId` must come from `/api/catalog`.
- Provide at least one `sourceImages` or `sourceImageUrls` entry.
- Template presets use source images as face references and build the final prompt in redraw mode.
- Style presets use the first source image as the photo to transform.
- Invalid `presetId` returns `404` before billing.
- The API returns `presetType` as `template` or `style`.
- `modelId` falls back to the preset default, then `seedream45`.

Success fields:

- `imageUrl`
- `presetId`
- `presetType`
- `promptUsed`
- `model`
- `remainingBalance`
- `transactionId`

## `/api/v2/generate-for-character`

- Method: `POST`
- Auth: body `userKey`
- Purpose: generate a scene using one or more saved characters

Request body:

```json
{
  "userKey": "required",
  "characterIds": ["required character IDs"],
  "prompt": "required scene description",
  "personImages": ["optional additional data URL base64 images"],
  "resolution": "optional: 1K | 2K | 4K",
  "ratio": "optional, default 3:4",
  "modelId": "optional, default seedream45"
}
```

Notes:

- The endpoint does not enhance the prompt automatically.
- Use `/api/enhance-prompt` first if the prompt needs refinement.
- Multi-character scenes are supported by sending multiple `characterIds`.
- Characters are resolved before billing and missing characters return `404`.
- This v2 endpoint replaces the legacy character scene generation flow.

Success fields:

- `imageUrl`
- `promptUsed`
- `model`
- `characterNames`
- `remainingBalance`
- `transactionId`
- `historyItem`

## `/api/enhance-prompt`

- Method: `POST`
- Auth: none
- Purpose: refine a prompt before generation

Request body:

```json
{
  "category": "required prompt category",
  "prompt": "required user prompt",
  "characters": [
    {
      "name": "optional",
      "description": "optional"
    }
  ],
  "model": "optional LLM model"
}
```

Success fields:

- `enhancedPrompt`

Notes:

- Use this endpoint before `/api/v2/generate-image` or `/api/v2/generate-for-character` when the source prompt is weak.
- The response is text only; it does not generate an image.

## `/api/catalog`

- Method: `GET`
- Auth: none
- Purpose: discover active presets and usage hints

Query parameters:

- `type`: `templates`, `styles`, or `all` (default)
- `category`: optional category filter

Success payload shape:

```json
{
  "success": true,
  "data": {
    "templates": [],
    "styles": [],
    "usage": {}
  }
}
```

Use this response to:

- choose a valid `presetId`
- inspect categories
- inspect preset metadata and usage guidance

## `/api/model-costs`

- Method: `GET`
- Auth: none
- Purpose: inspect token costs for supported models

Success payload shape:

```json
{
  "seedream45": {
    "generate": 10,
    "style": 12
  }
}
```

Use this response before overriding `modelId` on costly jobs.

## `/api/pricing-config`

- Method: `GET`
- Auth: none
- Purpose: resolve user-supplied model names to valid `modelId` values and inspect pricing coefficients

Success payload shape:

```json
{
  "basePoints": 10,
  "models": [
    {
      "id": "seedream45",
      "label": "Seedream 4.5",
      "labelEn": "Seedream 4.5",
      "seriesId": "seedream",
      "seriesName": "Seedream",
      "coefficient": 1
    }
  ],
  "resolutions": [
    {
      "id": "2K",
      "coefficient": 1
    }
  ]
}
```

Use this response to:

- resolve a user-provided model name to a real `models[].id`
- estimate cost with `basePoints * model.coefficient * resolution.coefficient`
- present valid models and resolutions back to the user when the request is ambiguous

## `/api/characters`

Supported methods:

- `GET /api/characters`: list characters
- `GET /api/characters?id=...`: fetch one character
- `POST /api/characters`: create a character
- `PUT /api/characters`: update a character
- `DELETE /api/characters?id=...`: delete a character

Auth:

- `x-api-key` header or `Authorization: Bearer`

Create request body:

```json
{
  "name": "required",
  "photoBase64": "required data URL base64 image",
  "description": "optional"
}
```

Update request body:

```json
{
  "id": "required",
  "name": "optional",
  "photoBase64": "optional",
  "description": "optional",
  "isActive": true
}
```

Use this endpoint to create and maintain the `characterIds` needed by `/api/v2/generate-for-character`.

## `/api/history`

Supported methods:

- `GET /api/history`: return up to 50 recent history items
- `POST /api/history`: add a history item
- `DELETE /api/history?id=...`: delete a history item

Auth:

- `x-api-key` header or `Authorization: Bearer`

POST request body:

```json
{
  "prompt": "required",
  "resultImageUrl": "required URL or data URL base64",
  "referenceImages": ["optional"],
  "templateImage": "optional",
  "timestamp": 1735689600,
  "model": "optional"
}
```

Notes:

- Some generation endpoints already return `historyItem`.
- Preserve returned IDs so later history cleanup stays possible.

## `/api/billing/balance`

- Method: `POST`
- Auth: body `userKey`
- Purpose: inspect remaining balance

Request body:

```json
{
  "userKey": "required"
}
```

Success fields:

- `balance`

## `/api/v1/recharge/plans`

- Method: `GET`
- Auth: `Authorization: Bearer <serviceKey>` preferred, or `serviceKey` query parameter
- Base URL: `https://billing.tuqu.ai`
- Purpose: list available recharge plans for the project bound to the service key

Request:

- No extra parameters beyond the service key.

Success payload shape:

```json
{
  "success": true,
  "data": {
    "plans": [
      {
        "id": "698b7fead4c733c85f2a9c74",
        "name": "20点送5点",
        "type": "perpetual",
        "priceAmount": 200,
        "priceCurrency": "USD",
        "tokenGrant": 20,
        "bonusToken": 5
      }
    ]
  }
}
```

Plan fields:

| Field | Type | Notes |
| --- | --- | --- |
| `id` | string | Pass as `planId` to recharge endpoints |
| `name` | string | Human-readable package name |
| `type` | string | `perpetual`, `monthly_refill`, or `pay_as_you_go` |
| `priceAmount` | number | Minor currency units; `JPY` already uses yen |
| `priceCurrency` | string | ISO currency code such as `USD`, `CNY`, or `JPY` |
| `tokenGrant` | number | Purchased token amount |
| `bonusToken` | number | Bonus token amount |

Notes:

- The service key determines both the project and the user; the client does not send project IDs.
- A revoked or frozen service key returns `401 UNAUTHORIZED`.

## `/api/v1/recharge/wechat`

- Method: `POST`
- Auth: `Authorization: Bearer <serviceKey>` preferred, or body `serviceKey`
- Base URL: `https://billing.tuqu.ai`
- Purpose: create a Unifpay-backed WeChat payment and return QR payment data

Request body:

```json
{
  "planId": "required",
  "serviceKey": "optional when Authorization header is used"
}
```

Success fields:

- `orderId`
- `unifpayOrderId`
- `qrcodeImg`
- `codeUrl`
- `payUrl`

Success payload shape:

```json
{
  "success": true,
  "data": {
    "orderId": "myproject_1709712345678_a1b2c3",
    "unifpayOrderId": "UP20240306123456",
    "qrcodeImg": "data:image/png;base64,...",
    "codeUrl": "weixin://wxpay/bizpayurl?pr=xxxxx",
    "payUrl": "https://pay.unifpay.com/..."
  }
}
```

Currency rules:

| Plan currency | Payment currency | Notes |
| --- | --- | --- |
| `CNY` | `CNY` | Direct |
| `JPY` | `JPY` | Direct |
| `USD` | `CNY` | Converted using the project's exchange rate, default `1 USD = 7.2 CNY` |
| Other | - | Returns `CURRENCY_NOT_SUPPORTED` |

Notes:

- `PAYMENT_NOT_CONFIGURED` means WeChat or Unifpay is not configured for the project.
- Return both `qrcodeImg` and `codeUrl` when present; some callers want to render their own QR code.

## `/api/v1/recharge/stripe`

- Method: `POST`
- Auth: `Authorization: Bearer <serviceKey>` preferred, or body `serviceKey`
- Base URL: `https://billing.tuqu.ai`
- Purpose: create a Stripe Checkout Session and return a payment link plus QR code

Request body:

```json
{
  "planId": "required",
  "successUrl": "optional",
  "cancelUrl": "optional",
  "serviceKey": "optional when Authorization header is used"
}
```

Success fields:

- `checkoutUrl`
- `sessionId`
- `qrcodeImg`

Success payload shape:

```json
{
  "success": true,
  "data": {
    "checkoutUrl": "https://checkout.stripe.com/c/pay/cs_test_xxx...",
    "sessionId": "cs_test_xxx...",
    "qrcodeImg": "data:image/png;base64,..."
  }
}
```

Notes:

- The selected plan must have a non-empty `stripePriceId`.
- The project must have Stripe configured either globally or in project-level `paymentConfig.stripe`.
- Preserve `sessionId`; it is the easiest handle for later payment-state checks.
- additional billing metadata when returned by the service

Use this endpoint before high-cost generation or when the user explicitly asks about credits.
