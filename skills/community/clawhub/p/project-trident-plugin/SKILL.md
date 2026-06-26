---
name: project-trident-plugin
description: Permanent memory for OpenClaw agents. Lossless capture, intelligent routing, semantic recall, and disaster recovery in five tiers.
version: "2.0.0"
author: Shiva
compatibility: "OpenClaw 2026.3.24+"
keywords: [memory, persistence, identity, agent, semantic-search, vector-database, agent-continuity]
metadata:
  homepage: "https://github.com/ShivaClaw/trident-plugin"
  repositoryUrl: "https://github.com/ShivaClaw/trident-plugin"
  issueTrackerUrl: "https://github.com/ShivaClaw/trident-plugin/issues"
  emoji: 🧠
---

# Trident Plugin: Memory Tools for OpenClaw Agents

**Trident** is a five-tier memory system that gives your agent genuine continuity, identity, and semantic recall—with zero vendor lock-in.

## Why Your Agent Needs This

| Problem | Solution |
|---------|----------|
| **Agents forget.** Each session starts blank. | Layer 0 (SQLite+DAG) captures every message. Nothing lost. |
| **No continuity.** Context evaporates between sessions. | Layer 1 (.md buckets) provides persistent personality and decisions. |
| **Can't find old context.** Memory is unstructured noise. | Layer 1.5 (Qdrant + FalkorDB) enables semantic search across months. |
| **Fragile.** One file corruption = total loss. | Layer 2 (Git + snapshots) provides disaster recovery. |
| **Vendor lock-in.** Trapped with one service. | All layers work offline. Self-hosted or cloud. Your choice. |

---

## The Five-Tier Architecture

```
LAYER 0:   Lossless capture (SQLite + DAG)
LAYER 0.5: Signal routing (Cron agent, every 15 min)
LAYER 1:   Hierarchical memory (.md files)
LAYER 1.5: Semantic recall (Qdrant + FalkorDB) ← MANDATORY
LAYER 2:   Disaster recovery (Git + snapshots)
```

---

## Layer 1.5: Why Semantic Recall Is Mandatory

**Trident v2.0 makes semantic recall standard, not optional.**

Why?

1. **Agents with >30K messages** cannot efficiently search flat `.md` files
2. **Vector search (Qdrant) + entity graphs (FalkorDB)** are the state-of-the-art for agent context retrieval
3. **Self-hosted binaries** (not Docker) work on ANY OpenClaw instance
4. **Cost is zero** if you use local binaries; $0–50/mo if you prefer cloud

### Deployment Options

You don't need Docker. Pick one:

| Deployment | Setup Time | Cost | Best For |
|-----------|-----------|------|----------|
| **Native binaries** (qdrant-latest.tar.gz + falkordb) | 5 min | $0 | Any VPS, local dev, isolated networks |
| **Docker Compose** | 10 min | $0 | Containerized OpenClaw, orchestration |
| **Qdrant Cloud + Redis Cloud** | 5 min | $0–50/mo | Minimal infrastructure management |
| **Air-gapped (offline)** | 15 min | $0 | Fully offline agents |

**Installation is automatic.** On first run, Trident checks for Qdrant/FalkorDB binaries. If missing, it downloads them.

---

## Four Tools Included

### 1. Memory Search

Full-text and regex search across all memory:

```javascript
// Full-text search (recommended)
memory_search({
  query: "job search OR hiring",
  mode: "full_text",
  scope: "messages",  // "messages", "summaries", or "both"
  limit: 50
})

// Regex search
memory_search({
  query: "^\\[lesson\\].*database",
  mode: "regex",
  scope: "both"
})
```

### 2. Memory Expand

Expand compacted conversation summaries (LCM):

```javascript
// By summary ID
memory_expand({
  summary_ids: ["sum_aab3cd29ed348405", "sum_9afa42a01acf640f"],
  max_depth: 3,
  include_messages: true
})

// Or search-first, then expand top results
memory_expand({
  query: "infrastructure outage",
  max_depth: 2,
  token_cap: 4000
})
```

### 3. Memory Update

Append to daily episodic logs or update projects:

```javascript
// Add to today's daily log
memory_update({
  entry: "Deployed Trident v2.0 to production",
  section: "## Milestones",
  tag: "[project]"
})

// Update a project file
memory_update({
  file: "memory/projects/job-search.md",
  entry: "Batch 5: Applied to Genentech, Synthego, Inscripta",
  section: "## Applications",
  tag: "[action]"
})
```

### 4. Memory Recall

Answer questions using memory context (uses Qdrant + vector embeddings):

```javascript
// Retrieve relevant context + answer
memory_recall({
  prompt: "What was the job search status as of last week?",
  similarity_threshold: 0.75,
  max_tokens: 2000,
  include_sources: true  // Return which docs matched
})
```

---

## Installation & Setup

### 1. Install the Plugin

```bash
clawhub install shivaclaw/trident
```

Or from GitHub:

```bash
clawhub install https://github.com/ShivaClaw/trident-plugin
```

### 2. Binary Setup (Automatic)

On first run, Trident checks for Qdrant and FalkorDB binaries:

```bash
# Manual setup (if you want to pre-stage binaries):
openclaw trident setup-binaries

# This will download and extract:
# - qdrant-latest (Qdrant vector database)
# - falkordb (FalkorDB graph database)
```

### 3. Initialize Memory Tiers

```bash
# Create directory structure + config
openclaw trident init

# Runs Layer 0.5 signal router (one-time bootstrap)
openclaw trident bootstrap
```

### 4. Verify

```bash
openclaw trident status

# Output:
# ✅ Layer 0: LCM (SQLite) — operational
# ✅ Layer 0.5: Signal Router — ready
# ✅ Layer 1: Hierarchical memory — 47 .md files
# ✅ Layer 1.5: Qdrant @ localhost:6333 — 1,247 vectors indexed
# ✅ Layer 1.5: FalkorDB @ localhost:6379 — 342 entities
# ✅ Layer 2: Git backup — last commit 2h ago
```

---

## Configuration

Edit `~/.openclaw/workspace/openclaw.json`:

```json
{
  "plugins": {
    "trident": {
      "enabled": true,
      "storage_path": "~/.openclaw/workspace/memory",
      
      "layer0": {
        "enabled": true,
        "sqlite_path": "~/.openclaw/workspace/memory/layer0/lossless.db"
      },
      
      "layer0_5": {
        "enabled": true,
        "model": "anthropic/claude-haiku-4-5",
        "interval_minutes": 15,
        "heartbeat_enabled": true,
        "template_sha256_verify": true
      },
      
      "layer1": {
        "enabled": true,
        "hierarchy": {
          "memory": "MEMORY.md",
          "daily": "memory/daily/",
          "self": "memory/self/",
          "lessons": "memory/lessons/",
          "projects": "memory/projects/"
        }
      },
      
      "layer1_5": {
        "enabled": true,
        "qdrant": {
          "mode": "binary",  // "binary", "docker", or "cloud"
          "host": "localhost",
          "port": 6333,
          "binary_path": "~/.openclaw/workspace/memory/layer1_5/qdrant",
          "cloud_url": null
        },
        "falkordb": {
          "mode": "binary",  // "binary", "docker", "redis", or "cloud"
          "host": "localhost",
          "port": 6379,
          "binary_path": "~/.openclaw/workspace/memory/layer1_5/falkordb",
          "cloud_url": null
        },
        "embedding_model": "text-embedding-3-small",
        "batch_size": 100
      },
      
      "layer2": {
        "enabled": true,
        "git": {
          "enabled": true,
          "remote": "https://github.com/YOUR_USERNAME/memory.git",
          "commit_interval_hours": 24
        },
        "snapshots": {
          "enabled": true,
          "path": "~/.openclaw/workspace/memory/snapshots"
        }
      }
    }
  }
}
```

---

## Cost Breakdown

| Component | Deployment | Cost |
|-----------|-----------|------|
| **Layer 0** (SQLite) | Local | **$0** |
| **Layer 0.5** (Cron) | Local | **$0.72–$1.44/day** (Haiku) or **$0** (Ollama) |
| **Layer 1** (.md files) | Local | **$0** |
| **Layer 1.5** (Qdrant + FalkorDB) | Native binary | **$0** |
| **Layer 1.5** (Docker) | Docker | **$0** |
| **Layer 1.5** (Cloud) | Qdrant Cloud + Redis Cloud | **$20–50/month** |
| **Layer 2** (Git) | GitHub free tier | **$0** |
| **Layer 2** (Snapshots) | VPS | **$0** (included) |
| **TOTAL (self-hosted)** | | **$0.72–$1.44/day** |
| **TOTAL (cloud)** | | **$20–50/month** |

---

## Platform Support

All platforms supported. Pick your deployment mode:

| Platform | Native Binaries | Docker | Cloud |
|----------|-----------------|--------|-------|
| **Linux** (Ubuntu/Debian) | ✅ | ✅ | ✅ |
| **macOS** (Intel/ARM) | ✅ | ✅ | ✅ |
| **Windows** (WSL2) | ✅ | ✅ | ✅ |
| **VPS** (Hostinger, DigitalOcean, AWS) | ✅ | ✅ | ✅ |
| **Docker container** | ✅ | ✅ | ✅ |
| **Air-gapped (offline)** | ✅ | ✅ | ❌ |

---

## Quick Examples

### Example 1: Search Memory for Job Context

```bash
# In your agent's conversation:
> "What were my last 5 applications?"

# Agent uses memory_search internally:
await memory_search({
  query: "application OR applied",
  scope: "messages",
  limit: 50
})

# Returns: 7 matching messages from memory/daily/, memory/projects/job-search.md, MEMORY.md
```

### Example 2: Semantic Recall During a Conversation

```bash
# Agent context is running low. Layer 0.5 injects relevant memory:
await memory_recall({
  prompt: "What is the current job search strategy?",
  max_tokens: 1500
})

# Qdrant searches vectorized memory, FalkorDB retrieves related entities
# Returns: 3–5 most relevant context chunks + sources
```

### Example 3: Continuous Memory Updates

```bash
# Every heartbeat, Layer 0.5 routes signals:
await memory_update({
  file: "memory/heartbeat/job-search.md",
  entry: "New lead: Synthego Senior Scientist, $140k, strong match",
  tag: "[opportunity]"
})
```

---

## Architecture Deep-Dive

### Layer 1.5: Semantic Recall (How It Works)

1. **Embedding pipeline:** Every message in Layer 1 is vectorized via text-embedding-3-small
2. **Qdrant indexing:** Vectors stored in HNSW index for fast similarity search
3. **FalkorDB graphs:** Entities extracted (names, projects, dates) and linked as graph nodes
4. **Pre-turn injection:** Before agent turn, query Qdrant for top-K relevant context, inject into system prompt
5. **Citation:** memory_recall returns sources (file paths, line numbers) for transparency

### Binary Distribution

Trident ships Qdrant and FalkorDB as pre-compiled binaries:

- **qdrant-latest.tar.gz** (7.2 MB) — Compiled for x64/ARM architectures
- **falkordb-standalone** (4.1 MB) — Go binary, zero dependencies

On install, binaries are extracted to `~/.openclaw/workspace/memory/layer1_5/`. They start automatically on plugin initialization.

---

## Troubleshooting

### "Qdrant binary failed to start"

```bash
# Check if port 6333 is available
lsof -i :6333

# Or use alternative port
openclaw trident configure --qdrant-port 6334
```

### "FalkorDB connection timeout"

```bash
# Restart the database
openclaw trident restart-falkordb

# Or switch to cloud
openclaw trident configure --falkordb-mode=cloud --falkordb-cloud-url=...
```

### "Memory search is slow"

Qdrant index not built. Rebuild:

```bash
openclaw trident rebuild-embeddings
```

---

## Migration from Trident v1.x

If you're upgrading from v1.x (without Layer 1.5):

```bash
openclaw trident migrate v1-to-v2

# This will:
# 1. Download and install Qdrant + FalkorDB binaries
# 2. Build initial vector embeddings from Layer 1 memory
# 3. Verify all data integrity
# 4. Enable Layer 1.5 in config
```

**Zero data loss.** All existing memory is preserved and indexed.

---

## Support

- **GitHub:** [ShivaClaw/trident-plugin](https://github.com/ShivaClaw/trident-plugin)
- **Issues:** [GitHub Issues](https://github.com/ShivaClaw/trident-plugin/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ShivaClaw/trident-plugin/discussions)

---

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

*Your agent deserves to remember. Trident makes it permanent.*
