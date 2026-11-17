---
name: oo-sorftime-mcp
description: "Sorftime MCP (sorftime.com). Use this skill for ANY Sorftime MCP request — reading, creating, updating, and deleting data. Whenever a task involves Sorftime MCP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sorftime MCP"
  author: "OOMOL"
  version: "1.0.6"
  services: ["sorftime_mcp"]
  icon: "https://static.oomol.com/logo/third-party/sorftime_mcp.png"
---

# Sorftime MCP

Operate **Sorftime MCP** through your OOMOL-connected account. This skill calls the `sorftime_mcp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sorftime MCP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sorftime_mcp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sorftime_mcp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ali1688_get_product` — Inspect one 1688 product using its ID from ali1688_search_products through Sorftime.
- `ali1688_list_categories` — Browse 1688 categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `ali1688_search_products` — Search 1688 products by name to find sourcing suppliers and procurement prices through Sorftime.
- `amazon_find_related_keywords` — Expand an Amazon keyword into related and long-tail search terms through Sorftime.
- `amazon_get_category_report` — Research an Amazon category market using a category ID from amazon_list_categories through Sorftime.
- `amazon_get_keyword` — Inspect demand for a specific Amazon keyword through Sorftime.
- `amazon_get_product` — Inspect one Amazon product using its ID from amazon_search_products through Sorftime.
- `amazon_get_product_trend` — Inspect historical Amazon product performance through Sorftime. Select one metric.
- `amazon_list_categories` — Browse Amazon categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `amazon_list_keywords` — Discover Amazon keywords ranked by weekly search volume through Sorftime. Supports optional rank and search-volume bounds.
- `amazon_search_products` — Find Amazon products by name through Sorftime.
- `call_tool` — Run a tool from list_tools with its required arguments. Supports research queries and changes to favorites, including deletion. Credit cost depends on the tool. [destructive]
- `list_tools` — List all tools available to your Sorftime MCP account with their descriptions and argument schemas.
- `shopee_get_product` — Inspect one Shopee product using its ID from shopee_search_products through Sorftime.
- `shopee_get_product_trend` — Inspect historical Shopee product performance through Sorftime. Returns available dimensions together. Ranges beyond one year cost 10 credits.
- `shopee_list_categories` — Browse Shopee categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `shopee_list_category_products` — Find best-selling products in a Shopee category through Sorftime. Optionally query historical natural-week snapshots for leaf categories.
- `shopee_list_keywords` — Discover Shopee keywords ranked by monthly search volume through Sorftime. Supports optional rank and search-volume bounds.
- `shopee_search_products` — Find Shopee products by name through Sorftime.
- `temu_get_product` — Inspect one Temu product using its ID from temu_search_products through Sorftime.
- `temu_get_product_trend` — Inspect historical Temu product performance through Sorftime. Returns available dimensions together. Ranges beyond one year cost 10 credits.
- `temu_list_categories` — Browse Temu categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `temu_list_category_products` — Find best-selling products in a Temu category through Sorftime.
- `temu_search_products` — Find Temu products by name through Sorftime.
- `tiktok_get_category_report` — Research a TikTok category market using a category ID from tiktok_list_categories through Sorftime.
- `tiktok_get_product` — Inspect one TikTok product using its ID from tiktok_search_products through Sorftime.
- `tiktok_get_product_trend` — Inspect historical TikTok product performance through Sorftime. Returns available dimensions together.
- `tiktok_list_categories` — Browse TikTok categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `tiktok_search_products` — Find TikTok products by name through Sorftime.
- `walmart_find_related_keywords` — Expand a Walmart US keyword into related and long-tail search terms through Sorftime.
- `walmart_get_category_report` — Research a Walmart US category market using a category ID from walmart_list_categories through Sorftime.
- `walmart_get_keyword` — Inspect demand for a specific Walmart US keyword through Sorftime.
- `walmart_get_product` — Inspect one Walmart US product using its ID from walmart_search_products through Sorftime.
- `walmart_get_product_trend` — Inspect historical Walmart US product performance through Sorftime. Select one metric.
- `walmart_list_categories` — Browse Walmart US categories through Sorftime. Omit parentId for the top levels, then pass a returned category ID to explore its children.
- `walmart_list_keywords` — Discover Walmart US keywords ranked by monthly search volume through Sorftime. Requires minRank and maxRank.
- `walmart_search_products` — Find Walmart US products by name through Sorftime.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sorftime MCP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sorftime MCP is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sorftime_mcp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sorftime MCP homepage: https://www.sorftime.com/
- API documentation: https://www.sorftime.com/en-US/mcp
