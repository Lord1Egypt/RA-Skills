---
name: oo-sorftime
description: "Sorftime (sorftime.com). Use this skill for ANY Sorftime request — searching and reading data. Whenever a task involves Sorftime, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sorftime"
  author: "OOMOL"
  version: "1.0.5"
  services: ["sorftime"]
  icon: "https://static.oomol.com/logo/third-party/sorftime.png"
---

# Sorftime

Operate **Sorftime** through your OOMOL-connected account. This skill calls the `sorftime` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sorftime. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sorftime" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sorftime" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `extend_keywords` — Find related Amazon keywords from a seed keyword through Sorftime. Consumes five Sorftime requests.
- `extend_walmart_keywords` — Find related Sorftime Walmart US keywords from a seed keyword. Consumes five Sorftime requests.
- `get_asin_keyword_rankings` — Get up to two years of US Amazon rankings for an ASIN and keyword through Sorftime. Returns 200 records per page and consumes two Sorftime requests.
- `get_asin_sales_history` — Get current or historical Sorftime estimated sales for one Amazon ASIN. Consumes one Sorftime request.
- `get_category_best_sellers` — Get the current or historical Amazon Best Seller Top 100 products for a category through Sorftime. Consumes five requests; historical lookup costs ten requests per three-day block.
- `get_category_trend` — Get up to two years of a selected Sorftime Amazon category market trend. Consumes five Sorftime requests.
- `get_credit_balance` — Get the current Sorftime credit balance. Consumes one Sorftime request.
- `get_keyword_details` — Get Sorftime Amazon keyword details including search volume, conversion, competition, and CPC trends. Consumes one Sorftime request.
- `get_keyword_product_rankings` — List products ranked for an Amazon keyword through Sorftime. Returns 200 products per page and consumes five Sorftime requests.
- `get_keyword_search_result_trend` — Get monthly Amazon search-result trends for a keyword through Sorftime. Consumes ten Sorftime requests.
- `get_keyword_search_results` — Get Amazon products appearing in organic or advertising search results for a keyword through Sorftime. Consumes five Sorftime requests.
- `get_product_details` — Get Sorftime Amazon product details for one ASIN, optionally including price, rank, sales, and other historical trends. Consumes one request, or two for trend ranges longer than 15 days.
- `get_product_review_summary` — Get Sorftime's Amazon customer review summary for one ASIN. Consumes one Sorftime request.
- `get_product_variations` — List Amazon product variations through Sorftime, optionally including variation sales. Consumes one request, or two when sales are included.
- `get_request_usage` — Get Sorftime monthly request purchases and consumption history without consuming a request.
- `get_walmart_category_report` — Get Sorftime's Walmart US category report and Best Seller Top 80 products for a known node path. Consumes five Sorftime requests.
- `get_walmart_keyword_details` — Get Sorftime Walmart US keyword details such as search volume, competition, and first-page averages. Consumes one Sorftime request.
- `get_walmart_keyword_search_results` — Get products appearing in the last 15 days of Walmart US results for a current Sorftime hot keyword. Consumes five Sorftime requests.
- `get_walmart_product_details` — Get current Sorftime Walmart US details for one product ID. Consumes one Sorftime request.
- `get_walmart_product_sales_history` — Get Sorftime Walmart US published variant sales history for one product ID. Defaults to the latest 30 days, returns up to 100 rows per page, and consumes one Sorftime request.
- `get_walmart_product_trend` — Get Sorftime Walmart US sales, price, review, rating, and category-rank trends for one product ID. Consumes two Sorftime requests.
- `list_category_products` — List Sorftime Amazon products in a category ordered by monthly sales. Returns 100 products per page and consumes five Sorftime requests.
- `list_credit_usage` — List paginated Sorftime credit usage records for Amazon, Shopee, or Walmart. Consumes one Sorftime request.
- `list_product_reviews` — List Sorftime Amazon product review records with rating and verified-purchase filters. Returns 100 records per page and consumes five Sorftime requests.
- `reverse_lookup_asin_keywords` — Find Amazon keywords that exposed an ASIN in the first three search-result pages during the last 30 days through Sorftime. Consumes one Sorftime request.
- `reverse_lookup_category_keywords` — Find Amazon keywords associated with a leaf category through Sorftime. Consumes one Sorftime request.
- `reverse_lookup_walmart_product_keywords` — Find keywords that exposed a Walmart US product in the first three search-result pages during the last 30 days. Consumes one Sorftime request.
- `search_categories_by_name` — Search Amazon category markets by natural-language name through Sorftime and return matching NodeIds. Consumes one Sorftime request.
- `search_keywords` — Search and filter the Sorftime Amazon keyword database. Consumes five Sorftime requests.
- `search_products` — Search and filter the Sorftime Amazon product database. Returns up to 100 products per page and consumes five Sorftime requests.
- `search_products_by_name` — Search Amazon products by name through Sorftime and return product research results. Consumes two Sorftime requests.
- `search_walmart_keywords` — Search and filter Sorftime's current Walmart US hot-keyword database. Consumes five Sorftime requests.
- `search_walmart_keywords_by_name` — Search Sorftime Walmart US hot keywords from a natural-language name. Consumes one Sorftime request.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sorftime state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sorftime is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sorftime
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sorftime homepage: https://www.sorftime.com/
- API documentation: https://github.com/sorftime/sorftime-cli/blob/master/README.md
