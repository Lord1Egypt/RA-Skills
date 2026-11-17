---
name: oo-chatra
description: "Chatra (chatra.com). Use this skill for ANY Chatra request — reading, creating, updating, and deleting data. Whenever a task involves Chatra, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chatra"
  author: "OOMOL"
  version: "1.0.2"
  services: ["chatra"]
  icon: "https://static.oomol.com/logo/third-party/chatra.svg"
---

# Chatra

Operate **Chatra** through your OOMOL-connected account. This skill calls the `chatra` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chatra. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chatra" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chatra" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_message` — Delete an agent message and return the deleted message. [destructive]
- `delete_pushed_message` — Delete an automated pushed message and return the deleted message. [destructive]
- `get_client` — Get visitor information by the secret visitor ID.
- `get_message` — Get an existing message by ID.
- `get_pushed_message` — Get an existing automated pushed message by ID.
- `send_message` — Send a message as an agent using an agent ID or an email identity. An unknown agent email creates a dummy agent. [write]
- `send_pushed_message` — Send an automated message to a visitor as a random agent, a specific agent, or a random agent from a group. [write]
- `update_client` — Update basic visitor information. Omitted fields stay unchanged; null removes a field. [write]
- `update_message` — Edit the text of an agent message. [write]
- `update_pushed_message` — Edit the text of an automated pushed message. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chatra state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chatra is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chatra
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chatra homepage: https://chatra.com/
- API documentation: https://chatra.com/help/api/#rest-api
