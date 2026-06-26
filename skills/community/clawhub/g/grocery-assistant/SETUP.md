# Setup

This is the shortest reliable setup for a real user.

The goal is not just "show a list." The goal is to keep pantry state in OpenClaw and expose a Telegram-friendly shopping checklist.

Recommended architecture:
- OpenClaw handles normal conversation
- this skill handles grocery state and actions
- Telegram is the UI surface for shopping list and pantry rendering
- use a dedicated `grocery` Telegram account if you want the cleanest separation

This package:
- includes `index.js` at the skill root so OpenClaw can load the grocery tools and Telegram callback handler
- reads `~/.openclaw/openclaw.json` for the Telegram `grocery` account token and allowlist when Telegram is enabled
- writes pantry state to `~/.openclaw/data/grocery-checklist/state.json`
- writes Telegram polling state to `~/.openclaw/data/grocery-checklist/telegram-bot-state.json`
- executes only the bundled scripts in this skill folder

## 1. Install the skill

Put this skill at:

```bash
~/.openclaw/skills/grocery-checklist
```

## 2. Verify prerequisites

You need:

```bash
python3 --version
openclaw --version
```

## 3. Smoke test the local wrapper

Run:

```bash
bash ~/.openclaw/skills/grocery-checklist/scripts/grocery.sh need salt eggs
bash ~/.openclaw/skills/grocery-checklist/scripts/grocery.sh show
```

## 4. Connect Telegram Through OpenClaw

This skill works best when the grocery bot is separate from your main assistant bot.

Typical shape:

```bash
openclaw channels add --channel telegram --account grocery --name "Grocery Shopping" --token <telegram-bot-token>
openclaw agents add grocery --workspace ~/.openclaw/workspace --bind telegram:grocery --non-interactive
```

Route grocery messages for that bot to this skill's wrapper and let OpenClaw stay in charge of conversation handling.

## 5. Allow exec approvals

If your OpenClaw setup requires exec approvals, allowlist:

```bash
~/.openclaw/skills/grocery-checklist/scripts/grocery.sh
~/.openclaw/skills/grocery-checklist/scripts/*.py
```

## 6. Smoke test in chat

Try:

```text
I ran out of salt and eggs
what do I need to buy
I bought eggs
```

## 7. Smoke test in Telegram

If you wired a Telegram bot:
- ask `what do i need to buy`
- tap a few items
- each tap immediately marks that item bought

## Common failures

`exec approval is required`
- allowlist the grocery wrapper and script paths

`wrong Telegram bot receives the checklist`
- make sure the `grocery` Telegram account is configured in `~/.openclaw/openclaw.json`

`button taps do nothing`
- confirm your OpenClaw Telegram route preserves `gchk:...` callback payloads

`list shows prose instead of checklist`
- your grocery Telegram route is probably going through a generic assistant prompt instead of the grocery skill path

## Advanced: standalone bot

`scripts/telegram_bot.py` is included as an optional standalone Telegram bot implementation.

Use it only if you explicitly want to bypass OpenClaw's managed conversation layer. The recommended install path is still the managed OpenClaw route above.
