---
name: notipo
description: Publish blog posts from AI agents to WordPress via Notion. One API call handles page creation, markdown conversion, image uploads, featured image generation, and SEO metadata.
homepage: https://notipo.com/docs/api/introduction
metadata: {"clawdbot":{"emoji":"📝","requires":{"bins":[],"env":["NOTIPO_URL","NOTIPO_API_KEY"]}}}
---

## Install Notipo CLI if it doesn't exist

```bash
npm install -g notipo
```

- npm release: https://www.npmjs.com/package/notipo
- notipo docs: https://notipo.com/docs/api/introduction
- notipo cli docs: https://notipo.com/docs/api/cli

## Setup

Sign up at [notipo.com](https://notipo.com/auth/register), connect your Notion database and WordPress site through the dashboard, then grab your API key from **Settings → Account**.

Set the environment variables:

```bash
export NOTIPO_URL="https://notipo.com"
export NOTIPO_API_KEY="ntp_your-api-key"
```

## Core Workflow

1. **Generate** — AI agent creates title, body (markdown), category, tags, SEO keyword
2. **Fetch context** — get categories and tags from Notipo to pick valid values
3. **Publish** — `notipo posts create` with all fields
4. **Monitor** — `notipo jobs` to check completion status

## Essential Commands

### Check connection status

```bash
notipo status
```

### Fetch categories and tags

```bash
# Get available categories (for picking a valid category)
curl -s $NOTIPO_URL/api/categories \
  -H "X-API-Key: $NOTIPO_API_KEY" | jq '.data[].name'

# Get available tags
curl -s $NOTIPO_URL/api/tags \
  -H "X-API-Key: $NOTIPO_API_KEY" | jq '.data[].name'
```

### Create a post (draft)

```bash
notipo posts create \
  --title "Your Post Title" \
  --body "## Introduction\n\nYour markdown content here.\n\n## Main Section\n\nMore content." \
  --category "Tutorials" \
  --tags "automation,ai" \
  --seo-keyword "your focus keyword" \
  --image-title "Featured Image Title" \
  --slug "custom-url-slug"
```

### Create and publish immediately

```bash
notipo posts create \
  --title "Your Post Title" \
  --body "Markdown content here." \
  --category "Guides" \
  --seo-keyword "focus keyword" \
  --publish
```

### Create, publish, and wait for completion

```bash
notipo posts create \
  --title "Your Post Title" \
  --body "Markdown content here." \
  --category "Guides" \
  --publish --wait
```

The `--wait` flag polls until the job completes and returns the result with the WordPress URL.

### Create with inline Unsplash images (Pro plan, curl only)

```bash
curl -X POST $NOTIPO_URL/api/posts/create \
  -H "X-API-Key: $NOTIPO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Your Post Title",
    "body": "## Introduction\n\nContent here.\n\n## Getting Started\n\nMore content.",
    "category": "Tutorials",
    "seoKeyword": "focus keyword",
    "images": [
      { "query": "developer workspace laptop", "afterHeading": "## Introduction" },
      { "query": "getting started tutorial", "afterHeading": "## Getting Started" }
    ],
    "publish": true
  }'
```

### Update a post (fix content, change metadata, re-sync to WordPress)

```bash
notipo posts update POST_ID \
  --body "## Introduction\n\nUpdated content without the H1." \
  --seo-keyword "updated focus keyword" \
  --wait
```

Updates the Notion page content and/or properties, then triggers a re-sync to WordPress. Only the provided fields are updated — omitted fields stay unchanged. This is the correct way to fix post content after creation.

### Check job status

```bash
notipo jobs
```

### List posts

```bash
notipo posts
```

### Trigger a sync (pick up Notion changes)

```bash
notipo sync
```

### Delete a post

```bash
notipo posts delete POST_ID
```

## Common Patterns

### AI-generated blog post with full metadata

```bash
# 1. Fetch categories to pick a valid one
curl -s $NOTIPO_URL/api/categories -H "X-API-Key: $NOTIPO_API_KEY" | jq '.data[].name'

# 2. Create the post with all fields and wait for completion
notipo posts create \
  --title "10 Docker Best Practices for Production" \
  --body "## Introduction\n\nDocker containers are the standard...\n\n## Use Multi-Stage Builds\n\nReduce image size by separating build and runtime...\n\n## Pin Base Image Versions\n\nAvoid surprises by pinning specific tags..." \
  --category "DevOps" \
  --tags "docker,containers,production" \
  --seo-keyword "docker best practices production" \
  --image-title "Docker Best Practices" \
  --slug "docker-best-practices-production" \
  --publish --wait
```

### Batch content pipeline

```bash
# Generate and publish multiple posts in sequence
for topic in "React hooks" "TypeScript generics" "Node.js streams"; do
  notipo posts create \
    --title "A Guide to $topic" \
    --body "## Overview\n\nGenerated content about $topic." \
    --category "Tutorials" \
    --seo-keyword "$(echo $topic | tr '[:upper:]' '[:lower:]')" \
    --wait
done
```

### Full pipeline with inline images (curl)

```bash
curl -X POST $NOTIPO_URL/api/posts/create \
  -H "X-API-Key: $NOTIPO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "10 Docker Best Practices for Production",
    "body": "## Introduction\n\nDocker containers are the standard...\n\n## Use Multi-Stage Builds\n\nReduce image size...",
    "category": "DevOps",
    "tags": ["docker", "containers", "production"],
    "seoKeyword": "docker best practices production",
    "imageTitle": "Docker Best Practices",
    "slug": "docker-best-practices-production",
    "images": [
      { "query": "docker containers server", "afterHeading": "## Introduction" }
    ],
    "publish": true
  }'
```

## CLI Reference

| Command | Description |
|---------|-------------|
| `notipo status` | Show Notion and WordPress connection status |
| `notipo sync` | Trigger an immediate Notion poll |
| `notipo posts` | List all posts |
| `notipo posts create` | Create a post in Notion and sync to WordPress |
| `notipo posts update <id>` | Update post content/properties and re-sync to WordPress |
| `notipo posts delete <id>` | Delete a post (cleans up WordPress + Notion) |
| `notipo jobs` | List recent sync and publish jobs |
| `notipo help` | Show usage and examples |

### posts create flags

| Flag | Description |
|------|-------------|
| `--title <title>` | Post title (required) |
| `--body <markdown>` | Markdown content |
| `--category <name>` | Category name (must exist in WordPress) |
| `--tags <a,b,c>` | Comma-separated tag names |
| `--seo-keyword <kw>` | Focus keyword for Rank Math / SEOPress |
| `--image-title <text>` | Text overlay on featured image (Pro) |
| `--slug <slug>` | Custom URL slug |
| `--publish` | Publish immediately (default: draft) |
| `--wait` | Wait for job completion and return result |

### posts update flags

| Flag | Description |
|------|-------------|
| `--title <title>` | New post title |
| `--body <markdown>` | New markdown content (replaces all existing content) |
| `--category <name>` | New category name |
| `--tags <a,b,c>` | New comma-separated tag names |
| `--seo-keyword <kw>` | New focus keyword for Rank Math / SEOPress |
| `--slug <slug>` | New URL slug |
| `--publish` | Publish after syncing (default: keep current status) |
| `--wait` | Wait for job completion and return result |

## API Request Body Reference

### PATCH /api/posts/:id (update)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **title** | string | No | New post title |
| **body** | string | No | New markdown content (replaces all existing content on the Notion page) |
| **category** | string | No | New category name |
| **tags** | string[] | No | New tag names |
| **seoKeyword** | string | No | New focus keyword |
| **slug** | string | No | New URL slug |
| **publish** | boolean | No | Publish after syncing |

Returns `{ jobId, postId, message }`. The update writes to Notion first, then triggers a sync job to push changes to WordPress.

### POST /api/posts/create

For curl/HTTP usage, `POST /api/posts/create` accepts:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| **title** | string | Yes | Post title |
| **body** | string | No | Markdown content with headings and paragraphs |
| **category** | string | No | Category name (must exist in WordPress) |
| **tags** | string[] | No | Array of tag names |
| **seoKeyword** | string | No | Focus keyword for Rank Math / SEOPress |
| **imageTitle** | string | No | Text overlay on featured image (Pro) |
| **slug** | string | No | Custom URL slug |
| **publish** | boolean | No | Publish immediately (default: false) |
| **images** | object[] | No | Inline Unsplash images (Pro). Each: `{query, afterHeading}` |

## What Notipo Handles

- Notion page creation from markdown (no Notion credentials needed)
- Markdown → Notion blocks → WordPress Gutenberg block conversion
- Image download from Notion and upload to WordPress media library
- Featured image generation (1200×628 with category background + title overlay)
- Inline Unsplash image insertion by search query (Pro plan)
- SEO metadata — Rank Math, Yoast, SEOPress, AIOSEO
- Post status management in Notion
- Failure notifications via Slack/Discord webhook

## Common Gotchas

1. **Use `posts update` to fix content** — don't delete and recreate. `notipo posts update <id> --body "..."` updates the Notion page and re-syncs to WordPress in one call.
2. **Include all fields for best results** — only `title` is technically required, but AI agents should always generate body, category, tags, seoKeyword, imageTitle, and slug for a complete post.
2. **Category must exist** — the category name must match an existing WordPress category. Fetch valid options first.
3. **`--publish` runs two jobs** — first SYNC_POST (creates draft), then PUBLISH_POST (makes it live). Use `--wait` to block until both complete.
4. **Images require Pro plan** — the `images` array and featured image generation are Pro features. On Free plan, these fields are silently ignored.
5. **Fire and forget** — the API returns a `jobId` immediately. Processing happens in the background. Use `notipo jobs` to check status.
6. **Markdown body format** — use `## Heading` for h2, `### Heading` for h3. Paragraphs are separated by `\n\n`. Images can be included as `![alt](url)`.
8. **Rate limits** — `notipo sync` has a 15-second cooldown. `notipo posts create` has no rate limit.
9. **API key format** — keys start with `ntp_`. Get yours from Settings → Account in the dashboard.
10. **Slug defaults** — if not set, the slug is derived from the SEO keyword. If no SEO keyword, WordPress generates it from the title.
