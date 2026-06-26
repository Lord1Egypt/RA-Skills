---
name: insightfulpipe
description: "Query and manage marketing data across 40+ platforms — Google Analytics, Google Ads, Facebook Ads, Instagram, Shopify, HubSpot, Klaviyo, TikTok, LinkedIn, and more."
homepage: https://insightfulpipe.com
metadata:
  {
    "openclaw":
      {
        "emoji": "📊",
        "requires": { "bins": ["insightfulpipe"], "env": ["INSIGHTFULPIPE_TOKEN"] },
        "install":
          [
            {
              "id": "node",
              "kind": "node",
              "package": "insightfulpipe",
              "bins": ["insightfulpipe"],
              "label": "Install InsightfulPipe CLI (npm)",
            },
          ],
      },
  }
---

## Install InsightfulPipe if it doesn't exist

```bash
npm install -g insightfulpipe
```

npm release: https://www.npmjs.com/package/insightfulpipe

---

| Property | Value |
|----------|-------|
| **name** | insightfulpipe |
| **description** | Query marketing data across analytics, ads, social, ecommerce, and SEO platforms |
| **allowed-tools** | Bash(insightfulpipe:*) |

---

## Authentication

The `INSIGHTFULPIPE_TOKEN` environment variable is expected to be pre-configured. If a command fails with "Invalid token" or "Not authenticated", inform the user that their token needs to be configured.

---

## Core Workflow

Every query follows: discover → schema → execute. Read operations (query) can run directly. Write operations (action) should be confirmed with the user before executing.

```bash
# 1. Get account IDs (workspace_id, brand_id, source IDs)
insightfulpipe accounts --platform <platform> --json

# 2. See available actions
insightfulpipe helper <platform>

# 3. Get request body schema for specific actions
insightfulpipe helper <platform> --actions <action1>,<action2>

# 4. Execute read query
insightfulpipe query <platform> -b '{"action":"<action>","workspace_id":<id>,"brand_id":<id>,...}'

# 5. Execute write operation (requires --yes)
insightfulpipe action <platform> -b '{"action":"<action>",...}' --yes
```

---

## Platform Examples

### Google Analytics — Top Pages

```bash
insightfulpipe accounts --platform google-analytics --json
insightfulpipe helper google-analytics --actions pages
insightfulpipe query google-analytics -b '{
  "action": "pages",
  "workspace_id": xxx,
  "brand_id": xxx,
  "property_id": "properties/xxx",
  "dimensions": ["pagePath"],
  "metrics": ["screenPageViews", "activeUsers"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-20",
  "limit": 10
}'
```

### Google Analytics — Traffic Sources

```bash
insightfulpipe query google-analytics -b '{
  "action": "traffic_sources",
  "workspace_id": xxx,
  "brand_id": xxx,
  "property_id": "properties/xxx",
  "dimensions": ["sessionSource", "sessionMedium"],
  "metrics": ["sessions", "totalUsers", "bounceRate"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-20"
}'
```

### Google Analytics — Freeform Report

```bash
insightfulpipe query google-analytics -b '{
  "action": "get_report",
  "workspace_id": xxx,
  "brand_id": xxx,
  "property_id": "properties/xxx",
  "dimensions": ["date", "country"],
  "metrics": ["activeUsers", "sessions"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-20"
}'
```

### Google Search Console — Top Queries

```bash
insightfulpipe query google-search-console -b '{
  "action": "search_analytics",
  "workspace_id": xxx,
  "brand_id": xxx,
  "site_url": "https://example.com/",
  "dimensions": ["query"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-20",
  "row_limit": 10
}'
```

### Google Search Console — Pages by Country

```bash
insightfulpipe query google-search-console -b '{
  "action": "search_analytics",
  "workspace_id": xxx,
  "brand_id": xxx,
  "site_url": "https://example.com/",
  "dimensions": ["page", "country"],
  "start_date": "2026-03-01",
  "end_date": "2026-03-20",
  "row_limit": 20
}'
```

### Google Sheets — Peek at Columns Then Query

```bash
# First peek to see column names
insightfulpipe query google-sheets -b '{
  "action": "get_sheet_peak",
  "workspace_id": xxx,
  "brand_id": xxx,
  "spreadsheet_id": "xxx",
  "sheet_id": "0"
}'

# Then query with filters using exact column names from peek
insightfulpipe query google-sheets -b '{
  "action": "query_sheet_data",
  "workspace_id": xxx,
  "brand_id": xxx,
  "spreadsheet_id": "xxx",
  "sheet_id": "0",
  "select": "Name,Email,Status",
  "where": "Status=Active",
  "limit": 50
}'
```

### Google Sheets — Write Cells

```bash
insightfulpipe action google-sheets -b '{
  "action": "update_cells",
  "workspace_id": xxx,
  "brand_id": xxx,
  "spreadsheet_id": "xxx",
  "sheet_id": "0",
  "range": "A1:C2",
  "values": [["Name", "Email", "Status"], ["John", "john@example.com", "Active"]]
}' --yes
```

### Shopify — Recent Orders

```bash
insightfulpipe query shopify -b '{
  "action": "get_orders",
  "workspace_id": xxx,
  "brand_id": xxx,
  "status": "any",
  "limit": 10
}'
```

### Shopify — Products

```bash
insightfulpipe query shopify -b '{
  "action": "get_products",
  "workspace_id": xxx,
  "brand_id": xxx,
  "limit": 10
}'
```

### Any Other Platform

```bash
# Same pattern works for all platforms:
insightfulpipe helper <platform>                        # See actions
insightfulpipe helper <platform> --actions <action>     # Get body schema
insightfulpipe query <platform> -b '{...}'              # Execute
```

Supported platforms include: facebook-ads, instagram, tiktok-ads, tiktok-pages, linkedin-ads, linkedin-pages, hubspot, klaviyo, mailchimp, stripe, slack, telegram, and many more. Run `insightfulpipe platforms` to see the full list.

---

## Common Patterns

### Pattern 1: Pipe to jq

```bash
# Extract just page paths from GA response
insightfulpipe query google-analytics -b '{...}' | jq '.data[].pagePath'

# Get total sessions
insightfulpipe query google-analytics -b '{...}' | jq '[.data[].sessions] | add'
```

### Pattern 2: Compare Data Across Platforms

```bash
# GA traffic
GA=$(insightfulpipe query google-analytics -b '{
  "action": "traffic_sources", "workspace_id": xxx, "brand_id": xxx,
  "property_id": "properties/xxx",
  "dimensions": ["sessionSource"], "metrics": ["sessions"],
  "start_date": "2026-03-01", "end_date": "2026-03-20"
}')

# GSC queries
GSC=$(insightfulpipe query google-search-console -b '{
  "action": "search_analytics", "workspace_id": xxx, "brand_id": xxx,
  "site_url": "https://example.com/",
  "dimensions": ["query"],
  "start_date": "2026-03-01", "end_date": "2026-03-20", "row_limit": 10
}')

echo "$GA" | jq '.data[:5]'
echo "$GSC" | jq '.data[:5]'
```

### Pattern 3: Write Operations

```bash
# Always use "action" (not "query") and --yes for writes
insightfulpipe action google-sheets -b '{
  "action": "create_sheet",
  "workspace_id": xxx,
  "brand_id": xxx,
  "spreadsheet_id": "xxx",
  "title": "New Sheet"
}' --yes
```

### Pattern 4: Use Prompts for Guided Analysis

```bash
insightfulpipe prompts google-analytics            # List templates
insightfulpipe prompts google-analytics --id 12    # Get specific prompt
```

---

## Gotchas

1. **Never guess the request body** — always run `helper <platform> --actions <action>` first.
2. **Replace ALL "xxx" placeholders** — get real values from `accounts --platform <platform> --json`.
3. **GA property_id needs "properties/" prefix** — use `"properties/510157516"` not `"510157516"`.
4. **Date format is YYYY-MM-DD** — use `"2026-03-20"` not `"2026-03-20T00:00:00Z"`.
5. **Use `query` for reads, `action --yes` for writes** — using the wrong one will fail.
6. **Google Sheets: peek before query** — call `get_sheet_peak` first to see column names.
7. **Different platforms have different source IDs** — GA uses `property_id`, GSC uses `site_url`, Shopify uses `shop_domain`, Facebook Ads uses `ad_account_id`.
8. **Empty data is not an error** — `{"status":"success","data":[]}` means no data matched your filters.
9. **Token should be pre-configured** — if auth fails, inform the user to check their token configuration.
10. **Confirm write operations with the user** — always ask before running `insightfulpipe action`. Read operations via `insightfulpipe query` are safe to run directly.

---

## All Commands

```bash
# Discovery
insightfulpipe platforms                              # All supported platforms
insightfulpipe accounts --platform <platform> --json  # Account IDs
insightfulpipe sources --platform <platform>          # Sources with IDs
insightfulpipe brands --workspace <id>                # Brand metadata
insightfulpipe whoami                                 # Current user
insightfulpipe doctor                                 # Check auth

# Schema
insightfulpipe helper <platform>                      # List actions
insightfulpipe helper <platform> --actions <a1>,<a2>  # Body schema

# Execute
insightfulpipe query <platform> -b '<json>'           # Read data
insightfulpipe query <platform> -f file.json          # Read from file
insightfulpipe action <platform> -b '<json>' --yes    # Write data

# Prompts
insightfulpipe prompts <platform>                     # List templates
insightfulpipe prompts <platform> --id <id>           # Get prompt
```
