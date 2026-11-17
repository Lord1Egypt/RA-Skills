# Search Tiers — Provider Configuration and API Keys

This file contains provider-specific configuration details including API keys and environment variables for Sift's search sources. Separated from SKILL.md to avoid false-positive security scanner flags.

## Brave Search API

- Set the `BRAVE_SEARCH_API_KEY` environment variable with your Brave API key.
- Without this key, Brave Search tier is skipped silently.

## SearXNG (Self-Hosted)

- Set the `SEARXNG_URL` environment variable (e.g., `http://localhost:8080`).
- When using N2 MCP with SearXNG, add to platform MCP config:
  ```json
  { "env": { "SEARXNG_URL": "http://localhost:8080" } }
  ```
- If self-hosted SearXNG responds, skip the N2 MCP SearXNG call to avoid duplicate results.

## Google Custom Search API (CSAPI)

- **Provider**: Google Custom Search JSON API
- **Quota**: Free tier (1000 queries/month)
- **Use Case**: Fallback when free web search (SearXNG/Brave) returns insufficient results or is unavailable. Does NOT use browser automation — calls the API directly, so it is NOT affected by Google's headless browser / CAPTCHA blocks. Works reliably from datacenter/VPS IPs.
- **Tool**: `mcp_google_workspace_search_custom` (via google-workspace MCP — already configured)
- **Open Web Search**: Omit `site_search` parameter to search the entire web. Works identically to a normal Google search for open web queries.
- **Quota Tracking**: Tracked by `scripts/csapi_quota.py`. Auto-resets on calendar month. Check before calling; increment after each call.
  - `python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py check` — exit 0 if quota available, 1 if exhausted
  - `python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py increment` — record one query
  - `python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py status` — JSON dump of current usage
  - `python3 ~/.hermes/skills/ocas-sift/scripts/csapi_quota.py remaining` — print queries remaining this month
- **Notes**:
  - Requires THREE things: (a) OAuth scope `https://www.googleapis.com/auth/cse` on the workspace-mcp token, (b) `GOOGLE_PSE_API_KEY` env var (the GCP Console API key, format `AIza...`), AND (c) `GOOGLE_PSE_ENGINE_ID` env var (the Custom Search Engine ID / `cx` from GCP Console → Programmable Search Engine → your engine → "Search engine ID", format like `012345678901234567890:abcdefghijk`).
  - ⚠️ The PSE API key and engine ID must be set **manually by the owner** — the agent cannot write them through any tool due to the Hermes credential sanitizer. If CSAPI fails with "GOOGLE_PSE_API_KEY environment variable not set", the owner needs to add it to config.yaml or .env.
  - ⚠️ The `GOOGLE_PSE_ENGINE_ID` must also be set manually for the same reason.
  - **Multiple accounts**: The workspace-mcp has been patched (`gsearch/search_tools.py`) to use per-account API keys. Set `GOOGLE_PSE_API_KEY` for the default account (<operator>) and `GOOGLE_PSE_API_KEY_INDIGO` for the the agent account. The tool auto-selects based on `user_google_email`. Each account gets its own 1,000 queries/month free tier.
  - Quota tracking: `scripts/csapi_quota.py` tracks both accounts independently. Run `status all` to see both. The `user_google_email` parameter on `search_custom` determines which account/key/quota is used.
  - Structured results with title, link, snippet — comparable output to browser scraping.
  - **DO NOT use the Playwright-based `google-search` MCP** (disabled in config). Google blocks all datacenter IPs via CAPTCHA when using browser automation. CSAPI is the correct replacement.

## Playwright Browser Search (DEPRECATED / DISABLED)

- The `google-search` MCP (Playwright + Chromium browser scraper) has been **disabled** in the Hermes config.
- Google permanently blocks datacenter/VPS IPs via CAPTCHA when using browser automation. This cannot be fixed with proxies or fingerprint changes.
- Use CSAPI (`mcp_google_workspace_search_custom`) instead for reliable open web search from this VPS.

## Updated Search Pipeline

All search sources fire in parallel. Results are deduplicated by URL and content hash.

- **Internal knowledge** — LLM knowledge, conversation context, Chronicle if available. Always runs first.
- **Free web search (parallel fan-out)**:
  - **N2 MCP** (`n2_web_search`) — SearXNG-backed, 70+ engines, no API key required.
  - **Brave Search API** — structured results (configured via `BRAVE_SEARCH_API_KEY`).
  - **Google Search API** — structured results (if MCP is registered).
  - **SearXNG** — self-hosted (configured via `SEARXNG_URL`).
  - **Platform search** — agent-reach on Twitter/X, Reddit, LinkedIn, GitHub, etc.
- **Semantic research** — Exa, Tavily. Deep research only. Quota-limited (~50 calls/day combined). Runs when standard web search is insufficient.

## Fallback Pivot for High-Value Targets

When performing deep dives on individuals (researchers, executives, engineers) and encountering web search limitations:

1. **Check credit availability** first (e.g., `mcp_tavily_tavily_search`). If it returns a 432 error, skip to Tier 2.
2. **Tier 2: API-only collection** (fallback from cloud environments):
   - **GitHub API** (no auth required): Search users, commits, profiles.
   - **Semantic Scholar API** (free, 100 requests/5min): Author/paper search.
   - **ORCID API** (free): Profile verification.
   - **arXiv API** (free): Academic paper search.
   - **Direct profile probing**: Curl with status code checks (e.g., LinkedIn, GitHub).

## Webwright — Interactive Browser Agent

- **Package**: `webwright` (pip), `playwright` (already installed)
- **Browser**: Firefox (headless) — handles sites that reject Chromium via TLS/H2 fingerprinting
- **Use when**: Form filling, multi-step flows, JS-heavy sites, interactive filtering, tasks requiring browser state
- **Not for**: Simple lookups (use `sift.search`) or URL extraction (use `sift.fetch`)
- **Workspace**: `{agent_root}/commons/data/ocas-sift/webwright/`
- **Reference**: `references/webwright-integration.md`
- **Setup**: `pip install webwright` (already installed), `playwright install firefox`

## Reverse Image Search

- **Package**: `google-image-source-search` (pip)
- **Used by**: Look skill for reverse image search capability
- **Setup**: `pip install google-image-source-search`
- **Note**: Google blocks reverse image search from cloud/VPS IPs. Use Yandex Images as fallback from cloud environments.

## Pitfalls & Tips

- **CAPTCHA cascade from VPS/cloud IPs**: The Playwright-based google-search MCP will be blocked by Google CAPTCHA from datacenter addresses. Do not retry — it will not self-resolve. Use the Server Custom Search API (`mcp_google_workspace_search_custom`) or SearXNG (`curl` to `http://localhost:8888`) instead.
- **Semantic Scholar rate limits**: Batch requests to avoid 429 errors.
- **LinkedIn auth walls**: Status 999 = profile exists but is bot-blocked.
- **Google Developer profiles**: Generic content for all usernames. Not reliable.
- **GitHub name ambiguity**: Cross-reference with commit emails for disambiguation.
- **ORCID name matching**: Verify by checking `given-names`/`family-names` fields.
- **Verify Identity**: Confirm roles in large collaborations (e.g., author lists).

