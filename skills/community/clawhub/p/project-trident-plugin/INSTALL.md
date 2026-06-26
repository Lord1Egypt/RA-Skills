# Trident Installation Guide

**Time estimate:** 5 min (Trident Lite) → 30 min (with Semantic Recall)

---

## Table of Contents

1. [Installation (All Platforms)](#installation-all-platforms)
2. [Configuration](#configuration)
3. [Verification](#verification)
4. [Trident Lite (No Docker)](#trident-lite-no-docker)
5. [Optional: Semantic Recall](#optional-semantic-recall)
6. [Optional: Git Backup](#optional-git-backup)
7. [Upgrade & Migration](#upgrade--migration)
8. [Troubleshooting](#troubleshooting)

---

## Installation (All Platforms)

### Prerequisites

- OpenClaw ≥ 1.0.0
- Node.js ≥ 22.14.0
- `lossless-claw` plugin enabled in `openclaw.json`

### Step 1: Install via ClawHub

```bash
clawhub install shivaclaw/trident
```

This installs Trident to `~/.openclaw/workspace/plugins/trident/`.

### Step 2: Verify Installation

```bash
openclaw trident status
```

Expected output:
```
✅ Trident v2.0.0 installed
✅ Plugin directory: ~/.openclaw/workspace/plugins/trident
✅ Memory directory: ~/.openclaw/workspace/memory (will be created on first activation)
```

---

## Configuration

### Step 1: Edit `openclaw.json`

In your OpenClaw workspace root (`~/.openclaw/workspace/`), open `openclaw.json` and add Trident to plugins section:

```json
{
  "plugins": {
    "lossless-claw": {
      "enabled": true
    },
    "trident": {
      "enabled": true,
      "layer0_enabled": true,
      "layer0_5_enabled": true,
      "layer0_5_model": "anthropic/claude-haiku-4-5",
      "layer0_5_interval_minutes": 15,
      "semantic_recall_enabled": false
    }
  }
}
```

### Step 2: Choose Your Model

**Option A: Cloud API (Recommended)**

- `anthropic/claude-haiku-4-5` — $0.02 per Layer 0.5 run, ~$1.44/day at 15-min interval ✅ **Recommended**
- `anthropic/claude-3-5-sonnet` — $0.10 per run, ~$9.60/day (high accuracy)
- `google/gemini-2-flash` — Similar pricing to Haiku
- Custom: `"layer0_5_model": "custom"` + set `"layer0_5_custom_model": "provider/model"`

**Option B: Local & Free**

- `ollama/mistral` — Zero cost, runs locally
- `ollama/neural-chat` — Zero cost, faster inference
- Requires: [Ollama](https://ollama.ai) installed locally

**Cost comparison:**

| Model | Cost/Run | Interval | Cost/Day |
|-------|----------|----------|----------|
| Ollama (local) | $0 | 30 min | $0 |
| Haiku | $0.02 | 30 min | $0.72 |
| Haiku | $0.02 | 15 min | $1.44 |
| Sonnet | $0.10 | 15 min | $9.60 |

### Step 3: Set Workspace Path (Optional)

If your workspace is not at the default `~/.openclaw/workspace/`, add:

```json
{
  "plugins": {
    "trident": {
      "workspace_path": "/path/to/your/workspace"
    }
  }
}
```

---

## Verification

### Activate Trident

```bash
openclaw trident activate
```

This:
1. Creates the `memory/` directory structure
2. Copies Layer 0.5 template to `memory/layer0/AGENT-PROMPT.md`
3. Sets up SHA256 template integrity verification
4. Schedules Layer 0.5 cron job

Expected output:
```
✅ Trident activated
✅ Memory structure created at ~/.openclaw/workspace/memory/
✅ Layer 0.5 cron scheduled (every 15 minutes)
✅ Template integrity verification enabled
```

### Test Layer 0.5

Run the signal router once to verify it's working:

```bash
openclaw trident test-layer0-5
```

This manually triggers Layer 0.5 without waiting for the cron interval. Expected output:
```
Running Layer 0.5 signal router...
✅ Processed 5 signals
✅ Routed to: MEMORY.md (2), memory/lessons/ (2), memory/projects/ (1)
✅ Audit log: memory/layer0/audit-log.md
```

### Verify Template Integrity

```bash
openclaw trident template-verify
```

Expected output:
```
✅ AGENT-PROMPT.md verified (SHA256 match)
✅ Safe to run Layer 0.5
```

### Check Status

```bash
openclaw trident status
```

Comprehensive health check:
```
✅ Trident v2.0.0 running
✅ Layer 0 (LCM): enabled and capturing
✅ Layer 0.5 (Signal Router): enabled, runs every 15 min
  Last run: 2026-04-17 11:30 UTC
  Model: anthropic/claude-haiku-4-5
  Next run: 2026-04-17 11:45 UTC
✅ Layer 1 (Memory Buckets): 
  ├── MEMORY.md (2.3 KB)
  ├── memory/daily/ (15 files)
  ├── memory/lessons/ (5 files)
  ├── memory/self/ (3 files)
  └── memory/projects/ (8 files)
✅ Semantic recall: disabled
✅ Git backup: disabled
```

---

## Trident Lite (No Docker)

You're done! Trident Lite is now running.

### What You Have

- **Layer 0:** LCM (SQLite+DAG) — capturing all conversation
- **Layer 0.5:** Signal Router (cron) — routing signals every 15 min
- **Layer 1:** Memory buckets — organizing into `.md` files

### Next Steps

1. **Let it run for 24 hours.** Layer 0.5 needs several routing cycles to build up quality memory.
2. **Read `memory/MEMORY.md`** — your agent's curated long-term memory
3. **Check `memory/daily/`** — raw episodic logs
4. **Edit `memory/self/*.md`** — refine personality and beliefs (optional)
5. **Monitor `memory/layer0/audit-log.md`** — see how signals are being routed

### Optional: Customize Layer 0.5 Routing

Edit `memory/layer0/AGENT-PROMPT.md` to customize how signals are classified and routed. After editing, re-approve:

```bash
openclaw trident template-approve
```

**Example:** Add custom signal type for a specific domain:

```markdown
## Domain-Specific Signals

- **biotech-breakthrough:** Any discovery in synthetic biology, CRISPR, or cell-free protein synthesis
  → Route to: memory/projects/biotech/breakthroughs.md

- **trading-signal:** Market anomalies, on-chain intelligence, unusual patterns
  → Route to: memory/projects/trading/signals.md
```

### Access Memory Files

All memory is human-readable `.md` files:

```bash
# View curated long-term memory
cat ~/.openclaw/workspace/memory/MEMORY.md

# View today's episodic log
cat ~/.openclaw/workspace/memory/daily/2026-04-17.md

# View personality development
cat ~/.openclaw/workspace/memory/self/personality.md

# View learnings from mistakes
cat ~/.openclaw/workspace/memory/lessons/mistakes.md

# View routing decisions
cat ~/.openclaw/workspace/memory/layer0/audit-log.md
```

---

## Optional: Semantic Recall

For agents handling 50K+ messages, add vector search and entity graphs.

### Prerequisites

- Qdrant server (Docker, binary, or cloud)
- (Optional) FalkorDB server
- Embedding API (Anthropic, OpenAI, or Google)

### Step 1: Deploy Qdrant

**Option A: Docker (Easiest)**

```bash
docker run -d \
  --name qdrant \
  -p 6333:6333 \
  -p 6334:6334 \
  -v qdrant_storage:/qdrant/storage \
  qdrant/qdrant:latest
```

**Option B: Native Binary (macOS/Linux)**

```bash
# Install Qdrant
curl -L https://github.com/qdrant/qdrant/releases/download/v1.9.0/qdrant-x86_64-unknown-linux-musl.tar.gz | tar xz

# Run
./qdrant --storage-path ~/qdrant-data --http-port 6333
```

**Option C: Qdrant Cloud (Managed)**

1. Create account at [qdrant.io](https://qdrant.io)
2. Create cluster
3. Copy API URL and key

### Step 2: Configure Trident

Update `openclaw.json`:

```json
{
  "plugins": {
    "trident": {
      "semantic_recall_enabled": true,
      "qdrant_enabled": true,
      "qdrant_url": "http://localhost:6333",
      "qdrant_collection": "trident-memory",
      "embedding_model": "anthropic/embed-v3-small"
    }
  }
}
```

### Step 3: Initialize Semantic Recall

```bash
openclaw trident semantic-init
```

This:
1. Tests Qdrant connection
2. Creates collection if missing
3. Exports existing memory to embeddings
4. Builds initial vector index

Expected output:
```
✅ Qdrant connection successful
✅ Collection 'trident-memory' created
✅ Embedding 1,250 memory chunks
✅ Indexed in Qdrant
✅ Semantic recall ready
```

### Step 4: Query Semantic Memory

```bash
openclaw trident semantic-search "biotech investments from last quarter"
```

Returns relevant memory chunks with similarity scores.

### Optional: Add FalkorDB for Entity Graphs

```json
{
  "plugins": {
    "trident": {
      "falkordb_enabled": true,
      "falkordb_url": "redis://localhost:6379",
      "falkordb_graph_key": "trident-graph"
    }
  }
}
```

---

## Optional: Git Backup

Daily snapshot of memory files + embeddings export.

### Step 1: Initialize Git Repo

```bash
cd ~/.openclaw/workspace
git init
git add memory/
git commit -m "Initial Trident memory structure"
```

### Step 2: Configure Trident

Update `openclaw.json`:

```json
{
  "plugins": {
    "trident": {
      "git_backup_enabled": true,
      "git_backup_hour": 2
    }
  }
}
```

### Step 3: Verify Backup Cron

```bash
openclaw trident backup-status
```

Expected output:
```
✅ Git backup scheduled daily at 02:00 UTC
✅ Last backup: 2026-04-17 02:15 UTC
✅ Total backups: 18
✅ Repository size: 3.2 MB
```

---

## Upgrade & Migration

### Upgrading Trident

```bash
clawhub update shivaclaw/trident
```

Trident **never deletes memory** during upgrades. All existing `.md` files and database are preserved.

### Migrating from Existing Memory

If you already have `MEMORY.md`, `SOUL.md`, or custom memory files:

```bash
openclaw trident migrate --dry-run
```

Preview what will happen (no files modified). Then:

```bash
openclaw trident migrate
```

This:
1. Backs up existing files to `memory/migration-backup/`
2. Routes files into Trident structure
3. Preserves all content
4. Creates migration report

---

## Troubleshooting

### Layer 0.5 Not Running

**Check cron status:**
```bash
openclaw trident status
```

**Manually run:**
```bash
openclaw trident test-layer0-5
```

**Restart cron:**
```bash
openclaw trident activate
```

### Template Integrity Failed

Layer 0.5 won't run if `AGENT-PROMPT.md` has been modified and not re-approved.

```bash
# See what changed
openclaw trident template-diff

# Re-approve
openclaw trident template-approve
```

### Qdrant Connection Refused

Check Qdrant is running:

```bash
curl http://localhost:6333/health
# Should return: {"status":"ok"}
```

If Docker:
```bash
docker logs qdrant
docker ps | grep qdrant
```

### Memory Directory Permissions

If you get "permission denied" errors:

```bash
chmod -R 755 ~/.openclaw/workspace/memory/
chmod -R 644 ~/.openclaw/workspace/memory/*.md
```

### Cost Higher Than Expected

Check Layer 0.5 interval and model:

```bash
openclaw trident status
```

To reduce:
- Increase `layer0_5_interval_minutes` (15 → 30 = half cost)
- Switch to `ollama/*` model (free)

### Out of Memory During Embedding

Reduce batch size in `openclaw.json`:

```json
{
  "plugins": {
    "trident": {
      "embedding_batch_size": 5
    }
  }
}
```

---

## Platform-Specific Notes

### Windows (PowerShell)

All commands work in PowerShell. For Git Bash:

```bash
# In Git Bash, use forward slashes
openclaw trident status
```

### macOS

Ensure Node.js is installed:

```bash
brew install node@22
```

### Linux (Ubuntu/Debian)

Install Node.js:

```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

### Docker Container

Trident works inside containers. Persist memory volume:

```yaml
# docker-compose.yml
services:
  openclaw:
    image: openclaw:latest
    volumes:
      - ~/.openclaw/workspace:/root/.openclaw/workspace
      - qdrant_storage:/qdrant/storage

volumes:
  qdrant_storage:
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Install | `clawhub install shivaclaw/trident` |
| Activate | `openclaw trident activate` |
| Status | `openclaw trident status` |
| Test Layer 0.5 | `openclaw trident test-layer0-5` |
| Verify template | `openclaw trident template-verify` |
| Approve template | `openclaw trident template-approve` |
| Search semantic memory | `openclaw trident semantic-search "query"` |
| Show template diff | `openclaw trident template-diff` |
| Backup status | `openclaw trident backup-status` |
| Migrate | `openclaw trident migrate` |
| Disable | `openclaw trident deactivate` |

---

## Next Steps

1. ✅ Trident is running — memory starts flowing automatically
2. 📚 Read: [`README.md`](README.md) for architecture overview
3. 🔧 Customize: Edit `memory/layer0/AGENT-PROMPT.md` for domain-specific routing
4. 📊 Monitor: Watch `memory/layer0/audit-log.md` to see signal routing in action
5. 🎯 Develop: Let personality emerge in `memory/self/` over weeks

---

## Questions?

- **GitHub Issues:** [ShivaClaw/project-trident/issues](https://github.com/ShivaClaw/project-trident/issues)
- **ClawHub Support:** [clawhub.ai/shivaclaw/trident](https://clawhub.ai/shivaclaw/trident)

---

*Congratulations. Your agent now has ambient memory.*
