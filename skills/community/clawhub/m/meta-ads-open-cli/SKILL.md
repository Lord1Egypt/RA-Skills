---
name: meta-ads-open-cli
description: >
  Meta Ads data analysis and reporting via meta-ads-open-cli.
  Use when the user wants to check Meta/Facebook/Instagram ad performance, pull campaign/ad set/ad stats,
  explore ad account structure, inspect creatives, analyze audiences, check pixel events, or retrieve lead form submissions.
  Triggers: "Meta Ads", "Facebook Ads", "Instagram Ads", "meta ad performance", "meta campaign stats",
  "meta ad spend", "meta insights", "meta pixel", "meta audience", "meta lead forms", "meta creatives",
  "Facebook ad account", "ad set performance", "meta breakdowns".
---

# Meta Ads CLI Skill

You have access to `meta-ads-open-cli`, a read-only CLI for the Meta Marketing API (Graph API v24.0). Use it to query ad accounts, pull performance insights, inspect creatives, analyze audiences, and retrieve lead form submissions across Facebook, Instagram, Messenger, and Audience Network.

## Quick start

```bash
# Check if the CLI is available
meta-ads-open-cli --help

# Get authenticated user info
meta-ads-open-cli me

# List accessible ad accounts
meta-ads-open-cli ad-accounts
```

If the CLI is not installed, install it:

```bash
npm install -g meta-ads-open-cli
```

## Authentication

The CLI requires a Meta **OAuth access token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `META_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/meta-ads-open-cli/credentials.json`

Required permissions depend on the commands used:
- `ads_read` -- read ad accounts and campaigns
- `ads_management` -- required for some read endpoints (e.g., ad-specific fields on leads)
- `pages_read_engagement` -- read Pages data
- `leads_retrieval` -- read lead gen form submissions
- `business_management` -- read business accounts

Before running any command, verify credentials are configured by running `meta-ads-open-cli me`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Business Manager
 +-- Ad Account (act_XXXXX)
      +-- Campaign
      |    +-- Ad Set
      |         +-- Ad -> Creative
      +-- Custom Audience
      +-- Meta Pixel
      +-- Custom Conversion
```

Ad account IDs use the `act_` prefix (e.g., `act_123456789`). The CLI accepts both `act_XXXXX` and plain numeric IDs.

## Monetary values

**Insights API** (`spend` field): returned as a decimal string in the major currency unit (e.g., `"12.34"` means $12.34). No conversion needed.

**Management API** (`daily_budget`, `lifetime_budget`, `bid_amount`): returned as integers in the smallest currency unit (cents). Divide by 100 for the actual amount.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Pagination uses cursor-based `--after` values from `paging.cursors.after` in the response.

## Commands reference

### Account discovery

```bash
# Authenticated user info
meta-ads-open-cli me

# List ad accounts
meta-ads-open-cli ad-accounts
meta-ads-open-cli ad-accounts --limit 50

# Get a specific ad account
meta-ads-open-cli ad-account act_123456789
meta-ads-open-cli ad-account 123456789

# List users with access to an ad account (--business is required)
meta-ads-open-cli account-users 123456789 --business 9876543210

# List businesses
meta-ads-open-cli businesses
```

### Campaign hierarchy

```bash
# Campaigns (filter by status: ACTIVE, PAUSED, ARCHIVED, DELETED)
meta-ads-open-cli campaigns 123456789
meta-ads-open-cli campaigns 123456789 --status ACTIVE

# Get a specific campaign
meta-ads-open-cli campaign 23851234567890

# Ad sets (filter by campaign, status)
meta-ads-open-cli adsets 123456789
meta-ads-open-cli adsets 123456789 --campaign 23851234567890 --status ACTIVE

# Get a specific ad set
meta-ads-open-cli adset 23851234567891

# Ads (filter by ad set, status)
meta-ads-open-cli ads 123456789
meta-ads-open-cli ads 123456789 --adset 23851234567891

# Get a specific ad
meta-ads-open-cli ad 23851234567892
```

All listing commands support `--limit <n>` (default 100). Most also support `--after <cursor>` for cursor-based pagination, except: `account-users`, `businesses`, `pixels`, `custom-conversions`, `pages`, and `lead-forms`.

### Creatives

```bash
# List ad creatives for an account
meta-ads-open-cli creatives 123456789

# Get a specific creative (includes asset_feed_spec)
meta-ads-open-cli creative 23851234567893
```

### Performance insights

The `insights` command is the primary tool for performance analysis. It works on any entity: account, campaign, ad set, or ad.

```bash
# Account-level insights (last 30 days)
meta-ads-open-cli insights act_123456789 --date-preset last_30d

# Campaign-level breakdown
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level campaign

# Daily trend for a campaign
meta-ads-open-cli insights 23851234567890 --date-preset last_7d --time-increment 1

# Breakdowns by age and gender
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level campaign --breakdowns age,gender

# Custom date range
meta-ads-open-cli insights-date act_123456789 --start 2026-01-01 --end 2026-01-31

# Custom fields
meta-ads-open-cli insights act_123456789 --date-preset last_30d --fields impressions,clicks,spend,ctr,cpc
```

#### date-preset values

`today`, `yesterday`, `last_3d`, `last_7d`, `last_14d`, `last_28d`, `last_30d`, `last_90d`, `this_week_mon_today`, `this_week_sun_today`, `last_week_mon_sun`, `last_week_sun_sat`, `this_month`, `last_month`, `this_quarter`, `last_quarter`, `this_year`, `last_year`, `maximum`, `data_maximum`

#### Breakdown dimensions

`age`, `gender`, `country`, `region`, `platform_position`, `publisher_platform`, `device_platform`, `impression_device`

Note: `platform_position` should typically be combined with `publisher_platform` for meaningful results.

#### time-increment values

Any integer from `1` to `90` (number of days per row), or `monthly`, or `all_days` (default). Common values: `1` (daily), `7` (weekly), `14` (bi-weekly).

#### Default metrics

When `--fields` is not specified, these metrics are returned: `impressions`, `reach`, `clicks`, `cpc`, `cpm`, `ctr`, `spend`, `actions`, `cost_per_action_type`, `conversions`, `conversion_values`, `frequency`

#### Common --fields combinations by analysis type

**ROAS / revenue analysis:**
```bash
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level campaign --fields spend,purchase_roas,actions,action_values,conversion_values,cost_per_action_type
```

**Cost efficiency:**
```bash
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level campaign --fields spend,impressions,clicks,cost_per_action_type,cost_per_inline_link_click,cost_per_unique_click,cost_per_outbound_click
```

**Video performance:**
```bash
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level ad --fields impressions,spend,video_avg_time_watched_actions,video_30_sec_watched_actions,video_p25_watched_actions,video_p50_watched_actions,video_p75_watched_actions,video_p100_watched_actions,cost_per_thruplay
```

**Reach & frequency:**
```bash
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level campaign --fields reach,frequency,impressions,spend,cpp
```

**Engagement:**
```bash
meta-ads-open-cli insights act_123456789 --date-preset last_30d --level ad --fields impressions,clicks,actions,inline_link_clicks,inline_link_click_ctr,social_spend
```

#### Valid breakdown combinations

Not all breakdowns can be combined. Common valid combinations:

- `age,gender` -- demographic segmentation (the most popular breakdown)
- `publisher_platform,platform_position` -- placement optimization (where ads perform best)
- `publisher_platform` -- platform comparison (Facebook vs Instagram vs Audience Network)
- `publisher_platform,impression_device` -- platform by device type
- `country` -- geographic performance for international campaigns

Note: `device_platform` exists as a dimension name but is not listed in any valid combination in official docs. Use `publisher_platform,impression_device` for device analysis instead. `impression_device` cannot be used alone.

Invalid combinations will return an API error. When in doubt, use breakdowns one at a time. The official API only supports a specific whitelist of breakdown permutations.

#### Understanding the actions array

The `actions` field returns an array of `{action_type, value}` objects. Common action types:

**On-Meta actions:**
- `link_click` -- link clicks
- `landing_page_view` -- landing page views (subset of link clicks that loaded)
- `post_engagement` -- all post interactions
- `video_view` -- 3-second video views
- `lead` -- all leads (offsite + on-Facebook)
- `like` -- page likes
- `comment` -- post comments

**Pixel conversion actions (off-Meta):**
- `offsite_conversion.fb_pixel_purchase` -- website purchases
- `offsite_conversion.fb_pixel_add_to_cart` -- adds to cart
- `offsite_conversion.fb_pixel_initiate_checkout` -- initiates checkout
- `offsite_conversion.fb_pixel_lead` -- leads (pixel-based)
- `offsite_conversion.fb_pixel_view_content` -- content views
- `offsite_conversion.fb_pixel_complete_registration` -- registrations

**Cross-platform aggregates:**
- `omni_purchase` -- all purchases (web + app + offline)
- `omni_add_to_cart` -- all add-to-cart events

The `cost_per_action_type` and `action_values` arrays use the same action_type keys.

### Audiences

```bash
# Custom audiences
meta-ads-open-cli custom-audiences 123456789
meta-ads-open-cli custom-audience 23851234567894

# Saved audiences
meta-ads-open-cli saved-audiences 123456789

# Reach estimate for targeting specs
meta-ads-open-cli reach-estimate 123456789 --targeting '{"geo_locations":{"countries":["US"]},"age_min":25,"age_max":45}'
```

### Pixels & conversions

```bash
# List Meta Pixels
meta-ads-open-cli pixels 123456789

# Pixel events
meta-ads-open-cli pixel-events 123456789012

# Custom conversions
meta-ads-open-cli custom-conversions 123456789
```

### Pages & Instagram

```bash
# List Facebook Pages the user manages
meta-ads-open-cli pages

# Get a specific page
meta-ads-open-cli page 123456789

# Instagram business account linked to a page
meta-ads-open-cli instagram-accounts 123456789
```

### Lead gen

```bash
# List lead forms for a page
meta-ads-open-cli lead-forms 123456789

# List leads (submissions) for a form
meta-ads-open-cli leads 987654321
meta-ads-open-cli leads 987654321 --limit 500
```

Note: lead fields `ad_id` and `campaign_id` require `ads_management` permission and are only populated for real leads from live ads (not test leads).

## Workflow guidance

### When the user asks for a quick overview

1. Run `meta-ads-open-cli ad-accounts` to find accessible accounts
2. Use `insights` with `--date-preset last_30d` for a performance snapshot
3. Present the data (insights `spend` is already in major currency units, no conversion needed)

### When the user asks for deep analysis

1. Start with account-level `insights` to see overall performance
2. Add `--level campaign` to identify top/bottom campaigns
3. Drill down with `--level adset` or `--level ad` for underperforming campaigns
4. Use `--breakdowns age,gender` or `--breakdowns country` for audience analysis
5. Use `--time-increment 1` for daily trends to spot anomalies
6. Cross-reference with `creatives` to review ad copy and visuals

### When the user asks about creative performance

1. Run `insights` with `--level ad` to get ad-level metrics
2. Use `ads` to find the creative IDs linked to each ad
3. Use `creative` to inspect the actual creative content (images, copy, CTAs)

### When the user asks about audience reach

1. Use `custom-audiences` to see existing audiences and their sizes
2. Use `reach-estimate` with targeting specs to estimate potential reach
3. Use `insights` with `--breakdowns age,gender` or `--breakdowns country` to see who is being reached

### When the user asks about conversion tracking

1. Run `pixels` to list active Meta Pixels
2. Use `pixel-events` to check what events are being tracked
3. Use `custom-conversions` to see custom conversion rules
4. Check `insights` with `conversions` and `cost_per_action_type` fields

### When the user asks about lead gen

1. Use `pages` to find the Page ID
2. Use `lead-forms` with the Page ID to list forms
3. Use `leads` with a form ID to retrieve submissions

### Error handling

- **Authentication errors** -- ask the user to verify their access token and permissions
- **"param business is required"** -- the `account-users` command requires `--business <id>`
- **Empty insights** -- check date range, entity status, and whether the account had active ads in the period
- **Missing lead fields** -- `ad_id`/`campaign_id` require `ads_management` permission and only appear on real (non-test) leads
- **Permission errors** -- different commands require different permissions; check the required permissions list above

## API documentation references

- [meta-ads-open-cli documentation](https://github.com/Bin-Huang/meta-ads-open-cli)
- [Meta Marketing API overview](https://developers.facebook.com/docs/marketing-apis/)
- [Ad Insights API](https://developers.facebook.com/docs/marketing-api/insights/)
- [Custom Audiences API](https://developers.facebook.com/docs/marketing-api/audiences/)
- [Lead Ads API](https://developers.facebook.com/docs/marketing-api/guides/lead-ads/)
- [Ad Creative reference](https://developers.facebook.com/docs/marketing-api/reference/ad-creative)
