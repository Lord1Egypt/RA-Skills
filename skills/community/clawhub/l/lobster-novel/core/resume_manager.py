#!/usr/bin/env python3
"""
lobster-novel: Resume/checkpoint manager (inspired by fiction-crafter).
Saves progress state for crash recovery and interrupt/resume.
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict
from datetime import datetime


@dataclass
class Checkpoint:
    """A snapshot of writing progress."""
    project_dir: str
    current_chapter: int = 0
    total_chapters_planned: int = 0
    arc_number: int = 0
    last_action: str = ""          # written / saved / reviewed / exported
    last_timestamp: str = ""
    pending_chapters: List[int] = field(default_factory=list)
    failed_chapters: List[Dict] = field(default_factory=list)  # [{chapter, error, time}]
    notes: str = ""


class ResumeManager:
    """Manage checkpoints for crash recovery and interrupt/resume."""

    FILE = "resume_state.json"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir)
        self.file = self.dir / self.FILE
        self.state: Checkpoint = self._load()

    def _load(self) -> Checkpoint:
        if not self.file.exists():
            return Checkpoint(project_dir=str(self.dir))
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            return Checkpoint(**data)
        except Exception:
            return Checkpoint(project_dir=str(self.dir))

    def save(self):
        self.state.last_timestamp = datetime.now().isoformat()
        self.file.write_text(
            json.dumps(asdict(self.state), ensure_ascii=False, indent=2),
            encoding="utf-8")

    def mark_written(self, chapter: int):
        self.state.current_chapter = chapter
        self.state.last_action = "written"
        if chapter in self.state.pending_chapters:
            self.state.pending_chapters.remove(chapter)
        self.save()

    def mark_reviewed(self, chapter: int):
        self.state.last_action = f"reviewed ch{chapter}"
        self.save()

    def mark_exported(self, fmt: str):
        self.state.last_action = f"exported to {fmt}"
        self.save()

    def record_failure(self, chapter: int, error: str):
        self.state.failed_chapters.append({
            "chapter": chapter,
            "error": str(error)[:200],
            "time": datetime.now().isoformat(),
        })
        self.save()

    def set_pending(self, chapters: List[int]):
        self.state.pending_chapters = chapters
        self.save()

    def clear_failures(self):
        self.state.failed_chapters = []
        self.save()

    @property
    def has_unsaved_work(self) -> bool:
        """Check if last action could have pending unsaved work."""
        return self.state.last_action in ("written",)

    @property
    def needs_review(self) -> List[int]:
        """Return chapters written but not yet reviewed."""
        reviewed = self.state.last_action
        if reviewed.startswith("reviewed ch"):
            reviewed_ch = int(reviewed.split("ch")[1])
            return [c for c in range(1, self.state.current_chapter + 1) if c > reviewed_ch]
        return []

    def status_text(self) -> str:
        """Human-readable status."""
        state = self.state
        lines = [
            "## Resume State",
            f"Current chapter: {state.current_chapter}",
            f"Planned total:   {state.total_chapters_planned}",
            f"Last action:     {state.last_action or 'none'}",
            f"Last timestamp:  {state.last_timestamp or 'never'}",
        ]
        if state.pending_chapters:
            lines.append(f"Pending:         ch{', '.join(str(c) for c in state.pending_chapters)}")
        if state.failed_chapters:
            lines.append(f"Failures:        {len(state.failed_chapters)}")
            for f in state.failed_chapters[-3:]:
                lines.append(f"  ch{f['chapter']}: {f['error'][:60]}")
        if self.needs_review:
            lines.append(f"Needs review:    ch{', '.join(str(c) for c in self.needs_review)}")
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="resume/checkpoint manager")
    parser.add_argument("--dir", default="./my-novel")
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("status", help="show current state")
    p_mark = sub.add_parser("mark", help="mark chapter as written")
    p_mark.add_argument("chapter", type=int)

    args = parser.parse_args()
    rm = ResumeManager(Path(args.dir))

    if args.cmd == "status":
        print(rm.status_text())
    elif args.cmd == "mark":
        rm.mark_written(args.chapter)
        print(f"✅ Marked ch{args.chapter} as written")
