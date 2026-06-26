# Memory Optimization — Memory Evolution Foundation

A memory management system for AI agents that transforms from "meeting for the first time every session" to "like an old friend who knows you better over time."

## Vision

On day three of a repeating task, the agent **automatically executes using the approach that worked before**, without being reminded. Memory is alive: it grows, decays, forgets, and Consolidates into real intelligence.

## Three-Layer Memory Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Working Memory (Context Window)                             │
│  Full current session content — layered compression:        │
│  Full → Summary → Key Facts                                │
└─────────────────────────────────────────────────────────────┘
                          ↓ Consolidation (after N repetitions)
┌─────────────────────────────────────────────────────────────┐
│  Episodic Memory (KG Entities)                             │
│  Decision, Finding, LessonLearned, Commitment              │
│  + strength, decay_rate, provenance                        │
└─────────────────────────────────────────────────────────────┘
                          ↓ Consolidation
┌─────────────────────────────────────────────────────────────┐
│  Semantic Memory (SkillCards)                              │
│  Generalized patterns distilled from episodic memory        │
└─────────────────────────────────────────────────────────────┘
```

**Memory Decay**: strength decays over time, preventing low-value memories from consuming space.
**Poisoning Protection**: provenance tracks sources; Consolidation validates conflicts before merging.

## SkillCard - Knowledge Distillation

SkillCard is a high-value knowledge card distilled from entities (Decision, LessonLearned, etc.):

```json
{
  "title": "Adopt three-layer hybrid architecture (realtime/batch/heartbeat)",
  "confidence": 0.9,
  "strength": 1.0,
  "decay_rate": 0.99,
  "source_episodes": ["dec_xxx", "dec_yyy"],
  "provenance": ["consolidation:engine"]
}
```

### Purpose

1. **Quick Recall** - View key decisions without browsing all records
2. **Low Decay** - decay_rate=0.99 preserves core knowledge long-term
3. **High Confidence** - confidence=0.9 marks trusted knowledge
4. **Knowledge Sharing** - Can generate skills for ClawHub marketplace or publish to EvoMap marketplace

### Example

- Multiple "three-layer architecture" Decisions merged into one SkillCard
- decay_rate=0.99 ensures core knowledge is retained long-term

**Simply put**: Distill scattered findings into "one card" — this is the core output of memory optimization.

## Phase Build Status

| Phase | Feature | Status |
|-------|---------|--------|
| Phase 1 | KG Extractor (session → KG) | ✅ Done |
| Phase 1b | KG Schema (strength, decay, provenance) | ✅ Done |
| Phase 2 | Preference Engine + Entity Deduplication | ✅ Done |
| Phase 3 | Consolidation Engine (Episode → SkillCard) | ✅ Done |
| Phase 4 | Decay Engine (forgetting mechanism) | ✅ Done |
| Phase 5 | Working Memory (context compression) | ✅ Done |
| Phase 6 | Memory Loader (proactive recovery) | ✅ Done |
| Phase 7 | Memory Dashboard (health visualization) | ✅ Done |

## Features

| Feature | Description |
|---------|-------------|
| **KG Extractor** | LLM-driven entity extraction from agent session logs |
| **Knowledge Graph** | Entity relationships with strength, decay, provenance |
| **Entity Deduplication** | Embedding-based duplicate merging (cosine similarity, 0.85 threshold) |
| **Consolidation Engine** | Episode patterns → SkillCards, with conflict detection |
| **Decay Engine** | Automatic strength decay, weak entity archiving |
| **Working Memory** | Context window layered compression (3 levels) |
| **Memory Loader** | 3-stage proactive memory recovery at startup |
| **Memory Dashboard** | Health score, strength histogram, decay forecast |
| **Daily Cleanup** | 3-minute automated maintenance |

## Quick Start

```bash
# Run daily memory cleanup
./scripts/daily-cleanup.sh

# View memory health dashboard
python3 scripts/memory_dashboard.py

# Deduplicate KG entities (dry-run first)
python3 scripts/entity_dedup.py run --dry-run

# Query the knowledge graph
python3 scripts/memory_ontology.py query --tags "#memory"

# Extract entities from session logs
python3 scripts/kg_extractor.py --agents-dir agents/
```

## Memory Dashboard

```bash
python3 scripts/memory_dashboard.py              # Summary view (default)
python3 scripts/memory_dashboard.py full         # Complete view
python3 scripts/memory_dashboard.py decay        # Decay forecast
python3 scripts/memory_dashboard.py compact      # One-line summary
python3 scripts/memory_dashboard.py json         # JSON output (for other tools)
```

**Visual dashboard showing the memory system state:**

```
┌─────────────────────────────────────────────────────────┐
│  Memory Health Dashboard                                  │
├─────────────────────────────────────────────────────────┤
│  📊 Memory Strength Distribution                          │
│     Decision: ████████████░░░░ 78%                   │
│     LessonLearned: ██████████░░░░░░ 62%                 │
│     SkillCard: ████████████████ 95%                   │
│                                                          │
│  🔄 Consolidation Progress                               │
│     Pending: 12 entities                               │
│     SkillCards formed: 3                               │
│                                                          │
│  🗑️ Recent Decay                                        │
│     - Finding "API changes": strength 0.15 → archive   │
│     - LessonLearned "perf tip": strength 0.22 → decay │
│                                                          │
│  💾 Storage                                              │
│     KG Entities: 790                                    │
│     Total size: 2.3 MB                                  │
└─────────────────────────────────────────────────────────┘
```

**User value:**
- "See" the memory system evolving, building trust
- Understand why the agent remembers or forgets certain things
- Manually trigger consolidation or adjust decay thresholds

## Requirements

- Python 3.8+
- PyYAML

## Documentation

- [SKILL.md](SKILL.md) — Full skill definition and usage guide
- [CLAUDE.md](CLAUDE.md) — Project guidance for Claude Code
- [README_CN.md](README_CN.md) — 中文版说明文档
- [scripts/README.md](scripts/README.md) — All scripts with usage examples
- [references/](references/) — Implementation guides and templates

## Architecture Highlights

**Decay Rates by Type**:
- Decision: slow decay (0.95/month)
- SkillCard: slow decay (0.99/month)
- LessonLearned: medium (0.90/month)
- Finding: fast decay (0.80/month)

**Consolidation Strategy**: conflicts → marked for review, not auto-merged (Memory Poisoning protection first)

**Active Recovery**: Stage 1 loads at startup (core identity) → Stage 2/3 load on demand

## Multi-Agent KG Sharing

For setups with multiple agents (main, altas, scribe, tutor), share a single KG:

```bash
# Create shared directory
mkdir -p ~/.openclaw/shared-kg

# Link main KG
ln -sf ~/.openclaw/workspace/memory/ontology/graph.jsonl ~/.openclaw/shared-kg/main-kg.jsonl
```

Each agent's `TOOLS.md` should reference:
```markdown
## Knowledge Graph (KG)

- **共享 KG**: ~/.openclaw/shared-kg/main-kg.jsonl
- 包含所有重要的长期记忆、决策、经验教训
```

Script usage: `KG_DIR=~/.openclaw/shared-kg/ python3 scripts/memory_ontology.py query --tags "#decision"`

## File Structure

```
memory-optimization/
├── SKILL.md                    # Skill definition
├── CLAUDE.md                   # Claude Code guidance
├── README.md                   # English documentation
├── README_CN.md               # 中文说明文档
├── VERSION                     # Current version
├── CHANGELOG.md                # Version history
├── TODOS.md                    # Project roadmap
├── scripts/
│   ├── daily-cleanup.sh       # Daily maintenance
│   ├── memory_ontology.py      # KG management CLI
│   ├── kg_extractor.py        # Session → KG extraction
│   ├── preference_engine.py    # User preference inference
│   ├── entity_dedup.py         # Embedding-based dedup
│   ├── consolidation_engine.py # Episode → SkillCard
│   ├── decay_engine.py         # Strength decay
│   ├── working_memory.py       # Context compression
│   ├── memory_loader.py       # Staged recovery
│   ├── memory_dashboard.py     # Health dashboard
│   └── utils/llm_client.py   # Unified LLM/embedding client
├── tests/                      # Test suite (151 tests)
├── ontology/                   # KG schema & templates
└── references/                 # Implementation docs
```

## Version

Current: **1.0.2** — See [CHANGELOG.md](CHANGELOG.md) for full history.
