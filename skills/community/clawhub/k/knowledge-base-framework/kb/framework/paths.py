"""
Centralized Path Resolution for KB Framework
=============================================

Single source of truth for default paths. All modules should
import from here instead of defining their own fallback logic.

Resolution order:
    1. Environment variable (KB_BASE_PATH, KB_DB_PATH, etc.)
    2. KBConfig singleton (if available)
    3. Package-relative detection (if kb/ is a standalone install)
    4. OpenClaw default (~/.openclaw/kb)

Usage:
    from kb.framework.paths import get_default_db_path, get_default_chroma_path

    db_path = get_default_db_path()
    chroma_path = get_default_chroma_path()
"""

import os
from pathlib import Path


def get_default_base_path() -> Path:
    """Resolve default KB base path.

    Priority: KB_BASE_PATH env > KBConfig > package-relative > ~/.openclaw/kb
    """
    env = os.getenv("KB_BASE_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().base_path
    except (ImportError, AttributeError):
        # Package-relative fallback: if kb/library/ exists relative to package
        package_root = Path(__file__).resolve().parent.parent  # kb/framework/ -> kb/
        if (package_root / "library").exists():
            return package_root
        return Path.home() / ".openclaw" / "kb"


def get_default_db_path() -> Path:
    """Resolve default SQLite database path."""
    env = os.getenv("KB_DB_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().db_path
    except (ImportError, AttributeError):
        return get_default_base_path() / "library" / "biblio.db"


def get_default_chroma_path() -> Path:
    """Resolve default ChromaDB path."""
    env = os.getenv("KB_CHROMA_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().chroma_path
    except (ImportError, AttributeError):
        return get_default_base_path() / "library" / "chroma_db"


def get_default_library_path() -> Path:
    """Resolve default library path."""
    env = os.getenv("KB_LIBRARY_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().library_path
    except (ImportError, AttributeError):
        return get_default_base_path() / "library"


def get_default_workspace_path() -> Path:
    """Resolve default workspace path."""
    env = os.getenv("KB_WORKSPACE_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().workspace_path
    except (ImportError, AttributeError):
        return get_default_base_path().parent / "workspace"


def get_default_ghost_cache_path() -> Path:
    """Resolve default ghost cache path."""
    env = os.getenv("KB_GHOST_CACHE_PATH")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().ghost_cache_path
    except (ImportError, AttributeError):
        return get_default_base_path() / "ghost_cache.json"


def get_default_backup_dir() -> Path:
    """Resolve default backup directory."""
    env = os.getenv("KB_BACKUP_DIR")
    if env:
        return Path(env).resolve()
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().backup_dir
    except (ImportError, AttributeError):
        return get_default_base_path() / "backup"


def get_default_cache_path() -> Path:
    """Resolve default embedding cache path."""
    try:
        from kb.base.config import KBConfig
        return KBConfig.get_instance().base_path / "library" / "embeddings" / "cache.json"
    except (ImportError, AttributeError):
        return get_default_base_path() / "library" / "embeddings" / "cache.json"