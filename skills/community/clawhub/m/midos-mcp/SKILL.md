---
name: midos-mcp
version: 1.0.0
description: MidOS — The MCP Knowledge OS. 134 tools for knowledge management, multi-agent orchestration, search, planning, and memory. 670K+ vectors, 46K+ chunks, EUREKA synthesis.
homepage: https://midos.dev
metadata: {"clawdbot":{"emoji":"🧠","category":"knowledge","api_base":"https://midos.dev/mcp"}}
---

# MidOS MCP — The Knowledge Operating System

MidOS is a knowledge middleware layer for AI agents. It gives you access to a continuously growing intelligence base: 670K+ vectors, 46K+ knowledge chunks, 451 EUREKA insights, and 134 MCP tools for search, memory, planning, and orchestration.

**Think of MidOS as your agent's long-term brain.**

## What You Get

| Cluster | Tools | What it does |
|---------|-------|--------------|
| 🔍 Search | `smart_search`, `semantic_search`, `hybrid_search` | Search 670K vectors — keyword, semantic, or hybrid |
| 🧠 Memory | `mem_save`, `mem_search`, `mem_context`, `where_was_i` | Persistent cross-session memory (91.67% hit@5) |
| 📋 Planning | `create_plan`, `update_plan_task`, `get_active_plans` | Multi-step task tracking with status checkpoints |
| 📚 Knowledge | `knowledge_preflight`, `quality_gate`, `knowledge_edit` | Create, validate, and improve knowledge chunks |
| ⚙️ Execution | `maker_run_bash`, `maker_read_file`, `maker_write_file` | File ops, shell commands, git, HTTP fetch |
| 🩺 Health | `system_health_check`, `hive_status`, `pulse_read` | Monitor knowledge base and pipeline health |
| 🔔 Notify | `maker_notify_discord`, `maker_notify_webhook` | Notifications to Discord, webhooks, Slack |

## Quick Start

### Connect via MCP (JSON-RPC 2.0)

```bash
# Health check
curl https://midos.dev/mcp/health

# Initialize session
curl -X POST https://midos.dev/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"my-agent","version":"1.0"}}}'
```

### Search the knowledge base

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "smart_search",
    "arguments": {
      "query": "your topic here",
      "mode": "hybrid",
      "limit": 5
    }
  }
}
```

### Save a memory

```json
{
  "method": "tools/call",
  "params": {
    "name": "mem_save",
    "arguments": {
      "content": "User prefers concise responses with code examples",
      "type": "preference",
      "project": "my-project"
    }
  }
}
```

### Create a plan

```json
{
  "method": "tools/call",
  "params": {
    "name": "create_plan",
    "arguments": {
      "goal": "Build a new feature",
      "tasks": "1. Research existing patterns\n2. Design API\n3. Implement\n4. Test"
    }
  }
}
```

## Knowledge Base Stats (live)

- **46,283** knowledge chunks across AI, engineering, research, strategy
- **670K+** vector embeddings (Gemini gemini-embedding-001, 3072-d)
- **451** EUREKA synthesized insights
- **139** SOTA benchmarks
- **φ = 0.932** knowledge coherence score

## Key Features

### 🔍 Hybrid Search (BM25 + Semantic)
Combines keyword precision with semantic understanding. Outperforms vector-only by 9.3% on relevance benchmarks.

### 🧠 Persistent Memory
`mem_save` / `mem_search` backed by LanceDB. Memories survive across sessions. 91.67% hit@5 on recall benchmarks.

### 📋 Smart Planning
Create structured multi-step plans, track progress, checkpoint completions. Survives context resets.

### ⚡ Fast Preflight
`knowledge_preflight` checks for duplicate knowledge in 19ms (title cache, 48K+ chunks). Prevents knowledge bloat.

### 🏗️ Quality Gate
`quality_gate` scores content on 7 dimensions before adding to the knowledge base. Keeps signal-to-noise high.

## Heartbeat Integration

Add to your agent's periodic check-in:

```markdown
## MidOS (every session start)
1. Call where_was_i(client="your-agent-name") to resume context
2. Call mem_context(scope="recent") to load recent memory
3. Before creating knowledge: knowledge_preflight(topic)
4. After important decisions: mem_save(content, type="decision")
```

## Self-Hosted Option

MidOS is open source. Run your own instance:

```bash
git clone https://github.com/MidOSresearch/midos-core
cd midos-core
python -m modules.mcp_server.midos_mcp --http --port 3100
```

Full docs: https://midos.dev/docs
GitHub: https://github.com/MidOSresearch/midos-core
