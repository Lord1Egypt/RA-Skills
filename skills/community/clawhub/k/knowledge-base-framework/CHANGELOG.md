# Changelog

## [1.2.0] - 2026-04-27

### Fixed
- **Phase A Path Bugs:** Fixed hardcoded `Path.home()` in `kb/update.py` (3 locations), `kb/__main__.py`, and `kb/config.py` — now use central `paths.py` API
- **CLI Crash:** Fixed `_SubParsersAction` issue in `kb/commands/llm.py` that caused complete CLI crash on `kb llm generate`
- **Performance - fetchall():** Changed `fetchall()` to `fetchmany(1000)` batch processing in `indexer.py` and `sync.py` to prevent memory extrusion on large databases
- **Performance - COUNT Query:** Optimized `_sync_stats()` to use single aggregated COUNT query instead of loading all content_full rows
- **Performance - ChromaDB Batching:** Added batch processing for ChromaDB ID retrieval with `peek(limit=batch_size)` loop
- **Link Graph Inversion:** Fixed inverted source/target logic in `kb/obsidian/indexer.py` line 225-233
- **SQL Injection Protection:** Fixed `isalnum()` check that rejected valid negative PRAGMA values like `-64000` in `kb/base/db.py`
- **add_wikilink Duplication:** Fixed incomplete duplication check that missed `[[target|alias]]` variants in `kb/obsidian/writer.py`
- **Silent DB Failure:** Changed `sync_manager.py` to re-raise exceptions instead of returning empty list on DB errors
- **Test Exception Handling:** Extended `test_indexer.py` exception catch to include `AttributeError`

### Changed
- **Refactored keyword.py:** Split long functions into sub-methods for better maintainability
- **Refactored llm.py:** Split long functions into sub-methods for better maintainability
- **requirements.txt:** Added upper bounds for major versions (`chromadb<1.0`, etc.) to prevent breaking changes

### Security
- **Path Traversal:** Improved validation in `update.py` path security checks
- **Exception Handling:** Replaced bare `except Exception:` with specific exception handling where critical

### Documentation
- **README.md:** Updated version badge from 1.1.1 → 1.2.0 and added missing 1.2.0 features (EngineRegistry, TransformersEngine, Compare Mode)
- **SKILL.md:** Updated version from 1.1.1 → 1.2.0

## [1.1.1] - 2026-04-16

### 🚨 Breaking Changes

- **EngineRegistry ist jetzt zentraler Singleton** – Engine-Zugriff nur noch über `EngineRegistry.get_instance()` statt direkter `OllamaEngine.get_instance()` Aufrufe
- **Import-Pfade geändert** – `kb.llm` → `kb.biblio` für Generator-Klassen
- **`kb.config.py` entfernt** – Alle relevanten Imports wurden auf `kb.base.config` umgestellt (W1, W2)

### Features

- **EngineRegistry**: Neue zentrale Registry für LLM-Engines mit Singleton-Pattern
  - Multi-Engine Support: Ollama + HuggingFace Transformers gleichzeitig
  - `model_source` Config: `auto`, `ollama`, `huggingface`, `compare`
  - `EngineRegistry.get_instance()` statt direkter Engine-Erstellung
  - `registry.get_primary()`, `registry.get_secondary()`, `registry.get_both()`
  
- **Config-Switch**: `model_source` "auto" als neuer Default
  - Auto Mode: HF primary + Ollama fallback (Lumen's Entscheidung)
  - Compare Mode: Beide Engines für Diff/Merge
  - `parallel_mode`, `parallel_strategy` für Generator Parallel Support
  
- **Neue Config-Keys**:
  - `ollama_model` – Ollama-Modell (default: `gemma4:e2b`)
  - `ollama_timeout` – Timeout in Sekunden (default: `120`)
  - `ollama_temperature` – Temperature 0-2 (default: `0.7`)
  - `model_source` – Engine-Auswahl (default: `auto`)
  - `parallel_mode` – Parallel-Ausführung (default: `False`)
  - `parallel_strategy` – `primary_first`, `aggregate` oder `compare` (default: `primary_first`)
  
- **Neue CLI-Befehle** (`kb llm engine`):
  - `kb llm engine status` – Status aller Engines anzeigen
  - `kb llm engine switch <source>` – Engine wechseln (ollama/huggingface/auto/compare)
  - `kb llm engine test` – Beide Engines testen
  - `kb llm engine list` – Verfügbare Engines auflisten
  - `kb llm engine info <name>` – Detaillierte Info zu einer Engine
  
- **TransformersEngine**: Local Hugging Face Transformers support
  - Direct model loading ohne externe API
  - 8-bit und 4-bit quantization support (bitsandbytes)
  - Auto device detection (CUDA/MPS/CPU)
  - Memory-efficient model loading/unloading
  - Streaming und batch generation support
  
- **Generator Parallel Support**:
  - `primary_first`: HF zuerst, bei Fehler Ollama
  - `aggregate`: Beide Engines, Ergebnisse zusammenführen
  - `compare`: Beide Engines, Unterschiede anzeigen

### Technical

- Complete engine factory pattern implementation
- Unified interface for Ollama and Transformers engines
- Thread-safe EngineRegistry mit Locking

### Test Coverage (1.1.1)

- **45 Tests** – EngineRegistry (`test_engine_registry.py`)
  - Singleton pattern, primary/secondary engine access, auto/compare/ollama/hf modes
  - `reset()`, `is_engine_available()`, `get_both()`, `repr()`, error handling
  - EngineFactory Protocol & Dependency Injection
  - Thread-safe singleton creation
- **38 Tests** – Model Source Config (`test_model_source.py`)
  - Validation: `ollama`, `huggingface`, `auto`, `compare`, quantization, `hf_model_name` required
  - Config reload, environment variable overrides, `to_dict()` serialization, token masking
  - Fallback behavior: HF failure → Ollama promotion, neither available → error
  - Parallel strategy validation
- **41 Tests** – Parallel Mode & Diff/Merge (`test_parallel_mode.py`)
  - `diff_essences()`, `merge_essences()`: item-level comparison, union merge, deduplication
  - `diff_reports()`, `merge_reports()`: line-level text diff, section merge
  - `DiffResult`, `DiffEntry`, `ParallelResult` dataclasses
  - `__init_parallel__()`, `_should_use_parallel()`, strategy initialization
- **Gesamt: 124 neue Tests** (alle grün ✅)

### Fixes (aus 3 Analyse-Runden)

- Deadlock issues in ChromaDB sync resolved
- Thread-safety improvements for concurrent DB access
- kb/config.py fälschlicherweise erstellt → wieder entfernt
- Orphan detection verbessert
- Fallback-Kette für HybridSearch dokumentiert (Semantic → Keyword → Fallback)

---

## [1.1.1] - 2026-04-15

### Features
- **LLM Integration**: Ollama/Gemma4 engine for knowledge extraction (`kb.llm` package)
- **EssenzGenerator**: Automatic essence generation from source documents
- **ReportGenerator**: Daily/weekly/monthly reports from indexed content
- **FileWatcher**: Monitors directories for new files, triggers auto-indexing
- **TaskScheduler**: Cron-like scheduling for recurring LLM jobs
- **LLMCommand**: Full CLI integration with 6 subcommands (`kb llm status|generate|watch|scheduler|list|config`)

### Fixes
- Deadlock issues in ChromaDB sync resolved
- Thread-safety improvements for concurrent DB access

---

# Phase 6: Obsidian Write-Funktion

**Status:** Geplant
**Voraussetzung:** Phase 1-5 abgeschlossen (131 Tests bestanden)
**Ziel:** Schreib-Zugriff auf Obsidian Vault

---

## 1. Funktionsumfang

### Core Write-Operationen

| Operation | Beschreibung |
|-----------|--------------|
| `create_note()` | Neue .md Datei mit Frontmatter und Body erstellen |
| `update_note()` | Bestehende Note überschreiben (Body +/ oder Frontmatter) |
| `update_frontmatter()` | Nur Frontmatter einer Note aktualisieren |
| `append_content()` | Inhalt an bestehende Note anhängen |
| `delete_note()` | Note löschen (optional, mit backup) |
| `move_note()` | Note umbenennen/verschieben (inkl. Link-Update) |

### Wikilink-Operationen

| Operation | Beschreibung |
|-----------|--------------|
| `add_wikilink()` | Wikilink in Datei einfügen |
| `remove_wikilink()` | Wikilink aus Datei entfernen |
| `replace_wikilink()` | Wikilink-Ziel ändern (bei Umbenennung) |
| `get_broken_links()` | Orphaned links finden |

### Sync-Operationen (Vault ↔ KB)

| Operation | Beschreibung |
|-----------|--------------|
| `sync_to_vault()` | KB-Eintrag als Note in Vault schreiben |
| `sync_from_vault()` | Vault-Note zurück in KB schreiben |
| `update_wikilinks_after_rename()` | Alle Links aktualisieren wenn Note umbenannt |

---

## 2. API-Design

### 2.1 Note Creation

```python
def create_note(
    self,
    relative_path: str,
    content: str = "",
    frontmatter: dict | None = None,
    auto_timestamp: bool = True
) -> Path:
    """
    Erstelle neue Note im Vault.
    
    Args:
        relative_path: Pfad relativ zum Vault (z.B. "Notes/Test.md")
        content: Body-Content (ohne Frontmatter)
        frontmatter: Metadata-Dict (wird als YAML serialisiert)
        auto_timestamp: Automatisch created/modified setzen
    
    Returns:
        Absoluter Path zur erstellten Datei
    
    Raises:
        FileExistsError: Datei bereits vorhanden
    """
```

### 2.2 Frontmatter Update

```python
def update_frontmatter(
    self,
    relative_path: str,
    updates: dict,
    merge: bool = True
) -> dict:
    """
    Aktualisiere Frontmatter einer Note.
    
    Args:
        relative_path: Pfad zur Note
        updates: Dictionary mit zu aktualisierenden Feldern
        merge: True = zusammenführen, False = ersetzen
    
    Returns:
        Neues Frontmatter-Dict
    """
```

### 2.3 Wikilink Operations

```python
def add_wikilink(
    self,
    source_path: str,
    target: str,
    context: str | None = None,
    position: str = "end"
) -> None:
    """
    Füge Wikilink in Datei ein.
    
    Args:
        source_path: Pfad zur Quell-Datei
        target: Link-Ziel (z.B. "Target Note" oder "folder/Target")
        context: Umgebender Text für den Link
        position: "end" (Default Section), "start", oder "after:<heading>"
    """

def replace_wikilink(
    self,
    old_target: str,
    new_target: str,
    scope: str | None = None
) -> int:
    """
    Ersetze Wikilink-Ziel über alle Dateien oder im Scope.
    
    Args:
        old_target: Altes Link-Ziel
        new_target: Neues Link-Ziel
        scope: Optional nur bestimmte Datei
    
    Returns:
        Anzahl der aktualisierten Links
    """
```

### 2.4 Sync mit KB

```python
def sync_to_vault(
    self,
    kb_entry_id: int,
    vault_path: str | None = None
) -> Path:
    """
    Schreibe KB-Eintrag als Obsidian Note.
    
    Args:
        kb_entry_id: ID des KB-Eintrags
        vault_path: Optionaler Zielpfad (sonst auto-generiert)
    
    Returns:
        Path zur erstellten/aktualisierten Note
    """

def sync_from_vault(
    self,
    vault_path: str
) -> int:
    """
    Importiere Vault-Note zurück in KB.
    
    Returns:
        KB-Eintrag ID
    """
```

---

## 3. Dateistruktur

### Neues Modul: `writer.py`

```
kb/obsidian/
├── writer.py          # NEU: Alle Write-Operationen
├── __init__.py        # Update: writer.py exportieren
├── vault.py           # Update: Write-Methoden delegieren
└── ...
```

### `writer.py` Struktur

```python
"""
Obsidian Writer - Write Operations for Obsidian Vault
"""

import re
import yaml
from pathlib import Path
from datetime import datetime
from typing import Optional

from kb.obsidian.parser import parse_frontmatter, WIKILINK_PATTERN

class VaultWriter:
    """Handles all write operations on an Obsidian vault."""
    
    def __init__(self, vault_path: Path):
        self.vault_path = vault_path
    
    # --- Core Operations ---
    def create_note(...)
    def update_note(...)
    def update_frontmatter(...)
    def append_content(...)
    def delete_note(...)
    def move_note(...)
    
    # --- Wikilink Operations ---
    def add_wikilink(...)
    def remove_wikilink(...)
    def replace_wikilink(...)
    def get_broken_links(...)
    
    # --- Sync Operations ---
    def sync_to_vault(...)
    def sync_from_vault(...)
    
    # --- Internal Helpers ---
    def _serialize_frontmatter(...)
    def _ensure_directory(...)
    def _atomic_write(...)
```

### Key Design Decisions

1. **Atomic Writes:** Temp-File + rename für Crash-Safety
2. **Frontmatter Preservation:** Kommentare und Formatierung erhalten (YAML-safe)
3. **Link-Update bei Move:** Automatische Korrektur aller eingehenden Links
4. **Backup-Option:** `delete_note()` verschiebt in `.trash/` statt rm

---

## 4. Test-Szenarien

### Unit Tests (`test_writer.py`)

| Test | Beschreibung |
|------|--------------|
| `test_create_note_basic` | Minimal-Notiz erstellen |
| `test_create_note_with_frontmatter` | Note mit vollem Frontmatter |
| `test_create_note_duplicate_error` | FileExistsError bei Doppelerstellung |
| `test_update_frontmatter_merge` | Frontmatter-Felder zusammenführen |
| `test_update_frontmatter_replace` | Frontmatter komplett ersetzen |
| `test_add_wikilink_end` | Link am Dateiende einfügen |
| `test_add_wikilink_with_context` | Link mit Kontext-Text einfügen |
| `test_add_wikilink_after_heading` | Link nach bestimmter Überschrift |
| `test_remove_wikilink` | Wikilink aus Datei entfernen |
| `test_replace_wikilink_single_file` | Link in einer Datei ersetzen |
| `test_replace_wikilink_vault_wide` | Link vaultweit ersetzen |
| `test_broken_links_detection` | Orphaned Links finden |

### Integration Tests

| Test | Beschreibung |
|------|--------------|
| `test_move_note_updates_backlinks` | Note umbenennen, Links自动更新 |
| `test_create_then_link` | Note erstellen, dann Link darauf setzen |
| `test_sync_kb_to_vault_roundtrip` | KB → Vault → KB (Daten bleiben gleich) |

### Edge Cases

- [ ] Leere Frontmatter (`---` ohne Inhalt)
- [ ] Unicode in Dateinamen und Links
- [ ] Overly long frontmatter values
- [ ] Nested folders (`Notes/Sub/Nested.md`)
- [ ] Sonderzeichen in Tags (#tag mit Umlaut)

---

## 5. Zeit-Schätzung

| Phase | Aufgabe | Zeit |
|-------|---------|------|
| 6a | `writer.py` Grundgerüst + `create_note()` | 45 min |
| 6b | `update_frontmatter()` + `update_note()` | 30 min |
| 6c | Wikilink-Operationen | 45 min |
| 6d | `move_note()` mit Link-Update | 30 min |
| 6e | Sync-Operationen (KB ↔ Vault) | 45 min |
| 6f | Tests schreiben + Bugfixes | 60 min |
| **Total** | | **~4 Stunden** |

### Risiken

| Risiko | Wahrscheinlichkeit | Mitigation |
|--------|-------------------|------------|
| YAML-Formatierung verloren | Mittel | PyYAML + custom preserve |
| Race Conditions bei parallel writes | Gering | File locking |
| Backlink-Update zu langsam bei großen Vaults | Mittel | Batch-Update mit Progress |

---

## 6. Abhängigkeiten

- **Bestehend:** `parser.py`, `resolver.py`, `indexer.py`
- **Neu:** Keine externen Dependencies (Standard-Bibliothek reicht)
- **Optional später:** `python-frontmatter` für bessere YAML-Persistenz

---

## 7. Implementation-Reihenfolge

```
1. VaultWriter-Klasse in writer.py
2. create_note() + _serialize_frontmatter()
3. update_frontmatter() (lesen → modifizieren → schreiben)
4. add_wikilink() + remove_wikilink()
5. replace_wikilink() vaultweit
6. move_note() mit backlink-update
7. Integration in vault.py (ObsidianVault.add_write_methods)
8. Tests
```

---

**Nächster Schritt:** Softaware kann mit Phase 6a beginnen.

---

# Korrekturen

## 2026-04-15

### `kb/config.py` entfernt

- **Problem:** O3 hatte fälschlicherweise eine neue `kb/config.py` mit Deprecation-Warnung erstellt
- **Lösung:** Datei vollständig entfernt (Commit 2026-04-15)
- **Grund:** Alle relevanten Imports wurden bereits auf `kb.base.config` umgestellt (W1, W2)
- **Geänderte Dateien:**
  - `kb/framework/embedding_pipeline.py` - Fallback-Import entfernt
  - `kb/framework/chroma_plugin.py` - Fallback-Import entfernt
  - `kb/config.py` - gelöscht
- **Status:** ✅ Tests bestanden
