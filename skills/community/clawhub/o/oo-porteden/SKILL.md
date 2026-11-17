---
name: oo-porteden
description: "PortEden (porteden.com). Use this skill for ANY PortEden request — reading, creating, updating, and deleting data. Whenever a task involves PortEden, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "PortEden"
  author: "OOMOL"
  version: "1.0.2"
  services: ["porteden"]
  icon: "https://static.oomol.com/logo/third-party/porteden.png"
---

# PortEden

Operate **PortEden** through your OOMOL-connected account. This skill calls the `porteden` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected PortEden. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "porteden" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "porteden" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_email` — Move an email to Trash or Deleted Items with PortEden delete_email permission. This is a recoverable soft delete. [destructive]
- `forward_email` — Forward an email to recipients with PortEden forward_email permission. [write]
- `get_email` — Read a provider-prefixed email, including its body by default, subject to PortEden view_email permissions.
- `get_thread` — Read a complete email thread in chronological order with body content, subject to PortEden view_thread permissions.
- `modify_email` — Change read status or labels/categories. PortEden requires mark_as_read and/or apply_labels permission for the requested changes. [write]
- `reply_email` — Reply to an email, preserving its thread, with PortEden reply_to_email permission. [write]
- `search_emails` — Search emails across connected Gmail and Microsoft 365 accounts. Email access and search_emails permission must be enabled in PortEden; pass nextPageToken as pageToken to continue.
- `send_email` — Send an email through a connected account with PortEden send_email permission. Choose sendFrom or connectionId when needed; the default account is otherwise used. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change PortEden state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — PortEden is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/porteden
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- PortEden homepage: https://porteden.com/
- API documentation: https://porteden.com/docs/api/authentication/
