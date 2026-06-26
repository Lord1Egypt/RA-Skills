#!/usr/bin/env python3
"""
lobster-novel: continuity tracker
"""
import json
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Optional

@dataclass
class ChapterState:
    """State snapshot after a chapter"""
    chapter: int
    summary: str = ""
    changed_characters: Dict[str, str] = field(default_factory=dict)  # name->new_state
    new_facts: List[str] = field(default_factory=list)
    resolved_hooks: List[str] = field(default_factory=list)
    new_hooks: List[str] = field(default_factory=list)
    continuity_risks: List[str] = field(default_factory=list)
    word_count: int = 0

class ContinuityTracker:
    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.state_file = self.dir / "state.jsonl"

    def append(self, state: ChapterState):
        """Append a chapter state record"""
        with open(self.state_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(asdict(state), ensure_ascii=False) + "\n")

    def get_latest(self, n: int = 5) -> List[ChapterState]:
        """Get the last N chapter states"""
        if not self.state_file.exists():
            return []
        with open(self.state_file, encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]
        return [ChapterState(**json.loads(l)) for l in lines[-n:]]

    def get_summary_for(self, chapter: int) -> str:
        """Get context summary up to chapter N"""
        states = self.get_latest(5)
        lines = []
        for s in states:
            if s.chapter > chapter:
                break
            lines.append(f"ch{s.chapter}: {s.summary}")
            if s.changed_characters:
                lines.append(f"  chars: {', '.join(f'{k}={v}' for k,v in s.changed_characters.items())}")
            if s.new_hooks:
                lines.append(f"  new hooks: {', '.join(s.new_hooks)}")
        return "\n".join(lines)

    def get_hook_status(self) -> str:
        """Get all active hooks (resolved hooks excluded)."""
        if not self.state_file.exists():
            return "no hooks"
        with open(self.state_file, encoding="utf-8") as f:
            states = [ChapterState(**json.loads(l)) for l in f if l.strip()]

        # First pass: collect all resolved hooks
        resolved = set()
        for s in states:
            for h in s.resolved_hooks:
                resolved.add(h)

        # Second pass: active = new_hooks not in resolved
        active = []
        seen = set()
        for s in states:
            for h in s.new_hooks:
                if h not in resolved and h not in seen:
                    active.append((s.chapter, h))
                    seen.add(h)

        if not active:
            return "no active hooks"
        return "\n".join(f"  ch{p[0]}: {p[1]}" for p in active[-10:])
