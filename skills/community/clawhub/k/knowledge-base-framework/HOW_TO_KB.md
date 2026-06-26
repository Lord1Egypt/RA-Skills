# HOW_TO_KB.md – Knowledge Base Framework

**Letzte Änderung:** 2026-04-16  
** Zielgruppe:** Entwickler

---

## 1. Übersicht

Das KB Framework ist ein semantischer Dokumentenindex mit Hybrid Search.

| Komponente | Technologie |
|------------|-------------|
| Datenbank | SQLite (WAL Mode) |
| Vector Store | ChromaDB |
| Embedding Modell | `all-MiniLM-L6-v2` (384 Dimensionen) |
| Suchmethode | Hybrid: 60% Semantic + 40% Keyword |
| Indexierung | Markdown-Header-basiert |

**Architektur-Prinzip:** Delta-Indexierung via `file_hash` (MD5). Nur geänderte Dateien werden neuindexiert.

---

## 2. Quick Start

### Installation

```bash
# Bereits installiert in ~/.openclaw/kb/
# CLI verfügbar via:
cd ~/projects/kb-framework && ./kb.sh --help

# Oder direkt:
python -m kb --help
```

### Erste Schritte

```bash
# 1. Verzeichnis indexieren
kb index ~/knowledge/library --recursive

# 2. ChromaDB synchen (nach Indexierung)
kb sync --stats

# 3. Erstes Query
kb search "Python async patterns"

# 4. Audit machen
kb audit --verbose
```

---

## 3. Architektur

### 3.1 Datenbank-Layer (SQLite)

**Pfad:** `~/.openclaw/kb/knowledge.db`

**Kerntabellen:**

| Tabelle | Zweck |
|---------|-------|
| `files` | Datei-Metadaten (1:1 pro Datei) |
| `file_sections` | Header-basierte Sections (1:N pro Datei) |
| `embeddings` | ChromaDB-Sync-Tracking |

**Änderungsdetection:**

```python
file_hash = md5(file.read_bytes())
# Bei Hash-Änderung → Section löschen + neu einfügen
```

### 3.2 ChromaDB-Integration

**Pfad:** `~/.openclaw/kb/chroma_db/`

```python
# Lazy Loading beim ersten Zugriff
from kb.framework import ChromaIntegration
chroma = ChromaIntegration()
collection = chroma.sections_collection  # "kb_sections"
```

**Collection-Struktur:**

```python
{
    "ids": ["uuid-section-id"],
    "embeddings": [[0.123, -0.456, ...]],  # 384-dim
    "metadatas": [{
        "file_id": "uuid",
        "file_path": "/path/to/file.md",
        "section_header": "Header",
        "importance_score": 0.75
    }],
    "documents": ["Header | Content Preview"]  # max 2000 chars
}
```

### 3.3 Hybrid Search

```
Query
  ├─→ ChromaDB Semantic Search (60%)
  │     └─→ collection.query() → cosine distance
  └─→ SQLite LIKE Keyword Search (40%)
        └─→ content_full LIKE '%term%'
  └─→ Merge & Rank
        └─→ normalized_scores × weights
        └─→ importance_boost × combined_score
```

**Fallback:** Wenn ChromaDB nicht verfügbar ist (Collection leer, Import-Fehler, Cold Start), fällt `HybridSearch` automatisch auf reine Keyword-Suche (SQLite LIKE) zurück. Der User sieht eine Warnung im `--debug`-Modus, Ergebnisse werden trotzdem geliefert – nur ohne semantische Komponente.

**Fallback-Kette:**

```
1. Hybrid (Semantic + Keyword) → Score: 0.6×semantic + 0.4×keyword
2. Semantic-Only              → Score: semantic direkt
3. Keyword-Only               → Score: keyword direkt
4. Fallback (ChromaDB down)   → Score: keyword, Warnung im debug
```

---

## 4. Commands

| Command | Beschreibung |
|---------|-------------|
| `kb index` | Dateien/Verzeichnisse in SQLite indexieren |
| `kb search` | Hybrid Search (Semantic + Keyword) |
| `kb sync` | ChromaDB mit SQLite synchronisieren |
| `kb audit` | Integritäts- und Konsistenzcheck |
| `kb ghost` | Neue/verwaiste Dateien finden |
| `kb warmup` | Embedding-Model vorladen |
| `kb llm engine status` | Status aller Engines anzeigen |
| `kb llm engine switch` | Engine wechseln (ollama/huggingface/auto/compare) |
| `kb llm engine test` | Beide Engines testen |

### 4.1 `kb index` – Indexieren

```bash
# Einzelne Datei
kb index ~/notes/meeting.md

# Verzeichnis rekursiv
kb index ~/knowledge/library --recursive

# Force-Reindex (auch bei unchanged hash)
kb index ~/notes/todo.md --force
```

**Return Codes:** 0 = Erfolg, 1 = Fehler

### 4.2 `kb search` – Suchen

```bash
# Standard Query
kb search "async await patterns"

# Mehr Results
kb search "database migrations" --limit 50

# Nur Semantic (ohne Keyword)
kb search "machine learning" --semantic-only

# Detailliertes Format
kb search "authentication" --format full
```

**Output (short):**
```
📄 auth.md:45 [0.87] JWT Token Validation
📄 oauth.md:120 [0.72] OAuth2 Flow
```

---

## 4a. kb search Beispiele

### Einfache Suche

```bash
kb search "singleton pattern"
```

```
📄 kb/base/config.py:42 [0.89] class KBConfig:
📄 kb/base/command.py:15 [0.76] BaseCommand ABC
```

### Mit Flags

```bash
# Nur Keyword-Suche (schnell, exakt)
kb search "MTHFR" --limit 5 --keyword-only

# Nur Semantic-Suche (natürliche Sprache)
kb search "health" --semantic-only --file-type md

# Mehr Results
kb search "async patterns" --limit 50

# Detailliertes Output
kb search "authentication" --format full
```

### Filter

```bash
# Zeitraum
kb search "nutrition" --date-from 2024-01-01 --date-to 2024-12-31

# Dateityp
kb search "meeting notes" --file-type md,pdf

# Debug-Info (Scores, Quellen)
kb search "workflow" --debug
```

### Kombiniert

```bash
# Keyword + Dateityp + Zeitraum + Limit
kb search "project plan" --keyword-only --file-type md --date-from 2025-06-01 --limit 10
```

### 4.3 `kb sync` – ChromaDB Sync

```bash
# Statistiken anzeigen
kb sync --stats

# Dry-Run (was würde passieren)
kb sync --dry-run

# Delta-Sync (nur fehlende) – Default
kb sync --delta

# Mit Cleanup verwaister Einträge
kb sync --delete-orphans

# Einzelne Datei synchen
kb sync --file-id <UUID>

# Batch-Size anpassen
kb sync --batch-size 64
```

### 4.4 `kb audit` – Integritätscheck

```bash
# Voller Audit mit Details
kb audit --verbose

# Ohne ChromaDB-Check (schneller)
kb audit --skip-chroma

# CSV-Export
kb audit --export-csv issues.csv

# Bestimmte Checks
kb audit --checks db_integrity,library_paths
```

**Checks:** `db_integrity`, `schema`, `library_paths`, `null_paths`, `embeddings_table`, `chroma_sync`, `orphaned_entries`

### 4.5 `kb ghost` – Neue Dateien finden

```bash
# Scan mit Defaults
kb ghost --scan-dirs ~/knowledge/library

# Nur PDFs und Textdateien
kb ghost --extensions .pdf,.txt,.md

# Dry-Run
kb ghost --scan-dirs ~/downloads --dry-run

# JSON Output für Scripting
kb ghost --scan-dirs ~/docs --json-output

# Größenfilter
kb ghost --min-size 1024 --max-size 104857600

# Bestimmte Verzeichnisse ausschließen
kb ghost --exclude-dirs node_modules,.git,temp
```

### 4.6 `kb warmup` – Model vorladen

```bash
# Model in RAM laden (braucht ~8s beim ersten Mal)
kb warmup

# Mit Memory-Check
kb warmup --verbose

# Bestimmtes Model
kb warmup --model all-MiniLM-L6-v2

# Check ob bereits geladen
kb warmup --check
```

### 4.7 `kb llm engine` – Engine Management

**Neu in 1.1.1** – Zentrale Registry für LLM-Engines.

```bash
# Status aller Engines anzeigen
kb llm engine status

# Verfügbare Engines auflisten
kb llm engine list

# Detaillierte Info zu einer Engine
kb llm engine info ollama
kb llm engine info huggingface

# Engine wechseln
kb llm engine switch huggingface   # HuggingFace Transformers
kb llm engine switch ollama        # Ollama API
kb llm engine switch auto          # Auto: HF primary, Ollama fallback
kb llm engine switch compare      # Compare: Beide Engines nebeneinander

# Beide Engines testen
kb llm engine test
```

**model_source Optionen:**

| Mode | Verhalten |
|------|----------|
| `ollama` | Nur OllamaEngine (externe Ollama-Instanz) |
| `huggingface` | Nur TransformersEngine (lokales Modell) |
| `auto` | HF primary + Ollama fallback |
| `compare` | Beide Engines für Diff/Merge |

**Config-Keys (Neu in 1.1.1):**

| Key | Default | Beschreibung |
|-----|---------|-------------|
| `model_source` | `auto` | Engine-Auswahl |
| `ollama_model` | `gemma4:e2b` | Ollama-Modell |
| `ollama_timeout` | `120` | Timeout in Sekunden |
| `ollama_temperature` | `0.7` | Temperature (0-2) |
| `parallel_mode` | `False` | Parallel-Ausführung |
| `parallel_strategy` | `primary_first` | `primary_first`, `aggregate` oder `compare` |

---

## 5. Python API

### 5.1 Hybrid Search

```python
from kb.framework import HybridSearch
from kb.base.config import KBConfig

config = KBConfig()
searcher = HybridSearch(config.db_path, config.chroma_path)

results = searcher.search(
    query="async await patterns",
    limit=20,
    semantic_only=False,  # Hybrid-Search
    keyword_only=False
)

for r in results:
    print(f"{r.section_header} [Score: {r.combined_score:.2f}]")
    print(f"  → {r.file_path}:{r.line_start}")
```

### 5.2 Indexierung

```python
from kb.indexer import BiblioIndexer
from pathlib import Path

indexer = BiblioIndexer("~/.openclaw/kb/knowledge.db")
with indexer:
    result = indexer.index_file(Path("~/notes/meeting.md"))
    print(f"Indexed {result['sections']} sections")
```

### 5.3 ChromaDB Direct Access

```python
from kb.framework import ChromaIntegration

chroma = ChromaIntegration()
collection = chroma.sections_collection

# Direkte Query
results = collection.query(
    query_texts=["Python decorators"],
    n_results=10,
    include=["metadatas", "distances"]
)

for i, section_id in enumerate(results['ids'][0]):
    distance = results['distances'][0][i]
    similarity = max(0.0, 1.0 - distance)
    print(f"Match: {results['metadatas'][0][i]['section_header']} ({similarity:.2f})")
```

### 5.4 LLM Engine API

**Neu in 1.1.1** – EngineRegistry und Multi-Engine Support.

```python
from kb.biblio import LLMConfig, EngineRegistry, create_engine

# Config via Singleton
config = LLMConfig.get_instance()
print(f"Source: {config.model_source}")
print(f"HF Model: {config.hf_model_name}")
print(f"Ollama Model: {config.ollama_model}")

# EngineRegistry Singleton
registry = EngineRegistry.get_instance(config)

# Primary Engine (auto: HF, compare: HF, single: respective)
primary = registry.get_primary()
print(f"Primary: {primary.get_provider().value}")

# Secondary (nur bei auto/compare)
secondary = registry.get_secondary()
if secondary:
    print(f"Secondary: {secondary.get_provider().value}")

# Status
status = registry.status()
print(status)

# Engine wechseln
from kb.biblio.engine.registry import EngineRegistry as ER
ER.reset()  # Cache leeren

# Neue Config mit anderem Source
config2 = LLMConfig(model_source="ollama")
registry2 = EngineRegistry.get_instance(config2)
```

**Generator Parallel Support:**

```python
from kb.biblio.generator import EssenzGenerator

# primary_first: HF zuerst, bei Fehler Ollama
# aggregate: Beide, Ergebnisse zusammenführen
# compare: Beide, Unterschiede anzeigen
generator = EssenzGenerator()
result = await generator.generate_essence(
    topic="Vitamin D",
    parallel_strategy="primary_first"  # oder "aggregate", "compare"
)
```

**Config Keys direkt setzen:**

```python
from kb.biblio.config import LLMConfig

# Environment Variable
# KB_LLM_MODEL_SOURCE=auto
# KB_LLM_OLLAMA_MODEL=gemma4:e2b
# KB_LLM_PARALLEL_MODE=true
# KB_LLM_PARALLEL_STRATEGY=compare

config = LLMConfig(
    model_source="auto",
    parallel_mode=True,
    parallel_strategy="compare"
)
```

---

## 6. Troubleshooting

### ChromaDB Connection Failed

```bash
# Prüfe ob Verzeichnis existiert
ls -la ~/.openclaw/kb/chroma_db/

# Repair permissions
chmod 755 ~/.openclaw/kb/chroma_db/

# Full Re-Sync
kb sync --full
```

### Search Quality Issues

```bash
# Sync-Status prüfen
kb sync --stats

# Fehlende nachsynchen
kb sync --delta

# Embeddings-Tabelle checken
kb audit --checks embeddings_table,chroma_sync
```

### langsame erste Query (Cold Start)

```bash
# Model vorladen
kb warmup --verbose

# Prüfe Memory
free -m | grep MemAvailable

# Minimum: 500MB
```

### Ghost findet keine Dateien

```bash
# Dry-Run für Debugging
kb ghost --scan-dirs ~/documents --dry-run --verbose

# Extensions prüfen
kb ghost --extensions .pdf,.md,.txt

# Verzeichnis ausschließen
kb ghost --exclude-dirs .git,node_modules,temp
```

### Delta-Indexierung funktioniert nicht

```bash
# Force-Reindex
kb index ~/path/to/file.md --force

# Audit prüft Hash-Mismatch
kb audit --verbose
```

### Ollama Engine nicht erreichbar

```bash
# Prüfe ob Ollama läuft
ollama list

# Prüfe spezifisches Modell
ollama run gemma4:e2b "test"

# Engine-Status anzeigen
kb llm engine status

# Falls Ollama down: auf HuggingFace umschalten
kb llm engine switch huggingface

# Auto-Modus (HF primary, Ollama Fallback)
kb llm engine switch auto
```

### HuggingFace Transformers Fehler

```bash
# Prüfe ob PyTorch/Transformers installiert
python -c "import torch; print(torch.__version__)"
python -c "import transformers; print(transformers.__version__)"

# Prüfe CUDA-Verfügbarkeit
python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"

# Prüfe GPU-Speicher
nvidia-smi

# Mit 4-bit Quantization laden (weniger RAM)
# Setze KB_LLM_HF_QUANTIZATION=4bit
export KB_LLM_HF_QUANTIZATION=4bit
kb llm engine switch huggingface

# Mit 8-bit Quantization
export KB_LLM_HF_QUANTIZATION=8bit
kb llm engine switch huggingface
```

### Engine-Wechsel funktioniert nicht

```bash
# Aktuelle Config anzeigen
kb llm config show

# Singleton zurücksetzen (Python)
from kb.biblio.config import LLMConfig
from kb.biblio.engine.registry import EngineRegistry
LLMConfig.reset()
EngineRegistry.reset()

# Neu erstellen
config = LLMConfig(model_source="auto", hf_model_name="google/gemma-2-2b-it")
registry = EngineRegistry(config=config)
```

### Parallel-Modus Probleme

```bash
# Prüfe ob beide Engines verfügbar
kb llm engine status

# Beide Engines testen
kb llm engine test

# Falls nur eine Engine verfügbar: primary_first als Fallback
export KB_LLM_PARALLEL_STRATEGY=primary_first
export KB_LLM_PARALLEL_MODE=true

# Compare-Modus braucht beide Engines
kb llm engine switch compare
# → Error wenn nur eine Engine verfügbar
```

**Parallel-Strategien erklärt:**

| Strategie | Verhalten | Use Case |
|-----------|-----------|----------|
| `primary_first` | HF zuerst, bei Fehler → Ollama Fallback | Default, robust |
| `aggregate` | Beide Engines parallel, Ergebnisse mergen | Mehr Quellen = bessere Qualität |
| `compare` | Beide Engines, Diff-Anzeige der Ergebnisse | Qualitätssicherung, A/B-Vergleich |

**DiffMerger (compare-Modus):**

Der DiffMerger vergleicht Ergebnisse von beiden Engines auf drei Ebenen:

1. **Essences** – Item-Level Diff: Hinzugefügte/entfernte/geänderte Items
2. **Reports** – Line-Level Diff: Sektion-basierte Text-Vergleiche
3. **Complementary** – Items, die nur in einem Ergebnis vorkommen, werden als Ergänzung markiert

Merge-Regeln:
- Identische Items → einmal übernehmen
- Komplementäre Items → beide behalten (Markierung)
- Konflikte → längere Summary bevorzugen, beide markieren
- Beide Engines müssen verfügbar sein (sonst Error)

```python
from kb.biblio.generator.parallel_mixin import diff_essences, merge_essences

# Essences vergleichen
diff_result = diff_essences(primary_essence, secondary_essence)
print(f"Added: {len(diff_result.added)}")
print(f"Removed: {len(diff_result.removed)}")
print(f"Changed: {len(diff_result.changed)}")
print(f"Complementary: {len(diff_result.complementary)}")

# Essences mergen
merged = merge_essences(primary_essence, secondary_essence, diff_result=diff_result)
```

---

## 7. Konfiguration

**Environment Variables:**

| Variable | Default | Beschreibung |
|----------|---------|--------------|
| `KB_BASE_PATH` | `~/.openclaw/kb` | Root |
| `KB_DB_PATH` | `{base}/knowledge.db` | SQLite |
| `KB_CHROMA_PATH` | `{base}/chroma_db` | ChromaDB |
| `KB_LIBRARY_PATH` | `~/knowledge/library` | Library |
| `KB_LLM_MODEL_SOURCE` | `auto` | Engine: ollama/huggingface/auto/compare |
| `KB_LLM_OLLAMA_MODEL` | `gemma4:e2b` | Ollama model |
| `KB_LLM_HF_MODEL` | `google/gemma-2-2b-it` | HuggingFace model |
| `KB_LLM_HF_QUANTIZATION` | `None` | 4bit/8bit oder None |
| `KB_LLM_PARALLEL_MODE` | `false` | Parallel-Ausführung |
| `KB_LLM_PARALLEL_STRATEGY` | `primary_first` | primary_first/aggregate/compare |

**Programmatisch:**

```python
from kb.base.config import KBConfig

config = KBConfig()
# Singleton – Änderungen global
config._base_path = Path("/custom/path")
```

---

## 8. Schema (Kurzreferenz)

```
knowledge.db
├── files (id, file_path, file_name, file_hash, index_status, ...)
├── file_sections (id, file_id, section_header, section_level, content_full, ...)
├── embeddings (id, section_id, chroma_id, embedding_hash, ...)
├── keywords, section_keywords (Many-to-Many)
└── entries, attachments, themen, kategorie, ...
```

---

*Quelle:* `~/.openclaw/agents/biblio/2026-04-15_kb_architecture_analysis.md`