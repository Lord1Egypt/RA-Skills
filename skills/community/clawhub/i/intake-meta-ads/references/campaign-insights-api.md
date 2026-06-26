# Campaign Insights API Reference

## Overview

The Meta Marketing API Insights endpoint (`/act_{AD_ACCOUNT_ID}/insights`) provides campaign performance data — the same data you see in Ads Manager but accessible programmatically. This skill bundles `scripts/meta_campaign_insights.py` to export this data.

**API Docs:**
- https://developers.facebook.com/docs/marketing-api/insights
- https://developers.facebook.com/docs/marketing-api/reference/ad-account/insights

## ⚠️ Authentication Required

Before running the script, ask the user for TWO things:

1. **Access Token** — with `ads_read` permission. Get at https://developers.facebook.com/tools/accesstoken/
2. **Ad Account ID** — format `act_123456789`. Found in Ads Manager → Account Overview, or Business Settings → Ad Accounts.

Prompt the user:
> "To export your campaign data, I need two things:
> 1. Your Meta access token (get one at https://developers.facebook.com/tools/accesstoken/ — ensure it has `ads_read` permission)
> 2. Your Ad Account ID (format: `act_123456789`, found in Ads Manager settings)
> Please provide both so I can pull your campaign insights."

## Requirements

```bash
pip install requests
```

## Script Usage

### Basic Usage

```bash
# Default: last 30 days, campaign level, CSV output
python scripts/meta_campaign_insights.py \
  -t YOUR_ACCESS_TOKEN \
  -a act_123456789

# Last 7 days, ad set level
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --date-preset last_7d \
  --level adset \
  -o adset_performance.csv

# Custom date range, ad level, daily breakdown
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --since 2025-01-01 \
  --until 2025-01-31 \
  --level ad \
  --time-increment 1 \
  -o daily_ad_data.csv

# With demographic breakdowns
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --level adset \
  --breakdowns age,gender \
  -o demographics.csv

# Platform breakdown (Facebook vs Instagram vs Audience Network)
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --level campaign \
  --breakdowns publisher_platform \
  -o platform_performance.csv

# JSON output instead of CSV
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --format json \
  -o insights.json

# Custom fields
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --fields impressions,spend,actions,purchase_roas,website_purchase_roas,cost_per_action_type \
  -o roas_report.csv

# Only active campaigns, sorted by spend
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --filtering '[{"field":"campaign.effective_status","operator":"IN","value":["ACTIVE"]}]' \
  --sort spend_descending \
  -o active_campaigns.csv

# Match Ads Manager attribution settings
python scripts/meta_campaign_insights.py \
  -t YOUR_TOKEN \
  -a act_123456789 \
  --use-unified-attribution \
  -o matched_to_ads_manager.csv
```

### All CLI Arguments

| Argument | Description |
|---|---|
| `-t`, `--access-token` | **Required.** Meta API access token |
| `-a`, `--account-id` | **Required.** Ad account ID (act_XXXXX) |
| `--level` | `account`, `campaign`, `adset`, `ad` (default: campaign) |
| `--fields` | Comma-separated fields (default: smart per-level selection) |
| `--date-preset` | Predefined range: `last_7d`, `last_30d`, `this_month`, `last_month`, `last_90d`, `maximum` (37 months max), etc. |
| `--since` | Start date YYYY-MM-DD (use with --until) |
| `--until` | End date YYYY-MM-DD (use with --since) |
| `--time-increment` | `1` (daily), `7` (weekly), `monthly`, or any N (1-90 days) |
| `--breakdowns` | Comma-separated: `age`, `gender`, `country`, `region`, `publisher_platform`, `platform_position`, `device_platform`, etc. |
| `--filtering` | JSON filter array for status, labels, etc. |
| `--sort` | Sort field: `spend_descending`, `impressions_ascending`, etc. |
| `--action-attribution-windows` | Attribution windows: `1d_click,7d_click,1d_view` |
| `-o`, `--output` | Output file path (default: meta_insights_export.csv) |
| `--format` | `csv` or `json` (default: csv) |
| `--no-summary` | Skip the summary printout |
| `--no-flatten` | Keep action fields as nested JSON (don't split into columns) |
| `--use-unified-attribution` | Match Ads Manager attribution behavior |

## Available Fields (Most Important)

### Core Performance
- `impressions` — Times ad was on screen
- `reach` — Unique accounts that saw ad (estimated)
- `frequency` — Average times each person saw ad (estimated)
- `clicks` — All clicks on ad
- `cpc` — Average cost per click
- `cpm` — Cost per 1,000 impressions
- `ctr` — Click-through rate (%)
- `spend` — Total amount spent (estimated)

### Conversion & Revenue
- `actions` — All conversion actions (list broken down by action_type)
- `action_values` — Total value of all conversions
- `cost_per_action_type` — Cost per each action type
- `conversions` — Conversion actions
- `cost_per_conversion` — Cost per conversion
- `purchase_roas` — Return on ad spend from all purchases
- `website_purchase_roas` — ROAS from website purchases only
- `mobile_app_purchase_roas` — ROAS from app purchases only

### Campaign Identity
- `campaign_id`, `campaign_name` — Campaign identifiers
- `adset_id`, `adset_name` — Ad set identifiers
- `ad_id`, `ad_name` — Ad identifiers
- `account_id`, `account_name` — Account identifiers
- `objective` — Campaign objective
- `optimization_goal` — Ad set optimization goal

### Engagement
- `inline_link_clicks` — Link clicks (1-day click attribution)
- `inline_post_engagement` — Post engagements (1-day click)
- `outbound_clicks` — Clicks leaving Meta properties
- `social_spend` — Spend on ads shown with social info

### Video
- `video_play_actions` — Video plays started
- `video_p25_watched_actions` — Plays at 25%
- `video_p50_watched_actions` — Plays at 50%
- `video_p75_watched_actions` — Plays at 75%
- `video_p100_watched_actions` — Plays at 100%
- `video_avg_time_watched_actions` — Average watch time
- `video_30_sec_watched_actions` — 30-second views

### Cost Metrics
- `cost_per_inline_link_click` — Cost per link click
- `cost_per_inline_post_engagement` — Cost per engagement
- `cost_per_outbound_click` — Cost per outbound click
- `cost_per_unique_click` — Cost per unique click (estimated)
- `cost_per_thruplay` — Cost per ThruPlay (in development)

### Other Useful
- `date_start`, `date_stop` — Report date range
- `buying_type` — Auction, reserved, etc.
- `attribution_setting` — Attribution window applied
- `canvas_avg_view_percent` — Instant Experience avg view %
- `canvas_avg_view_time` — Instant Experience avg time (seconds)
- `qualifying_question_qualify_answer_rate` — Lead ad qualify rate

## Available Breakdowns

### Demographics
- `age` — Age ranges
- `gender` — Male, Female, Unknown

### Geography
- `country` — Country code
- `region` — Region/state
- `dma` — Designated Market Area (US)

### Platform & Placement
- `publisher_platform` — Facebook, Instagram, Messenger, Audience Network
- `platform_position` — Feed, Stories, Reels, etc.
- `device_platform` — Mobile, Desktop
- `impression_device` — Specific device type (must combine with another breakdown)

### Creative
- `ad_format_asset`, `body_asset`, `image_asset`, `video_asset`, `title_asset`, `description_asset`, `link_url_asset`

### Time
- `hourly_stats_aggregated_by_advertiser_time_zone`
- `hourly_stats_aggregated_by_audience_time_zone`

**Note:** Not all breakdowns can be combined. See Meta docs for valid combinations.

## How Actions Are Flattened in CSV

The `actions` field returns a list like:
```json
[
  {"action_type": "link_click", "value": "150"},
  {"action_type": "landing_page_view", "value": "120"},
  {"action_type": "lead", "value": "15"},
  {"action_type": "purchase", "value": "5"}
]
```

The script automatically flattens these into separate columns:
```
actions:link_click | actions:landing_page_view | actions:lead | actions:purchase
150                | 120                       | 15           | 5
```

Same for `cost_per_action_type`, `action_values`, and other action-typed fields. Use `--no-flatten` to keep as raw JSON.

## Common Action Types

| Action Type | Description |
|---|---|
| `link_click` | Link clicks |
| `landing_page_view` | Landing page views (page fully loaded) |
| `post_engagement` | All post interactions |
| `page_engagement` | Page-level engagement |
| `lead` | Lead form submissions |
| `purchase` | Purchase conversions |
| `add_to_cart` | Add to cart events |
| `initiate_checkout` | Checkout initiated |
| `complete_registration` | Registrations completed |
| `view_content` | Content/product views |
| `search` | Search events |
| `onsite_conversion.messaging_first_reply` | First Messenger replies |
| `video_view` | 3-second video views |
| `comment` | Post comments |
| `like` | Reactions |
| `share` | Shares |

## Error Handling

The script handles common errors:

| Error Code | Meaning | Script Behavior |
|---|---|---|
| 190 | Invalid/expired token | Stops, suggests regenerating token |
| 200 | Permission error | Stops, suggests ads_read permission |
| 613 / 17 | Rate limited | Waits 60 seconds, retries |
| 3018 | Date range > 37 months | Stops, suggests shorter range |
| 100 | Invalid parameter | Stops, shows error message |

## Tips for Best Results

1. **Start with campaign level** to get the overview, then drill into adset/ad level for specifics
2. **Use `--time-increment 1`** for daily data — essential for spotting trends and anomalies
3. **Use `--use-unified-attribution`** if you want numbers that match Ads Manager exactly
4. **The `maximum` date preset** returns up to 37 months of data (the lifetime maximum)
5. **Break large queries** into smaller date ranges if you get timeouts
6. **Unique metrics** (reach, unique_clicks, etc.) are expensive to compute — query separately if other metrics time out
7. **June 2025 change:** `use_unified_attribution_setting` and `action_report_time` are being phased out; API will mimic Ads Manager settings by default
