---
name: oo-xydc-mcp
description: "XYDC MCP (platform.xydc.com). Use this skill for ANY XYDC MCP request — reading, creating, and updating data. Whenever a task involves XYDC MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "XYDC MCP"
  author: "OOMOL"
  version: "1.0.3"
  services: ["xydc_mcp"]
  icon: "https://static.oomol.com/logo/third-party/xydc_mcp.svg"
---

# XYDC MCP

Operate **XYDC MCP** through your OOMOL-connected account. This skill calls the `xydc_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected XYDC MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "xydc_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "xydc_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call a current XYDC MCP tool with JSON arguments matching its live schema. Calls may consume Credits. Each successful generate_category_insight_resource call costs 500 Credits, including existing resources; reuse the returned resource and do not blindly retry generation. Connector waits at most 55 seconds for generation. A timeout does not confirm upstream cancellation or prevent charges; the result may be unknown. Do not automatically retry generation after a timeout. [write]
- `generate_category_insight_resource` — Generate a category insight resource for a user-confirmed marketplace and category. XYDC waits up to five minutes and rebuilds failed resources internally. Each independent successful call costs 500 Credits, including existing-resource hits. Reuse resourceId for subsequent queries; do not blindly retry. Connector waits at most 55 seconds for generation. A timeout does not confirm upstream cancellation or prevent charges; the result may be unknown. Do not automatically retry generation after a timeout. Read xydc_mcp.read_category_insight_guide before the first category insight task. [write]
- `get_asin_ad_change_trends` — Get daily newly observed advertising campaigns for one ASIN. This does not establish whether existing campaigns stopped, decreased, were deleted or remain active. Use traffic trends for traffic changes.
- `get_asin_bsr_trends` — Get daily BSR category-ranking trends for one ASIN. Supports US, CA, MX, BR, UK, DE, FR, ES, IT and JP; this is not keyword ranking.
- `get_asin_info` — Get product titles, prices, currencies, star ratings, rating counts, images and Amazon links for up to 100 ASINs sharing one marketplace.
- `get_asin_info_change_trends` — Get daily changes to one ASIN title and main image, including current and previous values. Use get_asin_info_trends for prices, ratings and promotions.
- `get_asin_info_trends` — Get daily rating counts, stars, displayed/list/deal/Prime prices, coupons, promotions and subscription offers for one ASIN. Longer date ranges cost more.
- `get_asin_keyword_count_trends` — Get daily keyword counts and distributions for ASINs sharing one marketplace. Covers organic/advertising, ranking bands, head/long-tail and acquisition-rate groups. Keyword-count growth does not prove traffic growth.
- `get_asin_keyword_rank_hourly` — Get hourly rankings of one ASIN for one keyword on one day. Supports US, UK and DE; use daily trends for multiple days.
- `get_asin_keyword_rank_trends` — Get daily rankings of one ASIN for one keyword over a date range.
- `get_asin_keyword_traffic_trends` — Get daily organic, advertising and placement-level traffic for one ASIN and keyword.
- `get_asin_keywords` — Reverse-search keywords bringing rankings and traffic to one ASIN in the latest seven-day snapshot. Use daily or monthly tools for historical dates.
- `get_asin_keywords_daily` — Get historical daily reverse-search keywords, rankings and traffic for one ASIN over a date range.
- `get_asin_keywords_monthly` — Get historical monthly reverse-search keywords, rankings and traffic for one ASIN over a month range.
- `get_asin_order_trends` — Get monthly order counts for one ASIN over an explicit month range. Use get_asin_orders_last_30_days for recent orders.
- `get_asin_orders_last_30_days` — Get recent order counts for one or more ASINs, measured over the last 30 days.
- `get_asin_traffic` — Get the latest seven-day organic, advertising and total traffic scores and period-over-period changes for one or more ASINs.
- `get_asin_traffic_trends` — Get daily organic, advertising and placement-level traffic-score trends for one ASIN.
- `get_asin_traffic_trends_monthly` — Get monthly organic, advertising and placement-level traffic-score trends for one ASIN.
- `get_asin_traffic_trends_weekly` — Get weekly organic, advertising and placement-level traffic-score trends for one ASIN. Weeks run Monday through Sunday.
- `get_asin_variations` — Get the parent ASIN, child ASINs and variation attributes for one ASIN.
- `get_category_brand_market_size` — Get category brand market-size lists and complete trends, with monthly or last-30-day periods, price bands, rankings, sorting and pagination. Costs 5 Credits per 5 returned brands. newRelease sorts by descending sales and does not filter new brands; rankingType overrides orders. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_brand_sales_trends` — Get complete historical monthly sales trends and existing last-30-day summaries for specified brands; month-range filtering is unsupported. Cost: ceil((maximum historical months + 1) / 6) times requested brand count times 2 Credits. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_keyword_analysis` — Get category keyword summary, distribution and complete trends for one calendar month and an explicit correlationType. Omit the month for the latest available keyword month. Costs 5 Credits including trends; yearly, daily and rolling periods are unsupported. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_keywords` — Get category keywords for one calendar month, with correlation, brand, range, text and pagination filters. Omit the month for the latest available keyword month. Includes full historical trends unless includeTrend=false. Costs 1 Credit per 20 keywords. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_market_size_trends` — Get complete historical monthly category sales trends across all price bands and existing last-30-day summaries. Month-range filtering is unsupported. Costs 5 Credits per 6 historical months; last-30-day summaries add no charge. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_new_release_opportunity_trends` — Get category new-release opportunity summary, list, full trends and periods. Costs 5 Credits per 6 trend months; lists and periods add no charge. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_new_release_ranking` — Get category new-release rankings for required reportPeriod: YYYY-MM, YYYY, last30days or last12months. Set rangeFilters.streetDays explicitly: there is no default listing-age limit, so unfiltered results are not necessarily new products. Costs 5 Credits per 5 representative ASINs. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_price_segment_trends` — Get low, middle and high price-band analysis and full trends, with period prices, brands, representative ASINs, ratings and subranges. Historical trends do not contain monthly price boundaries. Costs 5 Credits per 6 distinct months across all bands. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_primary_asins` — Get representative ASINs and complete trends for a category or price band, with rankings, sorting and pagination. last12months only supports all price bands. Costs 5 Credits per 5 representative ASINs; rankingType overrides orders. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_review_analysis` — Get combined category star-rating and rating-count distributions and complete trends for a calendar month or the last 30 days. Costs 5 Credits per successful call. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_sales_ranking` — Get category sales rankings aggregated by primaryAsin for required reportPeriod: YYYY-MM, YYYY, last30days or last12months, with brand/range filters, sorting and pagination. Costs 5 Credits per 5 returned representative ASINs, rounded up. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_seasonality` — Get category seasonality, peak/off seasons, sales comparisons and forecasts. Both nonseasonal and indeterminate results use isSeasonal=false with empty analysis; request failures are errors. Costs 5 Credits per successful call. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_category_surging_ranking` — Get category surging-product rankings for required reportPeriod: YYYY-MM, YYYY, last30days or last12months, with growth rules, filtering and sorting. Costs 5 Credits per 5 representative ASINs. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `get_keyword_aba_trends` — Get weekly ABA search-volume trends for up to 100 keywords and at most 52 calendar weeks. ABA weeks run Sunday through Saturday, unlike ASIN traffic weeks.
- `get_keyword_advertising_replay` — Replay hourly advertising placements for one keyword on one day in US, UK or DE, returning up to 24 hours of placement competition.
- `get_keyword_analysis_monthly` — Get monthly ASIN competition, rankings and traffic for one keyword over a month range.
- `get_keyword_asin_analysis` — Reverse-search competing ASINs and their rankings and traffic for one keyword in the latest seven-day snapshot.
- `get_keyword_info` — Get the latest weekly search volume, ABA ranking, competition difficulty and suggested bids for up to 100 keywords in one marketplace.
- `get_multi_asin_keyword_comparison` — Compare latest seven-day keyword coverage, rankings and traffic across up to 20 ASINs when the user requests comparison or keyword-library building. Do not silently combine independent ASIN queries.
- `get_multi_asin_keyword_comparison_monthly` — Compare historical monthly keyword coverage, rankings and traffic across up to 20 ASINs for comparison or keyword-library building.
- `get_parent_asin_keywords` — Get latest seven-day keywords across all children of one parent. Supply one child ASIN; XYDC resolves its parent. Use only for an explicitly requested parent-level analysis.
- `get_parent_asin_keywords_monthly` — Get historical monthly keywords across all children of one parent. Supply one child ASIN; XYDC resolves its parent. Use only for an explicitly requested parent-level analysis.
- `get_primary_asin_children` — Get children and complete trends for one representative primaryAsin string, with reporting periods, price bands and pagination. Costs 5 Credits per 20 child ASINs. Read xydc_mcp.read_category_insight_guide before the first category insight task.
- `list_tools` — Discover the current XYDC MCP tools, behavior annotations, and live input schemas before choosing a tool to call.
- `read_category_insight_guide` — Read the official XYDC category insight workflow before a category analysis: marketplace and category confirmation, resource generation, reuse, reporting periods, pagination and Credits.
- `report_missing_xiyou_capability` — Submit a missing-capability feedback event to XYDC when requested by the user. This records product feedback, not Amazon data, and should not be used for ordinary input errors. Redact sensitive information before submission. [write]
- `search_market_insight_categories` — Search Amazon categories by keyword or ASIN, returning paths, representative-ASIN counts, availability and existing translations. Free. Present candidates and obtain user confirmation before generating a category resource, even for one candidate. Read xydc_mcp.read_category_insight_guide before the first category insight task.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change XYDC MCP state — confirm the exact payload and effect with the user before running.**
- **Actions tagged `[destructive]` remove or overwrite data — always confirm the target and get explicit approval first.**

## First-time setup

These are **one-time** steps — do not repeat them on every call. Run a step only when a command fails for the matching reason.

- **`oo: command not found`** — install the oo CLI (other platforms: <https://cli.oomol.com/install-guide.md>):

  ```bash
  curl -fsSL https://cli.oomol.com/install.sh | bash    # macOS / Linux
  ```

  ```powershell
  irm https://cli.oomol.com/install.ps1 | iex           # Windows PowerShell
  ```

- **Not signed in / authentication error** — sign in to your OOMOL account once:

  ```bash
  oo auth login
  ```

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — XYDC MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/xydc_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- XYDC MCP homepage: https://platform.xydc.com/mcp
- API documentation: https://platform.xydc.com/docs/mcp-access
