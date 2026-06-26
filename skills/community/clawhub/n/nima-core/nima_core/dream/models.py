"""
Dream Consolidation Models
===========================
Core data models for dream consolidation system.

This module contains:
  - Insight: Discovered patterns, connections, and questions
  - Pattern: Recurring themes across memories
  - DreamSession: Metadata for a consolidation run
  - Utility functions for timestamps and atomic JSON writes

Author: Lilu / nima-core
"""

from __future__ import annotations

import os
import json
import logging
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional

__all__ = [
    "Insight",
    "Pattern",
    "DreamSession",
]

logger = logging.getLogger(__name__)


# ── Dataclasses ───────────────────────────────────────────────────────────────

@dataclass
class Insight:
    id: str
    type: str            # "pattern" | "connection" | "question" | "emotion_shift"
    content: str
    confidence: float    # 0-1
    sources: List[str]
    domains: List[str]
    timestamp: str
    importance: float    # 0-1

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "Insight":
        return cls(**d)


@dataclass
class Pattern:
    id: str
    name: str
    description: str
    occurrences: int
    domains: List[str]
    examples: List[str]
    first_seen: str
    last_seen: str
    strength: float      # 0-1, accumulates with occurrences

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "Pattern":
        return cls(**d)


@dataclass
class DreamSession:
    id: str
    started_at: str
    ended_at: str
    hours: int
    memories_processed: int
    patterns_found: int
    insights_generated: int
    top_domains: List[str]
    dominant_emotion: Optional[str]
    narrative: Optional[str]    # LLM dream narrative (if generated)
    bot_name: str

    def to_dict(self) -> Dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: Dict) -> "DreamSession":
        return cls(**d)


# ── Utility ────────────────────────────────────────────────────────────────────

def _utcnow() -> str:
    return datetime.now(timezone.utc).isoformat()


def _now_str() -> str:
    return datetime.now().isoformat()


def _atomic_write_json(path: Path, data: dict) -> bool:
    """Write JSON atomically (tmp → rename) to prevent corruption."""
    try:
        dir_ = path.parent
        dir_.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=dir_, suffix=".tmp")
        try:
            with os.fdopen(fd, "w") as f:
                json.dump(data, f, indent=2, default=str)
            os.replace(tmp, path)
            return True
        except Exception:
            try:
                os.unlink(tmp)
            except OSError:
                pass
            raise
    except (OSError, IOError) as e:
        logger.error(f"Atomic write failed for {path}: {e}")
        return False
