---
name: hekkova
description: Permanent memory layer for AI agents. Mint moments to the blockchain via MCP.
metadata:
  openclaw:
    emoji: "🌙"
    requires:
      bins: ["npx"]
      env:
        - HEKKOVA_API_KEY
    tags:
      - blockchain
      - storage
      - ipfs
      - nft
      - polygon
      - mcp
      - memory
      - encryption
      - permanent
    version: "1.2.0"
    author: "hekkova"
    homepage: "https://hekkova.com"
---

# Hekkova — Permanent Memory for AI Agents

Hekkova lets you mint moments permanently to the Polygon blockchain. Content is stored on IPFS via Pinata and encrypted with Lit Protocol based on the privacy phase. Every mint produces a Block ID and on-chain transaction.

## Setup

You need a Hekkova account and API key:

1. Sign up at https://app.hekkova.com
2. Go to API Keys and generate a key (starts with `hk_live_`)
3. Buy a credit pack on the Billing page
4. Set the API key as an environment variable: `HEKKOVA_API_KEY`

## Connection

Connect to Hekkova via MCP. Use the `mcp-remote` bridge:

```
npx mcp-remote https://mcp.hekkova.com/mcp --header "Authorization: Bearer $HEKKOVA_API_KEY"
```

## Available Tools

Eight tools are available once connected.

### mint_moment
Mint content permanently to the blockchain. Supports text, images, and video.
- Required: `title`, `media` (base64), `media_type`
- Optional: `phase` (default: new_moon), `category`, `description`, `tags`, `timestamp`, `source`
- Costs 1 credit for text/image, 2 credits for video
- Video: mp4, webm, and quicktime supported. 50MB cap.
- `source` is an optional flat object for provenance metadata — see Source Metadata below

### mint_from_url
Mint from a public URL. Hekkova fetches the content server-side.
- Required: `url`
- Optional: `title`, `phase`, `category`, `tags`, `source`
- Works with image URLs, Twitter/X posts, Instagram public posts, and web pages
- Costs 1 credit for text/image, 2 credits for video

### list_moments
List minted moments with pagination and filters. Soft-deleted moments are excluded.
- Optional: `limit`, `offset`, `phase`, `category`, `search`, `sort`

### get_moment
Get full details for a single moment by Block ID.
- Required: `block_id`

### update_phase
Change a moment's privacy phase after minting.
- Required: `block_id`, `new_phase`
- Costs 1 credit for text/image moments, 2 credits for video moments
- Legacy Plan accounts get 10 free Phase Shifts per month

### export_moments
Export all moments as JSON or CSV. Soft-deleted moments are excluded.
- Optional: `format` (json or csv)

### get_balance
Check remaining credits and plan details.

### get_account
Get account details including Light ID and wallet address.

## Source Metadata

`mint_moment` and `mint_from_url` accept an optional `source` object for provenance. All fields are optional. Supported fields:

| Field | Type | Description |
|---|---|---|
| `platform` | string | Origin platform (e.g. `"twitter"`, `"instagram"`) |
| `url` | string | Canonical URL of the source |
| `author` | string | Author username or handle |
| `author_id` | string | Platform-specific author ID |
| `author_display_name` | string | Display name of the author |
| `post_id` | string | Platform-specific post/content ID |
| `created_at` | ISO 8601 | Timestamp of original content creation |
| `captured_at` | ISO 8601 | Timestamp when content was captured |
| `capture_hash` | string | SHA-256 hash of the captured content |
| `like_count` | number | Likes at capture time |
| `repost_count` | number | Reposts/shares at capture time |
| `reply_count` | number | Replies at capture time |
| `view_count` | number | Views at capture time |
| `quote_count` | number | Quotes at capture time |
| `bookmark_count` | number | Bookmarks at capture time |
| `reply_to_id` | string | ID of the post this is a reply to |
| `thread_id` | string | Thread root ID |
| `conversation_id` | string | Conversation ID |
| `media_urls` | string[] | Array of media URLs in the source post |
| `media_types` | string[] | MIME types corresponding to `media_urls` |
| `language` | string | BCP 47 language code |
| `is_verified` | boolean | Whether the author was verified at capture time |

Any additional provenance fields can be passed as `source_extra_*` freeform keys (e.g. `source_extra_note`, `source_extra_campaign_id`).

## Privacy Phases

Every moment has a privacy phase. Default is `new_moon` (fully encrypted).

- `new_moon` — Owner only. Encrypted with Lit Protocol. **This is the default.**
- `crescent` — Close circle. Token-gated encryption. *(coming soon)*
- `gibbous` — Extended group. Token-gated. *(coming soon)*
- `full_moon` — Fully public. No encryption. Accessible via any IPFS gateway.

## Moment Categories (optional)

- `super_moon` — Major life event
- `blue_moon` — Rare moment
- `super_blue_moon` — Once in a lifetime
- `eclipse` — Time-locked until a reveal date. Legacy Plan only. Requires `eclipse_reveal_date`. Functional.

## Pricing

**Credit packs:**

| Pack | Credits | Price |
|---|---|---|
| First Light | 5 | $2.50 |
| Arc Builder | 20 | $9.00 |
| Eternal Light | 50 | $20.00 |

**Legacy Plan:** $27.30/year — includes 10 free Phase Shifts per month, eclipse moments, and heir access (coming soon).

**Credit costs per action:**
- Text or image mint: 1 credit
- Video mint: 2 credits
- Text/image Phase Shift: 1 credit
- Video Phase Shift: 2 credits
- Legacy Plan: 10 Phase Shifts free per month, then standard credit cost

## Rules

- Check balance with `get_balance` before minting if credits may be low
- Video minting costs 2 credits and enforces a 50MB cap
- Eclipse moments require `eclipse_reveal_date` and a Legacy Plan — they are time-locked and sealed until the reveal date
- Soft-deleted moments (those with a `deleted_at` timestamp) are excluded from `list_moments` and `export_moments` results
- Never store or log the API key in any output
- When a mint succeeds, report the Block ID, Token ID, phase, and credits remaining
- When balance is 0, direct the user to https://app.hekkova.com/billing to purchase more credits
- Content on IPFS can be viewed at: `https://gateway.pinata.cloud/ipfs/{media_cid}`
- Transactions can be verified at: `https://polygonscan.com/tx/{polygon_tx}`

## Examples

**Mint text:**
"Mint a moment called 'Project launch day' with the text 'We shipped v1.0 today'"

**Mint an image:**
"Mint this screenshot as 'UI mockup v2' with New Moon privacy"

**Mint a video:**
"Mint this mp4 as 'Demo recording' — use 2 credits"

**Mint from URL:**
"Mint this tweet permanently: https://x.com/user/status/123"

**Mint with source provenance:**
"Mint this tweet and include the platform, author, and like count in the source metadata"

**Eclipse moment:**
"Mint this as an eclipse moment — seal it until 2026-01-01"

**Phase Shift:**
"Change moment BLK_abc123 to full_moon"

**Check balance:**
"How many Hekkova credits do I have left?"

**List moments:**
"Show me all my minted moments"

**Export:**
"Export my Hekkova moments as JSON"
