---
name: oo-svix
description: "Svix (svix.com). Use this skill for ANY Svix request — reading, creating, updating, and deleting data. Whenever a task involves Svix, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Svix"
  author: "OOMOL"
  version: "1.0.1"
  services: ["svix"]
  icon: "https://static.oomol.com/logo/third-party/Svix.svg"
---

# Svix

Operate **Svix** through your OOMOL-connected account. This skill calls the `svix` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Svix. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "svix" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "svix" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_application` — Create a Svix application. [write]
- `create_endpoint` — Create a new endpoint for a Svix application. [write]
- `create_event_type` — Create or unarchive a Svix event type. [write]
- `create_message` — Create and dispatch a Svix message to an application's endpoints. [write]
- `delete_application` — Delete a Svix application by ID or UID. [destructive]
- `delete_endpoint` — Delete a Svix endpoint by application and endpoint identifier. [destructive]
- `get_application` — Fetch one Svix application by ID or UID.
- `get_endpoint` — Fetch one Svix endpoint by application and endpoint identifier.
- `get_event_type` — Fetch one Svix event type by name.
- `get_message` — Fetch one Svix message by application and message identifier.
- `list_applications` — List Svix applications for the current account.
- `list_endpoints` — List endpoints attached to a Svix application.
- `list_event_types` — List event types available to the current Svix account.
- `list_messages` — List messages that belong to a Svix application.
- `update_application` — Partially update a Svix application by ID or UID. [write]
- `update_endpoint` — Partially update an existing Svix endpoint. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Svix state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Svix is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=svix
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Svix homepage: https://www.svix.com
