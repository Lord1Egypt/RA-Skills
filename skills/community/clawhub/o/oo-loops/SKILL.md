---
name: oo-loops
description: "Loops (loops.so). Use this skill for ANY Loops request — reading, creating, updating, and deleting data. Whenever a task involves Loops, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Loops"
  author: "OOMOL"
  version: "1.0.2"
  services: ["loops"]
  icon: "https://static.oomol.com/logo/third-party/loops.png"
---

# Loops

Operate **Loops** through your OOMOL-connected account. This skill calls the `loops` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Loops. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "loops" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "loops" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a Loops contact with default and custom contact properties. [write]
- `create_contact_property` — Create a custom contact property in Loops. [write]
- `delete_contact` — Delete a Loops contact by email or userId. [destructive]
- `find_contact` — Find Loops contacts by email or userId.
- `list_contact_properties` — List default or custom Loops contact properties.
- `list_mailing_lists` — List Loops mailing lists available to the current API key.
- `send_event` — Send a Loops event to trigger workflows for a contact. [write]
- `update_contact` — Update or create a Loops contact by email or userId. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Loops state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Loops is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=loops
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Loops homepage: https://loops.so
