---
name: index-now
description: Submit URLs for instant indexing via IndexNow (Bing, Yandex, Naver, Seznam) and Google Indexing API. Generate API keys, submit sitemaps, and check indexing status.
---

# index-now

Instantly submit URLs for indexing across search engines using IndexNow protocol and Google Indexing API.

## Capabilities

- **Submit URLs to IndexNow** — Instantly notify Bing, Yandex, Naver, Seznam about new or updated pages
- **Submit to Google Indexing API** — Request fast crawling from Google (requires service account)
- **Submit entire sitemaps** — Parse sitemap XML and submit all URLs at once
- **Generate API keys** — Create IndexNow API keys and verification files
- **Check indexing status** — See when Google last received indexing notifications

## IndexNow Setup

IndexNow requires two things:
1. An API key (any UUID string)
2. A verification file at your domain root (`https://yourdomain.com/{key}.txt`)

### Generate a key:
```bash
# Generate a UUID
uuidgen
# Example: a1b2c3d4-e5f6-7890-abcd-ef1234567890

# Create verification file
echo "a1b2c3d4-e5f6-7890-abcd-ef1234567890" > public/a1b2c3d4-e5f6-7890-abcd-ef1234567890.txt
```

## How to Submit URLs

### IndexNow (Bing, Yandex, Naver, Seznam)
When asked to submit URLs for indexing:
1. User needs an IndexNow API key (help them generate one if they don't have one)
2. Submit to all engines simultaneously using the IndexNow API
3. Report results per engine

### Google Indexing API
Requires a Google Cloud service account with Indexing API enabled:
1. Create a service account in Google Cloud Console
2. Enable the Indexing API
3. Add the service account email as an owner in Google Search Console
4. Generate an access token

## Supported Engines

| Engine | Protocol | Daily Limit |
|--------|----------|-------------|
| Bing | IndexNow | Unlimited |
| Yandex | IndexNow | Unlimited |
| Naver | IndexNow | Unlimited |
| Seznam | IndexNow | Unlimited |
| Google | Indexing API | 200 URLs/day (default) |

## Common Use Cases

- After publishing new blog posts or pages
- After updating existing content
- After a site migration (submit all new URLs)
- After fixing SEO issues (request re-crawl)
- Submitting an entire sitemap for a new site

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | OK — URLs submitted successfully |
| 202 | Accepted — URLs queued for processing |
| 400 | Bad request — check URL format |
| 403 | Forbidden — API key doesn't match host |
| 422 | Unprocessable — URLs don't belong to host |
| 429 | Rate limited — try again later |
