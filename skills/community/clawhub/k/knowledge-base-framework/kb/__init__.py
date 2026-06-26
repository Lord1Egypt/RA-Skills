"""
KB Framework - Core Package
==========================

Deterministic Context Mapping for AI Agents.

The KB Framework tracks exact source locations in knowledge bases,
providing line-level precision instead of document-level similarity.
Agents can cite, verify, and trace back every piece of context.

Architecture:
-------------
- kb.base: Core components (Config, DB, Logging, Commands)
- kb.commands: CLI command implementations
- kb.framework: Search, embeddings, chunking, vector DB
- kb.biblio: LLM integration (engines, generators, scheduler, watcher)
- kb.library: Data directory (biblio output, content, agent entries)
- kb.obsidian: Obsidian vault integration

Usage:
------
    from kb import KBConfig, KBLogger, KBConnection
    
    config = KBConfig.get_instance()
    logger = KBLogger.get_logger(__name__)
    
    with KBConnection() as conn:
        conn.execute("SELECT ...")

Modules:
--------
- kb.base: Framework core
- kb.commands: CLI commands
- kb.framework: Search & retrieval engine
- kb.biblio: LLM integration (engines, generators)
- kb.library: Data directory (biblio.db, essences, reports)
- kb.obsidian: Obsidian integration
"""

__version__ = "1.2.0"

__all__ = [
    '__version__',
]