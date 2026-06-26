---
name: magento2
description: >
  Manage a Magento 2 / Adobe Commerce store via REST API. Use for orders,
  catalog, customers, inventory, promotions, and sales reporting. It can also
  discover and interact with custom modules (like blogs) by exploring the
  system's modules and REST schema. Triggers on requests like "show me today's
  orders", "update product stock", "check installed modules", "call custom api",
  "morning brief", "store health", "inventory risk", "stockout", "promotion audit",
  "stuck orders", "order exceptions", "pricing issues", or anything referencing
  a Magento store.
version: 1.1.0
metadata:
  openclaw:
    emoji: "🛒"
    homepage: https://github.com/caravanglory/openclaw-magento2
    primaryEnv: MAGENTO_BASE_URL
    requires:
      env:
        - MAGENTO_BASE_URL
        - MAGENTO_CONSUMER_KEY
        - MAGENTO_CONSUMER_SECRET
        - MAGENTO_ACCESS_TOKEN
        - MAGENTO_ACCESS_TOKEN_SECRET
      bins:
        - python3
    install:
      - kind: uv
        packages:
          - requests
          - requests-oauthlib
          - pandas
          - tabulate
        label: "Install Python dependencies (uv)"
---

# Magento 2 Skill

Connect to one or more Magento 2 / Adobe Commerce stores via REST API using OAuth 1.0a.

## Authentication

All requests are signed with OAuth 1.0a. Credentials are read from environment variables — never ask the user to paste them in chat.

### Single site (default)

- `MAGENTO_BASE_URL` — e.g. `https://store.example.com`
- `MAGENTO_CONSUMER_KEY`
- `MAGENTO_CONSUMER_SECRET`
- `MAGENTO_ACCESS_TOKEN`
- `MAGENTO_ACCESS_TOKEN_SECRET`

### Multi-site setup

To connect to additional stores, define credentials with a site suffix (`MAGENTO_<VAR>_<SITE>`):

```
MAGENTO_BASE_URL_US=https://us.store.com
MAGENTO_CONSUMER_KEY_US=...
MAGENTO_CONSUMER_SECRET_US=...
MAGENTO_ACCESS_TOKEN_US=...
MAGENTO_ACCESS_TOKEN_SECRET_US=...

MAGENTO_BASE_URL_EU=https://eu.store.com
MAGENTO_CONSUMER_KEY_EU=...
...
```

All scripts accept `--site <alias>` to target a specific store. When omitted, the default (unsuffixed) credentials are used.

```
python3 orders.py list --site us --limit 10
python3 system.py sites            # list all configured sites
```

### Optional env vars

- `MAGENTO_TIMEOUT` — Default is 30 seconds. Supports per-site override: `MAGENTO_TIMEOUT_US`.
- `MAGENTO_DEBUG` — Set to 1 to enable verbose logging to stderr.

All scripts import the shared client from `scripts/magento_client.py`. Never construct raw HTTP requests inline — always use the client.

## Available commands

Run scripts with: `python3 <skill_dir>/scripts/<script>.py [args]`

### Orders — `scripts/orders.py`

```
# List recent orders (default: last 20)
python3 orders.py list [--limit N] [--status pending|processing|complete|canceled|closed|holded|payment_review]

# Get a single order
python3 orders.py get <order_id>

# Update order status
python3 orders.py update-status <order_id> <status>

# Cancel an order
python3 orders.py cancel <order_id>

# Ship an order (optional: add tracking number and carrier)
python3 orders.py ship <order_id> [--track N] [--carrier carrier_code] [--title title]

# Invoice an order
python3 orders.py invoice <order_id>
```

### Catalog — `scripts/catalog.py`

```
# Search products
python3 catalog.py search <query> [--limit N]

# Get product by SKU
python3 catalog.py get <sku>

# Update product price
python3 catalog.py update-price <sku> <price>

# Update product name / description
python3 catalog.py update-attribute <sku> <attribute> <value>

# Enable or disable a product
python3 catalog.py update-status <sku> {enabled|disabled}

# Delete a product
python3 catalog.py delete <sku>

# List categories
python3 catalog.py categories
```

### Customers — `scripts/customers.py`

```
# Search customers by email or name
python3 customers.py search <query> [--limit N]

# Get customer by ID
python3 customers.py get <customer_id>

# Get customer orders
python3 customers.py orders <customer_id>

# Update customer group
python3 customers.py update-group <customer_id> <group_id>
```

### Inventory — `scripts/inventory.py`

```
# Check stock for a SKU
python3 inventory.py check <sku>

# Update stock quantity
python3 inventory.py update <sku> <qty>

# List low-stock products (below threshold)
python3 inventory.py low-stock [--threshold N]

# Bulk stock check from a comma-separated SKU list
python3 inventory.py bulk-check <sku1,sku2,...>
```

#### Multi-Source Inventory (MSI)

Requires Magento 2.3+ with Inventory modules enabled.

```
# List inventory sources (warehouses)
python3 inventory.py sources [--limit N]

# Get details for a specific source
python3 inventory.py source-get <source_code>

# List source items (stock per source) — filter by SKU, source, or both
python3 inventory.py source-items --sku <sku> [--source <source_code>] [--limit N]

# Update quantity for a SKU at a specific source
python3 inventory.py source-item-update <sku> <source_code> <qty>

# Get salable quantity for a SKU in a stock
python3 inventory.py salable-qty <sku> <stock_id>

# Check if a product is salable in a stock
python3 inventory.py is-salable <sku> <stock_id>

# List inventory stocks (logical groupings)
python3 inventory.py stocks [--limit N]
```

### Promotions — `scripts/promotions.py`

```
# List active cart price rules
python3 promotions.py list [--active-only]

# Get a rule by ID
python3 promotions.py get <rule_id>

# Create a coupon code for an existing rule
python3 promotions.py create-coupon <rule_id> <code> [--uses N]

# Disable a promotion rule
python3 promotions.py disable <rule_id>

# List coupon usage stats
python3 promotions.py coupon-stats <coupon_code>
```

### Reporting — `scripts/reports.py`

```
# Sales summary for a date range
python3 reports.py sales --from YYYY-MM-DD --to YYYY-MM-DD

# Revenue by product (top N)
python3 reports.py top-products [--limit N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Revenue by customer (top N)
python3 reports.py top-customers [--limit N] [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Order status breakdown
python3 reports.py order-status [--from YYYY-MM-DD] [--to YYYY-MM-DD]

# Inventory value report
python3 reports.py inventory-value
```

### System & Discovery — `scripts/system.py`

```
# Check API connection status
python3 system.py status

# List installed modules
python3 system.py modules

# Inspect REST schema
python3 system.py schema

# List all configured sites
python3 system.py sites

# Cache management
python3 system.py cache-list
python3 system.py cache-flush [--types ID1,ID2]
```

### Custom API — `scripts/custom_api.py`

Use this for interacting with discovered custom endpoints.

```
# Call custom endpoints (e.g. blog module)
python3 custom_api.py GET <path> [--params '{"key": "value"}']
python3 custom_api.py POST <path> --data '{"body": "json"}'
```

### Morning Brief — `scripts/morning_brief.py`

Generate a daily store health summary across sales, orders, inventory, promotions, and customers.

```
# Generate morning brief (default: last 24 hours)
python3 morning_brief.py brief [--site SITE] [--hours 24] [--stock-threshold 10]

# JSON output for programmatic consumption
python3 morning_brief.py brief --format json
```

### Diagnostics — `scripts/diagnose.py`

Deep-dive analysis for specific store issues.

```
# Inventory risk radar with velocity-based stockout prediction
python3 diagnose.py inventory-risk [--days 7] [--threshold 10] [--limit 50]

# Audit promotions for expired rules, missing coupons, exhausted limits
python3 diagnose.py promotion-audit [--warn-hours 48]

# Find stuck orders (pending too long, payment review, processing delay)
python3 diagnose.py order-exceptions [--pending-hours 24] [--processing-hours 48]

# Detect pricing anomalies (zero price, negative price, inverted specials)
python3 diagnose.py pricing-anomaly [--limit 50]

# JSON output available for all subcommands
python3 diagnose.py inventory-risk --format json
```

### Bulk Operations

Batch update prices, stock, and shipments via CSV or inline input.

```
# Bulk update prices (preview mode)
python3 catalog.py bulk-update-price --items "SKU1:29.99,SKU2:49.99"
python3 catalog.py bulk-update-price --csv prices.csv

# Execute bulk price changes
python3 catalog.py bulk-update-price --csv prices.csv --execute

# Bulk update stock
python3 inventory.py bulk-update --items "SKU1:100,SKU2:50"
python3 inventory.py bulk-update --csv stock.csv --execute

# Bulk ship orders
python3 orders.py bulk-ship --csv shipments.csv --execute
```

## Output format

All scripts print a UTF-8 table (via `tabulate`) or a JSON summary to stdout. When presenting results to the user, render them as a markdown table. For single-record lookups, format as a definition list.

## Error handling

Scripts exit with code 1 on API errors and print a JSON error to stderr:
```json
{ "error": "404 Not Found", "message": "No such entity with id = 99", "url": "..." }
```

If a script fails, read stderr, extract the `message` field, and tell the user plainly what went wrong. Do not retry automatically unless the user asks.

## Rules

- Never expose OAuth credentials in chat output, logs, or summaries.
- For any **write operation** (cancel, delete, update-price, update-status, update-group, cache-flush, ship, invoice, create-coupon, disable, source-item-update, and all POST/PUT/DELETE via custom_api.py), always repeat the full command back to the user and wait for explicit confirmation before executing.
- **Read-only operations** (list, get, search, check, status, modules, schema, cache-list, reports) may be executed directly without confirmation.
- When a date range is not specified for reports, default to the last 30 days.
- Monetary values are returned in the store's base currency — include the currency code in output.
- **Multi-site**: When multiple sites are configured, always confirm which site the user intends before executing write operations. Use `system.py sites` to discover available sites.
- **Production Safety**: After performing updates to products or prices, it is recommended to run `system.py cache-flush` if the changes don't appear on the frontend.
- **Morning Brief** and **diagnose** commands are read-only — they may be executed directly without confirmation.
- After generating a morning brief, proactively recommend relevant `diagnose.py` subcommands based on the findings.
- **Bulk operations**: Always preview first (default), then require `--execute` flag and explicit user confirmation. Follow preview templates in `references/workflows.md`.
- **Scenarios**: For detailed routing guidance, see `references/workflows.md`.