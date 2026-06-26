# openclaw-feishu-multi-bot

One OpenClaw instance, multiple Feishu bot identities. Each Agent appears as an independent bot in Feishu with its own name, avatar, and group routing.

## What This Solves

When running multiple specialized Agents on OpenClaw, they share a single Feishu bot entry by default — all messages mix together. This skill teaches you how to give each Agent its own Feishu enterprise app, so users see completely separate assistants.

## What's Included

```
openclaw-feishu-multi-bot/
├── SKILL.md                           # Entry point — architecture overview + quick start
├── references/
│   ├── architecture.md                # Three-block config model, accountId mechanism
│   ├── build-guide.md                 # Step-by-step from Feishu console to gateway restart
│   ├── routing-deep-dive.md           # accountId consistency, binding rules, group isolation
│   └── troubleshooting.md             # Diagnostic flowchart + 7 common issues with fixes
└── scripts/
    └── setup-feishu-bots.sh           # Auto-generates channels/bindings/agents JSON blocks
```

## Quick Start

```bash
# Generate config for 3 agents
./scripts/setup-feishu-bots.sh \
  orchestrator:cli_xxx:secret1 \
  writer:cli_yyy:secret2 \
  coder:cli_zzz:secret3

# Merge output into openclaw.json, then:
openclaw doctor && openclaw gateway restart
```

## Key Lessons

- **accountId consistency** is the #1 failure point — must match in 3 places
- **Binding type must be `"route"`** — anything else crashes the gateway
- **Feishu apps must be published** — draft apps silently drop all messages
- **`agentToAgent` must be OFF** — breaks all sub-agent spawning (Bug #5813)
- **Incremental rollout** — add one bot at a time, not all at once

## Who This Is For

- OpenClaw users running 3+ Agents who want per-role Feishu entry points
- Teams using Feishu/Lark as their primary communication platform
- Anyone debugging Feishu bot routing issues in OpenClaw

## Author

[@simonlin1212](https://clawhub.ai/simonlin1212) — Based on production experience running 10+ Agents with independent Feishu bots
