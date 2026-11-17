"""
adapters/state_adapter.py — Backward-compatible NovelState wrapper

Wraps the existing NovelState API and delegates to StateRepository.
Provides write-protection: all _state mutations are tracked via set() method.

Deprecation: Direct _state access will emit DeprecationWarning.
Migration target: All new code should use StateRepository + UnitOfWork directly.
"""
from __future__ import annotations

import logging
import warnings
from typing import Optional, Dict, Any, List
from pathlib import Path

from domain.state import StateRoot
from dataclasses import replace as dc_replace
from infrastructure.state_repository import StateRepository
from infrastructure.persistence_gateway import PersistenceGateway

_log = logging.getLogger("state_adapter")


class StateAdapter:
    """
    Backward-compatible wrapper around the old NovelState interface.
    
    Internal delegates to StateRepository (single source of truth).
    External API mimics the old NovelState methods for drop-in compatibility.
    
    Migration path:
    1. Old code continues using StateAdapter via NovelState internals
    2. New code uses StateRepository + UnitOfWork directly
    3. Eventually remove this adapter
    """

    _WRITE_LOG: List[Dict[str, Any]] = []  # Audit log of all state mutations
    _MAX_LOG_SIZE = 500

    def __init__(self, book_dir: str):
        self.book_dir = Path(book_dir).resolve()
        self._state_repo = StateRepository(book_dir)
        self._persistence = PersistenceGateway(book_dir)
        self._state_root: StateRoot = self._state_repo.load()

    # ─── Write-protected state access ───

    def set(self, key: str, value: Any):
        """Set a top-level state field with audit logging."""
        old_value = getattr(self._state_root, key, None)
        self._audit("set", key, old_value, value)
        # We can't mutate StateRoot (it's frozen), so we build a new dict and reload
        data = self._state_root.to_dict()
        data[key] = value
        self._state_root = StateRoot.from_dict(data)
        self._state_repo.save(self._state_root)

    def set_meta_field(self, key: str, value: Any):
        """Set a meta field."""
        self._audit("set_meta", key, None, value)
        new_meta = replace_meta(self._state_root.meta, **{key: value})
        self._state_root = dc_replace(self._state_root, meta=new_meta)
        self._state_repo.save(self._state_root)

    def set_progress_field(self, key: str, value: Any):
        """Set a progress field."""
        self._audit("set_progress", key, None, value)
        from domain.state import Progress
        new_progress = replace_object(self._state_root.progress, **{key: value})
        self._state_root = dc_replace(self._state_root, progress=new_progress)
        self._state_repo.save(self._state_root)

    def set_character(self, name: str, data: dict):
        """Set character data."""
        self._audit("set_character", name, None, data)
        from domain.state import Character
        chars = dict(self._state_root.characters)
        chars[name] = Character.from_dict(dict(name=name, **data))
        self._state_root = dc_replace(self._state_root, characters=chars)
        self._state_repo.save(self._state_root)

    def update_character(self, name: str, **kw):
        """Update character fields."""
        chars = dict(self._state_root.characters)
        if name in chars:
            old = chars[name]
            updated = {k: v for k, v in kw.items() if v is not None}
            chars[name] = replace_object(old, **updated)
            self._audit("update_character", name, None, updated)
            self._state_root = dc_replace(self._state_root, characters=chars)
            self._state_repo.save(self._state_root)

    def add_hook(self, hook: Any = None, ch: int = 0, ht: str = "general"):
        """Add a story hook."""
        from domain.state import Hook
        hooks = list(self._state_root.plot.hooks)
        hooks.append(Hook(
            hook_id=f"h{len(hooks):04d}",
            text=str(hook) if hook else "",
            hook_type=ht,
            chapter_planted=ch,
        ))
        new_plot = replace_object(self._state_root.plot, hooks=hooks)
        self._state_root = dc_replace(self._state_root, plot=new_plot)
        self._state_repo.save(self._state_root)

    def mark_chapter_done(self, ch: int):
        """Mark a chapter as completed."""
        from domain.state import Progress
        new_progress = replace_object(self._state_root.progress,
            written=ch, last_chapter=ch)
        self._state_root = dc_replace(self._state_root, progress=new_progress)
        self._state_repo.save(self._state_root)

    def add_timeline_event(self, ch: int, ev: str):
        """Add timeline event."""
        from domain.state import TimelineEntry
        tl = list(self._state_root.timeline)
        tl.append(TimelineEntry(chapter=ch, event=ev))
        self._state_root = dc_replace(self._state_root, timeline=tl)
        self._state_repo.save(self._state_root)

    def update_readers(self, **kw):
        """Update reader stats."""
        from domain.state import ReaderStats
        new_readers = replace_object(self._state_root.readers, **kw)
        self._state_root = dc_replace(self._state_root, readers=new_readers)
        self._state_repo.save(self._state_root)

    # ─── Read methods (delegated from StateRoot) ───

    @property
    def meta(self):
        return self._state_root.meta

    @property
    def progress(self):
        return self._state_root.progress

    def get_character(self, name: str):
        return self._state_root.characters.get(name)

    def all_characters(self):
        return dict(self._state_root.characters)

    def hooks_list(self):
        return self._state_root.plot.hooks

    def unresolved_hooks(self):
        return [h for h in self._state_root.plot.hooks if h.status != "resolved"]

    def timeline_events(self):
        return self._state_root.timeline

    def written_chapters(self):
        return self._state_root.progress.written

    def total_planned(self):
        return self._state_root.progress.total_planned

    def last_chapter(self):
        return self._state_root.progress.last_chapter

    def next_chapter(self):
        return self._state_root.progress.last_chapter + 1

    # ─── Snapshot / Rollback ───

    def save_snapshot(self):
        """Save state snapshot for rollback."""
        self._state_repo.snapshot(self._state_root.progress.last_chapter)

    def rollback_state(self, chapter: Optional[int] = None):
        """Rollback to a snapshot."""
        ch = chapter or self._state_root.progress.last_chapter
        new_state, event = self._state_repo.rollback(ch)
        self._state_root = new_state
        return new_state, event

    # ─── Persistence ───

    def save(self):
        """Persist current state to disk."""
        self._state_repo.save(self._state_root)

    def reload_from_disk(self):
        """Force reload state from disk (for rollback guard)."""
        self._state_root = self._state_repo.load()
        _log.info("State force-reloaded from disk")

    # ─── Audit log ───

    def _audit(self, op: str, key: str, old: Any, new: Any):
        entry = {"op": op, "key": key, "old": str(old)[:100], "new": str(new)[:100]}
        self._WRITE_LOG.append(entry)
        if len(self._WRITE_LOG) > self._MAX_LOG_SIZE:
            self._WRITE_LOG = self._WRITE_LOG[-self._MAX_LOG_SIZE:]

    @classmethod
    def write_log(cls) -> List[Dict]:
        return list(cls._WRITE_LOG)


# ─── Helper: dataclass replace that works with our frozen dataclasses ───

def replace_object(obj, **kwargs):
    """Safely create a new instance of a dataclass with updated fields."""
    import dataclasses
    if hasattr(obj, '_fields'):  # namedtuple?
        return obj._replace(**kwargs)
    current = {f.name: getattr(obj, f.name) for f in dataclasses.fields(obj)}
    current.update(kwargs)
    return type(obj)(**current)


def replace_meta(obj, **kwargs):
    """Replace fields on Meta dataclass."""
    import dataclasses
    current = {f.name: getattr(obj, f.name) for f in dataclasses.fields(obj)}
    current.update(kwargs)
    return type(obj)(**current)
