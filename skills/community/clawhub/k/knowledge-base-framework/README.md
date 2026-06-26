# KB Framework – Deterministic Context Mapping

![Version](https://img.shields.io/badge/version-1.2.0-blue)
![Python](https://img.shields.io/badge/python-3.9+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

> Line numbers, not paragraphs.

## The Problem

RAG systems dump context into your agent's prompt — but you can't verify where it came from. When an agent says "According to your notes...", you're trusting fuzzy similarity search with no way to check.

**Lost-in-the-Middle:** Context gets buried. You're never sure which lines actually informed the answer.

The result: Hallucinations, outdated context, agents that can't trace their own reasoning.

## The Solution

KB Framework tracks **exact source locations** — not just documents, but line numbers:

```
📄 GESUNDHEITS_RATGEBER.md:142
📄 GESUNDHEITS_RATGEBER.md:156
📄 GESUNDHEITS_RATGEBER.md:189
```

Every search returns **pointers**, not paragraphs. The agent can cite, verify, and trace back every piece of context.

## Features

### 🎯 Precision over Recall
- **ChromaDB Integration** – Vector search for semantic similarity
- **Hybrid Search** – Combined 60% semantic + 40% keyword search
- **PDF Indexing** – Automatic PDF document indexing with OCR support
- **Obsidian Vault Support** – WikiLinks, Tags, Frontmatter, Embeds, Backlinks

### 🆕 Version 1.2.0 Features
- **EngineRegistry** – Multi-Engine LLM Support (Ollama + HuggingFace)
- **TransformersEngine** – Local HuggingFace Transformers
- **Compare Mode** – Side-by-Side Engine Comparison
- **Parallel Support** – Parallel Report Generation
- **Config Switch** – Runtime Engine Switching

### 🔗 Obsidian Integration
- Parse WikiLinks, Tags, Frontmatter, Embeds
- Backlink index with bidirectional linking
- Vault-wide search with source tracking

### 🔄 Always in Sync
- ChromaDB ↔ SQLite synchronization
- Orphan detection (entries in vector DB without source file)
- Audit reports with CSV export

### 🚀 Agent-Ready
- Drop-in Python API for your agents
- Context pointers work with any LLM
- No more "according to your notes... (unverified)"

### 🧠 LLM Engine Management (Neu in 1.1.1)
- **EngineRegistry** – Central singleton registry for all LLM engines
- **Multi-Engine Support** – Ollama, HuggingFace Transformers, or both
- **Auto Mode** – HF primary with Ollama fallback (Lumen's default)
- **Compare Mode** – Both engines side-by-side for result comparison
- **TransformersEngine** – Local model loading with quantization support (4-bit, 8-bit)
- **Config Switch** – Runtime engine switching via CLI or API

## Quick Start

```bash
# Installation (see INSTALL.md for full details)
python3 -m venv venv                       # Create virtual environment
./venv/bin/pip install -r requirements.txt  # Install dependencies
./install.sh                               # Optional: install OCR deps

# Use CLI (venv-aware wrapper)
./kb.sh index /path/to/docs          # Index documents
./kb.sh search "your query"          # Search knowledge base
./kb.sh sync                         # Sync ChromaDB with SQLite
./kb.sh audit                        # Run full audit
./kb.sh ghost                        # Find orphaned entries
./kb.sh warmup                       # Preload embedding model

# Or add an alias: alias kb='bash ./kb.sh'
```

## CLI Commands

| Command | Description |
|---------|-------------|
| `kb index <path>` | Index a file or directory recursively |
| `kb search "<query>"` | Search knowledge base with hybrid search |
| `kb sync` | Sync ChromaDB with SQLite (add `--stats`, `--dry-run`, `--delete-orphans`) |
| `kb audit` | Run full KB audit (add `-v` for verbose, `--csv <file>` for export) |
| `kb ghost` | Find orphaned entries in ChromaDB without source file |
| `kb warmup` | Preload embedding model into memory |
| `kb llm status` | Show LLM system status (model, jobs, recent essences) |
| `kb llm generate essence \| report` | Generate essences or reports via LLM |

### LLM Engine Management (Neu in 1.1.1)

The `kb llm engine` commands let you inspect and switch between LLM backends at runtime:

| Command | Description |
|---------|-------------|
| `kb llm engine status` | Show status of all engines (primary, secondary, available) |
| `kb llm engine list` | List all available engine types |
| `kb llm engine info <name>` | Detailed info about a specific engine |
| `kb llm engine switch <source>` | Switch model source (ollama/huggingface/auto/compare) |
| `kb llm engine test` | Test both engines with a sample prompt |

**Examples:**

```bash
# Check current engine status
kb llm engine status
# Output:
# Engine Registry Status
# =====================
# Primary:   huggingface (google/gemma-2-2b-it) ✓
# Secondary: ollama (gemma4:e2b) ✓
# Mode:      auto

# Switch to Ollama-only mode
kb llm engine switch ollama

# Switch to auto mode (HF primary, Ollama fallback)
kb llm engine switch auto

# Switch to compare mode (both engines, diff-view)
kb llm engine switch compare

# Test both engines
kb llm engine test
# Output:
# [ollama]       ✓  gemma4:e2b         0.45s
# [huggingface]  ✓  google/gemma-2-2b-it  1.23s

# Detailed engine info
kb llm engine info huggingface
```

**Config via environment variables:**

```bash
export KB_LLM_MODEL_SOURCE=auto          # ollama|huggingface|auto|compare
export KB_LLM_OLLAMA_MODEL=gemma4:e2b     # Ollama model name
export KB_LLM_HF_MODEL=google/gemma-2-2b-it  # HuggingFace model
export KB_LLM_PARALLEL_MODE=true          # Enable parallel generation
export KB_LLM_PARALLEL_STRATEGY=compare   # primary_first|aggregate|compare
```

**Python API for engine switching:**

```python
from kb.biblio.config import LLMConfig
from kb.biblio.engine.registry import EngineRegistry

# Get current registry
registry = EngineRegistry.get_instance()
print(f"Primary: {registry.primary_provider}")
print(f"Secondary: {registry.get_secondary()}")

# Switch model source at runtime
LLMConfig.reload(model_source="compare", hf_model_name="google/gemma-2-2b-it")
EngineRegistry.reset()
registry = EngineRegistry.get_instance()

# Access both engines
primary, secondary = registry.get_both()
print(f"Primary: {primary.get_model_name()}")
print(f"Secondary: {secondary.get_model_name() if secondary else 'N/A'}")
```

### LLM Integration

- **EssenzGenerator** – Automatically distills source documents into concise "essences" (knowledge summaries)
- **ReportGenerator** – Creates daily/weekly/monthly reports from indexed content
- **FileWatcher** – Monitors directories for new files and auto-indexes them
- **TaskScheduler** – Schedules recurring LLM jobs (essence generation, reports) with cron-like expressions

**Installation:**
```bash
pip install -r requirements.txt
# For HuggingFace support (optional):
pip install -r requirements-transformers.txt
```

**Quickstart:**
```bash
kb llm status                              # Check model availability & job status
kb llm generate essence "Thema"            # Generate an essence for a topic
kb llm generate report daily               # Generate a daily report
kb llm watch start                         # Start file watcher
kb llm scheduler list                      # List scheduled jobs
kb llm config show                         # Show LLM configuration
kb llm engine status                       # Show engine status (all engines)
kb llm engine switch huggingface           # Switch active engine
kb llm engine test                          # Test both engines
```

**CLI Overview (11 Commands):**

| Command | Description |
|---------|-------------|
| `kb index` | Index files/directories |
| `kb search` | Hybrid search (semantic + keyword) |
| `kb sync` | Sync ChromaDB with SQLite |
| `kb audit` | Full integrity check |
| `kb ghost` | Find orphaned entries |
| `kb warmup` | Preload embedding model |
| `kb llm` | LLM integration (essences, reports, watcher, scheduler, config) |
| `kb update` | Auto-updater for GitHub releases |
| `kb llm engine status` | Show status of all engines |
| `kb llm engine switch` | Switch model source (ollama/huggingface/auto/compare) |
| `kb llm engine test` | Test both engines |

### LLM Python API

```python
from kb.biblio.config import LLMConfig
from kb.biblio.engine.factory import create_engine
from kb.biblio.engine.registry import EngineRegistry

# Configure
config = LLMConfig.get_instance()
print(f"Model: {config.model}, Source: {config.model_source}")

# Create engine (single-source or auto mode)
engine = create_engine(config)

# Access registry for multi-engine modes
registry = EngineRegistry.get_instance()
print(f"Primary: {registry.primary_provider}")

# Compare/Auto mode: access both engines
primary, secondary = registry.get_both()
print(f"Primary: {primary.get_model_name()}, Secondary: {secondary.get_model_name() if secondary else 'N/A'}")

# Generate an essence
from kb.biblio.generator.essence_generator import EssenzGenerator

generator = EssenzGenerator()
result = await generator.generate_essence(topic="Vitamin D")
print(f"Hash: {result.essence_hash}, Path: {result.essence_path}")

# Generate a report
from kb.biblio.generator.report_generator import ReportGenerator

report_gen = ReportGenerator()
report = await report_gen.generate_daily_report()
print(f"Sources: {report.sources_count}, Duration: {report.duration_ms}ms")
```

## Demo

```bash
$ kb search "Vitamin D Mangel"

Found 3 context pointers:
📄 GESUNDHEITS_RATGEBER.md:142 [0.87] - "Vitamin D Mangel: Ursachen..."
📄 GESUNDHEITS_RATGEBER.md:156 [0.82] - "Laborwerte: 25-OH-D3..."
📄 GESUNDHEITS_RATGEBER.md:189 [0.79] - "Supplementierung: 2000IU..."

$ kb audit
{
  "total_entries": 2847,
  "with_line_refs": 2847,
  "orphaned": 0,
  "last_sync": "2026-04-15T08:00:00Z"
}
```

The agent receives pointers it can cite directly:
> "According to line 142 of your health notes, Vitamin D deficiency..."

You can verify: open the file, go to line 142, read the source.

## Installation

```bash
# Clone to OpenClaw workspace
git clone https://github.com/Minenclown/kb-framework.git ~/.openclaw/kb

# Or manually:
cp -r kb-framework ~/.openclaw/kb

# Install core dependencies
pip install -r requirements.txt

# For HuggingFace Transformers LLM support (optional):
pip install -r requirements-transformers.txt

# For development (includes core + test dependencies):
pip install -r requirements-dev.txt

./install.sh
```

For global CLI access, add to your `.bashrc`:
```bash
alias kb="~/.openclaw/kb/kb.sh"
source ~/.bashrc
```

## Python API

### Search (HybridSearch)

```python
from kb.framework import HybridSearch

# Initialize search
search = HybridSearch()

# Search with line-level precision
results = search.search("Vitamin D Mangel", limit=5)

for r in results:
    print(f"{r.file_path}:{r.section_id} [{r.combined_score:.2f}]")
    print(f"  → {r.content_preview[:80]}...")
```

### ChromaDB Integration

```python
from kb.framework import ChromaIntegration, embed_text

# Get singleton instance
chroma = ChromaIntegration.get_instance()

# Embed text directly
vector = embed_text("Your text here")

# Query a collection
collection = chroma.sections_collection
results = collection.query(
    query_embeddings=[embed_text("your query")],
    n_results=5,
    where={"file_path": {"$contains": "health"}}
)
```

### Text Chunking

```python
from kb.framework import SentenceChunker, chunk_document

# Configure chunker
chunker = SentenceChunker(max_chunk_size=500, overlap=50)

# Chunk a single text
chunks = chunker.chunk_text("Long text content here...")

# Chunk an entire document
file_chunks = chunk_document("/path/to/document.md", chunker=chunker)
```

### Obsidian Vault

```python
from kb.obsidian import ObsidianVault

vault = ObsidianVault("/path/to/vault")
vault.index()

# Find backlinks
backlinks = vault.find_backlinks("Notes/Meeting.md")

# Full-text search
results = vault.search("Project X")
```

### Module Hierarchy

```python
# Base modules (import directly from subpackages)
from kb.base.config import KBConfig
from kb.base.logger import KBLogger
from kb.base.db import KBConnection

# Knowledge base (re-exports from kb.framework)
from kb.framework import HybridSearch, ChromaIntegration

# Obsidian integration
from kb.obsidian import ObsidianVault
from kb.obsidian.parser import extract_wikilinks, extract_tags
```

## Structure

```
~/.openclaw/kb/
├── kb/                     # Core Python modules
│   ├── commands/           # CLI commands (sync, audit, ghost, warmup)
│   ├── obsidian/           # Obsidian integration
│   └── base/               # Core components
├── library/                # Your content (markdown, PDFs)
├── chroma_db/              # ChromaDB vector database
└── knowledge.db            # SQLite metadata database
```

## License

MIT License