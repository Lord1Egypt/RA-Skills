"""
domain/events.py — Domain Events (what happened, not what to do)

Dispatch uses class name via @property.
No 'event_type' field in base – breaks frozen dataclass field ordering.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Event:
    """Base domain event."""
    
    @property
    def event_type(self) -> str:
        """CamelCaseEvent → snake_case"""
        name = type(self).__name__
        if name.endswith('Event'):
            name = name[:-5]
        result = []
        for i, c in enumerate(name):
            if c.isupper() and i > 0:
                result.append('_')
            result.append(c.lower())
        return ''.join(result)


@dataclass(frozen=True)
class ChapterCompletedEvent(Event):
    chapter: int
    text_length: int


@dataclass(frozen=True)
class CharacterUpdatedEvent(Event):
    name: str
    updates: Dict[str, Any]


@dataclass(frozen=True)
class HookAddedEvent(Event):
    hook_id: str
    chapter: int


@dataclass(frozen=True)
class HookResolvedEvent(Event):
    hook_id: str
    chapter: int


@dataclass(frozen=True)
class ForeshadowRegisteredEvent(Event):
    foreshadow_id: str
    chapter: int


@dataclass(frozen=True)
class TimelineUpdatedEvent(Event):
    chapter: int
    event: str


@dataclass(frozen=True)
class ReaderStatsUpdatedEvent(Event):
    updates: Dict[str, Any]


@dataclass(frozen=True)
class StateSavedEvent(Event):
    chapter: int
    file_path: str


@dataclass(frozen=True)
class RollbackEvent(Event):
    reason: str
    from_chapter: int
    to_chapter: int
