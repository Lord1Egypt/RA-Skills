"""阶段 checkpoint，支持失败续跑."""
from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field, asdict


STEPS = [
    "script",
    "characters",
    "storyboard",
    "videos",
    "dubs",
    "lipsync",
    "bgm",
    "subtitle",
    "edit",
]


@dataclass
class Checkpoint:
    project_dir: pathlib.Path
    status: dict = field(default_factory=dict)

    def __post_init__(self):
        self.project_dir = pathlib.Path(self.project_dir)
        self._load()

    def _path(self) -> pathlib.Path:
        return self.project_dir / ".checkpoint.json"

    def _load(self) -> None:
        if self._path().exists():
            self.status = json.loads(self._path().read_text())
        else:
            self.status = {s: "pending" for s in STEPS}

    def save(self) -> None:
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self._path().write_text(json.dumps(self.status, ensure_ascii=False, indent=2))

    def is_done(self, step: str) -> bool:
        return self.status.get(step) == "done"

    def mark_done(self, step: str) -> None:
        self.status[step] = "done"
        self.save()

    def mark_running(self, step: str) -> None:
        self.status[step] = "running"
        self.save()

    def mark_failed(self, step: str, reason: str = "") -> None:
        self.status[step] = f"failed: {reason}" if reason else "failed"
        self.save()

    def next_pending(self) -> str | None:
        for s in STEPS:
            v = self.status.get(s, "pending")
            if v != "done":
                return s
        return None

    def sub_mark(self, step: str, sub_id: str, value: str = "done") -> None:
        """用于镜头级别的细粒度 checkpoint，如 videos.S01=done."""
        key = f"{step}.{sub_id}"
        self.status[key] = value
        self.save()

    def sub_done(self, step: str, sub_id: str) -> bool:
        return self.status.get(f"{step}.{sub_id}") == "done"
