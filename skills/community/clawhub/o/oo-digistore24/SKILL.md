---
name: oo-digistore24
description: "Digistore24 (digistore24.com). Use this skill for ANY Digistore24 request — searching and reading data. Whenever a task involves Digistore24, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Digistore24"
  author: "OOMOL"
  version: "1.0.4"
  services: ["digistore24"]
  icon: "https://static.oomol.com/logo/third-party/digistore24.svg"
---

# Digistore24

Operate **Digistore24** through your OOMOL-connected account. This skill calls the `digistore24` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Digistore24. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "digistore24" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "digistore24" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_buyer` — Retrieve details for a Digistore24 buyer.
- `get_product` — Retrieve details for a Digistore24 product.
- `get_purchase` — Retrieve details for one or more Digistore24 purchases.
- `get_user_info` — Retrieve information about the Digistore24 user that owns the API key.
- `list_buyers` — List buyers from the connected Digistore24 account.
- `list_products` — List products from the connected Digistore24 account.
- `list_purchases` — List purchases and sales from the connected Digistore24 account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Digistore24 state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Digistore24 is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/digistore24
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Digistore24 homepage: https://www.digistore24.com
- API documentation: https://digistore24.com/api/docs/index.html
