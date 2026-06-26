#!/usr/bin/env python3
"""
kb.llm.watcher - File Watcher Package

Monitors kb/library/ for new files and triggers essence generation.
"""

from kb.biblio.watcher.file_watcher import (
    FileWatcher,
    FileWatcherError,
    WatchedFile,
    FileWatcherState,
)

__all__ = [
    "FileWatcher",
    "FileWatcherError",
    "WatchedFile",
    "FileWatcherState",
]