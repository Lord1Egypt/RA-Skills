"""Environment-backed settings for the wrapper skill."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path

from .profiles import parse_outputs, resolve_model_profile, resolve_stt_profile


def _env(name: str, default: str = "") -> str:
    return str(os.getenv(name, default)).strip()


def _default_skill_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _locate_legacy_project_root(explicit: str, project_root: Path) -> Path | None:
    candidates: list[Path] = []
    if explicit:
        candidates.append(Path(explicit).expanduser())
    candidates.append(project_root / "openclaw_capture_workflow")
    candidates.append(Path.cwd() / "openclaw_capture_workflow")
    for candidate in candidates:
        if (candidate / "src" / "openclaw_capture_workflow").exists():
            return candidate.resolve()
    return None


def _default_model_api_base_url(model_profile: str) -> str:
    if model_profile == "openai_direct":
        return "https://api.openai.com/v1"
    return "https://aihubmix.com/v1"


@dataclass
class Settings:
    skill_root: Path
    project_root: Path
    state_dir: Path
    backend_mode: str = "library"
    backend_url: str = "http://127.0.0.1:8765"
    stt_profile: str = "remote_only"
    local_stt_command: str = ""
    model_profile: str = "aihubmix_gateway"
    model_api_base_url: str = "https://aihubmix.com/v1"
    model_api_key: str = ""
    summary_model: str = "gpt-4.1-mini"
    outputs: tuple[str, ...] = ("telegram",)
    telegram_bot_token: str = ""
    feishu_webhook: str = ""
    poll_interval_seconds: float = 1.0
    poll_timeout_seconds: float = 300.0
    legacy_project_root: Path | None = None
    legacy_config_path: Path | None = None
    legacy_env_path: Path | None = None
    vault_path_override: str = ""

    @classmethod
    def from_env(cls, skill_root: Path | None = None) -> "Settings":
        skill_root = (skill_root or _default_skill_root()).resolve()
        project_root = skill_root.parent
        raw_model_profile = _env("OPENCLAW_CAPTURE_MODEL_PROFILE", "aihubmix_gateway")
        model_profile = resolve_model_profile(raw_model_profile)
        explicit_base = _env("OPENCLAW_CAPTURE_MODEL_API_BASE_URL")
        model_api_base_url = explicit_base or _default_model_api_base_url(model_profile)
        local_stt_command = _env("OPENCLAW_CAPTURE_LOCAL_STT_COMMAND")
        stt_profile = resolve_stt_profile(
            _env("OPENCLAW_CAPTURE_STT_PROFILE"),
            local_command=local_stt_command,
        )
        outputs = parse_outputs(_env("OPENCLAW_CAPTURE_OUTPUTS", "telegram"))
        state_dir = Path(_env("OPENCLAW_CAPTURE_STATE_DIR") or str(skill_root / ".state")).expanduser().resolve()
        legacy_project_root = _locate_legacy_project_root(
            _env("OPENCLAW_CAPTURE_LEGACY_PROJECT_ROOT"),
            project_root,
        )
        explicit_config = _env("OPENCLAW_CAPTURE_LEGACY_CONFIG_PATH")
        legacy_config_path = None
        if explicit_config:
            legacy_config_path = Path(explicit_config).expanduser().resolve()
        elif legacy_project_root and (legacy_project_root / "config.json").exists():
            legacy_config_path = (legacy_project_root / "config.json").resolve()
        legacy_env_path = None
        if legacy_project_root and (legacy_project_root / ".env").exists():
            legacy_env_path = (legacy_project_root / ".env").resolve()
        return cls(
            skill_root=skill_root,
            project_root=project_root,
            state_dir=state_dir,
            backend_mode=_env("OPENCLAW_CAPTURE_BACKEND_MODE", "library") or "library",
            backend_url=_env("OPENCLAW_CAPTURE_BACKEND_URL", "http://127.0.0.1:8765") or "http://127.0.0.1:8765",
            stt_profile=stt_profile,
            local_stt_command=local_stt_command,
            model_profile=model_profile,
            model_api_base_url=model_api_base_url,
            model_api_key=_env("OPENCLAW_CAPTURE_MODEL_API_KEY"),
            summary_model=_env("OPENCLAW_CAPTURE_MODEL_NAME", "gpt-4.1-mini") or "gpt-4.1-mini",
            outputs=outputs,
            telegram_bot_token=_env("OPENCLAW_CAPTURE_TELEGRAM_BOT_TOKEN"),
            feishu_webhook=_env("OPENCLAW_CAPTURE_FEISHU_WEBHOOK"),
            poll_interval_seconds=float(_env("OPENCLAW_CAPTURE_POLL_INTERVAL_SECONDS", "1") or "1"),
            poll_timeout_seconds=float(_env("OPENCLAW_CAPTURE_POLL_TIMEOUT_SECONDS", "300") or "300"),
            legacy_project_root=legacy_project_root,
            legacy_config_path=legacy_config_path,
            legacy_env_path=legacy_env_path,
            vault_path_override=_env("OPENCLAW_CAPTURE_VAULT_PATH"),
        )

