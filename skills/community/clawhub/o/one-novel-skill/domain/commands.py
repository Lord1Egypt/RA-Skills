"""
domain/commands.py — Command objects (CQS: Commands mutate state)

Dispatch uses class name via @property: WriteChapterCommand → "write_chapter".
No 'type' field in base class – breaks frozen dataclass field ordering in subclasses.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class Command:
    """Base class. Subclass dispatch type is derived from class name."""
    
    @property
    def type(self) -> str:
        """CamelCaseCommand → snake_case"""
        name = type(self).__name__
        if name.endswith('Command'):
            name = name[:-7]
        result = []
        for i, c in enumerate(name):
            if c.isupper() and i > 0:
                result.append('_')
            result.append(c.lower())
        return ''.join(result)


@dataclass(frozen=True)
class WriteChapterCommand(Command):
    chapter: int
    text: str


@dataclass(frozen=True)
class UpdateCharacterCommand(Command):
    name: str
    updates: Dict[str, Any]


@dataclass(frozen=True)
class AddHookCommand(Command):
    hook_id: str
    text: str
    chapter: int
    hook_type: str = "general"
    chapter_target: int = 0


@dataclass(frozen=True)
class ResolveHookCommand(Command):
    hook_id: str
    chapter: int


@dataclass(frozen=True)
class AddForeshadowCommand(Command):
    foreshadow_id: str
    content: str
    chapter: int
    chapter_target: Optional[int] = None


@dataclass(frozen=True)
class RevealForeshadowCommand(Command):
    foreshadow_id: str
    chapter: int


@dataclass(frozen=True)
class UpdateTimelineCommand(Command):
    chapter: int
    event: str


@dataclass(frozen=True)
class UpdateReadersCommand(Command):
    updates: Dict[str, Any]
    read_rate: Optional[float] = None
    sentiment: Optional[str] = None


@dataclass(frozen=True)
class AddWarningCommand(Command):
    warning: str


@dataclass(frozen=True)
class AddStoryArcCommand(Command):
    name: str
    description: str
    start_chapter: int = 0
    end_chapter: int = 0


@dataclass(frozen=True)
class RecordPayoffCommand(Command):
    text: str
    chapter: int


@dataclass(frozen=True)
class FulfillPayoffCommand(Command):
    payoff_id: int
    chapter: int


@dataclass(frozen=True)
class SetMetaFieldCommand(Command):
    key: str
    value: Any


@dataclass(frozen=True)
class SetProgressFieldCommand(Command):
    key: str
    value: Any


@dataclass(frozen=True)
class UpdateGlobalMemoryCommand(Command):
    chapter: int
    summary: str
    key_events: List[str]
    characters_mentioned: List[str]


@dataclass(frozen=True)
class UpdateCharacterStateCommand(Command):
    name: str
    location: str = ""
    emotion: str = ""
    relationship_to_mc: str = ""
    chapter: int = 0
