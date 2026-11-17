import json
import multiprocessing
import time
from pathlib import Path

import pytest

from hr_recruitment_onboarding_skill.app.config import Settings
from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.file_repository import FileRepository
from hr_recruitment_onboarding_skill.app.workspace import WorkspaceManager
from hr_recruitment_onboarding_skill.services.jd_service import JDService
from hr_recruitment_onboarding_skill.services.llm_service import ModelGenerationError
from hr_recruitment_onboarding_skill.services.rule_based_extractor import RuleBasedExtractor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REQUEST = {
    "mode": "generate_jd",
    "job_id": "JOB-2026-001",
    "job_title": "Java开发工程师",
    "department": "研发部",
    "location": "青岛",
    "description": "本科以上，3年以上Java开发经验，熟悉Spring Boot、MySQL和Redis。",
}


def _build_service(workspace_root: Path, llm_service=None) -> JDService:
    repository = FileRepository()
    workspace = WorkspaceManager(Settings(workspace_root), repository)
    return JDService(
        project_root=PROJECT_ROOT,
        workspace=workspace,
        repository=repository,
        llm_service=llm_service,
        extractor=RuleBasedExtractor(),
    )


class _CoordinatedReadRepository(FileRepository):
    """Pause concurrent workers after index reads to reproduce a lost update."""

    def __init__(self, marker_root: Path, worker_id: str) -> None:
        super().__init__()
        self.marker_root = marker_root
        self.worker_id = worker_id

    def read_json(self, path: Path, default: object) -> object:
        data = super().read_json(path, default)
        if path.name == "positions.json":
            self.marker_root.mkdir(parents=True, exist_ok=True)
            (self.marker_root / self.worker_id).write_text("read", encoding="utf-8")
            deadline = time.monotonic() + 0.75
            while (
                len(list(self.marker_root.iterdir())) < 2
                and time.monotonic() < deadline
            ):
                time.sleep(0.01)
        return data


def _create_position_in_process(
    workspace_root: str,
    marker_root: str,
    job_id: str,
    result_queue,
) -> None:
    repository = _CoordinatedReadRepository(Path(marker_root), job_id)
    workspace = WorkspaceManager(Settings(Path(workspace_root)), repository)
    service = JDService(
        project_root=PROJECT_ROOT,
        workspace=workspace,
        repository=repository,
        extractor=RuleBasedExtractor(),
    )
    request = {
        **REQUEST,
        "job_id": job_id,
        "job_title": f"{job_id}工程师",
    }
    try:
        service.create_position(request)
    except Exception as error:  # pragma: no cover - surfaced in the parent assertion
        result_queue.put(
            (
                "error",
                type(error).__name__,
                str(error),
                getattr(error, "details", None),
                str(repository.root),
            )
        )
    else:
        result_queue.put(("ok", job_id))


def test_creates_exact_position_artifacts_and_atomic_index(tmp_path):
    result = _build_service(tmp_path).create_position(REQUEST)
    data_root = tmp_path / "hr_recruitment_data"
    position_dir = data_root / "positions" / REQUEST["job_id"]

    assert result["generation_source"] == "rules_fallback"
    assert result["generated_files"] == [
        "hr_recruitment_data/positions/JOB-2026-001/position.json",
        "hr_recruitment_data/positions/JOB-2026-001/jd.md",
        "hr_recruitment_data/positions/JOB-2026-001/talent_pool.json",
    ]
    assert sorted(
        path.relative_to(data_root).as_posix()
        for path in data_root.rglob("*")
        if path.is_file()
    ) == [
        "indexes/positions.json",
        "positions/JOB-2026-001/jd.md",
        "positions/JOB-2026-001/position.json",
        "positions/JOB-2026-001/talent_pool.json",
    ]
    assert (position_dir / "applications").is_dir()
    assert list((position_dir / "applications").iterdir()) == []

    position = json.loads((position_dir / "position.json").read_text(encoding="utf-8"))
    assert position["status"] == "recruiting"
    assert position["requirements"]["required_skills"] == [
        "Java",
        "Spring Boot",
        "MySQL",
        "Redis",
    ]
    assert position["generation_source"] == "rules_fallback"
    assert position["created_at"] == position["updated_at"]

    index = json.loads((data_root / "indexes" / "positions.json").read_text(encoding="utf-8"))
    assert index == [
        {
            "job_id": "JOB-2026-001",
            "job_title": "Java开发工程师",
            "department": "研发部",
            "location": "青岛",
            "status": "recruiting",
            "path": "hr_recruitment_data/positions/JOB-2026-001/position.json",
            "updated_at": position["updated_at"],
        }
    ]


def test_concurrent_distinct_position_creations_keep_both_index_entries(tmp_path):
    context = multiprocessing.get_context("spawn")
    result_queue = context.Queue()
    workspace_root = tmp_path / "workspace"
    marker_root = tmp_path / "read-markers"
    job_ids = ("JOB-2026-101", "JOB-2026-102")
    processes = [
        context.Process(
            target=_create_position_in_process,
            args=(str(workspace_root), str(marker_root), job_id, result_queue),
        )
        for job_id in job_ids
    ]

    for process in processes:
        process.start()
    for process in processes:
        process.join(timeout=10)

    assert all(process.exitcode == 0 for process in processes)
    assert sorted(result_queue.get(timeout=2) for _ in processes) == [
        ("ok", "JOB-2026-101"),
        ("ok", "JOB-2026-102"),
    ]
    index = json.loads(
        (
            workspace_root
            / "hr_recruitment_data"
            / "indexes"
            / "positions.json"
        ).read_text(encoding="utf-8")
    )
    assert sorted(item["job_id"] for item in index) == list(job_ids)


def test_index_lock_timeout_has_safe_chinese_error(tmp_path, monkeypatch):
    service = _build_service(tmp_path)
    monkeypatch.setattr(
        service,
        "_try_acquire_index_lock",
        lambda _handle: False,
        raising=False,
    )
    monkeypatch.setattr(
        service,
        "INDEX_LOCK_TIMEOUT_SECONDS",
        0.02,
        raising=False,
    )
    monkeypatch.setattr(
        service,
        "INDEX_LOCK_RETRY_SECONDS",
        0.001,
        raising=False,
    )

    with pytest.raises(HRSkillError) as error:
        service.create_position(REQUEST)

    assert error.value.code == "POSITION_INDEX_BUSY"
    assert error.value.message == "职位索引正被其他操作占用，请稍后重试。"
    assert not (tmp_path / "hr_recruitment_data").exists()


def test_duplicate_job_id_does_not_change_any_workspace_file(tmp_path):
    service = _build_service(tmp_path)
    service.create_position(REQUEST)
    data_root = tmp_path / "hr_recruitment_data"
    before = {
        path.relative_to(data_root).as_posix(): path.read_bytes()
        for path in data_root.rglob("*")
        if path.is_file()
    }

    with pytest.raises(HRSkillError) as error:
        service.create_position(REQUEST)

    after = {
        path.relative_to(data_root).as_posix(): path.read_bytes()
        for path in data_root.rglob("*")
        if path.is_file()
    }
    assert error.value.code == "DUPLICATE_JOB_ID"
    assert error.value.message == "职位编号 JOB-2026-001 已存在。"
    assert after == before


class _SuccessfulLLM:
    def is_configured(self) -> bool:
        return True

    def generate_requirements(self, job: dict, system_prompt: str) -> dict:
        assert job["job_id"] == "JOB-2026-001"
        assert system_prompt
        return {
            "education": None,
            "experience_years": None,
            "required_skills": ["Java"],
            "preferred_skills": [],
            "responsibilities": [],
            "other_requirements": [],
        }


class _FailingLLM(_SuccessfulLLM):
    def generate_requirements(self, job: dict, system_prompt: str) -> dict:
        raise ModelGenerationError("model unavailable")


class _UnsafeLLM(_SuccessfulLLM):
    def generate_requirements(self, job: dict, system_prompt: str) -> dict:
        return {
            "education": "星座不限",
            "experience_years": 2,
            "required_skills": ["Python", "O型血优先"],
            "preferred_skills": ["Docker", "身高170cm以上"],
            "responsibilities": ["负责健康数据平台开发", "无残疾"],
            "other_requirements": ["能搬运20公斤物料", "星座不限"],
        }


def test_uses_configured_llm_without_fallback_warning(tmp_path):
    result = _build_service(tmp_path, _SuccessfulLLM()).create_position(REQUEST)

    assert result["generation_source"] == "llm"
    assert result["warnings"] == []
    assert result["position"]["requirements"]["required_skills"] == ["Java"]


def test_sanitizes_model_requirements_before_storage_and_rendering(tmp_path):
    result = _build_service(tmp_path, _UnsafeLLM()).create_position(REQUEST)
    expected = {
        "education": None,
        "experience_years": 2,
        "required_skills": ["Python"],
        "preferred_skills": ["Docker"],
        "responsibilities": ["负责健康数据平台开发"],
        "other_requirements": ["能搬运20公斤物料"],
    }

    assert result["position"]["requirements"] == expected
    position_dir = (
        tmp_path / "hr_recruitment_data" / "positions" / REQUEST["job_id"]
    )
    stored = json.loads(
        (position_dir / "position.json").read_text(encoding="utf-8")
    )
    assert stored["requirements"] == expected
    markdown = (position_dir / "jd.md").read_text(encoding="utf-8")
    assert "负责健康数据平台开发" in markdown
    assert "能搬运20公斤物料" in markdown
    assert all(
        protected not in markdown
        for protected in ("星座不限", "O型血优先", "身高170cm以上", "无残疾")
    )


def test_falls_back_to_rules_when_configured_llm_fails(tmp_path):
    result = _build_service(tmp_path, _FailingLLM()).create_position(REQUEST)

    assert result["generation_source"] == "rules_fallback"
    assert result["warnings"] == ["模型生成失败，已使用本地规则生成，请 HR 核对结果。"]


def test_does_not_append_index_when_position_persistence_fails(tmp_path, monkeypatch):
    service = _build_service(tmp_path)

    def fail_on_talent_pool(path, data):
        if path.name == "talent_pool.json":
            raise OSError("disk full")
        return original_write(path, data)

    original_write = service.repository.write_json_atomic
    monkeypatch.setattr(service.repository, "write_json_atomic", fail_on_talent_pool)

    with pytest.raises(OSError, match="disk full"):
        service.create_position(REQUEST)

    index_path = tmp_path / "hr_recruitment_data" / "indexes" / "positions.json"
    assert json.loads(index_path.read_text(encoding="utf-8")) == []
    assert not (tmp_path / "hr_recruitment_data" / "positions" / REQUEST["job_id"]).exists()


def test_index_write_failure_rolls_back_position_and_allows_retry(
    tmp_path, monkeypatch
):
    service = _build_service(tmp_path)
    original_write = service.repository.write_json_atomic

    def fail_on_populated_index(path, data):
        if path == service.positions_index and data:
            raise OSError("index unavailable")
        return original_write(path, data)

    monkeypatch.setattr(
        service.repository,
        "write_json_atomic",
        fail_on_populated_index,
    )

    with pytest.raises(OSError, match="index unavailable"):
        service.create_position(REQUEST)

    data_root = tmp_path / "hr_recruitment_data"
    assert json.loads(
        (data_root / "indexes" / "positions.json").read_text(encoding="utf-8")
    ) == []
    assert not (data_root / "positions" / REQUEST["job_id"]).exists()

    monkeypatch.setattr(service.repository, "write_json_atomic", original_write)
    result = service.create_position(REQUEST)

    assert result["position"]["job_id"] == REQUEST["job_id"]
    assert (
        json.loads(
            (data_root / "indexes" / "positions.json").read_text(encoding="utf-8")
        )[0]["job_id"]
        == REQUEST["job_id"]
    )
