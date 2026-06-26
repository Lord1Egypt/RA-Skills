#!/usr/bin/env python3
"""Shared OpenMath config helpers for theorem discovery workflows."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path


ENV_CONFIG_FILENAME = "openmath-env.json"
PROJECT_CONFIG_DIRNAME = ".openmath-skills"
GLOBAL_CONFIG_DIR = Path.home() / ".openmath-skills"
GLOBAL_ENV_CONFIG_PATH = GLOBAL_CONFIG_DIR / ENV_CONFIG_FILENAME
DEFAULT_OPENMATH_SITE_URL = "https://openmath.shentu.org"
DEFAULT_OPENMATH_API_HOST = "https://openmath-be.shentu.org"

LANGUAGE_ALIASES = {
    "lean": "lean",
    "rocq": "rocq",
}


class OpenMathEnvConfigError(ValueError):
    """Raised when the shared OpenMath env config is missing or invalid."""


@dataclass(frozen=True)
class OpenMathPreferences:
    config_path: Path
    preferred_language: str | None
    openmath_site_url: str
    openmath_api_host: str


def project_env_config_path() -> Path:
    return Path.cwd() / PROJECT_CONFIG_DIRNAME / ENV_CONFIG_FILENAME


def candidate_env_config_paths() -> tuple[Path, Path]:
    return (project_env_config_path(), GLOBAL_ENV_CONFIG_PATH)


def submit_skill_root() -> Path:
    return Path(__file__).resolve().parents[2] / "openmath-submit-theorem"


def example_config_path() -> Path:
    return submit_skill_root() / "references" / "openmath-env.example.json"


def setup_doc_path() -> Path:
    return Path(__file__).resolve().parents[1] / "references" / "init-setup.md"


def find_env_config() -> Path | None:
    explicit = os.environ.get("OPENMATH_ENV_CONFIG")
    if explicit:
        path = Path(explicit).expanduser()
        return path if path.exists() else None

    for path in candidate_env_config_paths():
        if path.exists():
            return path
    return None


def normalize_preferred_language(value: object) -> str | None:
    raw = str(value or "").strip().lower()
    if not raw:
        return None
    return LANGUAGE_ALIASES.get(raw)


def normalize_api_language(value: object) -> str | None:
    return normalize_preferred_language(value)


def normalize_url(value: object) -> str | None:
    raw = str(value or "").strip()
    if not raw:
        return None
    return raw.rstrip("/")


def default_openmath_site_url() -> str:
    return DEFAULT_OPENMATH_SITE_URL


def default_openmath_api_host() -> str:
    return DEFAULT_OPENMATH_API_HOST


def onboarding_text(config_path: Path) -> str:
    project_config, global_config = candidate_env_config_paths()
    return "\n".join(
        [
            f"Environment config: {config_path}",
            "",
            "Auto-discovery only checks these locations:",
            f"- {project_config}",
            f"- {global_config}",
            "",
            f"First-time setup guide: {setup_doc_path()}",
            f"Example config: {example_config_path()}",
            "",
            "If no config exists, stop and ask the user where to create it:",
            f"- ./{PROJECT_CONFIG_DIRNAME}/{ENV_CONFIG_FILENAME} (recommended for project-specific settings)",
            "- ~/.openmath-skills/openmath-env.json (recommended for reusable settings)",
            "",
            "Collect at least these fields during setup:",
            "- preferred_language: lean or rocq",
            f"- config visibility / save scope: ./{PROJECT_CONFIG_DIRNAME} or ~/.openmath-skills",
            f"- OpenMath site URL comes from OPENMATH_SITE_URL or defaults to {DEFAULT_OPENMATH_SITE_URL}",
            f"- OpenMath API host comes from OPENMATH_API_HOST or defaults to {DEFAULT_OPENMATH_API_HOST}",
        ]
    )


def discovery_gate_text(config_path: Path, *, missing_preferred_language: bool = False) -> str:
    lines = [
        onboarding_text(config_path),
        "",
        "First-run gate: stop here.",
        "Do not query the OpenMath theorem list, theorem detail, or download APIs until setup is complete.",
    ]
    if missing_preferred_language:
        lines.extend(
            [
                "",
                "Config exists, but `preferred_language` is missing.",
                "Ask the user to choose `lean` or `rocq`, save it in openmath-env.json, then retry.",
            ]
        )
    return "\n".join(lines)


def _load_endpoint_preferences() -> tuple[str, str]:
    site_url = default_openmath_site_url()
    api_host = default_openmath_api_host()
    env_site_override = normalize_url(os.environ.get("OPENMATH_SITE_URL"))
    env_api_override = normalize_url(os.environ.get("OPENMATH_API_HOST"))
    if env_site_override:
        site_url = env_site_override
    if env_api_override:
        api_host = env_api_override

    return site_url, api_host


def load_openmath_preferences(
    config_path: str | os.PathLike[str] | None = None,
    *,
    require_preferred_language: bool = False,
) -> OpenMathPreferences:
    if config_path is not None:
        path = Path(config_path).expanduser()
    else:
        detected = find_env_config()
        path = detected if detected else project_env_config_path()

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise OpenMathEnvConfigError(discovery_gate_text(path)) from exc
    except json.JSONDecodeError as exc:
        raise OpenMathEnvConfigError(f"Invalid JSON in config file: {path}: {exc}") from exc

    preferred_language = normalize_preferred_language(data.get("preferred_language"))
    if data.get("preferred_language") is not None and preferred_language is None:
        raise OpenMathEnvConfigError(
            "Config field `preferred_language` must be `lean` or `rocq`."
        )
    if require_preferred_language and preferred_language is None:
        raise OpenMathEnvConfigError(
            discovery_gate_text(path, missing_preferred_language=True)
        )

    openmath_site_url, openmath_api_host = _load_endpoint_preferences()

    return OpenMathPreferences(
        config_path=path,
        preferred_language=preferred_language,
        openmath_site_url=openmath_site_url,
        openmath_api_host=openmath_api_host,
    )


def resolve_openmath_site_url(config_path: str | os.PathLike[str] | None = None) -> str:
    env_override = normalize_url(os.environ.get("OPENMATH_SITE_URL"))
    if env_override:
        return env_override
    return default_openmath_site_url()


def resolve_openmath_api_host(config_path: str | os.PathLike[str] | None = None) -> str:
    env_override = normalize_url(os.environ.get("OPENMATH_API_HOST"))
    if env_override:
        return env_override
    return default_openmath_api_host()
