#!/usr/bin/env python3
"""
lobster-novel: Character state tracker
Tracks per-chapter character states, relationships, and appearances.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional


@dataclass
class CharacterSnapshot:
    """State of a single character at a given chapter."""
    chapter: int
    name: str
    state: str = "alive"           # alive, injured, captured, transformed, dead
    location: str = ""
    emotional_state: str = ""
    allies_nearby: List[str] = field(default_factory=list)
    enemies_nearby: List[str] = field(default_factory=list)
    new_relationships: Dict[str, str] = field(default_factory=dict)
    notable_actions: List[str] = field(default_factory=list)
    power_level_change: str = ""   # awakened, breakthrough, weakened, etc.
    notes: str = ""


class CharacterTracker:
    """Per-chapter character state history with timeline queries."""

    FILE = "character_timeline.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / self.FILE
        self.timeline: List[CharacterSnapshot] = self._load()

    def _load(self) -> List[CharacterSnapshot]:
        if not self.file.exists():
            return []
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return [CharacterSnapshot(**s) for s in data]
        except Exception:
            return []

    def save(self):
        self.file.write_text(
            json.dumps([asdict(s) for s in self.timeline],
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def record(self, snapshot: CharacterSnapshot):
        """Record a character's state at a chapter."""
        # Remove previous snapshot for same char+chapter if exists
        self.timeline = [
            s for s in self.timeline
            if not (s.name == snapshot.name and s.chapter == snapshot.chapter)
        ]
        self.timeline.append(snapshot)
        self.save()

    def get_state_at(self, name: str, chapter: int) -> Optional[CharacterSnapshot]:
        """Get a character's state at or before chapter."""
        snapshots = [s for s in self.timeline if s.name == name and s.chapter <= chapter]
        if not snapshots:
            return None
        return max(snapshots, key=lambda s: s.chapter)

    def get_history(self, name: str) -> List[CharacterSnapshot]:
        """Get full timeline for a character."""
        return [s for s in self.timeline if s.name == name]

    def get_active_characters(self, chapter: int) -> List[str]:
        """Get all characters that appear at a specific chapter."""
        return list({s.name for s in self.timeline if s.chapter == chapter})

    def get_state_transition(self, name: str, field: str = "state") -> List[tuple]:
        """Get when a character's field changed: [(prev_chapter, prev_value, new_chapter, new_value)]."""
        hist = self.get_history(name)
        if len(hist) < 2:
            return []
        changes = []
        prev = getattr(hist[0], field)
        prev_ch = hist[0].chapter
        for s in hist[1:]:
            curr = getattr(s, field)
            if curr != prev:
                changes.append((prev_ch, prev, s.chapter, curr))
                prev = curr
                prev_ch = s.chapter
        return changes

    def summary(self, chapter: int) -> str:
        """Human-readable summary of all characters at chapter."""
        active = []
        for s in self.timeline:
            if s.chapter > chapter:
                break  # timeline is ordered by chapter
        chars_at_ch = self.get_active_characters(chapter)
        lines = [f"Characters active at ch{chapter}: {len(chars_at_ch)}"]
        for name in sorted(chars_at_ch):
            state = self.get_state_at(name, chapter)
            if state:
                parts = [f"  {name}: {state.state}"]
                if state.location:
                    parts.append(f" @ {state.location}")
                if state.emotional_state:
                    parts.append(f" [{state.emotional_state}]")
                if state.power_level_change:
                    parts.append(f" ⚡{state.power_level_change}")
                lines.append("".join(parts))
        return "\n".join(lines)

    @staticmethod
    def from_bible_snapshots(bible_manager, chapter: int) -> List[CharacterSnapshot]:
        """Generate initial snapshots from bible character current_state."""
        from bible import BibleManager
        snapshots = []
        for name, char in bible_manager.bible.characters.items():
            snapshots.append(CharacterSnapshot(
                chapter=chapter,
                name=name,
                state=char.current_state or "alive",
            ))
        return snapshots
