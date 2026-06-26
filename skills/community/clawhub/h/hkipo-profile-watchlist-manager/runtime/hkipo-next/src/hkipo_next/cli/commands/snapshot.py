"""Snapshot command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from hkipo_next.adapters.legacy_snapshot import LegacySnapshotAdapter
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.snapshot import SnapshotResponse
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import (
    render_error_markdown,
    render_snapshot_markdown,
)
from hkipo_next.renderers.text_renderer import render_error_response, render_snapshot_response
from hkipo_next.services.snapshot_service import SnapshotService
from hkipo_next.utils.output import export_rendered_output


def execute(
    args: Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
    adapter: object | None = None,
    run_context: RunContext | None = None,
) -> int:
    run_context = run_context or RunContext.create()
    service = SnapshotService(adapter=adapter or LegacySnapshotAdapter())

    try:
        result = service.snapshot(symbol=args.symbol)
        data_status = "partial" if result.issues else "complete"
        response = SnapshotResponse(
            data=result,
            meta=run_context.meta(degraded=bool(result.issues), data_status=data_status),
        )
        rendered = _render_success(response, args.format)
        export_rendered_output(rendered, args.output)
        print(rendered, file=stdout)
        return 0
    except AppException as exc:
        response = build_error_response(
            exc.error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        rendered = _render_error(response, args.format)
        print(rendered, file=target)
        return exit_code_for(exc.error.code)
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "快照命令执行失败。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        rendered = _render_error(response, args.format)
        print(rendered, file=target)
        return exit_code_for(error.code)


def _render_success(response: SnapshotResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_snapshot_markdown(response)
    return render_snapshot_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
