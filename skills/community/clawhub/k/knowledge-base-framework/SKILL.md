# KB Framework - OpenClaw Skill

**Version:** 1.2.0  
**Category:** Knowledge Base / Search  
**Requires:** Python 3.9+, SQLite, ChromaDB  
**Location:** `~/.openclaw/kb/`

---

## What is the KB Framework?

A complete Knowledge Base with:
- **Hybrid Search** (semantic + keyword)
- **Automatic Indexing** (Markdown, PDF, OCR)
- **SQLite + ChromaDB** Integration
- **Daily Audits** for data quality
- **LLM Integration** (Ollama/Gemma4, HuggingFace Transformers) for essence generation, reports, file watching, and scheduled jobs
- **EngineRegistry** – Central singleton for multi-engine support
- **Generator Parallel Support** – primary_first, aggregate, compare

---

## Installation (1 Minute)

### 1. Install the Skill
```bash
# Clone or extract into your OpenClaw workspace
git clone https://github.com/Minenclown/kb-framework.git ~/.openclaw/kb

# Or manually:
cp -r kb-framework ~/.openclaw/kb
```

### 2. Install Dependencies
```bash
cd ~/.openclaw/kb
pip install -r requirements.txt

# Optional: HuggingFace Transformers support
pip install -r requirements-transformers.txt
```

### 3. Initialize Database
```bash
python3 ~/.openclaw/kb/kb/indexer.py --init
```

### 4. Add CLI Alias
```bash
# Add to .bashrc for global access:
alias kb="bash ~/.openclaw/kb/kb.sh"
source ~/.bashrc
```

---

## Configuration

Configuration is managed via `kb/base/config.py`:

```python
from kb.base.config import KBConfig

# Get singleton instance
config = KBConfig.get_instance()

# Key properties:
config.base_path        # ~/.openclaw/kb
config.db_path          # ~/.openclaw/kb/knowledge.db
config.library_path     # ~/.openclaw/kb/library
config.chroma_path      # ~/.openclaw/kb/chroma_db

# Environment variable override:
# KB_BASE_PATH=/custom/path
```

### LLM Configuration (`kb/biblio/config.py`)

```python
from kb.biblio.config import LLMConfig

config = LLMConfig.get_instance()
print(f"Source: {config.model_source}")      # auto, ollama, huggingface, compare
print(f"Model: {config.model}")              # Full model name
print(f"HF Model: {config.hf_model_name}")   # google/gemma-2-2b-it
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KB_BASE_PATH` | `~/.openclaw/kb` | Base installation path |
| `KB_LLM_MODEL_SOURCE` | `auto` | Engine: ollama/huggingface/auto/compare |
| `KB_LLM_OLLAMA_MODEL` | `gemma4:e2b` | Ollama model name |
| `KB_LLM_HF_MODEL` | `google/gemma-2-2b-it` | HuggingFace model |
| `KB_LLM_PARALLEL_MODE` | `false` | Enable parallel generation |
| `KB_LLM_PARALLEL_STRATEGY` | `primary_first` | primary_first/aggregate/compare |

---

## Usage

### Python API

```python
import sys
sys.path.insert(0, "~/.openclaw/kb")

# Core Indexer
from kb.indexer import BiblioIndexer

with BiblioIndexer("~/.openclaw/kb/knowledge.db") as idx:
    idx.index_file("/path/to/file.md")

# Hybrid Search
from kb.framework.hybrid_search import HybridSearch
hs = HybridSearch()
results = hs.search("Your search term", limit=10)

# LLM Engine API
from kb.biblio.config import LLMConfig
from kb.biblio.engine.registry import EngineRegistry
from kb.biblio.engine.factory import create_engine

config = LLMConfig.get_instance()
print(f"Source: {config.model_source}")

# Create engine (auto mode mit HF primary + Ollama fallback)
engine = create_engine(config)

# Registry für Multi-Engine Zugriff
registry = EngineRegistry.get_instance(config)
primary, secondary = registry.get_both()

# Generator Parallel Support
from kb.biblio.generator import EssenzGenerator
generator = EssenzGenerator()
result = await generator.generate_essence(
    topic="Topic",
    parallel_strategy="primary_first"  # primary_first, aggregate, compare
)
```

### CLI (Recommended)

```bash
# Core commands:
kb index /path/to/file.md        # Index a file
kb search "machine learning"     # Search knowledge base
kb sync                          # Sync ChromaDB with SQLite
kb audit                         # Run full audit
kb ghost                         # Find orphaned entries
kb warmup                        # Preload ChromaDB model

# LLM commands:
kb llm status                    # LLM system status
kb llm generate essence "topic"  # Generate an essence
kb llm generate report daily     # Generate a daily report
kb llm watch start               # Start file watcher
kb llm scheduler list            # List scheduled jobs
kb llm config show               # Show LLM config

# LLM Engine management:
kb llm engine status             # Show all engine status
kb llm engine switch huggingface # Switch to HuggingFace
kb llm engine test               # Test both engines
```

### Legacy Scripts (`kb/scripts/`)

```bash
# Index PDFs with OCR
python3 ~/.openclaw/kb/kb/scripts/index_pdfs.py /path/to/pdfs/

# Ghost Scanner (finds orphaned DB entries)
python3 ~/.openclaw/kb/kb/scripts/kb_ghost_scanner.py

# Full Audit
python3 ~/.openclaw/kb/kb/scripts/kb_full_audit.py

# ChromaDB Warmup (at boot)
python3 ~/.openclaw/kb/kb/scripts/kb_warmup.py
```

---

## Architecture

```
~/.openclaw/kb/
├── SKILL.md                    # This file
├── README.md                   # Detailed documentation
├── CHANGELOG.md               # Version history
├── kb.sh                       # CLI wrapper
├── knowledge.db               # SQLite metadata database
├── chroma_db/                  # ChromaDB vector database
├── library/                    # Content library
│   ├── content/               # Raw files (PDFs, studies)
│   │   ├── Gesundheit/
│   │   └── Medizin_Studien/
│   └── agent/                 # Markdown files (agent docs)
│       ├── memory/
│       └── projektplanung/
└── kb/                        # Python package
    ├── __main__.py            # CLI entry point: python -m kb
    ├── indexer.py             # Core Indexer (BiblioIndexer)
    ├── config.py              # KB config facade
    ├── update.py              # Auto-updater
    │
    ├── base/                  # Core components
    │   ├── __init__.py
    │   ├── config.py          # KBConfig singleton
    │   ├── db.py              # KBConnection
    │   ├── logger.py          # KBLogger
    │   └── command.py         # Base command class
    │
    ├── commands/              # CLI commands
    │   ├── __init__.py
    │   ├── audit.py           # kb audit
    │   ├── backup.py          # kb backup
    │   ├── engine.py          # kb llm engine
    │   ├── ghost.py           # kb ghost
    │   ├── llm.py             # kb llm (status, generate, watch, scheduler)
    │   ├── search.py          # kb search
    │   ├── sync.py            # kb sync
    │   └── warmup.py          # kb warmup
    │
    ├── biblio/                # LLM Integration
    │   ├── config.py          # LLMConfig singleton
    │   ├── engine/
    │   │   ├── registry.py    # EngineRegistry singleton
    │   │   ├── factory.py     # EngineFactory (Protocol)
    │   │   ├── base.py        # BaseLLMEngine interface
    │   │   ├── ollama_engine.py
    │   │   └── transformers_engine.py
    │   ├── generator/
    │   │   ├── essence_generator.py
    │   │   └── report_generator.py
    │   ├── scheduler/
    │   │   └── task_scheduler.py
    │   └── templates/
    │       ├── essence_template.md
    │       └── report_template.md
    │
    ├── framework/             # Search & embeddings
    │   ├── __init__.py
    │   ├── hybrid_search/     # Hybrid search implementation
    │   ├── providers/         # Search providers
    │   ├── chroma_integration.py
    │   ├── chroma_plugin.py   # Collection management
    │   ├── embedding_pipeline.py
    │   ├── reranker.py
    │   ├── chunker.py
    │   ├── fts5_setup.py
    │   ├── synonyms.py
    │   └── batching.py
    │
    ├── library/               # Library management
    │   └── knowledge_base/
    │
    ├── obsidian/              # Obsidian vault integration
    │   ├── vault.py
    │   ├── parser.py
    │   └── resolver.py
    │
    ├── scripts/               # Standalone scripts
    │   ├── index_pdfs.py
    │   ├── kb_full_audit.py
    │   ├── kb_ghost_scanner.py
    │   ├── kb_warmup.py
    │   ├── sync_chroma.py
    │   └── migrate_fts5.py
    │
    └── llm/                   # (legacy, prefer biblio)
```

---

## Database Schema

### `files` Table
| Field | Type | Description |
|------|------|-------------|
| id | TEXT | UUID |
| file_path | TEXT | Absolute path |
| file_name | TEXT | Filename |
| file_category | TEXT | Category |
| file_type | TEXT | pdf/md/txt |
| file_size | INTEGER | Bytes |
| line_count | INTEGER | Lines |
| file_hash | TEXT | SHA256 |
| last_indexed | TIMESTAMP | Last indexing |
| index_status | TEXT | indexed/pending/failed |
| source_path | TEXT | Original path |
| indexed_path | TEXT | MD extract path |
| is_indexed | INTEGER | 0/1 |

### `file_sections` Table
| Field | Type | Description |
|------|------|-------------|
| id | TEXT | UUID |
| file_id | TEXT | FK → files |
| section_header | TEXT | Heading |
| section_level | INTEGER | 1-6 |
| content_preview | TEXT | First 500 characters |
| content_full | TEXT | Full content |
| keywords | TEXT | JSON Array |
| importance_score | REAL | 0.0-1.0 |

### `keywords` Table
| Field | Type | Description |
|------|------|-------------|
| id | INTEGER | AUTOINCREMENT |
| keyword | TEXT | Word |
| weight | REAL | Frequency |

---

## Library Structure

### `library/content/` - Raw Files
All non-Markdown files:
```
library/content/
├── Gesundheit/           # PDFs, Studies
├── Medizin_Studien/      # Medical Literature
├── Bücher/              # Books, Guides
├── Sonstiges/           # Uncategorized
└── [category]/          # Custom categories possible
```

### `library/agent/` - Markdown Files
All .md files for agents:
```
library/agent/
├── projektplanung/       # Agent plans
├── memory/               # Daily logs
├── Workflow_Referenzen/  # Reusable workflows
├── agents/              # Agent-specific docs
└── [category]/         # Custom categories possible
```

### Integrating New Files

**Rule:** `library/[content|agent]/[category]/[topic]/[file]`

Examples:
```bash
# New health PDF
library/content/Gesundheit/2026/Chelat-Therapie.pdf

# New agent plan
library/agent/projektplanung/Treechat_Upgrade.md

# New learning
library/agent/learnings/2026-04-12_Git_Workflow.md
```

---

## Workflows

### Basic Search Workflow

```bash
# 1. Index content
kb index ./library/content/Gesundheit/

# 2. Search
kb search "Vitamin D Mangel"

# 3. Verify with audit
kb audit
```

### LLM Essence Generation

```bash
# 1. Check status
kb llm engine status

# 2. Generate essence
kb llm generate essence "Vitamin D"

# 3. Or via Python API
python3 -c "
from kb.biblio.engine.registry import EngineRegistry
registry = EngineRegistry.get_instance()
print(registry.primary_provider)
"
```

### Sync & Audit Cycle

```bash
# Sync ChromaDB with SQLite
kb sync --stats

# Find orphaned entries
kb ghost

# Full integrity audit
kb audit -v --csv audit_results.csv
```

---

## API Reference

### KBConfig (`kb/base/config.py`)

```python
from kb.base.config import KBConfig

config = KBConfig.get_instance()

# Properties
config.base_path        # Path: ~/.openclaw/kb
config.db_path          # Path: ~/.openclaw/kb/knowledge.db
config.library_path     # Path: ~/.openclaw/kb/library
config.chroma_path      # Path: ~/.openclaw/kb/chroma_db

# Methods
config.validate()        # Validate paths exist
config.reload()         # Force reload from env
KBConfig.reset()        # Reset singleton (for tests)
```

### LLMConfig (`kb/biblio/config.py`)

```python
from kb.biblio.config import LLMConfig

config = LLMConfig.get_instance()

# Properties
config.model_source     # str: ollama, huggingface, auto, compare
config.model            # str: Full model identifier
config.hf_model_name    # str: HuggingFace model name
config.ollama_model      # str: Ollama model name
config.parallel_mode    # bool
config.parallel_strategy # str: primary_first, aggregate, compare

# Methods
config.reload(model_source=...)  # Reload with new config
config.to_dict()                # Serialize to dict
```

### EngineRegistry (`kb/biblio/engine/registry.py`)

```python
from kb.biblio.engine.registry import EngineRegistry

registry = EngineRegistry.get_instance()

# Properties
registry.primary_provider   # str: Current primary engine
registry.secondary_provider # str: Current secondary engine

# Methods
registry.get_primary()           # Get primary engine instance
registry.get_secondary()         # Get secondary engine instance
registry.get_both()              # (primary, secondary)
registry.is_engine_available(src)  # Check availability
registry.reset()                 # Reset singleton
```

### HybridSearch (`kb/framework/hybrid_search/`)

```python
from kb.framework import HybridSearch

search = HybridSearch()

# Search returns context pointers with line numbers
results = search.search("query", limit=10)

for r in results:
    print(f"{r.file_path}:{r.line_number} [{r.score}]")
    print(f"  → {r.content_preview[:80]}...")
```

### ObsidianVault (`kb/obsidian/vault.py`)

```python
from kb.obsidian import ObsidianVault

vault = ObsidianVault("/path/to/vault")
vault.index()

# Find backlinks
backlinks = vault.find_backlinks("Notes/Meeting.md")

# Search vault
results = vault.search("Project X")

# Full-text search
results = vault.search("keyword")
```

---

## Troubleshooting

### "ChromaDB slow on first start"
```bash
python3 ~/.openclaw/kb/kb/scripts/kb_warmup.py
# or
kb warmup
```

### "Search finds nothing"
```bash
# Run audit
kb audit -v

# Ghost Scanner (find orphaned entries)
kb ghost

# Check sync status
kb sync --stats
```

### "OCR too slow"
```python
# Enable GPU in index_pdfs.py:
GPU_ENABLED = True  # Default: False
```

### "LLM engine not responding"
```bash
# Check engine status
kb llm engine status

# Test both engines
kb llm engine test

# Switch engine if needed
kb llm engine switch ollama
```

### "Database locked"
```bash
# Check for running processes
ps aux | grep kb

# Restart if needed
pkill -f "kb.*"
```

### "Config not found"
```python
# Set environment variable
export KB_BASE_PATH=~/.openclaw/kb

# Or programmatically
from kb.base.config import KBConfig
config = KBConfig.reload(base_path="/path/to/kb")
```

---

## Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| ImportError: kb.base.config not found | Wrong base_path | Set `KB_BASE_PATH=~/.openclaw/kb` |
| ChromaDB timeout | Model not warmed up | Run `kb warmup` first |
| No search results | Empty index or sync needed | `kb sync` then `kb audit` |
| Ghost entries found | Files moved/deleted | `kb sync --delete-orphans` |
| LLM timeout | Model loading slow | Use `kb llm engine test` to verify |
| Engine switch failed | Model not available | Check `kb llm engine status` |

---

## Module Hierarchy

```python
# Core config & database
from kb.base.config import KBConfig
from kb.base.db import KBConnection
from kb.base.logger import KBLogger

# Search framework
from kb.framework import HybridSearch, ChromaIntegration

# Obsidian integration
from kb.obsidian import ObsidianVault
from kb.obsidian.parser import extract_wikilinks, extract_tags

# LLM integration
from kb.biblio.config import LLMConfig
from kb.biblio.engine.registry import EngineRegistry
from kb.biblio.engine.factory import create_engine
```

---

## License

MIT License - free to use.
