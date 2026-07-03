---
name: oo-bot-star
description: "BotStar (botstar.com). Use this skill for ANY BotStar request — reading, creating, updating, and deleting data. Whenever a task involves BotStar, use this skill instead of calling the API directly."
allowed-tools: [Bash(oo *)]
metadata:
  title: "BotStar"
  author: "OOMOL"
  version: "1.0.0"
  services: ["bot_star"]
  icon: "https://static.oomol.com/logo/third-party/bot_star.svg"
---

# BotStar

Operate **BotStar** through your OOMOL-connected account. This skill calls the `bot_star` connector with the [oo CLI](https://github.com/oomol-lab/oo-cli); OOMOL injects credentials server-side, so you never handle raw tokens.

## Running an action

Assume the user has already installed the oo CLI, signed in, and connected BotStar. **Do not run `oo auth login` or open the connection URL proactively — just run the action.** Fall back to [First-time setup](#first-time-setup) only when a command actually fails with an auth or connection error.

**1. Inspect the contract** to get the authoritative input/output schema before building a payload:

```bash
oo connector schema "bot_star" --action "<action_name>"
```

**2. Run the action** with a JSON payload that matches the input schema:

```bash
oo connector run "bot_star" --action "<action_name>" --data '<json>' --json
```

- `--data` takes a JSON object string or `@path/to/file.json`; omit it to send `{}`.
- The response is `{ "data": ..., "meta": { "executionId": "..." } }`; the execution id lives under `meta.executionId`.

Each action is listed below with a one-line description; actions that change state carry a `[write]` or `[destructive]` tag. Before constructing `--data`, fetch the action's live schema with `oo connector schema` to get its authoritative input fields.

## Available actions

- `create_bot` — Create a new BotStar bot. [write]
- `create_bot_attribute` — Create an attribute on a BotStar bot. [write]
- `create_cms_entity` — Create a BotStar CMS entity. [write]
- `create_cms_entity_item` — Create an item in a BotStar CMS entity. [write]
- `create_user_attribute` — Create a custom user attribute field for a BotStar bot. [write]
- `delete_bot_attribute` — Delete a BotStar bot attribute. [destructive]
- `delete_cms_entity` — Delete a BotStar CMS entity. [destructive]
- `delete_cms_entity_item` — Delete an item from a BotStar CMS entity. [destructive]
- `get_bot` — Get one BotStar bot by ID.
- `get_cms_entity` — Get one BotStar CMS entity by ID.
- `get_cms_entity_item` — Get one item from a BotStar CMS entity.
- `get_user` — Get a BotStar audience user by bot ID and user ID.
- `list_bot_attributes` — List attributes configured for a BotStar bot.
- `list_bots` — List bots available to the configured BotStar API token.
- `list_cms_entities` — List CMS entities configured for a BotStar bot.
- `list_cms_entity_items` — List items in a BotStar CMS entity.
- `publish_bot` — Publish BotStar bot changes to the live environment. [write]
- `update_bot_attribute` — Update an existing BotStar bot attribute. [write]
- `update_cms_entity` — Update a BotStar CMS entity. [write]
- `update_cms_entity_item` — Update an item in a BotStar CMS entity. [write]
- `update_user_attributes` — Update attributes on a BotStar audience user. [write]

## Safety

- Untagged actions are reads (get / list / search) — safe to run directly.
- **Actions tagged `[write]` change BotStar state — confirm the exact payload and effect with the user before running.**
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

- **`scope_missing` / `credential_expired` / `app_not_ready` / `app_not_found`** — BotStar is not connected, or the connection expired or lacks a scope. Connect once (auth type: API key) at:

  ```text
  https://console.oomol.com/app-connections?provider=bot_star
  ```

- **HTTP 402 / `OOMOL_INSUFFICIENT_CREDIT`** — billing stop. Recharge at `https://console.oomol.com/billing/token-recharge` before retrying.

## Resources

- BotStar homepage: https://botstar.com
