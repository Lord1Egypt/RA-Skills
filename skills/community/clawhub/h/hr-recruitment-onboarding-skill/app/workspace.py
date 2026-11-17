from pathlib import Path

from .config import Settings
from .exceptions import HRSkillError
from .file_repository import FileRepository


class WorkspaceManager:
    def __init__(self, settings: Settings, repository: FileRepository | None = None) -> None:
        self.settings = settings
        self.repository = repository or FileRepository()
        self.repository.set_root(self.data_root)

    @property
    def data_root(self) -> Path:
        return self.settings.workspace_root / "hr_recruitment_data"

    @property
    def indexes_dir(self) -> Path:
        return self.data_root / "indexes"

    @property
    def positions_dir(self) -> Path:
        return self.data_root / "positions"

    def initialize(self) -> None:
        self.indexes_dir.mkdir(parents=True, exist_ok=True)
        self.positions_dir.mkdir(parents=True, exist_ok=True)
        positions_index = self.indexes_dir / "positions.json"
        if not positions_index.exists():
            self.repository.write_json_atomic(positions_index, [])

    def position_dir(self, job_id: str) -> Path:
        positions_dir = self.positions_dir.resolve()
        candidate = (positions_dir / job_id).resolve()
        try:
            candidate.relative_to(positions_dir)
        except ValueError as error:
            raise HRSkillError(
                "INVALID_PATH",
                "职位目录必须位于工作区 positions 目录内。",
                {"job_id": job_id},
            ) from error
        return candidate
