# 🧠 LightRAG Knowledge Base — Shared Brain for Your OpenClaw Agents

Give all your agents a common memory. Any agent can query what other agents learned. Cross-agent knowledge with entity relationships, not just text search.

## Why Use This

| Without shared knowledge | With LightRAG |
|---|---|
| Each agent knows only its own files | **Any agent** queries all agents' knowledge |
| Text similarity search only | **Entity graph** — finds connections between facts |
| "What did ops agent find last week?" → no answer | Instant cross-agent answer with context |
| Knowledge dies with the session | **Persistent graph** — entities and relationships survive forever |
| Adding context = burning tokens | **~$0.003/query** — 15x cheaper than stuffing context |

## What's Inside

- 🐳 **Docker deployment** — one container, 5-minute setup, ~200MB RAM
- 📝 **Query + Insert scripts** — ready to symlink to all agent workspaces
- 🔗 **Three-tier memory architecture** — Hot (MEMORY.md) → Warm (memory_search) → Deep (LightRAG)
- 📊 **WebUI** — visual graph explorer for entities and relationships
- ⚡ **Auto-indexing** — cron script to index new daily logs automatically
- 💰 **Cost optimization guide** — which LLM model to use (hint: NOT your Claude subscription)
- 🔒 **Security rules** — what to never index, port binding, auth

## The Three-Tier Memory Stack

```
Hot:  MEMORY.md        → in context, free, instant, one agent
Warm: memory_search    → vector search, free, instant, one agent
Deep: LightRAG         → knowledge graph, $0.003/query, 3-8s, ALL agents
```

Use all three. Each layer has its job.

## Built From Experience

Deployed on a production system with **5 agents, 72 documents, 3,449 entities, 2,442 relationships**. Running 24/7 for weeks with ~$3/month total LightRAG cost.

## Install

```bash
clawhub install lightrag-knowledge-base
```

## Need Help Setting This Up?

LightRAG + multi-agent + ProxyAPI + auto-indexing + monitoring takes about a day to configure properly. Docker networking, API key management, embedding dimensions, chunking strategy — lots of details to get right.

📩 **Telegram: @Aleksander_on** — full deployment, integration with your agents, ongoing support.

## License

MIT
