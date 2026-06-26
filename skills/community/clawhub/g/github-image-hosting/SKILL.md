---
name: github-image-hosting
description: >
  Upload images to img402.dev for embedding in GitHub PRs, issues, and comments.
  Free tier (1MB, 7-day, no auth) is the default; paid tiers add 5MB max with
  1-year ($0.01) or permanent ($1) retention via x402. Use when the agent needs
  to share an image in a GitHub context — screenshots, mockups, diagrams, or any
  visual. Triggers: "screenshot this", "attach an image", "add a screenshot to
  the PR", "upload this mockup", or any task producing an image for GitHub.
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - gh
---

# Image Upload for GitHub

Upload an image to [img402.dev](https://img402.dev) and embed the returned URL in GitHub markdown.

## Pick a tier

| Tier | Price | Max size | Retention | Use when |
|------|-------|----------|-----------|----------|
| Free | $0 | 1 MB | 7 days | PR review screenshots, issue comments, draft mockups |
| 1-year | $0.01 USDC | 5 MB | 1 year | README diagrams, architecture docs |
| Permanent | $1.00 USDC | 5 MB | Permanent\* | README hero images, public blog post visuals |

\* Service-life retention with a 90-day on-site shutdown notice — see [Terms § 2A](https://img402.dev/terms).

## Quick reference

```bash
# Upload (multipart)
curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png

# Response
# {"url":"https://i.img402.dev/aBcDeFgHiJ.png","id":"aBcDeFgHiJ","contentType":"image/png","sizeBytes":182400,"expiresAt":"2026-02-17T..."}
```

## Workflow

1. **Get image**: Use an existing file, or capture a screenshot:
   ```bash
   screencapture -x /tmp/screenshot.png        # macOS — full screen
   screencapture -xw /tmp/screenshot.png       # macOS — frontmost window
   ```
2. **Verify size**: Must be under 1MB. If larger, resize:
   ```bash
   sips -Z 1600 /tmp/screenshot.png  # macOS — scale longest edge to 1600px
   ```
3. **Upload**:
   ```bash
   curl -s -X POST https://img402.dev/api/free -F image=@/tmp/screenshot.png
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

- **Max size**: 1MB
- **Retention**: 7 days
- **Formats**: PNG, JPEG, GIF, WebP
- **Rate limit**: 1,000 free uploads/day (global)
- **No auth required**

## Tips

- Prefer PNG for UI screenshots (sharp text). Use JPEG for photos.
- If a screenshot is too large, reduce dimensions with `sips -Z 1600` before uploading.
- When adding to a PR body or comment, use `gh pr comment` or `gh pr edit` with the image markdown.

## Paid tiers

For larger or longer-lived images, pay via x402 for a token, then upload with the token:

```bash
# Step 1: Get an upload token
POST https://img402.dev/api/upload/token            # $0.01 USDC → 1-year retention
POST https://img402.dev/api/upload/token/permanent  # $1.00 USDC → permanent retention
# → {"token": "a1b2c3...", "expiresAt": "..."}

# Step 2: Upload with the token
curl -s -X POST https://img402.dev/api/upload \
  -H "X-Upload-Token: a1b2c3..." \
  -F image=@/tmp/screenshot.png
# → {"url":"...", "expiresAt":"..."|null}   # null = permanent
```

x402 payment is handled by an x402-capable client (the [Payments MCP tool](https://docs.cdp.coinbase.com/mcp), `@x402/client`, or similar). See https://img402.dev/blog/paying-x402-apis.
