import json

import pytest

from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.file_repository import FileRepository


def test_atomic_write_replaces_valid_json(tmp_path):
    repository = FileRepository(tmp_path)
    path = tmp_path / "positions.json"

    repository.write_json_atomic(path, [{"job_id": "JOB-2026-001"}])

    assert json.loads(path.read_text(encoding="utf-8"))[0]["job_id"] == "JOB-2026-001"


def test_read_json_returns_default_for_a_missing_file(tmp_path):
    repository = FileRepository(tmp_path)
    path = tmp_path / "missing.json"

    assert repository.read_json(path, default=[]) == []


def test_write_json_atomic_rejects_path_outside_repository_root(tmp_path):
    repository = FileRepository(tmp_path / "workspace_data")

    with pytest.raises(HRSkillError) as exc:
        repository.write_json_atomic(tmp_path / "outside.json", [])

    assert exc.value.code == "INVALID_PATH"
    assert exc.value.message == "文件路径必须位于工作区数据目录内。"


def test_atomic_write_removes_temp_file_when_json_serialization_fails(tmp_path):
    repository = FileRepository(tmp_path)

    with pytest.raises(TypeError):
        repository.write_json_atomic(tmp_path / "positions.json", {"bad": object()})

    assert list(tmp_path.iterdir()) == []
