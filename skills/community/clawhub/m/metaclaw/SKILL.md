---
name: MetaClaw
description: Generischer Skill für Memory-Management, Hybrid Retrieval und Skill Evolution mit PluginEval Integration
---

# MetaClaw Skill - Memory Management & Skill Evolution

> **Use when:** Memory-Suche mit Hybrid Retrieval (LanceDB + FTS), automatische Memory-Extraktion, PluginEval Quality Checks, oder Skill Evolution. Dieser Skill bündelt die besten MetaClaw-Konzepte für generische Memory-Systeme.

---

## Overview

**MetaClaw** ist ein generischer Skill für fortgeschrittene Memory-Management-Lösungen mit:

- **Hybrid Retrieval** - Kombiniert semantische Suche (LanceDB) mit FTS/Keyword-Suche
- **Memory Extraction** - Automatische Extraktion aus Sessions in preferences.md, project-state.md
- **Session Counter** - Tracking für konsolidierte Memory-Konsolidation (Trigger: N Sessions)
- **PluginEval Integration** - Auto-Fix für Quality Badge ≥ Gold (≥85)
- **Auto-Dream Consolidation** - Automatische Memory-Konsolidierung basierend auf Session-Zähler

---

## Installation

```bash
# VEnv für Dependencies erstellen (wird automatisch verwendet)
cd ~/.openclaw/workspace/skills/metaclaw
python3 -m venv .venv-metaclaw
source .venv-metaclaw/bin/activate
pip install lancedb sentence-transformers
```

---

## Usage

### CLI Interface

```bash
# Hybrid Retrieval (default: 0.6 semantic + 0.4 keyword)
python3 scripts/memory-vector-wrapper.py "query" --mode hybrid

# Semantic Search
python3 scripts/memory-vector-wrapper.py "query" --mode semantic

# Keyword Search (FTS)
python3 scripts/memory-vector-wrapper.py "query" --mode keyword

# Memory Extraction
python3 scripts/memory-extract.py [--date YYYY-MM-DD] [--dry-run]

# Session Counter
./scripts/session-counter.sh --increment
./scripts/session-counter.sh --check  # exit 0 = consolidation ready

# PluginEval Quality Check
python3 scripts/skill-eval.py --layer1 skills/metaclaw/

# Auto-Fix (mit --allow-write zum Schreiben)
python3 scripts/skill-eval.py --auto-fix --allow-write skills/metaclaw/
```

### Output

#### Memory Vector Search (JSON)
```json
{
  "id": "memory/2026-04-01.md",
  "path": "/Users/donmeusi/.openclaw/workspace/memory/2026-04-01.md",
  "snippet": "Extrahierter Inhalt...",
  "date": "2026-04-01",
  "type": "daily",
  "tags": [],
  "score": 0.0,
  "relevance": 0.0,
  "method": "hybrid",
  "combined_score": 0.0
}
```

#### Memory Extraction (JSON)
```json
{
  "extracted": "2026-04-01",
  "type": "project_state",
  "confidence": 0.85,
  "items": [
    {
      "category": "Project",
      "content": "MetaClaw Integration Phase 1",
      "type": "update",
      "source": "session"
    }
  ],
  "preferences": [],
  "project_state": []
}
```

#### Session Counter
```bash
$ ./scripts/session-counter.sh --check
# exit 0: consolidation ready
# exit 1: not ready yet
```

---

## Config

### `memory/config.yaml`

```yaml
# Hybrid Retrieval Settings
retrieval:
  default_mode: "hybrid"  # semantic, keyword, fts, hybrid
  semantic_weight: 0.6    # 0.6 semantic + 0.4 keyword/fts
  default_limit: 5

# Consolidation Settings
consolidation:
  interval_sessions: 10   # alle N Sessions
  min_interval_hours: 6   # min 6h zwischen Consolidations
  max_memory_lines: 200   # Maximum Zeilen in MEMORY.md

# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: "~/.openclaw/workspace/memory/.log"
```

---

## Auto-Dream Consolidation

### Trigger-Logik

- **Session Counter**: Zählt Sessions (default: 10)
- **Mindestintervall**: 6 Stunden zwischen Consolidations
- **Auto-Detect**: In `memory-digest-enhanced.sh`

### Cron-Job (Optional)

```bash
# crontab -e
# Tägliche Auto-Dream Consolidation (03:00)
0 3 * * * "$HOME/.openclaw/workspace/scripts/memory-digest-enhanced.sh" --auto-dream
```

---

## PluginEval Integration

### Quality Check (Layer 1)

```bash
# Read-Only Check
python3 scripts/skill-eval.py --layer1 skills/metaclaw/

# Anti-Pattern Detection
python3 scripts/skill-eval.py --anti-patterns skills/metaclaw/

# Auto-Fix Preview (Read-Only)
python3 scripts/skill-eval.py --auto-fix skills/metaclaw/

# Auto-Fix (mit Schreiben)
python3 scripts/skill-eval.py --auto-fix --allow-write skills/metaclaw/
```

### Quality Targets

- **Gold Badge**: ≥85 Punkte (Ziel)
- **Silver Badge**: ≥70 Punkte
- **Bronze Badge**: ≥60 Punkte

---

## Implementation Details

### Hybrid Retrieval Algorithm

```python
# Combined Score = 0.6 * Semantic + 0.4 * FTS
combined_score = semantic_weight * semantic_relevance + (1 - semantic_weight) * fts_score
```

### Mode Selection

| Mode | Algorithmus | Use Case |
|------|-------------|----------|
| `semantic` | Vector-Suche | Semantische Ähnlichkeit |
| `keyword` | File-Inhalts-Suche | Exakte Begriffe |
| `fts` | LanceDB FTS | Schnelle Keyword-Suche |
| `hybrid` | Kombiniert | Standard (empfohlen) |

---

## Session Counter

### `scripts/session-counter.sh`

Trackt Sessions für konsolidierte Consolidation:

```bash
# Increment on Heartbeat
scripts/session-counter.sh --increment

# Get current count
scripts/session-counter.sh --get

# Reset after Consolidation
scripts/session-counter.sh --reset

# Check if consolidation should run
scripts/session-counter.sh --check  # exit 0 = yes, exit 1 = no
```

---

## Memory Digest

### `scripts/memory-digest-enhanced.sh`

Konsolidiert Memory-Files mit Session-basierter Logik:

```bash
# Normal run (check if consolidation needed)
scripts/memory-digest-enhanced.sh

# Force run (override check)
scripts/memory-digest-enhanced.sh --force

# Dry run (show what would be done)
scripts/memory-digest-enhanced.sh --dry-run

# Auto-dream mode (with consolidation)
scripts/memory-digest-enhanced.sh --auto-dream
```

---

## Integration in OpenClaw

### Heartbeat Integration

Füge folgenden Task zur Heartbeat-Logik hinzu:

```bash
# scripts/heartbeat.sh
"$HOME/.openclaw/workspace/scripts/session-counter.sh" --increment
```

### Cron Integration

```bash
# crontab -e
# Auto-Dream tägliche Consolidation (Optional)
0 3 * * * "$HOME/.openclaw/workspace/scripts/memory-digest-enhanced.sh" --auto-dream
```

---

## Troubleshooting

### Problem: "Dependencies nicht verfügbar"

**Lösung:**
```bash
source .venv-metaclaw/bin/activate
pip install lancedb sentence-transformers numpy
```

### Problem: "Tabelle nicht gefunden"

**Lösung:**
```bash
python3 skills/metaclaw/scripts/memory_vector_init.py
```

### Problem: Session-Counter füllt sich nicht auf

**Lösung:**
```bash
./scripts/session-counter.sh --status
# Prüfe ob --increment in Heartbeat aufgerufen wird
```

---

## Changelog

### Version 1.0.0 (2026-04-01)

**Added:**
- Generischer MetaClaw Skill für ClawHub
- Hybrid Retrieval (semantic + FTS)
- Memory Extraction Pipeline
- PluginEval Integration
- Session Counter für konsolidierte Consolidation
- Memory Digest mit Session-basierter Logik

**Changed:**
- Default Mode: `hybrid` (statt `semantic`)
- Score-Kombination: `0.6 * semantic + 0.4 * keyword`

**Removed:**
- Keine Breaking Changes (Backwards compatible)

---

## Referenzen

- `~/.openclaw/workspace/skills/memory-vector/` - Original Hybrid Retrieval
- `~/.openclaw/workspace/scripts/memory-extract.py` - Memory Extraction
- `~/.openclaw/workspace/scripts/skill-eval.py` - PluginEval
- `~/.openclaw/workspace/notes/projects/metaclaw-integration.md` - Integration Plan

---

*Last updated: 2026-04-01*
*Category: automation, memory*
*Tags: #hybrid-retrieval #memory #skill-evolution #plugineval*
