---
name: htmlpix-api
description: "Use when the user wants to call, test, or integrate the HTMLPix HTML-to-image API — including auth setup, signed URL minting, image rendering, template CRUD, and AI template generation."
---

# HTMLPix API Skill

Use the API contracts below when generating code, curl commands, SDK wrappers, or troubleshooting responses.

## Base URL and Auth

- API Base URL: `https://api.htmlpix.com`
- Private endpoints require: `Authorization: Bearer <API_KEY>`
- API keys are prefixed `hpx_` and managed at `https://htmlpix.com/api-keys`
- Do not call private endpoints from browser client code; mint URLs on the backend.

### Authentication Flow

Every private request goes through this pipeline:

1. Extract `Authorization: Bearer <key>` header
2. Hash the key with SHA-256, look up by hash in the `apiKeys` table
3. Verify key status is `active` (otherwise `403 KEY_INACTIVE`)
4. Query the user's subscription status from `quotas` table
5. Subscription must be `active`, `trialing`, or `canceled` with time remaining

### Error Codes

| Status | Code | Meaning |
|--------|------|---------|
| `401` | `MISSING_API_KEY` | No `Authorization: Bearer` header |
| `401` | `INVALID_API_KEY` | Key not found |
| `403` | `KEY_INACTIVE` | Key revoked or disabled |
| `402` | `NO_SUBSCRIPTION` | No quota record found |
| `402` | `SUBSCRIPTION_INACTIVE` | Subscription expired or past_due |
| `429` | `QUOTA_EXCEEDED` | Monthly mint quota exhausted |

## Endpoint Contracts

### POST `/v1/url` (private)

Mint one signed image URL. The server resolves template variables, executes the template JSX, uploads the rendered VNode to Cloudflare R2/KV, and returns a signed URL pointing to the Cloudflare Worker that renders the final image.

**Request JSON:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `templateId` | string | yes | max 128 chars |
| `width` | integer | no | 1–4096, defaults to template value or 1200 |
| `height` | integer | no | 1–4096, defaults to template value or 630 |
| `format` | string | no | `png`, `jpeg`, or `webp` — defaults to template value or `webp` |
| `quality` | integer | no | 0–100, defaults to template value |
| `devicePixelRatio` | number | no | positive number, defaults to template value or 1 |
| `tv` | string | no | max 128 chars, cache-busting version tag — defaults to template `updatedAt` |
| `variables` | object | no | max 64 keys, key max 64 chars, each value max 4000 chars serialized. Values can be string, number, boolean, null, array, or nested object. |

**Response `200`:**

```json
{ "url": "https://image.htmlpix.com/v1/image?...&sig=...", "expiresAt": 1710345600000 }
```

**Operational limits:**

- Body size max: 32 KB
- Rate: 120 mint requests per 60s per API key
- Concurrency: 4 in-flight per user
- URLs expire after ~5 years by default

### POST `/v1/urls` (private)

Mint multiple signed image URLs in one request.

**Request JSON:**

```json
{ "items": [ /* each item has same shape as POST /v1/url */ ] }
```

- `items.length` must be 1–25

**Response `200`:**

```json
{ "urls": [{ "templateId": "...", "url": "...", "expiresAt": 1710345600000 }] }
```

**Operational limits:**

- Body size max: 256 KB

### GET `/v1/image` (public, signed — served by Cloudflare Worker)

Requests to `api.htmlpix.com/v1/image` are **301-redirected** to the Cloudflare Worker at `image.htmlpix.com/v1/image`. The Worker renders the image from VNode data stored in R2/KV.

**Required query params:**

| Param | Description |
|-------|-------------|
| `templateId` | Template identifier |
| `uid` | User ID that minted the URL |
| `exp` | Expiry timestamp (unix ms) |
| `sig` | HMAC signature — invalidated if any param changes |

**Optional query params:**

| Param | Default | Description |
|-------|---------|-------------|
| `width` | 1200 | Image width |
| `height` | 630 | Image height |
| `format` | `webp` | `png`, `jpeg`, or `webp` |
| `quality` | — | 0–100 |
| `dpr` | — | Device pixel ratio |
| `tv` | — | Cache version tag |
| `rv` | — | Render version |
| `v_<name>` | — | Template variables as `v_title=Hello` |

**Behavior:**

- `403 URL_EXPIRED` — URL past expiry
- `403 INVALID_SIGNATURE` — params modified after signing
- Returns image bytes with immutable caching headers and ETag
- Supports `304 Not Modified` via `If-None-Match`

**Important:** treat minted URLs as opaque. If any query value changes, signature validation fails.

### GET `/v1/templates` (private)

List templates visible to the authenticated user.

**Query params:**

| Param | Default | Values |
|-------|---------|--------|
| `scope` | `all` | `all`, `mine`, `starter` |

**Response `200`:**

```json
{ "templates": [ /* template objects */ ] }
```

### POST `/v1/templates` (private)

Create a custom template. Templates are defined by a single `code` field containing JSX/TSX source code. The server compiles, validates, and extracts variables automatically.

**Request JSON:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | yes | max 120 chars |
| `description` | string | no | max 2000 chars |
| `code` | string | yes | max 180,000 chars — JSX/TSX template source |

**Legacy fields `jsx`, `variables`, `googleFonts`, `width`, `height`, `format` are rejected** with error code `LEGACY_TEMPLATE_PAYLOAD`. Use `code` only.

**Response `201`:**

```json
{ "templateId": "abc123..." }
```

**Error responses:**

- `400 COMPILE_ERROR` — JSX compilation or validation failed
- `400 LEGACY_TEMPLATE_PAYLOAD` — sent a deprecated field

### GET `/v1/templates/:templateId` (private)

Fetch one template visible to the caller.

**Response `200`:**

```json
{ "template": { /* template object */ } }
```

- `404 TEMPLATE_NOT_FOUND` if not visible to caller

### PATCH `/v1/templates/:templateId` (private)

Update template fields. At least one field required.

**Request JSON:**

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `name` | string | no | max 120 chars |
| `description` | string | no | max 2000 chars |
| `code` | string | no | max 180,000 chars — JSX/TSX template source |

**Legacy fields `jsx`, `variables`, `googleFonts`, `width`, `height`, `format` are rejected.**

**Response `200`:**

```json
{ "templateId": "abc123..." }
```

**Error responses:**

- `400 EMPTY_UPDATE` — no updatable field provided
- `400 COMPILE_ERROR` — JSX compilation failed
- `404 TEMPLATE_NOT_FOUND` — template doesn't exist or not owned by caller

### POST `/v1/templates/generate` (private)

AI-assisted template generation. Always uses batch format.

**Request JSON:**

```json
{
  "items": [
    { "prompt": "A social card with bold title and gradient background", "width": 1200, "height": 630 }
  ]
}
```

| Field | Type | Required | Constraints |
|-------|------|----------|-------------|
| `items` | array | yes | 1–5 items |
| `items[].prompt` | string | yes | max 2000 chars |
| `items[].width` | integer | no | 1–4096, default 1200 |
| `items[].height` | integer | no | 1–4096, default 630 |

**Response `200`:**

```json
{
  "results": [
    { "ok": true, "result": { /* generated template data */ } },
    { "ok": false, "error": "error message" }
  ]
}
```

Each item settles independently — some may succeed while others fail.

**Error responses:**

- `429 QUOTA_EXCEEDED` — AI generation quota hit
- `402 SUBSCRIPTION_REQUIRED` — paid plan needed
- `422 PARSE_FAILED` — AI output couldn't be parsed
- `502 AI_NOT_CONFIGURED` — AI provider not set up
- `502 GENERATION_FAILED` — generic AI failure

## Safe Integration Pattern

1. Keep API key server-side only.
2. Mint with `POST /v1/url` or `/v1/urls` on your backend.
3. Store/embed the returned `url` directly (meta tags, email HTML, social cards, etc.).
4. Do not re-sign or mutate query params client-side.
5. Handle `402`, `429`, and `503` with retries/fallback messaging.

## Minimal Examples

```bash
# Mint a single image URL
curl -X POST https://api.htmlpix.com/v1/url \
  -H "Authorization: Bearer $HTMLPIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "templateId": "tmpl_123",
    "variables": { "title": "Launch Day" },
    "width": 1200,
    "height": 630,
    "format": "png"
  }'
```

```bash
# List your templates
curl -X GET "https://api.htmlpix.com/v1/templates?scope=mine" \
  -H "Authorization: Bearer $HTMLPIX_API_KEY"
```

```bash
# Create a template from code
curl -X POST https://api.htmlpix.com/v1/templates \
  -H "Authorization: Bearer $HTMLPIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Social Card",
    "code": "export default function Template({ title }) {\n  return <div style={{ fontSize: 48 }}>{title}</div>\n}"
  }'
```

```bash
# AI-generate a template
curl -X POST https://api.htmlpix.com/v1/templates/generate \
  -H "Authorization: Bearer $HTMLPIX_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{ "prompt": "Minimalist blog post OG image with title and author" }]
  }'
```

If the user asks for an endpoint not listed above, say it is not present in the current server route table and avoid inventing routes.
