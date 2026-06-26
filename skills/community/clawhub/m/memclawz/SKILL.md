---
name: memclawz
description: AI agent fleet memory system — Qdrant + Mem0 + Neo4j/Graphiti. Composite scoring, compaction engine, temporal knowledge graph, multi-claw federation, sleep-time reflection, routing engine, MCP server. Use when you need to install, configure, manage, search, route, compact, or upgrade the agent memory system.
metadata:
  openclaw:
    requires:
      bins: ["python3", "pip3"]
---

# MemClawz v6 🧠

Fleet memory system for OpenClaw agents with composite scoring, compaction engine, Graphiti temporal knowledge graph, multi-claw federation, and sleep-time reflection.

## What's New in v6
- **Composite Scoring** — Weighted blend of semantic similarity + recency decay + importance + access frequency
- **Compaction Engine** — Session/daily/weekly compaction with LLM extraction
- **Graphiti Integration** — Neo4j temporal knowledge graph for entity relationships and contradiction detection
- **Multi-Claw Federation** — HTTP push/pull protocol for sharing memories across fleet
- **Sleep-Time Reflection** — LLM-driven pattern detection, insight generation, and MEMORY.md update proposals
- **Enhanced MCP Server** — New tools: compact_session, reflect, memory_stats

## Quick Install

### Prerequisites
- Python 3.10+
- Qdrant running (Docker or binary)
- Neo4j running (for Graphiti; optional but recommended)
- OpenAI API key (for embeddings)
- Anthropic API key (for classification)

### Install Qdrant
```bash
# Docker (preferred)
docker run -d --name qdrant -p 6333:6333 -p 6334:6334 \
  -v ~/.openclaw/qdrant-storage:/qdrant/storage \
  --restart unless-stopped qdrant/qdrant

# Or binary (no Docker)
curl -sL https://github.com/qdrant/qdrant/releases/latest/download/qdrant-x86_64-unknown-linux-musl.tar.gz | tar xz
./qdrant --storage-path ~/.openclaw/qdrant-storage &
```

### Install MemClawz
```bash
cd ~
git clone https://github.com/yoniassia/memclawz.git
cd memclawz
pip3 install -r requirements.txt
```

### Configure
```bash
cat > ~/memclawz/.env << EOF
OPENAI_API_KEY=<your-key>
ANTHROPIC_API_KEY=<your-key>
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION=yoniclaw_memories
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=
GRAPHITI_ENABLED=true
FEDERATION_ENABLED=true
FEDERATION_ROLE=master
WORKSPACE_DIR=/home/yoniclaw/.openclaw/workspace
EOF
```

### Deploy Services
```bash
cp ~/memclawz/systemd/*.service ~/.config/systemd/user/
systemctl --user daemon-reload
systemctl --user enable --now neo4j memclawz-api memclawz-watcher memclawz-cron
```

### Verify
```bash
curl http://localhost:3500/health
# {"status":"ok","version":"6.0.0","qdrant":"ok","neo4j":"ok","graphiti":"ok","federation":"ok",...}
```

## API Reference

### Core (v5 compatible)
```bash
# Search with composite scoring
curl "http://localhost:3500/api/v1/search?q=eToro+SuperApp&limit=10"
# Use raw cosine: &use_composite=false

# Add memory (feeds both Qdrant AND Graphiti)
curl -X POST "http://localhost:3500/api/v1/add" \
  -H "Content-Type: application/json" \
  -d '{"content":"BTC hit 100K on March 1","agent_id":"tradeclaw","memory_type":"event"}'

# List by agent
curl "http://localhost:3500/api/v1/memories?agent_id=tradeclaw&limit=20"

# Stats / Agents
curl http://localhost:3500/api/v1/stats
curl http://localhost:3500/api/v1/agents
```

### Graph Search (v6)
```bash
# Search temporal knowledge graph
curl "http://localhost:3500/api/v1/graph/search?q=eToro+deployment"

# Get entity relationships
curl "http://localhost:3500/api/v1/graph/entity/YoniClaw"
```

### Compaction (v6)
```bash
# Trigger session compaction
curl -X POST "http://localhost:3500/api/v1/compact/session" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"main:whatsapp:direct:+35794329522","agent_id":"main"}'

# Generate daily digest
curl -X POST "http://localhost:3500/api/v1/compact/daily"

# Run weekly merge
curl -X POST "http://localhost:3500/api/v1/compact/weekly"

# Check compaction status
curl "http://localhost:3500/api/v1/compact/status"
```

### Reflection (v6)
```bash
# Trigger reflection (analyzes last 24h of memories)
curl -X POST "http://localhost:3500/api/v1/reflect" \
  -H "Content-Type: application/json" \
  -d '{"hours":24,"max_memories":100}'
```

### Federation (v6)
```bash
# Register a remote node
curl -X POST "http://localhost:3500/api/v1/federation/register" \
  -H "Content-Type: application/json" \
  -d '{"node_id":"clawdet","node_url":"http://188.34.197.212:3500","node_key":"shared-secret"}'

# Push memories from remote
curl -X POST "http://localhost:3500/api/v1/federation/push" \
  -H "Content-Type: application/json" \
  -d '{"node_id":"clawdet","node_key":"shared-secret","memories":[{"content":"...","type":"fact","agent":"main"}]}'

# Pull memories to remote
curl -X POST "http://localhost:3500/api/v1/federation/pull" \
  -H "Content-Type: application/json" \
  -d '{"node_id":"clawdet","node_key":"shared-secret","since":"2026-03-13T00:00:00Z","limit":100}'

# Federation status
curl "http://localhost:3500/api/v1/federation/status"
```

## Composite Scoring
```
score = (w_semantic × similarity + w_recency × decay + w_importance × weight) × access_boost
```
- **Semantic**: 50% weight (cosine from Qdrant)
- **Recency**: 30% weight (exponential, 90-day half-life)
- **Importance**: 20% weight (type-based: decisions > preferences > facts > events)
- **Access boost**: up to 1.5× for frequently accessed memories
- **Persistent types** (decisions, preferences, relationships): 40% recency floor

## Memory Types
- **fact** — factual statement about a person, project, system
- **decision** — a choice that was made
- **preference** — user preference or style choice
- **procedure** — steps to accomplish something
- **relationship** — info about a person or org relationship
- **event** — something that happened at a specific time
- **insight** — learned lesson, pattern, or strategic insight

## Canonical Memory Order
1. **Local canonical files first** — `MEMORY.md`, `memory/*.md`, `memory/people/*`, `memory/sessions/*`, `knowledge/*.md`
2. **MemClawz second** — Qdrant + Mem0 + Neo4j/Graphiti + API + MCP
3. **LCM/transcripts third** — raw capture and extraction layer

## Services
| Service | Port | Description |
|---------|------|-------------|
| `memclawz-api` | 3500 | REST API (v6) |
| `memclawz-watcher` | — | LCM auto-extract (+ Graphiti feed) |
| `memclawz-cron` | — | Compaction scheduler (30-min cycle) |
| `memclawz-mcp` | stdio | MCP server (v6 tools) |
| Neo4j | 7474/7687 | Graph database (Graphiti) |
| Qdrant | 6333 | Vector database |

## MCP Integration
```json
{
  "mcpServers": {
    "memclawz": {
      "command": "python3",
      "args": ["/path/to/memclawz/memclawz/mcp_server.py"],
      "env": {"OPENAI_API_KEY": "<key>", "ANTHROPIC_API_KEY": "<key>"}
    }
  }
}
```

MCP tools: search_memory, add_memory, get_agent_memories, compact_session, reflect, memory_stats

## Architecture
```
LCM → Watcher → Classify → Mem0 → Qdrant + Graphiti/Neo4j
                                    ↑↓            ↑↓
Fleet Agents ←→ REST API :3500  ←→ Qdrant    Neo4j
MCP Clients  ←→ MCP Server     ←→ Qdrant
Remote Claws ←→ Federation API ←→ Qdrant
Cron         →  Compactor/Reflection → Files + Qdrant + Graphiti
```
