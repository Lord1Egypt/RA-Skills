---
name: github-image-hosting
description: >
  Upload images to img402.dev for embedding in GitHub PRs, issues, and comments.
  Images 1MB or under are free AND permanent — no payment, no auth — which
  covers virtually every screenshot. Larger images (up to 10MB) are free for 30
  days, or permanent for $0.01 USDC via x402. Use when the agent needs to share
  an image in a GitHub context — screenshots, mockups, diagrams, or any visual.
  Triggers: "screenshot this", "attach an image", "add a screenshot to the PR",
  "upload this mockup", or any task producing an image for GitHub.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - gh
---

# Image Upload for GitHub

Upload an image to [img402.dev](https://img402.dev) and embed the returned URL in GitHub markdown.

**Screenshots are free and permanent.** A UI screenshot is typically 100–400 KB, well under the 1 MB threshold where free hosting never expires — so a link you drop in a PR won't rot into a broken image six months later. You almost never need a paid tier here.

## Pick a tier

| Upload | Price | Retention | Use when |
|--------|-------|-----------|----------|
| ≤ 1 MB | $0 | **Permanent** | PR screenshots, issue comments, mockups, README diagrams |
| 1–10 MB | $0 | 30 days | Large captures you only need during review |
| Up to 10 MB | $0.01 USDC | **Permanent** | Large README hero images, public blog visuals |

\* Paid permanence is service-life retention with a 90-day on-site shutdown notice — see [Terms § 2A](https://img402.dev/terms).

## Quick reference

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png

# Response — expiresAt is null for images 1MB and under
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":null}
```

## Workflow

1. **Get image**: Use an existing file, or capture a screenshot:
   ```bash
   screencapture -x /tmp/screenshot.png        # macOS — full screen
   screencapture -xw /tmp/screenshot.png       # macOS — frontmost window
   ```
2. **Upload**:
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png
   ```
3. **Check `expiresAt`**: `null` means permanent. A timestamp means the file was over 1 MB and will be deleted then — if the image needs to outlive that, shrink it under 1 MB and re-upload:
   ```bash
   sips -Z 1600 /tmp/screenshot.png  # macOS — scale longest edge to 1600px
   ```
4. **Embed** the returned `url` in GitHub markdown:
   ```markdown
   ![Screenshot description](https://i.img402.dev/aBcDeFgHiJ.png)
   ```

## GitHub integration

Use `gh` CLI to embed images in PRs and issues:

```bash
# Add to PR description
gh pr edit --body "$(gh pr view --json body -q .body)

![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"

# Add as PR comment
gh pr comment --body "![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"

# Add to issue
gh issue comment 123 --body "![Screenshot](https://i.img402.dev/aBcDeFgHiJ.png)"
```

## Constraints

- **Max size**: 10 MB (every tier)
- **Formats**: PNG, JPEG, GIF, WebP
- **Rate limit**: 100,000 free uploads/day globally, 1,000/day per IP
- **No auth required**

## Tips

- Prefer PNG for UI screenshots (sharp text). Use JPEG for photos.
- Keeping screenshots under 1 MB is worth doing on purpose: it's the line between a permanent URL and one that expires in 30 days. `sips -Z 1600` usually gets there with no visible quality loss.
- When adding to a PR body or comment, use `gh pr comment` or `gh pr edit` with the image markdown.

## Paid tier

For images over 1 MB that need to be permanent, pay via x402 for a token, then upload with it:

```bash
# Step 1: Get an upload token
POST https://img402.dev/api/upload/token   # $0.01 USDC → permanent, up to 10MB
# → {"token": "a1b2c3...", "expiresAt": "..."}

# Step 2: Upload with the token
curl -s -X POST https://img402.dev/api/upload \
  -H "X-Upload-Token: a1b2c3..." \
  -F image=@/tmp/screenshot.png
# → {"url":"...", "expiresAt":null}   # null = permanent
```

`POST /api/upload/token/permanent` still exists at $1.00 USDC — a legacy alias for what $0.01 now does. Don't use it for new work.

x402 payment is handled by an x402-capable client (the [Payments MCP tool](https://docs.cdp.coinbase.com/mcp), `@x402/client`, or similar). See https://img402.dev/blog/paying-x402-apis.

## Public access

Uploaded images are reachable by anyone with the URL — there is no auth on serving, and most uploads are now permanent. Never upload screenshots containing internal systems, credentials, tokens, or customer data. To remove an image, email privacy@img402.dev.
