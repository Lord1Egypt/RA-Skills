from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
import json
import math
import subprocess
import time
from typing import Any

from .auth import persist_token_response
from .auth_failure_signals import looks_auth_style_failure
from .config import (
    AppConfig,
    DEFAULT_SERVICE_TASK_PROJECTED_REQUEST_COUNTS,
    DEFAULT_SERVICE_TASK_PROJECTED_REQUEST_COUNTS_BY_MODE,
    ensure_directories,
    load_config,
    load_mal_secrets,
)
from .crunchyroll_auth import load_crunchyroll_credentials, resolve_crunchyroll_state_paths
from .hidive_auth import load_hidive_credentials, resolve_hidive_state_paths
from .mal_client import MalApiError, MalClient
from .request_tracking import (
    estimate_budget_recovery_seconds,
    estimate_budget_recovery_seconds_for_ratio,
    prune_api_request_events,
    summarize_recent_api_usage,
)


@dataclass(slots=True)
class TaskSpec:
    name: str
    every_seconds: int
    budget_provider: str | None = None


_BUDGET_GATE_WINDOW_SECONDS = 3600
_FAILURE_BACKOFF_MIN_SECONDS = 300
_AUTO_PROJECTED_REQUEST_PERCENTILE = 0.9
_AUTO_PROJECTED_REQUEST_BURST_MIN_HISTORY = 4
_AUTO_PROJECTED_REQUEST_BURST_RATIO = 2.0


def _now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _iso_after_seconds(seconds: int) -> str:
    return (datetime.now(timezone.utc) + timedelta(seconds=max(0, seconds))).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _load_state(config: AppConfig) -> dict[str, Any]:
    if not config.service_state_path.exists():
        return {"started_at": _now_iso(), "tasks": {}}
    return json.loads(config.service_state_path.read_text(encoding="utf-8"))


def _save_state(config: AppConfig, state: dict[str, Any]) -> None:
    config.service_state_path.write_text(json.dumps(state, indent=2, sort_keys=True), encoding="utf-8")


def _set_task_next_due(task_state: dict[str, Any], *, base_epoch: float, every_seconds: int) -> None:
    task_state["every_seconds"] = int(every_seconds)
    task_state["next_due_epoch"] = float(base_epoch) + int(every_seconds)
    task_state["next_due_at"] = _iso_after_seconds(int(task_state["next_due_epoch"] - time.time()))


def _append_log(config: AppConfig, message: str) -> None:
    with config.service_log_path.open("a", encoding="utf-8") as fh:
        fh.write(f"[{_now_iso()}] {message}\n")


def _mark_task_decision(task_state: dict[str, Any], *, decision_at: str | None = None) -> None:
    task_state["last_decision_at"] = decision_at or _now_iso()


def _record_task_timing(
    task_state: dict[str, Any],
    *,
    started_epoch: float,
    finished_epoch: float,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> None:
    task_state["last_started_at"] = started_at or datetime.fromtimestamp(started_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    task_state["last_finished_at"] = finished_at or datetime.fromtimestamp(finished_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
    task_state["last_duration_seconds"] = max(0.0, round(float(finished_epoch) - float(started_epoch), 3))
    _mark_task_decision(task_state, decision_at=task_state["last_finished_at"])


def _normalized_request_delta_history(value: object) -> list[int]:
    if not isinstance(value, list):
        return []
    history: list[int] = []
    for item in value:
        if isinstance(item, int):
            history.append(max(0, int(item)))
    return history


def _trimmed_request_delta_history(history: list[int], *, limit: int) -> list[int]:
    normalized_limit = max(1, int(limit))
    if len(history) <= normalized_limit:
        return history
    return history[-normalized_limit:]


def _percentile_request_delta(history: list[int], percentile: float) -> int | None:
    if len(history) < 2:
        return None
    normalized = min(1.0, max(0.0, float(percentile)))
    if normalized <= 0.0:
        return None
    sorted_history = sorted(max(0, int(item)) for item in history)
    index = max(0, min(len(sorted_history) - 1, int(math.ceil(normalized * len(sorted_history))) - 1))
    return sorted_history[index]


def _smoothed_request_delta(history: list[int]) -> int | None:
    if len(history) < 2:
        return None
    return max(0, int(math.ceil(sum(history) / len(history))))


def _auto_projected_request_percentile(history: list[int]) -> float | None:
    if len(history) < _AUTO_PROJECTED_REQUEST_BURST_MIN_HISTORY:
        return None
    smoothed = _smoothed_request_delta(history)
    if smoothed is None or smoothed <= 0:
        return None
    highest = max(max(0, int(item)) for item in history)
    if highest < int(math.ceil(smoothed * _AUTO_PROJECTED_REQUEST_BURST_RATIO)):
        return None
    return _AUTO_PROJECTED_REQUEST_PERCENTILE


def _projected_request_delta_from_history(
    history: list[int],
    *,
    percentile: float | None,
) -> tuple[int | None, str | None]:
    chosen_percentile = percentile
    label_prefix = ""
    if chosen_percentile is None:
        chosen_percentile = _auto_projected_request_percentile(history)
        if chosen_percentile is not None:
            label_prefix = "auto_"
    if chosen_percentile is not None:
        projected = _percentile_request_delta(history, chosen_percentile)
        if projected is not None:
            return projected, f"{label_prefix}p{int(round(chosen_percentile * 100))}"
    projected = _smoothed_request_delta(history)
    if projected is not None:
        return projected, "smoothed"
    return None, None


def _record_observed_request_delta(
    task_state: dict[str, Any],
    *,
    observed_request_delta: int,
    fetch_mode: str | None,
    finished_at: str,
    history_limit: int,
) -> None:
    normalized_delta = max(0, int(observed_request_delta))
    task_state["last_request_delta"] = normalized_delta
    task_state["last_request_delta_at"] = finished_at
    history = _normalized_request_delta_history(task_state.get("last_request_delta_history"))
    history.append(normalized_delta)
    task_state["last_request_delta_history"] = _trimmed_request_delta_history(history, limit=history_limit)
    if fetch_mode is None:
        return
    delta_by_mode = task_state.get("last_request_delta_by_mode")
    if not isinstance(delta_by_mode, dict):
        delta_by_mode = {}
    delta_by_mode[fetch_mode] = normalized_delta
    task_state["last_request_delta_by_mode"] = delta_by_mode
    history_by_mode = task_state.get("last_request_delta_history_by_mode")
    if not isinstance(history_by_mode, dict):
        history_by_mode = {}
    mode_history = _normalized_request_delta_history(history_by_mode.get(fetch_mode))
    mode_history.append(normalized_delta)
    history_by_mode[fetch_mode] = _trimmed_request_delta_history(mode_history, limit=history_limit)
    task_state["last_request_delta_history_by_mode"] = history_by_mode


def _run_subprocess(config: AppConfig, args: list[str], *, label: str) -> dict[str, Any]:
    env = {
        **__import__("os").environ,
        "PYTHONPATH": str(config.project_root / "src"),
    }
    result = subprocess.run(args, cwd=config.project_root, text=True, capture_output=True, check=False, env=env)
    status = "ok" if result.returncode == 0 else "error"
    payload = {
        "status": status,
        "label": label,
        "returncode": result.returncode,
        "stdout": result.stdout,
        "stderr": result.stderr,
    }
    if result.returncode == 0:
        _append_log(config, f"task={label} status=ok")
    else:
        _append_log(config, f"task={label} status=error returncode={result.returncode} stderr={result.stderr.strip() or result.stdout.strip()}")
    return payload


def _refresh_mal_tokens(config: AppConfig) -> dict[str, Any]:
    secrets = load_mal_secrets(config)
    if not (secrets.client_id and secrets.refresh_token):
        return {"status": "skipped", "reason": "missing_mal_refresh_material"}
    client = MalClient(config, secrets)
    token = client.refresh_access_token()
    persisted = persist_token_response(token, secrets)
    return {
        "status": "ok",
        "access_token_path": str(persisted.access_token_path),
        "refresh_token_path": str(persisted.refresh_token_path),
    }


def _available_source_providers(config: AppConfig) -> list[str]:
    providers: list[str] = []
    crunchyroll_credentials = load_crunchyroll_credentials(config)
    if crunchyroll_credentials.username and crunchyroll_credentials.password:
        providers.append("crunchyroll")
    hidive_credentials = load_hidive_credentials(config)
    if hidive_credentials.username and hidive_credentials.password:
        providers.append("hidive")
    return providers



def _task_specs(config: AppConfig) -> list[TaskSpec]:
    specs = [TaskSpec("mal_refresh", config.service.mal_refresh_every_seconds, budget_provider="mal")]
    for provider in _available_source_providers(config):
        specs.append(TaskSpec(f"sync_fetch_{provider}", config.service.sync_every_seconds, budget_provider=provider))
    specs.append(TaskSpec("sync_apply", config.service.sync_every_seconds, budget_provider="mal"))
    specs.append(TaskSpec("health", config.service.health_every_seconds, budget_provider=None))
    return specs


def _provider_fetch_command(config: AppConfig, provider: str, *, full_refresh: bool = False) -> list[str]:
    command: list[str]
    if provider == "crunchyroll":
        snapshot_path = config.cache_dir / "live-crunchyroll-snapshot.json"
        command = [
            "python3",
            "-m",
            "mal_updater.cli",
            "crunchyroll-fetch-snapshot",
            "--out",
            str(snapshot_path),
            "--ingest",
        ]
    elif provider == "hidive":
        snapshot_path = config.cache_dir / "live-hidive-snapshot.json"
        command = [
            "python3",
            "-m",
            "mal_updater.cli",
            "provider-fetch-snapshot",
            "--provider",
            "hidive",
            "--out",
            str(snapshot_path),
            "--ingest",
        ]
    else:
        raise ValueError(f"unsupported provider fetch task: {provider}")
    if full_refresh:
        command.append("--full-refresh")
    return command



def _provider_fetch_requires_full_refresh(config: AppConfig, task_state: dict[str, Any], *, now: float) -> bool:
    interval = int(config.service.full_refresh_every_seconds)
    if interval <= 0:
        return False
    anchor_epoch = task_state.get("full_refresh_anchor_epoch")
    if not isinstance(anchor_epoch, (int, float)) or anchor_epoch <= 0:
        return False
    return float(now) - float(anchor_epoch) >= interval



def _provider_from_refresh_command_args(command_args: object) -> str | None:
    if not isinstance(command_args, list) or not command_args:
        return None
    if command_args[0] == "crunchyroll-fetch-snapshot":
        return "crunchyroll"
    if len(command_args) >= 3 and command_args[0] == "provider-fetch-snapshot" and command_args[1] == "--provider" and isinstance(command_args[2], str):
        return str(command_args[2])
    return None



def _provider_fetch_requested_by_health(config: AppConfig, provider: str, task_state: dict[str, Any]) -> bool:
    path = config.health_latest_json_path
    if not path.exists():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if not isinstance(payload, dict):
        return False
    maintenance = payload.get("maintenance")
    if not isinstance(maintenance, dict):
        return False
    commands = maintenance.get("recommended_commands")
    if not isinstance(commands, list):
        return False
    try:
        health_mtime = path.stat().st_mtime
    except OSError:
        return False
    last_full_refresh_epoch = task_state.get("last_successful_full_refresh_epoch")
    if isinstance(last_full_refresh_epoch, (int, float)) and float(last_full_refresh_epoch) >= float(health_mtime):
        return False
    for command in commands:
        if not isinstance(command, dict):
            continue
        if command.get("reason_code") != "refresh_full_snapshot":
            continue
        if _provider_from_refresh_command_args(command.get("command_args")) == provider:
            return True
    return False



def _apply_sync_command() -> list[str]:
    return [
        "python3",
        "-m",
        "mal_updater.cli",
        "apply-sync",
        "--limit",
        "0",
        "--exact-approved-only",
        "--execute",
    ]



def _planned_fetch_mode(config: AppConfig, spec: TaskSpec, task_state: dict[str, Any], *, now: float) -> tuple[str | None, list[str]]:
    if not spec.name.startswith("sync_fetch_"):
        return None, []
    provider = spec.name.removeprefix("sync_fetch_")
    full_refresh_reasons: list[str] = []
    if _provider_fetch_requires_full_refresh(config, task_state, now=now):
        full_refresh_reasons.append("periodic_cadence")
    if _provider_fetch_requested_by_health(config, provider, task_state):
        full_refresh_reasons.append("health_recommended")
    return ("full_refresh" if full_refresh_reasons else "incremental"), full_refresh_reasons



def _maybe_downgrade_fetch_mode_for_budget(
    config: AppConfig,
    spec: TaskSpec,
    task_state: dict[str, Any],
    *,
    planned_fetch_mode: str | None,
    planned_full_refresh_reasons: list[str],
    allowed: bool,
    reason: str | None,
    usage: dict[str, Any] | None,
) -> tuple[bool, str | None, dict[str, Any] | None, str | None, list[str], str | None, dict[str, Any] | None]:
    if allowed or not spec.name.startswith("sync_fetch_") or planned_fetch_mode != "full_refresh":
        return allowed, reason, usage, planned_fetch_mode, planned_full_refresh_reasons, None, None
    incremental_allowed, incremental_reason, incremental_usage = _budget_gate(config, spec, task_state, fetch_mode="incremental")
    if not incremental_allowed:
        return allowed, reason, usage, planned_fetch_mode, planned_full_refresh_reasons, None, incremental_usage
    deferred_reason = "+".join(planned_full_refresh_reasons) if planned_full_refresh_reasons else "budget_deferred"
    return True, None, incremental_usage, "incremental", [], deferred_reason, incremental_usage



def _projected_request_count(
    config: AppConfig,
    spec: TaskSpec,
    task_state: dict[str, Any],
    *,
    fetch_mode: str | None = None,
) -> tuple[int, str | None]:
    configured, configured_source = config.service.projected_request_count_for(spec.name, fetch_mode=fetch_mode)
    built_in_mode_default = None
    if fetch_mode:
        built_in_mode_default = DEFAULT_SERVICE_TASK_PROJECTED_REQUEST_COUNTS_BY_MODE.get(spec.name, {}).get(fetch_mode)
    built_in_task_default = DEFAULT_SERVICE_TASK_PROJECTED_REQUEST_COUNTS.get(spec.name)
    task_wide_configured = config.service.task_projected_request_counts.get(spec.name)

    use_mode_default_as_cold_start_seed = (
        fetch_mode is not None
        and configured_source == f"configured_{fetch_mode}"
        and isinstance(configured, int)
        and built_in_mode_default == configured
    )
    use_task_default_as_cold_start_seed = (
        configured_source == "configured"
        and isinstance(configured, int)
        and built_in_task_default == configured
    )

    if use_mode_default_as_cold_start_seed and isinstance(task_wide_configured, int):
        return max(0, int(task_wide_configured)), "configured"
    if configured is not None and not use_mode_default_as_cold_start_seed and not use_task_default_as_cold_start_seed:
        return configured, configured_source
    percentile = config.service.projected_request_percentile_for(spec.name, provider=spec.budget_provider)
    if fetch_mode:
        history_by_mode = task_state.get("last_request_delta_history_by_mode")
        if isinstance(history_by_mode, dict):
            projected_mode, projected_mode_label = _projected_request_delta_from_history(
                _normalized_request_delta_history(history_by_mode.get(fetch_mode)),
                percentile=percentile,
            )
            if projected_mode is not None and projected_mode_label is not None:
                return projected_mode, f"observed_{fetch_mode}_{projected_mode_label}"
        if isinstance(task_state.get("last_request_delta_by_mode"), dict):
            mode_value = task_state["last_request_delta_by_mode"].get(fetch_mode)
            if isinstance(mode_value, int):
                return max(0, int(mode_value)), f"observed_{fetch_mode}"
    projected, projected_label = _projected_request_delta_from_history(
        _normalized_request_delta_history(task_state.get("last_request_delta_history")),
        percentile=percentile,
    )
    if projected is not None and projected_label is not None:
        return projected, f"observed_{projected_label}"
    value = task_state.get("last_request_delta")
    if isinstance(value, int):
        return max(0, int(value)), "observed_last_run"
    if configured is not None:
        return configured, configured_source
    return 0, None



def _refresh_projected_request_state(
    config: AppConfig,
    spec: TaskSpec,
    task_state: dict[str, Any],
    *,
    fetch_mode: str | None = None,
) -> tuple[int, str | None]:
    projected_request_count, projected_request_source = _projected_request_count(config, spec, task_state, fetch_mode=fetch_mode)
    task_state["projected_request_count"] = projected_request_count
    if projected_request_source is not None:
        task_state["projected_request_source"] = projected_request_source
    else:
        task_state.pop("projected_request_source", None)
    return projected_request_count, projected_request_source


def _budget_gate(
    config: AppConfig,
    spec: TaskSpec,
    task_state: dict[str, Any],
    *,
    fetch_mode: str | None = None,
) -> tuple[bool, str | None, dict[str, Any] | None]:
    provider = spec.budget_provider
    if provider is None:
        return True, None, None
    usage = summarize_recent_api_usage(provider=provider, window_seconds=_BUDGET_GATE_WINDOW_SECONDS, config=config).as_dict()
    limit = config.service.hourly_limit_for(provider, task_name=spec.name)
    ratio = 0.0 if limit <= 0 else float(usage.get("request_count", 0)) / float(limit)
    projected_request_count, projected_request_source = _projected_request_count(config, spec, task_state, fetch_mode=fetch_mode)
    projected_request_total = int(usage.get("request_count", 0)) + projected_request_count
    projected_ratio = 0.0 if limit <= 0 else float(projected_request_total) / float(limit)
    warn_recovery_seconds = estimate_budget_recovery_seconds_for_ratio(
        provider=provider,
        limit=limit,
        target_ratio=config.service.warn_ratio,
        projected_requests=0,
        window_seconds=_BUDGET_GATE_WINDOW_SECONDS,
        config=config,
    )
    projected_warn_recovery_seconds = estimate_budget_recovery_seconds_for_ratio(
        provider=provider,
        limit=limit,
        target_ratio=config.service.warn_ratio,
        projected_requests=projected_request_count,
        window_seconds=_BUDGET_GATE_WINDOW_SECONDS,
        config=config,
    )
    recovery_seconds = estimate_budget_recovery_seconds(
        provider=provider,
        limit=limit,
        critical_ratio=config.service.critical_ratio,
        projected_requests=0,
        window_seconds=_BUDGET_GATE_WINDOW_SECONDS,
        config=config,
    )
    projected_recovery_seconds = estimate_budget_recovery_seconds(
        provider=provider,
        limit=limit,
        critical_ratio=config.service.critical_ratio,
        projected_requests=projected_request_count,
        window_seconds=_BUDGET_GATE_WINDOW_SECONDS,
        config=config,
    )
    budget_scope = config.service.budget_scope_for(provider, task_name=spec.name)
    warn_floor_seconds = config.service.backoff_floor_seconds_for(provider, level="warn", task_name=spec.name)
    critical_floor_seconds = config.service.backoff_floor_seconds_for(provider, level="critical", task_name=spec.name)
    warn_cooldown_seconds = max(warn_recovery_seconds, warn_floor_seconds)
    critical_cooldown_seconds = max(recovery_seconds, critical_floor_seconds)
    projected_warn_cooldown_seconds = max(projected_warn_recovery_seconds, warn_floor_seconds)
    projected_critical_cooldown_seconds = max(projected_recovery_seconds, critical_floor_seconds)
    usage["limit"] = limit
    usage["ratio"] = ratio
    usage["warn_ratio"] = config.service.warn_ratio
    usage["critical_ratio"] = config.service.critical_ratio
    usage["budget_scope"] = budget_scope
    usage["warn_recovery_seconds"] = warn_recovery_seconds
    usage["recovery_seconds"] = recovery_seconds
    usage["warn_backoff_floor_seconds"] = warn_floor_seconds
    usage["critical_backoff_floor_seconds"] = critical_floor_seconds
    usage["warn_cooldown_seconds"] = warn_cooldown_seconds
    usage["critical_cooldown_seconds"] = critical_cooldown_seconds
    usage["projected_request_count"] = projected_request_count
    usage["projected_request_total"] = projected_request_total
    usage["projected_ratio"] = projected_ratio
    usage["projected_warn_recovery_seconds"] = projected_warn_recovery_seconds
    usage["projected_recovery_seconds"] = projected_recovery_seconds
    usage["projected_warn_cooldown_seconds"] = projected_warn_cooldown_seconds
    usage["projected_critical_cooldown_seconds"] = projected_critical_cooldown_seconds
    if projected_request_source is not None:
        usage["projected_request_source"] = projected_request_source
    if ratio >= config.service.critical_ratio:
        usage["backoff_level"] = "critical"
        usage["cooldown_seconds"] = critical_cooldown_seconds
        if critical_floor_seconds > recovery_seconds:
            usage["cooldown_source"] = f"{budget_scope}_floor"
        return False, f"{provider}_budget_critical ratio={ratio:.3f} cooldown={critical_cooldown_seconds}s", usage
    if projected_request_count > 0 and projected_ratio >= config.service.critical_ratio:
        usage["backoff_level"] = "critical"
        usage["cooldown_seconds"] = projected_critical_cooldown_seconds
        if critical_floor_seconds > projected_recovery_seconds:
            usage["cooldown_source"] = f"{budget_scope}_floor"
        return False, f"{provider}_budget_projected_critical ratio={ratio:.3f} projected_ratio={projected_ratio:.3f} projected_requests={projected_request_count} cooldown={projected_critical_cooldown_seconds}s", usage
    if ratio >= config.service.warn_ratio and warn_cooldown_seconds > 0:
        usage["backoff_level"] = "warn"
        usage["cooldown_seconds"] = warn_cooldown_seconds
        if warn_floor_seconds > warn_recovery_seconds:
            usage["cooldown_source"] = f"{budget_scope}_floor"
        return False, f"{provider}_budget_warn ratio={ratio:.3f} cooldown={warn_cooldown_seconds}s", usage
    if projected_request_count > 0 and projected_ratio >= config.service.warn_ratio and projected_warn_cooldown_seconds > 0:
        usage["backoff_level"] = "warn"
        usage["cooldown_seconds"] = projected_warn_cooldown_seconds
        if warn_floor_seconds > projected_warn_recovery_seconds:
            usage["cooldown_source"] = f"{budget_scope}_floor"
        return False, f"{provider}_budget_projected_warn ratio={ratio:.3f} projected_ratio={projected_ratio:.3f} projected_requests={projected_request_count} cooldown={projected_warn_cooldown_seconds}s", usage
    return True, None, usage


def _failure_backoff_profile(config: AppConfig, spec: TaskSpec, reason: str) -> tuple[str, int]:
    provider = spec.budget_provider
    critical_floor = 0
    auth_floor = 0
    if provider:
        critical_floor = config.service.backoff_floor_seconds_for(provider, level="critical", task_name=spec.name)
        auth_floor = config.service.auth_failure_backoff_floor_seconds_for(provider, task_name=spec.name)
    classification = "auth" if provider and looks_auth_style_failure(reason) else "generic"
    configured_floor = critical_floor
    if classification == "auth":
        configured_floor = max(configured_floor, auth_floor)
    return classification, configured_floor


def _failure_backoff_seconds(config: AppConfig, spec: TaskSpec, task_state: dict[str, Any], *, reason: str) -> tuple[int, str, int]:
    classification, configured_floor = _failure_backoff_profile(config, spec, reason)
    base_seconds = max(_FAILURE_BACKOFF_MIN_SECONDS, configured_floor)
    consecutive_failures = int(task_state.get("failure_backoff_consecutive_failures", 0)) + 1
    max_seconds = max(base_seconds, int(spec.every_seconds))
    cooldown_seconds = min(max_seconds, base_seconds * (2 ** max(0, consecutive_failures - 1)))
    return max(0, int(cooldown_seconds)), classification, configured_floor


def _clear_failure_backoff(task_state: dict[str, Any]) -> None:
    task_state.pop("failure_backoff_until_epoch", None)
    task_state.pop("failure_backoff_until", None)
    task_state.pop("failure_backoff_remaining_seconds", None)
    task_state.pop("failure_backoff_reason", None)
    task_state.pop("failure_backoff_consecutive_failures", None)
    task_state.pop("failure_backoff_class", None)
    task_state.pop("failure_backoff_floor_seconds", None)


def _set_failure_backoff(
    config: AppConfig,
    spec: TaskSpec,
    task_state: dict[str, Any],
    *,
    now: float,
    reason: str,
) -> dict[str, Any]:
    cooldown_seconds, failure_class, floor_seconds = _failure_backoff_seconds(config, spec, task_state, reason=reason)
    consecutive_failures = int(task_state.get("failure_backoff_consecutive_failures", 0)) + 1
    task_state["failure_backoff_consecutive_failures"] = consecutive_failures
    task_state["failure_backoff_reason"] = reason
    task_state["failure_backoff_class"] = failure_class
    task_state["failure_backoff_floor_seconds"] = floor_seconds
    task_state["failure_backoff_until_epoch"] = now + cooldown_seconds
    task_state["failure_backoff_until"] = _iso_after_seconds(cooldown_seconds)
    task_state["failure_backoff_remaining_seconds"] = cooldown_seconds
    return {
        "failure_backoff_until": task_state["failure_backoff_until"],
        "failure_backoff_remaining_seconds": cooldown_seconds,
        "failure_backoff_reason": reason,
        "failure_backoff_consecutive_failures": consecutive_failures,
        "failure_backoff_class": failure_class,
        "failure_backoff_floor_seconds": floor_seconds,
    }


def _summarize_task_failure(result: dict[str, Any]) -> str | None:
    reason = result.get("reason")
    if isinstance(reason, str) and reason.strip():
        return reason.strip()
    stderr = result.get("stderr")
    if isinstance(stderr, str) and stderr.strip():
        return stderr.strip().splitlines()[0]
    stdout = result.get("stdout")
    if isinstance(stdout, str) and stdout.strip():
        return stdout.strip().splitlines()[0]
    return None


def run_pending_tasks(config: AppConfig | None = None) -> dict[str, Any]:
    config = config or load_config()
    ensure_directories(config)
    state = _load_state(config)
    tasks_state = state.setdefault("tasks", {})
    now = time.time()
    results: list[dict[str, Any]] = []
    pruned = prune_api_request_events(retention_days=14, config=config)
    if pruned:
        _append_log(config, f"api_request_events_pruned={pruned}")

    for spec in _task_specs(config):
        task_state = tasks_state.setdefault(spec.name, {})
        task_state["budget_provider"] = spec.budget_provider
        task_state["budget_scope"] = config.service.budget_scope_for(spec.budget_provider, task_name=spec.name)
        task_state["every_seconds"] = int(spec.every_seconds)
        last_run = float(task_state.get("last_run_epoch", 0))
        if now - last_run < spec.every_seconds:
            _set_task_next_due(task_state, base_epoch=last_run, every_seconds=spec.every_seconds)
            continue
        backoff_until_epoch = float(task_state.get("budget_backoff_until_epoch", 0))
        if backoff_until_epoch > now:
            remaining = max(0, int(backoff_until_epoch - now))
            task_state.update(
                {
                    "last_status": "skipped",
                    "last_skipped_at": _now_iso(),
                    "last_skip_reason": f"budget_backoff_active remaining={remaining}s",
                    "budget_backoff_remaining_seconds": remaining,
                }
            )
            results.append(
                {
                    "task": spec.name,
                    "status": "skipped",
                    "reason": f"budget_backoff_active remaining={remaining}s",
                    "budget_backoff_until": task_state.get("budget_backoff_until"),
                    "budget_backoff_remaining_seconds": remaining,
                    "budget_backoff_level": task_state.get("budget_backoff_level"),
                    "budget_scope": task_state.get("budget_scope"),
                }
            )
            continue
        failure_backoff_until_epoch = float(task_state.get("failure_backoff_until_epoch", 0))
        if failure_backoff_until_epoch > now:
            remaining = max(0, int(failure_backoff_until_epoch - now))
            task_state.update(
                {
                    "last_status": "skipped",
                    "last_skipped_at": _now_iso(),
                    "last_skip_reason": f"failure_backoff_active remaining={remaining}s",
                    "failure_backoff_remaining_seconds": remaining,
                }
            )
            results.append(
                {
                    "task": spec.name,
                    "status": "skipped",
                    "reason": f"failure_backoff_active remaining={remaining}s",
                    "failure_backoff_until": task_state.get("failure_backoff_until"),
                    "failure_backoff_remaining_seconds": remaining,
                    "failure_backoff_reason": task_state.get("failure_backoff_reason"),
                    "failure_backoff_consecutive_failures": task_state.get("failure_backoff_consecutive_failures"),
                    "failure_backoff_class": task_state.get("failure_backoff_class"),
                    "failure_backoff_floor_seconds": task_state.get("failure_backoff_floor_seconds"),
                }
            )
            continue
        planned_fetch_mode, planned_full_refresh_reasons = _planned_fetch_mode(config, spec, task_state, now=now)
        allowed, reason, usage = _budget_gate(config, spec, task_state, fetch_mode=planned_fetch_mode)
        downgrade_reason = None
        downgrade_usage = None
        allowed, reason, usage, planned_fetch_mode, planned_full_refresh_reasons, downgrade_reason, downgrade_usage = _maybe_downgrade_fetch_mode_for_budget(
            config,
            spec,
            task_state,
            planned_fetch_mode=planned_fetch_mode,
            planned_full_refresh_reasons=planned_full_refresh_reasons,
            allowed=allowed,
            reason=reason,
            usage=usage,
        )
        if isinstance(usage, dict):
            for field in ("projected_request_count", "projected_request_total", "projected_ratio", "projected_request_source"):
                value = usage.get(field)
                if value is not None:
                    task_state[field] = value
                else:
                    task_state.pop(field, None)
        if not allowed:
            backoff_level = usage.get("backoff_level") if isinstance(usage, dict) else None
            recovery_seconds = int(usage.get("cooldown_seconds", 0)) if isinstance(usage, dict) else 0
            backoff_floor_seconds = 0
            cooldown_source = None
            if isinstance(usage, dict):
                floor_key = "warn_backoff_floor_seconds" if backoff_level == "warn" else "critical_backoff_floor_seconds"
                backoff_floor_seconds = int(usage.get(floor_key, 0))
                cooldown_source = usage.get("cooldown_source")
            skipped_at = _now_iso()
            task_state.update(
                {
                    "last_status": "skipped",
                    "last_skipped_at": skipped_at,
                    "last_skip_reason": reason,
                    "budget_backoff_level": backoff_level,
                    "budget_backoff_until_epoch": now + recovery_seconds,
                    "budget_backoff_until": _iso_after_seconds(recovery_seconds),
                    "budget_backoff_remaining_seconds": recovery_seconds,
                    "budget_backoff_floor_seconds": backoff_floor_seconds,
                    "budget_scope": task_state.get("budget_scope"),
                }
            )
            if isinstance(cooldown_source, str) and cooldown_source:
                task_state["budget_backoff_cooldown_source"] = cooldown_source
            else:
                task_state.pop("budget_backoff_cooldown_source", None)
            _mark_task_decision(task_state, decision_at=skipped_at)
            _set_task_next_due(task_state, base_epoch=now, every_seconds=spec.every_seconds)
            results.append(
                {
                    "task": spec.name,
                    "status": "skipped",
                    "reason": reason,
                    "api_usage": usage,
                    "budget_backoff_level": backoff_level,
                    "budget_backoff_until": task_state.get("budget_backoff_until"),
                    "budget_backoff_remaining_seconds": recovery_seconds,
                    "budget_backoff_floor_seconds": backoff_floor_seconds,
                    "budget_backoff_cooldown_source": task_state.get("budget_backoff_cooldown_source"),
                    "budget_scope": task_state.get("budget_scope"),
                }
            )
            _append_log(config, f"task={spec.name} status=skipped reason={reason}")
            continue
        started_epoch = time.time()
        started_at = datetime.fromtimestamp(started_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        try:
            full_refresh_requested = planned_fetch_mode == "full_refresh"
            if spec.name == "mal_refresh":
                result = _refresh_mal_tokens(config)
            elif spec.name.startswith("sync_fetch_"):
                provider = spec.name.removeprefix("sync_fetch_")
                full_refresh_reasons = list(planned_full_refresh_reasons)
                result = _run_subprocess(
                    config,
                    _provider_fetch_command(config, provider, full_refresh=full_refresh_requested),
                    label=spec.name,
                )
                result["fetch_mode"] = planned_fetch_mode or "incremental"
                if full_refresh_reasons:
                    result["full_refresh_reason"] = "+".join(full_refresh_reasons)
                if downgrade_reason:
                    result["deferred_full_refresh_reason"] = downgrade_reason
            elif spec.name == "sync_apply":
                result = _run_subprocess(config, _apply_sync_command(), label="sync_apply")
            elif spec.name == "health":
                result = _run_subprocess(config, [str(config.project_root / "scripts" / "run_health_check_cycle.sh")], label="health")
            else:
                result = {"status": "skipped", "reason": "unknown_task"}
            finished_epoch = time.time()
            finished_at = datetime.fromtimestamp(finished_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            if spec.budget_provider is not None and isinstance(usage, dict):
                before_request_count = int(usage.get("request_count", 0))
                after_usage = summarize_recent_api_usage(provider=spec.budget_provider, window_seconds=_BUDGET_GATE_WINDOW_SECONDS, config=config).as_dict()
                observed_request_delta = max(0, int(after_usage.get("request_count", 0)) - before_request_count)
                fetch_mode_for_history = planned_fetch_mode if spec.name.startswith("sync_fetch_") else None
                _record_observed_request_delta(
                    task_state,
                    observed_request_delta=observed_request_delta,
                    fetch_mode=fetch_mode_for_history,
                    finished_at=finished_at,
                    history_limit=config.service.projected_request_history_window_for(spec.name, provider=spec.budget_provider),
                )
                projected_request_count, projected_request_source = _refresh_projected_request_state(
                    config,
                    spec,
                    task_state,
                    fetch_mode=fetch_mode_for_history,
                )
                result["request_delta"] = observed_request_delta
                result["next_projected_request_count"] = projected_request_count
                if projected_request_source is not None:
                    result["next_projected_request_source"] = projected_request_source
                if fetch_mode_for_history is not None:
                    result["request_delta_by_mode"] = {fetch_mode_for_history: observed_request_delta}
            task_status = result.get("status", "ok")
            task_state.update({"last_run_epoch": now, "last_run_at": finished_at, "last_status": task_status, "last_result": result})
            _record_task_timing(task_state, started_epoch=started_epoch, finished_epoch=finished_epoch, started_at=started_at, finished_at=finished_at)
            _set_task_next_due(task_state, base_epoch=now, every_seconds=spec.every_seconds)
            fetch_succeeded = task_status != "error"
            if spec.name.startswith("sync_fetch_") and fetch_succeeded:
                task_state["last_fetch_mode"] = "full_refresh" if full_refresh_requested else "incremental"
                task_state["last_fetch_mode_at"] = finished_at
                if full_refresh_requested:
                    task_state["last_full_refresh_reason"] = result.get("full_refresh_reason")
                    task_state["last_successful_full_refresh_epoch"] = finished_epoch
                    task_state["last_successful_full_refresh_at"] = finished_at
                    task_state["full_refresh_anchor_epoch"] = finished_epoch
                    task_state["full_refresh_anchor_at"] = finished_at
                else:
                    task_state.pop("last_full_refresh_reason", None)
                    if not isinstance(task_state.get("full_refresh_anchor_epoch"), (int, float)):
                        task_state["full_refresh_anchor_epoch"] = finished_epoch
                        task_state["full_refresh_anchor_at"] = finished_at
            task_state.pop("last_skip_reason", None)
            task_state.pop("last_skipped_at", None)
            task_state.pop("budget_backoff_level", None)
            task_state.pop("budget_backoff_until_epoch", None)
            task_state.pop("budget_backoff_until", None)
            task_state.pop("budget_backoff_remaining_seconds", None)
            task_state.pop("budget_backoff_floor_seconds", None)
            task_state.pop("budget_backoff_cooldown_source", None)
            if task_status == "error":
                failure_reason = _summarize_task_failure(result) or "subprocess_error"
                task_state["last_error"] = failure_reason
                failure_backoff = _set_failure_backoff(config, spec, task_state, now=now, reason=failure_reason)
                results.append({"task": spec.name, **result, **failure_backoff})
                _append_log(
                    config,
                    f"task={spec.name} status=error failure_backoff={failure_backoff['failure_backoff_remaining_seconds']}s reason={failure_reason}",
                )
                continue
            task_state.pop("last_error", None)
            _clear_failure_backoff(task_state)
            results.append({"task": spec.name, **result})
        except (MalApiError, OSError, subprocess.SubprocessError) as exc:
            finished_epoch = time.time()
            finished_at = datetime.fromtimestamp(finished_epoch, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
            task_state.update({"last_run_epoch": now, "last_run_at": finished_at, "last_status": "error", "last_error": f"{type(exc).__name__}: {exc}"})
            _record_task_timing(task_state, started_epoch=started_epoch, finished_epoch=finished_epoch, started_at=started_at, finished_at=finished_at)
            _set_task_next_due(task_state, base_epoch=now, every_seconds=spec.every_seconds)
            task_state.pop("last_skip_reason", None)
            task_state.pop("last_skipped_at", None)
            task_state.pop("budget_backoff_level", None)
            task_state.pop("budget_backoff_until_epoch", None)
            task_state.pop("budget_backoff_until", None)
            task_state.pop("budget_backoff_remaining_seconds", None)
            task_state.pop("budget_backoff_floor_seconds", None)
            task_state.pop("budget_backoff_cooldown_source", None)
            failure_backoff = _set_failure_backoff(config, spec, task_state, now=now, reason=f"{type(exc).__name__}: {exc}")
            results.append({"task": spec.name, "status": "error", "error": f"{type(exc).__name__}: {exc}", **failure_backoff})
            _append_log(
                config,
                f"task={spec.name} status=error error={type(exc).__name__}: {exc} failure_backoff={failure_backoff['failure_backoff_remaining_seconds']}s",
            )

    state["last_loop_at"] = _now_iso()
    tracked_providers = {"mal", "crunchyroll", *config.service.provider_hourly_limits.keys(), *_available_source_providers(config)}
    state["api_usage"] = {
        provider: summarize_recent_api_usage(provider=provider, window_seconds=_BUDGET_GATE_WINDOW_SECONDS, config=config).as_dict()
        for provider in sorted(tracked_providers)
    }
    _save_state(config, state)
    return {"status": "ok", "results": results, "state_file": str(config.service_state_path), "api_usage": state["api_usage"]}

def run_service_loop(config: AppConfig | None = None) -> int:
    config = config or load_config()
    ensure_directories(config)
    _append_log(config, "service loop starting")
    while True:
        run_pending_tasks(config)
        time.sleep(max(5, int(config.service.loop_sleep_seconds)))
