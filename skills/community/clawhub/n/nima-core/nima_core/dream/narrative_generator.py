#!/usr/bin/env python3
"""
Dream Narrative Generator
==========================
LLM-powered narrative generation for dream consolidation.

Generates surreal dream narratives from memory fragments using an LLM API.
Saves narratives to dated markdown journal files.

Functions:
  - generate_dream_narrative: Create narrative from memory fragments via LLM
  - save_dream_markdown: Append narrative to dated markdown journal

Environment:
    NIMA_LLM_PROVIDER    LLM provider for narrative generation
    NIMA_LLM_API_KEY     API key for narrative generation
    NIMA_LLM_BASE_URL    API base URL override
    NIMA_LLM_MODEL       Model for narrative

Author: Lilu / nima-core
"""

from __future__ import annotations

import os
import json
import logging
import urllib.request
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

from .models import DreamSession

__all__ = [
    "generate_dream_narrative",
    "save_dream_markdown",
]

logger = logging.getLogger(__name__)


def generate_dream_narrative(memories: List[Dict], theme: str) -> Optional[str]:
    """
    Generate a surreal dream narrative from memory fragments via LLM.

    Uses the canonical NIMA_LLM_* environment configuration.
    Gracefully returns None if unavailable or if API call fails.

    Args:
        memories: List of memory dictionaries with 'text' or 'summary' fields
        theme: Underlying theme to weave into the narrative

    Returns:
        Dream narrative string, or None if generation fails/unavailable

    Environment:
        NIMA_LLM_PROVIDER: provider name
        NIMA_LLM_API_KEY: API key
        NIMA_LLM_BASE_URL: API base URL override
        NIMA_LLM_MODEL: model name
    """
    snippets = [
        (m.get("text") or m.get("summary") or "")[:200]
        for m in memories[:10]
        if (m.get("text") or m.get("summary") or "").strip()
    ]

    prompt = (
        "Create a short surreal dream narrative (150 words max).\n"
        "Weave these memory fragments into dream logic:\n"
        + "\n".join(f"- {s}" for s in snippets)
        + f"\n\nUnderlying theme: {theme}\n\n"
        "Rules: sudden transitions, impossible physics, symbolic emotions, "
        "non-linear time. Output only the dream narrative — no explanation."
    )

    try:
        from nima_core.llm_client import llm_complete
        return llm_complete(prompt, max_tokens=250)
    except ImportError:
        logger.debug("llm_client not available; no fallback implemented, returning None")
        return None
    except Exception as e:
        logger.debug(f"Dream narrative generation failed: {e}")
        return None


def save_dream_markdown(narrative: str, session: DreamSession, dreams_dir: Path) -> None:
    """
    Append dream narrative to dated markdown journal.

    Creates or updates a markdown file named YYYY-MM-DD.md in the dreams directory.
    Each narrative is appended with timestamp, domains, and emotion metadata.

    Args:
        narrative: The dream narrative text to save
        session: DreamSession with metadata (domains, emotion, etc.)
        dreams_dir: Directory where dream journal files are stored

    Side effects:
        Writes to {dreams_dir}/{YYYY-MM-DD}.md
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    filepath  = dreams_dir / f"{date_str}.md"
    header    = filepath.read_text() if filepath.exists() else f"# Dream Journal — {date_str}\n\n"
    entry = (
        "---\n\n"
        f"## Dream — {datetime.now().strftime('%H:%M')}\n\n"
        f"**Domains:** {', '.join(session.top_domains)}\n"
        f"**Emotion:** {session.dominant_emotion or 'neutral'}\n\n"
        f"{narrative}\n\n"
    )
    filepath.write_text(header + entry)
