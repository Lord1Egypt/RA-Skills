---
name: oo-loyverse
description: "Loyverse (loyverse.com). Use this skill for ANY Loyverse request — searching and reading data. Whenever a task involves Loyverse, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Loyverse"
  author: "OOMOL"
  version: "1.0.1"
  services: ["loyverse"]
  icon: "https://static.oomol.com/logo/third-party/loyverse.svg"
---

# Loyverse

Operate **Loyverse** through your OOMOL-connected account. This skill calls the `loyverse` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Loyverse. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "loyverse" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "loyverse" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_category` — Get one Loyverse category by ID.
- `get_customer` — Get one Loyverse customer by ID.
- `get_item` — Get one Loyverse item by ID.
- `get_merchant` — Get merchant profile information for the connected Loyverse account.
- `get_receipt` — Get one Loyverse receipt by receipt number.
- `get_store` — Get one Loyverse store by ID.
- `list_categories` — List item categories in the connected Loyverse account.
- `list_customers` — List customers in the connected Loyverse account.
- `list_items` — List items in the connected Loyverse account.
- `list_receipts` — List receipts in the connected Loyverse account.
- `list_stores` — List stores in the connected Loyverse account.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Loyverse state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Loyverse is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=loyverse
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Loyverse homepage: https://loyverse.com/
