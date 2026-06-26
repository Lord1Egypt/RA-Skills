# Open Poker Skill for Claude Code

A Claude Code skill that helps you build an autonomous poker bot for [Open Poker](https://openpoker.ai) — a free competitive platform where AI bots play No-Limit Texas Hold'em in 2-week seasons, climbing a public leaderboard for prizes.

## Install

1. Copy `openpoker.md` to your Claude Code commands folder:

**Mac/Linux:**
```bash
mkdir -p ~/.claude/commands
cp openpoker.md ~/.claude/commands/
```

**Windows:**
```bash
mkdir %USERPROFILE%\.claude\commands 2>nul
copy openpoker.md %USERPROFILE%\.claude\commands\
```

2. Start Claude Code and type `/openpoker`.

## What it does

When you run `/openpoker`, Claude will:

1. Fetch the latest Open Poker API docs (cached locally for 3 days)
2. Interview you about your bot:
   - What language do you want to build in?
   - Do you have your API key?
   - How do you want your bot to play? (Aggressive, conservative, bluff-heavy, GTO, adaptive, etc.)
   - How complex should the first version be?
3. Build your bot based on YOUR answers — not a generic template
4. Share production-tested gotchas discovered from running bots against the live server

## What you need

- **An Open Poker account** — Register via API or at [openpoker.ai](https://openpoker.ai)
- **Your API key** — Shown once at registration, save it
- **That's it** — no wallet, no money, no SDK. Any language with WebSocket + JSON works.

## What you'll build

The skill guides you through creating a bot with:

- **WebSocket client** — connects, authenticates, auto-reconnects
- **Game state tracker** — tracks cards, pot, stacks, positions
- **Strategy engine** — YOUR strategy, not a prescribed one
- **Main loop** — handles all server messages, season transitions, rebuys

## Platform overview

- Free to play — virtual chips, 2-week seasons
- 5,000 starting chips, 10/20 blinds, no rake
- Public leaderboard with prizes for top 3
- 6-max tables (2-6 players)
- All bot names visible — no anonymization
- Optional $3 Season Pass for analytics (not needed to play)

## Uninstall

```bash
rm ~/.claude/commands/openpoker.md
rm ~/.claude/openpoker-docs-cache.txt
```
