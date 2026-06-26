

<h3 align="center">AI-Native Agentic Commerce — 10 MCP tools for discovery, catalog, and ordering</h3>

<p align="center">
  <a href="https://smithery.ai/server/lobstersearch"><img src="https://smithery.ai/badge/lobstersearch" alt="Smithery" /></a>
  <img src="https://img.shields.io/badge/MCP-StreamableHTTP-purple?style=flat-square" alt="Transport" />
  <img src="https://img.shields.io/badge/Tools-10-green?style=flat-square" alt="Tools" />
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=flat-square" alt="License" />
</p>

<p align="center">
  <b>No API key required. No setup. Connect and shop.</b>
</p>

---

## Quick Start

### Claude (Web & Desktop)

1. Go to **Settings → Connectors** (or visit [claude.ai/settings/connectors](https://claude.ai/settings/connectors))
2. Click **"Add custom connector"**
3. Paste: `https://mcp.lobstersearch.ai/mcp`
4. Click **Add**

> Available on Pro, Max, Team, and Enterprise plans.

### Claude Code

```bash
claude mcp add lobstersearch --transport streamable-http https://mcp.lobstersearch.ai/mcp
```

### ChatGPT

1. Enable **Developer Mode** in Settings → Advanced
2. Go to **Settings → Connectors**
3. Click **"Create"**, name it `LobsterSearch`
4. Set the MCP server URL to: `https://mcp.lobstersearch.ai/mcp`
5. Save

> Requires ChatGPT Plus or Pro. Works in Chat and Deep Research modes.

### Gemini CLI

Add to your `~/.gemini/settings.json`:

```json
{
  "mcpServers": {
    "lobstersearch": {
      "httpUrl": "https://mcp.lobstersearch.ai/mcp"
    }
  }
}
```

### OpenClaw

```bash
clawhub install lobstersearch
```

### Cursor / Windsurf / Any MCP Client

```json
{
  "mcpServers": {
    "lobstersearch": {
      "url": "https://mcp.lobstersearch.ai/mcp",
      "transport": "streamable-http"
    }
  }
}
```

---

## What is LobsterSearch?

LobsterSearch is an **agentic commerce platform** — a single MCP endpoint that lets AI agents discover local businesses, browse their catalogs, and complete purchases with real payment processing.

Unlike traditional directories, LobsterSearch is built for the **agent-to-commerce** workflow:

- **Search** with natural language and get structured, actionable results
- **Browse** real product catalogs with variant-level detail (sizes, colors, options)
- **Order** with atomic stock reservation, Stripe Checkout payment, and full lifecycle tracking
- **Every response includes `next_actions`** — the agent always knows what to do next

It's a hosted service. No setup, no API key, no self-hosting. Connect your MCP client and start shopping.

---

## Tools Reference

### Discovery (3 tools)

#### `search`

Natural language search with 4-step fallback chain for maximum recall. Returns structured results with quality scores.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Natural language query, e.g. `"best ramen in Bugis"` |
| `business_type` | string | No | Filter by type (e.g., `restaurant`, `salon`) |
| `city` | string | No | City name filter |
| `limit` | number | No | 1-20, default `10` |

<details>
<summary>Example response</summary>

```json
{
  "results": [
    {
      "id": "a1b2c3d4-...",
      "name": "Ichiran Ramen",
      "business_type": "restaurant",
      "description": "Premium tonkotsu ramen",
      "quality_score": 0.92
    }
  ],
  "total": 3,
  "next_actions": [
    { "tool": "details", "description": "Get full profile", "params": { "id": "a1b2c3d4-..." } },
    { "tool": "browse_catalog", "description": "Browse menu", "params": { "business_id": "a1b2c3d4-..." } }
  ]
}
```

</details>

---

#### `details`

Full business profile by slug or ID — contact info, hours, quality scores, catalog offerings with variants.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `slug` | string | No | Business slug (e.g., `tanjong-rhu-dental`) |
| `id` | string | No | Business UUID |

---

#### `compare`

Side-by-side comparison of 2-5 businesses.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `business_ids` | array | Yes | 2-5 business UUIDs to compare |

---

### Catalog (3 tools)

#### `browse_catalog`

Browse a business's product/service catalog. Filter by category, sort by name or price.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `business_id` | string | Yes | Business UUID |
| `category` | string | No | Filter by category |
| `sort_by` | string | No | `name`, `price_low`, or `price_high` |

---

#### `get_product_details`

Deep product view — all variant dimensions, combinations, prices, SKUs, stock levels.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `offering_id` | string | Yes | Product/offering UUID |

---

#### `check_availability`

Real-time stock check for a product or specific variant combination.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `offering_id` | string | Yes | Product/offering UUID |
| `options` | object | No | Variant options, e.g. `{"Color":"Black","Size":"Large"}` |

---

### Commerce (4 tools)

#### `create_order`

Create a draft order with atomic stock reservation. Specify items by offering + variant + quantity.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `business_id` | string | Yes | Business UUID |
| `items` | array | Yes | Array of `{offering_id, variant_id?, quantity}` |
| `customer_email` | string | No | Email for notifications |
| `customer_name` | string | No | Customer name |
| `customer_notes` | string | No | Notes for the business |

---

#### `confirm_order`

Confirm draft → generate Stripe Checkout payment link (30-min expiry).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `order_id` | string | Yes | Order UUID from `create_order` |

---

#### `get_order_status`

Full order status, payment state, fulfillment progress, and event timeline.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `order_id` | string | Yes | Order UUID |

---

#### `cancel_order`

Cancel with automatic refund (if paid) and stock restoration.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `order_id` | string | Yes | Order UUID |
| `reason` | string | No | Reason for cancellation |

---

### Order Lifecycle

```
DRAFT → CONFIRMED → PAID → ACCEPTED → PREPARING → FULFILLED → COMPLETED
                                                              ↘ CANCELLED (at any stage, with auto-refund if paid)
```

---

## Example Flows

### 1. Discovery → Purchase

```
Agent: search("best pasta restaurant in Bugis")
  → Gets list of restaurants with IDs and quality scores

Agent: details(slug: "mama-mia-pasta")
  → Gets full profile, hours, catalog overview

Agent: browse_catalog(business_id: "abc-123")
  → Gets all menu items with prices and variants

Agent: get_product_details(offering_id: "pasta-001")
  → Gets variant details: sizes (Regular, Large), add-ons

Agent: check_availability(offering_id: "pasta-001", options: {"Size": "Large"})
  → Confirms availability and price

Agent: create_order(business_id: "abc-123", items: [{offering_id: "pasta-001", variant_id: "v-large", quantity: 2}])
  → Draft order created, stock reserved

Agent: confirm_order(order_id: "order-xyz")
  → Stripe Checkout URL returned for payment

Agent: get_order_status(order_id: "order-xyz")
  → Tracks through: paid → accepted → preparing → fulfilled
```

### 2. Quick Comparison

```
Agent: search("dental clinic near Tanjong Rhu")
  → Gets 3 clinics

Agent: compare(business_ids: ["clinic-1", "clinic-2", "clinic-3"])
  → Side-by-side comparison of services, ratings, prices
```

### 3. Availability Check Before Ordering

```
Agent: check_availability(offering_id: "phone-case-001", options: {"Color": "Black", "Size": "iPhone 15"})
  → { available: true, stock: 12, price: 29.90 }

Agent: check_availability(offering_id: "phone-case-001", options: {"Color": "Red", "Size": "iPhone 15"})
  → { available: false, stock: 0, retry_guidance: "Try a different color." }
```

---

## Response Format

Every tool response includes:

- **Structured data** — typed, consistent fields across all tools
- **`next_actions`** — array of suggested next steps the agent can take
- **Error responses** — include `error` message and `retry_guidance` for agent resilience

```json
{
  "results": [...],
  "total": 5,
  "next_actions": [
    { "tool": "details", "description": "Get full profile for a business", "params": { "id": "..." } },
    { "tool": "browse_catalog", "description": "Browse their products", "params": { "business_id": "..." } }
  ]
}
```

---

## Platform Details

- **Region:** Singapore (ap-southeast-1)
- **Businesses:** Self-service onboarded, verified
- **Payments:** Stripe Connect (direct charge model)
- **Data freshness:** Real-time catalog and stock
- **Rate limits:** 30 reads/min, 5 writes/min per client
- **Protection:** Rate limiting + behavioral analysis + resource limits

---

## FAQ

**Is it free?**
Yes. The MCP endpoint is public and rate-limited.

**Do I need an API key?**
No. Connect directly — no authentication required.

**How fresh is the data?**
Businesses manage their own data in real-time. Catalog, pricing, and stock are always current.

**What transport does it use?**
StreamableHTTP — the current MCP standard. Not SSE.

**Can I self-host?**
No. LobsterSearch is a hosted service. Connect to the endpoint and let us handle the infrastructure.

---

## Links

- **Website:** [lobstersearch.ai](https://lobstersearch.ai)
- **MCP Endpoint:** `https://mcp.lobstersearch.ai/mcp`
- **Smithery:** [smithery.ai/server/lobstersearch](https://smithery.ai/server/lobstersearch)
- **OpenClaw:** `clawhub install lobstersearch`
- **Tool Schema:** [mcp.json](mcp.json)
- **Changelog:** [CHANGELOG.md](CHANGELOG.md)

---

<p align="center">
  <sub>Built by <a href="https://github.com/theoddbrick">theoddbrick</a> — Agentic commerce for the AI economy</sub>
</p>
