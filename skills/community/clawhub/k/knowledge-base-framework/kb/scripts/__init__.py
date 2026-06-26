"""
KB Scripts Module
=================

Standalone CLI scripts for KB Framework maintenance.
These are self-contained tools, not part of the library API.

Scripts:
--------
- kb_warmup.py: Pre-load ChromaDB for faster first query
- kb_full_audit.py: Comprehensive KB audit with reporting
- kb_ghost_scanner.py: Find orphaned entries in vector DB
- sync_chroma.py: Manual ChromaDB ↔ SQLite sync
- migrate_fts5.py: Migrate to FTS5 search
- reembed_all.py: Re-generate all embeddings
- sanitize.py: Clean up invalid entries
- index_pdfs.py: Index PDF documents
- migrate.py: General migration utilities

Usage:
------
    python3 -m kb.scripts.kb_warmup
    python3 -m kb.scripts.kb_full_audit --verbose
"""

__all__ = [
    'kb_warmup',
    'kb_full_audit',
    'kb_ghost_scanner',
    'sync_chroma',
    'migrate_fts5',
    'reembed_all',
    'sanitize',
    'index_pdfs',
    'migrate',
]