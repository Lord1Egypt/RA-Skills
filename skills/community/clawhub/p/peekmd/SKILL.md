# peekmd

Turn markdown into a beautiful, shareable web page with one API call. Built for AI agents, bots, and developers.

## When to Use

Use peekmd when you need to share formatted content — reports, docs, code snippets, tables, diagrams — as a readable web page instead of raw markdown. The page auto-expires, so it's ideal for temporary shares, previews, and one-off renders.

## Quick Start (Free Tier)

```bash
curl -X POST https://peekmd.dev/api/create \
  -H "Content-Type: application/json" \
  -d '{"markdown": "# Hello World\n\nThis is a **peekmd** page."}'
```

Response:

```json
{
  "url": "https://peekmd.dev/aBcDeFgH",
  "slug": "aBcDeFgH",
  "expiresAt": "2026-03-22T04:30:00.000Z",
  "tier": "free"
}
```

The `url` is immediately shareable. Free pages expire in 5 minutes and include a small ad banner.

## Endpoints

### `POST /api/create`

Create a rendered markdown page.

**Body (JSON):**

| Field      | Type   | Required | Description                                         |
|------------|--------|----------|-----------------------------------------------------|
| `markdown` | string | yes      | Markdown content (max 500 KB)                       |
| `ttl`      | number | no       | Time-to-live in seconds. 0 = permanent. Default: 300 (free tier max). |

**Response (201):**

```json
{
  "url": "https://peekmd.dev/aBcDeFgH",
  "slug": "aBcDeFgH",
  "expiresAt": "2026-03-22T04:30:00.000Z",
  "tier": "free"
}
```

### `GET /:slug`

Returns the rendered HTML page. Share this URL directly.

### `POST /api/burn/:slug`

Delete a page immediately. Returns `{ "ok": true }` or 404.

### `GET /api/pricing`

Returns pricing details for all tiers.

### `GET /health`

Health check. Returns `{ "status": "ok" }`.

## Payment Tiers

| Tier   | Max TTL     | Ad Banner | Auth                          | Price              |
|--------|-------------|-----------|-------------------------------|--------------------|
| free   | 5 min       | yes       | none                          | free               |
| stripe | unlimited   | no        | `Authorization: Bearer sk_...`| $0.001-$0.01/page (coming soon) |
| x402   | unlimited   | no        | `X-PAYMENT` header            | 0.01 USDC/page (coming soon)    |

### Stripe (metered billing)

1. `POST /api/stripe/checkout` to get a checkout URL.
2. Complete checkout to receive an API key.
3. Pass `Authorization: Bearer sk_your_key` on all requests.
4. Check usage: `GET /api/billing/status` with same auth header.

### x402 (crypto, no account needed)

1. Send a `POST /api/create` request — receive a 402 with payment details.
2. Pay the specified amount via the x402 protocol.
3. Retry the request with the `X-PAYMENT` header containing the receipt.

## Tips for Agents

- **Default to free tier** for quick shares. 5 minutes is enough for most agent-to-human handoffs.
- **Use TTL strategically**: set `ttl: 60` for a 1-minute preview, or omit it to get the tier default.
- **Markdown features**: supports GFM tables, fenced code blocks with syntax highlighting, task lists, and standard markdown.
- **Size limit**: 500 KB max per page. For larger content, split into multiple pages.
- **Burn after reading**: call `/api/burn/:slug` to delete a page after the recipient has viewed it.
- **Base URL**: `https://peekmd.dev`

## Source

Homepage: [peekmd.dev](https://peekmd.dev)

