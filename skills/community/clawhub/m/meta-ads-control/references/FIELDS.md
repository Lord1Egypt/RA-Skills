# Field Sets and Reporting Defaults

These are practical field bundles for agent use. Keep them small. Add more only when the user actually needs them.

## Ad account fields

### Basic account audit

```text
id,name,account_id,account_status,currency,timezone_name,amount_spent,spend_cap,business_name
```

### Operations context

```text
id,name,account_status,currency,timezone_name,disable_reason,owner,adtrust_dsl,io_number
```

## Campaign fields

### Minimal lifecycle view

```text
id,name,objective,status,effective_status,buying_type,created_time,updated_time
```

### Budget and policy context

```text
id,name,objective,status,effective_status,daily_budget,lifetime_budget,budget_rebalance_flag,special_ad_categories,start_time,stop_time
```

## Ad set fields

### Minimal lifecycle view

```text
id,name,campaign_id,status,effective_status,created_time,updated_time
```

### Delivery and optimisation view

```text
id,name,campaign_id,status,effective_status,daily_budget,lifetime_budget,billing_event,optimization_goal,bid_strategy,start_time,end_time,targeting,promoted_object
```

## Ad fields

### Minimal lifecycle view

```text
id,name,adset_id,campaign_id,status,effective_status,created_time,updated_time
```

### Creative and tracking view

```text
id,name,adset_id,campaign_id,status,effective_status,creative,tracking_specs,conversion_domain,preview_shareable_link
```

## Ad creative fields

### Safe default

```text
id,name,object_story_spec,effective_object_story_id,thumbnail_url,asset_feed_spec
```

Use specific extra fields only when you know the creative type.

## Asset library fields

### Ad images

```text
hash,name,url,permalink_url,original_width,original_height
```

### Ad videos

```text
id,title,status,source,created_time,updated_time,thumbnails
```

## Insights bundles

## 1. Overview bundle

Good first query for performance triage.

```text
account_id,account_name,campaign_id,campaign_name,adset_id,adset_name,ad_id,ad_name,impressions,reach,clicks,inline_link_clicks,spend,cpm,cpc,ctr
```

## 2. Efficiency bundle

Add this when the user asks what is efficient or wasteful.

```text
spend,impressions,reach,frequency,clicks,inline_link_clicks,ctr,cpc,cpm,cpp
```

## 3. Ecommerce bundle

Use when the user asks about purchases, revenue, ROAS, or cart events.

```text
spend,clicks,inline_link_clicks,actions,action_values,purchase_roas,website_purchase_roas
```

Practical note: many conversion metrics arrive inside `actions` and `action_values` arrays, not as flat columns.

## 4. Lead generation bundle

```text
spend,impressions,clicks,inline_link_clicks,actions,action_values,cpl
```

If `cpl` is unavailable or inconsistent for the chosen objective, use `actions` plus the relevant lead action type.

## 5. Creative diagnostic bundle

```text
ad_id,ad_name,impressions,clicks,inline_link_clicks,spend,ctr,cpc,quality_ranking,engagement_rate_ranking,conversion_rate_ranking
```

Field availability can vary by objective, account, and creative type.

## Common levels

- `account` — whole account summary
- `campaign` — best default for management summaries
- `adset` — audience, placement, and budget comparisons
- `ad` — creative-level diagnostics

## Common date presets

- `today`
- `yesterday`
- `last_3d`
- `last_7d`
- `last_14d`
- `last_30d`
- `this_month`
- `last_month`
- `maximum`

Prefer a short preset unless the user explicitly needs a long historical view.

## Common breakdowns

Use sparingly because they multiply row count.

### Placement and device

```text
publisher_platform
platform_position
impression_device
device_platform
```

### Geography and demographics

```text
country
region
age
gender
dma
```

### Time series

Use `time_increment=1` for daily rows, or a larger increment for less noisy reporting.

## Action breakdowns

Use only when the user needs action-level detail.

Examples:

```text
action_type
action_device
action_destination
```

Practical rule: if you use `action_breakdowns`, include `actions`.

## Reporting patterns by question

### “What is working?”

- level: `campaign`
- last 7 or 30 days
- overview + ecommerce or leadgen bundle
- sort by spend or ROAS

### “Which audience is underperforming?”

- level: `adset`
- efficiency bundle
- maybe `publisher_platform` or `country` breakdowns if asked

### “Which creative should we pause?”

- level: `ad`
- overview + creative diagnostic bundle
- short date window if creative was launched recently

### “Show me daily trend”

- level: `campaign` or `adset`
- `time_increment=1`
- keep fields minimal

## Budget notes

Budget values are usually integer minor units. Convert for human reporting but keep raw values in payloads and write operations.

## Query examples

### Campaign summary

```bash
python3 scripts/meta_ads.py insights act_123 --level campaign --date-preset last_7d --fields campaign_id,campaign_name,spend,impressions,clicks,ctr,cpc,actions,action_values,purchase_roas
```

### Ad-level creative read

```bash
python3 scripts/meta_ads.py insights act_123 --level ad --date-preset last_14d --fields ad_id,ad_name,spend,impressions,clicks,ctr,cpc,quality_ranking,engagement_rate_ranking,conversion_rate_ranking
```

### Daily trend

```bash
python3 scripts/meta_ads.py insights act_123 --level campaign --date-preset last_30d --time-increment 1 --fields campaign_id,campaign_name,date_start,date_stop,spend,impressions,clicks,ctr
```
