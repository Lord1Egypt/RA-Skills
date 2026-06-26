# Third-Party Alternatives to Meta's Official API

The official Meta Ad Library API has significant limitations for commercial ad research
(no spend data for non-EU ads, no impressions, no CTR). These alternatives fill the gap.

## 1. SearchAPI.io — Meta Ad Library API

**URL**: https://www.searchapi.io/docs/meta-ad-library-api  
**Best for**: Full ad data without token verification hassle  
**Cost**: 100 free requests, then paid plans

```python
import requests

def searchapi_query(api_key: str, page_id: str = None, query: str = None, country: str = "ALL"):
    params = {
        "engine": "meta_ad_library",
        "api_key": api_key,
        "ad_type": "all",
        "active_status": "active",
        "country": country,
        "media_type": "all",
    }
    if page_id:
        params["page_id"] = page_id
    if query:
        params["q"] = query
        params["search_type"] = "keyword_unordered"

    response = requests.get("https://www.searchapi.io/api/v1/search", params=params)
    return response.json()

# Also supports ad details (EU transparency data):
def searchapi_ad_details(api_key: str, ad_archive_id: str, page_id: str, country: str = "GB"):
    params = {
        "engine": "meta_ad_library_ad_details",
        "api_key": api_key,
        "ad_archive_id": ad_archive_id,
        "page_id": page_id,
        "country": country,
    }
    response = requests.get("https://www.searchapi.io/api/v1/search", params=params)
    return response.json()
    # Returns: eu_transparency, uk_transparency, age_country_gender_reach_breakdown
```

**Returns**:
- `ads[].snapshot.body.text` — Ad copy
- `ads[].snapshot.cards[].cta_text` — CTA
- `ads[].snapshot.cards[].link_url` — Landing page URL
- `ads[].is_active` — Whether ad is live
- `ads[].start_date`, `ads[].end_date` — Run dates
- `ads[].publisher_platform` — Platforms
- `ads[].page_name`, `ads[].page_id`

## 2. AdLibrary.com API

**URL**: https://adlibrary.com  
**Best for**: Richest commercial ad data, built for marketers  
**Has**: Engagement proxies, more creative metadata, landing page data

## 3. Apify Facebook Ads Library Scraper

**URL**: https://apify.com/shahzeb-king/facebook-ads-scraper  
**Best for**: High-volume batch scraping  
**Cost**: ~$0.50-0.75 per 1,000 ads  
**Uses**: Playwright under the hood, runs on Apify cloud

## 4. Bright Data / Data365 Social Media API

**URL**: https://data365.co  
**Best for**: Enterprise-scale, adds public reactions/comments/profile data  
**Has**: Real-time + historical, 99.9% uptime SLA

## When to Suggest Each

| User Need | Recommend |
|-----------|-----------|
| Free, quick research | Official API (Phase 2) + Playwright (Phase 1) |
| Richer data, willing to pay | SearchAPI.io |
| Bulk scraping at scale | Apify |
| Enterprise / agency use | Bright Data or AdLibrary.com |
| EU transparency data | SearchAPI.io ad_details endpoint |
