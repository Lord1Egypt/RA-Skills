---
name: linkedin
description: Use when you need to post content to LinkedIn, including text posts, image posts, and #BuildInPublic updates. Handles text-only and image posting via the LinkedIn UGC API through the linkedin channel extension. Triggers on phrases like "post to LinkedIn", "share on LinkedIn", "LinkedIn update", "publish to my feed", "build in public post".
homepage: https://github.com/openclaw/openclaw/tree/main/extensions/linkedin
metadata:
  {
    "openclaw":
      {
        "emoji": "💼",
        "requires": { "config": ["channels.linkedin"] },
        "author": "david-xu",
        "version": "1.0.0",
        "tags": ["social", "linkedin", "posting", "build-in-public"],
      },
  }
---

# LinkedIn Posting

## Overview

Post text and images to LinkedIn via the `message` tool using the linkedin channel. Supports text-only posts, image posts (local files or URLs), and #BuildInPublic updates.

## Prerequisites

The linkedin channel must be configured in `channels.linkedin` with:
- `accessToken`: OAuth 2.0 token with `w_member_social` scope
- `personUrn`: Your LinkedIn person URN (e.g. `urn:li:person:Abc123`)

## Posting Text

Use the `message` tool to send a text post:

```
message send --channel linkedin --text "Your post content here"
```

The post goes to the authenticated user's LinkedIn feed as a public post.

## Posting with Images

Two-step process:

1. **Create the image** — generate or locate the image file (PNG/JPG/GIF/WebP)
2. **Post with image** — use `message send` with the `--media` flag:

```
message send --channel linkedin --text "Post caption" --media /path/to/image.png
```

Supported image sources:
- Local file paths: `/Users/david/image.png`
- `file://` URLs: `file:///Users/david/image.png`
- Remote URLs: `https://example.com/image.png`

## Image Upload Flow (internals)

The extension handles a 3-step LinkedIn UGC API flow automatically:
1. Register upload → gets `uploadUrl` + `asset` URN
2. PUT binary to `uploadUrl`
3. Create UGC post with `asset` reference

You don't need to manage this — just provide the image path.

## Best Practices

- **Always confirm** post content with the owner before posting
- **Keep posts concise** — LinkedIn favors 150-300 word posts
- **Add hashtags** at the end, not inline (3-5 max)
- **For #BuildInPublic**: include what you built, what you learned, a visual
- **Image sizing**: 1200x627px for link previews, 1080x1080 for square posts
- **Never post** without explicit owner approval

## Post Templates

### #BuildInPublic Update
```
🚀 [What you built today]

[2-3 sentences about what it does and why it matters]

Tech stack: [list]

[Screenshot or diagram]

#BuildInPublic #[topic] #[tech]
```

### Project Milestone
```
✅ [Milestone achieved]

[Brief context — what, why, how]

Key learnings:
→ [Learning 1]
→ [Learning 2]
→ [Learning 3]

Next up: [what's coming]

#[project] #[topic]
```

### Technical Deep-Dive
```
💡 TIL: [Thing you learned]

[Explanation in 2-3 paragraphs]

[Code snippet or diagram if relevant]

#TIL #[topic] #[tech]
```

## Troubleshooting

| Error | Cause | Fix |
|---|---|---|
| 401 Unauthorized | Token expired | Re-authenticate, update `channels.linkedin.accessToken` |
| 403 Forbidden | Missing `w_member_social` scope | Re-create OAuth app with correct scopes |
| Image upload 400 | File too large (>10MB) | Compress image before uploading |
| Empty postUrn | API didn't return ID | Post likely succeeded — check LinkedIn feed |
