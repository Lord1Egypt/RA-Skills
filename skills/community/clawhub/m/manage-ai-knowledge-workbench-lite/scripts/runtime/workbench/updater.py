"""Incremental deterministic updates and semantic queue bookkeeping."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .builder import atomic_write_text, build_knowledge_pages
from .config import ConfigError, atomic_write_json, normalized
from .index import diff_records, load_index, write_index
from .manifest import register_generated_files
from .pipeline import _index_path, _runtime, _update_state
from .renderer import dashboard_data, render_dashboard, validate_dashboard_files
from .result import make_result
from .scanner import ScanCancelled, ScanLimitExceeded, scan_config
from .validator import markdown_report, validate_records


def detect_changes(config: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], Path]:
    index_path = _index_path(config)
    old = load_index(index_path)
    records = scan_config(config)
    return records, diff_records(old, records), index_path


def incremental_update(
    *,
    workspace: Path,
    requested_config: Path | None,
    max_batch: int | None = None,
) -> tuple[dict[str, Any], int]:
    try:
        config, config_path = _runtime(workspace, requested_config)
        index_path = _index_path(config)
        if not index_path.is_file():
            return make_result(
                status="not_ready",
                code="INDEX_NOT_FOUND",
                message="No source index exists yet; run the autonomous build first.",
                next_actions=[{"action": "build", "command": "run"}],
            ), 1
        records, changes, index_path = detect_changes(config)
        changed_total = int(changes["changed_total"])
        if max_batch is not None and changed_total > max_batch:
            return make_result(
                status="needs_user_input",
                code="UPDATE_BATCH_LIMIT",
                message="The detected change batch exceeds the configured session resource limit.",
                needs_user_input=[
                    {
                        "gate": "update_batch",
                        "detected": changed_total,
                        "max_batch": max_batch,
                        "requested_action": "review_scope_or_increase_limit",
                    }
                ],
                data={"changes": changes, "model_calls": 0, "source_files_changed": False},
            ), 3
        if changed_total == 0:
            state_path = _update_state(
                config,
                "UPDATE_NO_CHANGES",
                {"changes": changes, "model_calls": 0, "generated_files_rewritten": 0},
            )
            return make_result(
                status="ok",
                code="UPDATE_NO_CHANGES",
                message="No source changes were detected; generated knowledge, HTML, and semantic tasks were untouched.",
                artifacts=[str(config_path), str(index_path), str(state_path)],
                next_actions=[{"action": "wait_or_continue_work"}],
                data={
                    "changes": changes,
                    "model_calls": 0,
                    "semantic_tasks_queued": 0,
                    "generated_files_rewritten": 0,
                    "source_files_changed": False,
                },
            ), 0

        write_index(index_path, records)
        validation = validate_records(records)
        pages = build_knowledge_pages(config=config, records=records, validation=validation)
        internal = normalized(config["paths"]["internal"])
        knowledge = normalized(config["paths"]["knowledge"])
        json_report = internal / "reports" / "validation.json"
        markdown_path = knowledge / "99-系统" / "质量报告.md"
        queue_path = internal / "semantic-queue.json"
        atomic_write_json(json_report, validation)
        atomic_write_text(markdown_path, markdown_report(validation))
        semantic_queue = {
            "schema_version": 1,
            "status": "disabled",
            "reason": "The deterministic Metadata-only update does not require model calls.",
            "model_transport": config.get("model_transport", "none"),
            "items": [],
            "model_calls": 0,
        }
        atomic_write_json(queue_path, semantic_queue)
        data = dashboard_data(config=config, records=records, validation=validation)
        dashboard_files = render_dashboard(config=config, data=data)
        checks = validate_dashboard_files(config, dashboard_files)
        if not checks["passed"]:
            return make_result(
                status="error",
                code="UPDATE_DASHBOARD_SAFETY_FAILED",
                message="Incremental update stopped because the regenerated dashboard failed its safety check.",
                artifacts=[str(path) for path in dashboard_files],
                data={"changes": changes, "checks": checks, "model_calls": 0},
            ), 1
        generated = [index_path, *pages, json_report, markdown_path, queue_path, *dashboard_files]
        manifest_path = register_generated_files(config, generated)
        state_path = _update_state(
            config,
            "UPDATE",
            {
                "changes": changes,
                "model_calls": 0,
                "semantic_tasks_queued": 0,
                "generated_files_rewritten": len(generated),
            },
        )
    except ScanLimitExceeded as exc:
        return make_result(
            status="needs_user_input",
            code="UPDATE_SCAN_FILE_LIMIT",
            message=str(exc),
            needs_user_input=[{"gate": "scan_scope", "requested_action": "reduce_scope_or_raise_limit"}],
        ), 3
    except ScanCancelled as exc:
        return make_result(status="stopped", code="UPDATE_SCAN_CANCELLED", message=str(exc)), 1
    except (ConfigError, OSError, ValueError, KeyError, TypeError) as exc:
        return make_result(
            status="error",
            code="UPDATE_FAILED",
            message=str(exc),
            next_actions=[{"action": "inspect_state_then_resume", "command": "run --resume"}],
        ), 1
    return make_result(
        status="ok",
        code="UPDATE_APPLIED",
        message="Source differences were deterministically applied and the knowledge and HTML outputs were revalidated.",
        artifacts=[str(path) for path in generated] + [str(manifest_path), str(state_path)],
        next_actions=[{"action": "open_dashboard_if_requested", "path": str(normalized(config["paths"]["dashboard"]) / "index.html")}],
        data={
            "changes": changes,
            "records": len(records),
            "model_calls": 0,
            "semantic_tasks_queued": 0,
            "generated_files_rewritten": len(generated),
            "dashboard_validated": True,
            "source_files_changed": False,
        },
    ), 0
