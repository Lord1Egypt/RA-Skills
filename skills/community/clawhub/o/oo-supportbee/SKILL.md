---
name: oo-supportbee
description: "SupportBee (supportbee.com). Use this skill for ANY SupportBee request — reading, creating, updating, and deleting data. Whenever a task involves SupportBee, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "SupportBee"
  author: "OOMOL"
  version: "1.0.6"
  services: ["supportbee"]
  icon: "https://static.oomol.com/logo/third-party/supportbee.png"
---

# SupportBee

Operate **SupportBee** through your OOMOL-connected account. This skill calls the `supportbee` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected SupportBee. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "supportbee" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "supportbee" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_label_to_ticket` — Add an existing SupportBee label to a ticket. [write]
- `create_ticket` — Create a SupportBee ticket with JSON body content and optional email recipients. [write]
- `create_ticket_comment` — Create a SupportBee ticket comment with JSON body content. [write]
- `create_ticket_reply` — Create a SupportBee ticket reply with JSON body content. [write]
- `create_user` — Create a SupportBee user or customer group. [write]
- `get_ticket` — Retrieve a SupportBee ticket by ID.
- `get_ticket_reply` — Retrieve one SupportBee ticket reply by ticket ID and reply ID.
- `get_user` — Retrieve one SupportBee user or customer group by ID.
- `list_labels` — List custom SupportBee labels for the connected desk.
- `list_teams` — List SupportBee teams with optional user expansion filters.
- `list_ticket_comments` — List comments for a SupportBee ticket.
- `list_ticket_replies` — List replies for a SupportBee ticket.
- `list_tickets` — List SupportBee tickets with optional official ticket filters.
- `list_users` — List SupportBee users and customer groups.
- `remove_label_from_ticket` — Remove a SupportBee label from a ticket. [destructive]
- `search_tickets` — Search SupportBee tickets by query text with optional pagination filters.
- `update_user` — Update a SupportBee user or customer group by ID. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change SupportBee state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — SupportBee is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/supportbee
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- SupportBee homepage: https://supportbee.com
- API documentation: https://supportbee.com/docs/api/api
