---
name: novada-mcp
description: Web scraping, SERP and search API for OpenClaw through Novada MCP. Search Google, Bing, DuckDuckGo and Yandex, scrape Amazon, YouTube and LinkedIn data, extract and crawl pages, and use proxies. Use when the user needs live web data, SERP results or a search API, or asks to set up or troubleshoot the Novada connection.
version: 1.0.2
metadata:
  openclaw:
    homepage: https://novada.com/products/novada-mcp/
---

# Novada MCP: Web Scraping, SERP and Search API

Novada MCP is a remote MCP server operated by Novada at `https://mcp.novada.com/mcp`.
It gives the agent web scraping, SERP and search API access, plus live web data, through one connection. It runs no local code, so there is
nothing to install with npm and no key to put in a config file. Sign-in uses MCP OAuth with the
user's own Novada account.

## Set up the connection

Run these steps once. They change OpenClaw's saved MCP server list, so tell the user before you run them.

1. Save the server definition:

   ```bash
   openclaw mcp set novada '{"url":"https://mcp.novada.com/mcp","transport":"streamable-http","auth":"oauth"}'
   ```

2. Sign in. OpenClaw prints an authorization URL; the user opens it in a browser and approves:

   ```bash
   openclaw mcp login novada
   ```

   During the consent step Novada asks for the user's Novada API key. A key is created in the
   Novada dashboard (https://dashboard.novada.com). The key is entered in the browser only.

3. Check the connection and list the tools:

   ```bash
   openclaw mcp probe novada
   ```

If `openclaw mcp status` reports `authorization-required`, run step 2 again.
To disconnect: `openclaw mcp logout novada`, then `openclaw mcp unset novada`.

## Tools

OpenClaw exposes each tool as `novada__<tool_name>`.

| Group | Tools |
| --- | --- |
| Search and read | `novada_search`, `novada_extract`, `novada_crawl`, `novada_map`, `novada_research` |
| Structured data | `novada_scrape` (generic), plus per-platform tools: `novada_scrape_google`, `novada_scrape_bing`, `novada_scrape_duckduckgo`, `novada_scrape_yandex`, `novada_scrape_amazon`, `novada_scrape_walmart`, `novada_scrape_youtube`, `novada_scrape_instagram`, `novada_scrape_facebook`, `novada_scrape_tiktok`, `novada_scrape_x`, `novada_scrape_linkedin`, `novada_scrape_github`, `novada_scrape_perplexity` |
| Monitoring | `novada_monitor` (page change tracking), `novada_ai_monitor` (brand mentions on AI-company public pages) |
| Proxy | `novada_proxy`, `novada_proxy_account_create`, `novada_proxy_account_list` |
| Account | `novada_account` (balance and plans), `novada_setup`, `novada_discover` (lists every tool) |

## How to use it well

- Start with `novada_search` to find URLs, then `novada_extract` to read a page. Use `novada_research` when the question needs passages from several sources.
- For a known platform (Amazon, Google, YouTube, LinkedIn and so on) prefer the matching `novada_scrape_<platform>` tool over extracting raw HTML. It returns structured records.
- Scraping calls are billed to the user's Novada account. Before a call that can return many records, set a small `limit` and tell the user what it will cost to scale up.
- `novada_proxy_account_create` writes data. Never call it unless the user asked for a new sub-account.
- Only fetch pages the user is entitled to access, and respect the target site's terms.

## Data handling

Every call goes over HTTPS to `mcp.novada.com`. The server keeps the user's API key encrypted and records
operational metadata per call (tool name, argument key names, target hostname, outcome, latency),
not argument values or full URLs. Privacy policy: https://novada.com/privacy. Support: support@novada.com.
