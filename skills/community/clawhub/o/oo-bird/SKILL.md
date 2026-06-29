---
name: oo-bird
description: "Bird (bird.com). Use this skill for ANY Bird request — reading, creating, updating, and deleting data. Whenever a task involves Bird, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Bird"
  author: "OOMOL"
  version: "1.0.0"
  services: ["bird"]
  icon: "https://static.oomol.com/logo/third-party/bird.png"
---

# Bird

Operate **Bird** through your OOMOL-connected account. This skill calls the `bird` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Bird. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bird" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bird" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_contact` — Create a Bird contact with identifiers, attributes, display name, or list IDs. [write]
- `delete_contact` — Delete a Bird contact by ID. [destructive]
- `get_channel` — Retrieve a specific Bird workspace channel by ID.
- `get_contact` — Retrieve a Bird contact by ID, optionally requesting specific attributes.
- `get_message` — Retrieve a Bird channel message by ID.
- `list_channels` — List channels configured for a Bird workspace with optional filters.
- `list_contacts` — List contacts in a Bird workspace.
- `list_message_interactions` — List interactions recorded for a Bird channel message.
- `search_contact_by_identifier` — Search Bird contacts by an identifier key and value.
- `send_batch_messages` — Send a batch of up to 100 messages through a Bird workspace channel and return the accepted batch IDs. [write]
- `send_message` — Send one message through a Bird workspace channel. [write]
- `update_contact` — Update a Bird contact's identifiers, attributes, or list memberships. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Bird state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Bird is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=bird
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Bird homepage: https://bird.com
