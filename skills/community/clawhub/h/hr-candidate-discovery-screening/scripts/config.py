from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Settings:
    skill_root: Path
    database_path: Path
    retention_days: int
    deepseek_base_url: str
    deepseek_model: str
    deepseek_api_key_env: str
    thinking_enabled: bool
    reasoning_effort: str
    timeout_seconds: int
    max_attempts: int
    followup_days: tuple[int, ...]
    outreach_profile: dict[str, str]


REQUIRED_ACTIVE_JOB_FIELDS = (
    "id",
    "title",
    "responsibilities",
    "required_skills",
    "preferred_skills",
    "education_hard",
    "education_preferred",
    "research_areas",
    "application_scenarios",
    "locations",
    "outreach",
)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise ConfigError(f"Configuration file not found: {path}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ConfigError(f"Configuration root must be a mapping: {path}")
    return data


def load_settings(path: str | Path) -> Settings:
    settings_path = Path(path).resolve()
    skill_root = settings_path.parent.parent
    load_dotenv(skill_root / ".env", override=False)
    data = _load_yaml(settings_path)
    deepseek = data.get("deepseek", {})
    workflow = data.get("workflow", {})
    outreach = data.get("outreach", {})
    database_value = data.get("database_path", "data/recruitment.db")
    database_path = Path(database_value)
    if not database_path.is_absolute():
        database_path = skill_root / database_path
    return Settings(
        skill_root=skill_root,
        database_path=database_path,
        retention_days=int(data.get("retention_days", 180)),
        deepseek_base_url=str(deepseek.get("base_url", "https://api.deepseek.com")),
        deepseek_model=str(deepseek.get("model", "deepseek-v4-pro")),
        deepseek_api_key_env=str(deepseek.get("api_key_env", "DEEPSEEK_API_KEY")),
        thinking_enabled=bool(deepseek.get("thinking_enabled", True)),
        reasoning_effort=str(deepseek.get("reasoning_effort", "medium")),
        timeout_seconds=int(deepseek.get("timeout_seconds", 120)),
        max_attempts=int(deepseek.get("max_attempts", 3)),
        followup_days=tuple(int(value) for value in workflow.get("followup_days", [7, 21])),
        outreach_profile={
            "mailbox": str(outreach.get("mailbox", "")),
            "company_team_intro": str(outreach.get("company_team_intro", "")),
            "sender_signature": str(outreach.get("sender_signature", "")),
        },
    )


def load_jobs(path: str | Path) -> list[dict[str, Any]]:
    data = _load_yaml(Path(path))
    jobs = data.get("jobs", [])
    if not isinstance(jobs, list):
        raise ConfigError("jobs must be a list")
    for job in jobs:
        if not isinstance(job, dict):
            raise ConfigError("each job must be a mapping")
        if not job.get("active", False):
            continue
        for field in REQUIRED_ACTIVE_JOB_FIELDS:
            if field not in job or job[field] in (None, "", []):
                raise ConfigError(f"active job {job.get('id', '<unknown>')} missing {field}")
    return jobs


def load_sources(path: str | Path) -> dict[str, list[dict[str, Any]]]:
    data = _load_yaml(Path(path))
    conferences = data.get("conferences", [])
    journals = data.get("journals", [])
    if not isinstance(conferences, list) or not isinstance(journals, list):
        raise ConfigError("conferences and journals must be lists")
    return {"conferences": conferences, "journals": journals}
