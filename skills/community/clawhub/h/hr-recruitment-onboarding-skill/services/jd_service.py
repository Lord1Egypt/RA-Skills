"""Orchestration for creating a position workspace and its JD artifacts."""

import hashlib
import json
import os
import shutil
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterator

if os.name == "nt":
    import msvcrt
else:
    import fcntl

from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.file_repository import FileRepository
from hr_recruitment_onboarding_skill.app.validation import (
    validate_generate_jd_request,
)
from hr_recruitment_onboarding_skill.app.workspace import WorkspaceManager
from hr_recruitment_onboarding_skill.services.jd_renderer import render_jd
from hr_recruitment_onboarding_skill.services.llm_service import (
    LLMService,
    ModelGenerationError,
)
from hr_recruitment_onboarding_skill.services.rule_based_extractor import (
    RuleBasedExtractor,
    sanitize_requirements,
)


class JDService:
    """Create all persistent artifacts for one validated position request."""

    INDEX_LOCK_TIMEOUT_SECONDS = 75.0
    INDEX_LOCK_RETRY_SECONDS = 0.05

    def __init__(
        self,
        project_root: Path,
        workspace: WorkspaceManager,
        repository: FileRepository,
        llm_service: LLMService | None = None,
        extractor: RuleBasedExtractor | None = None,
    ) -> None:
        self.project_root = project_root
        self.workspace = workspace
        self.repository = repository
        self.llm_service = llm_service or LLMService(None, None, None)
        self.extractor = extractor or RuleBasedExtractor()

    @property
    def positions_index(self) -> Path:
        return self.workspace.indexes_dir / "positions.json"

    def create_position(self, request: dict) -> dict:
        """Validate a request, persist its artifacts, and atomically update the index."""
        request = validate_generate_jd_request(request)
        directory = self.workspace.position_dir(request["job_id"])

        # Detect an orphaned or already-created position before initialization so a
        # duplicate request cannot change even a missing global index.
        if directory.exists():
            self._raise_duplicate(request["job_id"])

        with self._positions_index_lock():
            self.workspace.initialize()
            index = self._read_positions_index()
            if any(item.get("job_id") == request["job_id"] for item in index):
                self._raise_duplicate(request["job_id"])

            requirements, source, warnings = self._generate_requirements(request)
            now = datetime.now(timezone.utc).isoformat()
            position = {
                **request,
                "status": "recruiting",
                "requirements": requirements,
                "generation_source": source,
                "created_at": now,
                "updated_at": now,
            }

            try:
                directory.mkdir(parents=True, exist_ok=False)
            except FileExistsError:
                self._raise_duplicate(request["job_id"])

            position_path = directory / "position.json"
            jd_path = directory / "jd.md"
            talent_pool_path = directory / "talent_pool.json"
            try:
                self.repository.write_json_atomic(position_path, position)
                jd_path.write_text(render_jd(position), encoding="utf-8")
                self.repository.write_json_atomic(talent_pool_path, [])
                (directory / "applications").mkdir()

                index.append(self._index_entry(position))
                self.repository.write_json_atomic(self.positions_index, index)
            except Exception:
                shutil.rmtree(directory)
                raise

        return {
            "position": position,
            "generation_source": source,
            "generated_files": [
                self._relative_path(position_path),
                self._relative_path(jd_path),
                self._relative_path(talent_pool_path),
            ],
            "warnings": warnings,
        }

    @property
    def _index_lock_path(self) -> Path:
        normalized = os.path.normcase(os.path.abspath(self.positions_index))
        digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
        return Path(tempfile.gettempdir()) / f"hr-skill-positions-{digest}.lock"

    @contextmanager
    def _positions_index_lock(self) -> Iterator[None]:
        try:
            handle = self._index_lock_path.open("a+b")
        except OSError as error:
            raise self._index_lock_error() from error

        with handle:
            if os.name == "nt":
                handle.seek(0, os.SEEK_END)
                if handle.tell() == 0:
                    handle.write(b"\0")
                    handle.flush()

            deadline = time.monotonic() + self.INDEX_LOCK_TIMEOUT_SECONDS
            while not self._try_acquire_index_lock(handle):
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise self._index_lock_error()
                time.sleep(min(self.INDEX_LOCK_RETRY_SECONDS, remaining))

            try:
                yield
            finally:
                self._release_index_lock(handle)

    @staticmethod
    def _try_acquire_index_lock(handle: BinaryIO) -> bool:
        try:
            if os.name == "nt":
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return False
        return True

    @staticmethod
    def _release_index_lock(handle: BinaryIO) -> None:
        if os.name == "nt":
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    @staticmethod
    def _index_lock_error() -> HRSkillError:
        return HRSkillError(
            "POSITION_INDEX_BUSY",
            "职位索引正被其他操作占用，请稍后重试。",
        )

    def _read_positions_index(self) -> list[dict]:
        try:
            index = self.repository.read_json(self.positions_index, [])
        except (json.JSONDecodeError, UnicodeError) as error:
            raise HRSkillError(
                "CORRUPT_POSITION_INDEX",
                "职位索引不是有效的 JSON，请检查后重试。",
            ) from error

        if not isinstance(index, list) or not all(
            isinstance(item, dict) for item in index
        ):
            raise HRSkillError(
                "CORRUPT_POSITION_INDEX",
                "职位索引格式无效，请检查后重试。",
            )
        return index

    def _generate_requirements(self, request: dict) -> tuple[dict, str, list[str]]:
        if self.llm_service.is_configured():
            try:
                requirements = self.llm_service.generate_requirements(
                    request,
                    (self.project_root / "prompts" / "jd_generation.md").read_text(
                        encoding="utf-8"
                    ),
                )
                return sanitize_requirements(requirements), "llm", []
            except ModelGenerationError:
                warning = "模型生成失败，已使用本地规则生成，请 HR 核对结果。"
        else:
            warning = "未配置模型，已使用本地规则生成，请 HR 核对结果。"

        requirements = self.extractor.extract(request["description"])
        return sanitize_requirements(requirements), "rules_fallback", [warning]

    def _index_entry(self, position: dict) -> dict:
        return {
            "job_id": position["job_id"],
            "job_title": position["job_title"],
            "department": position["department"],
            "location": position["location"],
            "status": position["status"],
            "path": (
                f"hr_recruitment_data/positions/{position['job_id']}/position.json"
            ),
            "updated_at": position["updated_at"],
        }

    def _relative_path(self, path: Path) -> str:
        normalized_path = self.repository._normalized_resolved_path(path)
        normalized_root = self.repository._normalized_resolved_path(
            self.workspace.settings.workspace_root
        )
        return normalized_path.relative_to(normalized_root).as_posix()

    @staticmethod
    def _raise_duplicate(job_id: str) -> None:
        raise HRSkillError(
            "DUPLICATE_JOB_ID",
            f"职位编号 {job_id} 已存在。",
            {"job_id": job_id},
        )
