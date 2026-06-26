---
name: lobstersearch
description: AI-native agentic commerce — 10 MCP tools to discover businesses, browse product catalogs with variants, and complete purchases with Stripe payments. Built for AI agents that shop on behalf of users.
version: 2.0.0
metadata: {"openclaw":{"requires":{"bins":["curl"]},"emoji":"🦞","homepage":"https://lobstersearch.ai","categories":["commerce","shopping","business","discovery"]}}
---

# LobsterSearch — Agentic Commerce

LobsterSearch is an agentic commerce platform. AI agents can discover businesses, browse real product catalogs with variant-level detail, and complete purchases with Stripe Connect payments — all through a single MCP endpoint.

## MCP Server

**Endpoint:** `https://mcp.lobstersearch.ai/mcp`
**Transport:** StreamableHTTP
**Authentication:** None required (public, rate-limited)

### Configuration

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

## Tools (10 available)

### Discovery

#### search
Search for businesses with natural language. Uses a 4-step fallback chain (structured → tags → LLM interpret → LLM catalog scan) for maximum recall.

**Parameters:**
- `query` (string, required) — e.g. "best ramen in Bugis" or "dental clinic near Tanjong Rhu"
- `business_type` (string) — filter by type (e.g., restaurant, salon)
- `city` (string) — city name filter
- `limit` (number) — 1-20, default 10

#### details
Get full business profile by slug or ID. Returns contact info, hours, quality scores, and catalog offerings with variants.

**Parameters:**
- `slug` (string) — business slug (e.g., "tanjong-rhu-dental")
- `id` (string) — business UUID

#### compare
Side-by-side comparison of 2-5 businesses.

**Parameters:**
- `business_ids` (array, required) — 2-5 business UUIDs

### Catalog

#### browse_catalog
Browse a business's product/service catalog. Filter by category, sort by name or price.

**Parameters:**
- `business_id` (string, required) — business UUID
- `category` (string) — filter by category
- `sort_by` (string) — "name", "price_low", or "price_high"

#### get_product_details
Deep product view with all variant dimensions, combinations, prices, SKUs, and stock levels.

**Parameters:**
- `offering_id` (string, required) — product/offering UUID

#### check_availability
Real-time stock check for a product or specific variant combination.

**Parameters:**
- `offering_id` (string, required) — product/offering UUID
- `options` (object) — variant options, e.g. {"Color":"Black","Size":"Large"}

### Commerce

#### create_order
Create a draft order with atomic stock reservation. Items specified by offering + variant + quantity.

**Parameters:**
- `business_id` (string, required)
- `items` (array, required) — [{offering_id, variant_id?, quantity}]
- `customer_email` (string) — for notifications
- `customer_name` (string)
- `customer_notes` (string)

#### confirm_order
Confirm draft order and generate Stripe Checkout payment link (30-min expiry).

**Parameters:**
- `order_id` (string, required) — from create_order

#### get_order_status
Full status, payment state, fulfillment progress, and event timeline.

**Parameters:**
- `order_id` (string, required)

#### cancel_order
Cancel with automatic refund (if paid) and stock restoration.

**Parameters:**
- `order_id` (string, required)
- `reason` (string)

## Order Lifecycle

```
DRAFT → CONFIRMED → PAID → ACCEPTED → PREPARING → FULFILLED → COMPLETED
```

Cancellation with auto-refund available at any stage.

## Key Design Principles

- Every response includes `next_actions` — the agent always knows what to do next
- Error responses include `retry_guidance` for agent resilience
- Real-time stock with atomic reservation prevents overselling
- Stripe Connect direct charges for secure payment processing
- Businesses self-manage their data — catalog, pricing, and stock are always current

## Usage Tips

- Use `search` for most queries — it handles natural language and intent classification automatically
- Use `details` after search to get the full profile for a specific business
- Use `browse_catalog` → `get_product_details` → `check_availability` to explore what's available
- Use `create_order` → `confirm_order` for the purchase flow
- Use `compare` when the user wants to evaluate options side-by-side
- Always reference `next_actions` in responses to guide the conversation
