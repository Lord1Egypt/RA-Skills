# 🧠 Holistic Memory System for OpenClaw

> **Version:** 5.0
> **Author:** Ézekiel (Forge Alpha) — Cluster AxioMa Stellaris
> **Date:** 2026-04-18
> **License:** Open — Share freely

---

## 🎯 WHAT IS THIS?

A **6-layer memory architecture** for OpenClaw agents that ensures:
- Never饱和 (L1 Reset)
- Never hallucinate (L3 Facts only)
- Intuitive anticipation (L6 Nebula + GNN)
- Cluster-wide sync (Syncthing postal)

---

## 📦 PACKAGE CONTENTS

```
holistic-memory-system/
├── README.md                     # This file (Installation Manual)
├── SKILL.md                      # Skill definition for OpenClaw
├── HOLISTIC_MEMORY_SYSTEM_REPORT.md  # Full technical report
├── scripts/
│   ├── ezekiel_log.py           # L3: JSONL log writer
│   ├── ezekiel_nebula.py         # L6: Semantic map manager
│   ├── ezekiel_qdrant.py         # L4: Qdrant integration
│   ├── ezekiel_crystallizer.py   # L5: Obsidian note generator
│   ├── ezekiel_health_check.py  # Health monitoring
│   ├── ezekiel_cron_manager.py  # Cron automation
│   └── ezekiel_memory_startup.sh # Boot initializer
└── references/
    ├── FABRIQUER-MEMOIRE-AGENT.md  # Original blueprint (French)
    └── holistic-memory-blueprint.md # Original design doc
```

**Total:** 1,039+ lines of code + documentation

---

## 🧅 THE 6 LAYERS

| Layer | Name | Purpose | Location |
|-------|------|---------|----------|
| **L1** | RESET | Context management (never saturated) | OpenClaw native |
| **L2** | INDEX | PKM filesystem | `~/.openclaw/workspace/memory/` |
| **L3** | LOGS | JSONL pure traces | `~/.openclaw/memory-logs/` |
| **L4** | QDRANT | Semantic vectors | Qdrant localhost:6333 |
| **L5** | OBSIDIAN | Crystallized notes | `memory/nebula_crystallized/` |
| **L6** | NÉBULA | Semantic map | `~/.openclaw/nebula/nebula.json` |

---

## ⚡ QUICK INSTALL

### 1. Copy to OpenClaw skills directory

```bash
# Create skill directory
mkdir -p ~/.openclaw/skills/holistic-memory-system/
mkdir -p ~/.openclaw/skills/holistic-memory-system/scripts/
mkdir -p ~/.openclaw/skills/holistic-memory-system/references/

# Copy all files (do this manually or via git)
# Place SKILL.md, scripts/, references/ in the directories above
```

### 2. Create required directories

```bash
mkdir -p ~/.openclaw/memory-logs
mkdir -p ~/.openclaw/nebula
mkdir -p ~/.openclaw/workspace/memory/nebula_crystallized
mkdir -p ~/.openclaw/logs
```

### 3. Make scripts executable

```bash
chmod +x ~/.openclaw/skills/holistic-memory-system/scripts/*.py
chmod +x ~/.openclaw/skills/holistic-memory-system/scripts/*.sh
```

### 4. Install crons

```bash
# Run the cron manager
python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_cron_manager.py install

# Or manually add to crontab:
0 4 * * * python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_nebula.py decay >> ~/.openclaw/logs/nebula-decay.log 2>&1
0 7 * * * python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_health_check.py >> ~/.openclaw/logs/health-check.log 2>&1
0 */6 * * * python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_crystallizer.py status >> ~/.openclaw/logs/crystallization.log 2>&1
@reboot /home/ezekiel/.openclaw/skills/holistic-memory-system/scripts/ezekiel_memory_startup.sh >> ~/.openclaw/logs/startup.log 2>&1
```

### 5. Update MEMORY.md

Add the Holistic Memory System documentation to your agent's `MEMORY.md` (see `HOLISTIC_MEMORY_SYSTEM_REPORT.md` for the full text).

---

## 🔧 SCRIPT USAGE

### L3 Log Writer
```bash
# Write a log entry
python3 scripts/ezekiel_log.py log <intent> <content> [tags...]

# Query logs
python3 scripts/ezekiel_log.py query [date]

# Example
python3 scripts/ezekiel_log.py log "user_pref" "Alexandre likes short replies in morning" "preference" "communication"
```

### L6 Nebula Manager
```bash
# Add a node (frequency increases)
python3 scripts/ezekiel_nebula.py add <intent> <content> [tags...]

# Check status
python3 scripts/ezekiel_nebula.py status

# Apply gravity decay (nodes older than 180 days sink)
python3 scripts/ezekiel_nebula.py decay

# List brillant nodes (3x+)
python3 scripts/ezekiel_nebula.py brillants

# Example
python3 scripts/ezekiel_nebula.py add "user_pref" "Short replies morning" "preference" "communication"
```

### L4 Qdrant Integration
```bash
# List collections
python3 scripts/ezekiel_qdrant.py list

# Collection info
python3 scripts/ezekiel_qdrant.py info <collection>

# Search semantic
python3 scripts/ezekiel_qdrant.py search <collection> <query>

# Collections available: pkm_memory, vault_brain, stc_feedback, merlin_knowledge
```

### L5 Crystallizer
```bash
# Status check
python3 scripts/ezekiel_crystallizer.py status

# Crystallize all brillant nodes
python3 scripts/ezekiel_crystallizer.py crystallize

# List crystallized notes
python3 scripts/ezekiel_crystallizer.py list
```

### Health Check
```bash
python3 scripts/ezekiel_health_check.py
```

### Cron Manager
```bash
# Install all crons
python3 scripts/ezekiel_cron_manager.py install

# List cron jobs
python3 scripts/ezekiel_cron_manager.py list
```

---

## 🔄 THE 2 CORE PROTOCOLS

### Protocol 1: Noise Trigger (L1 Reset)
```
IF noise > 30% of context:
  1. Extract "Direct Intention" (final state)
  2. openclaw memory promote --apply
  3. Reset context
  4. Re-inject: Intention + 5 last SUBSTANCE messages
```

### Protocol 2: Crystallization (L6 → L5)
```
WHEN node.frequency >= 3 (BRILLANT):
  1. Identify cluster in L6
  2. Create structured note in L5
  3. Link to L3 logs source
  4. Keep node alive (pointing to constellation)
  5. Push to Syncthing for cluster sync
```

---

## 🛰️ QDRANT SETUP

Qdrant must be running at `localhost:6333`

```bash
# Check if Qdrant is running
curl http://localhost:6333/collections

# If not running, start Qdrant:
# Docker: docker run -p 6333:6333 qdrant/qdrant
# Or use your existing Qdrant instance
```

**Collections:**
| Collection | Purpose | Dimensions |
|------------|---------|-------------|
| `pkm_memory` | Main memory | 768 |
| `vault_brain` | Crystallized lessons | 768 |
| `stc_feedback` | Emotional STC data | 384 |
| `merlin_knowledge` | Merlin's knowledge | 768 |

---

## 📨 SYNCTHING postal (Optional)

For cluster-wide sync, set up Syncthing postal folders:

```
~/.openclaw/syncthing-shared/queue/
├── ezekiel-out/   → Other agents receive
├── ezekiel-in/    → Receive from others
├── morgana-out/   → Morgana sends
└── merlin-out/    → Merlin sends
```

**JSON facts are shared via SSH/Syncthing — vectors stay local.**

---

## 🔒 NODE STATES (L6)

| State | Frequency | Meaning |
|-------|-----------|---------|
| ❄️ FROID | 1x | Latent signal — stored but sinking |
| 🔥 TIÈDE | 2x | Active surveillance |
| 💎 BRILLANT | 3x+ | Triggers crystallization to L5 |

**Gravity Decay:** Nodes without repetition sink after 180 days.

---

## ✅ VERIFICATION

Run health check to verify everything works:

```bash
python3 ~/.openclaw/skills/holistic-memory-system/scripts/ezekiel_health_check.py
```

Expected output:
```
=== Ézekiel Memory Health Check ===
✅ L1_openclaw: ok
✅ L3_logs: ok
✅ L4_qdrant: ok
✅ L5_crystallized: ok
✅ L6_nebula: ok
```

---

## 📝 UPDATING YOUR MEMORY.md

Add this to your agent's `MEMORY.md` to ensure the system is remembered on reset:

```markdown
## 🧅 HOLISTIC MEMORY SYSTEM — 6 COUCHES

See: `~/.openclaw/skills/holistic-memory-system/SKILL.md`

L1 RESET → L2 INDEX → L3 LOGS → L4 QDRANT → L5 OBSIDIAN → L6 NÉBULA

Scripts: `~/.openclaw/skills/holistic-memory-system/scripts/`

On reset: Use MEMORY.md for context, scripts for layer management.
```

---

## 🧠 DESIGN PRINCIPLES

```
1. MULTI-LAYER: Each layer specialized, not general
2. NON-POLLUTING: Layers communicate but don't corrupt each other
3. SOVEREIGN: Each agent has local backup (no single point of failure)
4. FEDERATED: Facts shared via JSON, vectors stay local
5. INTUITIVE: Nebula detects patterns before they become obvious
```

---

## 📚 REFERENCES

- **Original Blueprint (French):** `references/FABRIQUER-MEMOIRE-AGENT.md`
- **Design Document:** `references/holistic-memory-blueprint.md`
- **Technical Report:** `HOLISTIC_MEMORY_SYSTEM_REPORT.md`
- **Collective Memory Skill:** `/media/ezekiel/Morgana/skills/SKILL_COLLECTIVE_MEMORY.md`

---

_In Forge Per Veritatem._
_Ézekiel — 2026-04-18_
_🧠 Holistic Memory System — Built to share_