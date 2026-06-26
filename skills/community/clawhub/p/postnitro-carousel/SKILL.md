---
name: postnitro-carousel
description: Generate professional social media carousel posts using the PostNitro.ai Embed API. Supports AI-powered content generation and manual content import for LinkedIn, Instagram, TikTok, and X (Twitter) carousels. Use this skill whenever the user wants to create a carousel, social media post, slide deck for social media, multi-slide content, or mentions PostNitro. Also trigger when the user asks to turn text, articles, blog posts, or topics into carousel posts, or wants to automate social media content creation. Outputs PNG images or PDF files. Requires a PostNitro API key.
homepage: https://postnitro.ai
metadata: {"openclaw":{"emoji":"🎠","primaryEnv":"POSTNITRO_API_KEY","requires":{"env":["POSTNITRO_API_KEY","POSTNITRO_TEMPLATE_ID","POSTNITRO_BRAND_ID","POSTNITRO_PRESET_ID"]}}}
---

# PostNitro Carousel Generator

Generate social media carousel posts via the PostNitro.ai Embed API. Two workflows: **AI generation** (topic/article/X post → carousel) and **content import** (your own slides, with optional infographics).

## Setup

1. Sign up at https://postnitro.ai (free plan: 5 credits/month)
2. Go to account settings → "Embed" → generate an API key
3. Set up your template, brand, and AI preset in the PostNitro dashboard
4. Set environment variables:
   ```bash
   export POSTNITRO_API_KEY="your-api-key"
   export POSTNITRO_TEMPLATE_ID="your-template-id"
   export POSTNITRO_BRAND_ID="your-brand-id"
   export POSTNITRO_PRESET_ID="your-ai-preset-id"
   ```

Base URL: `https://embed-api.postnitro.ai`
Auth header: `embed-api-key: $POSTNITRO_API_KEY`

## Core Workflow

All carousel creation is asynchronous: **Initiate → Poll Status → Get Output**.

### 1. Generate a carousel with AI

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/generate' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "presetId": "'"$POSTNITRO_PRESET_ID"'",
    "responseType": "PNG",
    "aiGeneration": {
      "type": "text",
      "context": "5 tips for growing your LinkedIn audience in 2026",
      "instructions": "Professional tone, actionable advice"
    }
  }'
```

Returns `{ "success": true, "data": { "embedPostId": "post123", "status": "PENDING" } }`. Save the `embedPostId`.

**`aiGeneration.type` values:**
- `"text"` — context is the text content to turn into a carousel
- `"article"` — context is an article URL to extract and convert
- `"x"` — context is an X (Twitter) post or thread URL

See [examples/generate-from-text.json](examples/generate-from-text.json), [examples/generate-from-article.json](examples/generate-from-article.json), and [examples/generate-from-x-post.json](examples/generate-from-x-post.json).

### 2. Import your own slide content

```bash
curl -X POST 'https://embed-api.postnitro.ai/post/initiate/import' \
  -H 'Content-Type: application/json' \
  -H "embed-api-key: $POSTNITRO_API_KEY" \
  -d '{
    "postType": "CAROUSEL",
    "templateId": "'"$POSTNITRO_TEMPLATE_ID"'",
    "brandId": "'"$POSTNITRO_BRAND_ID"'",
    "responseType": "PNG",
    "slides": [
      { "type": "starting_slide", "heading": "Your Title", "description": "Intro text" },
      { "type": "body_slide", "heading": "Key Point", "description": "Details here" },
      { "type": "ending_slide", "heading": "Take Action!", "cta_button": "Learn More" }
    ]
  }'
```

Returns same response format with `embedPostId`.

**Slide rules:**
- Exactly 1 `starting_slide` (required)
- At least 1 `body_slide` (required)
- Exactly 1 `ending_slide` (required)
- `heading` is required on every slide

**Slide fields:** `heading` (required), `sub_heading`, `description`, `image` (URL), `background_image` (URL), `cta_button`, `layoutType`, `layoutConfig`.

For infographic slides, set `layoutType: "infographic"` on body slides — replaces the image with structured data columns. See [examples/import-infographics.json](examples/import-infographics.json) and [references/api-reference.md](references/api-reference.md) for full infographics config.

### 3. Check post status

```bash
curl -X GET "https://embed-api.postnitro.ai/post/status/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

Poll every 3–5 seconds until `data.embedPost.status` is `"COMPLETED"`. The `logs` array shows step-by-step progress.

### 4. Get the output

```bash
curl -X GET "https://embed-api.postnitro.ai/post/output/$EMBED_POST_ID" \
  -H "embed-api-key: $POSTNITRO_API_KEY"
```

Returns downloadable URLs in `data.result.data`:
- **PNG**: Array of URLs (one per slide)
- **PDF**: Single URL

See [references/api-reference.md](references/api-reference.md) for full response schemas.

## Common Patterns

### Pattern 1: LinkedIn thought leadership carousel

Generate a carousel from a topic with professional tone:

```json
{
  "aiGeneration": {
    "type": "text",
    "context": "5 mistakes startups make with their LinkedIn strategy and how to fix each one",
    "instructions": "Professional but conversational tone. Each slide should have one clear takeaway."
  }
}
```

### Pattern 2: Repurpose a blog post

Turn an existing article into a carousel:

```json
{
  "aiGeneration": {
    "type": "article",
    "context": "https://yourblog.com/posts/social-media-strategy-2026",
    "instructions": "Extract the 5 most actionable points. Keep slide text concise."
  }
}
```

### Pattern 3: Repurpose an X thread

Convert a viral X thread into a visual carousel:

```json
{
  "aiGeneration": {
    "type": "x",
    "context": "https://x.com/username/status/1234567890",
    "instructions": "Maintain the original voice and key points"
  }
}
```

### Pattern 4: Data-driven infographic carousel

Import slides with structured infographic layouts:

See [examples/import-infographics.json](examples/import-infographics.json) for a complete example with grid and cycle layouts.

## Content Strategy Tips

- **LinkedIn**: Professional tone, actionable insights, 6–10 slides, clear CTA.
- **Instagram**: Visual-first, concise text, 5–8 slides, storytelling arc.
- **TikTok**: Trendy, punchy, 4–7 slides, hook on slide 1.
- **X (Twitter)**: Data-driven, 3–6 slides, provocative opening.

## Common Gotchas

1. **Default responseType is PDF** — always specify `"PNG"` explicitly if you want individual slide images.
2. **`heading` is required** on every slide — omitting it returns an error.
3. **Slide structure is strict** — exactly 1 starting, at least 1 body, exactly 1 ending.
4. **Article type needs a URL** — `"article"` type expects a URL as `context`, not plain text.
5. **X type needs an X post URL** — `"x"` type expects `https://x.com/...` or `https://twitter.com/...` as `context`.
6. **Infographics replace images** — setting `layoutType: "infographic"` overrides any `image` on that slide.
7. **Cyclical infographics use first column only** — `columnDisplay: "cycle"` ignores data in columns 2+.
8. **Max 3 columns** — `columnCount` cannot exceed 3 for infographic layouts.
9. **Image URLs must be public** — `image` and `background_image` fields require publicly accessible URLs.
10. **Credits vary by method** — AI generation costs 2 credits/slide, content import costs 1 credit/slide.

## Credits & Pricing

| Plan | Price | Credits/Month |
|------|-------|---------------|
| Free | $0 | 5 |
| Monthly | $10 | 250+ (scalable) |

- Content import: 1 credit per slide
- AI generation: 2 credits per slide

## Supporting Resources

**Reference docs:**
- [references/api-reference.md](references/api-reference.md) — Complete endpoint reference with request/response schemas and infographics config

**Ready-to-use examples:**
- [examples/EXAMPLES.md](examples/EXAMPLES.md) — Index of all examples
- [examples/generate-from-text.json](examples/generate-from-text.json) — AI generation from text
- [examples/generate-from-article.json](examples/generate-from-article.json) — AI generation from article URL
- [examples/generate-from-x-post.json](examples/generate-from-x-post.json) — AI generation from X post
- [examples/import-default.json](examples/import-default.json) — Basic slide import
- [examples/import-infographics.json](examples/import-infographics.json) — Import with infographic layouts

## Quick Reference

```
# Auth
Header: embed-api-key: $POSTNITRO_API_KEY

# AI generation
POST /post/initiate/generate  { postType, templateId, brandId, presetId, responseType?, requestorId?, aiGeneration: { type, context, instructions? } }

# Content import
POST /post/initiate/import  { postType, templateId, brandId, responseType?, requestorId?, slides: [{ type, heading, ... }] }

# Check status (poll until COMPLETED)
GET /post/status/{embedPostId}

# Get output (download URLs)
GET /post/output/{embedPostId}
```

## Tips for the Agent

- Always confirm the user has set `POSTNITRO_API_KEY`, `POSTNITRO_TEMPLATE_ID`, `POSTNITRO_BRAND_ID` before calling any endpoint.
- `POSTNITRO_PRESET_ID` is only required for AI generation, not for content import.
- For `"article"` type, the `context` must be a URL — not article text. For article text, use `"text"` type.
- For `"x"` type, the `context` must be an X/Twitter post URL.
- Default `responseType` is `"PDF"` — always pass `"PNG"` if the user wants individual slide images.
- When importing slides, always structure as: 1 `starting_slide` → 1+ `body_slide` → 1 `ending_slide`.
- For data-heavy content, suggest using infographic layouts on body slides instead of plain text.
- Poll `GET /post/status/{embedPostId}` every 3–5 seconds — don't hammer the endpoint.
- After getting output, the `data` field contains download URLs — present them to the user directly.
- If the user doesn't specify a platform, suggest LinkedIn (most common carousel use case).
- Warn users about credit costs upfront: AI generation is 2x the cost of content import.
