"""Autonomous, resumable orchestration for agent hosts."""

from __future__ import annotations

import json
from pathlib import Path
import re
import threading
from typing import Any, Callable
from urllib.request import urlopen
import uuid

from .config import (
    STATE_NAME,
    ConfigError,
    atomic_write_json,
    default_config_path,
    load_config,
    load_json,
    normalized,
    now_iso,
)
from .doctor import diagnose
from .lifecycle import initialize
from .pipeline import build, render, scan, validate
from .result import make_result
from .server import create_server


WORKFLOW_STAGES = (
    "DISCOVER",
    "DIAGNOSE",
    "PLAN",
    "BOOTSTRAP",
    "SCAN",
    "BUILD",
    "VALIDATE",
    "GENERATE_HTML",
    "START",
    "VERIFY",
    "READY",
)

VALIDATED_HOST_PATTERN = re.compile(
    r"^[A-Za-z][A-Za-z0-9._-]*/[A-Za-z0-9][A-Za-z0-9._+-]*$"
)
FORBIDDEN_HOST_PRODUCTS = {
    "darwin",
    "linux",
    "mac",
    "macos",
    "osx",
    "windows",
    "windows-powershell",
}


def validated_host_gate(validated_host: str | None) -> tuple[dict[str, Any], int] | None:
    """Fail closed when a caller supplies an invalid agent-host identity.

    This helper is intentionally public so every CLI boundary can enforce the
    same trust rule before forwarding caller-controlled input to the workflow.
    """

    host_product = validated_host.split("/", 1)[0].lower() if validated_host and "/" in validated_host else ""
    if validated_host is None or (
        VALIDATED_HOST_PATTERN.fullmatch(validated_host) is not None
        and host_product not in FORBIDDEN_HOST_PRODUCTS
    ):
        return None

    cause = make_result(
        status="error",
        code="VALIDATED_HOST_INVALID",
        message=(
            "--validated-host must be Product/version from the agent host CLI "
            "(for example OpenClaw/2026.6.11); OS, kernel, device, user, and account identities are invalid."
        ),
        next_actions=[{"action": "probe_agent_cli_version_and_retry"}],
    )
    return _fail(stage="DISCOVER", cause=cause, stages=[], artifacts=[], config=None)


def _deduplicate(values: list[str]) -> list[str]:
    return list(dict.fromkeys(values))


def _checkpoint(config: dict[str, Any], stage: str, status: str, details: dict[str, Any]) -> Path:
    state_path = normalized(config["paths"]["internal"]) / STATE_NAME
    state = load_json(state_path)
    completed = [str(value) for value in state.get("completed_stages", [])]
    if stage not in completed and status == "ok":
        completed.append(stage)
    state.update(
        {
            "updated_at": now_iso(),
            "status": "ready" if stage == "READY" and status == "ok" else status,
            "stage": stage,
            "completed_stages": completed,
            "workflow": details,
        }
    )
    atomic_write_json(state_path, state)
    return state_path


def _stage_result(stage: str, payload: dict[str, Any], skipped: bool = False) -> dict[str, Any]:
    return {
        "stage": stage,
        "status": "skipped" if skipped else payload["status"],
        "code": "CHECKPOINT_REUSED" if skipped else payload["code"],
    }


def _pause(
    *,
    stage: str,
    cause: dict[str, Any],
    stages: list[dict[str, Any]],
    artifacts: list[str],
    config: dict[str, Any] | None,
) -> tuple[dict[str, Any], int]:
    details = {
        "workflow_status": "paused",
        "paused_at": stage,
        "stages": stages,
        "cause_code": cause["code"],
    }
    if config is not None:
        state_path = _checkpoint(config, stage, "paused", details)
        artifacts.append(str(state_path))
    return make_result(
        status="needs_user_input",
        code="AUTO_RUN_PAUSED",
        message=f"Autonomous workflow paused at {stage}: {cause['message']}",
        artifacts=_deduplicate(artifacts + list(cause.get("artifacts", []))),
        next_actions=[{"action": "resolve_gate_then_resume", "command": "run --resume"}],
        needs_user_input=list(cause.get("needs_user_input", [])),
        data={**details, "cause": cause},
    ), 3


def _fail(
    *,
    stage: str,
    cause: dict[str, Any],
    stages: list[dict[str, Any]],
    artifacts: list[str],
    config: dict[str, Any] | None,
) -> tuple[dict[str, Any], int]:
    details = {
        "workflow_status": "error",
        "failed_at": stage,
        "stages": stages,
        "cause_code": cause["code"],
    }
    if config is not None:
        state_path = _checkpoint(config, stage, "error", details)
        artifacts.append(str(state_path))
    return make_result(
        status="error",
        code="AUTO_RUN_FAILED",
        message=f"Autonomous workflow failed at {stage}: {cause['message']}",
        artifacts=_deduplicate(artifacts + list(cause.get("artifacts", []))),
        next_actions=[{"action": "inspect_cause_then_resume", "command": "run --resume"}],
        data={**details, "cause": cause},
    ), 1


def verify_loopback(config: dict[str, Any]) -> tuple[dict[str, Any], int]:
    """Start an ephemeral read-only service, verify it, then stop it."""

    dashboard = normalized(config["paths"]["dashboard"])
    instance_id = str(uuid.uuid4())
    server = None
    try:
        server = create_server(dashboard=dashboard, host="127.0.0.1", port=0, instance_id=instance_id)
        port = int(server.server_address[1])
        thread = threading.Thread(target=server.serve_forever, kwargs={"poll_interval": 0.05}, daemon=True)
        thread.start()
        health_url = f"http://127.0.0.1:{port}/healthz"
        data_url = f"http://127.0.0.1:{port}/api/data"
        last_error: Exception | None = None
        for _attempt in range(2):
            try:
                with urlopen(health_url, timeout=1.0) as response:  # noqa: S310 - fixed loopback host
                    health = json.loads(response.read().decode("utf-8"))
                with urlopen(data_url, timeout=1.0) as response:  # noqa: S310 - fixed loopback host
                    dashboard_data = json.loads(response.read().decode("utf-8"))
                if health.get("instance_id") != instance_id or health.get("read_only") is not True:
                    raise ValueError("Loopback health response did not match the temporary service instance.")
                if dashboard_data.get("schema_version") != 1:
                    raise ValueError("Dashboard API returned an unsupported schema version.")
                return make_result(
                    status="ok",
                    code="LOOPBACK_VERIFIED",
                    message="The generated dashboard passed an ephemeral read-only loopback health and data check.",
                    artifacts=[str(dashboard / "index.html"), str(dashboard / "data.json")],
                    data={
                        "service_persisted": False,
                        "service_verified": True,
                        "read_only": True,
                        "health_status": health.get("status"),
                    },
                ), 0
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                last_error = exc
        raise RuntimeError(str(last_error or "unknown loopback verification failure"))
    except (OSError, RuntimeError, ValueError) as exc:
        return make_result(
            status="error",
            code="LOOPBACK_VERIFY_FAILED",
            message=str(exc),
            next_actions=[{"action": "inspect_dashboard_and_port"}],
        ), 1
    finally:
        if server is not None:
            server.shutdown()
            server.server_close()


def run_auto(
    *,
    workspace: Path,
    sources: list[Path],
    requested_config: Path | None,
    mode: str,
    privacy_mode: str,
    preferred_port: int,
    max_vault_depth: int,
    resume: bool,
    validated_host: str | None,
    stage_hook: Callable[[str], None] | None = None,
) -> tuple[dict[str, Any], int]:
    """Run every safe stage and stop only at an explicit gate or error."""

    workspace = normalized(workspace)
    sources = [normalized(source) for source in sources]
    artifacts: list[str] = []
    stages: list[dict[str, Any]] = []
    stage_payloads: dict[str, dict[str, Any]] = {}
    config: dict[str, Any] | None = None
    completed_before: list[str] = []
    resumed_from: str | None = None
    workspace_created = False

    host_gate = validated_host_gate(validated_host)
    if host_gate is not None:
        return host_gate

    if not workspace.exists():
        try:
            workspace.mkdir(parents=True, exist_ok=False)
            workspace_created = True
        except OSError as exc:
            cause = make_result(
                status="needs_user_input",
                code="WORKSPACE_CREATE_FAILED",
                message=f"The explicitly selected workspace could not be created: {exc}",
                needs_user_input=[
                    {
                        "gate": "workspace_write_access",
                        "path": str(workspace),
                        "requested_action": "select_or_authorize_workspace",
                    }
                ],
            )
            return _pause(stage="DISCOVER", cause=cause, stages=stages, artifacts=artifacts, config=None)

    config_path = default_config_path(workspace) if requested_config is None else normalized(requested_config)

    if config_path.is_file():
        try:
            config = load_config(config_path, expected_workspace=workspace)
            state = load_json(normalized(config["paths"]["internal"]) / STATE_NAME)
            completed_before = [str(value) for value in state.get("completed_stages", [])]
            resumed_from = str(state.get("stage", "BOOTSTRAP")) if resume else None
            configured_sources = [normalized(entry["root"]) for entry in config["sources"]]
            if sources and sources != configured_sources:
                cause = make_result(
                    status="needs_user_input",
                    code="SOURCE_SCOPE_CHANGE_REQUIRED",
                    message="The requested sources differ from the initialized source boundary.",
                    needs_user_input=[
                        {
                            "gate": "source_scope",
                            "configured": [str(path) for path in configured_sources],
                            "requested": [str(path) for path in sources],
                            "requested_action": "confirm_reconfiguration_or_use_existing_scope",
                        }
                    ],
                )
                return _pause(
                    stage="DISCOVER", cause=cause, stages=stages, artifacts=artifacts, config=config
                )
            sources = configured_sources
        except (ConfigError, OSError, KeyError, TypeError) as exc:
            cause = make_result(status="error", code="INVALID_RUNTIME_STATE", message=str(exc))
            return _fail(stage="DISCOVER", cause=cause, stages=stages, artifacts=artifacts, config=config)

    def execute(stage: str, operation: Callable[[], tuple[dict[str, Any], int]]) -> bool | tuple[dict[str, Any], int]:
        if stage_hook:
            stage_hook(stage)
        if resume and config is not None and stage in completed_before and stage not in {
            "DISCOVER",
            "DIAGNOSE",
            "START",
        }:
            stages.append(_stage_result(stage, {}, skipped=True))
            return True
        payload, exit_code = operation()
        stage_payloads[stage] = payload
        stages.append(_stage_result(stage, payload))
        artifacts.extend(str(value) for value in payload.get("artifacts", []))
        if exit_code == 0:
            return True
        if payload.get("status") == "needs_user_input" or exit_code == 3:
            return _pause(stage=stage, cause=payload, stages=stages, artifacts=artifacts, config=config)
        return _fail(stage=stage, cause=payload, stages=stages, artifacts=artifacts, config=config)

    stages.append(
        {
            "stage": "DISCOVER",
            "status": "ok",
            "code": "WORKSPACE_CREATED" if workspace_created else "BOUNDARY_DISCOVERED",
        }
    )
    diagnosed = execute(
        "DIAGNOSE",
        lambda: diagnose(
            workspace=workspace,
            sources=sources or [workspace],
            preferred_port=preferred_port,
            max_vault_depth=max_vault_depth,
        ),
    )
    if diagnosed is not True:
        return diagnosed
    stages.append({"stage": "PLAN", "status": "ok", "code": "SAFE_DEFAULT_PLAN"})

    if config is None:
        initialized = execute(
            "BOOTSTRAP",
            lambda: initialize(
                workspace=workspace,
                sources=sources or [workspace],
                requested_config=requested_config,
                mode=mode,
                privacy_mode=privacy_mode,
                preferred_port=preferred_port,
                max_vault_depth=max_vault_depth,
            ),
        )
        if initialized is not True:
            return initialized
        try:
            config = load_config(config_path, expected_workspace=workspace)
        except ConfigError as exc:
            cause = make_result(status="error", code="BOOTSTRAP_CONFIG_MISSING", message=str(exc))
            return _fail(stage="BOOTSTRAP", cause=cause, stages=stages, artifacts=artifacts, config=None)
    else:
        stages.append({"stage": "BOOTSTRAP", "status": "skipped", "code": "ALREADY_INITIALIZED"})

    operations: list[tuple[str, Callable[[], tuple[dict[str, Any], int]]]] = [
        ("SCAN", lambda: scan(workspace=workspace, requested_config=requested_config)),
        ("BUILD", lambda: build(workspace=workspace, requested_config=requested_config)),
        ("VALIDATE", lambda: validate(workspace=workspace, requested_config=requested_config)),
        ("GENERATE_HTML", lambda: render(workspace=workspace, requested_config=requested_config)),
        ("START", lambda: verify_loopback(config)),
    ]
    for stage, operation in operations:
        outcome = execute(stage, operation)
        if outcome is not True:
            return outcome

    stages.append({"stage": "VERIFY", "status": "ok", "code": "LOCAL_VALIDATION_COMPLETE"})
    stages.append({"stage": "READY", "status": "ok", "code": "WORKBENCH_READY"})
    details = {
        "workflow_status": "ready",
        "stages": stages,
        "resumed": resume,
        "resumed_from": resumed_from,
        "validated_host": validated_host,
    }
    state_path = _checkpoint(config, "READY", "ok", details)
    artifacts.append(str(state_path))
    dashboard = normalized(config["paths"]["dashboard"])
    knowledge = normalized(config["paths"]["knowledge"])
    source_roots = [str(normalized(entry["root"])) for entry in config["sources"]]
    excluded = 0
    changes: dict[str, Any] = {}
    data_path = dashboard / "data.json"
    if data_path.is_file():
        excluded = int(load_json(data_path).get("summary", {}).get("excluded_sensitive", 0))
    scan_payload = stage_payloads.get("SCAN", {})
    if isinstance(scan_payload.get("data"), dict):
        candidate_changes = scan_payload["data"].get("changes", {})
        if isinstance(candidate_changes, dict):
            changes = candidate_changes
    return make_result(
        status="ok",
        code="AUTO_RUN_READY",
        message="The AI knowledge workbench was autonomously built and locally verified.",
        artifacts=_deduplicate(artifacts + [str(knowledge), str(dashboard / "index.html")]),
        next_actions=[
            {"action": "open_dashboard_if_requested", "path": str(dashboard / "index.html")},
            {
                "action": "edit_configured_source_then_ask_ai_to_refresh",
                "source_roots": source_roots,
                "manual_command_required": False,
            },
        ],
        data={
            **details,
            "built": True,
            "locally_validated": True,
            "dashboard_generated": True,
            "service_started": False,
            "service_verified": stage_payloads.get("START", {}).get("code") == "LOOPBACK_VERIFIED",
            "service_persisted": False,
            "update_mode": config.get("update", {}).get("mode", "manual"),
            "privacy_mode": config["privacy_mode"],
            "content_access": config.get("content_access", "unknown"),
            "model_transport": config.get("model_transport", "none"),
            "source_files_changed": False,
            "dashboard_body_embedded": False,
            "excluded_sensitive_records": excluded,
            "changes": changes,
            "unresolved_gates": [],
            "report_contract": {
                "show_manual_commands": False,
                "original_source_notes_changed": False,
                "source_truth": "configured_source_roots",
                "source_roots": source_roots,
                "derived_directories": [str(knowledge), str(dashboard)],
                "derived_directories_are_inputs": False,
                "refresh_instruction": "Edit a configured source, then ask the AI to refresh the workbench.",
            },
        },
    ), 0
