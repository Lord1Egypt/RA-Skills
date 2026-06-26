---
name: oo-ably
description: "Ably (ably.com). Use this skill for ANY Ably request — reading, creating, updating, and deleting data. Whenever a task involves Ably, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Ably"
  author: "OOMOL"
  version: "1.0.1"
  services: ["ably"]
  icon: "https://static.oomol.com/logo/third-party/ably.svg"
---

# Ably

Operate **Ably** through your OOMOL-connected account. This skill calls the `ably` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Ably. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "ably" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "ably" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `batch_presence` — Query current presence for multiple Ably channels.
- `batch_presence_history` — Query presence history for multiple Ably channels.
- `create_channel` — Activate an Ably channel by retrieving its metadata. [write]
- `delete_channel_subscription` — Delete an Ably push notification subscription for a channel, device, or client. [destructive]
- `get_channel_details` — Retrieve Ably metadata and occupancy details for one channel.
- `get_channel_history` — Retrieve message history for one Ably channel.
- `get_presence_history` — Retrieve presence history for one Ably channel.
- `get_service_time` — Retrieve Ably service time in milliseconds since the Unix epoch.
- `get_stats` — Retrieve Ably application usage statistics.
- `list_push_channel_subscriptions` — List Ably push notification channel subscriptions.
- `publish_message_to_channel` — Publish one message to an Ably channel. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Ably state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Ably is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=ably
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Ably homepage: https://ably.com
