#!/usr/bin/env python3
"""
lobster-novel: Foreshadowing/hook tracker (standalone)
Inspired by novel-writing's foreshadowing tracker.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional


@dataclass
class Hook:
    """A single hook or foreshadowing element."""
    id: str
    description: str
    planted_chapter: int
    expected_payoff_chapter: int
    status: str = "active"         # active, hinted, resolved, abandoned
    importance: str = "normal"     # minor, normal, major, critical
    category: str = "plot"         # plot, character, world, mystery
    resolved_chapter: int = 0
    notes: str = ""

    def overdue_by(self, current_chapter: int) -> int:
        if self.status != "active":
            return 0
        return max(0, current_chapter - self.expected_payoff_chapter)


class ForeshadowTracker:
    """Manages hooks/foreshadowing with overdue detection."""
    FILE = "hooks.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / self.FILE
        self.hooks: List[Hook] = self._load()

    def _load(self) -> List[Hook]:
        if not self.file.exists():
            return []
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return [Hook(**h) for h in data]
        except Exception:
            return []

    def save(self):
        self.file.write_text(
            json.dumps([asdict(h) for h in self.hooks],
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    def plant(self, description: str, chapter: int, payoff_chapter: int,
              category: str = "plot", importance: str = "normal") -> Hook:
        """Register a new hook."""
        hook = Hook(
            id=f"hook-{len(self.hooks) + 1}",
            description=description,
            planted_chapter=chapter,
            expected_payoff_chapter=payoff_chapter,
            category=category,
            importance=importance,
        )
        self.hooks.append(hook)
        self.save()
        return hook

    def resolve(self, hook_id: str, chapter: int):
        """Mark a hook as resolved (paid off)."""
        for h in self.hooks:
            if h.id == hook_id:
                h.status = "resolved"
                h.resolved_chapter = chapter
                break
        self.save()

    def resolve_by_desc(self, description: str, chapter: int):
        """Resolve by description (fuzzy match)."""
        for h in self.hooks:
            if h.status == "active" and description.lower() in h.description.lower():
                h.status = "resolved"
                h.resolved_chapter = chapter
                break
        self.save()

    def hint(self, hook_id: str):
        """Mark a hook as hinted (partial payoff)."""
        for h in self.hooks:
            if h.id == hook_id:
                h.status = "hinted"
                break
        self.save()

    def abandon(self, hook_id: str):
        """Mark a hook as abandoned."""
        for h in self.hooks:
            if h.id == hook_id:
                h.status = "abandoned"
                break
        self.save()

    def get_active(self, current_chapter: int) -> List[Hook]:
        """Get all active hooks, sorted by urgency."""
        active = [h for h in self.hooks if h.status == "active"]
        active.sort(key=lambda h: h.overdue_by(current_chapter), reverse=True)
        return active

    def get_overdue(self, current_chapter: int, threshold: int = 3) -> List[Hook]:
        """Get hooks overdue by threshold+ chapters."""
        return [h for h in self.get_active(current_chapter)
                if h.overdue_by(current_chapter) >= threshold]

    def get_resolved(self) -> List[Hook]:
        return [h for h in self.hooks if h.status == "resolved"]

    def summary(self, current_chapter: int) -> str:
        """Human-readable summary."""
        active = self.get_active(current_chapter)
        overdue = self.get_overdue(current_chapter)
        resolved = self.get_resolved()

        lines = [
            f"Hooks: {len(self.hooks)} total, {len(active)} active, "
            f"{len(overdue)} overdue, {len(resolved)} resolved"
        ]
        if overdue:
            lines.append("\n⚠️ Overdue hooks:")
            for h in overdue:
                lines.append(f"  [{h.importance}] {h.description[:60]} "
                             f"(planted ch{h.planted_chapter}, "
                             f"overdue by {h.overdue_by(current_chapter)} ch)")
        if active:
            lines.append("\nActive hooks:")
            for h in active[:10]:
                lines.append(f"  {h.id}: {h.description[:50]} → due ch{h.expected_payoff_chapter}")
        return "\n".join(lines)
