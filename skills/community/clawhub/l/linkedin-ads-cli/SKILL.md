---
name: linkedin-ads-cli
description: >
  LinkedIn Ads data analysis and reporting via linkedin-ads-cli.
  Use when the user wants to check LinkedIn ad performance, pull campaign analytics with pivot breakdowns,
  explore ad account structure, inspect creatives, analyze audiences, retrieve lead form submissions,
  forecast ad delivery, or get budget recommendations.
  Triggers: "LinkedIn Ads", "LinkedIn ad performance", "LinkedIn campaign stats", "LinkedIn ad spend",
  "LinkedIn analytics", "LinkedIn audience", "LinkedIn lead forms", "LinkedIn creatives",
  "LinkedIn ad account", "LinkedIn targeting", "LinkedIn budget forecast".
---

# LinkedIn Ads CLI Skill

You have access to `linkedin-ads-cli`, a read-only CLI for the LinkedIn Marketing API (REST API, version 202603). Use it to query ad accounts, pull performance analytics with pivot breakdowns, inspect creatives, explore audiences and targeting facets, retrieve lead form submissions, and get budget and delivery forecasts.

## Quick start

```bash
# Check if the CLI is available
linkedin-ads-cli --help

# Get authenticated user info
linkedin-ads-cli me

# List organizations you administer
linkedin-ads-cli organization-acls

# List ad accounts
linkedin-ads-cli accounts
```

If the CLI is not installed, install it:

```bash
npm install -g linkedin-ads-cli
```

## Authentication

The CLI requires a LinkedIn **OAuth2 Bearer token**. Credentials are resolved in this order:

1. `--credentials <path>` flag (per-command)
2. Environment variable: `LINKEDIN_ADS_ACCESS_TOKEN`
3. Auto-detected file: `~/.config/linkedin-ads-cli/credentials.json`

Required OAuth scopes depend on the commands used:
- `r_ads` -- read ad accounts and campaigns
- `r_ads_reporting` -- read ad analytics
- `r_organization_social` -- read organization data

Before running any command, verify credentials are configured by running `linkedin-ads-cli me`. If it fails with a credentials error, ask the user to set up authentication.

## Entity hierarchy

```
Organization (Company Page)
 +-- Ad Account (urn:li:sponsoredAccount:XXXXX)
      +-- Campaign Group
      |    +-- Campaign
      |         +-- Creative
      +-- Matched Audience (DMP Segment)
      +-- Conversion Rule
      +-- Insight Tag
      +-- Lead Gen Form
```

LinkedIn uses URN format for IDs (e.g., `urn:li:sponsoredAccount:123456`). The CLI accepts both full URNs and plain numeric IDs for all commands that take entity IDs.

When chaining commands, extract the numeric ID from URNs (the part after the last colon). For example, `organization-acls` returns organization URNs like `urn:li:organization:12345678` -- use `12345678` with the `organization` command.

Most list commands require the parent entity ID. Start with `me` to get your profile, then `organization-acls` to find organizations you manage, then `accounts` to find ad accounts.

## Monetary values

The analytics API returns monetary fields as-is from LinkedIn. The `costInLocalCurrency` field is in the account's local currency and `costInUsd` is in USD. Both are returned as decimal string values from the API in the major currency unit (e.g. `"244.85000"`).

## Output format

All commands output pretty-printed JSON by default. Use `--format compact` for single-line JSON (useful for piping).

Two pagination styles exist depending on the command:
- **Token-based:** uses `--page-size` and `--page-token` (look for `pageToken` in the response for the next page)
- **Offset-based:** uses `--count` and `--start` (increment `--start` by `--count` for the next page)

## Commands reference

### User & organization discovery

```bash
# Authenticated user profile
linkedin-ads-cli me

# Get an organization (company page) by numeric ID
linkedin-ads-cli organization 12345678

# List organizations the authenticated user administers
linkedin-ads-cli organization-acls
linkedin-ads-cli organization-acls --role ADMINISTRATOR
linkedin-ads-cli organization-acls --count 50 --start 0
```

`organization-acls` options:
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)
- `--role <role>` -- filter by role: ADMINISTRATOR, DIRECT_SPONSORED_CONTENT_POSTER, etc.

### Ad accounts

```bash
# List ad accounts
linkedin-ads-cli accounts
linkedin-ads-cli accounts --search "My Company"
linkedin-ads-cli accounts --page-size 50

# Get a specific ad account (numeric ID or full URN)
linkedin-ads-cli account 123456789
linkedin-ads-cli account urn:li:sponsoredAccount:123456789

# List users with access to an ad account
linkedin-ads-cli account-users 123456789
linkedin-ads-cli account-users 123456789 --count 50 --start 0
```

`accounts` options (token-based pagination):
- `--page-size <n>` -- results per page (default 100)
- `--page-token <token>` -- page token for pagination
- `--search <query>` -- search by account name or ID

`account-users` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)

### Campaign groups & campaigns

```bash
# List campaign groups for an ad account
linkedin-ads-cli campaign-groups 123456789
linkedin-ads-cli campaign-groups 123456789 --page-size 50

# Get a specific campaign group
linkedin-ads-cli campaign-group 987654321

# List campaigns for an ad account
linkedin-ads-cli campaigns 123456789
linkedin-ads-cli campaigns 123456789 --status ACTIVE
linkedin-ads-cli campaigns 123456789 --campaign-group 987654321

# Get a specific campaign
linkedin-ads-cli campaign 111222333
```

`campaign-groups` options (token-based pagination):
- `--page-size <n>` -- results per page (default 100)
- `--page-token <token>` -- page token for pagination

`campaigns` options (token-based pagination):
- `--page-size <n>` -- results per page (default 100)
- `--page-token <token>` -- page token for pagination
- `--status <status>` -- filter by status: ACTIVE, PAUSED, ARCHIVED, COMPLETED, CANCELED, DRAFT
- `--campaign-group <id>` -- filter by campaign group ID

### Creatives

```bash
# List creatives for an ad account
linkedin-ads-cli creatives 123456789
linkedin-ads-cli creatives 123456789 --campaign 111222333

# Get a specific creative
linkedin-ads-cli creative 444555666
```

`creatives` options (token-based pagination):
- `--page-size <n>` -- results per page (default 100)
- `--page-token <token>` -- page token for pagination
- `--campaign <campaign-id>` -- filter by campaign ID

### Analytics

The `analytics` command is the primary tool for performance analysis. It requires an account ID, a date range, and supports pivot breakdowns.

```bash
# Basic analytics for a date range
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31

# Daily granularity with campaign pivot
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31 --granularity DAILY --pivot CAMPAIGN

# Monthly granularity with campaign group pivot
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-06-30 --granularity MONTHLY --pivot CAMPAIGN_GROUP

# Account-level aggregate
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31 --granularity ALL --pivot ACCOUNT

# Filter by specific campaigns
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31 --campaign-ids 111222333,444555666

# Filter by campaign groups
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31 --campaign-group-ids 987654321

# Custom metric fields
linkedin-ads-cli analytics 123456789 --start-date 2026-01-01 --end-date 2026-01-31 --fields impressions,clicks,costInUsd
```

`analytics` options:
- `--start-date <date>` -- start date in YYYY-MM-DD format (**required**)
- `--end-date <date>` -- end date in YYYY-MM-DD format (**required**)
- `--granularity <gran>` -- time granularity: DAILY, MONTHLY, ALL (default DAILY)
- `--pivot <pivot>` -- pivot dimension: CAMPAIGN, CAMPAIGN_GROUP, CREATIVE, ACCOUNT (default CAMPAIGN)
- `--campaign-ids <ids>` -- filter by campaign IDs (comma-separated, numeric or URN)
- `--campaign-group-ids <ids>` -- filter by campaign group IDs (comma-separated, numeric or URN)
- `--fields <fields>` -- metric fields (comma-separated)

Default metric fields (when `--fields` is not specified): `impressions`, `clicks`, `costInLocalCurrency`, `costInUsd`, `externalWebsiteConversions`, `likes`, `comments`, `shares`, `follows`, `videoViews`

The CLI passes `--fields` and `--pivot` values directly to the LinkedIn API without validation. Additional fields and pivot values beyond the documented defaults may be available. Refer to the [LinkedIn Ad Analytics API docs](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting) for the full list.

### Audiences & targeting

```bash
# List matched audiences (DMP segments) for an ad account
linkedin-ads-cli audiences 123456789
linkedin-ads-cli audiences 123456789 --count 50 --start 0

# Get estimated audience size for targeting criteria
linkedin-ads-cli audience-counts 123456789

# List available targeting facets (industries, job titles, locations, etc.)
linkedin-ads-cli targeting-facets
```

`audiences` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)

`audience-counts` takes only the account ID argument (no additional options).

`targeting-facets` takes no arguments.

### Conversions & tracking

```bash
# List conversion rules for an ad account
linkedin-ads-cli conversion-rules 123456789
linkedin-ads-cli conversion-rules 123456789 --count 50

# List LinkedIn Insight Tags for an ad account
linkedin-ads-cli insight-tags 123456789
linkedin-ads-cli insight-tags 123456789 --count 50
```

`conversion-rules` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)

`insight-tags` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)

### Lead gen

```bash
# List Lead Gen forms for an ad account
linkedin-ads-cli lead-gen-forms 123456789
linkedin-ads-cli lead-gen-forms 123456789 --count 50

# List form responses (submissions) for an ad account
linkedin-ads-cli lead-form-responses 123456789
linkedin-ads-cli lead-form-responses 123456789 --form 777888999
linkedin-ads-cli lead-form-responses 123456789 --start-time 1709251200000 --end-time 1711929600000
```

`lead-gen-forms` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)

`lead-form-responses` options (offset-based pagination):
- `--count <n>` -- results per page (default 100)
- `--start <n>` -- start index (default 0)
- `--form <form-id>` -- filter by form ID (numeric or URN)
- `--start-time <time>` -- filter responses after this time (epoch milliseconds)
- `--end-time <time>` -- filter responses before this time (epoch milliseconds)

### Forecasting

```bash
# Get budget recommendations for a campaign
linkedin-ads-cli budget-recommendations 111222333

# Get ad delivery forecasts for an account
linkedin-ads-cli ad-forecasts 123456789
```

`budget-recommendations` takes a campaign ID (numeric or URN). No additional options.

`ad-forecasts` takes an account ID (numeric or URN). No additional options.

## Workflow guidance

### When the user asks for a quick overview

1. Run `linkedin-ads-cli accounts` to find accessible ad accounts
2. Use `analytics` with a recent date range and `--granularity ALL --pivot ACCOUNT` for a performance snapshot
3. Present the data with key metrics (impressions, clicks, cost, conversions)

### When the user asks for deep analysis

1. Start with account-level analytics using `--granularity ALL --pivot ACCOUNT`
2. Add `--pivot CAMPAIGN_GROUP` to identify top/bottom campaign groups
3. Drill down with `--pivot CAMPAIGN` for individual campaign performance
4. Use `--granularity DAILY` with `--pivot CAMPAIGN` for daily trends to spot anomalies
5. Filter specific campaigns with `--campaign-ids` for detailed analysis
6. Cross-reference with `creatives` to review ad content

### When the user asks about creative performance

1. Run `analytics` with `--pivot CREATIVE` to get creative-level metrics
2. Use `creatives` to list creatives for the account
3. Use `creative` to inspect the actual creative content

### When the user asks about audience and targeting

1. Use `audiences` to see matched audiences (DMP segments) and their details
2. Use `audience-counts` to get estimated audience size for targeting criteria
3. Use `targeting-facets` to explore available targeting dimensions (industries, job titles, locations)

### When the user asks about conversion tracking

1. Run `conversion-rules` to list conversion rules for the account
2. Run `insight-tags` to check active Insight Tags
3. Use `analytics` with `externalWebsiteConversions` in `--fields` to see conversion metrics

### When the user asks about lead gen

1. Use `lead-gen-forms` with the account ID to list forms
2. Use `lead-form-responses` with the account ID to retrieve submissions
3. Filter by specific form with `--form` or by time range with `--start-time` / `--end-time`

### When the user asks about budget planning

1. Use `budget-recommendations` with a campaign ID to get LinkedIn's budget suggestions
2. Use `ad-forecasts` with an account ID to get delivery forecasts
3. Combine with `analytics` historical data to compare forecasts against actual performance

## Error handling

- **Authentication errors** -- ask the user to verify their access token and OAuth scopes
- **"No credentials found"** -- the user needs to set `LINKEDIN_ADS_ACCESS_TOKEN`, use `--credentials`, or place credentials at `~/.config/linkedin-ads-cli/credentials.json`
- **Empty analytics** -- check the date range, ensure the account had active campaigns in the period, and verify the pivot dimension is appropriate
- **Permission errors** -- different commands require different scopes (`r_ads`, `r_ads_reporting`, `r_organization_social`); check the required scopes list above
- **URN format issues** -- the CLI accepts both plain numeric IDs and full URN format (e.g., `123456789` or `urn:li:sponsoredAccount:123456789`)

## API documentation references

- [linkedin-ads-cli documentation](https://github.com/Bin-Huang/linkedin-ads-cli)
- [LinkedIn Marketing API overview](https://learn.microsoft.com/en-us/linkedin/marketing/)
- [Ad Accounts API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-accounts)
- [Ad Analytics API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads-reporting/ads-reporting)
- [Campaign Management](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/account-structure/create-and-manage-campaigns)
- [Lead Gen Forms API](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/ads/advertising-targeting/lead-generation)
