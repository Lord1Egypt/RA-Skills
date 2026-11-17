---
name: oo-mailosaur
description: "Mailosaur (mailosaur.com). Use this skill for ANY Mailosaur request — reading, creating, updating, and deleting data. Whenever a task involves Mailosaur, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Mailosaur"
  author: "OOMOL"
  version: "1.0.4"
  services: ["mailosaur"]
  icon: "https://static.oomol.com/logo/third-party/mailosaur.svg"
---

# Mailosaur

Operate **Mailosaur** through your OOMOL-connected account. This skill calls the `mailosaur` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Mailosaur. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "mailosaur" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "mailosaur" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_server` — Create a new Mailosaur inbox server. [write]
- `delete_all_messages` — Delete all Mailosaur messages stored in one server. [destructive]
- `delete_message` — Delete one Mailosaur message and its attachments. [destructive]
- `delete_server` — Delete one Mailosaur inbox server and its stored messages. [destructive]
- `get_message` — Retrieve one Mailosaur message by ID, including parsed body content.
- `get_server` — Retrieve one Mailosaur inbox server by ID.
- `get_usage_limits` — Retrieve Mailosaur account usage limits.
- `list_messages` — List Mailosaur message summaries from one server.
- `list_servers` — List Mailosaur inbox servers in the current account.
- `list_usage_transactions` — List the last 31 days of Mailosaur usage transactions.
- `search_messages` — Search Mailosaur message summaries in one server.
- `update_server` — Update the name of one Mailosaur inbox server. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Mailosaur state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Mailosaur is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/mailosaur
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Mailosaur homepage: https://mailosaur.com
- API documentation: https://mailosaur.com/docs/api
