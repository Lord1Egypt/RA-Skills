---
name: image-hosting
description: >
  Upload images to img402.dev and get a public URL. Three tiers: free (1MB,
  7-day, no auth), $0.01 USDC (5MB, 1-year, x402), or $1 USDC (5MB, permanent,
  x402). Use when the agent needs a hosted image URL — for sharing in messages,
  embedding in documents, posting to social platforms, or any context that
  requires a public link to an image file.
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Image Hosting — img402

Upload an image to [img402.dev](https://img402.dev) and get a public URL. No account, no API key, no config.

## Pick a tier

| Tier | Price | Max size | Retention | Use when |
|------|-------|----------|-----------|----------|
| Free | $0 | 1 MB | 7 days | Trying things out, ephemeral sharing, PR review screenshots |
| 1-year | $0.01 USDC | 5 MB | 1 year | Diagrams, docs, references |
| Permanent | $1.00 USDC | 5 MB | Permanent\* | Blog hero images, public docs, brand assets |

\* Service-life retention. If img402 ever shuts down, there's a 90-day on-site notice before takedown. See [Terms § 2A](https://img402.dev/terms).

## Quick reference

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png

# Response
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":"2026-02-17T..."}
```

## Workflow

1. **Get image**: Use an existing file, or generate/download one.
2. **Check size**: Must be under 1MB. If larger, resize:
   ```bash
   sips -Z 1600 /path/to/image.png    # macOS — scale longest edge to 1600px
   convert /path/to/image.png -resize 1600x1600 /path/to/image.png  # ImageMagick
   ```
3. **Upload**:
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png
   ```
4. **Use the URL**: The `url` field in the response is a public CDN link. Embed it wherever needed.

## Constraints

- **Max size**: 1MB
- **Retention**: 7 days
- **Formats**: PNG, JPEG, GIF, WebP
- **Rate limit**: 1,000 free uploads/day (global)
- **No auth required**

## Paid tiers

When the user needs a longer-lived URL, use the paid flow. Two-step: pay for an upload token via x402, then upload the image with the token.

```bash
# Step 1: Get an upload token (requires x402 payment)
POST https://img402.dev/api/upload/token            # $0.01 USDC → 1-year retention
POST https://img402.dev/api/upload/token/permanent  # $1.00 USDC → permanent retention
# → {"token": "a1b2c3...", "expiresAt": "..."}

# Step 2: Upload with the token (same endpoint either way)
curl -s -X POST https://img402.dev/api/upload \
  -H "X-Upload-Token: a1b2c3..." \
  -F image=@/path/to/image.png
# → {"url":"...", "id":"...", "contentType":"...", "sizeBytes":..., "expiresAt":"..."|null}
```

For permanent uploads the response has `expiresAt: null`. Same flow otherwise.

x402 payment is handled by an x402-capable client (the [Payments MCP tool](https://docs.cdp.coinbase.com/mcp), `@x402/client`, or any other). The client handles the 402 challenge, signs the on-chain payment, and retries automatically. See https://img402.dev/blog/paying-x402-apis for details.

## Public access

**Uploaded images are reachable by anyone with the URL — there is no auth on serving.** Do not upload screenshots of internal systems, personal information, secrets, API keys, or anything else that shouldn't be public. Once uploaded, the only way to remove an image is to wait for expiry (free / 1-year tiers) or email privacy@img402.dev.
