---
name: oo-sendlane
description: "Sendlane (sendlane.com). Use this skill for ANY Sendlane request — reading, creating, updating, and deleting data. Whenever a task involves Sendlane, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sendlane"
  author: "OOMOL"
  version: "1.0.4"
  services: ["sendlane"]
  icon: "https://static.oomol.com/logo/third-party/sendlane.svg"
---

# Sendlane

Operate **Sendlane** through your OOMOL-connected account. This skill calls the `sendlane` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sendlane. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sendlane" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sendlane" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_custom_field` — Create a Sendlane custom field. [write]
- `create_list` — Create a Sendlane contact list. [write]
- `create_tag` — Create a Sendlane contact tag. [write]
- `delete_list` — Delete a Sendlane contact list by ID. [destructive]
- `delete_tag` — Delete a Sendlane contact tag by ID. [destructive]
- `get_campaign` — Get a Sendlane email campaign by ID.
- `get_custom_field` — Get a Sendlane custom field by ID.
- `get_list` — Get a Sendlane contact list by ID.
- `get_tag` — Get a Sendlane contact tag by ID.
- `list_campaigns` — List Sendlane email campaigns.
- `list_custom_fields` — List Sendlane custom fields.
- `list_lists` — List Sendlane contact lists.
- `list_tags` — List Sendlane contact tags.
- `update_custom_field` — Update a Sendlane custom field. [write]
- `update_list` — Update a Sendlane contact list. [write]
- `update_tag` — Update a Sendlane contact tag. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sendlane state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sendlane is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/sendlane
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Sendlane homepage: https://www.sendlane.com/
- API documentation: https://sendlane.stoplight.io/docs/api-documentation/c53add3c8b16f-overview
