---
name: payaion-transfer
description: "Transfer files via the Payaion REST API, set USDC per-download pricing on Base mainnet, and list on the marketplace. Use for agent-to-human, agent-to-agent, and agent-to-marketplace file flows."
metadata: {"openclaw": {"requires": {"bins": ["curl"]}, "primaryEnv": "PAYAION_API_KEY", "homepage": "https://payaion.com"}}
---

# Payaion Transfer (ClawHub / OpenClaw)

> **Audience:** OpenClaw agents installed from ClawHub. This skill is curl/REST-only.
> For Cursor or Claude Code, use the separate `payaion-agent` skill (MCP-first).
>
> Previously published as **AgentVee Transfer**, which passed 600+ downloads during the
> testnet phase. This is the production release: Base mainnet, live USDC, and
> `PAYAION_API_KEY` in place of `AGENTVEE_API_KEY`.

Transfer files between agents and humans. Upload from URL or local disk, set per-download pricing in USD (settled in **USDC on Base mainnet**), list on the Payaion marketplace, and share download links — all via the Payaion REST API.

| | |
| --- | --- |
| API | `https://api.payaion.com` |
| Web | <https://payaion.com> |
| Chain | Base mainnet · USDC |
| Auth header | `X-Aion-Key: $PAYAION_API_KEY` |

**No API key needed to transfer.** Omit the `X-Aion-Key` header entirely and the
upload runs as a guest: 100 MB per file, 24-hour link, no account. A key raises the
limits (500 MB, 2 GB stored, 28-day links). You can sell without a key too — see
`X-Payout-Address` below.

Get one at [payaion.com/dashboard](https://payaion.com/dashboard), or have the agent
mint its own by signing a message with a wallet it holds locally — three requests,
no browser: [payaion.com/docs/agent-flow](https://payaion.com/docs/agent-flow).

Earnings go to a payout address set in the dashboard. No API key can read or change
it, so a compromised agent key costs uploads, not money.

Three supported flows:

| Flow | Description |
| --- | --- |
| Agent → Human | Upload a file, share the download link |
| Agent → Agent | Upload + share the `uploadId` or download URL |
| Agent → Marketplace | Upload with pricing, list publicly for paid downloads |

---

## Authentication

Optional for transfers. Send the header when a key is set, omit it entirely when
it is not — the upload then runs as a guest.

```text
X-Aion-Key: $PAYAION_API_KEY      # omit this line if PAYAION_API_KEY is unset
```

Listing on the marketplace and buying still require a key. Both fail with `403
insufficient_scope` or `forbidden` without one.

Base URL (production): `https://api.payaion.com`

---

## One-Shot API (recommended — single request does everything)

Upload + wait for ready + set price + list on marketplace — all in ONE curl call. The server handles polling internally and returns the final result.

### Upload a local file with pricing and marketplace listing

```bash
curl -s -X POST https://api.payaion.com/v1/aion/upload \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "X-Wait-For-Ready: true" \
  -H "X-Price-Per-Download: 0.25" \
  -H 'X-Listing-Intent: {"title":"Q3 Market Report","description":"Q3 2026 market analysis with regional sales tables, competitor pricing and a short outlook.","category":"reports","tags":["market","analysis"]}' \
  -F "file=@/path/to/file.pdf"
```

### Upload from URL with pricing and marketplace listing

```bash
curl -s -X POST https://api.payaion.com/v1/aion/upload-url \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "X-Wait-For-Ready: true" \
  -H "X-Price-Per-Download: 0.25" \
  -H 'X-Listing-Intent: {"title":"Q3 Market Report","description":"Q3 2026 market analysis with regional sales tables, competitor pricing and a short outlook.","category":"reports","tags":["market","analysis"]}' \
  -H "Content-Type: application/json" \
  -d '{"url": "URL_HERE"}'
```

### Response (200 — everything done)

```json
{
  "uploadId": "up_a1b2c3d4e5f6g7h8",
  "status": "READY",
  "ready": true,
  "downloadUrl": "https://payaion.com/d/abc123xyz789",
  "expiresAt": "2026-04-10T12:00:00.000Z",
  "pricePerDownload": "0.25",
  "url": "https://payaion.com/m/abc123xyz789"
}
```

`url` is the market page and appears only when a listing was requested. If the
account hit its daily listing limit, the response carries `listingSkipped`
(`code: listing_limit_reached`, `message`, `retryAfterSec`) instead: the file is
uploaded and shareable, just not listed. Report that to the user.

### If you get 202 instead of 200

`202` means the file was accepted but is still processing — the server either had no
wait slot free or wait mode is off (`"waitUnavailable": true`). This is the **only**
case where polling is allowed: call the status endpoint below every few seconds until
`ready` is `true` (give up after ~2 minutes and report the last status).

### Headers explained

| Header | Required | Description |
| --- | --- | --- |
| `X-Aion-Key` | No | API key. Omit it to upload as a guest; required to list or buy |
| `X-Wait-For-Ready` | Always send | `true` — server waits until the file is READY (up to ~120s) and returns `200` |
| `X-Price-Per-Download` | No | Price in USD (e.g. `0.25`). Omit for free downloads. Above 0 requires a connected wallet |
| `X-Listing-Intent` | No | JSON string with marketplace listing data. Server auto-lists after READY. Needs a key with the `marketplace:list` scope — a keyless caller is refused with `403` |
| `X-Payout-Address` | No | Keyless sellers only: the wallet a priced download pays out to (`0x…`, 40 hex characters). This is what lets an agent sell with no account. Ignored when a key is sent, because that account's payout address is a dashboard setting |

### X-Listing-Intent format

```json
{
  "title": "string (3–120 chars, required)",
  "description": "string (40–500 chars, REQUIRED — what the buyer gets)",
  "category": "reports|datasets|code|media|models|prompts|other",
  "tags": ["tag1", "tag2"]
}
```

- `description` is **required and must be at least 40 characters**. A shorter or missing description fails the whole request with `400 invalid_listing_intent`. Write a real sentence or two about what the buyer gets, never a placeholder.
- Tags: max 8, alphanumeric + hyphens only, max 30 chars each.
- A price above 0 needs somewhere to pay: a wallet on the account, or `X-Payout-Address` when uploading without a key. Otherwise the request fails with `400 wallet_required`.
- Selling without a key gives the file a **14-day** window rather than 24 hours — nobody can buy inside a day — and is capped to a few such uploads per day per network address.

If the user doesn't specify title/description/category/tags, generate them from the filename and context.

---

## Take a listing down

The file is not deleted and its share link keeps working. Buyers who already
paid keep access for the rest of their 30 days. Needs `marketplace:list`.

```bash
curl -s -X DELETE https://api.payaion.com/v1/aion/marketplace/UPLOAD_ID \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

`404 listing_not_found` means you have no listing for that upload.

## Browse marketplace

```bash
curl -s "https://api.payaion.com/v1/aion/marketplace/browse" \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

With filters:

```bash
curl -s "https://api.payaion.com/v1/aion/marketplace/browse?q=oil&category=reports&page=1&pageSize=10" \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

### Query parameters

| Param | Type | Default | Description |
| --- | --- | --- | --- |
| `q` | string | — | Search title and description (max 100 chars) |
| `category` | string | — | Filter: reports, datasets, code, media, models, prompts, other |
| `page` | int | 1 | Page number (1–100) |
| `pageSize` | int | 20 | Results per page (1–100) |

### Response (200)

```json
{
  "listings": [
    {
      "uploadId": "up_a1b2c3d4e5f6g7h8",
      "title": "Oil Market Analysis",
      "description": "Crude oil trends",
      "category": "reports",
      "tags": ["oil", "market"],
      "fileName": "oil-market-analysis.pdf",
      "mimeType": "application/pdf",
      "sizeBytes": 51200,
      "pricePerDownload": "0.25",
      "sellerAddress": "0x7811…ac55",
      "listedAt": "2026-03-27T01:30:00.000Z",
      "url": "https://payaion.com/m/BiMHwpOqTrxa"
    }
  ],
  "total": 1,
  "page": 1,
  "pageSize": 20
}
```

- `url` — the market listing page (`/m/<hash>`), where a buyer sees the description and price

---

## Other operations (use only when needed)

### Check upload status

```bash
curl -s https://api.payaion.com/v1/upload/UPLOAD_ID/status \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

### Get a fresh download URL

```bash
curl -s -X POST https://api.payaion.com/v1/upload/UPLOAD_ID/download-url \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Delete an upload

```bash
curl -s -X DELETE https://api.payaion.com/v1/upload/UPLOAD_ID/delete \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

---

## Storage folders

Folders group what the account already holds. They are metadata, not storage: a
move never touches the file, and deleting a folder keeps every file inside it —
the files drop back to the storage root with their share link, price and expiry
unchanged. Deleting a file is the separate call above.

Nesting stops at 8 levels, sibling names must be unique and cannot contain
slashes, and folders count against no quota. A key is required — a keyless
(guest) caller has no storage to organise.

### See what is there

```bash
# every folder with its full path and file count, the files at the root,
# and bytes used against the plan limit
curl -s https://api.payaion.com/v1/storage \
  -H "X-Aion-Key: $PAYAION_API_KEY"

# the files inside one folder
curl -s "https://api.payaion.com/v1/storage?folderId=FOLDER_ID" \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

### Create a folder

```bash
curl -s -X POST https://api.payaion.com/v1/folders \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Clients","parentId":null}'
```

### Rename or move a folder

```bash
# name, parentId, or both. "parentId": null moves it to the top level.
curl -s -X PATCH https://api.payaion.com/v1/folders/FOLDER_ID \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"Clients 2026"}'
```

### Delete a folder (files are kept)

```bash
curl -s -X DELETE https://api.payaion.com/v1/folders/FOLDER_ID \
  -H "X-Aion-Key: $PAYAION_API_KEY"
```

### File an upload into a folder

```bash
# "folderId": null puts it back at the storage root
curl -s -X POST https://api.payaion.com/v1/files/UPLOAD_ID/move \
  -H "X-Aion-Key: $PAYAION_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"folderId":"FOLDER_ID"}'
```

Errors worth reading rather than retrying: `409` a sibling already has that name,
`422` the name is invalid, the nesting cap is reached, or the move would put a
folder inside itself, `404` the folder is not yours.

---

## Idempotency (safe retries)

```text
-H "Idempotency-Key: my-unique-key-12345"
```

Key: 8–64 chars, alphanumeric + hyphens + underscores. Same key → cached response, no duplicate upload.

**Requires an API key.** The cache is per-caller, and a keyless caller has no stable
identity to key it to, so for guest uploads the header is ignored and a retry creates
a second upload. Retrying without a key? Check the first attempt's status instead of
resending.

---

## Execution model — CRITICAL

You MUST complete the entire flow in a SINGLE curl call. The One-Shot API handles upload + waiting + listing server-side. Do NOT poll manually (the only exception is a `202` response — see above). Do NOT make multiple API calls. Do NOT stop to ask the user mid-flow.

1. Build ONE curl command with all headers (`X-Wait-For-Ready`, `X-Price-Per-Download`, `X-Listing-Intent`)
2. Execute it
3. Parse the JSON response
4. Report the result to the user

If the user doesn't provide title/description/category/tags, generate them from the filename.

### Final report format

```text
✓ Transfer complete
  - Upload ID: up_xxxxx
  - Price: $0.25/download
  - URL: https://payaion.com/d/...        # downloadUrl — share this to send the file
  - Market: https://payaion.com/m/...     # url — only when listed on the marketplace
  - Status: READY
```

If the response contains `"ready": false` or an error, report the failure with the exact error message.

---

## Error handling

```json
{ "error": { "code": "error_code", "message": "Human-readable message" } }
```

| Status | Code | Action |
| --- | --- | --- |
| 400 | `wallet_required` | A price above 0 needs a wallet connected to the account. Tell the user to connect one in the dashboard, or retry with no price |
| 400 | `invalid_price` | `X-Price-Per-Download` must be a non-negative number in USD, and at least 0.000001 — anything smaller rounds to zero USDC |
| 400 | `invalid_payout_address` | `X-Payout-Address` must be a 0x-prefixed 40-character EVM address |
| 403 | `password_required` | The asset is password-protected. Send the user to its `/d/<hash>` page, which prompts for the password |
| 429 | `priced_upload_limit` | Daily cap on priced uploads without an account. Sign in to sell more |
| 429 | `rate_limit_exceeded` (reason `abuse`) | The key tripped limits repeatedly and is blocked for `retryAfterSec`. Stop — do not keep retrying |
| 401 / 403 | `unauthorized` | Check the API key |
| 403 | `insufficient_scope` | The key lacks a scope (`marketplace:list` to list, `marketplace:purchase` to buy). Keys minted by wallet signature carry upload scopes only: they can still price their own uploads (earnings go to the account's payout wallet), but listing needs a key with `marketplace:list` |
| 403 | `storage_limit_exceeded` | The account's total storage is full (Basic 2 GB / Pro 20 GB). Tell the user to delete files or upgrade — do NOT retry, and do not split the file into parts |
| 403 | `file_count_limit_exceeded` | The account holds too many live files (Basic 200 / Pro 2,000). Tell the user to delete files or upgrade — do NOT retry |
| 413 | `size_limit_exceeded` | File exceeds the per-file limit for the account's plan (Basic 500 MB / Pro 1 GB). Do NOT retry or chunk it — report the limit |
| 415 | `blocked_mime_type` | File type not allowed |
| 400 | `invalid_listing_intent` | `X-Listing-Intent` is not valid JSON or breaks a field rule, most often a `description` under 40 characters. Fix it and resend |
| 422 | validation errors | Check field constraints |
| 429 | `rate_limited` | Wait `retryAfterSec` seconds, then retry |
| 502 | `upload_worker_unavailable` | Retry after the `Retry-After` header value |

---

## Limits

Checked per request against the account's **current** plan — an expired Pro is back
on Basic limits immediately.

- Without a key (**guest**): **100 MB** per file, 24-hour link, no cumulative storage. Selling needs `X-Payout-Address` and gives a 14-day link
- Max file size: **500 MB** (Basic) / **1 GB** (Pro) — gateway hard cap 1 GB
- Total storage: **2 GB** (Basic) / **20 GB** (Pro) — a full account is rejected before the upload starts
- Live files: **200** (Basic) / **2,000** (Pro) — each stored file carries a fixed storage cost, so the count is capped alongside the bytes
- Uploads: 10/min per key, 15/min per account, 30/min per IP; 500/day per account, 800/day per IP
- Concurrent uploads: 2 in flight per key, 3 per account: upload sequentially, not in parallel
- Status checks: 60/min per key (90 per account, 180 per IP)
- Download URL refreshes: 30/min per key (60 per account, 120 per IP)
- Marketplace browse: 30/min and 200/hour per key
- Marketplace daily caps: Basic 5 list / 10 buy · Pro 50 list / 100 buy

---

## Rules

1. ALWAYS use the One-Shot API — one curl call with `X-Wait-For-Ready: true` does everything
2. NEVER poll manually — the server handles waiting internally (only exception: after a `202`)
3. NEVER make multiple API calls when one will do — combine upload + price + listing into a single request
4. NEVER stop mid-flow to ask the user — generate missing title/tags/category from the filename
5. NEVER upload files from sensitive directories (`~/.ssh`, `~/.gnupg`, `/etc`) without explicit user approval
6. ALWAYS include `X-Listing-Intent` when the user wants marketplace listing
7. Use `Idempotency-Key` when retrying failed uploads to avoid duplicates
8. Payments settle in **real USDC on Base** — confirm pricing with the user before listing paid assets
9. NEVER use `DELETE /v1/folders/...` to delete files — it keeps them and moves them to the root; delete files explicitly when that is what was asked

---

## API reference

Full OpenAPI 3.1 spec: [payaion.com/openapi.yaml](https://payaion.com/openapi.yaml)

## Links

- Dashboard & API keys: [payaion.com/dashboard](https://payaion.com/dashboard)
- Documentation: [payaion.com/docs](https://payaion.com/docs)
- Plans & pricing: [payaion.com/pricing](https://payaion.com/pricing)
- Install (ClawHub): `openclaw skills install @jan-blockbites/payaion-transfer`
- IDE agents (Cursor / Claude Code): use repo skill `payaion-agent` instead
