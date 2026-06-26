#!/usr/bin/env python3
"""
DGRA Build State Persistence — v0.6 A-Layer

Global state file for tracking long-running build steps.
Allows resuming after crashes, network failures, or restarts.

State file: ~/.openclaw/skills/dgra-genomic-risk/.dgra_build_state.json
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Any

# =============================================================================
# State file path
# =============================================================================

_STATE_FILE: Path = Path(__file__).resolve().parent.parent / ".dgra_build_state.json"


def set_state_file(path: Path) -> None:
    """Override default state file path (for testing)."""
    global _STATE_FILE
    _STATE_FILE = path


# =============================================================================
# Core state functions
# =============================================================================

def load_state() -> Dict[str, Any]:
    """Load build state from JSON file. Returns empty dict if missing."""
    if _STATE_FILE.exists():
        try:
            with open(_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def save_state(step_name: str, data: Dict[str, Any]) -> None:
    """
    Save a build step's state.

    Args:
        step_name: e.g., "pseudogene_sync", "vep_reannotation", "gtf_download"
        data: Dict with at least "status" key ("complete", "in_progress", "failed")
    """
    state = load_state()
    state[step_name] = {
        "status": data.get("status", "done"),
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }
    _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)


def get_step_status(step_name: str) -> str:
    """Return status of a build step, or 'pending' if not recorded."""
    state = load_state()
    return state.get(step_name, {}).get("status", "pending")


def get_step_data(step_name: str) -> Optional[Dict[str, Any]]:
    """Return full data dict for a step, or None."""
    state = load_state()
    entry = state.get(step_name)
    if entry:
        return entry.get("data")
    return None


def is_step_complete(step_name: str) -> bool:
    """Check if a step is marked complete."""
    return get_step_status(step_name) == "complete"


def reset_state(step_name: Optional[str] = None) -> None:
    """
    Reset build state.

    Args:
        step_name: If provided, reset only that step.
                   If None, delete entire state file.
    """
    if step_name is None:
        if _STATE_FILE.exists():
            _STATE_FILE.unlink()
        return

    state = load_state()
    if step_name in state:
        del state[step_name]
        with open(_STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)


def list_completed_steps() -> list:
    """Return list of step names marked 'complete'."""
    state = load_state()
    return [k for k, v in state.items() if v.get("status") == "complete"]


# =============================================================================
# Convenience: step context manager
# =============================================================================

class BuildStep:
    """
    Context manager for atomic build steps.

    Usage:
        with BuildStep("pseudogene_sync") as step:
            # do work...
            step.complete(genes_synced=51)
    """
    def __init__(self, step_name: str):
        self.step_name = step_name
        self.data: Dict[str, Any] = {}

    def __enter__(self):
        save_state(self.step_name, {"status": "in_progress"})
        return self

    def complete(self, **kwargs):
        self.data.update(kwargs)
        self.data["status"] = "complete"
        save_state(self.step_name, self.data)

    def fail(self, error: str):
        save_state(self.step_name, {"status": "failed", "error": error})

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val and self.step_name:
            self.fail(str(exc_val))
        return False  # Don't suppress exceptions
