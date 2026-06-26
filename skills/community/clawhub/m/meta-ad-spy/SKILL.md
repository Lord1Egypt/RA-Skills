---
name: meta-ad-spy
description: >
  Competitive intelligence skill for spying on competitor ads using Meta's Ad Library.
  Use this skill whenever the user wants to: research competitor Facebook/Instagram ads,
  analyze ad strategies, extract ad creatives or copy, find how long ads have been running,
  scout ad spend patterns, monitor industry advertising trends, or build any kind of
  competitor ad intelligence report. Triggers on phrases like "check competitor ads",
  "what ads is [brand] running", "spy on ads", "Facebook ad library", "Meta ad library",
  "scrape ads", "monitor ads", "ad intelligence", "ad research", or any request to
  analyze advertising strategies on Meta platforms. Always use this skill even if the
  user just mentions they want to understand what a competitor is doing on Facebook or Instagram.
---

# Meta Ad Spy — Competitor Ad Intelligence Skill

A two-phase skill for extracting and analyzing competitor ads from Meta platforms.

## Architecture Overview

```
Phase 1: Playwright Scraper (No API key needed)
  └── facebook.com/ads/library → Ad creatives, copy, status, platforms, dates
  
Phase 2: Meta Graph API (Requires access token)
  └── graph.facebook.com/v23.0/ads_archive → Spend ranges, impressions, demographics
  
Analysis Layer: Claude synthesizes insights from both sources
```

---

## PHASE 1: Playwright Scraper

**When to use**: Always as the first step, or when user has no API token.  
**What it gets**: Ad creatives (image/video URLs), ad copy, CTA text, page name, start date, active status, platforms (Facebook/Instagram), ad format (carousel, video, static).  
**What it can't get**: Spend ranges, impressions, demographic breakdown (those need Phase 2).

### Setup

```bash
pip install playwright --break-system-packages
playwright install chromium
pip install asyncio --break-system-packages
```

### Core Playwright Script

Write this to `/tmp/meta_ad_scraper.py`:

```python
import asyncio
import json
import re
import sys
from playwright.async_api import async_playwright

async def scrape_ad_library(
    search_query: str = None,
    page_id: str = None,
    country: str = "ALL",
    ad_type: str = "all",           # all | political_and_issue_ads | housing_ads
    active_status: str = "active",  # active | inactive | all
    media_type: str = "all",        # all | image | meme | video | none
    max_ads: int = 50
) -> list[dict]:
    """
    Scrape Meta Ad Library for competitor ads.
    Either search_query or page_id must be provided.
    """
    results = []

    # Build URL
    base = "https://www.facebook.com/ads/library/?"
    params = {
        "active_status": active_status,
        "ad_type": ad_type,
        "country": country,
        "media_type": media_type,
    }
    if search_query:
        params["q"] = search_query
        params["search_type"] = "keyword_unordered"
    elif page_id:
        params["view_all_page_id"] = page_id
        params["search_type"] = "page"
    
    url = base + "&".join(f"{k}={v}" for k, v in params.items())

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--disable-dev-shm-usage",
            ]
        )
        context = await browser.new_context(
            viewport={"width": 1440, "height": 900},
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            locale="en-US",
        )
        # Stealth: mask webdriver
        await context.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        page = await context.new_page()
        print(f"[Phase 1] Navigating to: {url}")
        await page.goto(url, wait_until="networkidle", timeout=30000)
        await page.wait_for_timeout(3000)

        # Scroll to load more ads
        ads_loaded = 0
        scroll_attempts = 0
        while ads_loaded < max_ads and scroll_attempts < 20:
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(2000)
            # Count ad cards
            ad_cards = await page.query_selector_all('[data-testid="ad-card"], ._7jvw, [class*="x8t9es0"]')
            ads_loaded = len(ad_cards)
            scroll_attempts += 1
            if scroll_attempts % 5 == 0:
                print(f"[Phase 1] Loaded {ads_loaded} ads so far...")

        # Extract ad data via JavaScript
        ads_data = await page.evaluate("""
            () => {
                const ads = [];
                // Meta Ad Library renders ads in divs; extract all visible text/image data
                // Look for ad archive links which contain library IDs
                const links = document.querySelectorAll('a[href*="ads/archive"]');
                const seen_ids = new Set();
                links.forEach(link => {
                    const href = link.href;
                    const id_match = href.match(/id=(\d+)/);
                    if (id_match && !seen_ids.has(id_match[1])) {
                        seen_ids.add(id_match[1]);
                        // Walk up to find the ad container
                        let container = link;
                        for (let i = 0; i < 8; i++) {
                            container = container.parentElement;
                            if (!container) break;
                        }
                        const getText = (el, fallback='') => el ? el.innerText.trim() : fallback;
                        const getAttr = (el, attr, fallback='') => el ? el.getAttribute(attr) || fallback : fallback;
                        
                        ads.push({
                            ad_archive_id: id_match[1],
                            ad_snapshot_url: href,
                            page_name: getText(container?.querySelector('[class*="page-name"], strong')),
                            ad_body: getText(container?.querySelector('[data-ad-preview="message"], [class*="body"]')),
                            ad_title: getText(container?.querySelector('[class*="title"]')),
                            cta_text: getText(container?.querySelector('[class*="cta"], button')),
                            image_url: getAttr(container?.querySelector('img[src*="fbcdn"]'), 'src'),
                            started_running: getText(container?.querySelector('[class*="started-running"]')),
                            platforms: Array.from(container?.querySelectorAll('[class*="platform"]') || []).map(el => el.innerText.trim()).filter(Boolean),
                            raw_text: container?.innerText?.substring(0, 500) || '',
                        });
                    }
                });
                return ads;
            }
        """)
        
        # Also capture network requests for richer data
        print(f"[Phase 1] Extracted {len(ads_data)} ads from DOM")
        results = ads_data[:max_ads]
        
        await browser.close()
    
    return results


async def main():
    query = sys.argv[1] if len(sys.argv) > 1 else "Nike shoes"
    ads = await scrape_ad_library(search_query=query, max_ads=20)
    print(json.dumps(ads, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    asyncio.run(main())
```

### How to Run Phase 1

```bash
python /tmp/meta_ad_scraper.py "competitor brand name"
```

Or from within Python (for page ID lookups):
```python
ads = await scrape_ad_library(page_id="434174436675167", active_status="active")
```

### Filters Available in Phase 1

| Filter | Values | Notes |
|--------|--------|-------|
| `active_status` | `active`, `inactive`, `all` | `active` = currently running |
| `ad_type` | `all`, `political_and_issue_ads`, `housing_ads`, `employment_ads`, `credit_ads` | Default: all |
| `country` | `ALL`, `US`, `IN`, `GB`, `DE`, `FR`, `AU`, etc. | ISO codes |
| `media_type` | `all`, `image`, `meme`, `video`, `none` | Filter by creative format |
| `search_query` | Any keyword string | Brand name, product, keyword |
| `page_id` | Facebook Page ID | More precise than keyword search |

---

## PHASE 2: Meta Graph API

**When to use**: After Phase 1, or when user wants spend/impression/demographic data.  
**Requirements**: Meta developer account + access token (see setup below).  
**What it gets**: Spend ranges, impression ranges, demographic distribution (EU/political), delivery by region, ad creative details, estimated audience size.

### Setup Instructions (tell the user)

1. Go to [Meta for Developers](https://developers.facebook.com/) → Create App
2. Go to [facebook.com/ID](https://www.facebook.com/ID) → Confirm identity (required for spend data)
3. Generate a User Access Token with `ads_read` permission from [Graph API Explorer](https://developers.facebook.com/tools/explorer/)
4. Set as env var: `export META_ACCESS_TOKEN="your_token_here"`

### Core API Script

Write this to `/tmp/meta_ad_api.py`:

```python
import requests
import json
import os
import time
import sys
from typing import Optional

META_API_VERSION = "v23.0"
BASE_URL = f"https://graph.facebook.com/{META_API_VERSION}/ads_archive"

# All available fields from the API
ALL_FIELDS = [
    "id",
    "ad_archive_id", 
    "ad_creative_bodies",
    "ad_creative_link_captions",
    "ad_creative_link_descriptions", 
    "ad_creative_link_titles",
    "ad_delivery_start_time",
    "ad_delivery_stop_time",
    "ad_snapshot_url",
    "bylines",
    "delivery_by_region",
    "demographic_distribution",
    "estimated_audience_size",
    "impressions",
    "page_id",
    "page_name",
    "publisher_platforms",
    "spend",
    "languages",
    "currency",
    "ad_creative_link_caption",
    "ad_creative_link_url",
]

def query_ad_library(
    access_token: str,
    search_terms: str = None,
    search_page_ids: list[str] = None,
    ad_reached_countries: list[str] = ["US"],
    ad_active_status: str = "ACTIVE",     # ACTIVE | INACTIVE | ALL
    ad_type: str = "ALL",                  # ALL | POLITICAL_AND_ISSUE_ADS | etc.
    ad_delivery_date_min: str = None,      # "YYYY-MM-DD"
    ad_delivery_date_max: str = None,      # "YYYY-MM-DD"
    publisher_platforms: list[str] = None, # ["FACEBOOK", "INSTAGRAM"]
    languages: list[str] = None,
    limit: int = 50,
    max_pages: int = 5,
) -> list[dict]:
    """
    Query Meta Ad Library API with full pagination support.
    Returns list of ad objects with all available fields.
    """
    if not access_token:
        raise ValueError("META_ACCESS_TOKEN is required for Phase 2")

    params = {
        "access_token": access_token,
        "ad_active_status": ad_active_status,
        "ad_type": ad_type,
        "ad_reached_countries": json.dumps(ad_reached_countries),
        "fields": ",".join(ALL_FIELDS),
        "limit": min(limit, 500),  # API max per page
    }
    
    if search_terms:
        params["search_terms"] = search_terms
    if search_page_ids:
        params["search_page_ids"] = ",".join(search_page_ids)
    if ad_delivery_date_min:
        params["ad_delivery_date_min"] = ad_delivery_date_min
    if ad_delivery_date_max:
        params["ad_delivery_date_max"] = ad_delivery_date_max
    if publisher_platforms:
        params["publisher_platforms"] = json.dumps(publisher_platforms)
    if languages:
        params["languages"] = json.dumps(languages)

    all_ads = []
    page_count = 0
    next_url = None

    while page_count < max_pages:
        try:
            if next_url:
                response = requests.get(next_url, timeout=30)
            else:
                response = requests.get(BASE_URL, params=params, timeout=30)
            
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                print(f"[Phase 2] API Error: {data['error']}", file=sys.stderr)
                break
            
            ads = data.get("data", [])
            all_ads.extend(ads)
            page_count += 1
            print(f"[Phase 2] Page {page_count}: fetched {len(ads)} ads (total: {len(all_ads)})")
            
            # Pagination
            paging = data.get("paging", {})
            next_url = paging.get("next")
            if not next_url or len(all_ads) >= limit:
                break
            
            time.sleep(1)  # Rate limit courtesy
            
        except requests.exceptions.RequestException as e:
            print(f"[Phase 2] Request error: {e}", file=sys.stderr)
            break

    return all_ads[:limit]


def analyze_ads(ads: list[dict]) -> dict:
    """
    Extract competitive intelligence insights from raw ad data.
    """
    if not ads:
        return {"error": "No ads found"}

    # Spend analysis
    spends = []
    for ad in ads:
        spend = ad.get("spend", {})
        if isinstance(spend, dict):
            lo = spend.get("lower_bound", 0)
            hi = spend.get("upper_bound", 0)
            if lo and hi:
                spends.append({"ad_id": ad.get("ad_archive_id"), "min": int(lo), "max": int(hi), "midpoint": (int(lo)+int(hi))//2})

    # Platform distribution
    platform_counts = {}
    for ad in ads:
        for p in ad.get("publisher_platforms", []):
            platform_counts[p] = platform_counts.get(p, 0) + 1

    # Ad longevity (proxy for performance — longer running = likely working)
    from datetime import datetime
    long_running = []
    for ad in ads:
        start = ad.get("ad_delivery_start_time")
        if start:
            try:
                days = (datetime.now() - datetime.fromisoformat(start.replace("Z",""))).days
                long_running.append({"ad_id": ad.get("ad_archive_id"), "days_running": days, "page": ad.get("page_name")})
            except:
                pass
    long_running.sort(key=lambda x: x["days_running"], reverse=True)

    # Creative format distribution
    creative_bodies = [ad.get("ad_creative_bodies", []) for ad in ads if ad.get("ad_creative_bodies")]
    
    return {
        "total_ads": len(ads),
        "spend_analysis": {
            "ads_with_spend_data": len(spends),
            "estimated_total_min_spend": sum(s["min"] for s in spends),
            "estimated_total_max_spend": sum(s["max"] for s in spends),
            "top_spenders": sorted(spends, key=lambda x: x["midpoint"], reverse=True)[:5],
        },
        "platform_distribution": platform_counts,
        "longest_running_ads": long_running[:10],
        "pages_advertising": list(set(ad.get("page_name") for ad in ads if ad.get("page_name"))),
        "sample_creatives": [
            {
                "page": ad.get("page_name"),
                "body": (ad.get("ad_creative_bodies") or [""])[0][:300],
                "title": (ad.get("ad_creative_link_titles") or [""])[0],
                "platforms": ad.get("publisher_platforms", []),
                "snapshot_url": ad.get("ad_snapshot_url"),
            }
            for ad in ads[:10]
        ]
    }


if __name__ == "__main__":
    token = os.environ.get("META_ACCESS_TOKEN", "")
    search = sys.argv[1] if len(sys.argv) > 1 else "Nike"
    ads = query_ad_library(token, search_terms=search, ad_reached_countries=["US"], limit=50)
    analysis = analyze_ads(ads)
    print(json.dumps(analysis, indent=2, ensure_ascii=False))
    # Also save raw data
    with open("/tmp/meta_ads_raw.json", "w") as f:
        json.dump(ads, f, indent=2, ensure_ascii=False)
    print(f"\n[Phase 2] Raw data saved to /tmp/meta_ads_raw.json")
```

### API Filter Reference

| Parameter | Values | Notes |
|-----------|--------|-------|
| `search_terms` | Any string | Keyword search in ad content |
| `search_page_ids` | List of FB page IDs | Most precise competitor lookup |
| `ad_reached_countries` | `["US"]`, `["IN"]`, `["GB","DE"]` | Required parameter |
| `ad_active_status` | `ACTIVE`, `INACTIVE`, `ALL` | ACTIVE = currently live |
| `ad_type` | `ALL`, `POLITICAL_AND_ISSUE_ADS`, `HOUSING_ADS`, `EMPLOYMENT_ADS`, `FINANCIAL_SERVICES` | Filter by category |
| `ad_delivery_date_min` | `"2024-01-01"` | Start of date range |
| `ad_delivery_date_max` | `"2024-12-31"` | End of date range |
| `publisher_platforms` | `["FACEBOOK"]`, `["INSTAGRAM"]`, `["FACEBOOK","INSTAGRAM"]` | Platform filter |
| `languages` | `["en"]`, `["hi"]`, `["es"]` | Language codes |

### Data Fields Available from API

**Always available (all ads):**
- `ad_archive_id` — Unique ad ID
- `page_id`, `page_name` — Advertiser page
- `ad_creative_bodies` — Ad copy text(s)
- `ad_creative_link_titles`, `ad_creative_link_descriptions` — Headlines
- `ad_delivery_start_time`, `ad_delivery_stop_time` — Run dates
- `publisher_platforms` — FB/Instagram/Messenger/Audience Network
- `ad_snapshot_url` — Link to view the actual ad

**EU/UK/Political ads only:**
- `spend` — `{lower_bound, upper_bound, currency}` — Spend RANGE, not exact
- `impressions` — `{lower_bound, upper_bound}` — Impression RANGE
- `estimated_audience_size` — `{lower_bound, upper_bound}`
- `demographic_distribution` — `[{age, gender, percentage}]` array
- `delivery_by_region` — Geographic breakdown
- `bylines` — "Paid for by" disclaimer

> ⚠️ **Important**: Spend and impressions are RANGES, not exact numbers. For non-EU/non-political ads in most countries including US and India, spend/impression data will NOT be returned. The official API is primarily a transparency tool. For richer commercial ad data, see the third-party alternatives in `references/alternatives.md`.

---

## ANALYSIS WORKFLOW

When a user wants competitor ad intelligence, follow this flow:

### Step 1 — Clarify the Target

Ask (or infer from context):
- **Who** — brand name OR Facebook Page ID (better)
- **Where** — country/region (`US`, `IN`, `ALL`, etc.)
- **What** — active only, or historical too?
- **Goal** — creative inspiration, spend monitoring, format analysis, copy patterns?

### Step 2 — Find the Page ID (if only brand name given)

```bash
# Tell user to visit: https://www.facebook.com/ads/library/?q=BRAND_NAME
# The page_id appears in the URL when clicking on a page
# OR use the search API:
curl "https://graph.facebook.com/v23.0/pages/search?q=BRAND_NAME&access_token=TOKEN"
```

### Step 3 — Run Phase 1 (Playwright)

Always run Phase 1 first. Write and execute `/tmp/meta_ad_scraper.py`.

### Step 4 — Run Phase 2 (API), if token available

Check for `META_ACCESS_TOKEN` env var. If present, run Phase 2.
If missing, tell user what Phase 2 would add, and give setup instructions.

### Step 5 — Synthesize & Report

Produce a structured competitive intelligence report covering:

```
## 🕵️ Competitor Ad Intelligence Report: [Brand Name]

### 1. Current Ad Activity
- How many ads active right now
- Platforms being used (FB vs Instagram split)
- Ad formats (video, image, carousel)

### 2. Creative Strategy Analysis  
- Common themes in ad copy
- CTA patterns (Shop Now, Learn More, Sign Up, etc.)
- Headline formulas being used
- Hook styles (question, statement, social proof, urgency)

### 3. Ad Longevity Signals
- Longest-running ads (strong = likely performing well)
- New ads launched recently (testing phase)

### 4. Spend & Scale Signals (Phase 2 only, EU/political)
- Estimated spend ranges
- Impression volume estimates
- Geographic distribution

### 5. Audience Signals (Phase 2 EU only)
- Age/gender demographic breakdown
- Platform delivery split

### 6. Strategic Recommendations
- Gaps in competitor's strategy you can exploit
- Formats/messages they're NOT using
- High-performing creative patterns to draw inspiration from
```

---

## COMMON WORKFLOWS

### "What ads is [Brand] running right now?"

```python
# Phase 1
ads = await scrape_ad_library(search_query="Brand Name", active_status="active")

# Phase 2 (if token available)
ads_api = query_ad_library(token, search_terms="Brand Name", ad_active_status="ACTIVE")
```

### "Show me competitor video ads in India"

```python
ads = await scrape_ad_library(
    search_query="competitor name",
    country="IN",
    media_type="video",
    active_status="active"
)
```

### "How much is [Brand] spending on ads?" (EU/political only)

```python
ads = query_ad_library(
    token,
    search_terms="Brand",
    ad_reached_countries=["GB"],  # or EU countries
    ad_type="ALL",
)
analysis = analyze_ads(ads)
# Look at analysis["spend_analysis"]
```

### "Show me ads that have been running the longest" (= likely winners)

```python
ads = query_ad_library(token, search_terms="Brand", ad_active_status="ALL")
analysis = analyze_ads(ads)
# analysis["longest_running_ads"] — sorted by days running
```

### "Find ads about [topic/product keyword]"

```python
ads = await scrape_ad_library(search_query="keyword phrase", active_status="all")
```

---

## LIMITATIONS & WORKAROUNDS

| Limitation | Workaround |
|------------|------------|
| Spend data only for EU/political | Target EU countries in API query |
| No CTR/conversion data | Use ad longevity as performance proxy |
| Phase 1 DOM selectors may break | Fall back to raw text extraction + Claude analysis |
| Rate limits on API | Add `time.sleep(1)` between pages, use cursor pagination |
| Max ~429 ads per API session | Run multiple targeted queries, filter by date ranges |
| No exact targeting info | Infer from demographic distribution (EU only) |

---

## NOTES ON LEGALITY & ETHICS

- The Meta Ad Library is **public data** — no login required for commercial ads
- Using it for competitive research is explicitly Meta's stated purpose for the tool
- The official API is a **transparency tool** — use it as intended
- Playwright scraping of public pages is generally legal (ref: hiQ v. LinkedIn, 2022)
- Do NOT attempt to scrape user data, private profiles, or non-public content
- Always respect rate limits and avoid aggressive scraping

---

## SEE ALSO

- `references/alternatives.md` — Third-party APIs with richer data (SearchAPI.io, AdLibrary.com)
- `references/page_id_lookup.md` — How to find competitor Facebook Page IDs
- `references/field_reference.md` — Complete API field reference
