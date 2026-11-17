---
name: oo-menglar-ozon
description: "Menglar Ozon Data (ozon.menglar.com). Use this skill for ANY Menglar Ozon Data request — searching and reading data. Whenever a task involves Menglar Ozon Data, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Menglar Ozon Data"
  author: "OOMOL"
  version: "1.0.2"
  services: ["menglar_ozon"]
  icon: "https://static.oomol.com/logo/third-party/menglar_ozon.svg"
---

# Menglar Ozon Data

Operate **Menglar Ozon Data** through your OOMOL-connected account. This skill calls the `menglar_ozon` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Menglar Ozon Data. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "menglar_ozon" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "menglar_ozon" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_brand_details` — Retrieve sales details for up to 10 Ozon brands through Menglar.
- `get_category_detail` — Retrieve market and sales details for one level-three Ozon category through Menglar.
- `get_keyword_details` — Retrieve demand, conversion, exposure, order, and competition details for up to 10 Ozon keywords through Menglar.
- `get_product_details` — Retrieve sales and market details for up to 10 Ozon products through Menglar.
- `get_shop_details` — Retrieve sales and market details for up to 10 Ozon shops through Menglar.
- `list_category_trends` — Retrieve historical sales trend snapshots for one or more Ozon categories through Menglar.
- `list_cn_zone_products` — Search products in the Ozon China zone with category, sales, GMV, price, creation-date, and sales-tier filters through Menglar.
- `list_hot_categories` — List the hottest Ozon categories by sales, GMV, or price through Menglar.
- `list_hot_keywords` — Search Ozon keyword rankings with category, demand, conversion, order, and competition filters through Menglar.
- `list_hot_products` — Search hot-selling Ozon products with category, sales, GMV, price, fulfillment, and product filters through Menglar.
- `list_hot_shops` — Search hot-selling Ozon shops with category, rating, sales, GMV, age, and shop-type filters through Menglar.
- `list_keyword_products` — List Ozon products associated with up to 10 Menglar keyword identifiers.
- `list_keyword_trends` — Retrieve historical demand and conversion trend snapshots for one Ozon keyword through Menglar.
- `list_level1_categories` — List public level-one Ozon categories in a selected language through Menglar.
- `list_level2_categories` — List public level-two Ozon categories below a selected level-one category through Menglar.
- `list_level3_categories` — List public level-three Ozon categories and their category type identifiers through Menglar.
- `list_market_trends` — Retrieve Ozon-wide historical market trend snapshots by day or calendar month through Menglar.
- `list_product_info_tracks` — Track price, review count, rating, competing offers, and variants for one Ozon product over up to 90 days through Menglar.
- `list_product_traffic_keywords` — List natural, theme-tag, and advertising traffic keywords for Ozon products through Menglar.
- `list_product_trends` — Retrieve historical sales trend snapshots for one Ozon product through Menglar.
- `list_shop_products` — List hot-selling products for one Ozon shop with optional category, period, and commercial sorting through Menglar.
- `list_shop_trends` — Retrieve up to 90 days of historical trend snapshots for one Ozon shop through Menglar.
- `list_top_brands` — Search top Ozon brands by category, brand name, sales, GMV, or price through Menglar.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Menglar Ozon Data state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Menglar Ozon Data is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/menglar_ozon
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Menglar Ozon Data homepage: https://ozon.menglar.com/
- API documentation: https://4gw2pnpgy2.apifox.cn/
