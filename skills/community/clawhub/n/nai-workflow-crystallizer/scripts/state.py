#!/usr/bin/env python3
"""
Workflow Crystallizer — State Management

Manages persistent state across runs: event cache, suggestion lifecycle,
analysis history. State file lives alongside the scripts directory at
../state.json (or a custom path via --state-file).
"""

import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Optional

DEFAULT_STATE_PATH = Path(__file__).resolve().parent.parent / "state.json"

DEFAULT_CONFIG = {
    "min_confidence": 0.6,
    "max_suggestions_per_run": 3,
    "snooze_days": 30,
    "min_days_of_data": 3,
    "min_occurrences": 3,
    "min_unique_days": 2,
}

EMPTY_STATE = {
    "version": 1,
    "last_analysis": None,
    "last_analyzed_date": None,
    "config": DEFAULT_CONFIG.copy(),
    "event_cache": {},
    "suggestions": [],
    "analysis_log": [],
}


def load_state(path: Optional[str] = None) -> dict:
    """Load state from disk, or return empty state if not found."""
    p = Path(path) if path else DEFAULT_STATE_PATH
    if p.exists():
        try:
            with open(p, "r") as f:
                state = json.load(f)
            # Ensure config has all keys (forward-compat)
            for k, v in DEFAULT_CONFIG.items():
                state.setdefault("config", {})[k] = state.get("config", {}).get(k, v)
            state.setdefault("event_cache", {})
            state.setdefault("suggestions", [])
            state.setdefault("analysis_log", [])
            return state
        except (json.JSONDecodeError, KeyError):
            sys.stderr.write(f"Warning: Corrupt state file at {p}, starting fresh.\n")
            return EMPTY_STATE.copy()
    return EMPTY_STATE.copy()


def save_state(state: dict, path: Optional[str] = None) -> None:
    """Write state to disk atomically."""
    p = Path(path) if path else DEFAULT_STATE_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(".tmp")
    with open(tmp, "w") as f:
        json.dump(state, f, indent=2, default=str)
    tmp.replace(p)


def get_unanalyzed_dates(state: dict, memory_dir: str) -> list[str]:
    """Return list of YYYY-MM-DD dates that have memory files but aren't cached."""
    mem_path = Path(memory_dir)
    if not mem_path.exists():
        return []

    cached = set(state.get("event_cache", {}).keys())
    dates = []
    for f in sorted(mem_path.glob("*.md")):
        date_str = f.stem  # e.g., "2026-03-26"
        if date_str not in cached:
            dates.append(date_str)

    return dates


def get_modified_dates(state: dict, memory_dir: str) -> list[str]:
    """Return dates where the memory file was modified after we last analyzed it.
    
    This catches same-day updates (e.g., memory file grows throughout the day).
    Always includes today's date if a memory file exists for it.
    """
    mem_path = Path(memory_dir)
    if not mem_path.exists():
        return []

    last_analysis = state.get("last_analysis")
    if not last_analysis:
        return []  # No prior analysis — get_unanalyzed_dates handles this

    try:
        last_ts = datetime.fromisoformat(last_analysis).timestamp()
    except (ValueError, TypeError):
        return []

    modified = []
    today_str = datetime.now().strftime("%Y-%m-%d")

    for f in sorted(mem_path.glob("*.md")):
        date_str = f.stem
        # Always re-analyze today's file (it grows throughout the day)
        if date_str == today_str:
            modified.append(date_str)
        elif f.stat().st_mtime > last_ts and date_str in state.get("event_cache", {}):
            modified.append(date_str)

    return modified


def dates_to_analyze(state: dict, memory_dir: str) -> list[str]:
    """Combined: unanalyzed + modified dates. Deduplicated and sorted."""
    unanalyzed = set(get_unanalyzed_dates(state, memory_dir))
    modified = set(get_modified_dates(state, memory_dir))
    return sorted(unanalyzed | modified)


def add_events(state: dict, date_str: str, events: list[dict]) -> None:
    """Add or replace events for a date in the cache."""
    state["event_cache"][date_str] = events


def get_all_events(state: dict) -> list[dict]:
    """Flatten event cache into a single list with date attached."""
    all_events = []
    for date_str, events in sorted(state["event_cache"].items()):
        for ev in events:
            ev_copy = ev.copy()
            ev_copy["date"] = date_str
            all_events.append(ev_copy)
    return all_events


def add_suggestion(state: dict, suggestion: dict) -> None:
    """Add a new suggestion to the state."""
    suggestion.setdefault("status", "pending")
    suggestion.setdefault("first_suggested", datetime.now().isoformat())
    suggestion.setdefault("snooze_until", None)
    suggestion.setdefault("rejection_reason", None)
    state["suggestions"].append(suggestion)


def get_active_suggestions(state: dict) -> list[dict]:
    """Return suggestions that are pending or snoozed-and-ready."""
    now = datetime.now()
    active = []
    for s in state.get("suggestions", []):
        if s["status"] == "pending":
            active.append(s)
        elif s["status"] == "snoozed":
            snooze_until = s.get("snooze_until")
            if snooze_until:
                try:
                    if datetime.fromisoformat(snooze_until) <= now:
                        active.append(s)
                except (ValueError, TypeError):
                    pass
    return active


def update_suggestion(state: dict, suggestion_id: str, 
                      status: str, reason: str = "") -> bool:
    """Update a suggestion's status. Returns True if found."""
    for s in state.get("suggestions", []):
        if s.get("id") == suggestion_id:
            s["status"] = status
            if status == "rejected" and reason:
                s["rejection_reason"] = reason
            if status == "snoozed":
                snooze_days = state.get("config", {}).get("snooze_days", 30)
                s["snooze_until"] = (
                    datetime.now() + timedelta(days=snooze_days)
                ).isoformat()
            s["updated"] = datetime.now().isoformat()
            return True
    return False


def is_duplicate_suggestion(state: dict, title: str, pattern_type: str) -> bool:
    """Check if a similar suggestion already exists (any status)."""
    for s in state.get("suggestions", []):
        if s.get("title", "").lower() == title.lower():
            return True
        # Also check type + similar evidence
        if s.get("type") == pattern_type and s.get("status") in ("accepted", "rejected"):
            # Don't re-suggest accepted or hard-rejected patterns
            if s.get("status") == "rejected":
                return True
            if s.get("status") == "accepted":
                return True
    return False


def should_re_suggest(state: dict, suggestion_id: str, 
                      new_confidence: float) -> bool:
    """Check if a previously snoozed/rejected suggestion should re-surface."""
    for s in state.get("suggestions", []):
        if s.get("id") == suggestion_id:
            if s["status"] == "snoozed":
                snooze_until = s.get("snooze_until")
                if snooze_until:
                    try:
                        if datetime.fromisoformat(snooze_until) <= datetime.now():
                            return True
                    except (ValueError, TypeError):
                        pass
                # Re-suggest if confidence jumped significantly
                old_conf = s.get("confidence", 0)
                if new_confidence - old_conf > 0.2:
                    return True
            elif s["status"] == "rejected":
                # Only re-suggest rejected items at much higher confidence
                old_conf = s.get("confidence", 0)
                if new_confidence >= 0.8 and new_confidence - old_conf > 0.2:
                    return True
    return False


def log_analysis(state: dict, files_analyzed: list[str], 
                 events_extracted: int, clusters_found: int,
                 suggestions_generated: int) -> None:
    """Record this analysis run."""
    state["analysis_log"].append({
        "date": datetime.now().isoformat(),
        "files_analyzed": files_analyzed,
        "events_extracted": events_extracted,
        "clusters_found": clusters_found,
        "suggestions_generated": suggestions_generated,
    })
    state["last_analysis"] = datetime.now().isoformat()
    # Keep only last 20 analysis logs
    if len(state["analysis_log"]) > 20:
        state["analysis_log"] = state["analysis_log"][-20:]


if __name__ == "__main__":
    # Quick state inspection
    import argparse
    parser = argparse.ArgumentParser(description="Inspect crystallizer state")
    parser.add_argument("--state-file", default=None, help="Path to state.json")
    parser.add_argument("--reset", action="store_true", help="Reset state to empty")
    args = parser.parse_args()

    if args.reset:
        save_state(EMPTY_STATE.copy(), args.state_file)
        print("State reset to empty.")
    else:
        state = load_state(args.state_file)
        cached_dates = sorted(state.get("event_cache", {}).keys())
        total_events = sum(len(v) for v in state.get("event_cache", {}).values())
        suggestions = state.get("suggestions", [])
        print(f"Cached dates: {len(cached_dates)} ({', '.join(cached_dates) if cached_dates else 'none'})")
        print(f"Total events: {total_events}")
        print(f"Suggestions: {len(suggestions)}")
        for s in suggestions:
            print(f"  [{s.get('status', '?')}] {s.get('title', '?')} (confidence: {s.get('confidence', '?')})")
        print(f"Last analysis: {state.get('last_analysis', 'never')}")
