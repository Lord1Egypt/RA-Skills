#!/usr/bin/env python3
"""
Cross-Platform Temporary Directory Management

Manages temporary directories across Windows/macOS/Linux with automatic cleanup.
"""

import os
import re
import sys
import uuid
import time
import atexit
import signal
import shutil
from typing import List, Optional, Iterator
from contextlib import contextmanager


class TempDirManager:
    """
    Manages temporary directories across Windows/macOS/Linux.
    
    Features:
    - Uses system temp directory via tempfile.gettempdir()
    - Generates unique, collision-free directory names
    - Supports context manager for automatic cleanup
    - Registers with atexit for guaranteed cleanup
    """
    
    _instances: List[str] = []
    _cleanup_registered: bool = False
    
    def __init__(self, prefix: str = 'github-', base_dir: str = None):
        """
        Initialize TempDirManager.
        
        Args:
            prefix: Prefix for temporary directory name
            base_dir: Base directory (defaults to system temp)
        """
        self.prefix = prefix
        self.base_dir = base_dir or self._get_system_temp()
        self._path: Optional[str] = None
        self._owns_path: bool = False
    
    @staticmethod
    def _get_system_temp() -> str:
        """Get system temp directory."""
        import tempfile
        return tempfile.gettempdir()
    
    @staticmethod
    def _normalize_path(path: str) -> str:
        """Normalize path for cross-platform compatibility."""
        return os.path.normpath(os.path.abspath(path))
    
    @staticmethod
    def _sanitize_filename(name: str) -> str:
        """Sanitize filename for cross-platform compatibility."""
        # Remove or replace unsafe characters
        name = re.sub(r'[<>:"/\\|?*]', '-', name)
        name = re.sub(r'-+', '-', name)
        name = name.strip('.-')
        # Limit length for Windows compatibility (MAX_PATH issues)
        if len(name) > 100:
            name = name[:100]
        return name or 'repo'
    
    def create(self) -> str:
        """
        Create a unique temporary directory.
        
        Returns:
            Path to the created temporary directory
        """
        unique_id = uuid.uuid4().hex[:8]
        sanitized_prefix = self._sanitize_filename(self.prefix)
        dir_name = f"{sanitized_prefix}-{unique_id}"
        self._path = os.path.join(self.base_dir, dir_name)
        self._owns_path = True
        
        # Ensure parent directory exists
        os.makedirs(self.base_dir, exist_ok=True)
        
        # Create directory with restricted permissions (Unix) or standard (Windows)
        os.makedirs(self._path, mode=0o755, exist_ok=True)
        
        # Track for cleanup
        if self._path not in TempDirManager._instances:
            TempDirManager._instances.append(self._path)
        
        # Register cleanup handler once
        if not TempDirManager._cleanup_registered:
            self._register_cleanup()
        
        return self._path
    
    def create_named(self, name: str) -> str:
        """
        Create a named temporary directory (for predictable paths).
        
        Args:
            name: Directory name (will be sanitized)
            
        Returns:
            Path to the created temporary directory
        """
        sanitized_name = self._sanitize_filename(name)
        unique_id = uuid.uuid4().hex[:4]
        dir_name = f"{sanitized_name}-{unique_id}"
        self._path = os.path.join(self.base_dir, dir_name)
        self._owns_path = True
        
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self._path, mode=0o755, exist_ok=True)
        
        if self._path not in TempDirManager._instances:
            TempDirManager._instances.append(self._path)
        
        if not TempDirManager._cleanup_registered:
            self._register_cleanup()
        
        return self._path
    
    @staticmethod
    def _register_cleanup():
        """Register cleanup handlers for exit and signals."""
        TempDirManager._cleanup_registered = True
        
        # Register atexit
        atexit.register(TempDirManager.cleanup_all)
        
        # Register signal handlers (Unix)
        if hasattr(signal, 'SIGTERM'):
            signal.signal(signal.SIGTERM, TempDirManager._signal_handler)
        if hasattr(signal, 'SIGINT'):
            signal.signal(signal.SIGINT, TempDirManager._signal_handler)
    
    @staticmethod
    def _signal_handler(signum, frame):
        """Handle termination signals."""
        TempDirManager.cleanup_all()
        sys.exit(128 + signum)
    
    def cleanup(self) -> bool:
        """
        Remove the temporary directory.
        
        Returns:
            True if cleaned up successfully, False otherwise
        """
        if not self._path or not self._owns_path:
            return False
        
        try:
            if os.path.exists(self._path):
                # On Windows, try multiple times in case of locked files
                for attempt in range(3):
                    try:
                        shutil.rmtree(self._path, ignore_errors=True)
                        break
                    except PermissionError:
                        if attempt < 2:
                            time.sleep(0.1)
                        else:
                            # Last resort: mark for later cleanup
                            pass
                
                # Remove from tracking
                if self._path in TempDirManager._instances:
                    TempDirManager._instances.remove(self._path)
                
                return True
        except Exception:
            pass
        
        return False
    
    @staticmethod
    def cleanup_all():
        """Clean up all tracked temporary directories."""
        instances = TempDirManager._instances.copy()
        for path in instances:
            try:
                if os.path.exists(path):
                    shutil.rmtree(path, ignore_errors=True)
                if path in TempDirManager._instances:
                    TempDirManager._instances.remove(path)
            except Exception:
                pass
        
        TempDirManager._instances.clear()
    
    def __enter__(self) -> 'TempDirManager':
        """Context manager entry."""
        if not self._path:
            self.create()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Context manager exit."""
        self.cleanup()
    
    @property
    def path(self) -> Optional[str]:
        """Get the current temporary directory path."""
        return self._path


@contextmanager
def temp_directory(prefix: str = 'github-', base_dir: str = None) -> Iterator[str]:
    """
    Context manager for temporary directories.
    
    Usage:
        with temp_directory('github-sync-') as temp_dir:
            # Use temp_dir here
            pass
        # Automatically cleaned up after exiting
    """
    manager = TempDirManager(prefix=prefix, base_dir=base_dir)
    path = manager.create()
    try:
        yield path
    finally:
        manager.cleanup()
