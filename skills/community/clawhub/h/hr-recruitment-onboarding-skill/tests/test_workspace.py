import pytest

from hr_recruitment_onboarding_skill.app.config import Settings
from hr_recruitment_onboarding_skill.app.exceptions import HRSkillError
from hr_recruitment_onboarding_skill.app.workspace import WorkspaceManager


def test_initialization_creates_positions_index(tmp_path, monkeypatch):
    monkeypatch.setenv("OPIE_WORKSPACE", str(tmp_path / "opie"))
    manager = WorkspaceManager(Settings.from_environment(tmp_path))

    manager.initialize()

    assert (tmp_path / "opie" / "hr_recruitment_data" / "indexes" / "positions.json").exists()


def test_position_dir_rejects_path_that_escapes_positions_directory(tmp_path, monkeypatch):
    monkeypatch.setenv("OPIE_WORKSPACE", str(tmp_path / "opie"))
    manager = WorkspaceManager(Settings.from_environment(tmp_path))

    with pytest.raises(HRSkillError) as exc:
        manager.position_dir("../outside")

    assert exc.value.code == "INVALID_PATH"
