---
name: guandan
slug: guandan
description: >-
  Play GuanDan(掼蛋) card game via `clawguandan CLI`. Use when users ask to play GuanDan or create/list/join tables in game.
metadata:
  openclaw:
    emoji: "🃏"
    os:
      - linux
      - darwin
    requires:
      bins: ["npm"]
---

# Guandan

You can play **GuanDan** (掼蛋) card game through the `clawguandan CLI` as one or more AI players.

## Prerequisites

1) Check CLI available
   Run the CLI wrapper:
   ```
   ./scripts/run.sh show version
   ```
   When not found, install it first if the user trust it.

2) Check server ready
   Run:
   ```
   ./scripts/run.sh server status
   ```
   If the `status` is unreachable, you can restart the local server:
   ```
   ./scripts/run.sh server restart
   ```
   You can see the Web UI URLs for human users once everything is ready.

## Quick start (Bot Mode, default)

1) Read the current table list:
   ```
   ./scripts/run.sh table list
   ```

2) Confirm whether **you** should create the table or the user already specified a table.
   - If you create the table, run `./scripts/run.sh table create "<a_cool_table_name>"` and obtain `tableId`.

3) Confirm with the user how many **Bot players** should join, then run the command in background:
   ```
   ./scripts/run.sh bot llm-bot --default-script openclaw --players <number_of_bot_players> -t <tableId> -v
   ```
   If some error occurs, try to fix it and retry.

4) If it still does not work, confirm with user to degrade to rule-based bot player.
   ```
   ./scripts/run.sh bot rule-bot --players <number_of_bot_players> -t <tableId> -v
   ```

5) Game started. Report game status when needed.

## Security notes

This skill wraps the clawguandan CLI.
* The CLI communicates only with a local server process and local agent.
* It does not require API keys, tokens, or external credentials by default.
* It does not send data to external services unless the user explicitly configures it to do so.