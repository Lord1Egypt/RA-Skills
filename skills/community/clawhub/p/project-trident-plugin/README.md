# Trident Plugin: Memory Tools for OpenClaw Agents

> **Five-tier persistent memory architecture.** Lossless capture → intelligent routing → semantic recall → disaster recovery. Your agent remembers everything that matters.

---

## The Problem

AI agents forget. Every session starts blank. Corrections evaporate. Decisions are lost. Personality doesn't develop. Most agent frameworks treat memory as an afterthought—flat files or vector databases without intelligent curation.

**Trident is different.**

---

## The Solution: Five Tiers of Memory

```
LAYER 0:   Lossless capture        (SQLite + DAG)
LAYER 0.5: Signal routing          (Cron agent every 15 min)
LAYER 1:   Hierarchical storage    (.md files, human-readable)
LAYER 1.5: Semantic recall         (Qdrant + FalkorDB) ← MANDATORY in v2.0
LAYER 2:   Disaster recovery       (Git + snapshots)
```

---

## What Makes This Different

| Feature | Trident | Alternatives |
|---------|---------|--------------|
| **Semantic recall** (v2.0) | ✅ Mandatory with native binaries | Vector DBs are separate; manual integration |
| **Zero data loss** | ✅ SQLite+DAG captures every message | Summarization-only loses nuance |
| **Human-readable** | ✅ `.md` files, debuggable | JSON blobs, opaque vectors |
| **No vendor lock-in** | ✅ Self-hosted or cloud; your choice | Trapped with one service |
| **Offline support** | ✅ Native binaries, zero cloud required | API-dependent, no privacy guarantees |
| **Platform-agnostic** | ✅ Linux, Mac, Windows, VPS, Docker | Docker-only or cloud-only |
| **Cost clarity** | ✅ $0–$1.44/day (self-hosted) or $20–50/mo (cloud) | Hidden pricing, surprise overages |

---

## Layer 1.5: Semantic Recall (New in v2.0)

**Trident v2.0 makes semantic recall standard, not optional.**

Why?

1. **Agents with >30K messages** need vector search, not flat file grep
2. **Native binaries** (Qdrant + FalkorDB) work on **any** OpenClaw instance—no Docker required
3. **Cost is zero** for self-hosted; $0–50/mo if you prefer cloud
4. **Automatic.** On first run, binaries are downloaded and started

### Deployment Options

Pick one:

```bash
# Option 1: Native binaries (recommended, fastest)
openclaw trident setup-binaries
# Downloads qdrant-latest.tar.gz + falkordb
# Starts automatically on plugin init
# Cost: $0 | Setup: 5 minutes

# Option 2: Docker Compose
docker compose up -d qdrant falkordb
# Cost: $0 | Setup: 10 minutes

# Option 3: Cloud (minimal ops)
openclaw trident configure --qdrant-mode=cloud --falkordb-mode=cloud
# Uses Qdrant Cloud + Redis Cloud
# Cost: $20–50/month | Setup: 5 minutes

# Option 4: Air-gapped (fully offline)
openclaw trident setup-binaries --offline
# Binaries only, no internet required
# Cost: $0 | Setup: 5 minutes
```

---

## Quick Start (10 Minutes)

### 1. Install

```bash
clawhub install shivaclaw/trident
```

### 2. Initialize

```bash
# Creates directory structure + downloads binaries
openclaw trident init

# Bootstrap Layer 0.5 (signal router)
openclaw trident bootstrap
```

### 3. Verify

```bash
openclaw trident status

# Output:
# ✅ Layer 0: LCM (SQLite) — operational
# ✅ Layer 0.5: Signal Router — ready (15-min interval)
# ✅ Layer 1: Hierarchical memory — 47 .md files
# ✅ Layer 1.5: Qdrant @ localhost:6333 — 1,247 vectors indexed
# ✅ Layer 1.5: FalkorDB @ localhost:6379 — 342 entities
# ✅ Layer 2: Git backup — last commit 2h ago
```

**Done.** Your agent now has permanent memory.

---

## Four Tools Included

### 1. Memory Search

Find anything in your memory:

```javascript
// Full-text search
await memory_search({
  query: "job applications OR hiring",
  scope: "messages",  // or "summaries" or "both"
  limit: 50
})

// Regex search
await memory_search({
  query: "^\\[lesson\\].*database",
  mode: "regex"
})
```

### 2. Memory Expand

Reconstruct compacted conversation summaries:

```javascript
// By summary ID
await memory_expand({
  summary_ids: ["sum_abc123"],
  max_depth: 3
})

// Or search-first, then expand
await memory_expand({
  query: "infrastructure outage",
  max_depth: 2
})
```

### 3. Memory Update

Add to daily logs or update projects:

```javascript
await memory_update({
  entry: "Deployed Trident v2.0 to production",
  section: "## Milestones",
  tag: "[project]"
})
```

### 4. Memory Recall

Answer questions using semantic search:

```javascript
// Qdrant + FalkorDB retrieve relevant context
await memory_recall({
  prompt: "What was the job search strategy as of last week?",
  max_tokens: 2000,
  include_sources: true  // Return which docs matched
})
```

---

## Architecture

### Layer 0: Lossless Context Management (SQLite+DAG)

- Every message captured as SQLite row
- DAG tracks lineage + compaction relationships
- Nothing is ever truly lost
- Cost: **$0**

### Layer 0.5: Signal Router (Cron Agent)

- Runs every 15 minutes (configurable)
- Reads daily logs (WAL protocol)
- Classifies signals: corrections, decisions, facts, self-signals
- Routes to appropriate Layer 1 buckets
- Integrated with HEARTBEAT checks (job search, trading, subagents, deadlines)
- Cost: **$0.72–$1.44/day** (Haiku) or **$0** (Ollama)

### Layer 1: Hierarchical Memory Buckets (.md files)

```
memory/
├── MEMORY.md                    # Curated long-term
├── daily/2026-04-24.md          # Raw episodic logs
├── self/identity.md, beliefs.md # Personality
├── lessons/mistakes.md          # Learnings
├── projects/job-search.md       # Active work
└── heartbeat/                   # Time-sensitive tracking
    ├── job-search.md
    ├── trading/portfolio.md
    ├── subagent-status.md
    └── time-sensitive.md
```

- Human-readable, Git-compatible, fully debuggable
- Quality rule: Compress over accumulate
- Cost: **$0**

### Layer 1.5: Semantic Recall (Qdrant + FalkorDB) — MANDATORY in v2.0

**Qdrant (Vector Search)**
- Semantic similarity search: *"What did we discuss about synbio three months ago?"*
- HNSW indexing for fast retrieval
- Deployment: Native binary, Docker, or cloud

**FalkorDB (Entity Graphs)**
- Relationship tracking: *"Who works where? What dates matter?"*
- Graph queries: *"Find all people mentioned in job search context"*
- Deployment: Native binary, Redis module, or cloud

**Why mandatory?**
- Agents with >30K messages can't use grep
- State-of-the-art retrieval reduces context injection latency
- Native binaries require zero Docker infrastructure
- Cost is zero; no vendor lock-in

Cost: **$0** (self-hosted) or **$20–50/mo** (cloud)

### Layer 2: Disaster Recovery (Git + Snapshots)

- Daily Git commits (memory version control)
- VPS snapshots (point-in-time recovery)
- Pre-update snapshots (before OpenClaw upgrades)
- Post-update healthchecks (21 automated tests)
- Cost: **$0**

---

## Cost Breakdown

| Deployment | Layer 0.5 Model | Qdrant/FalkorDB | Total Cost/Day |
|-----------|-----------------|-----------------|----------------|
| **Zero Budget** | Ollama (local) | Native binary | **$0** |
| **Standard** | Claude Haiku | Native binary | **$0.72–$1.44** |
| **Premium** | Claude Sonnet | Native binary | **$3.12–$6.24** |
| **Cloud** | Claude Haiku | Qdrant/Redis Cloud | **$25–55/month** |

---

## Platform Support

**All platforms supported.** Choose your deployment mode:

| Platform | Native | Docker | Cloud |
|----------|--------|--------|-------|
| Linux (Ubuntu/Debian) | ✅ | ✅ | ✅ |
| macOS (Intel/ARM) | ✅ | ✅ | ✅ |
| Windows (WSL2) | ✅ | ✅ | ✅ |
| VPS (Hostinger, DigitalOcean, AWS) | ✅ | ✅ | ✅ |
| Docker container | ✅ | ✅ | ✅ |
| Air-gapped (offline) | ✅ | ✅ | ❌ |

---

## Configuration

Edit `~/.openclaw/workspace/openclaw.json`:

```json
{
  "plugins": {
    "trident": {
      "enabled": true,
      
      "layer0_5": {
        "model": "anthropic/claude-haiku-4-5",
        "interval_minutes": 15
      },
      
      "layer1_5": {
        "qdrant": {
          "mode": "binary",  // "binary", "docker", or "cloud"
          "host": "localhost",
          "port": 6333
        },
        "falkordb": {
          "mode": "binary",  // "binary", "docker", "redis", or "cloud"
          "host": "localhost",
          "port": 6379
        }
      },
      
      "layer2": {
        "git_remote": "https://github.com/YOUR_USERNAME/memory.git",
        "commit_interval_hours": 24
      }
    }
  }
}
```

---

## Migration from v1.x

Upgrading from Trident v1.0?

```bash
openclaw trident migrate v1-to-v2

# This will:
# 1. Download Qdrant + FalkorDB binaries
# 2. Build vector embeddings from existing Layer 1 memory
# 3. Migrate FalkorDB graphs
# 4. Enable Layer 1.5 in config
```

**Zero data loss.** All existing memory preserved and indexed.

---

## Examples

### Example 1: Search for Context

```bash
> "What were my top 3 job applications last month?"

# Agent internally uses:
await memory_search({
  query: "application Genentech OR Synthego OR Inscripta",
  scope: "both",
  limit: 20
})

# Returns: 5 matching messages from memory files
```

### Example 2: Semantic Context Injection

```bash
# Agent needs context. Layer 0.5 injects pre-turn via:
await memory_recall({
  prompt: "What is the current job search status and strategy?",
  max_tokens: 1500,
  similarity_threshold: 0.75
})

# Qdrant searches vectors. FalkorDB retrieves entities.
# Returns: 3–5 most relevant context chunks with source citations
```

### Example 3: Continuous Memory Updates

```bash
// Every heartbeat, Layer 0.5 routes signals:
await memory_update({
  file: "memory/heartbeat/job-search.md",
  entry: "New opportunity: Inscripta Principal Scientist, $160k, strong match",
  section: "## Active Leads",
  tag: "[opportunity]"
})
```

---

## Feature Comparison

| Feature | Trident v2.0 | Mem0 | LangChain | AutoGPT |
|---------|-------|------|-----------|---------|
| **Lossless capture** (SQLite+DAG) | ✅ | ❌ | ❌ | ❌ |
| **Semantic recall** (built-in) | ✅ | ❌ | ❌ | ❌ |
| **Native binaries** (no Docker) | ✅ | ❌ | ❌ | ❌ |
| **Human-readable storage** | ✅ (.md) | ❌ | ⚠️ | ⚠️ |
| **Personality development** | ✅ | ❌ | ❌ | ❌ |
| **Offline support** | ✅ | ❌ | ⚠️ | ⚠️ |
| **Git-compatible** | ✅ | ❌ | ❌ | ❌ |
| **No vendor lock-in** | ✅ | ❌ | ✅ | ✅ |

---

## Support

- **GitHub:** [ShivaClaw/trident-plugin](https://github.com/ShivaClaw/trident-plugin)
- **Issues:** [GitHub Issues](https://github.com/ShivaClaw/trident-plugin/issues)
- **Discussions:** [GitHub Discussions](https://github.com/ShivaClaw/trident-plugin/discussions)
- **ClawHub:** [shivaclaw/trident](https://clawhub.ai/shivaclaw/trident)

---

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.

---

*Your agent should remember. Trident makes it permanent.*
