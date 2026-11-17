#!/usr/bin/env python3
"""State machine persistence for GKN-Phantom.

Implements the StateSerializer contract: state can be checkpointed to a file
between transitions, so a run can be PAUSED (Ctrl-C, agent yield, network
outage) and RESUMED from the same transition.

State layout (persisted as JSON in runs/<run_id>.json):
  {
    "run_id": str,
    "current": <StateName>,
    "history": [log_event, ...],
    "context_snapshot": <AgentContext at the time of checkpoint>
  }

Usage:
  from state import StateSerializer
  ss = StateSerializer("runs/run-2026-06-20-001.json")
  ss.checkpoint("VALIDATION", history=[...], context=ctx)
  ...
  ss2 = StateSerializer("runs/run-2026-06-20-001.json")
  state = ss2.load()
  if state["current"] != "INIT": resume_from(state["current"])
"""

from __future__ import annotations

import json
import os
import shutil
from typing import Any

from utils import utc_now_iso


STATES = [
    "INIT", "SCOPE_CHECK", "PRE_FLIGHT", "RECONNAISSANCE", "AUTH_SETUP",
    "ACTIVE_TESTING", "VALIDATION", "ATTACK_PATH_ANALYSIS",
    "REPORT_GENERATION", "DONE",
]


class StateSerializer:
    """Atomic checkpoint + load for the run state machine.

    Writes go to <path>.tmp and are renamed atomically so a crash mid-write
    never produces a corrupt state file.
    """

    def __init__(self, path: str):
        self.path = path

    def checkpoint(self, current: str, history: list, context: dict | None = None) -> None:
        if current not in STATES:
            raise ValueError(f"unknown state: {current}")
        payload = {
            "run_id": _derive_run_id(self.path),
            "current": current,
            "history": history,
            "context_snapshot": context or {},
            "checkpointed_at": utc_now_iso(),
        }
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        # atomic write: write to .tmp then replace (with cross-device fallback)
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(payload, fh, indent=2, ensure_ascii=False)
        try:
            os.replace(tmp, self.path)
        except OSError:
            # Cross-device fallback (e.g. /tmp and runs/ on different mounts)
            shutil.move(tmp, self.path)

    def load(self) -> dict:
        if not os.path.exists(self.path):
            raise FileNotFoundError(f"no checkpoint at {self.path}")
        with open(self.path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def exists(self) -> bool:
        return os.path.exists(self.path)

    def clear(self) -> None:
        for suffix in ("", ".tmp"):
            p = self.path + suffix
            if os.path.exists(p):
                os.remove(p)


def _derive_run_id(path: str) -> str:
    base = os.path.basename(path)
    if base.endswith(".json"):
        base = base[:-5]
    return base


def next_state(current: str) -> str | None:
    """Return the next state in the pipeline, or None at DONE."""
    if current == "DONE":
        return None
    idx = STATES.index(current)
    return STATES[idx + 1]


def can_resume(checkpoint: dict) -> tuple[bool, str]:
    """Validate a loaded checkpoint is in a resumable state."""
    cur = checkpoint.get("current", "INIT")
    if cur not in STATES:
        return False, f"invalid state '{cur}'"
    if cur == "DONE":
        return False, "run already completed"
    return True, cur
