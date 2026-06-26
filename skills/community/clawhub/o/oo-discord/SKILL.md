---
name: oo-discord
description: "Discord (discord.com). Use this skill for ANY Discord request — reading, creating, updating, and deleting data. Whenever a task involves Discord, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "Discord"
  author: "OOMOL"
  version: "1.0.2"
  services: ["discord"]
  icon: "https://static.oomol.com/logo/third-party/Discord.svg"
---

# Discord

Operate **Discord** through your OOMOL-connected account. This skill calls the `discord` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected Discord. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "discord" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "discord" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `delete_my_application_role_connection` — Remove the current OAuth user's role connection data for a Discord application. [destructive]
- `get_current_user_application_entitlements` — Get entitlements for the current OAuth user under a Discord application.
- `get_gateway` — Get a Discord Gateway URL.
- `get_guild_template` — Get a Discord guild template by code.
- `get_guild_widget` — Get a Discord guild widget as JSON.
- `get_guild_widget_png` — Get a Discord guild widget PNG.
- `get_invite` — Get a Discord invite by code or URL. [write]
- `get_my_application_role_connection` — Read the current OAuth user's role connection data for a Discord application. [write]
- `get_my_guild_member` — Get the current OAuth user's member record in a guild.
- `get_my_oauth2_authorization` — Get the current OAuth2 authorization information.
- `get_my_user` — Get the current OAuth user profile.
- `get_openid_connect_userinfo` — Get OpenID Connect userinfo for the current OAuth user.
- `get_public_keys` — Get Discord OAuth2 public keys as JWKS.
- `get_user` — Get a Discord user. OAuth mode only supports @me in this provider.
- `list_my_connections` — List the current OAuth user's linked connections.
- `list_my_guilds` — List the current OAuth user's guilds.
- `list_sticker_packs` — List Discord Nitro sticker packs.
- `resolve_invite` — Resolve a Discord invite by code. [write]
- `update_my_application_role_connection` — Set the current OAuth user's role connection platform fields or metadata for a Discord application. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change Discord state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — Discord is not connected, or the connection expired or lacks a scope. Connect once (auth type: OAuth2) at:

  ```text
  https://console.oomol.com/app-connections?provider=discord
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- Discord homepage: https://discord.com
