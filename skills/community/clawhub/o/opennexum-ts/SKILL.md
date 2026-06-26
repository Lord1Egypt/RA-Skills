---
name: opennexum-ts
version: 0.1.0
description: Contract-driven multi-agent orchestration with ACP. TypeScript CLI for spawning and tracking coding agents via OpenClaw sessions_spawn.
requires:
  node: ">=20"
  tools: [pnpm, openclaw]
---

# OpenNexum TS

Contract-driven coding agent orchestration via OpenClaw ACP.

## When to use
- Coordinating multiple AI coding agents on a project
- Running generator/evaluator pairs with automatic retry
- Tracking parallel ACP sessions with Telegram notifications

## Quick Start
1. `pnpm install && pnpm build`
2. Set env: TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
3. `nexum init` — initialize project
4. Create Contract YAML in docs/nexum/contracts/
5. `nexum spawn <taskId>` — get spawn payload
6. Call sessions_spawn with payload
7. `nexum track <taskId> <sessionKey>` — record session
8. `nexum eval <taskId>` + spawn evaluator
9. `nexum complete <taskId> <verdict>` — process result
