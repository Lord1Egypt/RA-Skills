"""Suggestion comparison and decision command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from hkipo_next.config.loader import resolve_runtime_paths
from hkipo_next.config.parameters import ParameterRepository
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.review import SuggestionDetailResponse
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import render_error_markdown, render_suggestion_detail_markdown
from hkipo_next.renderers.text_renderer import render_error_response, render_suggestion_detail_response
from hkipo_next.services.review_service import ReviewService
from hkipo_next.storage.review_store import ReviewStore
from hkipo_next.storage.sqlite_store import SQLiteStore


def execute(
    args: Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
    run_context: RunContext | None = None,
) -> int:
    run_context = run_context or RunContext.create()
    runtime_paths = resolve_runtime_paths()
    service = ReviewService(
        ReviewStore(runtime_paths.sqlite_file),
        review_artifacts_dir=runtime_paths.review_artifacts_dir,
    )
    parameter_repository = ParameterRepository(SQLiteStore(runtime_paths.sqlite_file))

    try:
        if args.apply_action == "show":
            data = service.get_suggestion_detail(
                suggestion_id=args.suggestion_id,
                parameter_repository=parameter_repository,
            )
        elif args.apply_action == "accept":
            data = service.accept_suggestion_detail(
                suggestion_id=args.suggestion_id,
                parameter_repository=parameter_repository,
                decided_at=run_context.timestamp,
                decision_note=args.reason,
            )
        else:
            data = service.reject_suggestion_detail(
                suggestion_id=args.suggestion_id,
                parameter_repository=parameter_repository,
                decided_at=run_context.timestamp,
                decision_note=args.reason,
            )
        response = SuggestionDetailResponse(
            data=data,
            meta=run_context.meta(
                degraded=False,
                data_status="complete",
            ),
        )
        print(_render_success(response, args.format), file=stdout)
        return 0
    except KeyError as exc:
        error = AppError.arg(
            "未找到指定的 suggestion。",
            details={"suggestion_id": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except AppException as exc:
        response = build_error_response(
            exc.error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(exc.error.code)
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "apply-suggestions 命令执行失败。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)


def _render_success(response: SuggestionDetailResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_suggestion_detail_markdown(response)
    return render_suggestion_detail_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
