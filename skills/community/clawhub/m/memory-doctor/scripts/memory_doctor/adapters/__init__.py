"""Format adapters. v0.1: auto-memory. W2: mneme."""

import glob
import os

from .auto_memory import AutoMemoryAdapter
from .mneme import MnemeAdapter

ADAPTERS = {
    "auto-memory": AutoMemoryAdapter,
    "mneme": MnemeAdapter,
}


def get_adapter(name: str):
    if name not in ADAPTERS:
        raise ValueError(f"unknown format '{name}'. available: {', '.join(ADAPTERS)}")
    return ADAPTERS[name]()


def detect_format(root: str) -> str:
    """Pick an adapter for a directory by what files it contains."""
    if glob.glob(os.path.join(root, "*.mneme")) or glob.glob(os.path.join(root, "*.mn")):
        return "mneme"
    return "auto-memory"
