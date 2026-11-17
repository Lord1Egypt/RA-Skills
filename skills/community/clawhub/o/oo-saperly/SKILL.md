---
name: oo-saperly
description: "Saperly (saperly.com). Use this skill for ANY Saperly request — reading, creating, updating, and deleting data. Whenever a task involves Saperly, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Saperly"
  author: "OOMOL"
  version: "1.0.2"
  services: ["saperly"]
  icon: "https://static.oomol.com/logo/third-party/saperly.png"
---

# Saperly

Operate **Saperly** through your OOMOL-connected account. This skill calls the `saperly` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Saperly. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "saperly" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "saperly" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `ask_assistant` — Ask the workspace assistant a question; the assistant may use workspace tools. [destructive]
- `assign_connection` — Bind a connection to a number [write]
- `check_consent` — Check whether a contact has active consent
- `create_connection` — Create a connection (provisions inline) [write]
- `create_custom_voice` — Upload a voice sample from a public URL; poll get_custom_voice until the voice is active or failed. [write]
- `create_workspace_key` — Create a scoped API token [write]
- `create_workspace_webhook` — Create a webhook endpoint [write]
- `delete_connection` — Delete a connection [destructive]
- `delete_custom_voice` — Delete custom voice [destructive]
- `end_call` — End a live call [destructive]
- `get_call` — Get a call by id
- `get_connection` — Get a connection by id
- `get_custom_voice` — Get custom voice
- `get_number` — Get a phone number by id
- `get_price_quote` — Quote the price of a phone number
- `get_recording` — Get a temporary download URL for a completed call recording.
- `get_transcript` — Get a call transcript
- `get_usage` — Get a usage summary (optionally since a timestamp)
- `health` — Liveness probe
- `list_calls` — List calls
- `list_connections` — List all connections in the workspace
- `list_consent` — List all consent records in the workspace
- `list_custom_voices` — List custom voices
- `list_keys` — List the workspace's API keys
- `list_languages` — List the supported spoken languages
- `list_messages` — List messages (optionally filtered by number)
- `list_numbers` — List all phone numbers in the workspace
- `list_voices` — List available voices (optionally filtered by language)
- `list_webhook_deliveries` — List a webhook endpoint's recent delivery attempts
- `list_workspace_audit_events` — List the workspace audit-log events
- `list_workspace_keys` — List the workspace API tokens
- `list_workspace_members` — List the workspace members
- `list_workspace_webhooks` — List the workspace webhook endpoints
- `mint_key` — Mint a scoped API key [write]
- `place_call` — Place an outbound call [write]
- `provision_number` — Provision a phone number [write]
- `record_consent` — Record consent for a contact [write]
- `release_number` — Release a phone number [destructive]
- `revoke_consent` — Revoke consent for a contact [destructive]
- `revoke_key` — Revoke an API key [destructive]
- `revoke_workspace_key` — Revoke an API token [destructive]
- `send_message` — Send an SMS message [write]
- `send_workspace_invitation` — Invite a member by email [write]
- `set_caller_id` — Set the outbound caller ID name (CNAM) [write]
- `set_number_webhook` — Set a number's manual-mode brain URL [write]
- `set_sms_sender` — Set the alphanumeric SMS sender id [write]
- `transfer_call` — Blind-transfer a live call [write]
- `update_connection` — Update a connection (re-syncs the carrier) [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Saperly state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Saperly is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/connections/saperly
  ```

- **`OOMOL_INSUFFICIENT_CREDIT`** — OOMOL billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

- **HTTP 402 without `OOMOL_INSUFFICIENT_CREDIT`** — the third-party account itself has no active plan or credit. Report the provider error message as is; do not ask the user to recharge OOMOL.

## Resources

- Saperly homepage: https://saperly.com
- API documentation: https://saperly.com/docs/
