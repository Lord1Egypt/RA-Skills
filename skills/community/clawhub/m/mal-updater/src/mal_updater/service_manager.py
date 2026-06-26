from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess
from typing import Any

from .config import AppConfig, ensure_directories, load_config

SERVICE_NAME = "mal-updater.service"
_RECENT_LOG_LINES = 20
_RESULT_SNIPPET_LIMIT = 240


@dataclass(slots=True)
class ServiceCommandResult:
    status: str
    message: str
    details: dict[str, Any] | None = None


def _unit_path() -> Path:
    return Path.home() / ".config" / "systemd" / "user" / SERVICE_NAME


def _service_env_path() -> Path:
    return Path.home() / ".config" / "mal-updater-service.env"


def _run(args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, text=True, capture_output=True, check=check)


def _read_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(payload, dict):
        return None, f"Expected top-level object in {path.name}"
    return payload, None


def _tail_lines(path: Path, *, limit: int = _RECENT_LOG_LINES) -> list[str]:
    if not path.exists():
        return []
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError:
        return []
    if limit <= 0:
        return []
    return lines[-limit:]


def _snippet(value: object, *, limit: int = _RESULT_SNIPPET_LIMIT) -> str | None:
    if not isinstance(value, str):
        return None
    trimmed = value.strip()
    if not trimmed:
        return None
    if len(trimmed) <= limit:
        return trimmed
    return trimmed[: limit - 3] + "..."


def _parse_iso_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _summarize_last_result(value: object) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    summary: dict[str, Any] = {}
    for field in ("status", "label", "returncode", "reason", "access_token_path", "refresh_token_path"):
        field_value = value.get(field)
        if field_value is not None:
            summary[field] = field_value
    stdout_snippet = _snippet(value.get("stdout"))
    stderr_snippet = _snippet(value.get("stderr"))
    if stdout_snippet is not None:
        summary["stdout_snippet"] = stdout_snippet
    if stderr_snippet is not None:
        summary["stderr_snippet"] = stderr_snippet
    return summary or None


def _summarize_task_state(value: object) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    summary: dict[str, Any] = {}
    for field in (
        "last_run_at",
        "last_status",
        "last_skipped_at",
        "last_skip_reason",
        "last_error",
        "last_decision_at",
        "last_started_at",
        "last_finished_at",
        "budget_backoff_level",
        "budget_backoff_until",
        "budget_backoff_cooldown_source",
        "failure_backoff_until",
        "failure_backoff_reason",
        "failure_backoff_class",
        "next_due_at",
        "budget_provider",
        "budget_scope",
        "last_fetch_mode",
        "last_full_refresh_reason",
        "projected_request_source",
    ):
        field_value = value.get(field)
        if field_value is not None:
            summary[field] = field_value
    if isinstance(value.get("last_run_epoch"), (int, float)):
        summary["last_run_epoch"] = value["last_run_epoch"]
    if isinstance(value.get("every_seconds"), int):
        summary["every_seconds"] = value["every_seconds"]
    if isinstance(value.get("next_due_epoch"), (int, float)):
        summary["next_due_epoch"] = value["next_due_epoch"]
    if isinstance(value.get("last_duration_seconds"), (int, float)):
        summary["last_duration_seconds"] = float(value["last_duration_seconds"])
    if isinstance(value.get("budget_backoff_remaining_seconds"), (int, float)):
        summary["budget_backoff_remaining_seconds"] = int(value["budget_backoff_remaining_seconds"])
    if isinstance(value.get("budget_backoff_floor_seconds"), (int, float)):
        summary["budget_backoff_floor_seconds"] = int(value["budget_backoff_floor_seconds"])
    if isinstance(value.get("failure_backoff_remaining_seconds"), (int, float)):
        summary["failure_backoff_remaining_seconds"] = int(value["failure_backoff_remaining_seconds"])
    if isinstance(value.get("failure_backoff_consecutive_failures"), (int, float)):
        summary["failure_backoff_consecutive_failures"] = int(value["failure_backoff_consecutive_failures"])
    if isinstance(value.get("failure_backoff_floor_seconds"), (int, float)):
        summary["failure_backoff_floor_seconds"] = int(value["failure_backoff_floor_seconds"])
    if isinstance(value.get("projected_request_count"), (int, float)):
        summary["projected_request_count"] = int(value["projected_request_count"])
    if isinstance(value.get("projected_request_total"), (int, float)):
        summary["projected_request_total"] = int(value["projected_request_total"])
    if isinstance(value.get("projected_ratio"), (int, float)):
        summary["projected_ratio"] = round(float(value["projected_ratio"]), 6)
    if isinstance(value.get("last_request_delta"), (int, float)):
        summary["last_request_delta"] = int(value["last_request_delta"])
    next_due_at = _parse_iso_timestamp(value.get("next_due_at"))
    if next_due_at is not None:
        summary["next_due_in_seconds"] = max(0, int((next_due_at - datetime.now(timezone.utc)).total_seconds()))
    budget_backoff_until = _parse_iso_timestamp(value.get("budget_backoff_until"))
    if budget_backoff_until is not None:
        summary["budget_backoff_remaining_seconds"] = max(0, int((budget_backoff_until - datetime.now(timezone.utc)).total_seconds()))
    failure_backoff_until = _parse_iso_timestamp(value.get("failure_backoff_until"))
    if failure_backoff_until is not None:
        summary["failure_backoff_remaining_seconds"] = max(0, int((failure_backoff_until - datetime.now(timezone.utc)).total_seconds()))
    last_result = _summarize_last_result(value.get("last_result"))
    if last_result is not None:
        summary["last_result"] = last_result
    return summary or None


def unit_contents(config: AppConfig | None = None) -> str:
    config = config or load_config()
    ensure_directories(config)
    repo = config.project_root
    env_file = _service_env_path()
    python = Path(subprocess.run(["python3", "-c", "import sys; print(sys.executable)"], text=True, capture_output=True, check=True).stdout.strip())
    return f"""[Unit]
Description=MAL-Updater background sync daemon
After=default.target

[Service]
Type=simple
WorkingDirectory={repo}
Environment=PYTHONPATH={repo / 'src'}
EnvironmentFile=-{env_file}
ExecStart={python} -m mal_updater.cli --project-root {repo} service-run
Restart=always
RestartSec=15

[Install]
WantedBy=default.target
"""


def write_unit_file(config: AppConfig | None = None) -> Path:
    config = config or load_config()
    path = _unit_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(unit_contents(config), encoding="utf-8")
    return path


def daemon_reload() -> None:
    _run(["systemctl", "--user", "daemon-reload"])


def service_status() -> dict[str, Any]:
    unit = _unit_path()
    enabled = _run(["systemctl", "--user", "is-enabled", SERVICE_NAME], check=False)
    active = _run(["systemctl", "--user", "is-active", SERVICE_NAME], check=False)
    return {
        "unit_path": str(unit),
        "unit_exists": unit.exists(),
        "enabled": enabled.returncode == 0 and enabled.stdout.strip() == "enabled",
        "active": active.returncode == 0 and active.stdout.strip() == "active",
        "enabled_raw": enabled.stdout.strip() or enabled.stderr.strip(),
        "active_raw": active.stdout.strip() or active.stderr.strip(),
        "env_path": str(_service_env_path()),
        "env_exists": _service_env_path().exists(),
    }


def install_service(*, start_now: bool = True, config: AppConfig | None = None) -> ServiceCommandResult:
    config = config or load_config()
    unit = write_unit_file(config)
    daemon_reload()
    _run(["systemctl", "--user", "enable", SERVICE_NAME])
    if start_now:
        _run(["systemctl", "--user", "restart", SERVICE_NAME])
    return ServiceCommandResult(status="ok", message="MAL-Updater service installed.", details={"unit_path": str(unit), **service_status()})


def uninstall_service(*, stop_now: bool = True) -> ServiceCommandResult:
    if stop_now:
        _run(["systemctl", "--user", "stop", SERVICE_NAME], check=False)
    _run(["systemctl", "--user", "disable", SERVICE_NAME], check=False)
    unit = _unit_path()
    if unit.exists():
        unit.unlink()
    daemon_reload()
    return ServiceCommandResult(status="ok", message="MAL-Updater service uninstalled.", details=service_status())


def restart_service() -> ServiceCommandResult:
    _run(["systemctl", "--user", "restart", SERVICE_NAME])
    return ServiceCommandResult(status="ok", message="MAL-Updater service restarted.", details=service_status())


def stop_service() -> ServiceCommandResult:
    _run(["systemctl", "--user", "stop", SERVICE_NAME], check=False)
    return ServiceCommandResult(status="ok", message="MAL-Updater service stopped.", details=service_status())


def start_service() -> ServiceCommandResult:
    _run(["systemctl", "--user", "start", SERVICE_NAME])
    return ServiceCommandResult(status="ok", message="MAL-Updater service started.", details=service_status())


def doctor_service(config: AppConfig | None = None) -> dict[str, Any]:
    config = config or load_config()
    ensure_directories(config)
    status = service_status()
    service_state, service_state_error = _read_json(config.service_state_path)
    recent_health, recent_health_error = _read_json(config.health_latest_json_path)

    task_state: dict[str, Any] = {}
    if isinstance(service_state, dict):
        raw_tasks = service_state.get("tasks")
        if isinstance(raw_tasks, dict):
            for task_name, raw_task_state in raw_tasks.items():
                summary = _summarize_task_state(raw_task_state)
                if summary is not None:
                    task_state[str(task_name)] = summary

    payload = {
        **status,
        "service_log_path": str(config.service_log_path),
        "service_log_exists": config.service_log_path.exists(),
        "service_log_tail": _tail_lines(config.service_log_path),
        "service_state_path": str(config.service_state_path),
        "service_state_exists": config.service_state_path.exists(),
        "service_state_parse_error": service_state_error,
        "last_loop_at": service_state.get("last_loop_at") if isinstance(service_state, dict) else None,
        "task_state": task_state,
        "api_request_events_path": str(config.api_request_events_path),
        "api_request_events_exists": config.api_request_events_path.exists(),
        "health_latest_json_path": str(config.health_latest_json_path),
        "health_latest_exists": config.health_latest_json_path.exists(),
        "health_latest_parse_error": recent_health_error,
        "health_latest_summary": recent_health,
    }
    if isinstance(service_state, dict) and isinstance(service_state.get("api_usage"), dict):
        payload["api_usage"] = service_state["api_usage"]
    return payload
