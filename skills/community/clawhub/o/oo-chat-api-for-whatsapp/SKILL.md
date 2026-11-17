---
name: oo-chat-api-for-whatsapp
description: "Chat API for WhatsApp (chat-api.com). Use this skill for ANY Chat API for WhatsApp request — reading, creating, and updating data. Whenever a task involves Chat API for WhatsApp, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Chat API for WhatsApp"
  author: "OOMOL"
  version: "1.0.4"
  services: ["chat_api_for_whatsapp"]
  icon: "https://static.oomol.com/logo/third-party/chat_api_for_whatsapp.png"
---

# Chat API for WhatsApp

Operate **Chat API for WhatsApp** through your OOMOL-connected account. This skill calls the `chat_api_for_whatsapp` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Chat API for WhatsApp. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "chat_api_for_whatsapp" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "chat_api_for_whatsapp" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `get_settings` — Get the current webhook, notification, video upload, and proxy settings.
- `get_status` — Get the current Chat API WhatsApp instance status and QR code payload when authorization is pending.
- `list_chats` — List chats known to the connected Chat API WhatsApp instance.
- `list_messages` — List incoming and outgoing messages, optionally filtered by chat ID or paged from a previous response.
- `list_messages_queue` — List outbound messages currently waiting in the Chat API send queue.
- `send_file_by_url` — Send a file using a public URL to an existing Chat API chat ID or to a phone number. [write]
- `send_text_message` — Send a text message to an existing Chat API chat ID or to a phone number. [write]
- `test_api_key` — Validate the connected Chat API token and instance ID, returning the current instance status.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Chat API for WhatsApp state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Chat API for WhatsApp is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/chat_api_for_whatsapp
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Chat API for WhatsApp homepage: https://chat-api.com/en/
- API documentation: https://chat-api.com/en/docs.html
