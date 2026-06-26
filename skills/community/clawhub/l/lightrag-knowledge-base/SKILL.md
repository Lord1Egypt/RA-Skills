---
name: lightrag-knowledge-base
description: Deploy LightRAG as a shared knowledge graph for OpenClaw agents. Gives all your agents a common brain — query cross-agent knowledge, auto-index daily logs, and search entity relationships. Use when agents need to share knowledge or when memory_search is not enough.
version: 1.0.0
author: mosoonpi-ai
license: MIT
tags: lightrag, knowledge-graph, memory, rag, multi-agent, docker, embeddings
---

# LightRAG Knowledge Base — Shared Brain for Your Agents

## What You Get

- 🧠 **Cross-agent knowledge** — any agent can query what other agents learned
- 🔍 **Entity + relationship search** — not just text, but connections between facts
- 💰 **~$0.003 per query** — 15x cheaper than sending context to Claude
- 📊 **Visual knowledge graph** — built-in WebUI to explore entities and connections
- 🐳 **One Docker container** — 5-minute deploy, ~200MB RAM idle
- 📝 **Auto-indexing** — new daily logs added to the graph automatically

## Why Not Just memory_search?

| memory_search | LightRAG |
|---|---|
| Searches **one agent's** files | Searches **all agents'** knowledge |
| Text similarity only | **Entities + relationships** (who → did what → when) |
| No connections between facts | Builds a **graph** — finds hidden links |
| Free, instant | ~$0.003/query, 3-8 seconds |
| Great for recent context | Great for **cross-agent** and **historical** knowledge |

**Use both.** memory_search for quick lookups. LightRAG for deep cross-agent queries.

## Architecture

```
┌──────────┐  ┌──────────┐  ┌──────────┐
│  Agent 1 │  │  Agent 2 │  │  Agent N │
│  (main)  │  │  (ops)   │  │ (trade)  │
└────┬─────┘  └────┬─────┘  └────┬─────┘
     │              │              │
     ▼              ▼              ▼
   scripts/lightrag_query.py (symlinked)
   scripts/lightrag_insert.py (symlinked)
     │
     ▼
┌─────────────────────────────────┐
│     LightRAG Docker Container    │
│  API: http://127.0.0.1:9621     │
│  WebUI: http://127.0.0.1:9621   │
│  Storage: graph + embeddings     │
└─────────────────────────────────┘
     │
     ▼
  ProxyAPI / OpenAI API
  (LLM + Embeddings)
```

## Prerequisites

- Docker + Docker Compose
- OpenAI-compatible API for LLM and embeddings (ProxyAPI, OpenAI, local LLM)
- Python 3.10+ with `requests` (for query/insert scripts)
- ~500MB disk for initial graph, grows with data

## Step 1: Deploy LightRAG

Create `docker/lightrag/docker-compose.yml`:

```yaml
services:
  lightrag:
    image: lightrag/lightrag:latest
    container_name: lightrag
    restart: unless-stopped
    ports:
      - "127.0.0.1:9621:9621"
    volumes:
      - ./data:/app/data
    env_file:
      - .env
```

Create `docker/lightrag/.env`:

```bash
# LLM (for graph construction and queries)
LLM_BINDING=openai
LLM_MODEL=gpt-4.1-nano
LLM_BINDING_HOST=https://api.openai.com/v1
LLM_BINDING_API_KEY=sk-your-api-key

# Embeddings (for vector search)
EMBEDDING_BINDING=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_DIM=1536
EMBEDDING_BINDING_HOST=https://api.openai.com/v1
EMBEDDING_BINDING_API_KEY=sk-your-api-key

# Performance
MAX_ASYNC=4
MAX_PARALLEL_INSERT=2
CHUNK_SIZE=1200
CHUNK_OVERLAP_SIZE=100
TOP_K=40
MAX_TOTAL_TOKENS=30000
ENABLE_LLM_CACHE=true

# Auth
LIGHTRAG_API_KEY=your-secure-api-key
JWT_SECRET_KEY=your-jwt-secret
```

Deploy:
```bash
cd docker/lightrag
docker compose up -d
# Check it's running
curl -s http://127.0.0.1:9621/health
```

## Step 2: Create Query/Insert Scripts

### scripts/lightrag_query.py

```python
#!/usr/bin/env python3
"""Query LightRAG knowledge graph."""
import sys, json, requests

API = "http://127.0.0.1:9621"
KEY = "your-secure-api-key"

def query(text, mode="mix"):
    r = requests.post(f"{API}/query",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"query": text, "mode": mode, "only_need_context": False},
        timeout=30)
    r.raise_for_status()
    data = r.json()
    print(data.get("response", data))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lightrag_query.py 'question' [mode]")
        print("Modes: mix (default), hybrid, local, global, naive")
        sys.exit(1)
    query(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "mix")
```

### scripts/lightrag_insert.py

```python
#!/usr/bin/env python3
"""Insert text into LightRAG knowledge graph."""
import sys, requests

API = "http://127.0.0.1:9621"
KEY = "your-secure-api-key"

def insert(text, description="manual insert"):
    r = requests.post(f"{API}/documents/text",
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        json={"text": text, "description": description},
        timeout=120)
    r.raise_for_status()
    print(f"OK: {r.json()}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python lightrag_insert.py 'text to index' ['description']")
        sys.exit(1)
    insert(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "manual insert")
```

## Step 3: Symlink Scripts to All Agents

```bash
# Create scripts in main workspace
cp lightrag_query.py ~/.openclaw/workspace/scripts/
cp lightrag_insert.py ~/.openclaw/workspace/scripts/

# Symlink to every agent workspace
for ws in workspace-ops workspace-security workspace-trade workspace-freelance; do
    ln -sf ~/.openclaw/workspace/scripts/lightrag_query.py \
           ~/.openclaw/$ws/scripts/lightrag_query.py
    ln -sf ~/.openclaw/workspace/scripts/lightrag_insert.py \
           ~/.openclaw/$ws/scripts/lightrag_insert.py
done
```

## Step 4: Load Initial Data

Start with your agent profiles and key documents:

```bash
# Load agent descriptions
for file in SOUL.md USER.md; do
    python3 scripts/lightrag_insert.py "$(cat ~/.openclaw/workspace/$file)" "$file"
done

# Load daily logs (bulk)
for f in ~/.openclaw/workspace/memory/*.md; do
    python3 scripts/lightrag_insert.py "$(cat $f)" "$(basename $f)"
    sleep 2  # avoid rate limits
done

# Load from other workspaces
for ws in workspace-ops workspace-security workspace-trade; do
    for f in ~/.openclaw/$ws/memory/*.md; do
        python3 scripts/lightrag_insert.py "$(cat $f)" "$ws/$(basename $f)"
        sleep 2
    done
done
```

## Step 5: Add to TOOLS.md

Add to each agent's TOOLS.md:

```markdown
### LightRAG — Knowledge Graph

Query the shared knowledge graph:
\`\`\`bash
python3 scripts/lightrag_query.py "question" [mode]
\`\`\`
Modes: mix (default), hybrid, local, global, naive

Insert new knowledge:
\`\`\`bash
python3 scripts/lightrag_insert.py "text" "description"
\`\`\`

When to use: cross-agent knowledge, historical decisions, entity relationships.
When NOT needed: today's context (use memory_search instead).
\`\`\`
```

## Step 6: Auto-Index New Daily Logs (Optional)

Create a cron job to index new daily logs automatically:

```bash
#!/bin/bash
# index_new_logs.sh — run daily via cron
API="http://127.0.0.1:9621"
KEY="your-secure-api-key"
TODAY=$(date +%Y-%m-%d)

for ws in workspace workspace-ops workspace-security workspace-trade workspace-freelance; do
    FILE="$HOME/.openclaw/$ws/memory/${TODAY}.md"
    if [ -f "$FILE" ]; then
        TEXT=$(cat "$FILE")
        curl -s -X POST "$API/documents/text" \
            -H "Authorization: Bearer $KEY" \
            -H "Content-Type: application/json" \
            -d "{\"text\": $(echo "$TEXT" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read()))'), \"description\": \"$ws/$TODAY\"}" \
            > /dev/null
    fi
done
```

## Three-Tier Memory Architecture

Use all three layers together:

| Layer | Tool | Speed | Cost | Scope | Best For |
|-------|------|-------|------|-------|----------|
| **Hot** | MEMORY.md | Instant | Free | Current agent | Active context, rules |
| **Warm** | memory_search | Instant | Free | Current agent | Recent logs, quick lookup |
| **Deep** | LightRAG | 3-8 sec | ~$0.003 | **All agents** | Cross-agent, historical, relationships |

**Decision flow:**
1. Need today's context? → MEMORY.md (already in context)
2. Need recent info from this agent? → memory_search
3. Need cross-agent knowledge or old decisions? → LightRAG

## LLM Cost Optimization

| LLM Model | Cost per query | Quality | Recommendation |
|-----------|---------------|---------|----------------|
| gpt-4.1-nano | ~$0.003 | Good | ✅ Best for LightRAG |
| gpt-4o-mini | ~$0.005 | Good | OK alternative |
| gpt-4o | ~$0.03 | Great | Overkill for indexing |
| claude-sonnet | ~$0.01 | Great | Uses your Claude quota! |

**Key rule:** Use a cheap OpenAI-compatible model for LightRAG. Do NOT use your Claude subscription — LightRAG queries would eat into your agent's rate limits.

## Security Notes

- ⚠️ **Never index API keys, tokens, or passwords** into the graph
- Bind port to `127.0.0.1` only (never `0.0.0.0`)
- Use a strong API key for LightRAG auth
- WebUI credentials should differ from other services

## Monitoring

Check graph health:
```bash
curl -s http://127.0.0.1:9621/health
curl -s -H "Authorization: Bearer YOUR_KEY" http://127.0.0.1:9621/graphs/stats
```

Add to self-healing script:
```bash
if ! curl -sf http://127.0.0.1:9621/health > /dev/null; then
    cd ~/docker/lightrag && docker compose restart
fi
```

## WebUI

Access at `http://127.0.0.1:9621` — explore entities, relationships, search visually. Useful for understanding what your agents collectively know.
