---
name: image-hosting
description: >
  Upload images to img402.dev and get a public URL. Images 1MB or under are free
  AND permanent — no account, no API key, no payment. Larger images (up to 10MB)
  are free for 30 days, or permanent for $0.01 USDC via x402. Use when the agent
  needs a hosted image URL — for sharing in messages, embedding in documents,
  posting to social platforms, or any context that requires a public link to an
  image file.
metadata:
  openclaw:
    requires:
      bins:
        - curl
---

# Image Hosting — img402

Upload an image to [img402.dev](https://img402.dev) and get a public URL. No account, no API key, no config.

**Most uploads are free and permanent.** A median agent screenshot is ~100 KB, well under the 1 MB threshold where free hosting never expires. Reach for a paid tier only when the file is genuinely large.

## Pick a tier

| Upload | Price | Retention | Use when |
|--------|-------|-----------|----------|
| ≤ 1 MB | $0 | **Permanent** | Almost everything — screenshots, diagrams, charts |
| 1–10 MB | $0 | 30 days | Large images you only need short-term |
| Up to 10 MB | $0.01 USDC | **Permanent** | Large images that must outlive the month |

\* Paid permanence is service-life retention. If img402 ever shuts down, there's a 90-day on-site notice before takedown. See [Terms § 2A](https://img402.dev/terms).

Size is never the reason to pay — 10 MB uploads are free. You pay only to keep an image over 1 MB alive past 30 days.

## Quick reference

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png

# Response — expiresAt is null for images 1MB and under
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":null}
```

## Workflow

1. **Get image**: Use an existing file, or generate/download one.
2. **Upload**:
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/path/to/image.png
   ```
3. **Check `expiresAt`**: `null` means permanent. A timestamp means the file was over 1 MB and will be deleted then.
4. **Use the URL**: The `url` field is a public CDN link. Embed it wherever needed.

If you want a permanent URL and the file is over 1 MB, either shrink it below 1 MB:

```bash
sips -Z 1600 /path/to/image.png                                  # macOS — scale longest edge to 1600px
convert /path/to/image.png -resize 1600x1600 /path/to/image.png  # ImageMagick
```

…or use the paid flow below.

## Constraints

- **Max size**: 10 MB (every tier)
- **Formats**: PNG, JPEG, GIF, WebP
- **Rate limit**: 100,000 free uploads/day globally, 1,000/day per IP
- **No auth required**

## Paid tier

When you need permanence for a file over 1 MB, use the paid flow. Two steps: pay for an upload token via x402, then upload the image with that token.

```bash
# Step 1: Get an upload token (requires x402 payment)
POST https://img402.dev/api/upload/token   # $0.01 USDC → permanent, up to 10MB
# → {"token": "a1b2c3...", "expiresAt": "..."}

# Step 2: Upload with the token
curl -s -X POST https://img402.dev/api/upload \
  -H "X-Upload-Token: a1b2c3..." \
  -F image=@/path/to/image.png
# → {"url":"...", "id":"...", "contentType":"...", "sizeBytes":..., "expiresAt":null}
```

The `expiresAt` in step 1 is the token's expiry (10 minutes), not the image's. The uploaded image's `expiresAt` is `null` — permanent.

`POST /api/upload/token/permanent` still exists at $1.00 USDC. It's a legacy alias that does exactly what the $0.01 route now does; don't use it for new work.

x402 payment is handled by an x402-capable client (the [Payments MCP tool](https://docs.cdp.coinbase.com/mcp), `@x402/client`, or any other). The client handles the 402 challenge, signs the on-chain payment, and retries automatically. See https://img402.dev/blog/paying-x402-apis for details.

## Retention is fixed at upload

The `expiresAt` you get back is the commitment for that image. Later pricing changes apply to new uploads only — an image already uploaded keeps the retention it was given, and img402 won't silently extend it.

## Public access

**Uploaded images are reachable by anyone with the URL — there is no auth on serving.** Do not upload screenshots of internal systems, personal information, secrets, API keys, or anything else that shouldn't be public. Since most uploads are now permanent, treat every upload as public and irreversible: to remove an image, email privacy@img402.dev.
