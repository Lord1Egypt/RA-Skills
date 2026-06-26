---
name: pinterest-ads-cli
description: >
  Pinterest Ads data analysis and reporting via pinterest-ads-cli.
  Use when the user wants to check Pinterest ad performance, pull campaign/ad group/ad stats,
  explore ad account structure, inspect audiences, analyze billing, browse product catalogs,
  discover trending search terms, or retrieve analytics with attribution windows.
  Triggers: "Pinterest Ads", "Pinterest ad performance", "Pinterest campaign stats",
  "Pinterest ad spend", "Pinterest analytics", "Pinterest audience", "Pinterest catalogs",
  "Pinterest trends", "Pinterest keywords", "Pinterest billing", "Pinterest lead forms",
  "Pinterest conversion tags", "Pinterest shopping", "Pinterest feeds".
---

# Pinterest Ads CLI Skill

You have access to `pinterest-ads-cli`, a read-only CLI for the Pinterest REST API v5. Use it to query ad accounts, pull performance analytics, inspect campaigns and ads, analyze audiences, browse product catalogs, discover trending search terms, and review billing across Pinterest advertising.

## Quick start

```bash
# Check if the CLI is available
pinterest-ads-cli --help

# List accessible ad accounts
pinterest-ads-cli accounts

# Get a specific ad account
pinterest-ads-cli account 123456789
```

If the CLI is not installed, install it:

```bash
npm install -g pinterest-ads-cli
```

## Authentication

The CLI requires a Pinterest **OAuth2 access token**. Most commands need the `ads:read` scope. Additional scopes may be required for specific commands: `catalogs:read` for catalog commands, `user_accounts:read` for trends, and `billing:read` for billing data. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `PINTEREST_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/pinterest-ads-cli/credentials.json`

The credentials JSON file format:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN"
}
```

Before running any command, verify credentials are configured by running `pinterest-ads-cli accounts`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Ad Account
 +-- Campaign
 |    +-- Ad Group
 |         +-- Ad
 |         +-- Keyword
 +-- Audience
 +-- Customer List
 +-- Conversion Tag
 +-- Billing Profile
 +-- Order Line
 +-- Lead Form
```

Catalog resources (catalogs, feeds, product groups) are not scoped to an ad account and are accessed at the top level.

## Monetary values

Pinterest analytics returns monetary metrics in **micro-currency units** (1/1,000,000 of the ad account's currency). Fields like `SPEND_IN_MICRO_DOLLAR`, `CPC_IN_MICRO_DOLLAR`, and `ECPM_IN_MICRO_DOLLAR` must be divided by 1,000,000 to get the actual amount. Despite the `DOLLAR` suffix in field names, values are in the ad account's configured currency (USD, GBP, EUR, etc.).

Example: `SPEND_IN_MICRO_DOLLAR: 5000000` means 5.00 in the account's currency.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Pagination uses cursor-based `--bookmark` values returned in the response. Pass the bookmark from a previous response to get the next page.

## Commands reference

### Account discovery

```bash
# List ad accounts
pinterest-ads-cli accounts
pinterest-ads-cli accounts --page-size 50

# Get a specific ad account
pinterest-ads-cli account 123456789
```

#### accounts

List ad accounts the user has access to.

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### account

Get details of a specific ad account. Takes the ad account ID as a required argument.

```bash
pinterest-ads-cli account <ad-account-id>
```

### Campaign hierarchy

```bash
# List campaigns
pinterest-ads-cli campaigns 123456789
pinterest-ads-cli campaigns 123456789 --entity-statuses ACTIVE,PAUSED
pinterest-ads-cli campaigns 123456789 --order DESCENDING --page-size 100

# List ad groups
pinterest-ads-cli adgroups 123456789
pinterest-ads-cli adgroups 123456789 --campaign-ids campaign_1,campaign_2

# List ads
pinterest-ads-cli ads 123456789
pinterest-ads-cli ads 123456789 --campaign-ids campaign_1 --entity-statuses ACTIVE
```

#### campaigns

List campaigns for an ad account.

```bash
pinterest-ads-cli campaigns <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | Filter by campaign IDs (comma-separated) | -- |
| `--entity-statuses <statuses>` | Filter by status (comma-separated, e.g. ACTIVE,PAUSED) | -- |
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### adgroups

List ad groups for an ad account.

```bash
pinterest-ads-cli adgroups <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | Filter by campaign IDs (comma-separated) | -- |
| `--ad-group-ids <ids>` | Filter by ad group IDs (comma-separated) | -- |
| `--entity-statuses <statuses>` | Filter by status (comma-separated) | -- |
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### ads

List ads for an ad account.

```bash
pinterest-ads-cli ads <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | Filter by campaign IDs (comma-separated) | -- |
| `--ad-group-ids <ids>` | Filter by ad group IDs (comma-separated) | -- |
| `--ad-ids <ids>` | Filter by ad IDs (comma-separated) | -- |
| `--entity-statuses <statuses>` | Filter by status (comma-separated) | -- |
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

### Keywords

```bash
# List keywords for an ad account
pinterest-ads-cli keywords 123456789
pinterest-ads-cli keywords 123456789 --ad-group-id adgroup_1
```

#### keywords

List targeting keywords for an ad account.

```bash
pinterest-ads-cli keywords <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--ad-group-id <id>` | Filter by ad group ID | -- |
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

### Audiences

```bash
# List audiences
pinterest-ads-cli audiences 123456789

# List customer lists
pinterest-ads-cli customer-lists 123456789
```

#### audiences

List audiences for an ad account.

```bash
pinterest-ads-cli audiences <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### customer-lists

List customer lists for an ad account.

```bash
pinterest-ads-cli customer-lists <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

### Conversion tracking

```bash
# List all conversion tags
pinterest-ads-cli conversion-tags 123456789

# Get a specific conversion tag
pinterest-ads-cli conversion-tag 123456789 tag_abc
```

#### conversion-tags

List conversion tags for an ad account. No pagination options -- returns all tags.

```bash
pinterest-ads-cli conversion-tags <ad-account-id>
```

#### conversion-tag

Get a specific conversion tag.

```bash
pinterest-ads-cli conversion-tag <ad-account-id> <tag-id>
```

### Billing

```bash
# List billing profiles
pinterest-ads-cli billing-profiles 123456789
pinterest-ads-cli billing-profiles 123456789 --is-active

# List order lines
pinterest-ads-cli order-lines 123456789

# Get a specific order line
pinterest-ads-cli order-line 123456789 orderline_abc
```

#### billing-profiles

List billing profiles for an ad account.

```bash
pinterest-ads-cli billing-profiles <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--is-active` | Only return active profiles (boolean flag) | false |
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### order-lines

List order lines for an ad account.

```bash
pinterest-ads-cli order-lines <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### order-line

Get a specific order line.

```bash
pinterest-ads-cli order-line <ad-account-id> <order-line-id>
```

### Lead forms

```bash
# List lead forms
pinterest-ads-cli lead-forms 123456789

# Get a specific lead form
pinterest-ads-cli lead-form 123456789 leadform_abc
```

#### lead-forms

List lead generation forms for an ad account.

```bash
pinterest-ads-cli lead-forms <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--order <order>` | Sort order: ASCENDING or DESCENDING | -- |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### lead-form

Get a specific lead form.

```bash
pinterest-ads-cli lead-form <ad-account-id> <lead-form-id>
```

### Catalogs (Pinterest Shopping)

Catalog commands are not scoped to an ad account.

```bash
# List catalogs
pinterest-ads-cli catalogs

# List catalog feeds
pinterest-ads-cli feeds

# List catalog product groups
pinterest-ads-cli product-groups
```

#### catalogs

List catalogs.

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### feeds

List catalog feeds.

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

#### product-groups

List catalog product groups.

| Option | Description | Default |
|--------|-------------|---------|
| `--page-size <n>` | Results per page (max 250) | 25 |
| `--bookmark <cursor>` | Pagination cursor | -- |

### Trends

Discover trending search terms by region. Does not require an ad account ID.

```bash
# Growing trends in the US
pinterest-ads-cli trends US --trend-type growing

# Monthly trends filtered by interest
pinterest-ads-cli trends US --trend-type monthly --interests fashion --limit 20

# Seasonal trends filtered by demographics
pinterest-ads-cli trends GB --trend-type seasonal --genders female --ages 25-34
```

#### trends

Get trending search terms for a region.

```bash
pinterest-ads-cli trends <region>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--trend-type <type>` | **Required.** Trend type: growing, monthly, yearly, seasonal | -- |
| `--interests <interests>` | Filter by interests (comma-separated) | -- |
| `--genders <genders>` | Filter by genders (comma-separated) | -- |
| `--ages <ages>` | Filter by age groups (comma-separated) | -- |
| `--limit <n>` | Number of results | 50 |

Note: the `trends` command does not support `--bookmark` pagination. Use `--limit` to control the number of results.

### Analytics

Analytics commands pull performance metrics for ad accounts, campaigns, ad groups, and ads. All analytics commands require `--start-date`, `--end-date`, and `--columns`.

```bash
# Account-level analytics
pinterest-ads-cli analytics 123456789 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --columns SPEND_IN_MICRO_DOLLAR,IMPRESSION_1,CLICKTHROUGH_1 \
  --granularity DAY

# Campaign-level analytics
pinterest-ads-cli campaign-analytics 123456789 \
  --campaign-ids campaign_1,campaign_2 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --columns SPEND_IN_MICRO_DOLLAR,IMPRESSION_1,CLICKTHROUGH_1

# Ad group-level analytics
pinterest-ads-cli adgroup-analytics 123456789 \
  --ad-group-ids adgroup_1 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --columns SPEND_IN_MICRO_DOLLAR,IMPRESSION_1

# Ad-level analytics
pinterest-ads-cli ad-analytics 123456789 \
  --ad-ids ad_1 \
  --start-date 2026-03-01 \
  --end-date 2026-03-15 \
  --columns SPEND_IN_MICRO_DOLLAR,IMPRESSION_1
```

#### analytics

Get ad account-level analytics.

```bash
pinterest-ads-cli analytics <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--start-date <date>` | **Required.** Start date (YYYY-MM-DD) | -- |
| `--end-date <date>` | **Required.** End date (YYYY-MM-DD) | -- |
| `--columns <cols>` | **Required.** Metrics (comma-separated) | -- |
| `--granularity <gran>` | TOTAL, DAY, HOUR, WEEK, MONTH | DAY |
| `--click-window-days <n>` | Click attribution window: 0, 1, 7, 14, 30, 60 | -- |
| `--view-window-days <n>` | View attribution window: 0, 1, 7, 14, 30, 60 | -- |

#### campaign-analytics

Get campaign-level analytics.

```bash
pinterest-ads-cli campaign-analytics <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--campaign-ids <ids>` | **Required.** Campaign IDs (comma-separated) | -- |
| `--start-date <date>` | **Required.** Start date (YYYY-MM-DD) | -- |
| `--end-date <date>` | **Required.** End date (YYYY-MM-DD) | -- |
| `--columns <cols>` | **Required.** Metrics (comma-separated) | -- |
| `--granularity <gran>` | TOTAL, DAY, HOUR, WEEK, MONTH | DAY |

#### adgroup-analytics

Get ad group-level analytics.

```bash
pinterest-ads-cli adgroup-analytics <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--ad-group-ids <ids>` | **Required.** Ad group IDs (comma-separated) | -- |
| `--start-date <date>` | **Required.** Start date (YYYY-MM-DD) | -- |
| `--end-date <date>` | **Required.** End date (YYYY-MM-DD) | -- |
| `--columns <cols>` | **Required.** Metrics (comma-separated) | -- |
| `--granularity <gran>` | TOTAL, DAY, HOUR, WEEK, MONTH | DAY |

#### ad-analytics

Get ad-level analytics.

```bash
pinterest-ads-cli ad-analytics <ad-account-id>
```

| Option | Description | Default |
|--------|-------------|---------|
| `--ad-ids <ids>` | **Required.** Ad IDs (comma-separated) | -- |
| `--start-date <date>` | **Required.** Start date (YYYY-MM-DD) | -- |
| `--end-date <date>` | **Required.** End date (YYYY-MM-DD) | -- |
| `--columns <cols>` | **Required.** Metrics (comma-separated) | -- |
| `--granularity <gran>` | TOTAL, DAY, HOUR, WEEK, MONTH | DAY |

#### Common analytics columns

Columns documented in README: `SPEND_IN_MICRO_DOLLAR`, `IMPRESSION_1`, `CLICKTHROUGH_1`, `CPC_IN_MICRO_DOLLAR`, `ECPM_IN_MICRO_DOLLAR`, `CTR`, `TOTAL_CONVERSIONS`

The CLI passes column names directly to the Pinterest API v5 without validation. Refer to the [Pinterest Analytics API docs](https://developers.pinterest.com/docs/api/v5/) for all available columns (e.g., video metrics, engagement metrics, web conversion metrics). Column names use uppercase with underscores (e.g., `VIDEO_MRC_VIEWS_1`, `TOTAL_ENGAGEMENT`). Monetary columns end in `_IN_MICRO_DOLLAR` -- divide by 1,000,000.

#### Attribution windows

Only the account-level `analytics` command supports attribution window options (`--click-window-days` and `--view-window-days`). The campaign, ad group, and ad-level analytics commands do not support these options in the CLI (this is a CLI limitation; the Pinterest API supports attribution windows on all analytics endpoints).

## Workflow guidance

### When the user asks for a quick overview

1. Run `pinterest-ads-cli accounts` to find accessible accounts
2. Use `analytics` with a recent date range and key columns like `SPEND_IN_MICRO_DOLLAR,IMPRESSION_1,CLICKTHROUGH_1,CTR`
3. Remember to divide micro-dollar values by 1,000,000 when presenting to the user

### When the user asks for deep analysis

1. Start with account-level `analytics` to see overall performance
2. Use `campaigns` to list campaigns, then `campaign-analytics` for campaign-level breakdown
3. Drill down with `adgroup-analytics` or `ad-analytics` for underperforming entities
4. Use account-level `analytics` with `--click-window-days` and `--view-window-days` to understand attribution
5. Cross-reference with `keywords` to review targeting

### When the user asks about audience targeting

1. Use `audiences` to see existing audiences
2. Use `customer-lists` to see customer list audiences
3. Use `keywords` with `--ad-group-id` to see targeting keywords for specific ad groups

### When the user asks about conversion tracking

1. Run `conversion-tags` to list active conversion tags
2. Use `conversion-tag` to get details on a specific tag
3. Check `analytics` with `TOTAL_CONVERSIONS` column to see conversion performance

### When the user asks about product catalogs

1. Use `catalogs` to list catalogs
2. Use `feeds` to inspect catalog feeds
3. Use `product-groups` to see product groupings

### When the user asks about trends

1. Use `trends` with the appropriate region code (e.g., US, GB, CA)
2. Filter with `--trend-type` (growing, monthly, yearly, seasonal)
3. Narrow down with `--interests`, `--genders`, or `--ages`

### When the user asks about billing

1. Use `billing-profiles` to see billing configurations (add `--is-active` for active only)
2. Use `order-lines` to see order lines
3. Use `order-line` with a specific ID for details

## Error handling

- **Authentication errors** -- ask the user to verify their access token and `ads:read` scope
- **Credentials not found** -- check that one of the three credential sources is configured: `--credentials` flag, `PINTEREST_ADS_ACCESS_TOKEN` env var, or `~/.config/pinterest-ads-cli/credentials.json`
- **Empty analytics** -- check the date range, entity status, and whether the account had active ads in the period
- **Permission errors** -- ensure the access token has the required `ads:read` scope
- **Invalid column names** -- verify column names match the Pinterest API schema (e.g., `SPEND_IN_MICRO_DOLLAR`, not `SPEND`)

## API documentation references

- [pinterest-ads-cli documentation](https://github.com/Bin-Huang/pinterest-ads-cli)
- [Pinterest API v5 overview](https://developers.pinterest.com/docs/api/v5/)
- [Pinterest OAuth authentication](https://developers.pinterest.com/docs/getting-started/authentication/)
- [Pinterest Analytics API](https://developers.pinterest.com/docs/api/v5/#tag/ad_accounts)
- [Pinterest Catalogs API](https://developers.pinterest.com/docs/api/v5/#tag/catalogs)
- [Pinterest Trends API](https://developers.pinterest.com/docs/api/v5/#tag/trends)
