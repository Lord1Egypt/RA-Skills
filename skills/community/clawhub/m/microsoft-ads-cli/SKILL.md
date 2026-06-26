---
name: microsoft-ads-cli
description: >
  Microsoft Ads data analysis and reporting via microsoft-ads-cli.
  Use when the user wants to check Microsoft/Bing ad performance, pull campaign/ad group/keyword stats,
  explore ad account structure, inspect audiences, manage conversion goals, or retrieve performance reports.
  Triggers: "Microsoft Ads", "Bing Ads", "Microsoft Advertising", "bing ad performance", "microsoft campaign stats",
  "microsoft ad spend", "bing keywords", "microsoft audiences", "UET tags", "microsoft conversion goals",
  "bing search ads", "microsoft shopping ads", "microsoft performance max".
---

# Microsoft Ads CLI Skill

You have access to `microsoft-ads-cli`, a read-only CLI for the Bing Ads API v13. Use it to query ad accounts, pull campaign/ad group/keyword performance reports, inspect audiences, manage UET conversion goals, and analyze bid strategies across Search, Shopping, Audience, DynamicSearchAds, and PerformanceMax campaigns.

## Quick start

```bash
# Check if the CLI is available
microsoft-ads-cli --help

# Get authenticated user info
microsoft-ads-cli user

# List accessible ad accounts
microsoft-ads-cli accounts
```

If the CLI is not installed, install it:

```bash
npm install -g microsoft-ads-cli
```

## Authentication

The CLI requires a Microsoft **OAuth2 access token** and a **Developer Token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variables: `MICROSOFT_ADS_ACCESS_TOKEN` + `MICROSOFT_ADS_DEVELOPER_TOKEN` (both required), plus optional `MICROSOFT_ADS_CUSTOMER_ID` and `MICROSOFT_ADS_ACCOUNT_ID`
3. Auto-detected file: `~/.config/microsoft-ads-cli/credentials.json`

The credentials file format:

```json
{
  "access_token": "YOUR_ACCESS_TOKEN",
  "developer_token": "YOUR_DEVELOPER_TOKEN",
  "customer_id": "YOUR_CUSTOMER_ID",
  "account_id": "YOUR_DEFAULT_ACCOUNT_ID"
}
```

`access_token` and `developer_token` are required. `customer_id` and `account_id` are optional but needed for most campaign management commands.

Before running any command, verify credentials are configured by running `microsoft-ads-cli user`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Customer
 +-- Ad Account
      +-- Campaign (Search, Shopping, Audience, DynamicSearchAds, PerformanceMax)
      |    +-- Ad Group
      |         +-- Ad (AppInstall, DynamicSearch, ExpandedText, Hotel, Product, ResponsiveAd, ResponsiveSearch)
      |         +-- Keyword
      |         +-- Negative Keyword
      +-- Budget
      +-- Bid Strategy
      +-- Label
      +-- Audience (RemarketingList, CustomerList, Custom, InMarket, Product, SimilarRemarketingList, CombinedList)
      +-- UET Tag
           +-- Conversion Goal (Url, Duration, PagesViewedPerVisit, Event, AppInstall, OfflineConversion, InStoreTransaction)
```

Many commands accept `--account-id <id>` to override the default account from credentials. The `campaigns` command takes `<account-id>` as a required positional argument instead.

## Monetary values

The Bing Ads API returns monetary values (Spend, AverageCpc, CostPerConversion, Revenue, budgets, bids) in the currency of the ad account. Report values are typically in the major currency unit as strings (e.g., `"12.34"` means $12.34). Budget and bid amounts from campaign management endpoints may be returned as decimal numbers.

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

The `accounts` command supports pagination via `--page-index` and `--page-size`. Other listing commands return all results in a single response (no cursor-based pagination).

## Commands reference

### Account discovery

```bash
# List ad accounts (paginated)
microsoft-ads-cli accounts
microsoft-ads-cli accounts --page-index 0 --page-size 50

# Get a specific ad account
microsoft-ads-cli account 123456789

# Get the current authenticated user
microsoft-ads-cli user
```

**accounts** options:
- `--page-index <n>` -- page index, 0-based (default 0)
- `--page-size <n>` -- results per page (default 100)

### Campaigns

```bash
# List all campaigns for an account
microsoft-ads-cli campaigns 123456789

# Filter by campaign type
microsoft-ads-cli campaigns 123456789 --type Search
microsoft-ads-cli campaigns 123456789 --type "Shopping PerformanceMax"
```

**campaigns** options:
- `--type <type>` -- campaign type filter: Search, Shopping, Audience, DynamicSearchAds, PerformanceMax (space-separated for multiple, default all)

```bash
# Get a specific campaign by ID
microsoft-ads-cli campaign 987654321
microsoft-ads-cli campaign 987654321 --account-id 123456789
```

**campaign** options:
- `--account-id <id>` -- ad account ID

### Ad groups

```bash
# List ad groups for a campaign
microsoft-ads-cli adgroups 987654321
microsoft-ads-cli adgroups 987654321 --account-id 123456789
```

**adgroups** options:
- `--account-id <id>` -- ad account ID

### Ads

```bash
# List ads for an ad group
microsoft-ads-cli ads 111222333
microsoft-ads-cli ads 111222333 --type ResponsiveSearch
microsoft-ads-cli ads 111222333 --account-id 123456789
```

**ads** options:
- `--account-id <id>` -- ad account ID
- `--type <type>` -- ad type filter (default all: AppInstall, DynamicSearch, ExpandedText, Hotel, Product, ResponsiveAd, ResponsiveSearch)

### Keywords

```bash
# List keywords for an ad group
microsoft-ads-cli keywords 111222333
microsoft-ads-cli keywords 111222333 --account-id 123456789
```

**keywords** options:
- `--account-id <id>` -- ad account ID

### Negative keywords

```bash
# List negative keywords for a campaign (default)
microsoft-ads-cli negative-keywords 987654321

# List negative keywords for an ad group
microsoft-ads-cli negative-keywords 111222333 --type AdGroup
```

**negative-keywords** options:
- `--account-id <id>` -- ad account ID
- `--type <type>` -- entity type: Campaign or AdGroup (default Campaign)

### Audiences

```bash
# List remarketing lists (default)
microsoft-ads-cli audiences

# List specific audience types (comma-separated)
microsoft-ads-cli audiences --type "RemarketingList,CustomerList"
microsoft-ads-cli audiences --type "Custom,InMarket,Product"
microsoft-ads-cli audiences --account-id 123456789
```

**audiences** options:
- `--account-id <id>` -- ad account ID
- `--type <type>` -- audience type (comma-separated): Custom, InMarket, Product, RemarketingList, SimilarRemarketingList, CustomerList, CombinedList (default RemarketingList)

### UET tags

```bash
# List all UET tags
microsoft-ads-cli uet-tags
microsoft-ads-cli uet-tags --account-id 123456789
```

**uet-tags** options:
- `--account-id <id>` -- ad account ID

### Conversion goals

```bash
# List all conversion goals
microsoft-ads-cli conversion-goals

# Filter by goal type (comma-separated)
microsoft-ads-cli conversion-goals --type "Event,OfflineConversion"

# Filter by UET tag IDs
microsoft-ads-cli conversion-goals --tag-ids 12345,67890
```

**conversion-goals** options:
- `--account-id <id>` -- ad account ID
- `--type <type>` -- goal type (comma-separated): Url, Duration, PagesViewedPerVisit, Event, AppInstall, OfflineConversion, InStoreTransaction (default all)
- `--tag-ids <ids>` -- UET tag IDs to filter by (comma-separated, default all)

### Budgets

```bash
# Get budgets by IDs (comma-separated)
microsoft-ads-cli budgets 111,222,333
microsoft-ads-cli budgets 111,222 --account-id 123456789
```

**budgets** options:
- `--account-id <id>` -- ad account ID

### Bid strategies

```bash
# Get bid strategies by IDs (comma-separated)
microsoft-ads-cli bid-strategies 111,222
microsoft-ads-cli bid-strategies 111 --account-id 123456789
```

**bid-strategies** options:
- `--account-id <id>` -- ad account ID

### Labels

```bash
# List all labels for the account
microsoft-ads-cli labels
microsoft-ads-cli labels --account-id 123456789
```

**labels** options:
- `--account-id <id>` -- ad account ID

### Performance reports

Reports are asynchronous: submit a report request, then poll for its status. When the status is `Success`, the response includes a `ReportDownloadUrl`.

#### Campaign performance report

```bash
# Submit a campaign performance report
microsoft-ads-cli report 123456789 --start-date 2026-03-01 --end-date 2026-03-15

# With granularity
microsoft-ads-cli report 123456789 --start-date 2026-03-01 --end-date 2026-03-15 --granularity Weekly

# With custom columns
microsoft-ads-cli report 123456789 --start-date 2026-03-01 --end-date 2026-03-15 --columns "Impressions,Clicks,Spend,Conversions"
```

**report** options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- Daily, Weekly, Monthly, Summary (default Daily)
- `--columns <cols>` -- report columns, comma-separated (default: TimePeriod, AccountId, AccountName, CampaignId, CampaignName, CampaignStatus, Impressions, Clicks, Ctr, Spend, AverageCpc, Conversions, ConversionRate, CostPerConversion, Revenue)

#### Keyword performance report

```bash
microsoft-ads-cli keyword-report 123456789 --start-date 2026-03-01 --end-date 2026-03-15
microsoft-ads-cli keyword-report 123456789 --start-date 2026-03-01 --end-date 2026-03-15 --granularity Monthly
```

**keyword-report** options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- Daily, Weekly, Monthly, Summary (default Daily)

Default columns: TimePeriod, AccountId, CampaignId, CampaignName, AdGroupId, AdGroupName, Keyword, KeywordId, BidMatchType, DeliveredMatchType, Impressions, Clicks, Ctr, Spend, AverageCpc, Conversions, QualityScore

#### Ad group performance report

```bash
microsoft-ads-cli adgroup-report 123456789 --start-date 2026-03-01 --end-date 2026-03-15
microsoft-ads-cli adgroup-report 123456789 --start-date 2026-03-01 --end-date 2026-03-15 --granularity Summary
```

**adgroup-report** options:
- `--start-date <date>` -- start date, YYYY-MM-DD (required)
- `--end-date <date>` -- end date, YYYY-MM-DD (required)
- `--granularity <gran>` -- Daily, Weekly, Monthly, Summary (default Daily)

Default columns: TimePeriod, AccountId, CampaignId, CampaignName, AdGroupId, AdGroupName, AdGroupStatus, Impressions, Clicks, Ctr, Spend, AverageCpc, Conversions, ConversionRate, CostPerConversion

#### Check report status

```bash
# Poll for report completion
microsoft-ads-cli report-status abc123-report-id
```

When `Status` is `Success`, download the CSV from the `ReportDownloadUrl` in the response.

## Workflow guidance

### When the user asks for a quick overview

1. Run `microsoft-ads-cli accounts` to find accessible accounts
2. Run `microsoft-ads-cli campaigns <account-id>` to see campaigns
3. Submit a `report` for the desired date range to get performance metrics
4. Poll with `report-status` until the report is ready

### When the user asks for campaign analysis

1. List campaigns with `microsoft-ads-cli campaigns <account-id>`
2. Submit a campaign `report` with appropriate date range and granularity
3. For deeper analysis, drill into ad groups with `microsoft-ads-cli adgroups <campaign-id>`
4. Check keyword performance with `keyword-report`

### When the user asks about keyword performance

1. Use `microsoft-ads-cli keywords <adgroup-id>` to see keyword settings and bids
2. Submit a `keyword-report` for the account to get keyword-level metrics (impressions, clicks, spend, quality score)
3. Check negative keywords with `microsoft-ads-cli negative-keywords <entity-id>` to understand exclusions

### When the user asks about audiences and tracking

1. Run `microsoft-ads-cli audiences` to see remarketing lists and other audience types
2. Use `microsoft-ads-cli uet-tags` to check Universal Event Tracking setup
3. Use `microsoft-ads-cli conversion-goals` to review conversion goal configuration
4. Filter conversion goals by UET tag with `--tag-ids` to see which goals are tied to which tags

### When the user asks about budgets and bidding

1. Get campaign details to find budget and bid strategy IDs
2. Use `microsoft-ads-cli budgets <ids>` to check budget configurations
3. Use `microsoft-ads-cli bid-strategies <ids>` to review bidding strategies

### When the user asks for ad creative review

1. List campaigns with `microsoft-ads-cli campaigns <account-id>`
2. Drill into ad groups with `microsoft-ads-cli adgroups <campaign-id>`
3. List ads with `microsoft-ads-cli ads <adgroup-id>` to inspect ad content and types

## Error handling

- **Authentication errors** -- ask the user to verify their access token and developer token; tokens may be expired
- **Missing credentials** -- ensure both `access_token` and `developer_token` are configured
- **Empty responses** -- check that the correct account ID is being used and the account has active entities
- **Report not ready** -- poll `report-status` again after a short wait; reports can take time to generate
- **Permission errors** -- verify the user has access to the specified account and customer

## API documentation references

- [microsoft-ads-cli documentation](https://github.com/Bin-Huang/microsoft-ads-cli)
- [Bing Ads API Getting Started](https://learn.microsoft.com/en-us/advertising/guides/get-started)
- [Authentication with OAuth](https://learn.microsoft.com/en-us/advertising/guides/authentication-oauth)
- [Campaign Management Service](https://learn.microsoft.com/en-us/advertising/campaign-management-service/campaign-management-service-reference)
- [Reporting Service](https://learn.microsoft.com/en-us/advertising/reporting-service/reporting-service-reference)
- [Customer Management Service](https://learn.microsoft.com/en-us/advertising/customer-management-service/customer-management-service-reference)
