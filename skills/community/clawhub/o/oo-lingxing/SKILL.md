---
name: oo-lingxing
description: "Lingxing (lingxing.com). Use this skill for ANY Lingxing request — searching and reading data. Whenever a task involves Lingxing, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Lingxing"
  author: "OOMOL"
  version: "1.0.6"
  services: ["lingxing"]
  icon: "https://static.oomol.com/logo/third-party/lingxing.png"
---

# Lingxing

Operate **Lingxing** through your OOMOL-connected account. This skill calls the `lingxing` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Lingxing. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "lingxing" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "lingxing" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `analyze_ad_keywords` — Analyze aggregated Sponsored Products and Sponsored Brands keyword metrics.
- `analyze_ad_search_terms` — Analyze aggregated Sponsored Products and Sponsored Brands search-term metrics.
- `batch_get_fba_shipments` — Get details for up to 50 Lingxing FBA shipment orders in one request.
- `batch_get_products` — Get details for up to 100 Lingxing local products by IDs, SKUs, or SKU identifiers.
- `get_fba_shipment` — Get one Lingxing FBA shipment order by shipment order number.
- `get_fba_shipment_creation_result` — Get the processing result for an asynchronous FBA shipment creation request.
- `get_product` — Get one local product from Lingxing by product ID, SKU, or SKU identifier.
- `list_accounts` — List all ERP user accounts enabled for the Lingxing enterprise.
- `list_ad_accounts` — List DSP, seller, or vendor advertising accounts authorized in Lingxing.
- `list_competitor_monitors` — List Amazon competitor products monitored in Lingxing.
- `list_concept_sellers` — List all Amazon concept stores configured in the Lingxing ERP account.
- `list_currencies` — List the Lingxing ERP exchange rates for a calendar month.
- `list_fba_inventory` — List current Lingxing FBA inventory with product, store, stock-state, and advanced search filters.
- `list_fba_shipment_carriers` — List first-mile carriers available for Lingxing FBA shipment logistics.
- `list_fba_shipment_fee_types` — List additional first-mile logistics fee types for Lingxing FBA shipments.
- `list_fba_shipments` — List Lingxing FBA shipment orders with pagination and operational filters.
- `list_keyword_rankings` — List monitored Amazon keyword rankings in Lingxing.
- `list_listings` — List Amazon Listings in Lingxing with store, pairing, update-time, and product filters.
- `list_marketplaces` — List all Amazon marketplaces configured in the Lingxing ERP account.
- `list_msku_profit` — List Lingxing profit-report rows aggregated by merchant SKU.
- `list_order_profit` — List Lingxing order-profit rows aggregated by merchant SKU.
- `list_product_performance` — List Amazon product performance aggregated by ASIN, parent ASIN, MSKU, or local SKU.
- `list_products` — List local products in Lingxing with pagination, timestamp ranges, and SKU filters.
- `list_sb_ad_group_reports` — List Sponsored Brands ad group performance for one report date.
- `list_sb_campaign_reports` — List Sponsored Brands campaign performance for one report date.
- `list_sb_product_ad_reports` — List Sponsored Brands advertising creative performance for one report date.
- `list_sb_target_reports` — List Sponsored Brands targeting performance for one report date.
- `list_sd_ad_group_reports` — List Sponsored Display ad group performance for one report date.
- `list_sd_campaign_reports` — List Sponsored Display campaign performance for one report date.
- `list_sd_product_ad_reports` — List Sponsored Display advertised-product performance for one report date.
- `list_sd_target_reports` — List Sponsored Display targeting performance for one report date.
- `list_sellers` — List all Amazon seller stores authorized in the Lingxing ERP account.
- `list_sp_ad_group_reports` — List Sponsored Products ad group performance for one report date.
- `list_sp_campaign_reports` — List Sponsored Products campaign performance for one report date.
- `list_sp_product_ad_reports` — List Sponsored Products advertised-product performance for one report date.
- `list_sp_target_reports` — List Sponsored Products targeting performance for one report date.
- `list_states` — List standardized state and province codes for a country.
- `list_world_states` — List states and provinces for an Amazon country configured in Lingxing.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Lingxing state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Lingxing is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/lingxing
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Lingxing homepage: https://www.lingxing.com
- API documentation: https://apidoc.lingxing.com/docs/Guidance/newInstructions
