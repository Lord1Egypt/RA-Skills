from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from config import ConfigError, load_jobs, load_settings


def test_settings_resolve_database_relative_to_skill_root(tmp_path):
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    settings_path = config_dir / "settings.yaml"
    settings_path.write_text(
        yaml.safe_dump(
            {
                "database_path": "data/recruitment.db",
                "deepseek": {"api_key_env": "DEEPSEEK_API_KEY"},
                "outreach": {
                    "mailbox": "recruiting@example.com",
                    "company_team_intro": "人工智能研发团队",
                    "sender_signature": "招聘团队",
                },
            }
        ),
        encoding="utf-8",
    )

    settings = load_settings(settings_path)

    assert settings.database_path == tmp_path / "data" / "recruitment.db"
    assert settings.deepseek_api_key_env == "DEEPSEEK_API_KEY"
    assert settings.outreach_profile == {
        "mailbox": "recruiting@example.com",
        "company_team_intro": "人工智能研发团队",
        "sender_signature": "招聘团队",
    }


def test_active_job_requires_complete_fields(tmp_path):
    jobs_path = tmp_path / "jobs.yaml"
    jobs_path.write_text(
        yaml.safe_dump(
            {
                "jobs": [
                    {
                        "id": "cv",
                        "title": "视觉算法",
                        "active": True,
                        "responsibilities": ["研发视觉模型"],
                    }
                ]
            }
        ),
        encoding="utf-8",
    )

    with pytest.raises(ConfigError, match="required_skills"):
        load_jobs(jobs_path)


def test_empty_production_jobs_file_is_valid(tmp_path):
    jobs_path = tmp_path / "jobs.yaml"
    jobs_path.write_text("jobs: []\n", encoding="utf-8")

    assert load_jobs(jobs_path) == []
