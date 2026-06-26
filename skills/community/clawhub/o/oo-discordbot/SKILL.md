---
name: oo-discordbot
description: "Discord Bot (discord.com). Use this skill for ANY Discord Bot request — reading, creating, updating, and deleting data. Whenever a task involves Discord Bot, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Discord Bot"
  author: "OOMOL"
  version: "1.0.1"
  services: ["discordbot"]
  icon: "https://static.oomol.com/logo/third-party/Discord%20Bot.svg"
---

# Discord Bot

Operate **Discord Bot** through your OOMOL-connected account. This skill calls the `discordbot` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Discord Bot. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "discordbot" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "discordbot" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `add_group_dm_user` — Add a recipient to a group DM channel. [write]
- `add_guild_member` — Add a user to a guild with a user access token. [write]
- `add_guild_member_role` — Add a role to a guild member. [write]
- `add_my_message_reaction` — Add a reaction as the current bot user. [write]
- `add_thread_member` — Add a member to a thread. [write]
- `ban_user_from_guild` — Ban a user from a guild. [destructive]
- `bulk_ban_users_from_guild` — Bulk ban users from a guild. [destructive]
- `bulk_delete_messages` — Bulk delete messages in a Discord channel. [destructive]
- `create_application_command` — Create a global application command. [write]
- `create_auto_moderation_rule` — Create a guild auto moderation rule. [write]
- `create_channel_invite` — Create an invite for a Discord channel. [write]
- `create_dm` — Create or fetch a DM channel with a recipient user. [write]
- `create_guild` — Create a guild with the platform bot token. [write]
- `create_guild_application_command` — Create a guild-scoped application command. [write]
- `create_guild_channel` — Create a channel in a guild. [write]
- `create_guild_emoji` — Create a guild emoji. [write]
- `create_guild_from_template` — Create a guild from a template with the platform bot token. [write]
- `create_guild_role` — Create a role in a guild. [write]
- `create_guild_scheduled_event` — Create a guild scheduled event. [write]
- `create_guild_sticker` — Create a guild sticker from base64 file content. [write]
- `create_guild_template` — Create a template for a guild. [write]
- `create_message` — Create a Discord channel message with the platform bot token. [write]
- `create_thread` — Create a thread in a Discord channel. [write]
- `create_thread_from_message` — Create a thread from a Discord message. [write]
- `crosspost_message` — Crosspost a message in an announcement channel.
- `delete_all_message_reactions` — Delete all reactions on a message. [destructive]
- `delete_all_message_reactions_by_emoji` — Delete all reactions for a specific emoji on a message. [destructive]
- `delete_application_command` — Delete a global application command. [destructive]
- `delete_auto_moderation_rule` — Delete an auto moderation rule. [destructive]
- `delete_channel` — Delete a channel. [destructive]
- `delete_channel_permission_overwrite` — Delete a channel permission overwrite. [destructive]
- `delete_group_dm_user` — Remove a recipient from a group DM channel. [destructive]
- `delete_guild` — Delete a guild owned by the platform bot. [destructive]
- `delete_guild_application_command` — Delete a guild-scoped application command. [destructive]
- `delete_guild_emoji` — Delete a guild emoji. [destructive]
- `delete_guild_integration` — Delete a guild integration. [destructive]
- `delete_guild_member` — Delete a user from a guild. [destructive]
- `delete_guild_member_role` — Delete a role from a guild member. [destructive]
- `delete_guild_role` — Delete a guild role. [destructive]
- `delete_guild_scheduled_event` — Delete a guild scheduled event. [destructive]
- `delete_guild_sticker` — Delete a guild sticker. [destructive]
- `delete_guild_template` — Delete a guild template. [destructive]
- `delete_message` — Delete a message in a Discord channel. [destructive]
- `delete_my_message_reaction` — Delete the current bot user's reaction on a message. [destructive]
- `delete_thread_member` — Delete a member from a thread. [destructive]
- `delete_user_message_reaction` — Delete another user's reaction on a message. [destructive]
- `follow_channel` — Follow an announcement channel into a target channel. [write]
- `get_active_guild_threads` — Get active threads for a guild.
- `get_application` — Get an application by id.
- `get_application_command` — Get a global application command.
- `get_application_role_connections_metadata` — Get application role connection metadata. [write]
- `get_application_user_role_connection` — Get the current user's application role connection. [write]
- `get_auto_moderation_rule` — Get an auto moderation rule.
- `get_bot_gateway` — Get gateway connection info for the platform bot.
- `get_channel` — Get a channel by id.
- `get_gateway` — Get the public Discord gateway URL.
- `get_guild` — Get a guild by id using the platform bot token.
- `get_guild_application_command` — Get a guild-scoped application command.
- `get_guild_application_command_permissions` — Get guild application command permissions.
- `get_guild_ban` — Get a specific guild ban by user id. [destructive]
- `get_guild_emoji` — Get a guild emoji by id.
- `get_guild_member` — Get a guild member by guild id and user id.
- `get_guild_preview` — Get the preview for a discoverable guild.
- `get_guild_scheduled_event` — Get a guild scheduled event.
- `get_guild_sticker` — Get a guild sticker by id.
- `get_guild_template` — Get a guild template by code.
- `get_guild_vanity_url` — Get the vanity invite for a guild.
- `get_guild_welcome_screen` — Get a guild welcome screen.
- `get_guild_widget` — Get the public guild widget JSON.
- `get_guild_widget_png` — Get the public guild widget PNG.
- `get_guild_widget_settings` — Get guild widget settings.
- `get_guilds_onboarding` — Get guild onboarding configuration.
- `get_message` — Get a message by channel id and message id.
- `get_my_application` — Get the current platform bot application.
- `get_my_oauth2_application` — Get the current OAuth2 application information.
- `get_public_keys` — Get Discord OAuth2 public keys.
- `get_sticker` — Get a sticker by id.
- `get_thread_member` — Get a thread member by user id.
- `get_user` — Get a user by id.
- `invite_resolve` — Resolve a guild or channel invite by code. [write]
- `invite_revoke` — Revoke an invite by code. [destructive]
- `join_thread` — Join a thread as the current bot user. [write]
- `leave_guild` — Leave a guild as the current bot user. [write]
- `leave_thread` — Leave a thread as the current bot user. [write]
- `list_application_commands` — List global application commands.
- `list_auto_moderation_rules` — List auto moderation rules for a guild.
- `list_channel_invites` — List invites for a channel.
- `list_guild_application_command_permissions` — List guild application command permissions.
- `list_guild_application_commands` — List guild-scoped application commands.
- `list_guild_audit_log_entries` — List audit log entries for a guild.
- `list_guild_bans` — List bans for a guild.
- `list_guild_channels` — List channels in a guild.
- `list_guild_emojis` — List emojis for a guild.
- `list_guild_integrations` — List guild integrations.
- `list_guild_invites` — List invites for a guild.
- `list_guild_members` — List guild members.
- `list_guild_roles` — List roles in a guild.
- `list_guild_scheduled_event_users` — List users for a guild scheduled event.
- `list_guild_scheduled_events` — List scheduled events for a guild.
- `list_guild_stickers` — List stickers for a guild.
- `list_guild_templates` — List templates for a guild.
- `list_guild_voice_regions` — List voice regions for a guild.
- `list_message_reactions_by_emoji` — List users who reacted to a message with a specific emoji.
- `list_messages` — List messages in a channel.
- `list_my_private_archived_threads` — List private archived threads joined by the current bot user.
- `list_pinned_messages` — List pinned messages in a channel.
- `list_private_archived_threads` — List private archived threads in a channel.
- `list_public_archived_threads` — List public archived threads in a channel.
- `list_sticker_packs` — List public sticker packs.
- `list_thread_members` — List thread members.
- `list_voice_regions` — List public voice regions.
- `pin_message` — Pin a message in a channel.
- `preview_prune_guild` — Preview how many members would be pruned from a guild.
- `prune_guild` — Prune inactive members from a guild.
- `put_guilds_onboarding` — Update guild onboarding configuration. [write]
- `search_guild_members` — Search guild members by query.
- `set_channel_permission_overwrite` — Create or update a channel permission overwrite. [write]
- `sync_guild_template` — Sync a guild template with the current guild state. [write]
- `test_auth` — Test the configured bot token against /users/@me.
- `trigger_typing_indicator` — Trigger the typing indicator in a channel. [write]
- `unban_user_from_guild` — Remove a guild ban for a user.
- `unpin_message` — Unpin a message in a channel.
- `update_application_command` — Update a global application command. [write]
- `update_application_user_role_connection` — Update the current user's application role connection. [write]
- `update_auto_moderation_rule` — Update an auto moderation rule. [write]
- `update_channel` — Update settings for an existing channel. [write]
- `update_guild` — Update guild settings. [write]
- `update_guild_application_command` — Update a guild-scoped application command. [write]
- `update_guild_emoji` — Update a guild emoji. [write]
- `update_guild_member` — Update a guild member. [write]
- `update_guild_role` — Update a guild role. [write]
- `update_guild_scheduled_event` — Update a guild scheduled event. [write]
- `update_guild_sticker` — Update a guild sticker. [write]
- `update_guild_template` — Update a guild template. [write]
- `update_guild_welcome_screen` — Update a guild welcome screen. [write]
- `update_guild_widget_settings` — Update guild widget settings. [write]
- `update_message` — Update a message in a Discord channel. [write]
- `update_my_guild_member` — Update the current bot user's guild member profile. [write]
- `update_my_user` — Update the current bot user's profile. [write]
- `update_self_voice_state` — Update the current bot user's voice state. [write]
- `update_voice_state` — Update another user's voice state. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Discord Bot state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Discord Bot is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=discordbot
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Discord Bot homepage: https://discord.com/developers/applications
