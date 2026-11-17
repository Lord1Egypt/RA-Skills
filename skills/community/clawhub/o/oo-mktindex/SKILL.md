---
name: oo-mktindex
description: "Moojing Market Intelligence (mktindex.com). Use this skill for ANY Moojing Market Intelligence request — reading, creating, updating, and deleting data. Whenever a task involves Moojing Market Intelligence, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Moojing Market Intelligence"
  author: "OOMOL"
  version: "1.0.2"
  services: ["mktindex"]
  icon: "https://static.oomol.com/logo/third-party/mktindex.png"
---

# Moojing Market Intelligence

Operate **Moojing Market Intelligence** through your OOMOL-connected account. This skill calls the `mktindex` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Moojing Market Intelligence. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mktindex" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mktindex" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_monitored_item` — Add one provider item URL to Moojing price monitoring. [write]
- `add_monitored_items` — Add multiple provider item URLs to Moojing price monitoring asynchronously. [destructive]
- `add_monitored_shops` — Add provider shops to Moojing monitoring asynchronously. [write]
- `assign_monitored_items_to_group` — Assign selected monitored SKUs to a Moojing monitoring group. [destructive]
- `compare_market_periods` — Compare sales and volume for two date ranges in a Moojing market.
- `compare_region_market_periods` — Compare sales and volume for two date ranges in a regional Moojing market.
- `create_monitor_group` — Create a Moojing price-monitoring group. [write]
- `delete_monitor_group` — Delete a Moojing price-monitoring group. [destructive]
- `get_attribute_summary` — Get sales metrics and top items for one or two selected Moojing attributes.
- `get_comment_trend` — Get review-count and sentiment-rate trends for a Moojing market.
- `get_data_range` — Get the earliest and latest available Moojing data months for a market.
- `get_item_monitor_task` — Get the status and row results for one monitored-item batch task.
- `get_item_sales_trend` — Get price, sales, volume, and comment trends for one Moojing item.
- `get_jd_data_versions` — List data-model versions available for a JD-related Moojing platform.
- `get_market_summary` — Get monthly sales, volume, price, shop, item, and market-share metrics for a Moojing market.
- `get_market_trend` — Get sales, volume, price, item, shop, and market-share trends for a Moojing market.
- `get_monitor_task_trend` — Get success and failure count trends for Moojing price-monitoring tasks.
- `get_monitored_item_price_trend` — Get list-price, page-price, and discounted-price trends for one monitored SKU.
- `get_platform_sales_trends` — Get total sales trend series for each Moojing e-commerce platform.
- `get_price_distribution` — Get item share, volume, and sales across price ranges in a Moojing market.
- `get_region_market_summary` — Get monthly summary metrics for a province or city within a Moojing market.
- `get_region_market_trend` — Get trend series for a province or city within a Moojing market.
- `get_shop_details` — Get category, brand, location, and service details for one or more Moojing shops.
- `get_shop_monitor_task` — Get the status and results for a shop inspection or monitoring task.
- `get_shop_sales_trend` — Get sales trends for one Moojing shop within a category and brand.
- `get_spu` — Get one Tmall product model or SPU with its items and shops.
- `inspect_shops` — Start an asynchronous Moojing lookup for provider shops without adding monitoring. [write]
- `list_attribute_performance` — List sales performance for attribute values or combinations in a Moojing category.
- `list_brand_categories` — List categories and sales associated with a Moojing brand on a platform.
- `list_categories` — List Moojing categories for an e-commerce platform.
- `list_category_attributes` — List attribute groups and values available for a Moojing category in one month.
- `list_hot_items` — List top-selling items within a Moojing market for one month.
- `list_hot_shops` — List top-selling shops within a Moojing market for one month.
- `list_item_monitor_tasks` — List asynchronous batch tasks that added monitored items.
- `list_market_breakdown` — List category, brand, or province rows within a Moojing market for one month.
- `list_monitor_groups` — List monitoring groups in the connected Moojing account.
- `list_monitor_task_logs` — List execution logs for Moojing price-monitoring tasks.
- `list_monitored_items` — List items and SKUs configured in Moojing price monitoring.
- `list_region_hot_items` — List top-selling items within a regional Moojing market.
- `list_region_hot_shops` — List top-selling shops within a regional Moojing market.
- `list_region_market_breakdown` — List category, brand, or city rows within a regional Moojing market.
- `list_spus` — List product models or SPUs for a Tmall category and brand in one month.
- `list_subscriptions` — List markets subscribed to or followed by the connected Moojing account.
- `remove_monitored_items` — Remove items or selected SKUs from Moojing price monitoring. [destructive]
- `search_brands` — Search Moojing brands by keyword or stock code.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Moojing Market Intelligence state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Moojing Market Intelligence is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mktindex
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Moojing Market Intelligence homepage: https://www.mktindex.com/
- API documentation: https://doc.mktindex.com/
