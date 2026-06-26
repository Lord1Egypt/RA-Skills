# Meta Ad Library API — Complete Field Reference

Endpoint: `GET https://graph.facebook.com/v23.0/ads_archive`

## Search Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `access_token` | string | ✅ | Your Meta Graph API access token |
| `search_terms` | string | ⚠️ | Keyword to search. Either this or search_page_ids required |
| `search_page_ids` | string | ⚠️ | Comma-separated page IDs. Most precise method |
| `ad_reached_countries` | JSON array | ✅ | e.g. `["US"]`, `["IN","PK"]`, `["ALL"]` |
| `ad_active_status` | enum | — | `ACTIVE`, `INACTIVE`, `ALL`. Default: ALL |
| `ad_type` | enum | — | `ALL`, `POLITICAL_AND_ISSUE_ADS`, `HOUSING_ADS`, `EMPLOYMENT_ADS`, `FINANCIAL_SERVICES` |
| `ad_delivery_date_min` | date | — | Format: `"2024-01-01"` |
| `ad_delivery_date_max` | date | — | Format: `"2024-12-31"` |
| `publisher_platforms` | JSON array | — | `["FACEBOOK"]`, `["INSTAGRAM"]`, `["MESSENGER"]`, `["AUDIENCE_NETWORK"]` |
| `languages` | JSON array | — | `["en"]`, `["hi"]`, `["es"]` |
| `limit` | int | — | Ads per page. Max practical: 429 |
| `after` | string | — | Pagination cursor from previous response |

## Response Fields

### Core Fields (All Ads)

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Internal graph node ID |
| `ad_archive_id` | string | Ad Library unique ID |
| `page_id` | string | Advertiser's Facebook page ID |
| `page_name` | string | Advertiser's page name |
| `ad_creative_bodies` | array[string] | Ad copy text(s) — array because carousel has multiple |
| `ad_creative_link_titles` | array[string] | Headline text(s) |
| `ad_creative_link_descriptions` | array[string] | Description text(s) |
| `ad_creative_link_captions` | array[string] | Caption/domain shown |
| `ad_delivery_start_time` | datetime | When ad started running (ISO 8601) |
| `ad_delivery_stop_time` | datetime | When ad stopped (null if still active) |
| `ad_snapshot_url` | string | URL to view the ad creative |
| `publisher_platforms` | array[string] | `["FACEBOOK", "INSTAGRAM"]` etc. |
| `languages` | array[string] | Content language codes |
| `currency` | string | Currency code (e.g., "USD") |
| `bylines` | array[string] | "Paid for by" info (usually political ads) |

### Restricted Fields (EU/UK/Political Ads Only)

| Field | Type | Description |
|-------|------|-------------|
| `spend` | object | `{lower_bound, upper_bound, currency}` — RANGE not exact |
| `impressions` | object | `{lower_bound, upper_bound}` — RANGE not exact |
| `estimated_audience_size` | object | `{lower_bound, upper_bound}` |
| `demographic_distribution` | array | `[{age: "18-24", gender: "male", percentage: 0.25}]` |
| `delivery_by_region` | array | `[{region: "California", percentage: 0.3}]` |

## Spend Range Interpretation

Meta returns spend as broad buckets. Here's how to interpret:
- `lower: 0, upper: 100` → Very small test ad
- `lower: 100, upper: 499` → Small campaign
- `lower: 500, upper: 999` → Modest campaign
- `lower: 1000, upper: 4999` → Serious campaign
- `lower: 5000, upper: 9999` → Significant campaign
- `lower: 10000, upper: 49999` → Large campaign
- `lower: 50000, upper: 99999` → Major campaign
- `lower: 100000, upper: null` → Enterprise spend

## Ad Longevity as Performance Proxy

Since CTR/conversions aren't available, days-running is the best signal:
- **1-7 days**: New test / launch
- **7-30 days**: Scaling or testing
- **30-90 days**: Working well, being iterated
- **90+ days**: Proven winner, "evergreen" creative
- **180+ days**: Core brand asset, very high confidence

## Rate Limits

Meta doesn't publish exact limits. Practical guidance:
- ~200 requests/hour per token (conservative estimate)
- Add 1-2 second delays between paginated requests
- For large pulls, spread across multiple hours
- If you get error code 32 or 17, back off for 15-30 min
