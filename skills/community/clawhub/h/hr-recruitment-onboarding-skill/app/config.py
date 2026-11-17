import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    workspace_root: Path

    @classmethod
    def from_environment(cls, project_root: Path) -> "Settings":
        raw = os.getenv("OPIE_WORKSPACE")
        root = Path(raw) if raw else project_root / "workspace"
        return cls(root.resolve())
