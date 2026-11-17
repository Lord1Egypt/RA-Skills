"""Domain layer — immutable StateRoot, Commands, Events"""
from .state import StateRoot, Meta, Progress, Character, Plot, Hook, TimelineEntry, ReaderStats
from .state import ForeshadowEntry, GlobalMemoryEntry, PayoffLedgerEntry, CharacterStateEntry
from .state import StoryArc
from .commands import (
    Command, WriteChapterCommand, UpdateCharacterCommand, AddHookCommand,
    ResolveHookCommand, AddForeshadowCommand, RevealForeshadowCommand,
    UpdateTimelineCommand, UpdateReadersCommand, AddWarningCommand,
    AddStoryArcCommand, RecordPayoffCommand, FulfillPayoffCommand,
    SetMetaFieldCommand, SetProgressFieldCommand, UpdateGlobalMemoryCommand,
    UpdateCharacterStateCommand,
)
from .events import (
    Event, ChapterCompletedEvent, CharacterUpdatedEvent, HookAddedEvent,
    HookResolvedEvent, ForeshadowRegisteredEvent, TimelineUpdatedEvent,
    ReaderStatsUpdatedEvent, StateSavedEvent, RollbackEvent,
)

__all__ = [
    'StateRoot', 'Meta', 'Progress', 'Character', 'Plot', 'Hook', 'TimelineEntry', 'ReaderStats',
    'ForeshadowEntry', 'GlobalMemoryEntry', 'PayoffLedgerEntry', 'CharacterStateEntry',
    'StoryArc',
    'Command', 'WriteChapterCommand', 'UpdateCharacterCommand', 'AddHookCommand',
    'ResolveHookCommand', 'AddForeshadowCommand', 'RevealForeshadowCommand',
    'UpdateTimelineCommand', 'UpdateReadersCommand', 'AddWarningCommand',
    'AddStoryArcCommand', 'RecordPayoffCommand', 'FulfillPayoffCommand',
    'SetMetaFieldCommand', 'SetProgressFieldCommand', 'UpdateGlobalMemoryCommand',
    'UpdateCharacterStateCommand',
    'Event', 'ChapterCompletedEvent', 'CharacterUpdatedEvent', 'HookAddedEvent',
    'HookResolvedEvent', 'ForeshadowRegisteredEvent', 'TimelineUpdatedEvent',
    'ReaderStatsUpdatedEvent', 'StateSavedEvent', 'RollbackEvent',
]
