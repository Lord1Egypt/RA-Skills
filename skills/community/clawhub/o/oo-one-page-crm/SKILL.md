---
name: oo-one-page-crm
description: "OnePageCRM (onepagecrm.com). Use this skill for ANY OnePageCRM request — reading, creating, and updating data. Whenever a task involves OnePageCRM, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "OnePageCRM"
  author: "OOMOL"
  version: "1.0.0"
  services: ["one_page_crm"]
  icon: "https://static.oomol.com/logo/third-party/one_page_crm.svg"
---

# OnePageCRM

Operate **OnePageCRM** through your OOMOL-connected account. This skill calls the `one_page_crm` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected OnePageCRM. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "one_page_crm" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "one_page_crm" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a OnePageCRM contact using JSON-safe contact fields. [write]
- `create_deal` — Create a OnePageCRM deal using JSON-safe deal fields. [write]
- `get_contact` — Retrieve a single OnePageCRM contact by ID.
- `get_deal` — Retrieve a single OnePageCRM deal by ID.
- `list_contacts` — List OnePageCRM contacts with pagination, search, ownership, tag, and sorting filters.
- `list_deals` — List OnePageCRM deals with pagination, search, status, contact, owner, tag, and sorting filters.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change OnePageCRM state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — OnePageCRM is not connected, or the connection expired or lacks a scope. Connect once (auth type: custom credential) at:

  ```text
  https://console.oomol.com/app-connections?provider=one_page_crm
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- OnePageCRM homepage: https://www.onepagecrm.com/
