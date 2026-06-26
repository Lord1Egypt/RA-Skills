---
name: markdown.new-crawl
description: Use `https://markdown.new/crawl/{target_url}` endpoints to recursively crawl a site section and return markdowns. Trigger this skill when the user asks for multi-page extraction, whole-docs crawl, link-depth crawling, or job-based crawl polling from a URL. Prefer local terminal access (`curl`) with `/crawl`, `/crawl/status/{jobId}`, and `/crawl/{url}` before other browsing methods.
---

## Markdown.New Crawl Local-First Access

Use `markdown.new/crawl` for multi-page crawling and async Markdown generation.

### Required Behavior

1. Prefer local API calls with `curl` (or any suitable alternative tools).
2. Assume no authentication is required unless the service behavior changes.
3. Start with `POST /crawl` to get a job ID.
4. Poll `GET /crawl/status/{jobId}` until crawl completes.
5. Default to Markdown output; use `?format=json` only when structured output is needed.
6. Keep crawl scope explicit (`limit`, `depth`, subdomain/external toggles, include/exclude patterns).
7. State default crawl behavior: same-domain links only, up to `500` pages per job.
8. If `/crawl` fails (network, timeout, blocked host), fall back to another method and state the fallback.

### Core Commands

```sh
curl -X POST "https://markdown.new/crawl" \
  -H "Content-Type: application/json" \
  -d '{"url":"https://docs.example.com","limit":50}'
```

```sh
curl "https://markdown.new/crawl/status/<jobId>"
```

```sh
curl "https://markdown.new/crawl/status/<jobId>?format=json"
```

```sh
curl "https://markdown.new/crawl/https://docs.example.com"
```

```sh
curl -X DELETE "https://markdown.new/crawl/status/<jobId>"
```

### API Coverage

- `POST /crawl`: create async crawl job and return job ID.
- `GET /crawl/status/{jobId}`: return crawl output and status.
- `DELETE /crawl/status/{jobId}`: cancel a running crawl; completed pages remain available.
- `GET /crawl/{url}`: browser-style shortcut that starts crawl and returns tracking page.

### Common Crawl Options

- `url` (required): crawl starting URL.
- `limit`: max pages, `1-500` (default `500`).
- `depth`: max link depth, `1-10` (default `5`).
- `render`: enable JS rendering for SPA pages.
- `source`: URL discovery strategy (`all`, `sitemaps`, `links`).
- `maxAge`: max cache age seconds (`0-604800`, default `86400`).
- `modifiedSince`: UNIX timestamp; crawl pages modified after this time.
- `includeExternalLinks`: include cross-domain links.
- `includeSubdomains`: include subdomains.
- `includePatterns` / `excludePatterns`: wildcard URL filtering.

### Output Notes

- `GET /crawl/status/{jobId}` returns concatenated Markdown by default.
- Add `?format=json` for per-page structured records.
- Images are stripped by default; add `?retain_images=true` to keep them.
- Results are retained for 14 days; expired job IDs return errors.

### Operational Limits

- Rate model (as documented in the crawl page FAQ): each crawl costs 50 units against a 500 daily limit (about 10 crawls/day).
- Prefer lower `limit` values for targeted extraction to reduce cost and runtime.
