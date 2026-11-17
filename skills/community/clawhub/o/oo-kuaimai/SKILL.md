---
name: oo-kuaimai
description: "Kuaimai ERP (kuaimai.com). Use this skill for ANY Kuaimai ERP request — reading, creating, and updating data. Whenever a task involves Kuaimai ERP, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Kuaimai ERP"
  author: "OOMOL"
  version: "1.0.5"
  services: ["kuaimai"]
  icon: "https://static.oomol.com/logo/third-party/kuaimai.png"
---

# Kuaimai ERP

Operate **Kuaimai ERP** through your OOMOL-connected account. This skill calls the `kuaimai` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Kuaimai ERP. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "kuaimai" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "kuaimai" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_product` — Get one Kuaimai ERP product by system ID or merchant product code.
- `list_inventory` — List warehouse inventory for a Kuaimai merchant product or SKU code.
- `list_orders` — List Kuaimai ERP orders, excluding Taobao/Tmall and Pinduoduo orders that require separate platform credentials.
- `list_products` — List products and their SKU records from Kuaimai ERP.
- `list_sales_stockouts` — List Kuaimai ERP sales stockout records and their order details.
- `list_shops` — List shops configured for the connected Kuaimai ERP company.
- `list_warehouses` — List warehouses configured for the connected Kuaimai ERP company.
- `refresh_session` — Extend the Kuaimai Open Platform session validity by another 30 days. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Kuaimai ERP state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Kuaimai ERP is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/connections/kuaimai
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Kuaimai ERP homepage: https://www.kuaimai.com/
- API documentation: https://open.kuaimai.com/docs/api/API%E5%AF%B9%E6%8E%A5%E8%AF%B4%E6%98%8E/%E6%8E%A5%E5%85%A5%E6%8C%87%E5%8D%97/
