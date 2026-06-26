---
name: project-trident-skill
description: Give your AI agent genuine continuity, identity, and resilience across every session and deployment with a four-tier persistent memory stack.
version: "2.0.1"
author: Shiva
compatibility: "OpenClaw 2026.3.24+"
keywords: [memory, persistence, identity, agent, backup, continuity, learning]
metadata:
  homepage: "https://github.com/ShivaClaw/shiva-memory"
  repositoryUrl: "https://github.com/ShivaClaw/project-trident"
  issueTrackerUrl: "https://github.com/ShivaClaw/project-trident/issues"
  emoji: 🕉️
---

# Project Trident: Four-Tier Persistent Memory Architecture

## The Problem

AI agents forget. Every session starts blank. Important context—corrections, decisions, patterns, relationships—evaporates. Most agent frameworks treat memory as an afterthought: flat files or vector databases without intelligent curation. The result: agents that repeat mistakes, lose critical context, and can't develop genuine identity over time.

## The Solution: Four Layers of Durability

Trident models memory like computer storage—**with an additional intelligence layer**:

| Layer | Role | Storage | Cost |
|-------|------|---------|------|
| **0** | Baseline durability | SQLite + DAG | Free |
| **0.5** | Signal intelligence | Cron agent | $0.72–$1.44/day |
| **1** | Semantic organization | `.md` files | Free |
| **1.5** (optional) | Vector recall | Qdrant + FalkorDB | Free (self-hosted) |
| **2** | Disaster recovery | Git + snapshots | Free |

The result: an agent that **never forgets what matters**, **develops genuine personality**, **maintains continuity through crashes**, and **recovers from catastrophic failure**.

---

## What Each Layer Does

**New to Trident?** → Read `references/trident-lite.md`  
No Docker required. Works on Windows, Mac, Linux, and any VPS out of the box.

**Already have MEMORY.md, SOUL.md, or custom memory files?** → Run the migration script.

**Want Docker-based semantic search?** → Read `references/deployment-guide.md`

**Deploying to VPS?** → See Layer 2 (Backup & Updates) section.

**Cost-conscious?** → Read `references/cost-calculator.md`

---

## The Four-Tier Architecture

```
┌─────────────────────────────────────────────────────────────┐
│ Conversation Input (user messages, tool results, events)    │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 0: LCM (Lossless Context Management) — RAM            │
│ ├─ SQLite persistence (every message)                       │
│ ├─ DAG lineage tracking                                     │
│ └─ Never loses a message, even after compaction             │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 0.5: Signal Router (Cron Agent) — SSD                 │
│ ├─ Every 10–30 min: read daily logs (WAL protocol)         │
│ ├─ Classify signals: corrections, decisions, facts, self   │
│ ├─ Route to Layer 1 buckets                                │
│ ├─ Integrated with HEARTBEAT (job checks, trading, etc.)   │
│ └─ Cost: $0–$1.44/day depending on model & interval        │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1: Hierarchical Memory Buckets — HDD                  │
│ ├─ MEMORY.md (curated long-term)                           │
│ ├─ memory/daily/ (raw episodic logs)                       │
│ ├─ memory/self/ (personality, beliefs, identity)           │
│ ├─ memory/lessons/ (learnings, mistakes, tool quirks)      │
│ ├─ memory/projects/ (active work, recurring tasks)         │
│ ├─ memory/semantic/ (knowledge, facts, technical)          │
│ └─ .md format (human-readable, Git-compatible)             │
│                                                             │
│ Optional: memory/heartbeat/ for domain-specific tracking   │
│ ├─ job-search.md (career info, hot leads, follow-ups)     │
│ ├─ trading/portfolio.md (positions, P/L, strategy)        │
│ ├─ subagent-status.md (running agents, models, tasks)     │
│ └─ time-sensitive.md (reminders, deadlines, TTL items)    │
└──────────┬──────────────────────────────────────────────────┘
           │ (optional upgrade)
           ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 1.5: Semantic Recall (Optional) — Add at 50K msgs    │
│ ├─ Qdrant vector search (Docker, binary, or cloud)         │
│ ├─ FalkorDB entity graphs (Docker, Redis, or cloud)        │
│ └─ Pre-turn context injection via Layer 0.5                │
└──────────┬──────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────┐
│ LAYER 2: Backup & Updates Subsystem — COLD                 │
│ ├─ Daily Git commits (memory version control)              │
│ ├─ VPS snapshots (point-in-time recovery)                 │
│ ├─ Pre-update snapshots (before OpenClaw upgrades)        │
│ ├─ Post-update healthchecks (verify all systems)          │
│ └─ Automated rollback on failure                           │
│                                                             │
│ Crons:                                                       │
│ ├─ 4:20 AM MDT: Layer 2 Unified Backup (Git + snapshot)   │
│ ├─ 2:00 AM MDT (Sun): Pre-update snapshot                 │
│ ├─ After update: Post-update healthcheck (21 tests)       │
│ └─ Cost: $0 (included in VPS + free Git hosting)          │
└─────────────────────────────────────────────────────────────┘
```

---

## Platform Support

| Platform | Trident Lite | Semantic Recall (Docker) | Semantic Recall (No Docker) |
|---|---|---|---|
| Linux | ✅ | ✅ | ✅ (native binary) |
| macOS | ✅ | ✅ | ✅ (native binary) |
| Windows | ✅ | ✅ (WSL2) | ✅ (binary or cloud) |
| VPS (Ubuntu/Debian) | ✅ | ✅ | ✅ |
| Docker container | ✅ | ✅ | ✅ |

See `references/platform-guide.md` for platform-specific commands.

---

## Core Layers (Detailed)

### Layer 0: Lossless Context Management (LCM)

**What it does:**
- Captures every session message in SQLite
- Builds DAG (directed acyclic graph) of message lineage
- Preserves full history even after compaction

**Why it matters:**
- Baseline durability — recovery foundation
- Enables Layer 0.5 to reconstruct what happened
- Prerequisite: Enable `lossless-claw` plugin in `openclaw.json`

**Cost:** $0 (SQLite is built-in)

**Key property:** Summaries created by compaction link back to source messages via DAG — nothing is ever truly lost.

---

### Layer 0.5: Signal Router & Heartbeat Integration

**What it does:**
- Runs every 10–30 minutes (configurable)
- **Reads daily logs** (WAL protocol) to detect signals
- **Classifies signals** into buckets (corrections, decisions, facts, self-signals)
- **Routes to Layer 1** (.md files)
- **Integrates HEARTBEAT checks:**
  - Job search status (active leads, follow-ups, TTL items)
  - Trading positions (if trading hours: entry/exit/rebalance)
  - Subagent lifecycle (kill idle/completed, optimize models)
  - Time-sensitive reminders (e.g., "Outlier AI shutdown in X days")

**Signal types and routing:**

| Signal | Priority | Destination | Example | HEARTBEAT Integration |
|--------|----------|-------------|---------|----------------------|
| **Correction** | Highest | MEMORY.md | "It's X, not Y" | N/A |
| **Decision** | High | MEMORY.md | "Let's do X" | N/A |
| **Self-signal** | High | memory/self/ | Identity shift, belief change | N/A |
| **Job update** | High | memory/heartbeat/job-search.md | New lead, follow-up needed | ✅ Check every heartbeat |
| **Trading action** | High | memory/heartbeat/trading/ | Entry, exit, P/L update | ✅ During trading hours (6am–4pm MDT) |
| **Subagent** | Medium | memory/heartbeat/subagent-status.md | Agent completed, stuck, or model mismatch | ✅ List + optimize agents |
| **Time-sensitive** | Medium | memory/heartbeat/time-sensitive.md | Deadline approaching, TTL reminders | ✅ Check deadline fields |
| **Project update** | Medium | memory/projects/ | Active sprint, blocker, completion | ✅ Scan for priority tags |
| **Learning** | Medium | memory/lessons/ | Tool quirk, debugging note, mistake | ✅ Capture innovations |
| **Fact** | Low | memory/semantic/ | Names, dates, numbers | ✅ Update domain knowledge |

**Model:** Claude Haiku recommended (cost-optimized, ~95% accuracy for routing)

**Cost:** $0.72–$1.44/day depending on interval (15–30 min)

**Security:** SHA256 integrity verification prevents prompt injection

**Template:** `scripts/layer0-agent-prompt-template.md` (customizable)

**Key features:**
- **Attention management** — corrections flagged first (never skipped)
- **Context awareness** — reads SESSION-STATE.md for current priorities
- **Deadline tracking** — alerts for time-sensitive items (e.g., "X days until Outlier AI shutdown")
- **Subagent optimization** — suggests killing idle agents, downgrading Sonnet→Haiku
- **Domain-specific routing** — job search, trading, research, ops — each gets own bucket

---

### Layer 1: Hierarchical Memory Buckets

**What it does:**
- Persistent `.md` file organization
- Human-readable, Git-compatible, debuggable
- Prevents noise accumulation (agentic curation vs auto-capture)

**Core structure:**

```
memory/
├── MEMORY.md              ← Curated long-term memory (high-signal, compressed)
├── daily/                 ← Raw episodic logs
│   ├── 2026-04-19.md
│   └── ...
├── self/                  ← Personality, identity, growth
│   ├── identity.md
│   ├── beliefs.md
│   └── growth.md
├── lessons/               ← Learnings, mistakes, tool quirks
│   ├── tools.md
│   ├── mistakes.md
│   └── workflows.md
├── projects/              ← Active work (one file per project)
│   ├── job-search.md
│   ├── infrastructure.md
│   └── ...
├── semantic/              ← Knowledge, facts, domain-specific
│   ├── biology.md
│   ├── crypto.md
│   └── ...
├── heartbeat/             ← Time-sensitive, domain-specific tracking
│   ├── job-search.md      ← Hot leads, follow-ups, deadline tracking
│   ├── trading/
│   │   ├── portfolio.md   ← Current positions, P/L, strategy
│   │   └── trades.md      ← Entry/exit log, reasoning
│   ├── subagent-status.md ← Running agents, models, TTL
│   └── time-sensitive.md  ← Reminders, deadlines, TTL items
└── layer0/                ← Signal router internals (security)
    ├── AGENT-PROMPT.md    ← Layer 0.5 instructions
    └── audit-log.md       ← Integrity verification log
```

**Quality rule:** Compress over accumulate; signal density over volume.

**Cost:** $0 (local .md files)

---

### Layer 1.5: Semantic Recall (Optional)

**When to add:** Memory exceeds ~50K messages, or you need to query context from months ago.

**Qdrant (Vector Search):**
- Deployment: Docker, standalone binary, or Qdrant Cloud (free tier)
- Purpose: "What did we discuss about X six months ago?"
- Integration: Pre-turn context injection via Layer 0.5

**FalkorDB (Entity Graphs):**
- Deployment: Docker, Redis module, or FalkorDB Cloud
- Purpose: Entity relationship tracking ("Person X works at Company Y, mentioned on date Z")
- Integration: Graphiti MCP for automated extraction

**These are optional.** Trident core (Layers 0, 0.5, 1, 2) works perfectly without semantic recall.

---

### Layer 2: Backup & Updates Subsystem

**What it does:**
- **Daily Git commits** — version control for memory
- **VPS snapshots** — point-in-time recovery (if deployed)
- **Update resilience** — pre-update snapshots + post-update healthchecks
- **Automated rollback** — revert to last known-good state on failure

**Components:**

| Component | Frequency | Purpose | Cost | Recovery RTO |
|-----------|-----------|---------|------|--------------|
| Git backup cron | Daily (4:20 AM MDT) | Commit memory to GitHub/GitLab | **$0** (free tier) | ~5 min (restore from history) |
| VPS snapshot | Daily (3 AM MDT) | Point-in-time VM backup | **$0** (included) | ~30 min (restore VM) |
| Pre-update snapshot | Before OpenClaw upgrade (Sun 2 AM) | Capture state before changes | **$0** | ~5 min (Git rollback) |
| Post-update healthcheck | After updates (manual trigger) | Verify all systems operational (21 tests) | **$0** | ~10 min (diagnosis) |

**Example backup cron (Layer 2 Unified):**

```bash
# Cron: 4:20 AM MDT daily
# Task: Unified backup combining multiple backup operations

Steps:
1. git add -A
2. git commit -m "Daily snapshot: $(date)"
3. git push origin main
4. (Optional) curl Hostinger VPS API → create snapshot
5. Log results to memory/daily/$(date).md

Result: Memory version-controlled + point-in-time VM snapshot
```

**Recovery procedures:**

1. **Memory corrupted** → restore from Git:
   ```bash
   git log --oneline     # Find last good commit
   git reset --hard <commit>  # Restore
   ```

2. **Deployment broken** → restore VPS snapshot:
   ```bash
   # Via Hostinger dashboard or API
   # Rollback to pre-update state
   # Container restarts with clean image
   ```

3. **Update failed** → check post-update healthcheck log:
   ```bash
   cat memory/layer2/post-update-healthcheck.log
   # Identifies which subsystem failed
   # Suggests rollback if needed
   ```

**Cost:** $0 (Git free tier + VPS snapshots included)

---

## Integration: Layer 0.5 + HEARTBEAT

Layer 0.5 is **the operational manifestation of HEARTBEAT**. Rather than manual heartbeat checks, Layer 0.5 runs automatically every 15 minutes and:

1. **Reads HEARTBEAT.md** for standing priorities
2. **Checks career transition status** — flags blocking items
3. **Monitors trading hours** — enables entry/exit at 6am–4pm MDT
4. **Scans subagent lifecycle** — kills idle agents, optimizes models
5. **Tracks time-sensitive items** — reminds before TTL expires
6. **Routes all discoveries to Layer 1** — memory never loses these insights

**Example signals detected by integrated Layer 0.5:**

```
Daily 6:00 AM:
  ✅ "Check job email from Indeed" → memory/heartbeat/job-search.md
  ✅ "Outlier AI shutdown in 33 days" → memory/heartbeat/time-sensitive.md (urgent)

Daily 6:30 AM (trading hours):
  ✅ "BTC up 2% since yesterday" → memory/heartbeat/trading/portfolio.md
  ✅ Check stop/take-profit levels, liquidation risk

Daily 4:20 AM (during backup):
  ✅ Layer 2 runs git backup
  ✅ Captures all daily signals + updates

Every 15 min (Layer 0.5):
  ✅ Read daily logs
  ✅ Detect: corrections, decisions, self-signals
  ✅ Route to appropriate Layer 1 buckets
  ✅ Flag HEARTBEAT priorities
  ✅ Kill idle subagents (>30 min inactivity)
  ✅ Log actions to audit-log.md
```

---

## Migration from Existing Memory

If you already have `MEMORY.md`, `SOUL.md`, or custom memory files:

```bash
chmod +x scripts/migrate-existing-memory.sh

# Dry run (preview changes, no files modified)
./scripts/migrate-existing-memory.sh --dry-run

# Live migration (automatic backup)
./scripts/migrate-existing-memory.sh
```

**What it does:**
1. Creates backup of all existing files → `memory/migration-backup/`
2. Creates Trident directory structure
3. Guides you through file routing (interactive)
4. Installs AGENT-PROMPT.md
5. Generates migration report

**Safety guarantees:**
- Dry-run mode previews all changes
- Originals always backed up (never deleted)
- You approve each routing decision

---

## Security

### Template Integrity

Layer 0.5 reads and executes `memory/layer0/AGENT-PROMPT.md`. A compromised prompt = compromised routing.

**Setup:**
```bash
chmod +x scripts/template-integrity-check.sh
./scripts/template-integrity-check.sh --approve
```

**Before each Layer 0.5 run (optional, adds trust layer):**
```bash
./scripts/template-integrity-check.sh --silent
# Exit 0: clean | Exit 1: tampered (routing halted)
```

**After intentional edits:**
```bash
./scripts/template-integrity-check.sh --approve
```

All integrity events logged to `memory/layer0/audit-log.md`.

### Defense in Depth

- **Sandboxed cron:** Layer 0.5 runs in `isolated` session (no main session access)
- **File scope:** Layer 0.5 only writes to `memory/` subdirectory
- **Audit trail:** Every routing decision logged (memory/layer0/audit-log.md)
- **Network isolation:** Layer 0.5 cron has no external network requirements
- **Backup:** All memory protected by Git + VPS snapshots (Layer 2)
- **Rate limiting:** Layer 0.5 has 15-min minimum interval (prevents spam)

---

## WAL Protocol (Write-Ahead Logging)

**Rule:** Write important facts **before** composing responses.

**Triggers:**
- Corrections: "It's X, not Y"
- Proper nouns: names, places, products
- Preferences: "I like/don't like X"
- Decisions: "Let's do X"
- Specific values: numbers, dates, URLs, prices

**Pattern:**
1. User message arrives
2. Scan for WAL triggers
3. **Write to daily log first**
4. Then compose response

This prevents blank spots where critical context gets lost between Layer 0.5 runs.

---

## Cost

| Profile | Model | Layer 0.5 Interval | Layer 2 (Backup) | Total/day |
|---------|-------|-------------------|------------------|-----------|
| **Zero Budget** | Ollama (local) | 30 min | Git only | **$0** |
| **Budget** | Claude Haiku | 30 min | Git + Git | **$0.72** |
| **Standard (recommended)** | **Claude Haiku** | **15 min** | **Git + VPS** | **$1.44** |
| **Premium** | Claude Sonnet | 15 min | Git + VPS | **$3.12** |

All costs exclude VPS hosting (which you pay anyway). Layer 1, Layer 0, and Layer 2 backup are all **$0**.

See `references/cost-calculator.md` for detailed decision tree.

---

## Implementation Checklist

### Trident Lite + Layer 0.5 + Layer 2

**Phase 1: Core Setup (30 min)**
- [ ] Enable `lossless-claw` plugin in `openclaw.json`
- [ ] Create memory directory structure (memory/daily, memory/self, etc.)
- [ ] Create memory/heartbeat/ subdirectory
- [ ] Populate MEMORY.md with Trident header
- [ ] Copy `scripts/layer0-agent-prompt-template.md` → `memory/layer0/AGENT-PROMPT.md`
- [ ] Customize AGENT-PROMPT.md for your workspace path
- [ ] Run `template-integrity-check.sh --approve`

**Phase 2: Layer 0.5 Cron (15 min)**
- [ ] Create Layer 0.5 cron job (15-min interval, Haiku model)
- [ ] Test Layer 0.5 manually (force-run)
- [ ] Verify signals routing to Layer 1 buckets

**Phase 3: Layer 2 Backup (15 min)**
- [ ] Initialize Git repo: `git init`
- [ ] Create .gitignore (SOUL.md, USER.md, TOKENS_AND_KEYS.md, etc.)
- [ ] Create Layer 2 Unified Backup cron (4:20 AM MDT daily)
- [ ] Create Pre-Update Snapshot cron (Sun 2 AM)
- [ ] Create Post-Update Healthcheck (manual trigger for now)

**Phase 4: HEARTBEAT Integration (10 min)**
- [ ] Review HEARTBEAT.md for standing priorities
- [ ] Ensure Layer 0.5 reads HEARTBEAT.md priorities
- [ ] Populate memory/heartbeat/job-search.md (if applicable)
- [ ] Populate memory/heartbeat/time-sensitive.md with TTL items

### Optional: Semantic Recall (1 hour)

- [ ] Deploy Qdrant (Docker, binary, or cloud)
- [ ] Deploy FalkorDB (optional)
- [ ] Add pre-turn context injection to Layer 0.5
- [ ] Test semantic search queries

---

## Design Principles

1. **Durability over convenience** — SQLite+DAG slower than in-memory, but persistent
2. **Human-readable over compressed** — `.md` files debuggable, diff-able, Git-compatible
3. **Agentic curation over auto-capture** — Layer 0.5 prevents noise accumulation
4. **Deployment-agnostic** — No required cloud services; local-first by default
5. **Personality as first-class** — `memory/self/` is core architecture, not metadata
6. **Security by default** — Template integrity, sandboxed cron, audit logging
7. **Progressive complexity** — Start Lite; upgrade when needed
8. **Resilience first** — Layer 2 ensures recovery from any failure scenario

---

## What This Solves

- **Blank spots** — Layer 0.5 recovers missed signals via Layer 0
- **Session coherence** — LCM + Layer 1 + Layer 0.5 form continuous pipeline
- **Offline resilience** — Ollama can substitute for cloud APIs
- **Identity development** — `memory/self/` supports autonomous personality formation
- **Audit trail** — `.md` files + Git provide complete version history
- **Trust** — Template integrity check prevents prompt injection
- **Disaster recovery** — Layer 2 enables recovery from crashes, corruption, failed updates
- **Time-sensitive tracking** — HEARTBEAT integration ensures critical deadlines never missed

## What This Doesn't Solve

- **Real-time decision making** — 10–30 min lag in Layer 0.5; for sub-second decisions use LCM
- **50K+ message contexts without Semantic Recall** — Add Qdrant/FalkorDB for historical query
- **Private data encryption** — Assumes secure local filesystem; add encryption-at-rest for regulated environments

---

## Further Reading

| File | Purpose |
|---|---|
| **README.md** | Overview, features, getting started |
| **SKILL.md** | This file. Core architecture + checklist |
| `references/trident-lite.md` | **Start here.** Full setup (no Docker) |
| `references/deployment-guide.md` | Semantic Recall (Qdrant/FalkorDB) + Git backup |
| `references/cost-calculator.md` | Model selection, interval tuning, pricing |
| `references/platform-guide.md` | Windows, Mac, Linux, VPS commands |
| `scripts/migrate-existing-memory.sh` | Migrate existing memory files |
| `scripts/template-integrity-check.sh` | Security verification for Layer 0.5 |
| `scripts/layer0-agent-prompt-template.md` | Customizable signal router prompt |

---

## License

**MIT-0** — Free to use, modify, and redistribute. No attribution required.

---

*Like a lobster shell, memory has layers. Make them durable. Make them resilient. Make them yours.*
