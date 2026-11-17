---
name: oo-pylon
description: "Pylon (usepylon.com). Use this skill for ANY Pylon request — reading, creating, and updating data. Whenever a task involves Pylon, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Pylon"
  author: "OOMOL"
  version: "1.0.5"
  services: ["pylon"]
  icon: "https://static.oomol.com/logo/third-party/pylon.svg"
---

# Pylon

Operate **Pylon** through your OOMOL-connected account. This skill calls the `pylon` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Pylon. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "pylon" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "pylon" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_account` — Create a Pylon account. [write]
- `create_contact` — Create a Pylon contact. [write]
- `create_issue` — Create a Pylon issue with a title, HTML body, and requester or account context. [write]
- `create_issue_note` — Create an internal note on a Pylon issue. [write]
- `get_account` — Fetch one Pylon account by account ID or external ID.
- `get_contact` — Fetch one Pylon contact by contact ID with optional paginated account context.
- `get_issue` — Fetch one Pylon issue by ID or issue number.
- `get_me` — Fetch the Pylon organization associated with the API token.
- `list_issue_messages` — List messages, replies, and internal notes on one Pylon issue.
- `list_issues` — List Pylon issues within a required time range of up to 30 days.
- `search_accounts` — Search Pylon accounts with a filter and optional fuzzy text search.
- `search_contacts` — Search Pylon contacts with a filter and optional fuzzy text search.
- `update_issue` — Update mutable fields on one Pylon issue by ID or issue number. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Pylon state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Pylon is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/pylon
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Pylon homepage: https://www.usepylon.com
- API documentation: https://docs.usepylon.com/pylon-docs/developer/api
