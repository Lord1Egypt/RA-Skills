---
name: invisit-analytics
description: "Read and act on a site’s invisit analytics (visitors, sources, AI referrals, funnels, revenue, web vitals) through the invisit MCP server or REST API. Use when asked about traffic, conversions or revenue of a site measured with invisit."
---

# Read invisit analytics

## Over MCP (assistants)

Add `https://app.invisit.dev/mcp` as a remote MCP server (Streamable HTTP). There is no key to paste: the client opens invisit in the browser, the person signs in and approves read, write or manage access on a consent screen. Clients that can only send a fixed header use a personal token from **Account → Connected apps → Personal tokens** as `Authorization: Bearer invisit_mcp_…`.

Start with `list_sites`, then pass its `site_id` (or the site's domain) to the other tools. `get_site` shows a site's configuration and health, the first stop when data looks missing. The reports: `get_overview`, `get_timeseries`, `get_breakdown` (pages, sources, UTM, countries, devices, AI crawlers, short links, custom events), `run_funnel`, `get_search_queries`, `get_discover_pages`, `get_ai_assistants`, `get_web_vitals`, `get_heatmap`, `get_errors`, `get_link_clicks`, `get_realtime`, `list_visits`, `get_revenue`, `list_feedback`, `get_debug_events`. Those over a time window take a `period` such as `7d`, `30d` or `month`, or `from`/`to` dates. Every tool and its grant: https://invisit.dev/docs/api/mcp.md

## Over REST (code)

Create a site API key under **Settings → API keys** and send it as `Authorization: Bearer invisit_sk_…` to `https://api.invisit.dev/v1/…`. The OpenAPI document lists every operation: https://api.invisit.dev/openapi/json. Scopes, pagination and rate limits: https://invisit.dev/docs/api/rest.md
