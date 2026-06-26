# Hekkova — Permanent Memory for AI Agents

An OpenClaw skill that connects your agent to [Hekkova](https://hekkova.com), the permanent memory layer for AI agents.

Mint moments permanently to the Polygon blockchain with IPFS storage and Lit Protocol encryption. Your agent can preserve photos, videos, text, and web content — encrypted by default, owned by you forever.

## Installation

```
clawhub install hekkova
```

## Setup

1. Sign up at [app.hekkova.com](https://app.hekkova.com)
2. Generate an API key on the API Keys page (starts with `hk_live_`)
3. Buy a credit pack on the Billing page
4. Set your API key:

```
export HEKKOVA_API_KEY=hk_live_your_key_here
```

## MCP Endpoint

```
https://mcp.hekkova.com/mcp
```

Auth: `Authorization: Bearer $HEKKOVA_API_KEY`

## What You Can Do

- **Mint text and images** via `mint_moment` — 1 credit each
- **Mint video** (mp4, webm, quicktime) via `mint_moment` — 2 credits, 50MB cap
- **Mint from URLs** — tweets, Instagram posts, images, web pages via `mint_from_url`
- **Attach source provenance** — optional metadata object with platform, author, timestamps, engagement counts, SHA-256 capture hash, and freeform extensions
- **Four privacy phases** — from fully encrypted owner-only (`new_moon`) to fully public (`full_moon`)
- **Phase Shifts** — change a moment's privacy phase after minting (1 credit for text/image, 2 for video)
- **Eclipse moments** — time-locked until a reveal date, Legacy Plan only
- **List and search** all your minted moments
- **Export** your archive as JSON or CSV
- **Verify** every mint on Polygonscan and IPFS

## Tools (8)

| Tool | What it does |
|---|---|
| `mint_moment` | Mint text, image, or video content directly |
| `mint_from_url` | Mint from a public URL (server-side fetch) |
| `list_moments` | List moments with pagination and filters |
| `get_moment` | Get full details for a moment by Block ID |
| `update_phase` | Change a moment's privacy phase |
| `export_moments` | Export all moments as JSON or CSV |
| `get_balance` | Check credit balance and plan details |
| `get_account` | Get Light ID and wallet address |

## Pricing

**Credit packs:**

| Pack | Credits | Price |
|---|---|---|
| First Light | 5 | $2.50 |
| Arc Builder | 20 | $9.00 |
| Eternal Light | 50 | $20.00 |

**Credit costs:**
- Text or image mint: 1 credit
- Video mint: 2 credits
- Text/image Phase Shift: 1 credit
- Video Phase Shift: 2 credits

**Legacy Plan:** $27.30/year — 10 free Phase Shifts/month, eclipse moments, heir access (coming soon).

## Privacy Phases

| Phase | Access |
|---|---|
| `new_moon` | Owner only. Encrypted. Default. |
| `crescent` | Close circle. *(coming soon)* |
| `gibbous` | Extended group. *(coming soon)* |
| `full_moon` | Fully public. No encryption. |

## Links

- Landing page: [hekkova.com](https://hekkova.com)
- Dashboard: [app.hekkova.com](https://app.hekkova.com)
- MCP endpoint: `mcp.hekkova.com/mcp`

## Security

This skill contains no executable scripts — only MCP connection instructions. Your API key is passed via environment variable and never logged or stored by the skill. All data transmission uses HTTPS. Content encryption is handled server-side by Lit Protocol.
