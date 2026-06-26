# Changelog

All notable changes to the LobsterSearch MCP server will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [2.0.0] - 2026-03-18

### Complete Rebuild — Agentic Commerce

LobsterSearch v2 is a ground-up rebuild from directory to agentic commerce platform.

#### Added
- **Commerce tools:** `create_order`, `confirm_order`, `get_order_status`, `cancel_order` — full order lifecycle with Stripe Connect payments
- **Catalog tools:** `browse_catalog`, `get_product_details`, `check_availability` — real product catalogs with 5-level variant support
- **Hybrid search intelligence** — pre-computed search tags + 4-step fallback chain (structured → tags → LLM interpret → LLM catalog scan)
- **`next_actions` in every response** — agents always know what to do next
- **Atomic stock reservation** — stock reserved on draft creation, restored on cancellation
- **Order state machine** — DRAFT → CONFIRMED → PAID → ACCEPTED → PREPARING → FULFILLED → COMPLETED
- **Protection layer** — rate limiting (Upstash Redis), behavioral analysis, resource limits
- **Business notifications** — email notifications for order events via Resend
- **Config-driven behavior** — 39 platform config keys across 11 namespaces

#### Changed
- `search_businesses` → `search` (simplified name, 4-step fallback chain)
- `get_business_details` → `details` (includes catalog and variants)
- `compare_businesses` → `compare` (supports 2-5 businesses)

#### Removed
- `list_nearby_businesses` — GPS-based search (will return when businesses self-report coordinates)
- `get_promotions` — replaced by catalog browsing with real pricing
- `get_trending` — replaced by search intelligence
- `report_data_mismatch` — v2 uses self-service business data, not crawled data
- All v1 crawled data concepts: GEO scores, confidence scores, 46 categories, 800+ seeded businesses

### Architecture
- Hexagonal architecture: domain services → thin MCP adapters
- Self-service businesses (not scraped/crawled)
- Stripe Connect for payments (platform is facilitator)
- StreamableHTTP transport (unchanged)

---

## [1.0.0] - 2026-03-13

### Added
- 7 MCP tools: `search_businesses`, `get_business_details`, `list_nearby_businesses`, `get_promotions`, `compare_businesses`, `get_trending`, `report_data_mismatch`
- StreamableHTTP transport (MCP SDK 1.27.1)
- Hybrid search: full-text search + semantic vector matching
- Confidence-scored results with quality annotations
- Answer quality scoring for AI agent decision-making
- 100+ verified Singapore businesses across 46 categories
