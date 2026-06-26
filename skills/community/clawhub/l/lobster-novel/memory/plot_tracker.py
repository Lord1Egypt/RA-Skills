#!/usr/bin/env python3
"""
lobster-novel: Plot progression tracker
Tracks arc progress, subplot status, pacing, and tension curve.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional


@dataclass
class PlotEvent:
    """A plot event / beat at a given chapter."""
    chapter: int
    event_type: str          # inciting_incident, rising_action, climax, revelation, twist, resolution
    description: str
    arc: str = ""            # which arc this belongs to
    importance: str = "normal"  # minor, normal, major, climax
    subplot: str = ""
    characters_involved: List[str] = field(default_factory=list)
    emotional_impact: str = "neutral"  # positive, negative, neutral, mixed
    pacing: str = "normal"   # slow, normal, fast, intense


@dataclass
class ArcProgress:
    """Progress of an arc."""
    arc_name: str
    arc_number: int
    start_chapter: int
    target_end_chapter: int
    current_chapter: int = 0
    beats_completed: List[str] = field(default_factory=list)
    beats_planned: List[str] = field(default_factory=list)
    status: str = "active"   # planned, active, climax, resolved


class PlotTracker:
    """Tracks plot progression across arcs and chapters."""

    FILE = "plot_timeline.json"
    ARCS_FILE = "arcs_progress.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.dir / self.FILE
        self.arcs_file = self.dir / self.ARCS_FILE
        self.events: List[PlotEvent] = self._load_events()
        self.arcs: List[ArcProgress] = self._load_arcs()

    def _load_events(self) -> List[PlotEvent]:
        if not self.events_file.exists():
            return []
        try:
            data = json.loads(self.events_file.read_text(encoding="utf-8"))
            return [PlotEvent(**e) for e in data]
        except Exception:
            return []

    def _load_arcs(self) -> List[ArcProgress]:
        if not self.arcs_file.exists():
            return []
        try:
            data = json.loads(self.arcs_file.read_text(encoding="utf-8"))
            return [ArcProgress(**a) for a in data]
        except Exception:
            return []

    def save_events(self):
        self.events_file.write_text(
            json.dumps([asdict(e) for e in self.events],
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def save_arcs(self):
        self.arcs_file.write_text(
            json.dumps([asdict(a) for a in self.arcs],
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def add_event(self, event: PlotEvent):
        self.events.append(event)
        self.save_events()

    def add_arc(self, arc: ArcProgress):
        # Replace existing arc with same number
        self.arcs = [a for a in self.arcs if a.arc_number != arc.arc_number]
        self.arcs.append(arc)
        self.save_arcs()

    def update_arc(self, arc_number: int, **kwargs):
        for a in self.arcs:
            if a.arc_number == arc_number:
                for k, v in kwargs.items():
                    if hasattr(a, k):
                        setattr(a, k, v)
                break
        self.save_arcs()

    def get_events_for_chapter(self, chapter: int) -> List[PlotEvent]:
        return [e for e in self.events if e.chapter == chapter]

    def get_events_for_arc(self, arc_name: str) -> List[PlotEvent]:
        return [e for e in self.events if e.arc == arc_name]

    def get_pacing_profile(self, chapter: int, window: int = 3) -> str:
        """Get the dominant pacing over a window of chapters."""
        recent = [e for e in self.events
                  if chapter - window < e.chapter <= chapter]
        if not recent:
            return "normal"
        from collections import Counter
        pacing_counts = Counter(e.pacing for e in recent)
        return pacing_counts.most_common(1)[0][0]

    def get_tension_trend(self, chapter: int) -> str:
        """Estimate tension trajectory: rising, falling, plateau, climax."""
        recent = sorted(
            [e for e in self.events if e.chapter <= chapter],
            key=lambda x: x.chapter
        )[-5:]
        if not recent:
            return "neutral"
        climax_count = sum(1 for e in recent if e.importance == "climax")
        if climax_count >= 2:
            return "climax"
        intense = sum(1 for e in recent if e.pacing == "intense")
        if intense >= 3:
            return "rising"
        slow = sum(1 for e in recent if e.pacing == "slow")
        if slow >= 3:
            return "falling"
        return "plateau"

    def arc_status_summary(self) -> str:
        """Human-readable arc progress summary."""
        lines = ["## Arc Progress"]
        for a in self.arcs:
            pct = (a.current_chapter - a.start_chapter) / max(
                a.target_end_chapter - a.start_chapter, 1) * 100
            pct = min(max(pct, 0), 100)
            beats = f"beats: {len(a.beats_completed)}/{len(a.beats_planned) + len(a.beats_completed)}"
            lines.append(
                f"  Arc {a.arc_number} [{a.status}]: {a.arc_name} "
                f"({pct:.0f}% complete, {beats})"
            )
        if not self.arcs:
            lines.append("  (no arcs defined)")
        return "\n".join(lines)

    def summary(self, chapter: int) -> str:
        """Full plot summary up to chapter."""
        lines = [f"## Plot Status (ch{chapter})"]
        events_here = self.get_events_for_chapter(chapter)
        if events_here:
            lines.append(f"Events at ch{chapter}:")
            for e in events_here:
                lines.append(f"  [{e.event_type}] {e.description[:60]}")
        lines.append(f"Pacing: {self.get_pacing_profile(chapter)}")
        lines.append(f"Tension: {self.get_tension_trend(chapter)}")
        lines.append("")
        lines.append(self.arc_status_summary())
        return "\n".join(lines)

    def init_from_bible(self, bible_manager):
        """Initialize arcs from bible data."""
        from bible import BibleManager
        for arc in bible_manager.bible.arcs:
            ch_list = arc.chapters or []
            ap = ArcProgress(
                arc_name=arc.name or f"Arc {arc.number}",
                arc_number=arc.number,
                start_chapter=ch_list[0] if ch_list else 1,
                target_end_chapter=ch_list[-1] if ch_list else 20,
                status="active",
            )
            self.add_arc(ap)
