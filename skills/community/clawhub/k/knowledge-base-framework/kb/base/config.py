#!/usr/bin/env python3
"""
KBConfig - Singleton für KB Konfiguration

Einmal laden, überall nutzen.
Environment Variables können Werte überschreiben.

Verbesserungen gegenüber Original:
- Thread-safe Initialization
- Lazy Loading mit Validation
- Path Existence Checks
- Type-Safe Property Access
"""

from pathlib import Path
from typing import Optional, Dict, Any
import os
import threading


class KBConfigError(Exception):
    """Configuration-related errors."""
    pass


class KBConfig:
    """
    Singleton für KB Konfiguration.
    
    Thread-safe implementation mit lazy loading.
    __new__-based singleton enforcement prevents race conditions
    after reset() — direct constructor calls always return the
    shared singleton instead of creating duplicates.
    
    Usage:
        config = KBConfig.get_instance()
        db_path = config.db_path  # Auto-initialized
        
        # Force reload
        config = KBConfig.reload(base_path="/new/path")
        
        # Reset for tests
        KBConfig.reset()
    """
    
    _instance: Optional['KBConfig'] = None
    _lock = threading.Lock()
    _initialized: bool = False
    
    DEFAULT_BASE = None  # Resolved lazily via paths.py to avoid circular import
    
    def __new__(cls, base_path: Optional[Path] = None, skip_validation: bool = False):
        """Enforce singleton — constructor always returns the shared instance.
        
        This prevents race conditions after reset(): if two threads
        call KBConfig(...) concurrently when _instance is None, both
        get the same object (only the first triggers __init__).
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                # Mark as needing __init__ on first creation
                cls._instance._needs_init = True  # type: ignore[attr-defined]
            else:
                # Subsequent constructor calls: skip __init__
                cls._instance._needs_init = False  # type: ignore[attr-defined]
        return cls._instance
    
    def __init__(self, base_path: Optional[Path] = None, skip_validation: bool = False):
        # Guard: only init on first construction (or after reset)
        if not getattr(self, '_needs_init', False):
            return
        
        self._base_path = self._resolve_base_path(base_path)
        self._env_overrides: Dict[str, str] = {}
        self._validated = False
        self._needs_init = False
        
        if not skip_validation:
            self._validate()
        
        KBConfig._initialized = True
    
    @staticmethod
    def _resolve_base_path(base_path: Optional[Path]) -> Path:
        """Resolve base path from parameter or environment."""
        if base_path is not None:
            return Path(base_path).resolve()
        
        env_base = os.getenv("KB_BASE_PATH")
        if env_base:
            return Path(env_base).resolve()
        
        # Package-relative fallback: if kb/library/ exists relative to this package
        package_root = Path(__file__).resolve().parent.parent  # kb/base/ -> kb/
        if (package_root / "library").exists():
            return package_root
        
        # OpenClaw-managed installation default
        return get_default_base_path()
    
    def _validate(self) -> None:
        """Validate configuration paths. Fails fast on critical issues."""
        # Check base directory - should exist or be creatable
        if not self._base_path.exists():
            # Try to create it
            try:
                self._base_path.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                raise KBConfigError(f"Cannot create base path {self._base_path}: {e}")
        
        # Check if base_path is actually a directory
        if not self._base_path.is_dir():
            raise KBConfigError(f"Base path exists but is not a directory: {self._base_path}")
        
        self._validated = True
    
    @classmethod
    def get_instance(cls, base_path: Optional[Path] = None) -> 'KBConfig':
        """
        Returns singleton instance (lazy initialization).
        
        Thread-safe: All reads/writes of _instance are protected by cls._lock.
        No fast path outside the lock to avoid race conditions.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._needs_init = True  # type: ignore[attr-defined]
                cls._instance.__init__(base_path)
            elif base_path is not None:
                # If a different base_path is requested, reload under lock
                existing = cls._instance._base_path.resolve()
                requested = Path(base_path).resolve()
                if existing != requested:
                    old_instance = cls._instance
                    cls._instance = super().__new__(cls)
                    cls._instance._needs_init = True  # type: ignore[attr-defined]
                    try:
                        cls._instance.__init__(base_path)
                    except KBConfigError:
                        # Restore on failure — don't leave singleton in broken state
                        cls._instance = old_instance
                        cls._initialized = True
                        raise
        
        return cls._instance
    
    @classmethod
    def reload(cls, base_path: Optional[Path] = None) -> 'KBConfig':
        """Forces reload of configuration."""
        with cls._lock:
            cls._instance = None
            cls._initialized = False
        return cls.get_instance(base_path)
    
    @classmethod
    def reset(cls) -> None:
        """Reset singleton (mainly for testing). Thread-safe."""
        with cls._lock:
            cls._instance = None
            cls._initialized = False
    
    # --- Path Properties with Environment Override Support ---
    
    @property
    def base_path(self) -> Path:
        """Root directory of KB installation."""
        return self._base_path
    
    @property
    def db_path(self) -> Path:
        env = os.getenv("KB_DB_PATH")
        if env:
            return Path(env).resolve()
        return self._base_path / "library" / "biblio.db"
    
    @property
    def chroma_path(self) -> Path:
        env = os.getenv("KB_CHROMA_PATH")
        if env:
            return Path(env).resolve()
        return self._base_path / "library" / "chroma_db"
    
    @property
    def library_path(self) -> Path:
        env = os.getenv("KB_LIBRARY_PATH")
        if env:
            return Path(env).resolve()
        return self._base_path / "library"
    
    @property
    def library_biblio_path(self) -> Path:
        """Path to library/biblio/ (LLM-generated content)."""
        return self.library_path / "biblio"
    
    @property
    def knowledge_base_path(self) -> Path:
        """Path to kb/framework/ (search engine code path)."""
        return self._base_path / "framework"
    
    @property
    def workspace_path(self) -> Path:
        env = os.getenv("KB_WORKSPACE_PATH")
        if env:
            return Path(env).resolve()
        return self._base_path.parent / "workspace"
    
    @property
    def ghost_cache_path(self) -> Path:
        env = os.getenv("KB_GHOST_CACHE_PATH")
        if env:
            return Path(env).resolve()
        return self._base_path / "ghost_cache.json"
    
    @property
    def backup_dir(self) -> Path:
        env = os.getenv("KB_BACKUP_DIR")
        if env:
            return Path(env).resolve()
        return self._base_path / "backup"
    
    @property
    def index_roots(self) -> list[str]:
        """
        Root directories to index by default.
        
        Override via KB_INDEX_ROOTS env var (comma-separated):
            KB_INDEX_ROOTS=projektplanung,learnings,dokumentation
        """
        env = os.getenv("KB_INDEX_ROOTS")
        if env:
            return [p.strip() for p in env.split(",") if p.strip()]
        return ["projektplanung", "learnings"]
    
    # --- Utility Methods ---
    
    def ensure_dir(self, path: Path) -> Path:
        """Ensure directory exists, create if needed."""
        path = Path(path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path
    
    def to_dict(self) -> Dict[str, Any]:
        """Export configuration as dictionary."""
        return {
            'base_path': str(self.base_path),
            'db_path': str(self.db_path),
            'chroma_path': str(self.chroma_path),
            'library_path': str(self.library_path),
            'library_biblio_path': str(self.library_biblio_path),
            'knowledge_base_path': str(self.knowledge_base_path),
            'workspace_path': str(self.workspace_path),
            'ghost_cache_path': str(self.ghost_cache_path),
            'backup_dir': str(self.backup_dir),
        }
    
    def __repr__(self) -> str:
        return f"KBConfig(base={self._base_path}, validated={self._validated})"
    
    def __str__(self) -> str:
        return f"KBConfig at {self._base_path}"


# Convenience function for quick access
def get_config() -> KBConfig:
    """Get KBConfig singleton instance."""
    return KBConfig.get_instance()
