---
name: oo-sendbird
description: "Sendbird (sendbird.com). Use this skill for ANY Sendbird request — reading, creating, updating, and deleting data. Whenever a task involves Sendbird, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Sendbird"
  author: "OOMOL"
  version: "1.0.1"
  services: ["sendbird"]
  icon: "https://static.oomol.com/logo/third-party/Sendbird.svg"
---

# Sendbird

Operate **Sendbird** through your OOMOL-connected account. This skill calls the `sendbird` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Sendbird. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "sendbird" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "sendbird" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_members_group_channel` — Invite members into an existing Sendbird group channel. [write]
- `ban_user_from_group_channel` — Ban a user from a Sendbird group channel. [destructive]
- `create_channel` — Create a Sendbird group channel with common JSON body fields. [write]
- `create_user` — Create a Sendbird user with common profile and metadata fields. [write]
- `delete_channel` — Delete a Sendbird group channel. [destructive]
- `delete_message` — Delete a Sendbird group channel message. [destructive]
- `delete_user` — Delete a Sendbird user. [destructive]
- `get_number_of_channels_by_join_status` — Get Sendbird group channel counts grouped by join status. [write]
- `get_number_of_unread_items` — Get unread message, mention, and invitation counts for a Sendbird user.
- `issue_session_token` — Issue a Sendbird session token for a user.
- `leave_group_channels` — Make a Sendbird user leave one or more joined group channels. [write]
- `list_banned_members` — List banned users from a Sendbird group channel.
- `list_group_channel_messages` — List messages from a Sendbird group channel around a timestamp or message anchor.
- `list_group_channels` — List Sendbird group channels in the application with common filtering controls.
- `list_members_group_channel` — List members of a Sendbird group channel.
- `list_users` — List Sendbird users with common pagination and filtering controls.
- `mark_all_user_messages_as_read` — Mark all messages as read for a Sendbird user. [write]
- `mute_user` — Mute a user in a Sendbird group channel. [write]
- `revoke_all_session_tokens` — Revoke all Sendbird session tokens for a user. [destructive]
- `send_message` — Send a message into a Sendbird group channel. [write]
- `unban_user` — Unban a user from a Sendbird group channel.
- `unmute_user` — Unmute a user in a Sendbird group channel. [write]
- `update_group_channel` — Update a Sendbird group channel with common JSON body fields. [write]
- `update_message` — Update an existing Sendbird group channel message. [write]
- `update_user` — Update a Sendbird user's profile, metadata, or activation settings. [write]
- `view_group_channel` — Get a Sendbird group channel by channel URL.
- `view_message` — Get a single Sendbird group channel message by message ID.
- `view_user` — Get a single Sendbird user by user ID.

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Sendbird state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Sendbird is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=sendbird
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Sendbird homepage: https://sendbird.com
