# 🤖 Multi-Agent Architecture — Run Multiple AI Agents on One Server

Build a team of specialized AI agents on a single VPS. Each with its own role, memory, skills, and Telegram bot.

## Why Use This

| Single agent | Multi-agent with this skill |
|---|---|
| One bot does everything (badly) | **Specialized agents** — each expert in their domain |
| Rate limits by Wednesday | **60% fewer rate limit hits** with multi-token strategy |
| Giant context = wasted tokens | **75% less token burn** with optimized AGENTS.md (<5KB) |
| Service crashes at 3 AM, you find out at 9 AM | **Self-healing** — auto-restart in under 5 minutes |
| €200/mo for multiple VPS | **5 agents on one €47/mo VPS** |
| Memory stays in one agent | **Shared knowledge** across all agents |

## What's Inside

- **Architecture design**: plan agent roles, workspaces, communication
- **Workspace isolation**: separate memory, skills, configs per agent
- **Telegram routing**: one bot per agent OR topic-based routing in forums
- **Rate limit management**: multi-token, model selection per agent priority
- **Shared memory**: three-tier (hot → warm → deep knowledge graph)
- **Monitoring**: heartbeats, self-healing, watchdog daemon
- **Backup & recovery**: automated daily backups, 7-day retention
- **Production checklist**: 10-point verification

## Built From Experience

Extracted from running **5 production agents** on a single VPS for 3+ months:
- Main (CEO/strategy) + Ops (monitoring) + Security (audits) + Trader (markets) + Freelancer (client work)
- All 24/7, two Claude Max subscriptions, automated monitoring, zero unplanned downtime

## Install

```bash
clawhub install multi-agent-architecture
```

## Need a Multi-Agent Setup?

Building this from scratch takes 2-3 days. Most people underestimate: workspace isolation, rate limit balancing, cross-agent memory, monitoring, backup automation.

📩 **Telegram: @Aleksander_on** — full setup, architecture consulting, ongoing support.

## License

MIT
