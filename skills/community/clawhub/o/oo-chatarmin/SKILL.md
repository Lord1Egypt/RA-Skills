---
name: oo-chatarmin
description: "Chatarmin (chatarmin.com). Use this skill for ANY Chatarmin request — reading, creating, updating, and deleting data. Whenever a task involves Chatarmin, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chatarmin"
  author: "OOMOL"
  version: "1.0.6"
  services: ["chatarmin"]
  icon: "https://static.oomol.com/logo/third-party/chatarmin.svg"
---

# Chatarmin

Operate **Chatarmin** through your OOMOL-connected account. This skill calls the `chatarmin` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chatarmin. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chatarmin" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chatarmin" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_or_replace_voucher_codes` — Add new voucher codes to a Chatarmin pool or replace one unused code. [destructive]
- `create_contact` — Create a new Chatarmin contact. [write]
- `create_voucher_pool` — Create a Chatarmin voucher pool with an initial list of voucher codes. [write]
- `create_webhook` — Create a Chatarmin webhook for one supported topic. [write]
- `delete_contact` — Delete a Chatarmin contact by contact ID or externalId. [destructive]
- `delete_voucher_pool` — Delete a Chatarmin voucher pool and its unused voucher codes. [destructive]
- `delete_webhook` — Delete a Chatarmin webhook by webhook ID. [destructive]
- `get_campaign` — Retrieve one Chatarmin campaign by campaign ID.
- `get_contact` — Retrieve one Chatarmin contact by contact ID or externalId.
- `get_flow` — Retrieve one Chatarmin flow by flow ID.
- `get_flow_analytics` — Retrieve paginated Chatarmin flow analytics for a flow.
- `get_flow_contact_analytics` — Retrieve Chatarmin flow analytics for specific contacts.
- `get_voucher_pool` — Retrieve one Chatarmin voucher pool by voucher pool ID.
- `list_campaigns` — Retrieve a paginated list of Chatarmin campaigns with optional day or month metrics.
- `list_contacts` — Retrieve a paginated list of Chatarmin contacts with optional text search.
- `list_flows` — Retrieve a paginated list of Chatarmin flows with optional day or month metrics.
- `list_voucher_pools` — Retrieve a paginated list of Chatarmin voucher pools with voucher codes.
- `list_webhooks` — Retrieve all Chatarmin webhooks for the authenticated user.
- `remove_voucher_code` — Remove one unused voucher code from a Chatarmin voucher pool. [destructive]
- `send_message` — Send a WhatsApp text, media, document, or template message to a Chatarmin contact. [write]
- `update_contact` — Update an existing Chatarmin contact by contact ID or externalId. [write]
- `update_voucher_pool` — Update a Chatarmin voucher pool's name, settings, or unused voucher codes. [write]
- `update_webhook` — Update a Chatarmin webhook URL or topic. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chatarmin state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chatarmin is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chatarmin
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chatarmin homepage: https://chatarmin.com/
- API documentation: https://apidocs.chatarmin.com/reference/api-overview
