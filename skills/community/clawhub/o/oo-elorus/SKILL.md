---
name: oo-elorus
description: "Elorus (elorus.com). Use this skill for ANY Elorus request — reading, creating, and updating data. Whenever a task involves Elorus, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Elorus"
  author: "OOMOL"
  version: "1.0.1"
  services: ["elorus"]
  icon: "https://static.oomol.com/logo/third-party/elorus.svg"
---

# Elorus

Operate **Elorus** through your OOMOL-connected account. This skill calls the `elorus` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Elorus. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "elorus" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "elorus" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create one Elorus contact in the selected organization. [write]
- `create_invoice` — Create one Elorus invoice in the selected organization. [write]
- `create_product` — Create one Elorus product or service in the selected organization. [write]
- `get_contact` — Get one Elorus contact by ID.
- `get_invoice` — Get one Elorus invoice by ID.
- `get_product` — Get one Elorus product or service by ID.
- `list_contacts` — List Elorus contacts with optional search, filters, and pagination.
- `list_invoices` — List Elorus invoices with optional filters and pagination.
- `list_products` — List Elorus products or services with optional filters and pagination.
- `update_contact` — Update one Elorus contact by ID. [write]
- `update_invoice` — Update one Elorus invoice by ID using the official full-update endpoint. [write]
- `update_product` — Update one Elorus product or service by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Elorus state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Elorus is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=elorus
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Elorus homepage: https://www.elorus.com/
