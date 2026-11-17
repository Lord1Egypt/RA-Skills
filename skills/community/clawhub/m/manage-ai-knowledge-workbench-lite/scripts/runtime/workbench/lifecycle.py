"""Safe initialization, status, stop, and uninstall operations."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import signal
import time
from typing import Any
from urllib.error import URLError
from urllib.request import urlopen
import uuid

from .config import (
    CONFIG_NAME,
    DASHBOARD_DIR,
    INTERNAL_DIR,
    KNOWLEDGE_DIR,
    KNOWLEDGE_SUBDIRS,
    MANIFEST_REL,
    PRODUCT_ID,
    STATE_NAME,
    ConfigError,
    atomic_write_json,
    default_config_path,
    is_within,
    load_config,
    load_json,
    make_config,
    normalized,
    now_iso,
    relative_to_workspace,
    reserved_paths,
    resolve_config_path,
)
from .doctor import diagnose
from .result import make_result


VALID_MODES = {"auto", "markdown", "obsidian", "hybrid"}
VALID_PRIVACY_MODES = {"metadata-only", "cloud-assisted", "local-model"}


def _config_for_lookup(workspace: Path, requested: Path | None) -> Path:
    workspace = normalized(workspace)
    if requested is None:
        return default_config_path(workspace)
    requested = normalized(requested)
    if not is_within(workspace, requested):
        raise ConfigError("Config path must stay inside the selected workspace.")
    return requested


def _process_exists(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError):
        return False
    return True


def watch_status(state: dict[str, Any]) -> dict[str, Any]:
    """Inspect foreground-watch state without importing the optional watcher module."""
    watch = state.get("watch")
    if not isinstance(watch, dict):
        return {"status": "not_configured", "persistent": False}
    result = dict(watch)
    pid = result.get("pid")
    if result.get("status") == "running" and isinstance(pid, int) and not _process_exists(pid):
        result["status"] = "stale"
        result["recoverable"] = True
    return result


def _output_conflicts(workspace: Path, config_path: Path) -> list[str]:
    paths = reserved_paths(workspace)
    if config_path.exists():
        return []
    candidates = [paths["internal"], paths["knowledge"], paths["dashboard"]]
    return [str(path) for path in candidates if path.exists()]


def initialize(
    *,
    workspace: Path,
    sources: list[Path],
    requested_config: Path | None,
    mode: str,
    privacy_mode: str,
    preferred_port: int,
    max_vault_depth: int,
) -> tuple[dict[str, Any], int]:
    workspace = normalized(workspace)
    sources = [normalized(path) for path in sources]
    if mode not in VALID_MODES:
        return make_result(
            status="error",
            code="INVALID_MODE",
            message=f"Unsupported mode: {mode}",
        ), 1
    if privacy_mode not in VALID_PRIVACY_MODES:
        return make_result(
            status="error",
            code="INVALID_PRIVACY_MODE",
            message=f"Unsupported privacy mode: {privacy_mode}",
        ), 1
    if privacy_mode != "metadata-only":
        return make_result(
            status="needs_user_input",
            code="PRIVACY_MODE_AUTHORIZATION_REQUIRED",
            message="Content-processing modes require explicit authorization and are not enabled by bootstrap.",
            needs_user_input=[
                {
                    "gate": "content_processing",
                    "requested_mode": privacy_mode,
                    "requested_action": "authorize_scope_and_model_transport",
                }
            ],
            next_actions=[{"action": "use_metadata_only_or_authorize_later"}],
        ), 3

    try:
        config_path = resolve_config_path(workspace, requested_config)
    except ConfigError as exc:
        return make_result(status="error", code="UNSAFE_CONFIG_PATH", message=str(exc)), 1

    if config_path.exists():
        try:
            config = load_config(config_path, expected_workspace=workspace)
        except ConfigError as exc:
            return make_result(
                status="error",
                code="INVALID_EXISTING_CONFIG",
                message=str(exc),
                artifacts=[str(config_path)],
            ), 1
        return make_result(
            status="ok",
            code="ALREADY_INITIALIZED",
            message="The workspace is already initialized; no files were changed.",
            artifacts=[str(config_path)],
            next_actions=[{"action": "inspect_status", "command": "status"}],
            data={"config": config},
        ), 0

    conflicts = _output_conflicts(workspace, config_path)
    if conflicts:
        return make_result(
            status="needs_user_input",
            code="OUTPUT_CONFLICT",
            message="Reserved output paths already exist without a valid workbench manifest.",
            needs_user_input=[
                {
                    "gate": "output_paths",
                    "reason": "Unknown existing files must not be overwritten.",
                    "paths": conflicts,
                    "requested_action": "select_another_workspace_or_review_paths",
                }
            ],
            next_actions=[{"action": "resolve_output_conflict_then_resume", "command": "init"}],
        ), 3

    doctor_result, doctor_exit = diagnose(
        workspace=workspace,
        sources=sources,
        preferred_port=preferred_port,
        max_vault_depth=max_vault_depth,
    )
    if doctor_exit != 0:
        return doctor_result, doctor_exit

    doctor_data = doctor_result["data"]
    selected_mode = doctor_data["recommended_mode"] if mode == "auto" else mode
    vault_count = doctor_data["obsidian"]["vault_count"]
    if selected_mode == "obsidian" and vault_count == 0:
        return make_result(
            status="needs_user_input",
            code="OBSIDIAN_VAULT_REQUIRED",
            message="Obsidian mode was requested, but no vault was found in the bounded source roots.",
            needs_user_input=[
                {
                    "gate": "vault_selection",
                    "requested_action": "select_vault_or_use_markdown_mode",
                }
            ],
        ), 3

    paths = reserved_paths(workspace)
    source_output_roots = {paths["knowledge"], paths["dashboard"], paths["internal"]}
    if any(source in source_output_roots for source in sources):
        return make_result(
            status="error",
            code="UNSAFE_SOURCE_PATH",
            message="A source directory cannot be one of the reserved generated-output directories.",
        ), 1

    directories = [
        paths["internal"],
        paths["internal"] / "manifests",
        paths["cache"],
        paths["logs"],
        paths["knowledge"],
        *(paths["knowledge"] / name for name in KNOWLEDGE_SUBDIRS),
        paths["dashboard"],
        paths["dashboard_assets"],
    ]
    created_dirs: list[Path] = []
    created_files: list[Path] = []
    try:
        for directory in directories:
            if not directory.exists():
                directory.mkdir(parents=True, exist_ok=False)
                created_dirs.append(directory)

        config = make_config(
            workspace=workspace,
            sources=sources,
            mode=selected_mode,
            privacy_mode=privacy_mode,
            port=int(doctor_data["server"]["selected_port"]),
        )
        state = {
            "product": PRODUCT_ID,
            "schema_version": 1,
            "run_id": str(uuid.uuid4()),
            "updated_at": now_iso(),
            "status": "initialized",
            "stage": "BOOTSTRAP",
            "completed_stages": ["DISCOVER", "DIAGNOSE", "PLAN", "BOOTSTRAP"],
            "service": {"status": "stopped", "pid": None},
        }
        manifest_path = paths["manifest"]
        manifest = {
            "product": PRODUCT_ID,
            "schema_version": 1,
            "created_at": now_iso(),
            "workspace": str(workspace),
            "generated_dirs": relative_to_workspace(workspace, directories),
            "generated_files": relative_to_workspace(
                workspace,
                [config_path, paths["state"], manifest_path],
            ),
            "preserve_by_default": [KNOWLEDGE_DIR, DASHBOARD_DIR],
        }

        atomic_write_json(config_path, config)
        created_files.append(config_path)
        atomic_write_json(paths["state"], state)
        created_files.append(paths["state"])
        atomic_write_json(manifest_path, manifest)
        created_files.append(manifest_path)
    except Exception as exc:
        for path in reversed(created_files):
            path.unlink(missing_ok=True)
        for directory in reversed(created_dirs):
            try:
                directory.rmdir()
            except OSError:
                pass
        return make_result(
            status="error",
            code="INITIALIZATION_FAILED",
            message=f"Initialization failed and newly created empty paths were rolled back: {exc}",
        ), 1

    return make_result(
        status="ok",
        code="INITIALIZED",
        message="The local workbench was initialized without installing software or changing source files.",
        artifacts=[str(path) for path in created_files] + [str(paths["knowledge"]), str(paths["dashboard"])],
        next_actions=[{"action": "inspect_status", "command": "status"}],
        data={
            "mode": selected_mode,
            "privacy_mode": privacy_mode,
            "config": str(config_path),
            "doctor": doctor_data,
        },
    ), 0


def status(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    workspace = normalized(workspace)
    try:
        config_path = _config_for_lookup(workspace, requested_config)
    except ConfigError as exc:
        return make_result(status="error", code="UNSAFE_CONFIG_PATH", message=str(exc)), 1
    if not config_path.is_file():
        return make_result(
            status="not_initialized",
            code="NOT_INITIALIZED",
            message="No workbench config was found in the selected workspace.",
            next_actions=[{"action": "initialize", "command": "init"}],
        ), 1
    try:
        config = load_config(config_path, expected_workspace=workspace)
        state_path = Path(config["paths"]["internal"]) / STATE_NAME
        state = load_json(state_path)
    except (ConfigError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="INVALID_RUNTIME_STATE",
            message=str(exc),
            artifacts=[str(config_path)],
        ), 1

    path_status = {
        key: {"path": str(value), "exists": value.exists()}
        for key, value in {
            "config": config_path,
            "internal": Path(config["paths"]["internal"]),
            "knowledge": Path(config["paths"]["knowledge"]),
            "dashboard": Path(config["paths"]["dashboard"]),
        }.items()
    }
    service = state.get("service") if isinstance(state.get("service"), dict) else {"status": "unknown"}
    background_state = Path(config["paths"]["internal"]) / "background.json"
    background_data: dict[str, Any] = {
        "installed": False,
        "active": False,
        "dashboard_update_mode": config.get("update", {}).get("mode", "manual"),
    }
    if background_state.is_file():
        try:
            from .background import status as background_status
        except ModuleNotFoundError as exc:
            if exc.name != f"{__package__}.background":
                raise
            background_data = {
                "installed": "unknown",
                "active": "unknown",
                "state_present": True,
                "inspection": "module_not_included",
            }
        else:
            background_payload, _background_exit = background_status(
                workspace=workspace,
                requested_config=requested_config,
            )
            background_data = background_payload.get("data", background_data)

    return make_result(
        status="ok",
        code="STATUS_OK",
        message="Workbench runtime state was loaded.",
        artifacts=[str(config_path), str(state_path)],
        next_actions=[{"action": "build", "command": "scan"}],
        data={
            "config": config,
            "state": state,
            "paths": path_status,
            "service": service,
            "watch": watch_status(state),
            "background": background_data,
        },
    ), 0


def stop(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    current, exit_code = status(workspace=workspace, requested_config=requested_config)
    if exit_code != 0:
        return current, exit_code
    service = current["data"].get("service", {})
    if service.get("status") != "running" or not service.get("pid"):
        return make_result(
            status="ok",
            code="NO_SERVICE",
            message="No managed workbench service is running; no process was changed.",
            artifacts=current["artifacts"],
            next_actions=[{"action": "inspect_status", "command": "status"}],
            data={"service": service},
        ), 0
    host = str(service.get("host", ""))
    port = service.get("port")
    instance_id = str(service.get("instance_id", ""))
    pid = service.get("pid")
    if host not in {"127.0.0.1", "localhost", "::1"} or not isinstance(port, int) or not isinstance(pid, int):
        return make_result(
            status="needs_user_input",
            code="SERVICE_IDENTITY_UNVERIFIED",
            message="The running-service record is incomplete or not loopback-only; no process was changed.",
            needs_user_input=[{"gate": "process_identity", "requested_action": "inspect_service_state"}],
        ), 3
    url_host = f"[{host}]" if ":" in host else host
    health_url = f"http://{url_host}:{port}/healthz"
    try:
        with urlopen(health_url, timeout=0.75) as response:  # noqa: S310 - loopback URL is validated above
            health = json.loads(response.read().decode("utf-8"))
    except (OSError, URLError, ValueError, json.JSONDecodeError) as exc:
        return make_result(
            status="needs_user_input",
            code="SERVICE_IDENTITY_UNVERIFIED",
            message=f"The recorded loopback service could not be verified; no process was changed: {exc}",
            needs_user_input=[
                {
                    "gate": "process_identity",
                    "pid": pid,
                    "url": health_url,
                    "requested_action": "inspect_service_before_stop",
                }
            ],
        ), 3
    if health.get("instance_id") != instance_id:
        return make_result(
            status="needs_user_input",
            code="SERVICE_IDENTITY_MISMATCH",
            message="The loopback health response did not match the recorded service instance; no process was changed.",
            needs_user_input=[{"gate": "process_identity", "pid": pid, "requested_action": "inspect_service_state"}],
        ), 3
    state = current["data"]["state"]
    state["updated_at"] = now_iso()
    state["service"] = {**service, "status": "stop_requested", "stop_requested_at": now_iso()}
    state_path = Path(current["artifacts"][1])
    atomic_write_json(state_path, state)
    try:
        os.kill(pid, signal.SIGTERM)
    except (OSError, ProcessLookupError) as exc:
        state["service"] = {**service, "status": "running", "stop_error": str(exc)}
        atomic_write_json(state_path, state)
        return make_result(status="error", code="SERVICE_STOP_FAILED", message=str(exc)), 1
    running = True
    for _attempt in range(20):
        try:
            os.kill(pid, 0)
        except (OSError, ProcessLookupError):
            running = False
            break
        time.sleep(0.05)
    latest = load_json(state_path)
    latest_service = latest.get("service", state["service"])
    final_status = str(latest_service.get("status", "stop_requested"))
    return make_result(
        status="ok",
        code="SERVICE_STOPPED" if final_status == "stopped" else "SERVICE_STOP_REQUESTED",
        message="The verified managed loopback service received a stop request.",
        artifacts=[str(state_path)],
        next_actions=[{"action": "inspect_status", "command": "status"}],
        data={"service": latest_service, "identity_verified": True, "process_visible": running},
    ), 0


def _remove_empty_dirs(paths: list[Path]) -> list[str]:
    removed: list[str] = []
    for path in sorted((normalized(path) for path in paths), key=lambda item: len(item.parts), reverse=True):
        try:
            path.rmdir()
        except OSError:
            continue
        removed.append(str(path))
    return removed


def uninstall(
    *,
    workspace: Path,
    requested_config: Path | None,
    remove_outputs: bool,
    confirm_remove_outputs: bool,
) -> tuple[dict[str, Any], int]:
    workspace = normalized(workspace)
    try:
        config_path = _config_for_lookup(workspace, requested_config)
    except ConfigError as exc:
        return make_result(status="error", code="UNSAFE_CONFIG_PATH", message=str(exc)), 1
    if not config_path.is_file():
        return make_result(
            status="ok",
            code="NOT_INSTALLED",
            message="No workbench config exists; no files were changed.",
        ), 0
    try:
        config = load_config(config_path, expected_workspace=workspace)
        internal = normalized(config["paths"]["internal"])
        manifest_path = internal / MANIFEST_REL
        manifest = load_json(manifest_path)
    except (ConfigError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="UNINSTALL_MANIFEST_INVALID",
            message=f"Uninstall stopped because ownership could not be verified: {exc}",
            artifacts=[str(config_path)],
        ), 1
    if manifest.get("product") != PRODUCT_ID or normalized(manifest.get("workspace", "")) != workspace:
        return make_result(
            status="error",
            code="UNINSTALL_OWNERSHIP_MISMATCH",
            message="Uninstall stopped because the manifest does not match this workspace.",
        ), 1

    try:
        runtime_state = load_json(internal / STATE_NAME)
    except ConfigError as exc:
        return make_result(
            status="error",
            code="UNINSTALL_STATE_INVALID",
            message=f"Uninstall stopped because runtime state could not be verified: {exc}",
        ), 1
    service = runtime_state.get("service") if isinstance(runtime_state.get("service"), dict) else {}
    if service.get("status") in {"running", "stop_requested"}:
        return make_result(
            status="needs_user_input",
            code="SERVICE_STOP_REQUIRED",
            message="Stop the managed loopback service before uninstalling runtime metadata.",
            needs_user_input=[{"gate": "running_service", "requested_action": "run_stop_then_uninstall"}],
        ), 3
    watch = watch_status(runtime_state)
    if watch.get("status") == "running":
        return make_result(
            status="needs_user_input",
            code="WATCH_STOP_REQUIRED",
            message="Stop the foreground session watch before uninstalling runtime metadata.",
            needs_user_input=[{"gate": "session_watch", "requested_action": "stop_watch_then_uninstall"}],
        ), 3
    background_state = internal / "background.json"
    if background_state.is_file():
        try:
            from .background import status as background_status
        except ModuleNotFoundError as exc:
            if exc.name != f"{__package__}.background":
                raise
            return make_result(
                status="error",
                code="BACKGROUND_MODULE_UNAVAILABLE",
                message="Uninstall stopped because background state exists but this package cannot verify it.",
                artifacts=[str(background_state)],
            ), 1

        background_payload, background_exit = background_status(
            workspace=workspace,
            requested_config=requested_config,
        )
        if background_exit != 0:
            return make_result(
                status="error",
                code="BACKGROUND_STATE_INVALID",
                message="Uninstall stopped because background adapter ownership could not be verified.",
                data={"background": background_payload},
            ), 1
        if background_payload.get("data", {}).get("installed"):
            return make_result(
                status="needs_user_input",
                code="BACKGROUND_UNINSTALL_REQUIRED",
                message="Stop and uninstall the managed background adapter before removing runtime metadata.",
                needs_user_input=[
                    {
                        "gate": "background_adapter",
                        "active": bool(background_payload["data"].get("active")),
                        "requested_action": "background_stop_and_uninstall_first",
                    }
                ],
            ), 3

    knowledge = normalized(config["paths"]["knowledge"])
    dashboard = normalized(config["paths"]["dashboard"])
    if remove_outputs and not confirm_remove_outputs:
        return make_result(
            status="needs_user_input",
            code="REMOVE_OUTPUTS_CONFIRMATION_REQUIRED",
            message="Removing knowledge or dashboard outputs requires explicit confirmation.",
            needs_user_input=[
                {
                    "gate": "destructive_outputs",
                    "paths": [str(knowledge), str(dashboard)],
                    "requested_action": "rerun_with_confirm_remove_outputs",
                }
            ],
        ), 3

    removed: list[str] = []
    generated_files = [
        workspace / value
        for value in manifest.get("generated_files", [])
        if isinstance(value, str)
    ]
    for generated_file in generated_files:
        generated_file = normalized(generated_file)
        remove_runtime = is_within(internal, generated_file)
        remove_confirmed_output = remove_outputs and (
            is_within(knowledge, generated_file) or is_within(dashboard, generated_file)
        )
        if (remove_runtime or remove_confirmed_output) and generated_file.is_file():
            generated_file.unlink()
            removed.append(str(generated_file))

    cache = internal / "cache"
    logs = internal / "logs"
    for owned_runtime_dir in (cache, logs):
        if owned_runtime_dir.is_dir() and is_within(internal, owned_runtime_dir):
            shutil.rmtree(owned_runtime_dir)
            removed.append(str(owned_runtime_dir))

    for file_path in (internal / STATE_NAME, config_path, manifest_path):
        if file_path.is_file() and is_within(workspace, file_path):
            file_path.unlink()
            removed.append(str(file_path))

    manifest_dirs = [workspace / value for value in manifest.get("generated_dirs", []) if isinstance(value, str)]
    removable_dirs = [path for path in manifest_dirs if is_within(workspace, path)]
    # Reports can be created after initialization and are not guaranteed to be
    # present in the original install manifest. Remove only empty, owned
    # runtime directories; rmdir intentionally fails closed if an unknown file
    # remains.
    removable_dirs.extend([internal / "reports", internal])
    if not remove_outputs:
        removable_dirs = [
            path
            for path in removable_dirs
            if not is_within(knowledge, path) and not is_within(dashboard, path)
        ]
    removed.extend(_remove_empty_dirs(removable_dirs))

    preserved = [path for path in (knowledge, dashboard) if path.exists()]
    if remove_outputs:
        removed.extend(_remove_empty_dirs([knowledge / name for name in KNOWLEDGE_SUBDIRS]))
        removed.extend(_remove_empty_dirs([dashboard / "assets", knowledge, dashboard]))
        preserved = [path for path in (knowledge, dashboard) if path.exists()]

    return make_result(
        status="ok",
        code="UNINSTALLED",
        message="Workbench runtime metadata was removed. Knowledge and dashboard outputs were preserved unless explicitly confirmed and empty.",
        artifacts=removed,
        next_actions=[{"action": "review_preserved_paths", "paths": [str(path) for path in preserved]}],
        data={
            "removed": removed,
            "preserved": [str(path) for path in preserved],
            "source_files_changed": False,
        },
    ), 0
