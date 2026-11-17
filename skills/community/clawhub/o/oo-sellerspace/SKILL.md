---
name: oo-sellerspace
description: "SellerSpace (sellerspace.com). Use this skill for ANY SellerSpace request — searching and reading data. Whenever a task involves SellerSpace, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SellerSpace"
  author: "OOMOL"
  version: "1.0.4"
  services: ["sellerspace"]
  icon: "https://static.oomol.com/logo/third-party/sellerspace.png"
---

# SellerSpace

Operate **SellerSpace** through your OOMOL-connected account. This skill calls the `sellerspace` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SellerSpace. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sellerspace" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sellerspace" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `call_tool` — Call an explicitly approved SellerSpace MCP read tool with JSON arguments after discovering its live schema. Write, export, and browser-task tools are unavailable through this action.
- `discover_fields` — Discover current SellerSpace fields for advanced selection, filtering, sorting, or output interpretation in a supported data domain.
- `get_ad_metric_history` — Get time-series or placement-level metrics for one SellerSpace advertising campaign, ad group, promoted product, keyword, target, or search term.
- `list_fba_shipments` — List SellerSpace FBA inbound shipments with status, warehouse, quantities, and SKU-level receiving differences for one Amazon store and marketplace.
- `list_stores` — List Amazon stores and marketplaces authorized in SellerSpace so their seller IDs and marketplace codes can be used in subsequent queries.
- `list_tools` — Discover SellerSpace tools approved by Connector for read-only dynamic calls, including their live input schemas and behavior annotations.
- `query_ads` — Query SellerSpace Amazon advertising campaigns, ad groups, promoted products, keywords, targets, search terms, or negative targeting with filters and pagination.
- `query_products` — Query SellerSpace product performance or long-term storage fee data across one or more Amazon store-marketplace stations.
- `query_store_performance` — Query SellerSpace store or marketplace performance, including orders, revenue, profit, refunds, advertising spend, FBA fees, ROI, and ACoS.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SellerSpace state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SellerSpace is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sellerspace
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SellerSpace homepage: https://www.sellerspace.com/
- API documentation: https://www.sellerspace.com/help/doc/sellerspace-mcp-configuration-tutorial/
