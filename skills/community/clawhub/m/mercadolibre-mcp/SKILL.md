---
name: mercadolibre-mcp
description: Complete MCP server for Mercado Libre seller operations — products, orders, pricing, stock, questions, ads, reputation, competitor analysis
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - ML_CLIENT_ID
        - ML_CLIENT_SECRET
        - ML_REFRESH_TOKEN
      bins:
        - node
    primaryEnv: ML_REFRESH_TOKEN
    emoji: "🛒"
    homepage: https://github.com/MarcosNahuel/mercadolibre-mcp
---

# Mercado Libre MCP Server

The first complete MCP server for Mercado Libre. 11 tools for seller operations — manage products, orders, pricing, stock, customer questions, advertising, reputation, and competitor intelligence.

## Setup

Two authentication modes:

### Option A: Direct token (recommended if you have n8n/cron managing refresh)

```
ML_ACCESS_TOKEN=APP_USR-...
ML_SITE_ID=MLA
```

### Option B: Auto-refresh (standalone, no external dependencies)

1. Create an app at [developers.mercadolibre.com](https://developers.mercadolibre.com)
2. Authorize via OAuth to get your refresh token
3. Set environment variables:

```
ML_CLIENT_ID=your_client_id
ML_CLIENT_SECRET=your_client_secret
ML_REFRESH_TOKEN=your_refresh_token
ML_SITE_ID=MLA
```

## Tools

### Read operations
- **list_products** — List all products/listings for a seller with price, stock, status, and thumbnails
- **get_orders** — Get orders/sales with buyer info, items, shipping, and payment details
- **list_questions** — List questions received on listings, filterable by status (unanswered/answered)
- **get_item_metrics** — Get visits, health score, conversion rate, and catalog status for a listing
- **get_reputation** — Get seller reputation: level, completed sales, claims, cancellations, handling time
- **search_competitors** — Search competitor products by keyword with price, seller, sales volume
- **get_categories** — Browse ML categories and required attributes for publishing

### Write operations
- **update_price** — Update listing price (returns before/after for confirmation)
- **update_stock** — Update available quantity (returns before/after for confirmation)
- **answer_question** — Answer a buyer question (public, visible to all buyers)
- **manage_ads** — Activate, pause, or check status of Product Ads

## Supported countries

Works with all Mercado Libre sites: MLA (Argentina), MLU (Uruguay), MLB (Brazil), MLC (Chile), MLM (Mexico), MCO (Colombia), and more.

## Features

- **OAuth2 auto-refresh** — Token renews automatically every 6 hours
- **Rate limiting** — Automatic retry with backoff when hitting API limits
- **Multi-get batching** — Fetches multiple items in batches of 20
- **Zod validation** — All inputs validated before calling the API
- **Clear error messages** — Human-readable errors in Spanish, not raw JSON

## Example prompts

- "List my active products"
- "Show me today's orders"
- "Update the price of MLA123456 to $5000"
- "What unanswered questions do I have?"
- "Search competitors for brake pads Toyota"
- "What category should I use for motorcycle parts?"
- "Activate ads on MLA123456 with $500/day budget"
- "How is my seller reputation?"

## License

MIT — by [TRAID](https://traid.ai)
