from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import platform
import re
import shutil

from .auth import OAuthCallbackError, format_auth_flow_prompt, persist_token_response, wait_for_oauth_callback
from .auth_failure_signals import AUTH_STYLE_SESSION_PHASES, looks_auth_style_failure
from .config import ensure_directories, load_config, load_mal_secrets
from .crunchyroll_auth import (
    CrunchyrollAuthError,
    crunchyroll_login_with_credentials,
    load_crunchyroll_credentials,
    resolve_crunchyroll_state_paths,
)
from .crunchyroll_snapshot import CrunchyrollSnapshotError, snapshot_to_dict
from .hidive_auth import load_hidive_credentials, resolve_hidive_state_paths
from .provider_registry import get_provider, list_provider_slugs
from . import providers as _providers  # noqa: F401
from .db import (
    bootstrap_database,
    get_operational_snapshot,
    get_provider_series_title_map,
    list_review_queue_entries,
    list_series_mappings,
    refresh_review_queue_entries,
    update_review_queue_entry_statuses,
    upsert_series_mapping,
)
from .ingestion import ingest_snapshot_file, ingest_snapshot_payload
from .mal_client import MalApiError, MalClient
from .mapping import SeriesMappingInput, map_series, normalize_title
from .recommendation_metadata import refresh_recommendation_metadata
from .recommendations import build_recommendations, group_recommendations
from .service_manager import doctor_service, install_service, restart_service, service_status, start_service, stop_service, uninstall_service
from .service_runtime import run_pending_tasks, run_service_loop
from .sync_planner import (
    MAPPING_REVIEW_HEURISTICS_REVISION,
    build_dry_run_sync_plan,
    build_mapping_review,
    execute_approved_sync,
    load_provider_series_states,
    persist_mapping_review_queue,
    persist_sync_review_queue,
)
from .validation import SnapshotValidationError, validate_snapshot_payload


def _cmd_init(project_root: Path | None) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    print(f"project_root={config.project_root}")
    print(f"workspace_root={config.workspace_root}")
    print(f"runtime_root={config.runtime_root}")
    print(f"db_path={config.db_path}")
    return 0


def _cmd_status(project_root: Path | None) -> int:
    config = load_config(project_root)
    secrets = load_mal_secrets(config)
    crunchyroll_credentials = load_crunchyroll_credentials(config)
    crunchyroll_state = resolve_crunchyroll_state_paths(config)
    hidive_credentials = load_hidive_credentials(config)
    hidive_state = resolve_hidive_state_paths(config)
    print(f"project_root={config.project_root}")
    print(f"workspace_root={config.workspace_root}")
    print(f"runtime_root={config.runtime_root}")
    print(f"settings_path={config.settings_path}")
    print(f"config_dir={config.config_dir}")
    print(f"secrets_dir={config.secrets_dir}")
    print(f"data_dir={config.data_dir}")
    print(f"state_dir={config.state_dir}")
    print(f"cache_dir={config.cache_dir}")
    print(f"db_path={config.db_path}")
    print(f"contract_version={config.contract_version}")
    print(f"request_timeout_seconds={config.request_timeout_seconds}")
    print(f"completion_threshold={config.completion_threshold}")
    print(f"credits_skip_window_seconds={config.credits_skip_window_seconds}")
    print(f"mal.base_url={config.mal.base_url}")
    print(f"mal.auth_url={config.mal.auth_url}")
    print(f"mal.token_url={config.mal.token_url}")
    print(f"mal.bind_host={config.mal.bind_host}")
    print(f"mal.redirect_uri={config.mal.redirect_uri}")
    print(f"mal.request_spacing_seconds={config.mal.request_spacing_seconds}")
    print(f"mal.request_spacing_jitter_seconds={config.mal.request_spacing_jitter_seconds}")
    print(f"crunchyroll.locale={config.crunchyroll.locale}")
    print(f"crunchyroll.request_spacing_seconds={config.crunchyroll.request_spacing_seconds}")
    print(f"crunchyroll.request_spacing_jitter_seconds={config.crunchyroll.request_spacing_jitter_seconds}")
    print(f"crunchyroll.username_present={bool(crunchyroll_credentials.username)}")
    print(f"crunchyroll.password_present={bool(crunchyroll_credentials.password)}")
    print(f"crunchyroll.username_path={crunchyroll_credentials.username_path}")
    print(f"crunchyroll.password_path={crunchyroll_credentials.password_path}")
    print(f"crunchyroll.state_root={crunchyroll_state.root}")
    print(f"crunchyroll.refresh_token_path={crunchyroll_state.refresh_token_path}")
    print(f"crunchyroll.device_id_path={crunchyroll_state.device_id_path}")
    print(f"crunchyroll.session_state_path={crunchyroll_state.session_state_path}")
    print(f"crunchyroll.sync_boundary_path={crunchyroll_state.sync_boundary_path}")
    print(f"crunchyroll.refresh_token_present={crunchyroll_state.refresh_token_path.exists()}")
    print(f"crunchyroll.device_id_present={crunchyroll_state.device_id_path.exists()}")
    print(f"crunchyroll.sync_boundary_present={crunchyroll_state.sync_boundary_path.exists()}")
    print(f"hidive.username_present={bool(hidive_credentials.username)}")
    print(f"hidive.password_present={bool(hidive_credentials.password)}")
    print(f"hidive.username_path={hidive_credentials.username_path}")
    print(f"hidive.password_path={hidive_credentials.password_path}")
    print(f"hidive.state_root={hidive_state.root}")
    print(f"hidive.authorisation_token_path={hidive_state.access_token_path}")
    print(f"hidive.refresh_token_path={hidive_state.refresh_token_path}")
    print(f"hidive.session_state_path={hidive_state.session_state_path}")
    print(f"hidive.authorisation_token_present={hidive_state.access_token_path.exists()}")
    print(f"hidive.refresh_token_present={hidive_state.refresh_token_path.exists()}")
    print(f"mal.client_id_present={bool(secrets.client_id)}")
    print(f"mal.client_secret_present={bool(secrets.client_secret)}")
    print(f"mal.access_token_present={bool(secrets.access_token)}")
    print(f"mal.refresh_token_present={bool(secrets.refresh_token)}")
    print(f"mal.client_id_path={secrets.client_id_path}")
    print(f"mal.client_secret_path={secrets.client_secret_path}")
    print(f"mal.access_token_path={secrets.access_token_path}")
    print(f"mal.refresh_token_path={secrets.refresh_token_path}")
    return 0


def _cmd_service_status(project_root: Path | None, output_format: str) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    payload = doctor_service(config)
    if output_format == "summary":
        _emit_service_status_summary(payload)
    else:
        print(json.dumps(payload, indent=2))
    return 0


def _cmd_install_service(project_root: Path | None, start_now: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    result = install_service(start_now=start_now, config=config)
    print(json.dumps(result.details or {"status": result.status, "message": result.message}, indent=2))
    return 0


def _cmd_uninstall_service(stop_now: bool) -> int:
    result = uninstall_service(stop_now=stop_now)
    print(json.dumps(result.details or {"status": result.status, "message": result.message}, indent=2))
    return 0


def _cmd_start_service() -> int:
    result = start_service()
    print(json.dumps(result.details or {"status": result.status, "message": result.message}, indent=2))
    return 0


def _cmd_stop_service() -> int:
    result = stop_service()
    print(json.dumps(result.details or {"status": result.status, "message": result.message}, indent=2))
    return 0


def _cmd_restart_service() -> int:
    result = restart_service()
    print(json.dumps(result.details or {"status": result.status, "message": result.message}, indent=2))
    return 0


def _cmd_service_run_once(project_root: Path | None) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    print(json.dumps(run_pending_tasks(config), indent=2))
    return 0


def _cmd_service_run(project_root: Path | None) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    return run_service_loop(config)


def _cmd_bootstrap_audit(project_root: Path | None, summary_only: bool) -> int:
    config = load_config(project_root)
    secrets = load_mal_secrets(config)
    crunchyroll_credentials = load_crunchyroll_credentials(config)
    crunchyroll_state = resolve_crunchyroll_state_paths(config)
    hidive_credentials = load_hidive_credentials(config)
    hidive_state = resolve_hidive_state_paths(config)

    dependency_checks = {
        "python3": shutil.which("python3") is not None,
        "systemctl": shutil.which("systemctl") is not None,
        "flock": shutil.which("flock") is not None,
        "curl_cffi": importlib.util.find_spec("curl_cffi") is not None,
    }
    missing_dependencies = [name for name, present in dependency_checks.items() if not present]

    crunchyroll_credentials_present = bool(crunchyroll_credentials.username) and bool(crunchyroll_credentials.password)
    crunchyroll_session_present = crunchyroll_state.refresh_token_path.exists() and crunchyroll_state.device_id_path.exists()
    hidive_credentials_present = bool(hidive_credentials.username) and bool(hidive_credentials.password)
    hidive_session_present = hidive_state.access_token_path.exists() and hidive_state.refresh_token_path.exists()
    mal_app_present = bool(secrets.client_id)
    mal_oauth_present = bool(secrets.access_token) and bool(secrets.refresh_token)

    onboarding_steps: list[dict[str, object]] = []

    def add_onboarding_step(
        *,
        step: str,
        details: str,
        user_action_required: bool,
        command: str | None = None,
        command_args: list[str] | None = None,
        applies_to: str | None = None,
    ) -> None:
        onboarding_steps.append(
            {
                "step": step,
                "status": "missing",
                "user_action_required": user_action_required,
                "command": command,
                "command_args": command_args or [],
                "applies_to": applies_to,
                "details": details,
            }
        )

    if not dependency_checks["python3"]:
        add_onboarding_step(
            step="install-python",
            details="Install Python 3.10+ so the mal-updater console script and CLI can run.",
            user_action_required=True,
            applies_to="host",
        )
    if not dependency_checks["curl_cffi"]:
        add_onboarding_step(
            step="install-optional-crunchyroll-transport",
            details="Install the optional crunchyroll extra (`pip install -e '.[crunchyroll]'`) for browser-TLS impersonation against Crunchyroll.",
            user_action_required=False,
            command="python3 -m pip install -e '.[crunchyroll]'",
            command_args=["python3", "-m", "pip", "install", "-e", ".[crunchyroll]"],
            applies_to="crunchyroll",
        )

    if not mal_app_present:
        add_onboarding_step(
            step="create-mal-app",
            details=f"Create a MyAnimeList API app and record its client id at {secrets.client_id_path}. Configure redirect URI {config.mal.redirect_uri} in the MAL app settings.",
            user_action_required=True,
            applies_to="mal",
        )
    if not mal_oauth_present:
        add_onboarding_step(
            step="complete-mal-oauth",
            details="Run `mal-updater mal-auth-login` after the MAL app exists so the skill can persist access and refresh tokens.",
            user_action_required=True,
            command="PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login",
            command_args=["PYTHONPATH=src", "python3", "-m", "mal_updater.cli", "mal-auth-login"],
            applies_to="mal",
        )
    if not crunchyroll_credentials_present:
        add_onboarding_step(
            step="stage-crunchyroll-credentials",
            details=f"Store Crunchyroll credentials at {crunchyroll_credentials.username_path} and {crunchyroll_credentials.password_path}.",
            user_action_required=True,
            applies_to="crunchyroll",
        )
    if not crunchyroll_session_present:
        add_onboarding_step(
            step="bootstrap-crunchyroll-session",
            details="Run `mal-updater provider-auth-login --provider crunchyroll` to mint and stage the long-lived Crunchyroll refresh token/device id pair.",
            user_action_required=False,
            command="PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider crunchyroll",
            command_args=["PYTHONPATH=src", "python3", "-m", "mal_updater.cli", "provider-auth-login", "--provider", "crunchyroll"],
            applies_to="crunchyroll",
        )
    if not hidive_credentials_present:
        add_onboarding_step(
            step="stage-hidive-credentials",
            details=f"Store HIDIVE credentials at {hidive_credentials.username_path} and {hidive_credentials.password_path}.",
            user_action_required=True,
            applies_to="hidive",
        )
    if not hidive_session_present:
        add_onboarding_step(
            step="bootstrap-hidive-session",
            details="Run `mal-updater provider-auth-login --provider hidive` to mint and stage HIDIVE authorisation/refresh tokens.",
            user_action_required=False,
            command="PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider hidive",
            command_args=["PYTHONPATH=src", "python3", "-m", "mal_updater.cli", "provider-auth-login", "--provider", "hidive"],
            applies_to="hidive",
        )
    if not dependency_checks["systemctl"]:
        add_onboarding_step(
            step="install-service-manager",
            details="systemctl is unavailable; install/enable a compatible service manager or plan to run `mal-updater service-run` manually in the foreground.",
            user_action_required=True,
            applies_to="automation",
        )

    blocking_steps = [item for item in onboarding_steps if item["user_action_required"]]
    nonblocking_steps = [item for item in onboarding_steps if not item["user_action_required"]]
    actionable_commands = [item for item in onboarding_steps if isinstance(item.get("command"), str)]
    providers = {
        "crunchyroll": {
            "enabled_by_credentials": crunchyroll_credentials_present,
            "credentials_present": crunchyroll_credentials_present,
            "session_present": crunchyroll_session_present,
            "transport_ready": dependency_checks["curl_cffi"],
            "ready": crunchyroll_credentials_present and crunchyroll_session_present and dependency_checks["curl_cffi"],
            "missing": [
                name
                for name, present in (
                    ("credentials", crunchyroll_credentials_present),
                    ("session", crunchyroll_session_present),
                    ("transport", dependency_checks["curl_cffi"]),
                )
                if not present
            ],
            "bootstrap_command": "PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider crunchyroll",
        },
        "hidive": {
            "enabled_by_credentials": hidive_credentials_present,
            "credentials_present": hidive_credentials_present,
            "session_present": hidive_session_present,
            "transport_ready": True,
            "ready": hidive_credentials_present and hidive_session_present,
            "missing": [
                name
                for name, present in (
                    ("credentials", hidive_credentials_present),
                    ("session", hidive_session_present),
                )
                if not present
            ],
            "bootstrap_command": "PYTHONPATH=src python3 -m mal_updater.cli provider-auth-login --provider hidive",
        },
    }

    payload = {
        "project_root": str(config.project_root),
        "workspace_root": str(config.workspace_root),
        "runtime_root": str(config.runtime_root),
        "settings_path": str(config.settings_path),
        "runtime_paths": {
            "config_dir": str(config.config_dir),
            "secrets_dir": str(config.secrets_dir),
            "data_dir": str(config.data_dir),
            "state_dir": str(config.state_dir),
            "cache_dir": str(config.cache_dir),
            "db_path": str(config.db_path),
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
        },
        "dependencies": {
            "checks": dependency_checks,
            "missing": missing_dependencies,
        },
        "credentials": {
            "mal_client_id_present": mal_app_present,
            "mal_access_token_present": bool(secrets.access_token),
            "mal_refresh_token_present": bool(secrets.refresh_token),
            "crunchyroll_username_present": bool(crunchyroll_credentials.username),
            "crunchyroll_password_present": bool(crunchyroll_credentials.password),
            "crunchyroll_refresh_token_present": crunchyroll_state.refresh_token_path.exists(),
            "crunchyroll_device_id_present": crunchyroll_state.device_id_path.exists(),
            "hidive_username_present": bool(hidive_credentials.username),
            "hidive_password_present": bool(hidive_credentials.password),
            "hidive_authorisation_token_present": hidive_state.access_token_path.exists(),
            "hidive_refresh_token_present": hidive_state.refresh_token_path.exists(),
        },
        "services": {
            "installer_script": str(config.project_root / "scripts" / "install_user_systemd_units.sh"),
            "service_manager_available": dependency_checks["systemctl"],
            "service_unit_name": "mal-updater.service",
            "service_model": "user-systemd daemon",
        },
        "mal": {
            "client_id_present": mal_app_present,
            "oauth_ready": mal_oauth_present,
            "ready": mal_app_present and mal_oauth_present,
            "redirect_uri": config.mal.redirect_uri,
            "bind_host": config.mal.bind_host,
            "redirect_host": config.mal.redirect_host,
            "redirect_port": config.mal.redirect_port,
            "auth_command": "PYTHONPATH=src python3 -m mal_updater.cli mal-auth-login",
        },
        "providers": providers,
        "summary": {
            "blocking_step_count": len(blocking_steps),
            "nonblocking_step_count": len(nonblocking_steps),
            "actionable_command_count": len(actionable_commands),
            "ready_provider_count": sum(1 for provider in providers.values() if provider["ready"]),
            "provider_count": len(providers),
        },
        "onboarding_steps": onboarding_steps,
        "recommended_commands": actionable_commands,
        "ready": not onboarding_steps and not missing_dependencies,
    }

    if summary_only:
        print(f"ready={payload['ready']}")
        print(f"runtime_root={config.runtime_root}")
        print(f"settings_path={config.settings_path}")
        print(f"blocking_step_count={payload['summary']['blocking_step_count']}")
        print(f"nonblocking_step_count={payload['summary']['nonblocking_step_count']}")
        print(f"ready_provider_count={payload['summary']['ready_provider_count']}")
        if missing_dependencies:
            print("missing_dependencies=" + ", ".join(missing_dependencies))
        for provider_name, provider_payload in providers.items():
            print(f"provider_{provider_name}_ready={provider_payload['ready']}")
            missing = provider_payload.get("missing") if isinstance(provider_payload.get("missing"), list) else []
            if missing:
                print(f"provider_{provider_name}_missing=" + ", ".join(str(item) for item in missing))
        for item in onboarding_steps:
            print(f"next_step={item['step']}: {item['details']}")
            command = item.get("command")
            if isinstance(command, str) and command:
                print(f"next_command={command}")
        return 0

    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0



def _emit_service_status_summary(payload: dict[str, object]) -> None:
    print(f"unit_exists={bool(payload.get('unit_exists'))}")
    print(f"enabled={bool(payload.get('enabled'))}")
    print(f"active={bool(payload.get('active'))}")
    if payload.get("enabled_raw"):
        print(f"enabled_raw={payload['enabled_raw']}")
    if payload.get("active_raw"):
        print(f"active_raw={payload['active_raw']}")
    print(f"env_exists={bool(payload.get('env_exists'))}")
    print(f"service_state_exists={bool(payload.get('service_state_exists'))}")
    print(f"service_log_exists={bool(payload.get('service_log_exists'))}")
    print(f"health_latest_exists={bool(payload.get('health_latest_exists'))}")

    if isinstance(payload.get("last_loop_at"), str):
        print(f"last_loop_at={payload['last_loop_at']}")
        age_seconds = _age_seconds_from_timestamp(payload["last_loop_at"])
        if age_seconds is not None:
            print(f"last_loop_age_seconds={age_seconds:.1f}")

    service_state_parse_error = payload.get("service_state_parse_error")
    if isinstance(service_state_parse_error, str) and service_state_parse_error:
        print(f"service_state_parse_error={service_state_parse_error}")
    health_latest_parse_error = payload.get("health_latest_parse_error")
    if isinstance(health_latest_parse_error, str) and health_latest_parse_error:
        print(f"health_latest_parse_error={health_latest_parse_error}")

    health_latest = payload.get("health_latest_summary")
    if isinstance(health_latest, dict):
        if isinstance(health_latest.get("healthy"), bool):
            print(f"health_healthy={health_latest['healthy']}")
        warnings = health_latest.get("warnings") if isinstance(health_latest.get("warnings"), list) else []
        warning_count = health_latest.get("warning_count")
        if not isinstance(warning_count, int):
            warning_count = len(warnings)
        print(f"health_warning_count={warning_count}")
        warning_codes = [item.get("code") for item in warnings if isinstance(item, dict) and isinstance(item.get("code"), str)]
        if warning_codes:
            print("health_warnings=" + ", ".join(warning_codes))

        maintenance = health_latest.get("maintenance")
        if isinstance(maintenance, dict):
            recommended_command = maintenance.get("recommended_command")
            if isinstance(recommended_command, dict) and isinstance(recommended_command.get("command"), str):
                print("maintenance_recommended_command=" + recommended_command["command"])
            recommended_automation_command = maintenance.get("recommended_automation_command")
            if isinstance(recommended_automation_command, dict) and isinstance(recommended_automation_command.get("command"), str):
                print("maintenance_recommended_auto_command=" + recommended_automation_command["command"])

    api_usage = payload.get("api_usage")
    if isinstance(api_usage, dict):
        for provider_name in sorted(api_usage):
            provider_usage = api_usage.get(provider_name)
            if not isinstance(provider_usage, dict):
                continue
            request_count = provider_usage.get("request_count")
            if isinstance(request_count, int):
                print(f"api_{provider_name}_request_count={request_count}")
            success_count = provider_usage.get("success_count")
            if isinstance(success_count, int):
                print(f"api_{provider_name}_success_count={success_count}")
            error_count = provider_usage.get("error_count")
            if isinstance(error_count, int):
                print(f"api_{provider_name}_error_count={error_count}")
            last_event_at = provider_usage.get("last_event_at")
            if isinstance(last_event_at, str) and last_event_at:
                print(f"api_{provider_name}_last_event_at={last_event_at}")

    task_state = payload.get("task_state")
    if isinstance(task_state, dict):
        for task_name in sorted(task_state):
            task_payload = task_state.get(task_name)
            if not isinstance(task_payload, dict):
                continue
            status = task_payload.get("last_status") if isinstance(task_payload.get("last_status"), str) else None
            if status is not None:
                print(f"task_{task_name}_last_status={status}")
            last_run_at = task_payload.get("last_run_at") if isinstance(task_payload.get("last_run_at"), str) else None
            if last_run_at is not None:
                print(f"task_{task_name}_last_run_at={last_run_at}")
            last_skipped_at = task_payload.get("last_skipped_at") if isinstance(task_payload.get("last_skipped_at"), str) else None
            if last_skipped_at is not None:
                print(f"task_{task_name}_last_skipped_at={last_skipped_at}")
            last_skip_reason = task_payload.get("last_skip_reason") if isinstance(task_payload.get("last_skip_reason"), str) else None
            if last_skip_reason is not None:
                print(f"task_{task_name}_last_skip_reason={last_skip_reason}")
            last_error = task_payload.get("last_error") if isinstance(task_payload.get("last_error"), str) else None
            if last_error is not None:
                print(f"task_{task_name}_last_error={last_error}")
            last_decision_at = task_payload.get("last_decision_at") if isinstance(task_payload.get("last_decision_at"), str) else None
            if last_decision_at is not None:
                print(f"task_{task_name}_last_decision_at={last_decision_at}")
            last_started_at = task_payload.get("last_started_at") if isinstance(task_payload.get("last_started_at"), str) else None
            if last_started_at is not None:
                print(f"task_{task_name}_last_started_at={last_started_at}")
            last_finished_at = task_payload.get("last_finished_at") if isinstance(task_payload.get("last_finished_at"), str) else None
            if last_finished_at is not None:
                print(f"task_{task_name}_last_finished_at={last_finished_at}")
            last_duration_seconds = task_payload.get("last_duration_seconds") if isinstance(task_payload.get("last_duration_seconds"), (int, float)) else None
            if last_duration_seconds is not None:
                print(f"task_{task_name}_last_duration_seconds={last_duration_seconds}")
            every_seconds = task_payload.get("every_seconds") if isinstance(task_payload.get("every_seconds"), int) else None
            if every_seconds is not None:
                print(f"task_{task_name}_every_seconds={every_seconds}")
            budget_provider = task_payload.get("budget_provider") if isinstance(task_payload.get("budget_provider"), str) else None
            if budget_provider is not None:
                print(f"task_{task_name}_budget_provider={budget_provider}")
            budget_scope = task_payload.get("budget_scope") if isinstance(task_payload.get("budget_scope"), str) else None
            if budget_scope is not None:
                print(f"task_{task_name}_budget_scope={budget_scope}")
            projected_request_source = task_payload.get("projected_request_source") if isinstance(task_payload.get("projected_request_source"), str) else None
            if projected_request_source is not None:
                print(f"task_{task_name}_projected_request_source={projected_request_source}")
            projected_request_count = task_payload.get("projected_request_count") if isinstance(task_payload.get("projected_request_count"), int) else None
            if projected_request_count is not None:
                print(f"task_{task_name}_projected_request_count={projected_request_count}")
            projected_request_total = task_payload.get("projected_request_total") if isinstance(task_payload.get("projected_request_total"), int) else None
            if projected_request_total is not None:
                print(f"task_{task_name}_projected_request_total={projected_request_total}")
            projected_ratio = task_payload.get("projected_ratio") if isinstance(task_payload.get("projected_ratio"), (int, float)) else None
            if projected_ratio is not None:
                print(f"task_{task_name}_projected_ratio={projected_ratio}")
            last_request_delta = task_payload.get("last_request_delta") if isinstance(task_payload.get("last_request_delta"), int) else None
            if last_request_delta is not None:
                print(f"task_{task_name}_last_request_delta={last_request_delta}")
            last_fetch_mode = task_payload.get("last_fetch_mode") if isinstance(task_payload.get("last_fetch_mode"), str) else None
            if last_fetch_mode is not None:
                print(f"task_{task_name}_last_fetch_mode={last_fetch_mode}")
            last_full_refresh_reason = task_payload.get("last_full_refresh_reason") if isinstance(task_payload.get("last_full_refresh_reason"), str) else None
            if last_full_refresh_reason is not None:
                print(f"task_{task_name}_last_full_refresh_reason={last_full_refresh_reason}")
            next_due_at = task_payload.get("next_due_at") if isinstance(task_payload.get("next_due_at"), str) else None
            if next_due_at is not None:
                print(f"task_{task_name}_next_due_at={next_due_at}")
            next_due_in_seconds = task_payload.get("next_due_in_seconds") if isinstance(task_payload.get("next_due_in_seconds"), int) else None
            if next_due_in_seconds is not None:
                print(f"task_{task_name}_next_due_in_seconds={next_due_in_seconds}")
            budget_backoff_level = task_payload.get("budget_backoff_level") if isinstance(task_payload.get("budget_backoff_level"), str) else None
            if budget_backoff_level is not None:
                print(f"task_{task_name}_budget_backoff_level={budget_backoff_level}")
            budget_backoff_until = task_payload.get("budget_backoff_until") if isinstance(task_payload.get("budget_backoff_until"), str) else None
            if budget_backoff_until is not None:
                print(f"task_{task_name}_budget_backoff_until={budget_backoff_until}")
            budget_backoff_remaining_seconds = task_payload.get("budget_backoff_remaining_seconds") if isinstance(task_payload.get("budget_backoff_remaining_seconds"), int) else None
            if budget_backoff_remaining_seconds is not None:
                print(f"task_{task_name}_budget_backoff_remaining_seconds={budget_backoff_remaining_seconds}")
            budget_backoff_floor_seconds = task_payload.get("budget_backoff_floor_seconds") if isinstance(task_payload.get("budget_backoff_floor_seconds"), int) else None
            if budget_backoff_floor_seconds is not None:
                print(f"task_{task_name}_budget_backoff_floor_seconds={budget_backoff_floor_seconds}")
            budget_backoff_cooldown_source = task_payload.get("budget_backoff_cooldown_source") if isinstance(task_payload.get("budget_backoff_cooldown_source"), str) else None
            if budget_backoff_cooldown_source is not None:
                print(f"task_{task_name}_budget_backoff_cooldown_source={budget_backoff_cooldown_source}")
            failure_backoff_until = task_payload.get("failure_backoff_until") if isinstance(task_payload.get("failure_backoff_until"), str) else None
            if failure_backoff_until is not None:
                print(f"task_{task_name}_failure_backoff_until={failure_backoff_until}")
            failure_backoff_remaining_seconds = task_payload.get("failure_backoff_remaining_seconds") if isinstance(task_payload.get("failure_backoff_remaining_seconds"), int) else None
            if failure_backoff_remaining_seconds is not None:
                print(f"task_{task_name}_failure_backoff_remaining_seconds={failure_backoff_remaining_seconds}")
            failure_backoff_reason = task_payload.get("failure_backoff_reason") if isinstance(task_payload.get("failure_backoff_reason"), str) else None
            if failure_backoff_reason is not None:
                print(f"task_{task_name}_failure_backoff_reason={failure_backoff_reason}")
            failure_backoff_class = task_payload.get("failure_backoff_class") if isinstance(task_payload.get("failure_backoff_class"), str) else None
            if failure_backoff_class is not None:
                print(f"task_{task_name}_failure_backoff_class={failure_backoff_class}")
            failure_backoff_floor_seconds = task_payload.get("failure_backoff_floor_seconds") if isinstance(task_payload.get("failure_backoff_floor_seconds"), int) else None
            if failure_backoff_floor_seconds is not None:
                print(f"task_{task_name}_failure_backoff_floor_seconds={failure_backoff_floor_seconds}")
            failure_backoff_consecutive_failures = task_payload.get("failure_backoff_consecutive_failures") if isinstance(task_payload.get("failure_backoff_consecutive_failures"), int) else None
            if failure_backoff_consecutive_failures is not None:
                print(f"task_{task_name}_failure_backoff_consecutive_failures={failure_backoff_consecutive_failures}")

    service_log_tail = payload.get("service_log_tail")
    if isinstance(service_log_tail, list) and service_log_tail:
        last_log_line = service_log_tail[-1]
        if isinstance(last_log_line, str) and last_log_line:
            print(f"service_log_last_line={last_log_line}")


def _parse_sqlite_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    normalized = value.strip().replace("T", " ")
    if normalized.endswith("Z"):
        normalized = normalized[:-1]
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)



def _age_seconds_from_timestamp(value: object) -> float | None:
    parsed = _parse_sqlite_timestamp(value)
    if parsed is None:
        return None
    return max(0.0, (datetime.now(timezone.utc) - parsed).total_seconds())



def _sync_run_summary_counts(sync_run: dict[str, object] | None) -> dict[str, int]:
    if not isinstance(sync_run, dict):
        return {}
    summary = sync_run.get("summary")
    if not isinstance(summary, dict):
        return {}
    counts: dict[str, int] = {}
    for field in ("series_count", "progress_count", "watchlist_count"):
        value = summary.get(field)
        if isinstance(value, bool):
            continue
        if isinstance(value, (int, float)):
            counts[field] = max(0, int(value))
    return counts



def _build_partial_sync_coverage(
    latest_sync_run: dict[str, object] | None,
    provider_counts: dict[str, object] | None,
) -> dict[str, object] | None:
    latest_counts = _sync_run_summary_counts(latest_sync_run)
    if not latest_counts or not isinstance(provider_counts, dict):
        return None

    field_map = {
        "series_count": "series",
        "progress_count": "progress",
        "watchlist_count": "watchlist",
    }
    partial_fields: dict[str, dict[str, object]] = {}
    for summary_field, provider_field in field_map.items():
        latest_value = latest_counts.get(summary_field)
        provider_value = provider_counts.get(provider_field)
        if not isinstance(latest_value, int):
            continue
        if not isinstance(provider_value, int) or provider_value <= 0:
            continue
        if latest_value >= provider_value:
            continue
        partial_fields[provider_field] = {
            "latest_sync_run_count": latest_value,
            "provider_total_count": provider_value,
            "coverage_ratio": round(latest_value / provider_value, 4),
        }

    if not partial_fields:
        return None

    return {
        "sync_run_id": latest_sync_run.get("id") if isinstance(latest_sync_run, dict) else None,
        "fields": partial_fields,
    }



def _build_mapping_coverage_snapshot(
    provider_counts: dict[str, object] | None,
    mapping_counts: dict[str, object] | None,
) -> dict[str, object] | None:
    if not isinstance(provider_counts, dict) or not isinstance(mapping_counts, dict):
        return None
    provider_series_count = provider_counts.get("series")
    approved_mapping_count = mapping_counts.get("approved")
    total_mapping_count = mapping_counts.get("total")
    if not isinstance(provider_series_count, int) or provider_series_count < 0:
        return None
    if not isinstance(approved_mapping_count, int) or approved_mapping_count < 0:
        return None
    if not isinstance(total_mapping_count, int) or total_mapping_count < 0:
        total_mapping_count = approved_mapping_count

    coverage_ratio = None
    if provider_series_count > 0:
        coverage_ratio = round(min(1.0, approved_mapping_count / provider_series_count), 4)

    return {
        "provider_series_count": provider_series_count,
        "approved_mapping_count": approved_mapping_count,
        "unmapped_series_count": max(0, provider_series_count - approved_mapping_count),
        "total_mapping_count": total_mapping_count,
        "approved_coverage_ratio": coverage_ratio,
    }



def _build_mapping_review_revision_snapshot(items: list[object]) -> dict[str, object] | None:
    if not isinstance(items, list):
        return None
    total_open = 0
    stale_items: list[dict[str, object]] = []
    for item in items:
        payload = item.payload if hasattr(item, "payload") else None
        if not isinstance(payload, dict):
            continue
        total_open += 1
        revision = payload.get("mapper_revision")
        if revision == MAPPING_REVIEW_HEURISTICS_REVISION:
            continue
        provider_series_id = item.provider_series_id if hasattr(item, "provider_series_id") else None
        stale_items.append(
            {
                "provider_series_id": provider_series_id,
                "title": payload.get("title") if isinstance(payload.get("title"), str) else None,
                "mapper_revision": revision if isinstance(revision, str) and revision else None,
            }
        )
    return {
        "current_revision": MAPPING_REVIEW_HEURISTICS_REVISION,
        "open_count": total_open,
        "stale_open_count": len(stale_items),
        "stale_examples": stale_items[:10],
        "all_current": len(stale_items) == 0,
    }



def _format_systemd_usec_timestamp(value: str) -> str | None:
    raw = value.strip()
    if not raw or raw == "0":
        return None
    try:
        timestamp = int(raw) / 1_000_000
    except ValueError:
        return None
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat().replace("+00:00", "Z")



def _read_systemd_user_unit_runtime(unit_name: str) -> dict[str, object]:
    properties = [
        "ActiveState",
        "SubState",
        "UnitFileState",
        "NextElapseUSecRealtime",
        "LastTriggerUSec",
        "Result",
    ]
    try:
        result = subprocess.run(
            [
                "systemctl",
                "--user",
                "show",
                unit_name,
                *(f"--property={name}" for name in properties),
            ],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,
        )
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": str(exc)}

    if result.returncode != 0:
        error = (result.stderr or result.stdout or f"systemctl exited with code {result.returncode}").strip()
        return {"available": False, "error": error}

    runtime: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        if key in properties:
            runtime[key] = value
    return {
        "available": True,
        "active_state": runtime.get("ActiveState") or None,
        "sub_state": runtime.get("SubState") or None,
        "unit_file_state": runtime.get("UnitFileState") or None,
        "next_elapse_at": _format_systemd_usec_timestamp(runtime.get("NextElapseUSecRealtime") or ""),
        "last_trigger_at": _format_systemd_usec_timestamp(runtime.get("LastTriggerUSec") or ""),
        "result": runtime.get("Result") or None,
    }



def _render_systemd_unit_template(source_path: Path, project_root: Path, env_path: Path) -> str:
    text = source_path.read_text(encoding="utf-8")
    return text.replace("__MAL_UPDATER_REPO_ROOT__", str(project_root)).replace(
        "__MAL_UPDATER_SERVICE_ENV_FILE__", str(env_path)
    )


def _build_automation_installation_status(project_root: Path) -> dict[str, object] | None:
    source_dir = project_root / "ops" / "systemd-user"
    script_path = project_root / "scripts" / "install_user_systemd_units.sh"
    unit_name = "mal-updater.service"
    source_path = source_dir / unit_name
    if not source_dir.is_dir() or not script_path.exists() or not source_path.exists():
        return None

    config_home = Path(os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config"))
    target_dir = config_home / "systemd" / "user"
    env_path = config_home / "mal-updater-service.env"
    target_path = target_dir / unit_name
    installed = target_path.exists()
    content_matches_repo = False
    if installed:
        try:
            rendered_source = _render_systemd_unit_template(source_path, project_root, env_path)
            content_matches_repo = rendered_source == target_path.read_text(encoding="utf-8")
        except OSError:
            content_matches_repo = False
    runtime_state = _read_systemd_user_unit_runtime(unit_name) if installed else None
    enabled = None
    active = None
    runtime_state_error = None
    if isinstance(runtime_state, dict):
        if runtime_state.get("available") is True:
            enabled = runtime_state.get("unit_file_state") == "enabled"
            active = runtime_state.get("active_state") == "active"
        else:
            runtime_state_error = str(runtime_state.get("error") or "runtime state unavailable")
    return {
        "available": True,
        "source_dir": str(source_dir),
        "install_script_path": str(script_path),
        "target_dir": str(target_dir),
        "env_path": str(env_path),
        "env_present": env_path.exists(),
        "unit_name": unit_name,
        "unit": {
            "installed": installed,
            "target_path": str(target_path),
            "content_matches_repo": content_matches_repo if installed else None,
            "enabled": enabled,
            "active": active,
            "runtime_state": runtime_state,
        },
        "all_units_installed": installed,
        "all_units_current": installed and content_matches_repo,
        "service_enabled": enabled,
        "service_active": active,
        "runtime_state_available": bool(isinstance(runtime_state, dict) and runtime_state.get("available") is True),
        "runtime_state_error": runtime_state_error,
        "missing_units": [] if installed else [unit_name],
        "outdated_units": [] if (not installed or content_matches_repo) else [unit_name],
        "disabled_services": [] if (enabled is None or enabled) else [unit_name],
        "inactive_services": [] if (active is None or active) else [unit_name],
    }



def _load_service_state_for_health(config: AppConfig) -> dict[str, object] | None:
    if not config.service_state_path.exists():
        return None
    try:
        payload = json.loads(config.service_state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(payload, dict):
        return None
    return payload


def _load_json_dict(path: Path) -> dict[str, object] | None:
    if not path.exists():
        return None
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def _provider_auth_session_residue(config: AppConfig, provider: str) -> dict[str, object] | None:
    if provider == "crunchyroll":
        session_path = resolve_crunchyroll_state_paths(config).session_state_path
        phase_key = "crunchyroll_phase"
    elif provider == "hidive":
        session_path = resolve_hidive_state_paths(config).session_state_path
        phase_key = "hidive_phase"
    else:
        return None
    payload = _load_json_dict(session_path)
    if not isinstance(payload, dict):
        return None
    phase = payload.get(phase_key)
    last_error = payload.get("last_error")
    residue: dict[str, object] = {}
    if isinstance(phase, str) and phase in AUTH_STYLE_SESSION_PHASES:
        residue["session_phase"] = phase
    if isinstance(last_error, str) and last_error.strip():
        residue["session_last_error"] = last_error.strip()
    return residue or None


def _provider_service_auth_failure(
    service_state: dict[str, object] | None,
    *,
    provider: str,
    config: AppConfig,
    min_consecutive_failures: int = 2,
) -> dict[str, object] | None:
    if not isinstance(service_state, dict):
        return None
    tasks = service_state.get("tasks")
    if not isinstance(tasks, dict):
        return None
    task_state = tasks.get(f"sync_fetch_{provider}")
    if not isinstance(task_state, dict):
        return None
    reason = task_state.get("failure_backoff_reason") or task_state.get("last_error")
    if not isinstance(reason, str) or not reason.strip():
        return None
    consecutive_failures = task_state.get("failure_backoff_consecutive_failures", 0)
    if not isinstance(consecutive_failures, (int, float)) or int(consecutive_failures) < min_consecutive_failures:
        return None
    session_residue = _provider_auth_session_residue(config, provider)
    if not looks_auth_style_failure(reason, session_residue=session_residue):
        return None
    payload: dict[str, object] = {
        "provider": provider,
        "reason": reason.strip(),
        "consecutive_failures": int(consecutive_failures),
    }
    if isinstance(task_state.get("failure_backoff_until"), str):
        payload["failure_backoff_until"] = task_state["failure_backoff_until"]
    if isinstance(task_state.get("failure_backoff_remaining_seconds"), (int, float)):
        payload["failure_backoff_remaining_seconds"] = int(task_state["failure_backoff_remaining_seconds"])
    if isinstance(task_state.get("failure_backoff_class"), str):
        payload["failure_backoff_class"] = task_state["failure_backoff_class"]
    if isinstance(task_state.get("failure_backoff_floor_seconds"), (int, float)):
        payload["failure_backoff_floor_seconds"] = int(task_state["failure_backoff_floor_seconds"])
    if isinstance(session_residue, dict):
        payload.update(session_residue)
    return payload


def _build_health_maintenance_commands(
    *,
    crunchyroll_credentials_present: bool,
    crunchyroll_state_present: bool,
    hidive_credentials_present: bool,
    hidive_state_present: bool,
    mal_client_id_present: bool,
    mal_auth_present: bool,
    latest_sync_run: dict[str, object] | None,
    latest_completed_sync_run: dict[str, object] | None,
    latest_completed_age_seconds: float | None,
    stale_hours: float,
    crunchyroll_snapshot_output_path: Path,
    hidive_snapshot_output_path: Path,
    partial_sync_coverage: dict[str, object] | None = None,
    mapping_coverage: dict[str, object] | None = None,
    mapping_coverage_threshold: float | None = None,
    maintenance_review_limit: int = 25,
    automation_installation: dict[str, object] | None = None,
    review_queue_refresh_command_args: list[str] | None = None,
    review_queue_refresh_worklist_command_args: list[str] | None = None,
    provider_auth_failures: dict[str, dict[str, object]] | None = None,
) -> list[dict[str, object]]:
    commands: list[dict[str, object]] = []
    seen_commands: set[str] = set()

    def add_command(
        reason_code: str,
        detail: str,
        args: list[str],
        *,
        automation_safe: bool,
        requires_auth_interaction: bool,
        command_builder=None,
    ) -> None:
        command = command_builder(args) if command_builder is not None else _build_review_queue_command(args)
        if command in seen_commands:
            return
        seen_commands.add(command)
        commands.append(
            {
                "reason_code": reason_code,
                "detail": detail,
                "command_args": args,
                "command": command,
                "automation_safe": automation_safe,
                "requires_auth_interaction": requires_auth_interaction,
            }
        )

    if crunchyroll_credentials_present and not crunchyroll_state_present:
        add_command(
            "missing_crunchyroll_state",
            "Re-bootstrap Crunchyroll auth state from the staged local credentials",
            ["crunchyroll-auth-login"],
            automation_safe=False,
            requires_auth_interaction=False,
        )
    if hidive_credentials_present and not hidive_state_present:
        add_command(
            "missing_hidive_state",
            "Re-bootstrap HIDIVE auth state from the staged local credentials",
            ["provider-auth-login", "--provider", "hidive"],
            automation_safe=False,
            requires_auth_interaction=False,
        )

    if mal_client_id_present and not mal_auth_present:
        add_command(
            "missing_mal_auth_material",
            "Complete MAL OAuth and persist fresh access/refresh tokens",
            ["mal-auth-login"],
            automation_safe=False,
            requires_auth_interaction=True,
        )

    if isinstance(provider_auth_failures, dict):
        crunchyroll_failure = provider_auth_failures.get("crunchyroll")
        if crunchyroll_credentials_present and isinstance(crunchyroll_failure, dict):
            detail = (
                "Re-bootstrap Crunchyroll auth state after repeated auth-style unattended fetch failures"
            )
            reason = crunchyroll_failure.get("reason")
            if isinstance(reason, str) and reason:
                detail += f": {reason}"
            add_command(
                "rebootstrap_crunchyroll_auth_after_failures",
                detail,
                ["crunchyroll-auth-login"],
                automation_safe=False,
                requires_auth_interaction=False,
            )
        hidive_failure = provider_auth_failures.get("hidive")
        if hidive_credentials_present and isinstance(hidive_failure, dict):
            detail = (
                "Re-bootstrap HIDIVE auth state after repeated auth-style unattended fetch failures"
            )
            reason = hidive_failure.get("reason")
            if isinstance(reason, str) and reason:
                detail += f": {reason}"
            add_command(
                "rebootstrap_hidive_auth_after_failures",
                detail,
                ["provider-auth-login", "--provider", "hidive"],
                automation_safe=False,
                requires_auth_interaction=False,
            )

    snapshot_needs_refresh = not isinstance(latest_completed_sync_run, dict)
    if latest_completed_age_seconds is not None and latest_completed_age_seconds > stale_hours * 3600:
        snapshot_needs_refresh = True
    if isinstance(latest_sync_run, dict) and latest_sync_run.get("status") == "failed":
        snapshot_needs_refresh = True

    refresh_provider = "crunchyroll"
    if isinstance(latest_completed_sync_run, dict) and isinstance(latest_completed_sync_run.get("provider"), str):
        refresh_provider = str(latest_completed_sync_run.get("provider"))
    elif hidive_credentials_present and hidive_state_present and not crunchyroll_credentials_present:
        refresh_provider = "hidive"

    provider_ready = {
        "crunchyroll": crunchyroll_credentials_present and crunchyroll_state_present,
        "hidive": hidive_credentials_present and hidive_state_present,
    }
    provider_snapshot_output = {
        "crunchyroll": crunchyroll_snapshot_output_path,
        "hidive": hidive_snapshot_output_path,
    }
    provider_refresh_args = {
        "crunchyroll": ["crunchyroll-fetch-snapshot"],
        "hidive": ["provider-fetch-snapshot", "--provider", "hidive"],
    }
    provider_label = {
        "crunchyroll": "Crunchyroll",
        "hidive": "HIDIVE",
    }

    if provider_ready.get(refresh_provider) and isinstance(partial_sync_coverage, dict):
        add_command(
            "refresh_full_snapshot",
            f"Run a full-refresh {provider_label.get(refresh_provider, refresh_provider)} ingest so untouched older rows are refreshed instead of only the incremental overlap page",
            [*provider_refresh_args[refresh_provider], "--full-refresh", "--out", str(provider_snapshot_output[refresh_provider]), "--ingest"],
            automation_safe=True,
            requires_auth_interaction=False,
        )
    elif provider_ready.get(refresh_provider) and snapshot_needs_refresh:
        add_command(
            "refresh_ingested_snapshot",
            f"Fetch a fresh {provider_label.get(refresh_provider, refresh_provider)} snapshot and ingest it so health state is current again",
            [*provider_refresh_args[refresh_provider], "--out", str(provider_snapshot_output[refresh_provider]), "--ingest"],
            automation_safe=True,
            requires_auth_interaction=False,
        )

    missing_units = automation_installation.get("missing_units") if isinstance(automation_installation, dict) else None
    outdated_units = automation_installation.get("outdated_units") if isinstance(automation_installation, dict) else None
    disabled_services = automation_installation.get("disabled_services") if isinstance(automation_installation, dict) else None
    inactive_services = automation_installation.get("inactive_services") if isinstance(automation_installation, dict) else None
    install_script_path = automation_installation.get("install_script_path") if isinstance(automation_installation, dict) else None
    if (
        isinstance(install_script_path, str)
        and install_script_path
        and (
            (isinstance(missing_units, list) and missing_units)
            or (isinstance(outdated_units, list) and outdated_units)
            or (isinstance(disabled_services, list) and disabled_services)
            or (isinstance(inactive_services, list) and inactive_services)
        )
    ):
        detail = "Install the repo-owned user systemd service so MAL-Updater can run as a persistent unattended daemon"
        if isinstance(outdated_units, list) and outdated_units:
            detail = "Reinstall/update the repo-owned user systemd service so the installed daemon matches the current repo version"
        elif isinstance(disabled_services, list) and disabled_services:
            detail = "Enable the repo-owned user systemd service so the background daemon starts automatically for this user"
        elif isinstance(inactive_services, list) and inactive_services:
            detail = "Restart the repo-owned user systemd service so the background daemon is actually active in the user runtime"
        add_command(
            "install_user_systemd_service",
            detail,
            [install_script_path],
            automation_safe=True,
            requires_auth_interaction=False,
            command_builder=_build_shell_command,
        )

    if review_queue_refresh_worklist_command_args and mal_auth_present:
        add_command(
            "refresh_mapping_review_worklist",
            "Re-evaluate the highest-signal open mapping-review slices under the latest mapper heuristics before rebuilding the whole backlog",
            review_queue_refresh_worklist_command_args,
            automation_safe=True,
            requires_auth_interaction=False,
        )
    elif review_queue_refresh_command_args and mal_auth_present:
        add_command(
            "refresh_mapping_review_queue",
            "Re-evaluate the highest-signal open mapping-review slice under the latest mapper heuristics before rebuilding the whole backlog",
            review_queue_refresh_command_args,
            automation_safe=True,
            requires_auth_interaction=False,
        )

    coverage_ratio = mapping_coverage.get("approved_coverage_ratio") if isinstance(mapping_coverage, dict) else None
    unmapped_series_count = mapping_coverage.get("unmapped_series_count") if isinstance(mapping_coverage, dict) else None
    if (
        provider_ready.get(refresh_provider)
        and not isinstance(partial_sync_coverage, dict)
        and isinstance(coverage_ratio, float)
        and isinstance(unmapped_series_count, int)
        and unmapped_series_count > 0
        and isinstance(mapping_coverage_threshold, float)
        and coverage_ratio < mapping_coverage_threshold
    ):
        threshold_percent = int(round(mapping_coverage_threshold * 100))
        recommended_review_limit = max(0, int(maintenance_review_limit))
        review_command_args = ["review-mappings", "--limit", str(recommended_review_limit), "--mapping-limit", "5", "--persist-review-queue"]
        detail = (
            f"Run a bounded mapping review pass and persist the resulting residue because approved mapping coverage is still below {threshold_percent}%"
        )
        if recommended_review_limit == 0:
            detail = f"Rebuild mapping review residue because approved mapping coverage is still below {threshold_percent}%"
        add_command(
            "refresh_mapping_review_backlog",
            detail,
            review_command_args,
            automation_safe=True,
            requires_auth_interaction=False,
        )

    return commands



def _select_maintenance_command(
    recommended_commands: object,
    *,
    require_automation_safe: bool = False,
) -> dict[str, object] | None:
    if not isinstance(recommended_commands, list):
        return None
    for item in recommended_commands:
        if not isinstance(item, dict):
            continue
        command = item.get("command")
        if not isinstance(command, str) or not command:
            continue
        if require_automation_safe:
            if item.get("automation_safe") is not True:
                continue
            if item.get("requires_auth_interaction") is True:
                continue
        return item
    return None



def _emit_health_check_summary(payload: dict[str, object]) -> None:
    warnings = payload.get("warnings") if isinstance(payload.get("warnings"), list) else []
    warning_codes = [item.get("code") for item in warnings if isinstance(item, dict) and item.get("code")]
    review_queue = payload.get("review_queue") if isinstance(payload.get("review_queue"), dict) else {}
    recommended_next = review_queue.get("recommended_next") if isinstance(review_queue.get("recommended_next"), dict) else None
    recommended_worklist = review_queue.get("recommended_worklist") if isinstance(review_queue.get("recommended_worklist"), list) else []
    recommended_apply_worklist = review_queue.get("recommended_apply_worklist") if isinstance(review_queue.get("recommended_apply_worklist"), dict) else None
    recommended_refresh_worklist = review_queue.get("recommended_refresh_worklist") if isinstance(review_queue.get("recommended_refresh_worklist"), dict) else None
    maintenance = payload.get("maintenance") if isinstance(payload.get("maintenance"), dict) else {}
    recommended_commands = maintenance.get("recommended_commands") if isinstance(maintenance.get("recommended_commands"), list) else []
    automation = payload.get("automation") if isinstance(payload.get("automation"), dict) else None
    mappings = payload.get("mappings") if isinstance(payload.get("mappings"), dict) else {}
    mapping_coverage = mappings.get("coverage") if isinstance(mappings.get("coverage"), dict) else None
    mapping_review_revision = review_queue.get("mapping_review_revision") if isinstance(review_queue.get("mapping_review_revision"), dict) else None

    install_units_command = None
    if isinstance(recommended_commands, list):
        for item in recommended_commands:
            if not isinstance(item, dict):
                continue
            if item.get("reason_code") != "install_user_systemd_service":
                continue
            command = item.get("command")
            if isinstance(command, str) and command:
                install_units_command = command
                break

    print(f"healthy={bool(payload.get('healthy'))}")
    print(f"warning_count={len(warnings)}")
    if isinstance(mapping_coverage, dict):
        approved_count = mapping_coverage.get("approved_mapping_count")
        provider_series_count = mapping_coverage.get("provider_series_count")
        coverage_ratio = mapping_coverage.get("approved_coverage_ratio")
        if isinstance(approved_count, int) and isinstance(provider_series_count, int):
            if isinstance(coverage_ratio, float):
                print(
                    "approved_mapping_coverage="
                    + f"{approved_count}/{provider_series_count} ({coverage_ratio * 100:.1f}%)"
                )
            else:
                print(f"approved_mapping_coverage={approved_count}/{provider_series_count}")
    if warning_codes:
        print("warnings=" + ", ".join(str(code) for code in warning_codes))
    if isinstance(mapping_review_revision, dict):
        stale_open_count = mapping_review_revision.get("stale_open_count")
        open_count = mapping_review_revision.get("open_count")
        current_revision = mapping_review_revision.get("current_revision")
        if isinstance(stale_open_count, int) and isinstance(open_count, int) and open_count > 0:
            line = f"mapping_review_stale_entries={stale_open_count}/{open_count}"
            if current_revision:
                line += f" revision={current_revision}"
            print(line)
    if isinstance(automation, dict):
        all_units_installed = automation.get("all_units_installed")
        if isinstance(all_units_installed, bool):
            print(f"automation_all_units_installed={all_units_installed}")
        all_units_current = automation.get("all_units_current")
        if isinstance(all_units_current, bool):
            print(f"automation_all_units_current={all_units_current}")
        service_enabled = automation.get("service_enabled")
        if isinstance(service_enabled, bool):
            print(f"automation_service_enabled={service_enabled}")
        service_active = automation.get("service_active")
        if isinstance(service_active, bool):
            print(f"automation_service_active={service_active}")
        missing_units = automation.get("missing_units")
        if isinstance(missing_units, list) and missing_units:
            print("automation_missing_units=" + ", ".join(str(item) for item in missing_units))
        outdated_units = automation.get("outdated_units")
        if isinstance(outdated_units, list) and outdated_units:
            print("automation_outdated_units=" + ", ".join(str(item) for item in outdated_units))
        disabled_services = automation.get("disabled_services")
        if isinstance(disabled_services, list) and disabled_services:
            print("automation_disabled_services=" + ", ".join(str(item) for item in disabled_services))
        inactive_services = automation.get("inactive_services")
        if isinstance(inactive_services, list) and inactive_services:
            print("automation_inactive_services=" + ", ".join(str(item) for item in inactive_services))
        unit_info = automation.get("unit")
        if isinstance(unit_info, dict):
            runtime_state = unit_info.get("runtime_state")
            if isinstance(runtime_state, dict) and runtime_state.get("available") is True:
                parts = [str(automation.get("unit_name") or "mal-updater.service")]
                active_state = runtime_state.get("active_state")
                sub_state = runtime_state.get("sub_state")
                last_trigger_at = runtime_state.get("last_trigger_at")
                if active_state:
                    parts.append(f"active={active_state}")
                if sub_state:
                    parts.append(f"sub={sub_state}")
                if last_trigger_at:
                    parts.append(f"last={last_trigger_at}")
                print("automation_service_runtime=" + " | ".join(parts))
    if install_units_command:
        print("automation_install_command=" + install_units_command)
    top_command = _select_maintenance_command(recommended_commands)
    if isinstance(top_command, dict) and top_command.get("command"):
        print("maintenance_recommended_command=" + str(top_command["command"]))
    top_auto_command = _select_maintenance_command(recommended_commands, require_automation_safe=True)
    if isinstance(top_auto_command, dict) and top_auto_command.get("command"):
        print("maintenance_recommended_auto_command=" + str(top_auto_command["command"]))
    if recommended_next:
        command = recommended_next.get("drilldown_command")
        if command:
            print("recommended_next=" + str(command))
    if recommended_apply_worklist and recommended_apply_worklist.get("command"):
        print("recommended_apply_worklist=" + str(recommended_apply_worklist["command"]))
    if recommended_refresh_worklist and recommended_refresh_worklist.get("command"):
        print("recommended_refresh_worklist=" + str(recommended_refresh_worklist["command"]))
    if recommended_worklist:
        top = recommended_worklist[0]
        if isinstance(top, dict):
            action_command = top.get("action_command")
            if action_command:
                print("recommended_action=" + str(action_command))
            resolve_command = top.get("resolve_command")
            if resolve_command:
                print("recommended_resolve=" + str(resolve_command))



def _cmd_health_check(
    project_root: Path | None,
    stale_hours: float,
    strict: bool,
    review_issue_type: str | None,
    review_worklist_limit: int,
    output_format: str,
    mapping_coverage_threshold: float,
    maintenance_review_limit: int,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    secrets = load_mal_secrets(config)
    crunchyroll_credentials = load_crunchyroll_credentials(config)
    crunchyroll_state = resolve_crunchyroll_state_paths(config)
    hidive_credentials = load_hidive_credentials(config)
    hidive_state = resolve_hidive_state_paths(config)
    snapshot = get_operational_snapshot(config.db_path)

    latest_sync_run = snapshot.get("latest_sync_run")
    latest_completed_sync_run = snapshot.get("latest_completed_sync_run")
    latest_completed_age_seconds = _age_seconds_from_timestamp(
        latest_completed_sync_run.get("completed_at") if isinstance(latest_completed_sync_run, dict) else None
    )
    partial_sync_coverage = _build_partial_sync_coverage(
        latest_sync_run if isinstance(latest_sync_run, dict) else None,
        snapshot.get("provider_counts") if isinstance(snapshot.get("provider_counts"), dict) else None,
    )
    mapping_coverage = _build_mapping_coverage_snapshot(
        snapshot.get("provider_counts") if isinstance(snapshot.get("provider_counts"), dict) else None,
        snapshot.get("mappings") if isinstance(snapshot.get("mappings"), dict) else None,
    )
    automation_installation = _build_automation_installation_status(config.project_root)
    service_state = _load_service_state_for_health(config)
    provider_auth_failures = {
        provider: payload
        for provider in ("crunchyroll", "hidive")
        if (payload := _provider_service_auth_failure(service_state, provider=provider, config=config)) is not None
    }

    warnings: list[dict[str, object]] = []

    if not crunchyroll_credentials.username or not crunchyroll_credentials.password:
        warnings.append({"code": "missing_crunchyroll_credentials", "detail": "Crunchyroll username/password secrets are not both present"})
    if not crunchyroll_state.refresh_token_path.exists() or not crunchyroll_state.device_id_path.exists():
        warnings.append({"code": "missing_crunchyroll_state", "detail": "Crunchyroll refresh token or device id is missing"})
    if hidive_credentials.username or hidive_credentials.password:
        if not (hidive_credentials.username and hidive_credentials.password):
            warnings.append({"code": "missing_hidive_credentials", "detail": "HIDIVE username/password secrets are not both present"})
    if (hidive_credentials.username and hidive_credentials.password) and (
        not hidive_state.access_token_path.exists() or not hidive_state.refresh_token_path.exists()
    ):
        warnings.append({"code": "missing_hidive_state", "detail": "HIDIVE authorisation token or refresh token is missing"})
    if not secrets.client_id or not secrets.access_token or not secrets.refresh_token:
        warnings.append({"code": "missing_mal_auth_material", "detail": "MAL client id/access token/refresh token are not all present"})
    missing_automation_units = automation_installation.get("missing_units") if isinstance(automation_installation, dict) else None
    outdated_automation_units = automation_installation.get("outdated_units") if isinstance(automation_installation, dict) else None
    disabled_automation_services = automation_installation.get("disabled_services") if isinstance(automation_installation, dict) else None
    inactive_automation_services = automation_installation.get("inactive_services") if isinstance(automation_installation, dict) else None
    if isinstance(missing_automation_units, list) and missing_automation_units:
        warnings.append(
            {
                "code": "automation_units_missing",
                "detail": "Repo-owned MAL-Updater user systemd units are not fully installed for this user",
                "missing_units": missing_automation_units,
                "target_dir": automation_installation.get("target_dir"),
            }
        )
    if isinstance(outdated_automation_units, list) and outdated_automation_units:
        warnings.append(
            {
                "code": "automation_units_outdated",
                "detail": "Installed repo-owned MAL-Updater user systemd units do not match the current checked-in repo versions",
                "outdated_units": outdated_automation_units,
                "target_dir": automation_installation.get("target_dir"),
            }
        )
    if isinstance(disabled_automation_services, list) and disabled_automation_services:
        warnings.append(
            {
                "code": "automation_service_disabled",
                "detail": "Repo-owned MAL-Updater user systemd service is installed but not enabled for this user",
                "disabled_services": disabled_automation_services,
            }
        )
    if isinstance(inactive_automation_services, list) and inactive_automation_services:
        warnings.append(
            {
                "code": "automation_service_inactive",
                "detail": "Repo-owned MAL-Updater user systemd service is enabled on disk but is not currently active in the user systemd runtime",
                "inactive_services": inactive_automation_services,
            }
        )
    if not isinstance(latest_completed_sync_run, dict):
        warnings.append({"code": "no_completed_ingest_snapshot", "detail": "No completed sync_runs row exists yet"})
    if isinstance(latest_sync_run, dict) and latest_sync_run.get("status") == "failed":
        warnings.append({"code": "latest_sync_run_failed", "detail": "Latest sync_runs row is failed", "sync_run_id": latest_sync_run.get("id")})
    if latest_completed_age_seconds is not None and latest_completed_age_seconds > stale_hours * 3600:
        warnings.append(
            {
                "code": "completed_snapshot_stale",
                "detail": f"Latest completed ingest snapshot is older than {stale_hours:g} hours",
                "age_seconds": latest_completed_age_seconds,
            }
        )
    if isinstance(partial_sync_coverage, dict):
        warnings.append(
            {
                "code": "latest_sync_run_partial_coverage",
                "detail": "Latest completed ingest touched fewer provider rows than currently exist in the local cache; freshness is only partial until a full refresh runs",
                "sync_run_id": partial_sync_coverage.get("sync_run_id"),
                "fields": partial_sync_coverage.get("fields"),
            }
        )
    for provider, failure in provider_auth_failures.items():
        warning = {
            "code": f"{provider}_auth_failures_repeated",
            "detail": f"Repeated unattended {provider} fetch failures look auth-related and likely need auth re-bootstrap",
            **failure,
        }
        warnings.append(warning)
    coverage_ratio = mapping_coverage.get("approved_coverage_ratio") if isinstance(mapping_coverage, dict) else None
    unmapped_series_count = mapping_coverage.get("unmapped_series_count") if isinstance(mapping_coverage, dict) else None
    if (
        not isinstance(partial_sync_coverage, dict)
        and isinstance(coverage_ratio, float)
        and isinstance(unmapped_series_count, int)
        and unmapped_series_count > 0
        and coverage_ratio < mapping_coverage_threshold
    ):
        warnings.append(
            {
                "code": "approved_mapping_coverage_below_threshold",
                "detail": f"Approved mapping coverage is below the configured {mapping_coverage_threshold * 100:.1f}% threshold",
                "coverage": mapping_coverage,
                "threshold_ratio": round(mapping_coverage_threshold, 4),
            }
        )

    review_queue = snapshot.get("review_queue") if isinstance(snapshot.get("review_queue"), dict) else {}
    open_review_counts = review_queue.get("open") if isinstance(review_queue.get("open"), dict) else {}
    open_review_total = sum(value for value in open_review_counts.values() if isinstance(value, int))
    review_queue_next: dict[str, object] | None = None
    review_queue_worklist: list[dict[str, object]] = []
    review_queue_apply_worklist: dict[str, object] | None = None
    review_queue_refresh_worklist: dict[str, object] | None = None
    mapping_review_items = list_review_queue_entries(
        config.db_path,
        status="open",
        issue_type="mapping_review",
    )
    mapping_review_revision = _build_mapping_review_revision_snapshot(mapping_review_items)
    if isinstance(mapping_review_revision, dict) and mapping_review_revision.get("stale_open_count"):
        warnings.append(
            {
                "code": "mapping_review_queue_stale_heuristics",
                "detail": "Open mapping-review rows were produced by older or unknown mapper heuristics and should be refreshed before manual triage",
                "current_revision": mapping_review_revision.get("current_revision"),
                "stale_open_count": mapping_review_revision.get("stale_open_count"),
                "open_count": mapping_review_revision.get("open_count"),
                "stale_examples": mapping_review_revision.get("stale_examples"),
            }
        )
    if open_review_total > 0:
        warnings.append(
            {
                "code": "open_review_queue",
                "detail": "Open review backlog exists",
                "open_count": open_review_total,
                "by_issue_type": open_review_counts,
            }
        )
        recommendation_items = list_review_queue_entries(
            config.db_path,
            status="open",
            issue_type=review_issue_type,
        )
        provider_series_titles = get_provider_series_title_map(
            config.db_path,
            provider="crunchyroll",
            provider_series_ids=[item.provider_series_id for item in recommendation_items if item.provider_series_id],
        )
        review_queue_summary = _summarize_review_queue(
            recommendation_items,
            status="open",
            issue_type=review_issue_type,
            provider_series_titles=provider_series_titles,
        )
        review_queue_next = _select_review_queue_next_bucket(review_queue_summary, bucket="cluster-strategy")
        if review_queue_next is None:
            for fallback_bucket in ("fix-strategy", "title-cluster", "reason", "decision"):
                review_queue_next = _select_review_queue_next_bucket(review_queue_summary, bucket=fallback_bucket)
                if review_queue_next is not None:
                    break
        review_queue_worklist = _build_review_queue_worklist(
            review_queue_summary,
            bucket_order=["cluster-strategy", "fix-strategy", "title-cluster", "reason", "decision"],
            limit=review_worklist_limit,
        )
        if review_queue_worklist:
            apply_args = _review_queue_apply_worklist_args(
                status="open",
                issue_type=review_issue_type,
                limit=review_worklist_limit,
                per_bucket_limit=20,
            )
            review_queue_apply_worklist = {
                "status_from": "open",
                "status_to": "resolved",
                "bucket_limit": review_worklist_limit,
                "per_bucket_limit": 20,
                "command_args": apply_args,
                "command": _build_review_queue_command(apply_args),
            }
            if review_issue_type != "sync_review":
                refresh_issue_type = review_issue_type if review_issue_type == "mapping_review" else None
                refresh_args = _review_queue_refresh_worklist_args(
                    status="open",
                    issue_type=refresh_issue_type,
                    limit=review_worklist_limit,
                    per_bucket_limit=20,
                    mapping_limit=5,
                )
                review_queue_refresh_worklist = {
                    "status": "open",
                    "issue_type": refresh_issue_type or "mapping_review",
                    "bucket_limit": review_worklist_limit,
                    "per_bucket_limit": 20,
                    "mapping_limit": 5,
                    "command_args": refresh_args,
                    "command": _build_review_queue_command(refresh_args),
                }

    review_queue_refresh_command_args = None
    if isinstance(review_queue_next, dict):
        refresh_args = review_queue_next.get("refresh_args")
        if isinstance(refresh_args, list) and refresh_args:
            review_queue_refresh_command_args = [str(item) for item in refresh_args if item is not None]

    review_queue_refresh_worklist_command_args = None
    if isinstance(review_queue_refresh_worklist, dict):
        refresh_worklist_args = review_queue_refresh_worklist.get("command_args")
        refresh_worklist_provider_series_ids: set[str] = set()
        for item in review_queue_worklist:
            if not isinstance(item, dict):
                continue
            provider_series_ids = item.get("refresh_provider_series_ids")
            if not isinstance(provider_series_ids, list):
                continue
            for provider_series_id in provider_series_ids:
                if isinstance(provider_series_id, str) and provider_series_id.strip():
                    refresh_worklist_provider_series_ids.add(provider_series_id)
        if isinstance(refresh_worklist_args, list) and len(refresh_worklist_provider_series_ids) > 1:
            review_queue_refresh_worklist_command_args = [str(item) for item in refresh_worklist_args if item is not None]

    maintenance_commands = _build_health_maintenance_commands(
        crunchyroll_credentials_present=bool(crunchyroll_credentials.username and crunchyroll_credentials.password),
        crunchyroll_state_present=crunchyroll_state.refresh_token_path.exists() and crunchyroll_state.device_id_path.exists(),
        hidive_credentials_present=bool(hidive_credentials.username and hidive_credentials.password),
        hidive_state_present=hidive_state.access_token_path.exists() and hidive_state.refresh_token_path.exists(),
        mal_client_id_present=bool(secrets.client_id),
        mal_auth_present=bool(secrets.client_id and secrets.access_token and secrets.refresh_token),
        latest_sync_run=latest_sync_run if isinstance(latest_sync_run, dict) else None,
        latest_completed_sync_run=latest_completed_sync_run if isinstance(latest_completed_sync_run, dict) else None,
        latest_completed_age_seconds=latest_completed_age_seconds,
        stale_hours=stale_hours,
        crunchyroll_snapshot_output_path=Path(os.path.relpath(config.cache_dir / "live-crunchyroll-snapshot.json", config.project_root)),
        hidive_snapshot_output_path=Path(os.path.relpath(config.cache_dir / "live-hidive-snapshot.json", config.project_root)),
        partial_sync_coverage=partial_sync_coverage,
        mapping_coverage=mapping_coverage,
        mapping_coverage_threshold=mapping_coverage_threshold,
        maintenance_review_limit=maintenance_review_limit,
        automation_installation=automation_installation,
        review_queue_refresh_command_args=review_queue_refresh_command_args,
        review_queue_refresh_worklist_command_args=review_queue_refresh_worklist_command_args,
        provider_auth_failures=provider_auth_failures,
    )

    payload = {
        "healthy": not warnings,
        "stale_hours_threshold": stale_hours,
        "warnings": warnings,
        "maintenance": {
            "recommended_commands": maintenance_commands,
            "recommended_command": _select_maintenance_command(maintenance_commands),
            "recommended_automation_command": _select_maintenance_command(
                maintenance_commands,
                require_automation_safe=True,
            ),
        },
        "paths": {
            "project_root": str(config.project_root),
            "db_path": str(config.db_path),
            "sync_boundary_path": str(crunchyroll_state.sync_boundary_path),
            "provider_state_roots": {
                "crunchyroll": str(crunchyroll_state.root),
                "hidive": str(hidive_state.root),
            },
            "provider_runtime_paths": {
                "crunchyroll": {
                    "refresh_token_path": str(crunchyroll_state.refresh_token_path),
                    "device_id_path": str(crunchyroll_state.device_id_path),
                    "session_state_path": str(crunchyroll_state.session_state_path),
                    "sync_boundary_path": str(crunchyroll_state.sync_boundary_path),
                },
                "hidive": {
                    "authorisation_token_path": str(hidive_state.access_token_path),
                    "refresh_token_path": str(hidive_state.refresh_token_path),
                    "session_state_path": str(hidive_state.session_state_path),
                },
            },
        },
        "automation": automation_installation,
        "auth": {
            "crunchyroll": {
                "username_present": bool(crunchyroll_credentials.username),
                "password_present": bool(crunchyroll_credentials.password),
                "refresh_token_present": crunchyroll_state.refresh_token_path.exists(),
                "device_id_present": crunchyroll_state.device_id_path.exists(),
                "sync_boundary_present": crunchyroll_state.sync_boundary_path.exists(),
            },
            "hidive": {
                "username_present": bool(hidive_credentials.username),
                "password_present": bool(hidive_credentials.password),
                "authorisation_token_present": hidive_state.access_token_path.exists(),
                "refresh_token_present": hidive_state.refresh_token_path.exists(),
            },
            "mal": {
                "client_id_present": bool(secrets.client_id),
                "access_token_present": bool(secrets.access_token),
                "refresh_token_present": bool(secrets.refresh_token),
            },
        },
        "latest_sync_run": latest_sync_run,
        "latest_completed_sync_run": latest_completed_sync_run,
        "latest_completed_sync_run_age_seconds": latest_completed_age_seconds,
        "provider_counts": snapshot.get("provider_counts"),
        "provider_freshness": snapshot.get("provider_freshness"),
        "partial_sync_coverage": partial_sync_coverage,
        "review_queue": {
            **review_queue,
            "mapping_review_revision": mapping_review_revision,
            "recommendation_issue_type_filter": review_issue_type,
            "recommendation_worklist_limit": review_worklist_limit,
            "recommended_next": review_queue_next,
            "recommended_worklist": review_queue_worklist,
            "recommended_apply_worklist": review_queue_apply_worklist,
            "recommended_refresh_worklist": review_queue_refresh_worklist,
        },
        "mappings": {
            **(snapshot.get("mappings") if isinstance(snapshot.get("mappings"), dict) else {}),
            "coverage": mapping_coverage,
            "coverage_threshold": round(mapping_coverage_threshold, 4),
        },
    }
    if output_format == "summary":
        _emit_health_check_summary(payload)
    else:
        print(json.dumps(payload, indent=2))
    if strict and warnings:
        return 2
    return 0



def _cmd_mal_auth_url(project_root: Path | None, emit_json: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    client = MalClient(config, load_mal_secrets(config))
    pkce = client.generate_pkce_pair()
    try:
        auth_url = client.build_authorization_url(code_challenge=pkce.code_challenge)
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if emit_json:
        print(
            json.dumps(
                {
                    "authorization_url": auth_url,
                    "redirect_uri": config.mal.redirect_uri,
                    "code_verifier": pkce.code_verifier,
                    "code_challenge": pkce.code_challenge,
                },
                indent=2,
            )
        )
        return 0
    print("Open this URL in a browser after writing down the code verifier:")
    print(auth_url)
    print()
    print("code_verifier=")
    print(pkce.code_verifier)
    print()
    print(f"redirect_uri={config.mal.redirect_uri}")
    return 0


def _cmd_mal_auth_login(project_root: Path | None, timeout_seconds: float, verify_whoami: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    secrets = load_mal_secrets(config)
    client = MalClient(config, secrets)
    pkce = client.generate_pkce_pair()
    state = client.generate_state()
    try:
        auth_url = client.build_authorization_url(code_challenge=pkce.code_challenge, state=state)
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(format_auth_flow_prompt(config, auth_url, timeout_seconds))
    try:
        callback = wait_for_oauth_callback(
            config.mal.bind_host,
            config.mal.redirect_port,
            expected_state=state,
            timeout_seconds=timeout_seconds,
        )
        token = client.exchange_code(callback.code, pkce.code_verifier)
        persisted = persist_token_response(token, secrets)
    except OSError as exc:
        print(f"Unable to start MAL callback listener on {config.mal.redirect_uri}: {exc}", file=sys.stderr)
        return 1
    except TimeoutError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except (OAuthCallbackError, MalApiError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print()
    print(f"Persisted access token to {persisted.access_token_path}")
    if token.refresh_token:
        print(f"Persisted refresh token to {persisted.refresh_token_path}")
    else:
        print("No refresh token returned by MAL; existing refresh token file left untouched")

    if not verify_whoami:
        return 0

    try:
        whoami = client.get_my_user(access_token=token.access_token)
    except MalApiError as exc:
        print(f"Token exchange succeeded, but /users/@me verification failed: {exc}", file=sys.stderr)
        return 1

    print(f"Authenticated MAL user: {json.dumps(whoami, indent=2)}")
    return 0


def _cmd_mal_refresh(project_root: Path | None, verify_whoami: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    secrets = load_mal_secrets(config)
    client = MalClient(config, secrets)
    try:
        token = client.refresh_access_token()
        persisted = persist_token_response(token, secrets)
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Persisted access token to {persisted.access_token_path}")
    if token.refresh_token:
        print(f"Persisted refresh token to {persisted.refresh_token_path}")

    if not verify_whoami:
        return 0

    try:
        whoami = client.get_my_user(access_token=token.access_token)
    except MalApiError as exc:
        print(f"Refresh succeeded, but /users/@me verification failed: {exc}", file=sys.stderr)
        return 1

    print(f"Authenticated MAL user: {json.dumps(whoami, indent=2)}")
    return 0


def _cmd_mal_whoami(project_root: Path | None) -> int:
    config = load_config(project_root)
    secrets = load_mal_secrets(config)
    client = MalClient(config, secrets)
    try:
        whoami = client.get_my_user()
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(whoami, indent=2))
    return 0


def _cmd_provider_auth_login(project_root: Path | None, provider_slug: str, profile: str, no_verify: bool) -> int:
    if provider_slug == "crunchyroll":
        return _cmd_crunchyroll_auth_login(project_root, profile, no_verify)
    if provider_slug == "hidive":
        from .hidive_auth import HidiveAuthError, hidive_login_with_credentials

        config = load_config(project_root)
        ensure_directories(config)
        try:
            result = hidive_login_with_credentials(
                config,
                profile=profile,
                verify_account=not no_verify,
            )
        except HidiveAuthError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        print(f"Staged HIDIVE authorisation token to {result.access_token_path}")
        print(f"Staged HIDIVE refresh token to {result.refresh_token_path}")
        print(f"Updated session state at {result.session_state_path}")
        if result.account_id:
            print(f"HIDIVE account_id={result.account_id}")
        if result.account_name:
            print(f"HIDIVE account_name={result.account_name}")
        print(f"profile={result.profile}")
        return 0
    print(f"provider-auth-login is not implemented yet for provider '{provider_slug}'", file=sys.stderr)
    return 2



def _cmd_crunchyroll_auth_login(project_root: Path | None, profile: str, no_verify: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    try:
        result = crunchyroll_login_with_credentials(
            config,
            profile=profile,
            verify_account=not no_verify,
        )
    except CrunchyrollAuthError as exc:
        print(str(exc), file=sys.stderr)
        return 1

    print(f"Staged Crunchyroll refresh token to {result.refresh_token_path}")
    print(f"Staged Crunchyroll device id to {result.device_id_path}")
    print(f"Updated session state at {result.session_state_path}")
    if result.account_id:
        print(f"Crunchyroll account_id={result.account_id}")
    if result.account_email:
        print(f"Crunchyroll account_email={result.account_email}")
    print(f"profile={result.profile}")
    print(f"locale={result.locale}")
    print(f"device_type={result.device_type}")
    return 0


def _cmd_validate_snapshot(project_root: Path | None, snapshot_path: Path | None) -> int:
    load_config(project_root)
    if snapshot_path is None:
        payload = json.load(sys.stdin)
        source = "stdin"
    else:
        payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
        source = str(snapshot_path)
    try:
        validate_snapshot_payload(payload)
    except SnapshotValidationError as exc:
        print(f"INVALID: {exc}", file=sys.stderr)
        return 1
    print(f"VALID: {source}")
    return 0


def _cmd_provider_fetch_snapshot(
    project_root: Path | None,
    provider_slug: str,
    profile: str,
    out_path: Path | None,
    ingest: bool,
    full_refresh: bool,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    provider = get_provider(provider_slug)
    try:
        result = provider.fetch_snapshot(
            config,
            profile=profile,
            full_refresh=full_refresh,
        )
    except (CrunchyrollAuthError, CrunchyrollSnapshotError) as exc:
        print(str(exc), file=sys.stderr)
        return 1

    payload = snapshot_to_dict(result.snapshot)
    target_path = out_path
    if target_path is not None:
        provider.write_snapshot_file(target_path, result.snapshot)
        print(f"Wrote {provider.display_name} snapshot to {target_path}")

    if ingest:
        summary = ingest_snapshot_payload(payload, config)
        print(json.dumps(summary.as_dict(), indent=2))
        return 0

    print(json.dumps(payload, indent=2))
    return 0



def _cmd_crunchyroll_fetch_snapshot(
    project_root: Path | None,
    profile: str,
    out_path: Path | None,
    ingest: bool,
    full_refresh: bool,
) -> int:
    return _cmd_provider_fetch_snapshot(
        project_root,
        "crunchyroll",
        profile,
        out_path,
        ingest,
        full_refresh,
    )


def _cmd_ingest_snapshot(project_root: Path | None, snapshot_path: Path | None) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    if snapshot_path is None:
        payload = json.load(sys.stdin)
        summary = ingest_snapshot_payload(payload, config)
    else:
        summary = ingest_snapshot_file(snapshot_path, config)
    print(json.dumps(summary.as_dict(), indent=2))
    return 0


def _cmd_map_series(project_root: Path | None, limit: int, mapping_limit: int) -> int:
    config = load_config(project_root)
    states = load_provider_series_states(config, limit=limit)
    client = MalClient(config, load_mal_secrets(config))
    results = []
    for state in states:
        try:
            mapping = map_series(
                client,
                SeriesMappingInput(
                    provider=state.provider,
                    provider_series_id=state.provider_series_id,
                    title=state.title,
                    season_title=state.season_title,
                    season_number=state.season_number,
                    max_episode_number=state.max_episode_number,
                    completed_episode_count=state.completed_episode_count,
                    max_completed_episode_number=state.max_completed_episode_number,
                ),
                limit=mapping_limit,
            )
        except MalApiError as exc:
            print(str(exc), file=sys.stderr)
            return 1
        results.append(
            {
                "provider_series_id": state.provider_series_id,
                "title": state.title,
                "season_title": state.season_title,
                "mapping_status": mapping.status,
                "confidence": mapping.confidence,
                "rationale": mapping.rationale,
                "chosen_candidate": None
                if not mapping.chosen_candidate
                else {
                    "mal_anime_id": mapping.chosen_candidate.mal_anime_id,
                    "title": mapping.chosen_candidate.title,
                    "score": mapping.chosen_candidate.score,
                    "matched_query": mapping.chosen_candidate.matched_query,
                    "match_reasons": mapping.chosen_candidate.match_reasons,
                },
                "bundle_companion_candidate": None
                if not mapping.bundle_companion_candidate
                else {
                    "mal_anime_id": mapping.bundle_companion_candidate.mal_anime_id,
                    "title": mapping.bundle_companion_candidate.title,
                    "score": mapping.bundle_companion_candidate.score,
                    "matched_query": mapping.bundle_companion_candidate.matched_query,
                    "match_reasons": mapping.bundle_companion_candidate.match_reasons,
                    "media_type": mapping.bundle_companion_candidate.media_type,
                    "num_episodes": mapping.bundle_companion_candidate.num_episodes,
                },
                "bundle_companion_candidates": [
                    {
                        "mal_anime_id": candidate.mal_anime_id,
                        "title": candidate.title,
                        "score": candidate.score,
                        "matched_query": candidate.matched_query,
                        "match_reasons": candidate.match_reasons,
                        "media_type": candidate.media_type,
                        "num_episodes": candidate.num_episodes,
                    }
                    for candidate in (mapping.bundle_companion_candidates or [])
                ],
                "candidates": [
                    {
                        "mal_anime_id": candidate.mal_anime_id,
                        "title": candidate.title,
                        "score": candidate.score,
                        "matched_query": candidate.matched_query,
                        "media_type": candidate.media_type,
                    }
                    for candidate in mapping.candidates
                ],
            }
        )
    print(json.dumps(results, indent=2))
    return 0


def _normalize_limit(limit: int) -> int | None:
    return None if limit <= 0 else limit


def _cmd_review_mappings(project_root: Path | None, limit: int, mapping_limit: int, persist_queue: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    normalized_limit = _normalize_limit(limit)
    if persist_queue and normalized_limit is not None:
        print("--persist-review-queue requires a full scan; rerun with --limit 0", file=sys.stderr)
        return 2
    try:
        items = build_mapping_review(config, limit=normalized_limit, mapping_limit=mapping_limit)
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    payload: dict[str, object] = {"items": [item.as_dict() for item in items]}
    if persist_queue:
        payload["review_queue"] = persist_mapping_review_queue(config, items)
    print(json.dumps(payload, indent=2))
    return 0



def _refresh_mapping_review_queue_for_provider_series_ids(
    config: object,
    provider_series_ids: list[str],
    mapping_limit: int,
) -> dict[str, object]:
    normalized_provider_series_ids = sorted({value.strip() for value in provider_series_ids if isinstance(value, str) and value.strip()})
    items = build_mapping_review(
        config,
        limit=None,
        mapping_limit=mapping_limit,
        provider_series_ids=normalized_provider_series_ids,
    )
    queue_entries = []
    for item in items:
        if item.decision in {"preserved", "auto_approved", "ready_for_approval"}:
            continue
        severity = "error" if item.decision == "needs_manual_match" else "warning"
        queue_entries.append(
            {
                "provider": item.provider,
                "provider_series_id": item.provider_series_id,
                "severity": severity,
                "payload": item.as_dict(),
            }
        )
    review_queue_result = refresh_review_queue_entries(
        config.db_path,
        issue_type="mapping_review",
        provider_series_ids=normalized_provider_series_ids,
        entries=queue_entries,
    )
    return {
        "provider_series_ids": normalized_provider_series_ids,
        "items": [item.as_dict() for item in items],
        "review_queue": review_queue_result,
    }



def _resolve_refresh_mapping_review_queue_provider_series_ids(
    config: object,
    provider_series_ids: list[str],
    *,
    include_all_open: bool,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> list[str]:
    normalized_provider_series_ids = {
        value.strip() for value in provider_series_ids if isinstance(value, str) and value.strip()
    }
    if include_all_open or any(
        value is not None
        for value in (
            title_cluster,
            fix_strategy,
            cluster_strategy,
            decision,
            reason,
            reason_family,
            fix_strategy_family,
            cluster_strategy_family,
        )
    ):
        open_rows = list_review_queue_entries(config.db_path, status="open", issue_type="mapping_review")
        provider_series_titles = get_provider_series_title_map(
            config.db_path,
            provider="crunchyroll",
            provider_series_ids=[item.provider_series_id for item in open_rows if item.provider_series_id],
        )
        filtered_open_rows = _filter_review_queue_items(
            open_rows,
            provider_series_titles=provider_series_titles,
            title_cluster=title_cluster,
            fix_strategy=fix_strategy,
            cluster_strategy=cluster_strategy,
            decision=decision,
            reason=reason,
            reason_family=reason_family,
            fix_strategy_family=fix_strategy_family,
            cluster_strategy_family=cluster_strategy_family,
        )
        normalized_provider_series_ids.update(
            str(item.provider_series_id).strip()
            for item in filtered_open_rows
            if isinstance(item.provider_series_id, str) and item.provider_series_id.strip()
        )
    return sorted(normalized_provider_series_ids)



def _cmd_refresh_mapping_review_queue(
    project_root: Path | None,
    provider_series_ids: list[str],
    mapping_limit: int,
    include_all_open: bool = False,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    normalized_provider_series_ids = _resolve_refresh_mapping_review_queue_provider_series_ids(
        config,
        provider_series_ids,
        include_all_open=include_all_open,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    if not normalized_provider_series_ids:
        print(
            "--provider-series-id is required at least once (or use --all-open or a queue-slice filter)",
            file=sys.stderr,
        )
        return 2
    try:
        payload = _refresh_mapping_review_queue_for_provider_series_ids(
            config,
            normalized_provider_series_ids,
            mapping_limit,
        )
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_list_mappings(project_root: Path | None, approved_only: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    items = list_series_mappings(config.db_path, provider="crunchyroll", approved_only=approved_only)
    print(
        json.dumps(
            [
                {
                    "provider": item.provider,
                    "provider_series_id": item.provider_series_id,
                    "mal_anime_id": item.mal_anime_id,
                    "confidence": item.confidence,
                    "mapping_source": item.mapping_source,
                    "approved_by_user": item.approved_by_user,
                    "notes": item.notes,
                    "created_at": item.created_at,
                    "updated_at": item.updated_at,
                }
                for item in items
            ],
            indent=2,
        )
    )
    return 0


def _cmd_approve_mapping(
    project_root: Path | None,
    provider_series_id: str,
    mal_anime_id: int,
    confidence: float | None,
    notes: str | None,
    exact: bool,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    mapping = upsert_series_mapping(
        config.db_path,
        provider="crunchyroll",
        provider_series_id=provider_series_id,
        mal_anime_id=mal_anime_id,
        confidence=confidence,
        mapping_source="user_exact" if exact else "user_approved",
        approved_by_user=True,
        notes=notes,
    )
    print(
        json.dumps(
            {
                "provider": mapping.provider,
                "provider_series_id": mapping.provider_series_id,
                "mal_anime_id": mapping.mal_anime_id,
                "confidence": mapping.confidence,
                "mapping_source": mapping.mapping_source,
                "approved_by_user": mapping.approved_by_user,
                "notes": mapping.notes,
                "created_at": mapping.created_at,
                "updated_at": mapping.updated_at,
            },
            indent=2,
        )
    )
    return 0


def _cmd_dry_run_sync(
    project_root: Path | None,
    provider: str = "crunchyroll",
    limit: int = 20,
    mapping_limit: int = 5,
    approved_mappings_only: bool = False,
    exact_approved_only: bool = False,
    persist_queue: bool = False,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    normalized_limit = _normalize_limit(limit)
    if persist_queue and normalized_limit is not None:
        print("--persist-review-queue requires a full scan; rerun with --limit 0", file=sys.stderr)
        return 2
    try:
        proposals = build_dry_run_sync_plan(
            config,
            limit=normalized_limit,
            mapping_limit=mapping_limit,
            approved_mappings_only=approved_mappings_only,
            exact_approved_only=exact_approved_only,
            provider=None if provider == "all" else provider,
        )
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    payload: dict[str, object] = {"proposals": [proposal.as_dict() for proposal in proposals]}
    if persist_queue:
        payload["review_queue"] = persist_sync_review_queue(config, proposals)
    print(json.dumps(payload, indent=2))
    return 0


def _review_queue_item_label(
    item: object,
    *,
    provider_series_titles: dict[str, dict[str, str | None]] | None = None,
) -> dict[str, object]:
    payload = getattr(item, "payload", None)
    title = None
    if isinstance(payload, dict):
        for key in ("title", "provider_title", "crunchyroll_title", "season_title", "mal_title", "suggested_mal_title"):
            value = payload.get(key)
            if isinstance(value, str) and value.strip():
                title = value.strip()
                break
    provider_series_id = getattr(item, "provider_series_id", None)
    series_row = provider_series_titles.get(provider_series_id) if provider_series_titles and isinstance(provider_series_id, str) else None
    if title is None and isinstance(series_row, dict):
        for key in ("season_title", "title"):
            value = series_row.get(key)
            if isinstance(value, str) and value.strip():
                title = value.strip()
                break
    return {
        "provider_series_id": provider_series_id,
        "issue_type": getattr(item, "issue_type", None),
        "severity": getattr(item, "severity", None),
        "title": title,
        "created_at": getattr(item, "created_at", None),
    }



_TRAILING_INSTALLMENT_CLUSTER_RE = re.compile(
    r"(?:\b(?:season|part|cour)\s*\d+\b|\b\d+(?:st|nd|rd|th)\s+season\b|\b(?:final|last)\s+season\b|\b(?:part|cour)\s+[ivx]+\b|\b[ivx]+\b)$",
    re.IGNORECASE,
)


def _review_queue_title_cluster_key(title: str | None) -> str | None:
    if not isinstance(title, str) or not title.strip():
        return None
    value = title.strip()
    previous = None
    while previous != value:
        previous = value
        value = _TRAILING_INSTALLMENT_CLUSTER_RE.sub("", value).strip(" -:()[]")
    normalized = normalize_title(value)
    return normalized or None


def _review_queue_reason_family(reason: str | None) -> str | None:
    if not isinstance(reason, str) or not reason.strip():
        return None
    normalized_reason = reason.strip()
    if "=" in normalized_reason:
        return normalized_reason.split("=", 1)[0].strip() or normalized_reason
    return normalized_reason


def _review_queue_fix_strategy_key(payload: dict[str, object], *, canonicalize_reasons: bool = False) -> str | None:
    decision = payload.get("decision")
    if not isinstance(decision, str) or not decision.strip():
        return None
    parts = [decision.strip()]
    reasons = payload.get("reasons")
    normalized_reasons: list[str] = []
    if isinstance(reasons, list):
        normalized_reason_values: set[str] = set()
        for reason in reasons:
            if not isinstance(reason, str) or not reason.strip():
                continue
            normalized_reason = reason.strip()
            if canonicalize_reasons:
                normalized_reason = _review_queue_reason_family(normalized_reason) or normalized_reason
            normalized_reason_values.add(normalized_reason)
        normalized_reasons = sorted(normalized_reason_values)
    parts.extend(normalized_reasons)
    return " | ".join(parts)


def _review_queue_cluster_strategy_key(
    title: str | None,
    payload: dict[str, object],
    *,
    canonicalize_reasons: bool = False,
) -> dict[str, str] | None:
    cluster = _review_queue_title_cluster_key(title)
    strategy = _review_queue_fix_strategy_key(payload, canonicalize_reasons=canonicalize_reasons)
    if cluster is None or strategy is None:
        return None
    return {
        "cluster": cluster,
        "strategy": strategy,
        "key": f"{cluster} || {strategy}",
    }


def _review_queue_command_args(
    command: str,
    *,
    status: str,
    issue_type: str | None,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
    limit: int | None = None,
) -> list[str]:
    args: list[str] = [command]
    status_value = status if command == "list-review-queue" and status != "open" else None
    option_pairs = [
        ("--status", status_value),
        ("--issue-type", issue_type),
        ("--title-cluster", title_cluster),
        ("--fix-strategy", fix_strategy),
        ("--cluster-strategy", cluster_strategy),
        ("--decision", decision),
        ("--reason", reason),
        ("--reason-family", reason_family),
        ("--fix-strategy-family", fix_strategy_family),
        ("--cluster-strategy-family", cluster_strategy_family),
    ]
    seen_pairs: set[tuple[str, str]] = set()
    for flag, value in option_pairs:
        if not isinstance(value, str):
            continue
        normalized_value = value.strip()
        if not normalized_value:
            continue
        pair = (flag, normalized_value)
        if pair in seen_pairs:
            continue
        args.extend([flag, normalized_value])
        seen_pairs.add(pair)
    if command == "resolve-review-queue" and isinstance(limit, int):
        args.extend(["--limit", str(limit)])
    return args


def _review_queue_drilldown_args(
    *,
    status: str,
    issue_type: str | None,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> list[str]:
    return _review_queue_command_args(
        "list-review-queue",
        status=status,
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )


def _review_queue_status_action_command(status: str) -> str:
    return "reopen-review-queue" if status == "resolved" else "resolve-review-queue"



def _review_queue_status_action_args(
    *,
    status: str,
    issue_type: str | None,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
    limit: int = 20,
) -> list[str]:
    command = _review_queue_status_action_command(status)
    return _review_queue_command_args(
        command,
        status="resolved" if command == "reopen-review-queue" else "open",
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
        limit=limit if command == "resolve-review-queue" else None,
    )



def _review_queue_resolve_args(
    *,
    issue_type: str | None,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
    limit: int = 20,
) -> list[str]:
    return _review_queue_status_action_args(
        status="open",
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
        limit=limit,
    )



def _review_queue_status_action_fields(status: str, args: list[str]) -> dict[str, object]:
    command = _review_queue_status_action_command(status)
    action = "reopen" if command == "reopen-review-queue" else "resolve"
    payload: dict[str, object] = {
        "action": action,
        "action_args": args,
        "action_command": _build_review_queue_command(args),
    }
    if action == "resolve":
        payload["resolve_args"] = args
        payload["resolve_command"] = payload["action_command"]
    else:
        payload["reopen_args"] = args
        payload["reopen_command"] = payload["action_command"]
    return payload



def _review_queue_refresh_args(
    *,
    issue_type: str | None,
    provider_series_ids: list[str],
    mapping_limit: int = 5,
) -> list[str] | None:
    if issue_type != "mapping_review":
        return None
    normalized_ids = sorted(
        {
            value.strip()
            for value in provider_series_ids
            if isinstance(value, str) and value.strip()
        }
    )
    if not normalized_ids:
        return None
    args = ["refresh-mapping-review-queue"]
    for provider_series_id in normalized_ids:
        args.extend(["--provider-series-id", provider_series_id])
    if mapping_limit != 5:
        args.extend(["--mapping-limit", str(mapping_limit)])
    return args



def _review_queue_refresh_fields(
    *,
    issue_type: str | None,
    provider_series_ids: list[str],
    mapping_limit: int = 5,
) -> dict[str, object]:
    args = _review_queue_refresh_args(
        issue_type=issue_type,
        provider_series_ids=provider_series_ids,
        mapping_limit=mapping_limit,
    )
    if args is None:
        return {}
    return {
        "refresh_provider_series_ids": provider_series_ids,
        "refresh_args": args,
        "refresh_command": _build_review_queue_command(args),
    }



def _review_queue_apply_worklist_args(
    *,
    status: str,
    issue_type: str | None,
    limit: int,
    per_bucket_limit: int,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> list[str]:
    args = _review_queue_command_args(
        "review-queue-apply-worklist",
        status=status,
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    args.extend(["--limit", str(limit), "--per-bucket-limit", str(per_bucket_limit)])
    return args



def _review_queue_refresh_worklist_args(
    *,
    status: str,
    issue_type: str | None,
    limit: int,
    per_bucket_limit: int,
    mapping_limit: int,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> list[str]:
    args = _review_queue_command_args(
        "review-queue-refresh-worklist",
        status=status,
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    args.extend(["--limit", str(limit), "--per-bucket-limit", str(per_bucket_limit), "--mapping-limit", str(mapping_limit)])
    return args


def _filter_review_queue_items(
    items: list[object],
    *,
    provider_series_titles: dict[str, dict[str, str | None]] | None = None,
    title_cluster: str | None = None,
    fix_strategy: str | None = None,
    cluster_strategy: str | None = None,
    decision: str | None = None,
    reason: str | None = None,
    reason_family: str | None = None,
    fix_strategy_family: str | None = None,
    cluster_strategy_family: str | None = None,
) -> list[object]:
    normalized_title_cluster = _review_queue_title_cluster_key(title_cluster) if title_cluster else None
    normalized_fix_strategy = fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None
    normalized_cluster_strategy = cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None
    normalized_decision = decision.strip() if isinstance(decision, str) and decision.strip() else None
    normalized_reason = reason.strip() if isinstance(reason, str) and reason.strip() else None
    normalized_reason_family = _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None
    normalized_fix_strategy_family = fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None
    normalized_cluster_strategy_family = cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None
    if (
        normalized_title_cluster is None
        and normalized_fix_strategy is None
        and normalized_cluster_strategy is None
        and normalized_decision is None
        and normalized_reason is None
        and normalized_reason_family is None
        and normalized_fix_strategy_family is None
        and normalized_cluster_strategy_family is None
    ):
        return items
    filtered: list[object] = []
    for item in items:
        payload = getattr(item, "payload", None)
        if not isinstance(payload, dict):
            continue
        label = _review_queue_item_label(item, provider_series_titles=provider_series_titles)
        if normalized_title_cluster is not None:
            if _review_queue_title_cluster_key(label.get("title")) != normalized_title_cluster:
                continue
        if normalized_fix_strategy is not None and _review_queue_fix_strategy_key(payload) != normalized_fix_strategy:
            continue
        if normalized_cluster_strategy is not None:
            cluster_strategy_parts = _review_queue_cluster_strategy_key(label.get("title"), payload)
            if cluster_strategy_parts is None or cluster_strategy_parts["key"] != normalized_cluster_strategy:
                continue
        if normalized_decision is not None:
            payload_decision = payload.get("decision")
            if not isinstance(payload_decision, str) or payload_decision.strip() != normalized_decision:
                continue
        if normalized_reason is not None or normalized_reason_family is not None:
            reasons = payload.get("reasons")
            normalized_reasons = {
                item_reason.strip() for item_reason in reasons if isinstance(item_reason, str) and item_reason.strip()
            } if isinstance(reasons, list) else set()
            if normalized_reason is not None and normalized_reason not in normalized_reasons:
                continue
            if normalized_reason_family is not None:
                normalized_reason_families = {_review_queue_reason_family(item_reason) for item_reason in normalized_reasons}
                normalized_reason_families.discard(None)
                if normalized_reason_family not in normalized_reason_families:
                    continue
        if normalized_fix_strategy_family is not None:
            if _review_queue_fix_strategy_key(payload, canonicalize_reasons=True) != normalized_fix_strategy_family:
                continue
        if normalized_cluster_strategy_family is not None:
            cluster_strategy_family_parts = _review_queue_cluster_strategy_key(
                label.get("title"),
                payload,
                canonicalize_reasons=True,
            )
            if cluster_strategy_family_parts is None or cluster_strategy_family_parts["key"] != normalized_cluster_strategy_family:
                continue
        filtered.append(item)
    return filtered


def _summarize_review_queue(
    items: list[object],
    *,
    status: str,
    issue_type: str | None,
    provider_series_titles: dict[str, dict[str, str | None]] | None = None,
    title_cluster_filter: str | None = None,
    fix_strategy_filter: str | None = None,
    cluster_strategy_filter: str | None = None,
    decision_filter: str | None = None,
    reason_filter: str | None = None,
    reason_family_filter: str | None = None,
    fix_strategy_family_filter: str | None = None,
    cluster_strategy_family_filter: str | None = None,
) -> dict[str, object]:
    by_issue_type = Counter(getattr(item, "issue_type", None) for item in items)
    by_severity = Counter(getattr(item, "severity", None) for item in items)
    by_decision: Counter[str] = Counter()
    by_reason: Counter[str] = Counter()
    by_reason_family: Counter[str] = Counter()
    by_title_cluster: Counter[str] = Counter()
    by_fix_strategy: Counter[str] = Counter()
    by_fix_strategy_family: Counter[str] = Counter()
    by_cluster_strategy: Counter[str] = Counter()
    by_cluster_strategy_family: Counter[str] = Counter()
    decision_examples: dict[str, list[dict[str, object]]] = {}
    reason_examples: dict[str, list[dict[str, object]]] = {}
    reason_family_examples: dict[str, list[dict[str, object]]] = {}
    title_cluster_examples: dict[str, list[dict[str, object]]] = {}
    title_cluster_labels: dict[str, str] = {}
    fix_strategy_examples: dict[str, list[dict[str, object]]] = {}
    fix_strategy_family_examples: dict[str, list[dict[str, object]]] = {}
    cluster_strategy_examples: dict[str, list[dict[str, object]]] = {}
    cluster_strategy_family_examples: dict[str, list[dict[str, object]]] = {}
    cluster_strategy_parts: dict[str, dict[str, str]] = {}
    cluster_strategy_family_parts: dict[str, dict[str, str]] = {}
    decision_provider_series_ids: dict[str, list[str]] = {}
    reason_provider_series_ids: dict[str, list[str]] = {}
    reason_family_provider_series_ids: dict[str, list[str]] = {}
    title_cluster_provider_series_ids: dict[str, list[str]] = {}
    fix_strategy_provider_series_ids: dict[str, list[str]] = {}
    fix_strategy_family_provider_series_ids: dict[str, list[str]] = {}
    cluster_strategy_provider_series_ids: dict[str, list[str]] = {}
    cluster_strategy_family_provider_series_ids: dict[str, list[str]] = {}

    def add_provider_series_id(target: dict[str, list[str]], key: str, provider_series_id: str | None) -> None:
        if not isinstance(provider_series_id, str) or not provider_series_id.strip():
            return
        values = target.setdefault(key, [])
        normalized_id = provider_series_id.strip()
        if normalized_id in values or len(values) >= 20:
            return
        values.append(normalized_id)

    for item in items:
        payload = getattr(item, "payload", None)
        if not isinstance(payload, dict):
            continue
        label = _review_queue_item_label(item, provider_series_titles=provider_series_titles)
        provider_series_id = getattr(item, "provider_series_id", None)
        decision = payload.get("decision")
        if isinstance(decision, str) and decision.strip():
            normalized_decision = decision.strip()
            by_decision[normalized_decision] += 1
            examples = decision_examples.setdefault(normalized_decision, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(decision_provider_series_ids, normalized_decision, provider_series_id)
        title_cluster_key = _review_queue_title_cluster_key(label.get("title"))
        if title_cluster_key is not None:
            by_title_cluster[title_cluster_key] += 1
            title_cluster_labels.setdefault(title_cluster_key, str(label.get("title") or title_cluster_key))
            examples = title_cluster_examples.setdefault(title_cluster_key, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(title_cluster_provider_series_ids, title_cluster_key, provider_series_id)
        fix_strategy_key = _review_queue_fix_strategy_key(payload)
        if fix_strategy_key is not None:
            by_fix_strategy[fix_strategy_key] += 1
            examples = fix_strategy_examples.setdefault(fix_strategy_key, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(fix_strategy_provider_series_ids, fix_strategy_key, provider_series_id)
        fix_strategy_family_key = _review_queue_fix_strategy_key(payload, canonicalize_reasons=True)
        if fix_strategy_family_key is not None:
            by_fix_strategy_family[fix_strategy_family_key] += 1
            examples = fix_strategy_family_examples.setdefault(fix_strategy_family_key, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(fix_strategy_family_provider_series_ids, fix_strategy_family_key, provider_series_id)
        cluster_strategy = _review_queue_cluster_strategy_key(label.get("title"), payload)
        if cluster_strategy is not None:
            cluster_strategy_key = cluster_strategy["key"]
            by_cluster_strategy[cluster_strategy_key] += 1
            cluster_strategy_parts.setdefault(cluster_strategy_key, cluster_strategy)
            examples = cluster_strategy_examples.setdefault(cluster_strategy_key, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(cluster_strategy_provider_series_ids, cluster_strategy_key, provider_series_id)
        cluster_strategy_family = _review_queue_cluster_strategy_key(
            label.get("title"),
            payload,
            canonicalize_reasons=True,
        )
        if cluster_strategy_family is not None:
            cluster_strategy_family_key = cluster_strategy_family["key"]
            by_cluster_strategy_family[cluster_strategy_family_key] += 1
            cluster_strategy_family_parts.setdefault(cluster_strategy_family_key, cluster_strategy_family)
            examples = cluster_strategy_family_examples.setdefault(cluster_strategy_family_key, [])
            if len(examples) < 3:
                examples.append(label)
            add_provider_series_id(cluster_strategy_family_provider_series_ids, cluster_strategy_family_key, provider_series_id)
        reasons = payload.get("reasons")
        if isinstance(reasons, list):
            for reason in reasons:
                if not isinstance(reason, str) or not reason.strip():
                    continue
                normalized_reason = reason.strip()
                by_reason[normalized_reason] += 1
                examples = reason_examples.setdefault(normalized_reason, [])
                if len(examples) < 3:
                    examples.append(label)
                add_provider_series_id(reason_provider_series_ids, normalized_reason, provider_series_id)
                reason_family = _review_queue_reason_family(normalized_reason)
                if reason_family is None:
                    continue
                by_reason_family[reason_family] += 1
                family_examples = reason_family_examples.setdefault(reason_family, [])
                if len(family_examples) < 3:
                    family_examples.append(label)
                add_provider_series_id(reason_family_provider_series_ids, reason_family, provider_series_id)

    effective_refresh_issue_type = issue_type
    visible_issue_types = {key for key, value in by_issue_type.items() if key and value}
    if effective_refresh_issue_type is None and visible_issue_types == {"mapping_review"}:
        effective_refresh_issue_type = "mapping_review"

    return {
        "status": status,
        "issue_type_filter": issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster_filter) if title_cluster_filter else None,
        "fix_strategy_filter": fix_strategy_filter.strip() if isinstance(fix_strategy_filter, str) and fix_strategy_filter.strip() else None,
        "cluster_strategy_filter": cluster_strategy_filter.strip() if isinstance(cluster_strategy_filter, str) and cluster_strategy_filter.strip() else None,
        "decision_filter": decision_filter.strip() if isinstance(decision_filter, str) and decision_filter.strip() else None,
        "reason_filter": reason_filter.strip() if isinstance(reason_filter, str) and reason_filter.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family_filter) if isinstance(reason_family_filter, str) and reason_family_filter.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family_filter.strip() if isinstance(fix_strategy_family_filter, str) and fix_strategy_family_filter.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family_filter.strip() if isinstance(cluster_strategy_family_filter, str) and cluster_strategy_family_filter.strip() else None,
        "count": len(items),
        "by_issue_type": dict(sorted((key, value) for key, value in by_issue_type.items() if key)),
        "by_severity": dict(sorted((key, value) for key, value in by_severity.items() if key)),
        "by_decision": dict(sorted(by_decision.items())),
        "decision_examples": {key: value for key, value in sorted(decision_examples.items())},
        "decision_drilldowns": {
            key: _review_queue_drilldown_args(
                status=status,
                issue_type=issue_type,
                title_cluster=title_cluster_filter,
                fix_strategy=fix_strategy_filter,
                cluster_strategy=cluster_strategy_filter,
                decision=key,
                reason=reason_filter,
            )
            for key in sorted(by_decision)
        },
        "decision_actions": {
            key: {
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=key,
                        reason=reason_filter,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=decision_provider_series_ids.get(key, []),
                ),
            }
            for key in sorted(by_decision)
        },
        "decision_resolutions": {
            key: _review_queue_resolve_args(
                issue_type=issue_type,
                title_cluster=title_cluster_filter,
                fix_strategy=fix_strategy_filter,
                cluster_strategy=cluster_strategy_filter,
                decision=key,
                reason=reason_filter,
            )
            for key in sorted(by_decision)
            if status == "open"
        },
        "top_reasons": [
            {
                "reason": reason,
                "count": count,
                "examples": reason_examples.get(reason, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=reason_provider_series_ids.get(reason, []),
                ),
            }
            for reason, count in by_reason.most_common(10)
        ],
        "top_reason_families": [
            {
                "reason_family": reason_family,
                "count": count,
                "examples": reason_family_examples.get(reason_family, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason_filter,
                    reason_family=reason_family,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason_filter,
                        reason_family=reason_family,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=reason_family_provider_series_ids.get(reason_family, []),
                ),
            }
            for reason_family, count in by_reason_family.most_common(10)
        ],
        "top_title_clusters": [
            {
                "cluster": cluster,
                "label": title_cluster_labels.get(cluster, cluster),
                "count": count,
                "examples": title_cluster_examples.get(cluster, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=cluster,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason_filter,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=cluster,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason_filter,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=title_cluster_provider_series_ids.get(cluster, []),
                ),
            }
            for cluster, count in by_title_cluster.most_common(10)
        ],
        "top_fix_strategies": [
            {
                "strategy": strategy,
                "count": count,
                "examples": fix_strategy_examples.get(strategy, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=strategy,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason_filter,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=strategy,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason_filter,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=fix_strategy_provider_series_ids.get(strategy, []),
                ),
            }
            for strategy, count in by_fix_strategy.most_common(10)
        ],
        "top_fix_strategy_families": [
            {
                "strategy_family": strategy_family,
                "count": count,
                "examples": fix_strategy_family_examples.get(strategy_family, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason_filter,
                    fix_strategy_family=strategy_family,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason_filter,
                        fix_strategy_family=strategy_family,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=fix_strategy_family_provider_series_ids.get(strategy_family, []),
                ),
            }
            for strategy_family, count in by_fix_strategy_family.most_common(10)
        ],
        "top_cluster_strategies": [
            {
                "cluster_strategy": cluster_strategy_key,
                "cluster": cluster_strategy_parts.get(cluster_strategy_key, {}).get("cluster"),
                "strategy": cluster_strategy_parts.get(cluster_strategy_key, {}).get("strategy"),
                "label": title_cluster_labels.get(
                    cluster_strategy_parts.get(cluster_strategy_key, {}).get("cluster", ""),
                    cluster_strategy_parts.get(cluster_strategy_key, {}).get("cluster"),
                ),
                "count": count,
                "examples": cluster_strategy_examples.get(cluster_strategy_key, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_key,
                    decision=decision_filter,
                    reason=reason_filter,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_key,
                        decision=decision_filter,
                        reason=reason_filter,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=cluster_strategy_provider_series_ids.get(cluster_strategy_key, []),
                ),
            }
            for cluster_strategy_key, count in by_cluster_strategy.most_common(10)
        ],
        "top_cluster_strategy_families": [
            {
                "cluster_strategy_family": cluster_strategy_family_key,
                "cluster": cluster_strategy_family_parts.get(cluster_strategy_family_key, {}).get("cluster"),
                "strategy_family": cluster_strategy_family_parts.get(cluster_strategy_family_key, {}).get("strategy"),
                "label": title_cluster_labels.get(
                    cluster_strategy_family_parts.get(cluster_strategy_family_key, {}).get("cluster", ""),
                    cluster_strategy_family_parts.get(cluster_strategy_family_key, {}).get("cluster"),
                ),
                "count": count,
                "examples": cluster_strategy_family_examples.get(cluster_strategy_family_key, []),
                "drilldown_args": _review_queue_drilldown_args(
                    status=status,
                    issue_type=issue_type,
                    title_cluster=title_cluster_filter,
                    fix_strategy=fix_strategy_filter,
                    cluster_strategy=cluster_strategy_filter,
                    decision=decision_filter,
                    reason=reason_filter,
                    cluster_strategy_family=cluster_strategy_family_key,
                ),
                **_review_queue_status_action_fields(
                    status,
                    _review_queue_status_action_args(
                        status=status,
                        issue_type=issue_type,
                        title_cluster=title_cluster_filter,
                        fix_strategy=fix_strategy_filter,
                        cluster_strategy=cluster_strategy_filter,
                        decision=decision_filter,
                        reason=reason_filter,
                        cluster_strategy_family=cluster_strategy_family_key,
                    ),
                ),
                **_review_queue_refresh_fields(
                    issue_type=effective_refresh_issue_type,
                    provider_series_ids=cluster_strategy_family_provider_series_ids.get(cluster_strategy_family_key, []),
                ),
            }
            for cluster_strategy_family_key, count in by_cluster_strategy_family.most_common(10)
        ],
    }


_REVIEW_QUEUE_NEXT_BUCKET_ORDER = {
    "cluster-strategy": "top_cluster_strategies",
    "cluster-strategy-family": "top_cluster_strategy_families",
    "fix-strategy": "top_fix_strategies",
    "fix-strategy-family": "top_fix_strategy_families",
    "title-cluster": "top_title_clusters",
    "reason": "top_reasons",
    "reason-family": "top_reason_families",
    "decision": "by_decision",
}


_REVIEW_QUEUE_AUTO_BUCKET_ORDER = [
    "cluster-strategy-family",
    "cluster-strategy",
    "fix-strategy-family",
    "fix-strategy",
    "title-cluster",
    "reason-family",
    "reason",
    "decision",
]


def _review_queue_bucket_candidates(summary: dict[str, object], *, bucket: str) -> list[dict[str, object]]:
    if bucket == "decision":
        decision_counts = summary.get("by_decision")
        if not isinstance(decision_counts, dict) or not decision_counts:
            return []
        drilldowns = summary.get("decision_drilldowns")
        ordered = sorted(
            ((str(key), value) for key, value in decision_counts.items() if isinstance(value, int)),
            key=lambda item: (-item[1], item[0]),
        )
        candidates: list[dict[str, object]] = []
        for decision_name, count in ordered:
            drilldown_args = drilldowns.get(decision_name) if isinstance(drilldowns, dict) else None
            if not isinstance(drilldown_args, list):
                drilldown_args = _review_queue_drilldown_args(
                    status=summary.get("status") if isinstance(summary.get("status"), str) else "open",
                    issue_type=summary.get("issue_type_filter") if isinstance(summary.get("issue_type_filter"), str) else None,
                    title_cluster=summary.get("title_cluster_filter") if isinstance(summary.get("title_cluster_filter"), str) else None,
                    fix_strategy=summary.get("fix_strategy_filter") if isinstance(summary.get("fix_strategy_filter"), str) else None,
                    cluster_strategy=summary.get("cluster_strategy_filter") if isinstance(summary.get("cluster_strategy_filter"), str) else None,
                    decision=decision_name,
                    reason=summary.get("reason_filter") if isinstance(summary.get("reason_filter"), str) else None,
                )
            action_args = _review_queue_status_action_args(
                status=summary.get("status") if isinstance(summary.get("status"), str) else "open",
                issue_type=summary.get("issue_type_filter") if isinstance(summary.get("issue_type_filter"), str) else None,
                title_cluster=summary.get("title_cluster_filter") if isinstance(summary.get("title_cluster_filter"), str) else None,
                fix_strategy=summary.get("fix_strategy_filter") if isinstance(summary.get("fix_strategy_filter"), str) else None,
                cluster_strategy=summary.get("cluster_strategy_filter") if isinstance(summary.get("cluster_strategy_filter"), str) else None,
                decision=decision_name,
                reason=summary.get("reason_filter") if isinstance(summary.get("reason_filter"), str) else None,
            )
            decision_actions = summary.get("decision_actions") if isinstance(summary.get("decision_actions"), dict) else {}
            action_fields = decision_actions.get(decision_name) if isinstance(decision_actions, dict) else None
            if not isinstance(action_fields, dict):
                action_fields = _review_queue_status_action_fields(
                    summary.get("status") if isinstance(summary.get("status"), str) else "open",
                    action_args,
                )
            candidates.append(
                {
                    "bucket_type": "decision",
                    "bucket_key": decision_name,
                    "count": count,
                    "drilldown_args": drilldown_args,
                    "drilldown_command": _build_review_queue_command(drilldown_args),
                    **action_fields,
                }
            )
        return candidates

    summary_key = _REVIEW_QUEUE_NEXT_BUCKET_ORDER[bucket]
    entries = summary.get(summary_key)
    if not isinstance(entries, list):
        return []
    key_field = {
        "cluster-strategy": "cluster_strategy",
        "cluster-strategy-family": "cluster_strategy_family",
        "fix-strategy": "strategy",
        "fix-strategy-family": "strategy_family",
        "title-cluster": "cluster",
        "reason": "reason",
        "reason-family": "reason_family",
    }[bucket]
    candidates: list[dict[str, object]] = []
    for chosen in entries:
        if not isinstance(chosen, dict):
            continue
        drilldown_args = chosen.get("drilldown_args")
        if not isinstance(drilldown_args, list):
            continue
        action_fields = {
            key: value
            for key, value in chosen.items()
            if key in {
                "action",
                "action_args",
                "action_command",
                "resolve_args",
                "resolve_command",
                "reopen_args",
                "reopen_command",
                "refresh_provider_series_ids",
                "refresh_args",
                "refresh_command",
            }
        }
        candidates.append(
            {
                "bucket_type": bucket,
                "bucket_key": chosen.get(key_field),
                "count": chosen.get("count"),
                "label": chosen.get("label"),
                "examples": chosen.get("examples"),
                "drilldown_args": drilldown_args,
                "drilldown_command": _build_review_queue_command(drilldown_args),
                **action_fields,
            }
        )
    return candidates


def _build_review_queue_worklist(
    summary: dict[str, object],
    *,
    bucket_order: list[str],
    limit: int,
) -> list[dict[str, object]]:
    if limit <= 0:
        return []
    selected: list[dict[str, object]] = []
    seen_commands: set[str] = set()
    for bucket in bucket_order:
        for candidate in _review_queue_bucket_candidates(summary, bucket=bucket):
            command = candidate.get("drilldown_command")
            if not isinstance(command, str) or not command:
                continue
            if command in seen_commands:
                continue
            selected.append(candidate)
            seen_commands.add(command)
            if len(selected) >= limit:
                return selected
    return selected


def _build_shell_command(args: list[str]) -> str:
    return " ".join(shlex.quote(part) for part in args)



def _build_review_queue_command(args: list[str]) -> str:
    return "PYTHONPATH=src python3 -m mal_updater.cli " + " ".join(
        json.dumps(part) if any(char.isspace() for char in part) else part
        for part in args
    )


def _select_review_queue_next_bucket(summary: dict[str, object], *, bucket: str) -> dict[str, object] | None:
    candidates = _review_queue_bucket_candidates(summary, bucket=bucket)
    return candidates[0] if candidates else None


def _cmd_review_queue_next(
    project_root: Path | None,
    status: str,
    issue_type: str | None,
    bucket: str,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    items = list_review_queue_entries(config.db_path, status=status, issue_type=issue_type)
    provider_series_titles = get_provider_series_title_map(
        config.db_path,
        provider="crunchyroll",
        provider_series_ids=[item.provider_series_id for item in items if item.provider_series_id],
    )
    filtered_items = _filter_review_queue_items(
        items,
        provider_series_titles=provider_series_titles,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    summary = _summarize_review_queue(
        filtered_items,
        status=status,
        issue_type=issue_type,
        provider_series_titles=provider_series_titles,
        title_cluster_filter=title_cluster,
        fix_strategy_filter=fix_strategy,
        cluster_strategy_filter=cluster_strategy,
        decision_filter=decision,
        reason_filter=reason,
        reason_family_filter=reason_family,
        fix_strategy_family_filter=fix_strategy_family,
        cluster_strategy_family_filter=cluster_strategy_family,
    )
    bucket_order = [bucket] if bucket != "auto" else list(_REVIEW_QUEUE_AUTO_BUCKET_ORDER)
    chosen_bucket = None
    for candidate_bucket in bucket_order:
        chosen_bucket = _select_review_queue_next_bucket(summary, bucket=candidate_bucket)
        if chosen_bucket is not None:
            break
    payload = {
        "status": status,
        "issue_type_filter": issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster) if title_cluster else None,
        "fix_strategy_filter": fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None,
        "cluster_strategy_filter": cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None,
        "decision_filter": decision.strip() if isinstance(decision, str) and decision.strip() else None,
        "reason_filter": reason.strip() if isinstance(reason, str) and reason.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None,
        "count": summary["count"],
        "bucket_preference": bucket,
        "selected": chosen_bucket,
    }
    print(json.dumps(payload, indent=2))
    return 0


def _load_filtered_review_queue_context(
    project_root: Path | None,
    *,
    status: str,
    issue_type: str | None,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> tuple[object, dict[str, dict[str, str | None]], list[object], dict[str, object]]:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    items = list_review_queue_entries(config.db_path, status=status, issue_type=issue_type)
    provider_series_titles = get_provider_series_title_map(
        config.db_path,
        provider="crunchyroll",
        provider_series_ids=[item.provider_series_id for item in items if item.provider_series_id],
    )
    filtered_items = _filter_review_queue_items(
        items,
        provider_series_titles=provider_series_titles,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    summary = _summarize_review_queue(
        filtered_items,
        status=status,
        issue_type=issue_type,
        provider_series_titles=provider_series_titles,
        title_cluster_filter=title_cluster,
        fix_strategy_filter=fix_strategy,
        cluster_strategy_filter=cluster_strategy,
        decision_filter=decision,
        reason_filter=reason,
        reason_family_filter=reason_family,
        fix_strategy_family_filter=fix_strategy_family,
        cluster_strategy_family_filter=cluster_strategy_family,
    )
    return config, provider_series_titles, filtered_items, summary


def _cmd_review_queue_worklist(
    project_root: Path | None,
    status: str,
    issue_type: str | None,
    limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    _, _, _, summary = _load_filtered_review_queue_context(
        project_root,
        status=status,
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    selected = _build_review_queue_worklist(
        summary,
        bucket_order=list(_REVIEW_QUEUE_AUTO_BUCKET_ORDER),
        limit=limit,
    )
    payload = {
        "status": status,
        "issue_type_filter": issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster) if title_cluster else None,
        "fix_strategy_filter": fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None,
        "cluster_strategy_filter": cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None,
        "decision_filter": decision.strip() if isinstance(decision, str) and decision.strip() else None,
        "reason_filter": reason.strip() if isinstance(reason, str) and reason.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None,
        "count": summary["count"],
        "limit": limit,
        "selected": selected,
    }
    print(json.dumps(payload, indent=2))
    return 0


def _review_queue_bucket_filter_kwargs(candidate: dict[str, object]) -> dict[str, str]:
    bucket_type = candidate.get("bucket_type")
    bucket_key = candidate.get("bucket_key")
    if not isinstance(bucket_type, str) or not isinstance(bucket_key, str) or not bucket_key.strip():
        return {}
    if bucket_type == "cluster-strategy":
        return {"cluster_strategy": bucket_key.strip()}
    if bucket_type == "cluster-strategy-family":
        return {"cluster_strategy_family": bucket_key.strip()}
    if bucket_type == "fix-strategy":
        return {"fix_strategy": bucket_key.strip()}
    if bucket_type == "fix-strategy-family":
        return {"fix_strategy_family": bucket_key.strip()}
    if bucket_type == "title-cluster":
        return {"title_cluster": bucket_key.strip()}
    if bucket_type == "reason":
        return {"reason": bucket_key.strip()}
    if bucket_type == "reason-family":
        return {"reason_family": bucket_key.strip()}
    if bucket_type == "decision":
        return {"decision": bucket_key.strip()}
    return {}



def _cmd_review_queue_apply_worklist(
    project_root: Path | None,
    status: str,
    issue_type: str | None,
    limit: int,
    per_bucket_limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    config, provider_series_titles, filtered_items, summary = _load_filtered_review_queue_context(
        project_root,
        status=status,
        issue_type=issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    selected_buckets = _build_review_queue_worklist(
        summary,
        bucket_order=list(_REVIEW_QUEUE_AUTO_BUCKET_ORDER),
        limit=limit,
    )
    selected_ids: list[int] = []
    seen_ids: set[int] = set()
    bucket_updates: list[dict[str, object]] = []
    for candidate in selected_buckets:
        bucket_filters = _review_queue_bucket_filter_kwargs(candidate)
        bucket_items = _filter_review_queue_items(
            filtered_items,
            provider_series_titles=provider_series_titles,
            **bucket_filters,
        )
        chosen_items = bucket_items if per_bucket_limit == 0 else bucket_items[:per_bucket_limit]
        new_items = [item for item in chosen_items if item.id not in seen_ids]
        if not new_items:
            continue
        for item in new_items:
            seen_ids.add(item.id)
            selected_ids.append(item.id)
        bucket_updates.append(
            {
                **candidate,
                "matched_rows": len(bucket_items),
                "selected_rows": len(chosen_items),
                "new_rows": len(new_items),
                "selected_entry_ids": [item.id for item in new_items],
            }
        )
    status_to = "open" if status == "resolved" else "resolved"
    updated_count = update_review_queue_entry_statuses(
        config.db_path,
        entry_ids=selected_ids,
        status=status_to,
    )
    payload = {
        "status_from": status,
        "status_to": status_to,
        "issue_type_filter": issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster) if title_cluster else None,
        "fix_strategy_filter": fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None,
        "cluster_strategy_filter": cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None,
        "decision_filter": decision.strip() if isinstance(decision, str) and decision.strip() else None,
        "reason_filter": reason.strip() if isinstance(reason, str) and reason.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None,
        "count": summary["count"],
        "worklist_limit": limit,
        "per_bucket_limit": per_bucket_limit,
        "selected_bucket_count": len(selected_buckets),
        "updated": updated_count,
        "selected_entry_ids": selected_ids,
        "selected_buckets": bucket_updates,
    }
    print(json.dumps(payload, indent=2))
    return 0



def _cmd_review_queue_refresh_worklist(
    project_root: Path | None,
    status: str,
    issue_type: str | None,
    limit: int,
    per_bucket_limit: int,
    mapping_limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    effective_issue_type = issue_type or "mapping_review"
    if effective_issue_type != "mapping_review":
        print("review-queue-refresh-worklist currently supports only mapping_review", file=sys.stderr)
        return 2
    config, provider_series_titles, filtered_items, summary = _load_filtered_review_queue_context(
        project_root,
        status=status,
        issue_type=effective_issue_type,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    selected_buckets = _build_review_queue_worklist(
        summary,
        bucket_order=list(_REVIEW_QUEUE_AUTO_BUCKET_ORDER),
        limit=limit,
    )
    selected_provider_series_ids: list[str] = []
    seen_provider_series_ids: set[str] = set()
    bucket_updates: list[dict[str, object]] = []
    for candidate in selected_buckets:
        bucket_filters = _review_queue_bucket_filter_kwargs(candidate)
        bucket_items = _filter_review_queue_items(
            filtered_items,
            provider_series_titles=provider_series_titles,
            **bucket_filters,
        )
        chosen_items = bucket_items if per_bucket_limit == 0 else bucket_items[:per_bucket_limit]
        chosen_provider_series_ids = [
            item.provider_series_id
            for item in chosen_items
            if isinstance(item.provider_series_id, str) and item.provider_series_id.strip()
        ]
        new_provider_series_ids = [
            provider_series_id
            for provider_series_id in chosen_provider_series_ids
            if provider_series_id not in seen_provider_series_ids
        ]
        if not new_provider_series_ids:
            continue
        for provider_series_id in new_provider_series_ids:
            seen_provider_series_ids.add(provider_series_id)
            selected_provider_series_ids.append(provider_series_id)
        bucket_updates.append(
            {
                **candidate,
                "matched_rows": len(bucket_items),
                "selected_rows": len(chosen_items),
                "new_rows": len(new_provider_series_ids),
                "selected_provider_series_ids": new_provider_series_ids,
            }
        )
    try:
        refresh_result = _refresh_mapping_review_queue_for_provider_series_ids(
            config,
            selected_provider_series_ids,
            mapping_limit,
        ) if selected_provider_series_ids else {
            "provider_series_ids": [],
            "items": [],
            "review_queue": {"resolved": 0, "inserted": 0},
        }
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    payload = {
        "status": status,
        "issue_type_filter": effective_issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster) if title_cluster else None,
        "fix_strategy_filter": fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None,
        "cluster_strategy_filter": cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None,
        "decision_filter": decision.strip() if isinstance(decision, str) and decision.strip() else None,
        "reason_filter": reason.strip() if isinstance(reason, str) and reason.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None,
        "count": summary["count"],
        "worklist_limit": limit,
        "per_bucket_limit": per_bucket_limit,
        "mapping_limit": mapping_limit,
        "selected_bucket_count": len(selected_buckets),
        "selected_provider_series_ids": selected_provider_series_ids,
        "selected_buckets": bucket_updates,
        "refresh": refresh_result,
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_list_review_queue(
    project_root: Path | None,
    status: str,
    issue_type: str | None,
    summary: bool,
    limit: int,
    provider_series_id: str | None,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    items = list_review_queue_entries(
        config.db_path,
        status=status,
        issue_type=issue_type,
        provider_series_id=provider_series_id,
    )
    provider_series_titles = get_provider_series_title_map(
        config.db_path,
        provider="crunchyroll",
        provider_series_ids=[item.provider_series_id for item in items if item.provider_series_id],
    )
    items = _filter_review_queue_items(
        items,
        provider_series_titles=provider_series_titles,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    if summary:
        print(
            json.dumps(
                _summarize_review_queue(
                    items,
                    status=status,
                    issue_type=issue_type,
                    provider_series_titles=provider_series_titles,
                    title_cluster_filter=title_cluster,
                    fix_strategy_filter=fix_strategy,
                    cluster_strategy_filter=cluster_strategy,
                    decision_filter=decision,
                    reason_filter=reason,
                ),
                indent=2,
            )
        )
        return 0
    if limit > 0:
        items = items[:limit]
    print(
        json.dumps(
            [
                {
                    "id": item.id,
                    "provider": item.provider,
                    "provider_series_id": item.provider_series_id,
                    "provider_episode_id": item.provider_episode_id,
                    "issue_type": item.issue_type,
                    "severity": item.severity,
                    "status": item.status,
                    "created_at": item.created_at,
                    "resolved_at": item.resolved_at,
                    "payload": item.payload,
                }
                for item in items
            ],
            indent=2,
        )
    )
    return 0


def _cmd_update_review_queue_status(
    project_root: Path | None,
    *,
    status_from: str,
    status_to: str,
    issue_type: str | None,
    limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    items = list_review_queue_entries(config.db_path, status=status_from, issue_type=issue_type)
    provider_series_titles = get_provider_series_title_map(
        config.db_path,
        provider="crunchyroll",
        provider_series_ids=[item.provider_series_id for item in items if item.provider_series_id],
    )
    filtered_items = _filter_review_queue_items(
        items,
        provider_series_titles=provider_series_titles,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )
    selected_items = filtered_items if limit == 0 else filtered_items[:limit]
    updated_count = update_review_queue_entry_statuses(
        config.db_path,
        entry_ids=[item.id for item in selected_items],
        status=status_to,
    )
    payload = {
        "status_from": status_from,
        "status_to": status_to,
        "issue_type_filter": issue_type,
        "title_cluster_filter": _review_queue_title_cluster_key(title_cluster) if title_cluster else None,
        "fix_strategy_filter": fix_strategy.strip() if isinstance(fix_strategy, str) and fix_strategy.strip() else None,
        "cluster_strategy_filter": cluster_strategy.strip() if isinstance(cluster_strategy, str) and cluster_strategy.strip() else None,
        "decision_filter": decision.strip() if isinstance(decision, str) and decision.strip() else None,
        "reason_filter": reason.strip() if isinstance(reason, str) and reason.strip() else None,
        "reason_family_filter": _review_queue_reason_family(reason_family) if isinstance(reason_family, str) and reason_family.strip() else None,
        "fix_strategy_family_filter": fix_strategy_family.strip() if isinstance(fix_strategy_family, str) and fix_strategy_family.strip() else None,
        "cluster_strategy_family_filter": cluster_strategy_family.strip() if isinstance(cluster_strategy_family, str) and cluster_strategy_family.strip() else None,
        "limit": limit,
        "matched": len(filtered_items),
        "updated": updated_count,
        "selected": [
            {
                "id": item.id,
                "provider_series_id": item.provider_series_id,
                "issue_type": item.issue_type,
                "severity": item.severity,
                "decision": item.payload.get("decision") if isinstance(item.payload, dict) else None,
                "reasons": item.payload.get("reasons") if isinstance(item.payload.get("reasons"), list) else [],
                "title": _review_queue_item_label(item, provider_series_titles=provider_series_titles).get("title"),
            }
            for item in selected_items
        ],
    }
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_resolve_review_queue(
    project_root: Path | None,
    issue_type: str | None,
    limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    return _cmd_update_review_queue_status(
        project_root,
        status_from="open",
        status_to="resolved",
        issue_type=issue_type,
        limit=limit,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )


def _cmd_reopen_review_queue(
    project_root: Path | None,
    issue_type: str | None,
    limit: int,
    title_cluster: str | None,
    fix_strategy: str | None,
    cluster_strategy: str | None,
    decision: str | None,
    reason: str | None,
    reason_family: str | None,
    fix_strategy_family: str | None,
    cluster_strategy_family: str | None,
) -> int:
    return _cmd_update_review_queue_status(
        project_root,
        status_from="resolved",
        status_to="open",
        issue_type=issue_type,
        limit=limit,
        title_cluster=title_cluster,
        fix_strategy=fix_strategy,
        cluster_strategy=cluster_strategy,
        decision=decision,
        reason=reason,
        reason_family=reason_family,
        fix_strategy_family=fix_strategy_family,
        cluster_strategy_family=cluster_strategy_family,
    )


def _cmd_apply_sync(project_root: Path | None, limit: int, mapping_limit: int, exact_approved_only: bool, execute: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    try:
        results = execute_approved_sync(
            config,
            limit=_normalize_limit(limit),
            mapping_limit=mapping_limit,
            exact_approved_only=exact_approved_only,
            dry_run=not execute,
        )
    except MalApiError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps([item.as_dict() for item in results], indent=2))
    return 0


def _cmd_recommend(project_root: Path | None, limit: int, flat: bool) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    results = build_recommendations(config, limit=_normalize_limit(limit))
    payload: object
    if flat:
        payload = [item.as_dict() for item in results]
    else:
        payload = group_recommendations(results)
    print(json.dumps(payload, indent=2))
    return 0


def _cmd_recommend_refresh_metadata(
    project_root: Path | None,
    limit: int,
    include_discovery_targets: bool,
    discovery_target_limit: int,
) -> int:
    config = load_config(project_root)
    ensure_directories(config)
    bootstrap_database(config.db_path)
    summary = refresh_recommendation_metadata(
        config,
        limit=_normalize_limit(limit),
        include_discovery_targets=include_discovery_targets,
        discovery_target_limit=_normalize_limit(discovery_target_limit),
    )
    print(json.dumps(summary.as_dict(), indent=2))
    return 0


def _cmd_sync(_: Path | None) -> int:
    raise SystemExit(
        "Sync pipeline not implemented yet. Use 'dry-run-sync' for guarded read-only proposals or 'apply-sync' for the approved-mapping-only executor."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mal-updater")
    parser.add_argument("--project-root", type=Path, default=None, help="Override project root")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("init", help="Create the externalized runtime dirs and initialize SQLite schema")
    subparsers.add_parser("status", help="Print resolved config, runtime paths, and secret presence")
    install_service_parser = subparsers.add_parser("install-service", help="Install/update the repo-owned user systemd service for the long-lived MAL-Updater daemon")
    install_service_parser.add_argument("--no-start", action="store_true", help="Write/enable the service but do not restart it immediately")
    uninstall_service_parser = subparsers.add_parser("uninstall-service", help="Disable and remove the repo-owned user systemd service")
    uninstall_service_parser.add_argument("--no-stop", action="store_true", help="Remove/disable the service without attempting a stop first")
    subparsers.add_parser("start-service", help="Start the MAL-Updater user service")
    subparsers.add_parser("stop-service", help="Stop the MAL-Updater user service")
    subparsers.add_parser("restart-service", help="Restart the MAL-Updater user service")
    service_status = subparsers.add_parser("service-status", help="Print MAL-Updater user service health/runtime status")
    service_status.add_argument("--format", default="json", choices=["json", "summary"], help="Output format: machine-readable JSON (default) or terse operator summary")
    subparsers.add_parser("service-run", help="Run the MAL-Updater daemon loop in the foreground")
    subparsers.add_parser("service-run-once", help="Run one MAL-Updater daemon loop pass and exit")
    bootstrap_audit = subparsers.add_parser(
        "bootstrap-audit",
        help="Audit bootstrap/onboarding readiness: dependencies, runtime dirs, credentials, redirect settings, and service install prerequisites",
    )
    bootstrap_audit.add_argument("--summary", action="store_true", help="Emit terse line-oriented output instead of JSON")
    health_check = subparsers.add_parser("health-check", help="Emit a local operational health summary for auth material, snapshot freshness, mappings, and review backlog")
    health_check.add_argument("--stale-hours", type=float, default=72.0, help="Warn when the latest completed ingest snapshot is older than this many hours")
    health_check.add_argument("--strict", action="store_true", help="Return exit code 2 when warnings are present, while still printing the JSON payload")
    health_check.add_argument("--review-issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional review_queue issue type to use when building recommended_next/recommended_worklist")
    health_check.add_argument("--review-worklist-limit", type=int, default=3, help="How many ranked review backlog drilldowns to include in recommended_worklist (use 0 to suppress it)")
    health_check.add_argument("--format", default="json", choices=["json", "summary"], help="Output format: machine-readable JSON (default) or terse operator summary")
    health_check.add_argument("--mapping-coverage-threshold", type=float, default=0.8, help="Warn when approved provider->MAL mapping coverage falls below this ratio (default: 0.8)")
    health_check.add_argument("--maintenance-review-limit", type=int, default=25, help="When coverage is low, cap the auto-recommended review-mappings series scan to this many series (use 0 for all)")
    mal_auth = subparsers.add_parser("mal-auth-url", help="Generate a MAL OAuth authorization URL + PKCE verifier")
    mal_auth.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    mal_auth_login = subparsers.add_parser("mal-auth-login", help="Run a local loopback MAL OAuth flow and persist returned tokens")
    mal_auth_login.add_argument("--timeout-seconds", type=float, default=300.0, help="How long to wait for the local callback before failing")
    mal_auth_login.add_argument("--no-verify", action="store_true", help="Skip the follow-up GET /users/@me token check")
    mal_refresh = subparsers.add_parser("mal-refresh", help="Refresh the persisted MAL access token using the local refresh token")
    mal_refresh.add_argument("--no-verify", action="store_true", help="Skip the follow-up GET /users/@me token check")
    subparsers.add_parser("mal-whoami", help="Call MAL GET /users/@me with the currently configured access token")
    provider_auth_login = subparsers.add_parser(
        "provider-auth-login",
        help="Run provider-specific auth bootstrap for a named content provider",
    )
    provider_auth_login.add_argument("--provider", required=True, choices=list_provider_slugs(), help="Provider slug")
    provider_auth_login.add_argument("--profile", default="default", help="Provider state profile name")
    provider_auth_login.add_argument("--no-verify", action="store_true", help="Skip any provider-specific follow-up account verification step")
    provider_fetch_snapshot = subparsers.add_parser(
        "provider-fetch-snapshot",
        help="Fetch a live normalized snapshot from a named content provider",
    )
    provider_fetch_snapshot.add_argument("--provider", required=True, choices=list_provider_slugs(), help="Provider slug")
    provider_fetch_snapshot.add_argument("--profile", default="default", help="Provider state profile name")
    provider_fetch_snapshot.add_argument("--out", type=Path, default=None, help="Optional JSON file path to write the fetched snapshot")
    provider_fetch_snapshot.add_argument("--ingest", action="store_true", help="Immediately validate and ingest the fetched snapshot into SQLite")
    provider_fetch_snapshot.add_argument(
        "--full-refresh",
        action="store_true",
        help="Ignore provider-local incremental boundaries and fetch the full currently reachable history/watchlist surfaces",
    )
    crunchyroll_auth_login = subparsers.add_parser(
        "crunchyroll-auth-login",
        help="Use local Crunchyroll username/password secrets to stage Crunchyroll refresh-token auth material",
    )
    crunchyroll_auth_login.add_argument("--profile", default="default", help="Crunchyroll state profile name")
    crunchyroll_auth_login.add_argument("--no-verify", action="store_true", help="Skip the follow-up GET /accounts/v1/me token check")
    crunchyroll_fetch_snapshot = subparsers.add_parser(
        "crunchyroll-fetch-snapshot",
        help="Use the Python Crunchyroll transport to fetch a live normalized snapshot",
    )
    crunchyroll_fetch_snapshot.add_argument("--profile", default="default", help="Crunchyroll state profile name")
    crunchyroll_fetch_snapshot.add_argument("--out", type=Path, default=None, help="Optional JSON file path to write the fetched snapshot")
    crunchyroll_fetch_snapshot.add_argument("--ingest", action="store_true", help="Immediately validate and ingest the fetched snapshot into SQLite")
    crunchyroll_fetch_snapshot.add_argument(
        "--full-refresh",
        action="store_true",
        help="Ignore the local incremental sync boundary and fetch the full currently reachable Crunchyroll history/watchlist pages",
    )
    validate_snapshot = subparsers.add_parser("validate-snapshot", help="Validate a normalized provider snapshot JSON payload")
    validate_snapshot.add_argument("snapshot", nargs="?", type=Path, help="Snapshot JSON file path (defaults to stdin)")
    ingest_snapshot = subparsers.add_parser("ingest-snapshot", help="Validate and ingest a normalized provider snapshot into SQLite")
    ingest_snapshot.add_argument("snapshot", nargs="?", type=Path, help="Snapshot JSON file path (defaults to stdin)")
    map_series_cmd = subparsers.add_parser("map-series", help="Search MAL for conservative mapping candidates for ingested provider series")
    map_series_cmd.add_argument("--limit", type=int, default=20, help="How many ingested series to inspect")
    map_series_cmd.add_argument("--mapping-limit", type=int, default=5, help="How many MAL candidates to keep per series")
    review_mappings = subparsers.add_parser(
        "review-mappings",
        help="Build a mapping review list that preserves existing approved mappings and flags the rest for approval or manual review",
    )
    review_mappings.add_argument("--limit", type=int, default=20, help="How many ingested series to inspect (use 0 for all; required when persisting review_queue)")
    review_mappings.add_argument("--mapping-limit", type=int, default=5, help="How many MAL candidates to keep per series")
    review_mappings.add_argument("--persist-review-queue", action="store_true", help="Replace the open mapping_review queue rows with this run's unresolved items")
    refresh_mapping_review_queue = subparsers.add_parser(
        "refresh-mapping-review-queue",
        help="Recompute mapping-review results for specific provider_series_id values and refresh only those persisted queue rows",
    )
    refresh_mapping_review_queue.add_argument(
        "--provider-series-id",
        action="append",
        default=[],
        help="Provider provider_series_id to refresh in the persisted mapping_review queue (repeatable)",
    )
    refresh_mapping_review_queue.add_argument(
        "--all-open",
        action="store_true",
        help="Refresh every currently open persisted mapping_review row (may be combined with explicit --provider-series-id values)",
    )
    refresh_mapping_review_queue.add_argument("--title-cluster", default=None, help="Only refresh open mapping_review rows whose normalized title cluster matches this value")
    refresh_mapping_review_queue.add_argument("--decision", default=None, help="Only refresh open mapping_review rows whose payload decision exactly matches this value")
    refresh_mapping_review_queue.add_argument("--reason", default=None, help="Only refresh open mapping_review rows whose payload reasons include this exact value")
    refresh_mapping_review_queue.add_argument("--reason-family", default=None, help="Only refresh open mapping_review rows whose payload reasons include this normalized reason family")
    refresh_mapping_review_queue.add_argument("--fix-strategy", default=None, help="Only refresh open mapping_review rows whose normalized fix strategy exactly matches this value")
    refresh_mapping_review_queue.add_argument("--fix-strategy-family", default=None, help="Only refresh open mapping_review rows whose normalized fix strategy family exactly matches this value")
    refresh_mapping_review_queue.add_argument("--cluster-strategy", default=None, help="Only refresh open mapping_review rows whose combined normalized title-cluster/fix-strategy exactly matches this value")
    refresh_mapping_review_queue.add_argument("--cluster-strategy-family", default=None, help="Only refresh open mapping_review rows whose combined normalized title-cluster/fix-strategy family exactly matches this value")
    refresh_mapping_review_queue.add_argument("--mapping-limit", type=int, default=5, help="How many MAL candidates to keep per series")
    list_mappings = subparsers.add_parser("list-mappings", help="List persisted provider -> MAL mappings from SQLite")
    list_mappings.add_argument("--approved-only", action="store_true", help="Only include mappings explicitly approved by the user")
    approve_mapping = subparsers.add_parser("approve-mapping", help="Persist a user-approved provider -> MAL series mapping")
    approve_mapping.add_argument("provider_series_id", help="Provider provider_series_id to approve")
    approve_mapping.add_argument("mal_anime_id", type=int, help="Chosen MAL anime id")
    approve_mapping.add_argument("--confidence", type=float, default=None, help="Optional confidence score to store alongside the approval")
    approve_mapping.add_argument("--notes", default=None, help="Optional operator note explaining the approval")
    approve_mapping.add_argument(
        "--exact",
        action="store_true",
        help="Mark this manual approval as exact-safe so the unattended exact-approved executor may use it",
    )
    dry_run_sync = subparsers.add_parser("dry-run-sync", help="Generate guarded read-only MAL sync proposals from ingested provider data")
    dry_run_sync.add_argument("--provider", default="all", choices=["all", *list_provider_slugs()], help="Provider slug to plan against, or 'all' to aggregate across providers")
    dry_run_sync.add_argument("--limit", type=int, default=20, help="How many ingested series to inspect (use 0 for all; required when persisting review_queue)")
    dry_run_sync.add_argument("--mapping-limit", type=int, default=5, help="How many MAL candidates to keep per series")
    dry_run_sync.add_argument(
        "--approved-mappings-only",
        action="store_true",
        help="Only produce proposals for series with explicit user-approved persisted mappings",
    )
    dry_run_sync.add_argument("--persist-review-queue", action="store_true", help="Replace the open sync_review queue rows with this run's non-actionable items")
    dry_run_sync.add_argument(
        "--exact-approved-only",
        action="store_true",
        help="When using approved mappings, restrict planning to exact approved mappings only (currently auto_exact/user_exact)",
    )
    list_review_queue = subparsers.add_parser("list-review-queue", help="List persisted review_queue rows from SQLite")
    list_review_queue.add_argument("--status", default="open", choices=["open", "resolved"], help="Review row status to show")
    list_review_queue.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    list_review_queue.add_argument("--summary", action="store_true", help="Emit a compact summary of queue counts/decisions/reasons instead of every row")
    list_review_queue.add_argument("--limit", type=int, default=0, help="Maximum number of filtered rows to emit in non-summary mode (use 0 for all)")
    list_review_queue.add_argument("--provider-series-id", default=None, help="Only show review rows for one exact provider_series_id")
    list_review_queue.add_argument("--title-cluster", default=None, help="Only show review rows whose normalized title cluster matches this value (for example: 'example show' or 'Example Show Season 2')")
    list_review_queue.add_argument("--decision", default=None, help="Only show review rows whose payload decision exactly matches this value from --summary")
    list_review_queue.add_argument("--reason", default=None, help="Only show review rows whose payload reasons include this exact value from --summary")
    list_review_queue.add_argument("--reason-family", default=None, help="Only show review rows whose payload reasons include this normalized reason family from --summary")
    list_review_queue.add_argument("--fix-strategy", default=None, help="Only show review rows whose decision+reasons strategy exactly matches this value from --summary")
    list_review_queue.add_argument("--fix-strategy-family", default=None, help="Only show review rows whose normalized decision+reason-family strategy exactly matches this value from --summary")
    list_review_queue.add_argument("--cluster-strategy", default=None, help="Only show review rows whose combined franchise/fix-strategy bucket exactly matches this value from --summary (format: '<cluster> || <strategy>')")
    list_review_queue.add_argument("--cluster-strategy-family", default=None, help="Only show review rows whose combined franchise/fix-strategy-family bucket exactly matches this value from --summary (format: '<cluster> || <strategy-family>')")
    review_queue_next = subparsers.add_parser(
        "review-queue-next",
        help="Pick the next highest-signal review backlog bucket and emit the exact drilldown command to run",
    )
    review_queue_next.add_argument("--status", default="open", choices=["open", "resolved"], help="Review row status to inspect")
    review_queue_next.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    review_queue_next.add_argument(
        "--bucket",
        default="auto",
        choices=["auto", "cluster-strategy", "cluster-strategy-family", "fix-strategy", "fix-strategy-family", "title-cluster", "reason", "reason-family", "decision"],
        help="Which bucket family to prefer when choosing the next drilldown",
    )
    review_queue_next.add_argument("--title-cluster", default=None, help="Optional existing title-cluster scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--decision", default=None, help="Optional existing decision scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--reason", default=None, help="Optional existing reason scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--fix-strategy", default=None, help="Optional existing fix-strategy scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--cluster-strategy", default=None, help="Optional existing combined cluster/fix-strategy scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--reason-family", default=None, help="Optional existing reason-family scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--fix-strategy-family", default=None, help="Optional existing fix-strategy-family scope to preserve while choosing the next drilldown")
    review_queue_next.add_argument("--cluster-strategy-family", default=None, help="Optional existing combined cluster/fix-strategy-family scope to preserve while choosing the next drilldown")
    review_queue_worklist = subparsers.add_parser(
        "review-queue-worklist",
        help="Emit the next several highest-signal review backlog drilldowns as a ranked worklist",
    )
    review_queue_worklist.add_argument("--status", default="open", choices=["open", "resolved"], help="Review row status to inspect")
    review_queue_worklist.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    review_queue_worklist.add_argument("--limit", type=int, default=5, help="Maximum number of ranked drilldowns to emit")
    review_queue_worklist.add_argument("--title-cluster", default=None, help="Optional existing title-cluster scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--decision", default=None, help="Optional existing decision scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--reason", default=None, help="Optional existing reason scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--fix-strategy", default=None, help="Optional existing fix-strategy scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--cluster-strategy", default=None, help="Optional existing combined cluster/fix-strategy scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--reason-family", default=None, help="Optional existing reason-family scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--fix-strategy-family", default=None, help="Optional existing fix-strategy-family scope to preserve while building the worklist")
    review_queue_worklist.add_argument("--cluster-strategy-family", default=None, help="Optional existing combined cluster/fix-strategy-family scope to preserve while building the worklist")
    review_queue_apply_worklist = subparsers.add_parser(
        "review-queue-apply-worklist",
        help="Apply the ranked review-queue worklist in one shot by resolving or reopening the selected buckets",
    )
    review_queue_apply_worklist.add_argument("--status", default="open", choices=["open", "resolved"], help="Review row status to mutate (open -> resolve, resolved -> reopen)")
    review_queue_apply_worklist.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    review_queue_apply_worklist.add_argument("--limit", type=int, default=3, help="How many ranked worklist buckets to apply")
    review_queue_apply_worklist.add_argument("--per-bucket-limit", type=int, default=20, help="Maximum number of matching rows to update per selected bucket (use 0 for all)")
    review_queue_apply_worklist.add_argument("--title-cluster", default=None, help="Optional existing title-cluster scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--decision", default=None, help="Optional existing decision scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--reason", default=None, help="Optional existing reason scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--fix-strategy", default=None, help="Optional existing fix-strategy scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--cluster-strategy", default=None, help="Optional existing combined cluster/fix-strategy scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--reason-family", default=None, help="Optional existing reason-family scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--fix-strategy-family", default=None, help="Optional existing fix-strategy-family scope to preserve while applying the worklist")
    review_queue_apply_worklist.add_argument("--cluster-strategy-family", default=None, help="Optional existing combined cluster/fix-strategy-family scope to preserve while applying the worklist")
    review_queue_refresh_worklist = subparsers.add_parser(
        "review-queue-refresh-worklist",
        help="Apply the ranked review-queue worklist in one shot by recomputing mapping_review buckets and refreshing the persisted rows",
    )
    review_queue_refresh_worklist.add_argument("--status", default="open", choices=["open", "resolved"], help="Review row status to inspect while selecting refresh buckets")
    review_queue_refresh_worklist.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter (currently only mapping_review is supported)")
    review_queue_refresh_worklist.add_argument("--limit", type=int, default=3, help="How many ranked worklist buckets to refresh")
    review_queue_refresh_worklist.add_argument("--per-bucket-limit", type=int, default=20, help="Maximum number of matching rows to refresh per selected bucket (use 0 for all)")
    review_queue_refresh_worklist.add_argument("--mapping-limit", type=int, default=5, help="How many MAL candidates to keep per refreshed series")
    review_queue_refresh_worklist.add_argument("--title-cluster", default=None, help="Optional existing title-cluster scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--decision", default=None, help="Optional existing decision scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--reason", default=None, help="Optional existing reason scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--fix-strategy", default=None, help="Optional existing fix-strategy scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--cluster-strategy", default=None, help="Optional existing combined cluster/fix-strategy scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--reason-family", default=None, help="Optional existing reason-family scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--fix-strategy-family", default=None, help="Optional existing fix-strategy-family scope to preserve while refreshing the worklist")
    review_queue_refresh_worklist.add_argument("--cluster-strategy-family", default=None, help="Optional existing combined cluster/fix-strategy-family scope to preserve while refreshing the worklist")
    resolve_review_queue = subparsers.add_parser(
        "resolve-review-queue",
        help="Mark matching open review_queue rows as resolved after triage",
    )
    resolve_review_queue.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    resolve_review_queue.add_argument("--limit", type=int, default=20, help="Maximum number of matching open rows to resolve (use 0 for all)")
    resolve_review_queue.add_argument("--title-cluster", default=None, help="Only resolve rows whose normalized title cluster matches this value")
    resolve_review_queue.add_argument("--decision", default=None, help="Only resolve rows whose payload decision exactly matches this value")
    resolve_review_queue.add_argument("--reason", default=None, help="Only resolve rows whose payload reasons include this value")
    resolve_review_queue.add_argument("--fix-strategy", default=None, help="Only resolve rows whose decision+reasons strategy exactly matches this value")
    resolve_review_queue.add_argument("--cluster-strategy", default=None, help="Only resolve rows whose combined franchise/fix-strategy bucket exactly matches this value")
    resolve_review_queue.add_argument("--reason-family", default=None, help="Only resolve rows whose payload reasons include this normalized family")
    resolve_review_queue.add_argument("--fix-strategy-family", default=None, help="Only resolve rows whose normalized decision+reason-family strategy exactly matches this value")
    resolve_review_queue.add_argument("--cluster-strategy-family", default=None, help="Only resolve rows whose combined franchise/fix-strategy-family bucket exactly matches this value")
    reopen_review_queue = subparsers.add_parser(
        "reopen-review-queue",
        help="Move matching resolved review_queue rows back to open when residue was cleared too aggressively or needs another pass",
    )
    reopen_review_queue.add_argument("--issue-type", default=None, choices=["mapping_review", "sync_review"], help="Optional issue type filter")
    reopen_review_queue.add_argument("--limit", type=int, default=20, help="Maximum number of matching resolved rows to reopen (use 0 for all)")
    reopen_review_queue.add_argument("--title-cluster", default=None, help="Only reopen rows whose normalized title cluster matches this value")
    reopen_review_queue.add_argument("--decision", default=None, help="Only reopen rows whose payload decision exactly matches this value")
    reopen_review_queue.add_argument("--reason", default=None, help="Only reopen rows whose payload reasons include this value")
    reopen_review_queue.add_argument("--fix-strategy", default=None, help="Only reopen rows whose decision+reasons strategy exactly matches this value")
    reopen_review_queue.add_argument("--cluster-strategy", default=None, help="Only reopen rows whose combined franchise/fix-strategy bucket exactly matches this value")
    reopen_review_queue.add_argument("--reason-family", default=None, help="Only reopen rows whose payload reasons include this normalized family")
    reopen_review_queue.add_argument("--fix-strategy-family", default=None, help="Only reopen rows whose normalized decision+reason-family strategy exactly matches this value")
    reopen_review_queue.add_argument("--cluster-strategy-family", default=None, help="Only reopen rows whose combined franchise/fix-strategy-family bucket exactly matches this value")
    apply_sync = subparsers.add_parser("apply-sync", help="Guarded MAL executor that only operates on approved mappings and forward-safe proposals")
    apply_sync.add_argument("--limit", type=int, default=20, help="How many ingested series to inspect")
    apply_sync.add_argument("--mapping-limit", type=int, default=5, help="Reserved for parity with dry-run planning")
    apply_sync.add_argument(
        "--exact-approved-only",
        action="store_true",
        help="Only operate on exact approved mappings (currently auto_exact/user_exact)",
    )
    apply_sync.add_argument("--execute", action="store_true", help="Actually write MAL updates; otherwise revalidate and print what would be applied")
    recommend = subparsers.add_parser(
        "recommend",
        help="Generate local recommendations from the ingested provider dataset (grouped by category by default)",
    )
    recommend.add_argument("--limit", type=int, default=20, help="How many recommendations to emit (use 0 for all)")
    recommend.add_argument("--flat", action="store_true", help="Emit the legacy single flat JSON list instead of grouped sections")
    recommend_refresh = subparsers.add_parser(
        "recommend-refresh-metadata",
        help="Refresh MAL metadata/relation cache for mapped anime so recommendations can use richer continuation evidence",
    )
    recommend_refresh.add_argument("--limit", type=int, default=0, help="How many mapped MAL anime to refresh (use 0 for all)")
    recommend_refresh.add_argument(
        "--include-discovery-targets",
        action="store_true",
        help="Also hydrate minimal metadata for top recommended target anime so discovery suppression/ranking can use MAL list state and metadata",
    )
    recommend_refresh.add_argument(
        "--discovery-target-limit",
        type=int,
        default=0,
        help="How many discovered target anime to hydrate when --include-discovery-targets is used (use 0 for all discovered targets)",
    )
    subparsers.add_parser("sync", help="Reserved for future sync orchestration")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.command == "init":
        return _cmd_init(args.project_root)
    if args.command == "status":
        return _cmd_status(args.project_root)
    if args.command == "install-service":
        return _cmd_install_service(args.project_root, start_now=not args.no_start)
    if args.command == "uninstall-service":
        return _cmd_uninstall_service(stop_now=not args.no_stop)
    if args.command == "start-service":
        return _cmd_start_service()
    if args.command == "stop-service":
        return _cmd_stop_service()
    if args.command == "restart-service":
        return _cmd_restart_service()
    if args.command == "service-status":
        return _cmd_service_status(args.project_root, args.format)
    if args.command == "service-run":
        return _cmd_service_run(args.project_root)
    if args.command == "service-run-once":
        return _cmd_service_run_once(args.project_root)
    if args.command == "bootstrap-audit":
        return _cmd_bootstrap_audit(args.project_root, args.summary)
    if args.command == "health-check":
        return _cmd_health_check(
            args.project_root,
            args.stale_hours,
            args.strict,
            args.review_issue_type,
            args.review_worklist_limit,
            args.format,
            args.mapping_coverage_threshold,
            args.maintenance_review_limit,
        )
    if args.command == "mal-auth-url":
        return _cmd_mal_auth_url(args.project_root, args.json)
    if args.command == "mal-auth-login":
        return _cmd_mal_auth_login(args.project_root, args.timeout_seconds, verify_whoami=not args.no_verify)
    if args.command == "mal-refresh":
        return _cmd_mal_refresh(args.project_root, verify_whoami=not args.no_verify)
    if args.command == "mal-whoami":
        return _cmd_mal_whoami(args.project_root)
    if args.command == "provider-auth-login":
        return _cmd_provider_auth_login(args.project_root, args.provider, args.profile, args.no_verify)
    if args.command == "provider-fetch-snapshot":
        return _cmd_provider_fetch_snapshot(args.project_root, args.provider, args.profile, args.out, args.ingest, args.full_refresh)
    if args.command == "crunchyroll-auth-login":
        return _cmd_crunchyroll_auth_login(args.project_root, args.profile, args.no_verify)
    if args.command == "crunchyroll-fetch-snapshot":
        return _cmd_crunchyroll_fetch_snapshot(args.project_root, args.profile, args.out, args.ingest, args.full_refresh)
    if args.command == "validate-snapshot":
        return _cmd_validate_snapshot(args.project_root, args.snapshot)
    if args.command == "ingest-snapshot":
        return _cmd_ingest_snapshot(args.project_root, args.snapshot)
    if args.command == "map-series":
        return _cmd_map_series(args.project_root, args.limit, args.mapping_limit)
    if args.command == "review-mappings":
        return _cmd_review_mappings(args.project_root, args.limit, args.mapping_limit, args.persist_review_queue)
    if args.command == "refresh-mapping-review-queue":
        return _cmd_refresh_mapping_review_queue(
            args.project_root,
            args.provider_series_id,
            args.mapping_limit,
            include_all_open=args.all_open,
            title_cluster=args.title_cluster,
            fix_strategy=args.fix_strategy,
            cluster_strategy=args.cluster_strategy,
            decision=args.decision,
            reason=args.reason,
            reason_family=args.reason_family,
            fix_strategy_family=args.fix_strategy_family,
            cluster_strategy_family=args.cluster_strategy_family,
        )
    if args.command == "list-mappings":
        return _cmd_list_mappings(args.project_root, args.approved_only)
    if args.command == "approve-mapping":
        return _cmd_approve_mapping(
            args.project_root,
            args.provider_series_id,
            args.mal_anime_id,
            args.confidence,
            args.notes,
            args.exact,
        )
    if args.command == "dry-run-sync":
        return _cmd_dry_run_sync(
            args.project_root,
            args.provider,
            args.limit,
            args.mapping_limit,
            args.approved_mappings_only,
            args.exact_approved_only,
            args.persist_review_queue,
        )
    if args.command == "list-review-queue":
        return _cmd_list_review_queue(
            args.project_root,
            args.status,
            args.issue_type,
            args.summary,
            args.limit,
            args.provider_series_id,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "review-queue-next":
        return _cmd_review_queue_next(
            args.project_root,
            args.status,
            args.issue_type,
            args.bucket,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "review-queue-worklist":
        return _cmd_review_queue_worklist(
            args.project_root,
            args.status,
            args.issue_type,
            args.limit,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "review-queue-apply-worklist":
        return _cmd_review_queue_apply_worklist(
            args.project_root,
            args.status,
            args.issue_type,
            args.limit,
            args.per_bucket_limit,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "review-queue-refresh-worklist":
        return _cmd_review_queue_refresh_worklist(
            args.project_root,
            args.status,
            args.issue_type,
            args.limit,
            args.per_bucket_limit,
            args.mapping_limit,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "resolve-review-queue":
        return _cmd_resolve_review_queue(
            args.project_root,
            args.issue_type,
            args.limit,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "reopen-review-queue":
        return _cmd_reopen_review_queue(
            args.project_root,
            args.issue_type,
            args.limit,
            args.title_cluster,
            args.fix_strategy,
            args.cluster_strategy,
            args.decision,
            args.reason,
            args.reason_family,
            args.fix_strategy_family,
            args.cluster_strategy_family,
        )
    if args.command == "apply-sync":
        return _cmd_apply_sync(args.project_root, args.limit, args.mapping_limit, args.exact_approved_only, args.execute)
    if args.command == "recommend":
        return _cmd_recommend(args.project_root, args.limit, args.flat)
    if args.command == "recommend-refresh-metadata":
        return _cmd_recommend_refresh_metadata(
            args.project_root,
            args.limit,
            args.include_discovery_targets,
            args.discovery_target_limit,
        )
    if args.command == "sync":
        return _cmd_sync(args.project_root)
    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
