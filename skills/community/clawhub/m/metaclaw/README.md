# MetaClaw Skill - Memory Management & Skill Evolution

![Quality: Gold](https://img.shields.io/badge/Quality-Gold-blue.svg)
![Category: memory](https://img.shields.io/badge/Category-memory-green.svg)

**MetaClaw** ist ein generischer Skill für fortgeschrittene Memory-Management-Lösungen mit Hybrid Retrieval, automatischer Memory-Extraktion und PluginEval Integration.

---

## 📋 Overview

Dieser Skill bündelt die besten MetaClaw-Konzepte für generische Memory-Systeme:

| Feature | Beschreibung |
|---------|--------------|
| **Hybrid Retrieval** | Kombiniert semantische Suche (LanceDB) mit FTS/Keyword-Suche |
| **Memory Extraction** | Automatische Extraktion aus Sessions in `preferences.md`, `project-state.md` |
| **Session Counter** | Tracking für konsolidierte Memory-Konsolidation (Trigger: N Sessions) |
| **PluginEval Integration** | Auto-Fix für Quality Badge ≥ Gold (≥85) |
| **Auto-Dream Consolidation** | Automatische Memory-Konsolidierung basierend auf Session-Zähler |

---

## 🚀 Installation

### Vorbereitung

```bash
# VEnv für Dependencies erstellen
cd ~/.openclaw/workspace/skills/metaclaw
python3 -m venv .venv-metaclaw
source .venv-metaclaw/bin/activate
pip install lancedb sentence-transformers
```

### Klonen (ClawHub)

```bash
# Wenn MetaClaw über ClawHub installiert wird
clawhub install metaclaw
```

---

## 💻 Usage

### CLI Interface

#### 1. Hybrid Retrieval (Standard: 0.6 semantic + 0.4 keyword)

```bash
# Semantic Search
python3 skills/metaclaw/scripts/memory-vector-wrapper.py "query" --mode semantic

# Keyword Search (FTS)
python3 skills/metaclaw/scripts/memory-vector-wrapper.py "query" --mode keyword

# Hybrid Search (default)
python3 skills/metaclaw/scripts/memory-vector-wrapper.py "query"
```

#### 2. Memory Extraction

```bash
# Extrahiere aus latest Session
python3 skills/metaclaw/scripts/memory-extract.py

# Extrahiere aus spezifischem Datum
python3 skills/metaclaw/scripts/memory-extract.py --date 2026-04-01

# Test-Run (ohne Schreiben)
python3 skills/metaclaw/scripts/memory-extract.py --dry-run
```

#### 3. Session Counter

```bash
# Increment (in Heartbeat)
scripts/metaclaw/scripts/session-counter.sh --increment

# Get current count
scripts/metaclaw/scripts/session-counter.sh --get

# Reset after Consolidation
scripts/metaclaw/scripts/session-counter.sh --reset

# Check if consolidation should run
scripts/metaclaw/scripts/session-counter.sh --check  # exit 0 = yes
```

#### 4. PluginEval Quality Check

```bash
# Read-Only Check
python3 skills/metaclaw/scripts/skill-eval.py --layer1 skills/metaclaw/

# Anti-Pattern Detection
python3 skills/metaclaw/scripts/skill-eval.py --anti-patterns skills/metaclaw/

# Auto-Fix Preview (Read-Only)
python3 skills/metaclaw/scripts/skill-eval.py --auto-fix skills/metaclaw/

# Auto-Fix (mit Schreiben)
python3 skills/metaclaw/scripts/skill-eval.py --auto-fix --allow-write skills/metaclaw/
```

---

## 📊 Output Formate

### Memory Vector Search (JSON)

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

### Memory Extraction (JSON)

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

---

## ⚙️ Config

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

## 🔁 Auto-Dream Consolidation

### Trigger-Logik

- **Session Counter**: Zählt Sessions (default: 10)
- **Mindestintervall**: 6 Stunden zwischen Consolidations
- **Auto-Detect**: In `memory-digest.sh`

### Cron-Job (Optional)

```bash
# crontab -e
# Tägliche Auto-Dream Consolidation (03:00)
0 3 * * * "$HOME/.openclaw/workspace/skills/metaclaw/scripts/memory-digest.sh" --auto-dream
```

---

## 🔍 Implementation Details

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

## 📁 File Structure

```
skills/metaclaw/
├── SKILL.md              # Hauptdokumentation
├── README.md             # Usage + Installation
├── scripts/
│   ├── memory-vector-wrapper.py   # Hybrid Retrieval
│   ├── memory-extract.py          # Memory Extraction
│   ├── session-counter.sh         # Session Counter
│   ├── memory-digest.sh           # Auto-Dream Consolidation
│   └── skill-eval.py              # PluginEval Integration
└── references/           # Referenzen (optional)
```

---

## 🧪 Testing

### Test Queries

```bash
# Deutsche Begriffe (Keyword-orientiert)
python3 skills/metaclaw/scripts/memory-vector-wrapper.py "Verti Versicherung" --mode keyword

# Hybrid Search (Standard)
python3 skills/metaclaw/scripts/memory-vector-wrapper.py "MetaClaw Integration"
```

### Erwartetes Verhalten

- **"Verti Versicherung"**: Sollte Keyword-Match in `memory/*.md` finden
- **"MetaClaw Integration"**: Sollte semantic-match in `MEMORY.md` finden

---

## 🔧 Troubleshooting

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

## 📈 PluginEval Score

**Ziel: ≥85 (Gold Badge)**

| Dimension | Gewicht | Status |
|-----------|---------|--------|
| Frontmatter Quality | 35% | ✅ |
| Orchestration Wiring | 25% | ✅ |
| Progressive Disclosure | 15% | ✅ |
| Structural Completeness | 10% | ✅ |
| Token Efficiency | 6% | ✅ |
| Ecosystem Coherence | 2% | ✅ |

---

## 🔄 Changelog

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

## 📚 Referenzen

- `~/.openclaw/workspace/skills/memory-vector/` - Original Hybrid Retrieval
- `~/.openclaw/workspace/scripts/memory-extract.py` - Memory Extraction
- `~/.openclaw/workspace/scripts/skill-eval.py` - PluginEval
- `~/.openclaw/workspace/notes/projects/metaclaw-integration.md` - Integration Plan

---

## 👥 Author

**Nova** - OpenClaw AI Assistant

**Category:** `memory`, `automation`  
**Tags:** `#hybrid-retrieval` `#memory` `#skill-evolution` `#plugineval`

---

*Last updated: 2026-04-01*
