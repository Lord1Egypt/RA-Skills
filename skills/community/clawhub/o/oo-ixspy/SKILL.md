---
name: oo-ixspy
description: "IXSPY (ixspy.com). Use this skill for ANY IXSPY request — searching and reading data. Whenever a task involves IXSPY, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "IXSPY"
  author: "OOMOL"
  version: "1.0.2"
  services: ["ixspy"]
  icon: "https://static.oomol.com/logo/third-party/ixspy.png"
---

# IXSPY

Operate **IXSPY** through your OOMOL-connected account. This skill calls the `ixspy` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected IXSPY. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ixspy" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ixspy" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_category_resource` — Get the current IXSPY CDN URL for the complete AliExpress category tree resource.
- `get_keyword_rank` — Get an IXSPY AliExpress keyword ranking with search popularity, click, conversion, competition, supply, and growth metrics.
- `get_market_insights` — Compare immediate child categories in IXSPY using product, sales, revenue, review, market-share, and Choice-product metrics.
- `get_product_details` — Get IXSPY details for up to 10 AliExpress product IDs.
- `get_product_rank` — Get an IXSPY AliExpress total, hot, growth, new-product, or holiday product ranking.
- `get_product_region_sales` — Get estimated AliExpress product order counts grouped by buyer country or region.
- `get_product_shipping_stats` — Get estimated AliExpress order counts grouped by shipping method for a product.
- `get_product_sku_sales` — Get the estimated order distribution across SKU variants for an AliExpress product.
- `get_product_trends` — Get up to 90 days of IXSPY price, sales, and review trend data for a product.
- `get_region_product_rank` — Get an IXSPY weekly or monthly AliExpress product ranking for one buyer region.
- `get_store_category_distribution` — Get IXSPY product and sales distribution by category for an AliExpress store.
- `get_store_details` — Get IXSPY details for up to 10 AliExpress stores by merchant IDs or link IDs.
- `get_store_rank` — Get an IXSPY AliExpress total, hot, growth, new-store, or rising-store ranking.
- `get_store_region_sales` — Get estimated AliExpress store order counts grouped by buyer country or region.
- `get_store_trends` — Get up to 90 days of IXSPY follower, sales, and review trend data for a store.
- `list_category_children` — List the immediate AliExpress child categories under an IXSPY category, including root categories.
- `list_rank_dates` — List the IXSPY dates currently available for normal, holiday, or keyword AliExpress rankings.
- `research_categories` — Compare immediate child categories in IXSPY using products, stores, sales, reviews, supply-demand, regional, and top-100 opportunity metrics.
- `search_categories` — Search AliExpress categories in IXSPY by Chinese or English name, path, or fuzzy keyword.
- `search_products` — Search IXSPY AliExpress products with keyword, category, price, sales, review, rating, fulfillment, discovery, and update filters.
- `search_stores` — Search IXSPY AliExpress stores with name, category, sales, followers, reviews, rating, price, product count, origin, age, tags, and fulfillment filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change IXSPY state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — IXSPY is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/ixspy
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- IXSPY homepage: https://ixspy.com/
