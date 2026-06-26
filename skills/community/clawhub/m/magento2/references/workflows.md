# AI Agent Workflow Reference

This document guides the AI agent on how to route user requests, handle write operations safely, and chain commands for maximum value.

## Scenario Routing

| User says | Command | Next step |
|-----------|---------|-----------|
| "morning brief" / "today's summary" / "store health" | `morning_brief.py brief` | Based on findings, suggest relevant `diagnose.py` subcommand |
| "low stock" / "running out" / "stockout risk" | `diagnose.py inventory-risk` | If risks found, suggest `inventory.py update` or `inventory.py bulk-update` |
| "promotion issues" / "coupon not working" / "discount check" | `diagnose.py promotion-audit` | If expired rules found, suggest `promotions.py disable` |
| "stuck orders" / "pending too long" / "order problems" | `diagnose.py order-exceptions` | Review specific orders with `orders.py get` |
| "price issues" / "zero price" / "pricing error" | `diagnose.py pricing-anomaly` | Fix with `catalog.py update-price` or `catalog.py bulk-update-price` |
| "batch update prices" / "bulk pricing" | `catalog.py bulk-update-price --csv` | After execute, suggest `system.py cache-flush` |
| "batch update stock" / "restock" | `inventory.py bulk-update --csv` | After execute, suggest `system.py cache-flush` |
| "batch ship" / "bulk ship orders" | `orders.py bulk-ship --csv` | Verify with `orders.py list --status processing` |
| "sales report" / "how are sales" | `reports.py sales` | Follow up with `reports.py top-products` for details |
| "show orders" / "recent orders" | `orders.py list` | Drill into specifics with `orders.py get <id>` |

## Chain Recommendations

After Morning Brief, use findings to suggest next steps:

```
Morning Brief finding → Recommended action
─────────────────────────────────────────────
"3 orders stuck in pending" → diagnose.py order-exceptions → orders.py get <id> → orders.py cancel or orders.py ship
"SKU X has low stock"      → diagnose.py inventory-risk → inventory.py bulk-update
"Rule #5 expired"          → diagnose.py promotion-audit → promotions.py disable
"No pricing issues"        → No action needed
```

## Write Operation Safety Matrix

| Operation | Risk Level | Needs Preview | Post-Action Cache Flush | Confirmation Required |
|-----------|-----------|---------------|------------------------|----------------------|
| `catalog.py update-price` | Medium | No (single item) | Recommended: config,block_html | Yes |
| `catalog.py bulk-update-price` | High | Yes (auto) | Recommended: config,block_html | Yes (on --execute) |
| `catalog.py update-attribute` | Medium | No | Recommended: config,block_html | Yes |
| `catalog.py update-status` | Medium | No | Recommended: full_page | Yes |
| `catalog.py delete` | Critical | No | Recommended: full_page,config | Yes |
| `inventory.py update` | Medium | No | Recommended: config | Yes |
| `inventory.py bulk-update` | High | Yes (auto) | Recommended: config | Yes (on --execute) |
| `inventory.py source-item-update` | Medium | No | Recommended: config | Yes |
| `orders.py cancel` | High | No | No | Yes |
| `orders.py ship` | Medium | No | No | Yes |
| `orders.py bulk-ship` | High | Yes (auto) | No | Yes (on --execute) |
| `orders.py invoice` | Medium | No | No | Yes |
| `orders.py update-status` | Medium | No | No | Yes |
| `promotions.py create-coupon` | Low | No | Recommended: config | Yes |
| `promotions.py disable` | Medium | No | Recommended: config,block_html | Yes |
| `system.py cache-flush` | Medium | No | N/A | Yes |
| `custom_api.py POST/PUT/DELETE` | Variable | No | Depends on endpoint | Yes |

## Bulk Operation Preview Template

Before executing any bulk write, show the user:

```
## Preview: [Operation Name]
**Scope:** N item(s) will be affected

| Identifier | Current | New | Change |
|-----------|---------|-----|--------|
| ... | ... | ... | ... |

⚠ Not found: [list of SKUs/orders not found]
To apply: re-run with --execute flag
```

After execution:

```
## Result: [Operation Name]
Updated: N | Failed: M | Total: T

[If failures, list them]
Tip: run system.py cache-flush to reflect changes.
```

## Environment Variable Defaults

Bulk operations and diagnostics respect these env vars (CLI args take precedence):

| Env Var | Default | Used By |
|---------|---------|---------|
| `OPENCLAW_STOCK_THRESHOLD` | 10 | morning_brief, diagnose inventory-risk |
| `OPENCLAW_PENDING_HOURS` | 24 | morning_brief, diagnose order-exceptions |
| `OPENCLAW_PROCESSING_HOURS` | 48 | diagnose order-exceptions |
| `OPENCLAW_WARN_HOURS` | 48 | diagnose promotion-audit |
| `OPENCLAW_DELAY_MS` | 200 | All bulk operations (delay between writes) |
