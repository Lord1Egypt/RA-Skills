---
name: phoenix-scraper
description: "Resilient multi-layer web scraper with automatic failover. Use when scraping web content that may be JS-rendered, behind bot protection, or on sites that block standard HTTP requests. Supports three-tier failover chain: Brave Search API, then Bright Data Web Unlocker (with optional browser render mode), then Playwright headless browser. Use for job boards (LinkedIn, Glassdoor, Reed, Indeed, CWJobs, TotalJobs), social media monitoring (X/Twitter via API v2), news sites, and any page requiring JS rendering. Includes zone routing logic for Bright Data (web_unlocker vs job_search_scraper zones)."
---

# Phoenix Scraper

Resilient three-tier failover scraper. Never returns empty — if one method fails, the next activates automatically.

## Failover Chain

```
Tier 1: Brave Search API (fast, free tier, 2k req/month)
    ↓ (on block/empty/timeout)
Tier 2: Bright Data Web Unlocker (residential proxy, JS-render optional)
    ↓ (on block/429/timeout)
Tier 3: Playwright headless browser (full JS execution)
```

## Quick Start

```python
from scripts.phoenix_scraper import scrape

# Basic fetch
result = scrape("https://example.com/page")

# With JS rendering (for SPA/dynamic sites)
result = scrape("https://example.com/page", render_js=True)

# With specific Bright Data zone
result = scrape("https://linkedin.com/jobs/...", zone="job_search_scraper")
```

## Zone Routing

| Use Case | Zone |
|----------|------|
| Job boards (LinkedIn, Glassdoor, Reed, Indeed) | `job_search_scraper` |
| Social media, news, general web | `web_unlocker` |
| X.com / Twitter | Use X API v2 (see references/x-api.md) |

## Bright Data render_js

Set `render_js=True` for JS-heavy sites (CWJobs, TotalJobs, ContractorUK). Adds `"render": True` (boolean) to payload and uses 60s timeout.

**Critical:** Use boolean `True`, not string `"html"` — Bright Data validation rejects strings.

## Bright Data Premium Domains (Cost Note)

LinkedIn, Glassdoor, and other heavily-protected job boards may be classified as **Premium Domains** in your Bright Data zone (updated quarterly). API call syntax is identical — but cost per request is higher. Check your zone's Premium Domains list if costs spike unexpectedly.

## Playwright Stealth (2026 Enhancement)

For Tier 3, consider installing `playwright-stealth` to patch headless browser fingerprints — reduces detection on Cloudflare/advanced bot-protected sites:

```bash
pip install playwright-stealth
```

```python
# Optional enhancement in phoenix_scraper.py Tier 3:
from playwright_stealth import stealth_sync
stealth_sync(page)
```

The base Playwright tier works without this, but stealth patching significantly improves success rates on heavily protected sites (Coupang, Naver, etc.) as of 2026.

## URL Formatting

- CWJobs/TotalJobs: use hyphen-slugs — `finance-systems-consultant` NOT `finance+systems+consultant`
- Glassdoor: `https://www.glassdoor.co.uk/Job/united-kingdom-{slug}-jobs-SRCH_IL.0,14_IN2_KO15,{end}.htm`

## Environment Variables

```bash
BRIGHT_DATA_API_KEY=<key>          # Bright Data API key
BRIGHT_DATA_ZONE=job_search_scraper # Default zone (override per-call)
BRAVE_API_KEY=<key>                # Brave Search API key
X_BEARER_TOKEN=<token>             # X API v2 bearer token (for X.com)
```

## X.com Monitoring

For X/Twitter, use X API v2 (not scraping). See `references/x-api.md` for endpoint details and rate limits.

## Error Handling

All tiers log failures before escalating. On total failure, returns `{"success": False, "html": "", "method": "all_failed", "error": "<reason>"}`.

Never raises exceptions — always returns a result dict.
