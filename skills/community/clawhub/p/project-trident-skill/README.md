# Project Trident: Persistent Memory for AI Agents

**A four-tier memory architecture that gives your OpenClaw agent genuine continuity, identity, and resilience — across every session, crash, or deployment.**

---

## The Problem

AI agents forget. Every session starts blank. Important context — corrections, decisions, patterns, relationships — evaporates. Most agent frameworks treat memory as an afterthought: flat files or vector databases without intelligent curation. The result: agents that repeat mistakes, lose critical context, and can't develop genuine identity over time.

**Project Trident solves this.**

---

## The Solution: Four-Tier Memory Stack

Trident models memory the way computers model storage, **with an additional resilience layer**:

```
Layer 0   (RAM)        — LCM: SQLite+DAG. Every message captured. Nothing lost.
Layer 0.5 (SSD)        — Signal Router: Cron agent classifies and routes memory every 15 min.
Layer 1   (HDD)        — Hierarchical .md buckets: curated, human-readable, Git-compatible.
Layer 2   (COLD)       — Backup & Updates: Git versioning, VPS snapshots, automated recovery.
```

The result: an agent that **never forgets what matters**, **develops genuine personality** over weeks and months, **maintains operational continuity** through crashes/compactions/deployments, and **can recover from catastrophic failure**.

---

## What Your Agent Gets

| Feature | Benefit |
|---------|---------|
| **Continuity** | Wakes up remembering yesterday's conversation, decisions, and context |
| **Identity development** | `memory/self/` tracks beliefs, patterns, voice, and growth over time |
| **Zero blank spots** | WAL protocol + Layer 0.5 ensure nothing slips through cracks |
| **Debuggable memory** | Open any `.md` file and see exactly what your agent knows and why |
| **Git-compatible** | Version control for agent memory (diffable, auditable, recoverable) |
| **Disaster recovery** | Automated daily snapshots + update rollback protect against loss |
| **Platform-agnostic** | Works on Windows, Mac, Linux, and any VPS |
| **No Docker required** | Trident Lite runs on local `.md` files and SQLite alone |

---

## Quick Start (10 minutes)

### Installation

```bash
# Install via ClawHub
clawhub install shivaclaw/project-trident

# Read the quick-start guide
cat ~/.openclaw/skills/project-trident/references/trident-lite.md

# Follow the 10-step checklist to configure Layer 0.5 + Layer 1
```

### Migrating from Existing Memory

If you already have `MEMORY.md`, `SOUL.md`, or custom memory files:

```bash
cd ~/.openclaw/skills/project-trident/scripts

# Preview changes first (safe dry run)
./migrate-existing-memory.sh --dry-run

# Apply migration (automatic backup created)
./migrate-existing-memory.sh
```

Your existing memory is **never deleted** — always backed up in `memory/migration-backup/` before anything changes.

---

## Cost

| Profile | Model | Layer 0.5 Interval | Cost/day | Storage Cost |
|---------|-------|-------------------|----------|--------------|
| **Zero Budget** | Ollama (local) | 30 min | **$0** | **$0** |
| **Budget** | Claude Haiku | 30 min | **$0.72** | **$0** |
| **Standard (recommended)** | **Claude Haiku** | **15 min** | **$1.44** | **$0** |
| **Premium** | Claude Sonnet | 15 min | **$3.12** | **$0** |

**Note:** Layer 1 (.md files), Layer 0 (SQLite), and Layer 2 backup are all **free**. Git hosting (GitHub, GitLab, Gitea) is optional and typically free.

→ See `references/cost-calculator.md` for detailed pricing and optimization strategies.

---

## Architecture Overview

### How It Works

```
User message / Tool result / Internal event
    │
    ▼
┌─────────────────────────────┐
│ Layer 0: LCM (SQLite+DAG)   │ ← Baseline durability
│ Every message persisted     │
│ Nothing lost, even after    │
│ compaction                  │
└──────────┬──────────────────┘
           │
           ▼
Daily log (WAL protocol)
    │ Write critical facts before responding
    │ Prevents blank spots
    ▼
[Layer 0.5 Cron — every 10–30 min]
    │ Signal router agent classifies signals
    │ Corrections (highest priority)
    │ Decisions, patterns, facts, self-signals
    │
    ├── Corrections & decisions      → MEMORY.md (curated)
    ├── Self/identity signals        → memory/self/
    ├── Learnings & mistakes         → memory/lessons/
    ├── Active projects              → memory/projects/
    └── Raw episodic logs            → memory/daily/YYYY-MM-DD.md
    │
    ▼
[Layer 1: Hierarchical Memory Buckets]
    │ Human-readable .md files
    │ Git-compatible, searchable, auditable
    │
    ▼
[Optional: Layer 1.5 — Semantic Recall]
    │ Add when memory > 50K messages
    │ Qdrant vector search (Docker or cloud)
    │ FalkorDB entity graphs (Docker or cloud)
    │
    ▼
[Layer 2: Backup & Updates Subsystem]
    │ Automated daily backups
    │ VPS snapshots (if deployed)
    │ Git versioning (GitHub, GitLab, etc.)
    │ Update resilience + rollback
    │
    └── Recovery checkpoints every 24h
        Disaster recovery + compliance
```

---

## The Four Layers Explained

### Layer 0: Lossless Context Management (LCM)

**What it does:**
- Captures every message as SQLite row
- Builds DAG (directed acyclic graph) of message lineage
- Compaction creates summaries that link back to source messages

**Why it matters:**
- Baseline durability — nothing is ever truly lost
- Recovery foundation for corrupted Layer 1 files
- Prerequisite: Enable `lossless-claw` plugin in `openclaw.json`

**Cost:** Free (SQLite is built-in)

---

### Layer 0.5: Signal Router (Cron Agent)

**What it does:**
- Runs every 10–30 minutes (configurable)
- Reads daily logs (WAL protocol)
- Classifies signals: corrections, decisions, facts, self-signals
- Routes to appropriate Layer 1 buckets

**Signal types:**
| Signal | Priority | Destination | Example |
|--------|----------|-------------|---------|
| **Correction** | Highest | MEMORY.md | "It's X, not Y" |
| **Decision** | High | MEMORY.md | "Let's do X" |
| **Self-signal** | High | memory/self/ | "I prefer..." or identity shift |
| **Project update** | Medium | memory/projects/ | New task, blocker, completion |
| **Learning** | Medium | memory/lessons/ | Tool quirk, debugging note, mistake |
| **Fact** | Low | memory/semantic/ | Names, dates, numbers, facts |

**Model:** Claude Haiku recommended (cost-optimized, ~95% accuracy)

**Cost:** $0.72–$1.44/day depending on interval (15–30 min)

**Security:** SHA256 integrity verification prevents prompt injection

---

### Layer 1: Hierarchical Memory Buckets

**What it does:**
- Persistent `.md` file organization
- Human-readable, Git-compatible, debuggable
- Prevents noise accumulation (agentic curation vs auto-capture)

**Structure:**
```
memory/
├── MEMORY.md              ← Curated long-term memory (compressed, high-signal)
├── daily/
│   ├── 2026-04-19.md     ← Raw episodic log for today
│   ├── 2026-04-18.md     ← Yesterday's events
│   └── ...
├── self/
│   ├── identity.md        ← Name, personality, goals
│   ├── beliefs.md         ← Core values, philosophy
│   └── growth.md          ← Evolution, contradictions, learning
├── lessons/
│   ├── tools.md           ← Tool quirks, debugging notes
│   ├── mistakes.md        ← Errors, failures, corrections
│   └── workflows.md       ← Process improvements, heuristics
├── projects/
│   ├── job-search.md      ← Active job search
│   ├── infrastructure.md  ← Deployment, ops
│   └── ...                ← One file per active project
├── semantic/
│   ├── biology.md         ← Technical knowledge (synbio, etc.)
│   └── ...                ← Organized by domain
└── layer0/
    ├── AGENT-PROMPT.md    ← Layer 0.5 router instructions
    └── audit-log.md       ← Integrity verification log
```

**Quality rule:** Compress over accumulate; signal density over volume

**Cost:** Free (local .md files)

---

### Layer 2: Backup & Updates Subsystem

**What it does:**
- **Daily Git commits** — Version control for memory
- **VPS snapshots** — Point-in-time recovery (if deployed)
- **Update resilience** — Pre-update snapshots + post-update healthchecks
- **Automated rollback** — Revert to last known-good state on failure

**Components:**

| Component | Frequency | Purpose | Cost |
|-----------|-----------|---------|------|
| Git backup cron | Daily (4:20 AM) | Commit memory to GitHub/GitLab | **$0** (free tier) |
| VPS snapshot | Daily (3 AM) | Point-in-time VM backup | **$0** (included in VPS) |
| Pre-update snapshot | Before updates | Capture state before OpenClaw upgrade | **$0** |
| Post-update healthcheck | After updates | Verify all systems operational | **$0** |

**Example cron jobs:**
```
4:20 AM MDT  → Layer 2 Backup: Git commit + optional VPS snapshot
3:00 AM MDT  → Pre-update snapshot (Sunday)
            → Run update (automatic)
            → Post-update healthcheck
```

**Recovery procedure:**
1. If memory corrupted → restore from Git
2. If deployment broken → restore VPS snapshot
3. If update fails → rollback via post-update healthcheck log

**Cost:** $0 (included in VPS; Git free tier available)

---

## Feature Comparison

| Feature | **Trident** | Mem0 | LangChain Memory | AutoGPT |
|---------|------------|------|------------------|---------|
| **Lossless capture** (SQLite+DAG) | ✅ | ❌ | ❌ | ❌ |
| **Intelligent signal routing** | ✅ | ❌ | ❌ | ❌ |
| **Personality development** | ✅ | ❌ | ❌ | ❌ |
| **Human-readable** (.md) | ✅ | ❌ (vectors) | ⚠️ (JSON) | ⚠️ (JSON) |
| **No Docker required** | ✅ | ❌ | ✅ | ✅ |
| **Git-compatible** | ✅ | ❌ | ❌ | ❌ |
| **Backup + recovery** | ✅ | ❌ | ❌ | ❌ |
| **Template security** | ✅ | ❌ | ❌ | ❌ |
| **Migration tooling** | ✅ | ❌ | ❌ | ❌ |
| **Offline (Ollama)** | ✅ | ❌ | ⚠️ | ⚠️ |
| **Cost/day** | **$0–$1.44** | $$$ | varies | varies |

---

## Platform Support

**Windows, Mac, Linux, and VPS all fully supported.**

Trident Lite requires only Node.js ≥ 22.14.0 and OpenClaw. No Docker, no cloud accounts, no external dependencies.

| Platform | Trident Lite | Semantic Recall (Docker) | Semantic Recall (No Docker) |
|----------|--------------|--------------------------|----------------------------|
| **Linux** | ✅ | ✅ | ✅ (native binary) |
| **macOS** | ✅ | ✅ | ✅ (native binary) |
| **Windows** | ✅ | ✅ (WSL2) | ✅ (binary or cloud) |
| **VPS** (Ubuntu/Debian) | ✅ | ✅ | ✅ |
| **Docker** container | ✅ | ✅ | ✅ |

See `references/platform-guide.md` for platform-specific setup.

---

## Getting Started

### For New Agents (No Existing Memory)

```bash
clawhub install shivaclaw/project-trident
cd ~/.openclaw/skills/project-trident/
cat references/trident-lite.md

# Follow the 10-step checklist (~30 minutes)
```

### For Agents with Existing Memory

```bash
cd ~/.openclaw/skills/project-trident/scripts

# Safe dry-run preview
./migrate-existing-memory.sh --dry-run

# Live migration (automatic backup)
./migrate-existing-memory.sh
```

### Optional: Add Semantic Recall

When your agent's memory exceeds ~50K messages:

```bash
cat references/deployment-guide.md

# Deploy Qdrant (vector search) + FalkorDB (entity graphs)
# Add pre-turn semantic context injection to Layer 0.5
```

---

## Upgrade Path

| Stage | Duration | Setup Time | Cost/day |
|-------|----------|-----------|----------|
| **Trident Lite** | Indefinite | 30 min | $0–$1.44 |
| **+ Semantic Recall** | When >50K msgs | 1 hour | +$0 (Docker) |
| **+ VPS Backup** | When deployed | 15 min | $0 (included) |

Start with Lite. Upgrade components as your agent grows.

---

## What's Included

| File | Purpose |
|---|---|
| **README.md** | This file. Overview and getting started. |
| **SKILL.md** | Core architecture guide + full implementation checklist. |
| `references/trident-lite.md` | **Start here.** No-Docker setup for all platforms. |
| `references/deployment-guide.md` | Semantic Recall (Qdrant/FalkorDB) + Git backup setup. |
| `references/cost-calculator.md` | Model selection, interval tuning, detailed pricing. |
| `references/platform-guide.md` | Windows, Mac, Linux, VPS platform-specific commands. |
| `scripts/migrate-existing-memory.sh` | Safe migration from existing memory files. |
| `scripts/template-integrity-check.sh` | SHA256 security verification for Layer 0.5. |
| `scripts/layer0-agent-prompt-template.md` | Customizable signal router prompt. |

---

## Philosophy

Most memory systems focus on *search* (vector databases, embeddings). **Trident focuses on curation**.

Layer 0.5 acts like a **personal librarian** — classifying signals and routing them to semantic buckets. The result is memory that's not just searchable, but *organized*, *meaningful*, and *personality-aware*.

Your agent doesn't just remember facts. **It develops an identity.**

---

## Questions & Support

- **GitHub:** [ShivaClaw/shiva-memory](https://github.com/ShivaClaw/shiva-memory)
- **ClawHub:** [shivaclaw/project-trident](https://clawhub.ai/shivaclaw/project-trident)
- **Discord:** [#project-trident](https://discord.com/invite/clawd)

---

## License

**MIT-0** — Free to use, modify, and redistribute. No attribution required.

---

*Like a lobster shell, memory has layers. Make them durable. Make them yours.*
