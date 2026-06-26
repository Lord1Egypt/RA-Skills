# KB Framework - Funktionsdokumentation
**Version:** 1.1.1  
**Stand:** 2026-04-15

---

## Inhaltsverzeichnis
1. [Architektur-Überblick](#1-architektur-überblick)
2. [Base Module (`kb.base`)](#2-base-module-kbbase)
3. [Commands (`kb.commands`)](#3-commands-kbcommands)
4. [Obsidian Module (`kb.obsidian`)](#4-obsidian-module-kbobsidian)
5. [Knowledge Base Module (`kb.framework`)](#5-knowledge-base-module-kbframework)
6. [Indexer & Updater](#6-indexer--updater)
7. [LLM Module (`kb.llm`)](#7-llm-module-kbllm)
8. [Abhängigkeiten](#9-abhängigkeiten)
9. [Nutzungsbeispiele](#10-nutzungsbeispiele)

---

## 1. Architektur-Überblick

```
kb-framework/
├── kb/                          # Hauptpaket
│   ├── __init__.py              # Paket-Export
│   ├── __main__.py             # CLI Entry Point
│   ├── config.py               # Globale Konfiguration
│   ├── indexer.py              # Markdown Indexer
│   ├── update.py               # Auto-Updater
│   └── version.py              # Versionsinfo
│
├── kb/base/                     # Core Komponenten
│   ├── config.py               # KBConfig Singleton
│   ├── logger.py              # KBLogger Singleton
│   ├── db.py                   # KBConnection Context Manager
│   └── command.py              # BaseCommand ABC
│
├── kb/commands/                 # CLI Commands
│   ├── sync.py                 # ChromaDB Sync
│   ├── audit.py                # Full Audit
│   ├── ghost.py                # Ghost Scanner
│   ├── warmup.py               # Model Warmup
│   └── search.py               # Hybrid Search
│
├── kb/obsidian/                 # Obsidian Integration
│   ├── parser.py               # Frontmatter & Wikilinks Parser
│   ├── resolver.py             # Link Resolution
│   ├── indexer.py              # Backlink Indexer
│   ├── vault.py                # High-Level Vault API
│   └── writer.py               # Vault Write Operations
│
├── kb/framework/  # Vector Search
│   ├── chroma_integration.py   # ChromaDB Interface
│   ├── hybrid_search.py        # Hybrid Search (Phase 1-6)
│   ├── fts5_setup.py           # SQLite FTS5 Setup
│   ├── reranker.py             # Cross-Encoder Re-Ranking
│   ├── synonyms.py            # Synonym Expansion
│   ├── chunker.py             # Text Chunking
│   └── embedding_pipeline.py   # Batch Embedding
│
└── tests/                      # Test Suite
```

---

## 2. Base Module (`kb.base`)

### KBConfig (`kb.base.config`)

**Singleton für Konfigurationsmanagement.**

```python
from kb.base.config import KBConfig

# Get instance
config = KBConfig.get_instance()

# Paths (automatisch mit Environment Override)
config.base_path        # Root KB Verzeichnis
config.db_path          # SQLite Database
config.chroma_path      # ChromaDB Persistence
config.library_path     # Dokumenten-Bibliothek
config.workspace_path   # Workspace
config.ghost_cache_path # Ghost Scanner Cache
config.backup_dir       # Backup Verzeichnis

# Methoden
config.ensure_dir(path)  # Erstelle Verzeichnis wenn nötig
config.to_dict()          # Exportiere als Dict
KBConfig.reload()         # Force Reload
KBConfig.reset()          # Reset Singleton (für Tests)
```

**Konfiguration via Environment Variables:**
- `KB_BASE_PATH` - Basisverzeichnis
- `KB_DB_PATH` - Datenbankpfad
- `KB_CHROMA_PATH` - ChromaDB Pfad
- `KB_LIBRARY_PATH` - Bibliothek Pfad
- `KB_WORKSPACE_PATH` - Workspace Pfad

---

### KBLogger (`kb.base.logger`)

**Singleton für strukturiertes Logging.**

```python
from kb.base.logger import KBLogger

# Setup (einmal am Start)
KBLogger.setup_logging(level=logging.INFO)

# Logger für Module
log = KBLogger.get_logger("kb.sync")
log.info("Nachricht")
log.warning("Warnung")
log.error("Fehler")
```

**Features:**
- Thread-safe mit Locking
- Colored Output für TTY
- Logger Cache für Performance
- Konfigurierbares Format

---

### KBConnection (`kb.base.db`)

**Datenbank-Connection mit Context Manager.**

```python
from kb.base.db import KBConnection

# Als Context Manager
with KBConnection(config.db_path) as conn:
    rows = conn.fetchall("SELECT * FROM files WHERE id = ?", file_id)
    conn.commit()

# Oder direkt
conn = KBConnection(db_path)
conn.__enter__()
# ... work ...
conn.__exit__()
```

**Methoden:**
```python
conn.execute(sql, *args)           # SQL ausführen
conn.executemany(sql, *args)      # Batch operations
conn.fetchone(sql, *args)          # Einzelne Zeile
conn.fetchall(sql, *args)         # Alle Zeilen
conn.fetchdict(sql, *args)        # Als Dict
conn.execute_many_with_progress(sql, data, chunk_size=1000)
conn.commit()                       # Transaktion commit
conn.rollback()                     # Rollback
conn.close()                        # Explizit schließen
```

**Performance Pragmas:**
- WAL Mode
- 64MB Cache
- Memory Temp Store
- 256MB MMap

---

### BaseCommand (`kb.base.command`)

**Abstract Base Class für alle Commands.**

```python
from kb.base.command import BaseCommand, register_command

@register_command
class MyCommand(BaseCommand):
    name = "mycmd"
    help = "Description of my command"
    
    def add_arguments(self, parser):
        parser.add_argument('--flag', action='store_true')
    
    def _execute(self) -> int:
        log = self.get_logger()
        log.info("Executing...")
        return self.EXIT_SUCCESS
```

**Geerbte Methoden:**
```python
self.get_config()        # KBConfig Singleton
self.get_logger()        # Logger für diesen Command
self.get_db()           # DB Connection
self.require_db()       # DB mit Fail-Fast
self.log_section(title)  # Header ausgeben
self.log_progress()     # Progress Log
self.validate(args)     # Override für Validierung
self.cleanup()          # Override für Aufräumen
```

---

## 3. Commands (`kb.commands`)

### SyncCommand (`kb.commands.sync`)

**ChromaDB Sync mit Delta Indexing.**

```bash
kb sync                  # Delta Sync (fehlende Einträge)
kb sync --stats         # Statistiken anzeigen
kb sync --dry-run       # Simulation ohne Änderungen
kb sync --full         # Full Re-Sync Info
kb sync --file-id UUID # Einzelne Datei sync
kb sync --delete-orphans # Verwaiste löschen
kb sync --batch-size 32 # Batch Größe
```

**Kernmethoden:**
```python
_sync_stats(conn)              # Sync-Statistiken
_cmd_delta()                   # Delta Sync
_embed_missing_sections()      # Embedding Batch
_delete_orphans()             # Orphan Cleanup
```

---

### AuditCommand (`kb.commands.audit`)

**Vollständiger KB Integrity Check.**

```bash
kb audit                  # Alle Checks
kb audit -v              # Verbose
kb audit --skip-chroma   # ChromaDB überspringen
kb audit --skip-files    # Datei-Check überspringen
kb audit --export-csv pfad # CSV Export
kb audit --checks db_integrity,schema # Nur bestimmte Checks
```

**Checks:**
- `db_integrity` - DB Tabellen/Indizes
- `schema` - Required Tables
- `library_paths` - Fehlende Dateien
- `null_paths` - NULL/empty paths
- `embeddings_table` - Embeddings Status
- `chroma_sync` - SQLite/ChromaDB Sync
- `orphaned_entries` - Verwaiste Einträge

---

### GhostCommand (`kb.commands.ghost`)

**Findet neue, nicht indexierte Dateien.**

```bash
kb ghost                 # Standardscan
kb ghost --scan-dirs ~/docs,~/notes # Verzeichnisse
kb ghost --extensions md,pdf       # Dateitypen
kb ghost --exclude-dirs .git,.tmp   # Ausschlüsse
kb ghost --min-size 1000           # Min Größe
kb ghost --dry-run                # Vorschau
kb ghost --json-output            # JSON statt CSV
```

**Kernmethoden:**
```python
_get_indexed_files()            # Bereits indexierte Dateien
_scan_for_new_files()           # Scanner
_save_ghost_files()             # Export
```

---

### WarmupCommand (`kb.commands.warmup`)

**Lädt das Embedding-Modell vor.**

```bash
kb warmup               # Modell laden
kb warmup --check      # Status prüfen
kb warmup --verbose    # Detaillierte Ausgabe
kb warmup --force      # Erzwungenes Neuladen
kb warmup --timeout 30 # Timeout in Sekunden
kb warmup --model "all-MiniLM-L6-v2" # Modell wählen
```

**Kernmethoden:**
```python
_check_memory()          # Memory Check
_report_model_info()     # Modell-Info
```

---

### SearchCommand (`kb.commands.search`)

**Hybrid Search (Semantic + Keyword).**

```bash
kb search "query text"              # Hybrid Suche
kb search "query" -n 10             # Limit 10
kb search "query" -s                 # Nur Semantic
kb search "query" -k                 # Nur Keyword
kb search "query" --format full      # Vollständiges Format
kb search "query" --ft md pdf         # Dateityp-Filter
kb search "query" --date-from 2024-01-01
kb search "query" --debug            # Debug Info
```

---

## 4. Obsidian Module (`kb.obsidian`)

### ObsidianVault (`kb.obsidian.vault`)

**High-Level API für Obsidian Vaults.**

```python
from kb.obsidian.vault import ObsidianVault

vault = ObsidianVault("/path/to/vault")

# Indexing
vault.index()                    # Vault indexieren
vault.index_file(file_path)      # Einzelne Datei

# Suche
results = vault.search("query", limit=20)

# Backlinks
backlinks = vault.find_backlinks("Note.md")

# Graph
graph = vault.get_graph()  # {'nodes': [...], 'edges': [...]}

# Link Resolution
path = vault.resolve_link("Note#Heading")

# File Info
info = vault.get_file_info("Note.md")

# Statistiken
stats = vault.get_stats()
```

---

### BacklinkIndexer (`kb.obsidian.indexer`)

**Invertierter Index für Backlinks.**

```python
from kb.obsidian.indexer import BacklinkIndexer

indexer = BacklinkIndexer("/path/to/vault")
indexer.index_vault()

# Backlinks für eine Datei
backlinks = indexer.get_backlinks(Path("Note.md"))
# [{'source': Path(...), 'context': '...', 'link_text': 'Note'}]

# Unlinked Mentions
mentions = indexer.get_unlinked_mentions("term")

# Link Graph
graph = indexer.get_link_graph()

# Statistiken
stats = indexer.get_stats()
```

---

### VaultWriter (`kb.obsidian.writer`)

**Schreiboperationen für Vaults.**

```python
from kb.obsidian.writer import VaultWriter

writer = VaultWriter("/path/to/vault")

# Notizen erstellen
writer.create_note("Notes/New.md", content, frontmatter={'tags': ['test']})

# Frontmatter aktualisieren
writer.update_frontmatter("Notes/New.md", {'tags': ['updated']})

# Wikilinks
writer.add_wikilink("Note.md", "Target", "context")
writer.remove_wikilink("Note.md", "Target")

# Links ersetzen
count = writer.replace_wikilink("Old", "New")

# Note verschieben
writer.move_note("old/path.md", "new/path.md")

# Note löschen
writer.delete_note("Notes/Old.md")
```

---

## 5. Knowledge Base Module (`kb.framework`)

### HybridSearch (`kb.framework.hybrid_search`)

**Kombinierte Semantic + Keyword Suche.**

```python
from kb.framework.hybrid_search import HybridSearch

searcher = HybridSearch(
    db_path="library/biblio.db",
    chroma_path="library/chroma_db/"
)

# Suche
results = searcher.search("query", limit=20)

# Spezifische Modi
semantic_results = searcher.search_semantic("query")
keyword_results = searcher.search_keyword("query")

# Mit Filtern
results = searcher.search_with_filters(
    query="query",
    file_types=["md", "pdf"],
    date_from="2024-01-01",
    date_to="2024-12-31"
)

# Statistiken
stats = searcher.get_stats()

# Cache leeren
searcher._query_cache.clear()

searcher.close()
```

**SearchResult Struktur:**
```python
@dataclass
class SearchResult:
    section_id: str
    file_id: str
    file_path: str
    section_header: str
    content_preview: str
    content_full: str
    section_level: int
    importance_score: float
    keywords: list[str]
    semantic_score: float = 0.0   # ChromaDB
    keyword_score: float = 0.0    # SQLite
    combined_score: float = 0.0  # Gewichtet
    source: str = ""             # "chroma", "sqlite", "hybrid"
```

**Features (implementierte Phasen):**
- Phase 1: Vector Search Foundation ✅
- Phase 2: Synonym Expansion ✅
- Phase 3.1: Wing/Room/Hall Filter ✅
- Phase 3.2: Query Caching (LRU) ✅
- Phase 4: Advanced Chunking ✅
- Phase 5: Re-Ranking (BM25) ✅
- Phase 6: Cross-Encoder (optional) ✅

---

### ChromaIntegration (`kb.framework.chroma_integration`)

**ChromaDB Wrapper mit Thread-Safety.**

```python
from kb.framework.chroma_integration import ChromaIntegration

chroma = ChromaIntegration(chroma_path="library/chroma_db/")

# Collection Zugriff
collection = chroma.sections_collection

# Operationen
chroma.add_sections(sections)      # Sections hinzufügen
chroma.delete_sections(ids)         # Löschen
chroma.query(text, n_results=10)   # Query

# Statistiken
stats = chroma.get_collection_stats("kb_sections")
```

---

### EmbeddingPipeline (`kb.framework.embedding_pipeline`)

**Batch-Embedding für file_sections.**

```python
from kb.framework.embedding_pipeline import EmbeddingPipeline

pipeline = EmbeddingPipeline(
    db_path="library/biblio.db",
    chroma_path="library/chroma_db/"
)

# Batch-Verarbeitung
pipeline.process_all_sections(batch_size=100, parallel=True)

# Einzelne Datei
pipeline.process_file(file_id)

pipeline.close()
```

**Dataclass:**
```python
@dataclass
class SectionRecord:
    id: str
    file_id: str
    file_path: str
    section_header: str
    content_full: str
    content_preview: str
    section_level: int
    importance_score: float
    keywords: list[str]
```

---

### Reranker (`kb.framework.reranker`)

**Cross-Encoder Re-Ranking.**

```python
from kb.framework.reranker import Reranker, get_reranker

reranker = get_reranker()

# Re-ranking
reranked = reranker.rerank(query, results)
```

---

### SynonymExpander (`kb.framework.synonyms`)

**Query Expansion mit Synonymen.**

```python
from kb.framework.synonyms import SynonymExpander, get_expander

expander = get_expander()
expanded = expander.expand_query("machine learning")
# -> "machine learning ml ai artificial_intelligence"
```

---

## 6. Indexer & Updater

### BiblioIndexer (`kb.indexer`)

**Vollständiger Markdown Indexer.**

```python
from kb.indexer import BiblioIndexer

with BiblioIndexer("library/biblio.db", plugins=[...]) as indexer:
    # Einzelne Datei
    sections = indexer.index_file(Path("test.md"))
    
    # Verzeichnis
    stats = indexer.index_directory("/path/to/docs")
    
    # Delta Indexing
    stats = indexer.check_and_update(["/path/to/watch"])
    
    # Full Reindex
    stats = indexer.full_reindex(["docs/", "learnings/"])
    
    # Index unindexed/
    stats = indexer.index_unindexed()
    
    # Datei entfernen
    indexer.remove_file("path/to/file.md")
```

**Plugin System:**
```python
class MyPlugin(IndexingPlugin):
    def on_file_indexed(self, file_path, sections, file_id):
        # Called after successful indexing
        pass
    
    def on_file_removed(self, file_path):
        # Called after file removal
        pass
    
    def on_indexing_complete(self, stats):
        # Called after batch indexing
        pass
```

---

### MarkdownIndexer (`kb.indexer`)

**Parst Markdown nach Header-Struktur.**

```python
from kb.indexer import MarkdownIndexer

indexer = MarkdownIndexer("library/biblio.db")
sections = indexer.parse_file(Path("test.md"))
# -> [{'header': '...', 'level': 1, 'content': [...], ...}]
```

---

### KBUpdate (`kb.update`)

**Auto-Updater für GitHub Releases.**

```python
from kb.update import main, get_current_version, get_latest_release

# Check only
main(["--check"])

# Force update
main(["--force"])

# Normal update with confirmation
main([])
```

---

## 7. LLM Module (`kb.llm`)  *(Neu in 1.1.1)*

### LLMConfig (`kb.llm.config`)

**Singleton für LLM-Konfiguration (Ollama/Gemma4).**

```python
from kb.llm.config import LLMConfig

config = LLMConfig.get_instance()
config.model           # Modell-Name (default: gemma3:4b)
config.ollama_url      # Ollama Server URL
config.temperature     # Generation temperature
config.essences_path   # Pfad für Essenzen
config.reports_path   # Pfad für Reports
```

### OllamaEngine (`kb.llm.engine`)

**LLM-Engine mit Ollama-Backend.**

```python
from kb.llm.engine import OllamaEngine

engine = OllamaEngine.get_instance()
available = engine.is_available()       # Modell verfügbar?
response = await engine.generate(prompt) # Text generieren
stream = await engine.stream(prompt)     # Streaming-Antwort
```

### EssenzGenerator (`kb.llm.generator.essence_generator`)

**Erstellt Wissens-Essenzen aus Quelldokumenten.**

```python
from kb.llm.generator import EssenzGenerator

generator = EssenzGenerator()
result = await generator.generate_essence(topic="Thema", source_files=[...])
# result.success, result.essence_hash, result.essence_path, result.model_used
```

### ReportGenerator (`kb.llm.generator.report_generator`)

**Erstellt täglich/wöchentlich/monatlich Berichte.**

```python
from kb.llm.generator import ReportGenerator

generator = ReportGenerator()
result = await generator.generate_daily_report()
result = await generator.generate_weekly_report()
result = await generator.generate_monthly_report()
```

### FileWatcher (`kb.llm.watcher`)

**Überwacht Verzeichnisse auf neue Dateien.**

```python
from kb.llm.watcher import FileWatcher

watcher = FileWatcher()
await watcher.run(interval_minutes=30)  # Startet Überwachung
watcher.stop()                           # Stoppt
stats = watcher.get_stats()              # Status-Info
```

### TaskScheduler (`kb.llm.scheduler`)

**Cron-ähnlicher Scheduler für LLM-Jobs.**

```python
from kb.llm.scheduler import TaskScheduler

scheduler = TaskScheduler()
await scheduler.start()                  # Startet Scheduler
jobs = scheduler.list_jobs()            # Jobs auflisten
result = await scheduler.run_job("id")   # Job manuell triggern
await scheduler.shutdown()               # Stoppen
```

### LLMContentManager (`kb.llm.content_manager`)

**Verwaltet Essenzen und Reports (CRUD + Storage).**

```python
from kb.llm.content_manager import LLMContentManager

manager = LLMContentManager()
essences = await manager.list_essences(limit=10)
reports = await manager.list_reports(report_type="daily")
essence = await manager.get_essence_by_topic("Thema")
```

### LLMCommand (`kb.commands.llm`)

**CLI-Integration für alle LLM-Funktionen.**

```bash
kb llm status                               # System-Status
kb llm generate essence "Thema"             # Essenz erstellen
kb llm generate report daily                # Report erstellen
kb llm watch start|stop|status              # FileWatcher
kb llm scheduler start|stop|list|trigger ID  # Scheduler
kb llm list essences|reports               # Auflisten
kb llm config [show|set key value]          # Konfiguration
```

---

## 9. Abhängigkeiten

### Modul-Diagramm

```
kb.__main__
    └── kb.commands (Registry)
            ├── SyncCommand
            ├── AuditCommand
            ├── GhostCommand
            ├── WarmupCommand
            └── SearchCommand
                    └── HybridSearch
                            ├── ChromaIntegration
                            ├── SynonymExpander
                            ├── Reranker
                            └── FTS5 Setup

kb.indexer
    ├── MarkdownIndexer
    ├── BiblioIndexer
    │       └── IndexingPlugin (ABC)
    └── KBConnection

kb.obsidian
    ├── VaultWriter
    ├── PathResolver
    ├── BacklinkIndexer
    └── ObsidianVault

kb.base
    ├── KBConfig
    ├── KBLogger
    ├── KBConnection
    └── BaseCommand
```

---

## 10. Nutzungsbeispiele

### CLI Nutzung

```bash
# Help anzeigen
python3 -m kb --help

# Sync mit Statistiken
python3 -m kb sync --stats

# Audit durchführen
python3 -m kb audit -v

# Nach neuer Dateien scannen
python3 -m kb ghost --scan-dirs ~/Documents

# Embedding Modell vorladen
python3 -m kb warmup --verbose

# Suchen
python3 -m kb search "MTHFR Genmutation" -n 10
```

### Python API

```python
# Konfiguration
from kb.base.config import KBConfig
config = KBConfig.get_instance()

# Logging
from kb.base.logger import KBLogger
KBLogger.setup_logging()
log = KBLogger.get_logger("my.module")

# Datenbank
from kb.base.db import KBConnection
with KBConnection(config.db_path) as conn:
    files = conn.fetchall("SELECT * FROM files")
    for f in files:
        print(f['file_name'])

# Indexing
from kb.indexer import BiblioIndexer
with BiblioIndexer(config.db_path) as indexer:
    indexer.index_directory("/path/to/docs")

# Suche
from kb.framework.hybrid_search import HybridSearch
searcher = HybridSearch(db_path=config.db_path, chroma_path=config.chroma_path)
results = searcher.search("Suchanfrage")
for r in results:
    print(f"{r.file_path}: {r.section_header} [{r.combined_score:.2f}]")
searcher.close()

# Obsidian Vault
from kb.obsidian.vault import ObsidianVault
vault = ObsidianVault("/path/to/vault")
vault.index()
backlinks = vault.find_backlinks("Note.md")
```

---

## Anhang: Exit Codes

| Code | Name | Bedeutung |
|------|------|----------|
| 0 | EXIT_SUCCESS | Erfolgreich |
| 1 | EXIT_VALIDATION_ERROR | Validierung fehlgeschlagen |
| 2 | EXIT_EXECUTION_ERROR | Ausführung fehlgeschlagen |
| 3 | EXIT_CLEANUP_ERROR | Cleanup fehlgeschlagen |
| 130 | KeyboardInterrupt | Ctrl+C |

---

*Document erstellt: 2026-04-15*
*Prüfer: Sir Stern 🔍*