"""P3 scan, build, and validation command implementations."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builder import atomic_write_text, build_knowledge_pages
from .config import (
    STATE_NAME,
    ConfigError,
    atomic_write_json,
    default_config_path,
    load_config,
    load_json,
    normalized,
    now_iso,
    resolve_config_path,
)
from .index import diff_records, load_index, write_index
from .manifest import register_generated_files
from .renderer import dashboard_data, render_dashboard, validate_dashboard_files
from .result import make_result
from .scanner import ScanCancelled, ScanLimitExceeded, scan_config
from .server import serve as serve_dashboard
from .validator import markdown_report, validate_records


def _runtime(workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], Path]:
    workspace = normalized(workspace)
    config_path = resolve_config_path(workspace, requested_config) if requested_config else default_config_path(workspace)
    return load_config(config_path, expected_workspace=workspace), config_path


def _index_path(config: dict[str, Any]) -> Path:
    return normalized(config["paths"]["internal"]) / "source-index.jsonl"


def _update_state(config: dict[str, Any], stage: str, details: dict[str, Any] | None = None) -> Path:
    state_path = normalized(config["paths"]["internal"]) / STATE_NAME
    state = load_json(state_path)
    completed = [str(value) for value in state.get("completed_stages", [])]
    if stage not in completed:
        completed.append(stage)
    completed_command_stages = {
        "BUILD",
        "VALIDATE",
        "GENERATE_HTML",
        "UPDATE",
        "UPDATE_NO_CHANGES",
        "READY",
    }
    state.update(
        {
            "updated_at": now_iso(),
            "status": "ready" if stage in completed_command_stages else "in_progress",
            "stage": stage,
            "completed_stages": completed,
        }
    )
    if details is not None:
        state["last_result"] = details
    atomic_write_json(state_path, state)
    return state_path


def _scan(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], Path]:
    index_path = _index_path(config)
    old = load_index(index_path)
    records = scan_config(config)
    changes = diff_records(old, records)
    write_index(index_path, records)
    register_generated_files(config, [index_path])
    return records, changes, index_path


def scan(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    try:
        config, config_path = _runtime(workspace, requested_config)
        records, changes, index_path = _scan(config)
        state_path = _update_state(config, "SCAN", {"records": len(records), "changes": changes})
    except ScanLimitExceeded as exc:
        return make_result(
            status="needs_user_input",
            code="SCAN_FILE_LIMIT",
            message=str(exc),
            needs_user_input=[{"gate": "scan_scope", "requested_action": "reduce_scope_or_raise_limit"}],
        ), 3
    except ScanCancelled as exc:
        return make_result(status="stopped", code="SCAN_CANCELLED", message=str(exc)), 1
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="SCAN_FAILED",
            message=str(exc),
            next_actions=[{"action": "run_doctor_or_reinitialize"}],
        ), 1
    return make_result(
        status="ok",
        code="SCAN_OK",
        message="Source metadata was scanned and the atomic JSONL index was updated.",
        artifacts=[str(config_path), str(index_path), str(state_path)],
        next_actions=[{"action": "build_knowledge", "command": "build"}],
        data={"records": len(records), "changes": changes, "source_files_changed": False},
    ), 0


def build(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    try:
        config, config_path = _runtime(workspace, requested_config)
        records, changes, index_path = _scan(config)
        validation = validate_records(records)
        pages = build_knowledge_pages(config=config, records=records, validation=validation)
        manifest_path = register_generated_files(config, pages)
        state_path = _update_state(
            config,
            "BUILD",
            {"records": len(records), "pages": len(pages), "changes": changes},
        )
    except ScanLimitExceeded as exc:
        return make_result(
            status="needs_user_input",
            code="SCAN_FILE_LIMIT",
            message=str(exc),
            needs_user_input=[{"gate": "scan_scope", "requested_action": "reduce_scope_or_raise_limit"}],
        ), 3
    except ScanCancelled as exc:
        return make_result(status="stopped", code="SCAN_CANCELLED", message=str(exc)), 1
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="BUILD_FAILED",
            message=str(exc),
            next_actions=[{"action": "inspect_config_and_scan"}],
        ), 1
    return make_result(
        status="ok",
        code="BUILD_OK",
        message="Derived Markdown knowledge pages were built without changing source files.",
        artifacts=[str(index_path), str(manifest_path), str(state_path), *[str(path) for path in pages]],
        next_actions=[{"action": "validate", "command": "validate"}],
        data={
            "records": len(records),
            "visible_records": len([record for record in records if not record.get("sensitive")]),
            "generated_pages": len(pages),
            "changes": changes,
            "source_files_changed": False,
            "dashboard_body_embedded": False,
        },
    ), 0


def validate(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    try:
        config, _config_path = _runtime(workspace, requested_config)
        index_path = _index_path(config)
        if not index_path.is_file():
            return make_result(
                status="not_ready",
                code="INDEX_NOT_FOUND",
                message="No source index exists yet.",
                next_actions=[{"action": "scan", "command": "scan"}],
            ), 1
        records = load_index(index_path)
        result = validate_records(records)
        internal = normalized(config["paths"]["internal"])
        knowledge = normalized(config["paths"]["knowledge"])
        json_path = internal / "reports" / "validation.json"
        markdown_path = knowledge / "99-系统" / "质量报告.md"
        atomic_write_json(json_path, result)
        atomic_write_text(markdown_path, markdown_report(result))
        manifest_path = register_generated_files(config, [json_path, markdown_path])
        state_path = _update_state(config, "VALIDATE", result["summary"])
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="VALIDATION_FAILED",
            message=str(exc),
        ), 1
    return make_result(
        status="ok",
        code="VALIDATION_OK",
        message="Metadata, link, sensitivity, provenance, and progress validation completed non-destructively.",
        artifacts=[str(json_path), str(markdown_path), str(manifest_path), str(state_path)],
        next_actions=[{"action": "render_dashboard", "command": "render"}],
        data={**result, "source_files_changed": False, "dashboard_body_embedded": False},
    ), 0


def render(*, workspace: Path, requested_config: Path | None) -> tuple[dict[str, Any], int]:
    try:
        config, _config_path = _runtime(workspace, requested_config)
        index_path = _index_path(config)
        if not index_path.is_file():
            return make_result(
                status="not_ready",
                code="INDEX_NOT_FOUND",
                message="No source index exists yet.",
                next_actions=[{"action": "build", "command": "build"}],
            ), 1
        records = load_index(index_path)
        validation = validate_records(records)
        data = dashboard_data(config=config, records=records, validation=validation)
        files = render_dashboard(config=config, data=data)
        checks = validate_dashboard_files(config, files)
        if not checks["passed"]:
            return make_result(
                status="error",
                code="DASHBOARD_SAFETY_CHECK_FAILED",
                message="Dashboard generation was stopped by the local safety check.",
                artifacts=[str(path) for path in files],
                data=checks,
            ), 1
        manifest_path = register_generated_files(config, files)
        state_path = _update_state(config, "GENERATE_HTML", data["summary"])
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="RENDER_FAILED",
            message=str(exc),
        ), 1
    return make_result(
        status="ok",
        code="RENDER_OK",
        message="The offline dashboard and audit data were rendered without remote assets.",
        artifacts=[str(path) for path in files] + [str(manifest_path), str(state_path)],
        next_actions=[{"action": "serve_or_open", "command": "serve"}],
        data={**checks, "summary": data["summary"], "source_files_changed": False},
    ), 0


def serve(
    *,
    workspace: Path,
    requested_config: Path | None,
    host: str | None,
    port: int | None,
    open_browser: bool,
    duration: float | None,
) -> tuple[dict[str, Any], int]:
    try:
        config, _config_path = _runtime(workspace, requested_config)
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(status="error", code="SERVER_CONFIG_FAILED", message=str(exc)), 1
    return serve_dashboard(
        config=config,
        host=host,
        port=port,
        open_browser=open_browser,
        duration=duration,
    )
