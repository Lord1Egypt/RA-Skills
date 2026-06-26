# Grocery Checklist

Grocery Checklist is a pantry-backed shopping skill for OpenClaw.

It supports:
- persistent `needed` / `have` state
- natural language pantry updates like `I ran out of salt`
- shopping-list queries like `what do I need to buy`
- Telegram inline checklist buttons
- immediate mark-bought on tap in Telegram
- normal conversational handling through OpenClaw

## What this skill is

This is not a generic todo list.

It is a lightweight pantry state machine:
- `ran out of eggs` -> eggs become `needed`
- `bought eggs` -> eggs become `have`
- `what do I need to buy` -> only `needed` items are shown

If you want OpenClaw to be the source of truth and Telegram to be the shopping UI, this is the right shape.

## Intended install mode

The intended experience is:
- OpenClaw handles conversation normally
- this skill provides the grocery state/actions
- Telegram is just the UI surface for shopping list and pantry views

The default install path is the managed OpenClaw route, not a standalone Telegram parser bot.

## Files and config it uses

- reads `~/.openclaw/openclaw.json` when you bind a Telegram `grocery` account
- writes pantry state to `~/.openclaw/data/grocery-checklist/state.json`
- writes Telegram polling offset to `~/.openclaw/data/grocery-checklist/telegram-bot-state.json`
- uses the bundled wrapper at `scripts/grocery.sh`

## What the user needs

- `python3`
- `openclaw`
- a working OpenClaw Telegram bot if you want the inline checklist UI

Optional:
- a dedicated grocery Telegram bot/account bound to a dedicated OpenClaw agent

## Install summary

1. Put the skill at `~/.openclaw/skills/grocery-checklist`
2. Verify `python3` and `openclaw` are installed
3. Keep the bundled `index.js` in the skill root so OpenClaw can load the grocery tools and Telegram callback handler
4. Run the wrapper in `scripts/grocery.sh`
5. Bind a dedicated Telegram bot/account to grocery-only routing if you want Telegram UI
6. Let OpenClaw handle the conversation layer

Advanced:
- `scripts/telegram_bot.py` exists as an optional standalone bot implementation, but it is not the primary recommended setup

For the full process, read [SETUP.md](./SETUP.md).

## Good test prompts

- `I ran out of salt`
- `I ran out of eggs, rice, and bread`
- `what do I need to buy`
- `I bought eggs`

## For agents

Agent-specific operating rules live in [AGENTS.md](./AGENTS.md).
