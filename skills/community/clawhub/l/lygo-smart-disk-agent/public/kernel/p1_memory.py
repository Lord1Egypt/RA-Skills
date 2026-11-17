"""P1 mycelium — append-only JSONL memory for Smart Disk."""
from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any


class P1Memory:
    def __init__(self, root: Path, max_events: int = 500):
        self.path = root / "mycelium" / "events.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.max_events = max_events

    def store(self, bundle: dict[str, Any]) -> str:
        mid = str(uuid.uuid4())
        row = {
            "id": mid,
            "ts": time.time(),
            "bundle": bundle,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        self._rotate()
        return mid

    def list_recent(self, n: int = 20) -> list[dict[str, Any]]:
        if not self.path.is_file():
            return []
        lines = self.path.read_text(encoding="utf-8", errors="ignore").splitlines()
        out = []
        for line in lines[-n:]:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        return list(reversed(out))

    def _rotate(self) -> None:
        if not self.path.is_file():
            return
        lines = self.path.read_text(encoding="utf-8", errors="ignore").splitlines()
        if len(lines) <= self.max_events:
            return
        self.path.write_text("\n".join(lines[-self.max_events :]) + "\n", encoding="utf-8")
