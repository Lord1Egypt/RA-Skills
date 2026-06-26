"""Review history list/export command handler."""

from __future__ import annotations

from argparse import Namespace
from datetime import date, datetime, time, timezone
from json import JSONDecodeError
from typing import TextIO

from pydantic import ValidationError

from hkipo_next.config.loader import resolve_runtime_paths
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.review import (
    ReviewActualResult,
    ReviewDetailResponse,
    ReviewExportResponse,
    ReviewListResponse,
    SuggestionImportResponse,
    SuggestionListResponse,
)
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import (
    render_error_markdown,
    render_review_export_markdown,
    render_review_list_markdown,
)
from hkipo_next.renderers.text_renderer import (
    render_error_response,
    render_review_export_response,
    render_review_list_response,
)
from hkipo_next.services.review_service import ReviewService
from hkipo_next.storage.review_store import ReviewStore


def execute(
    args: Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
    run_context: RunContext | None = None,
) -> int:
    run_context = run_context or RunContext.create()
    runtime_paths = resolve_runtime_paths()
    service = _build_review_service(runtime_paths)

    try:
        from_date = _parse_bound(getattr(args, "from_date", None), is_end=False)
        to_date = _parse_bound(getattr(args, "to_date", None), is_end=True)
        if args.review_action == "list":
            data = service.list_records(from_date=from_date, to_date=to_date, limit=args.limit)
            response = ReviewListResponse(
                data=data,
                meta=run_context.meta(
                    degraded=False,
                    data_status="complete",
                ),
            )
            print(_render_success(response, args.format), file=stdout)
            return 0
        if args.review_action == "show":
            data = service.get_record_detail(record_id=args.record_id)
            response = ReviewDetailResponse(
                data=data,
                meta=run_context.meta(
                    degraded=False,
                    data_status="complete",
                ),
            )
            print(_render_success(response, args.format), file=stdout)
            return 0
        if args.review_action == "update":
            actual_result = _build_actual_result(args)
            if actual_result is None and args.variance_note is None:
                raise AppException(AppError.arg("review update 至少需要一个实际结果字段或 variance_note。"))
            data = service.update_record_detail(
                record_id=args.record_id,
                actual_result=actual_result,
                variance_note=args.variance_note,
                updated_at=run_context.timestamp,
            )
            response = ReviewDetailResponse(
                data=data,
                meta=run_context.meta(
                    degraded=False,
                    data_status="complete",
                ),
            )
            print(_render_success(response, args.format), file=stdout)
            return 0
        if args.review_action == "import-suggestions":
            data = service.import_suggestions(
                source_file=args.input,
                imported_at=run_context.timestamp,
            )
            response = SuggestionImportResponse(
                data=data,
                meta=run_context.meta(
                    degraded=False,
                    data_status="complete",
                ),
            )
            print(_render_success(response, args.format), file=stdout)
            return 0
        if args.review_action == "suggestions":
            data = service.list_suggestions(
                record_id=args.record_id,
                batch_id=args.batch_id,
                status=args.status,
            )
            response = SuggestionListResponse(
                data=data,
                meta=run_context.meta(
                    degraded=False,
                    data_status="complete",
                ),
            )
            print(_render_success(response, args.format), file=stdout)
            return 0

        data = service.export_records(
            run_context=run_context,
            from_date=from_date,
            to_date=to_date,
            limit=args.limit,
            output_path=args.output,
        )
        response = ReviewExportResponse(
            data=data,
            meta=run_context.meta(
                degraded=False,
                data_status="complete",
            ),
        )
        print(_render_success(response, args.format), file=stdout)
        return 0
    except AppException as exc:
        response = build_error_response(
            exc.error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(exc.error.code)
    except KeyError as exc:
        error = AppError.arg(
            "未找到指定的 review record。",
            details={"record_id": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except FileNotFoundError as exc:
        error = AppError.arg(
            "未找到指定的 suggestions 文件。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except JSONDecodeError as exc:
        error = AppError.arg(
            "suggestions 文件不是合法 JSON。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except ValueError as exc:
        error = AppError.arg(
            "review 时间参数无效。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except ValidationError as exc:
        error = AppError.arg(
            "review 输入无效。",
            details={"reason": exc.errors()},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "review 命令执行失败。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        print(_render_error(response, args.format), file=target)
        return exit_code_for(error.code)


def _build_review_service(runtime_paths) -> ReviewService:
    return ReviewService(
        ReviewStore(runtime_paths.sqlite_file),
        review_artifacts_dir=runtime_paths.review_artifacts_dir,
    )


def _build_actual_result(args: Namespace) -> ReviewActualResult | None:
    exited_at = _parse_bound(args.exited_at, is_end=False) if getattr(args, "exited_at", None) else None
    payload = {
        "allocated_lots": getattr(args, "allocated_lots", None),
        "listing_return_pct": getattr(args, "listing_return_pct", None),
        "exit_return_pct": getattr(args, "exit_return_pct", None),
        "realized_pnl_hkd": getattr(args, "realized_pnl_hkd", None),
        "exited_at": exited_at,
        "notes": getattr(args, "notes", None),
    }
    if not any(value is not None for value in payload.values()):
        return None
    return ReviewActualResult(**payload)


def _parse_bound(value: str | None, *, is_end: bool) -> datetime | None:
    if value in (None, ""):
        return None
    try:
        parsed_date = date.fromisoformat(value)
    except ValueError:
        parsed_datetime = datetime.fromisoformat(value)
        if parsed_datetime.tzinfo is None:
            parsed_datetime = parsed_datetime.replace(tzinfo=timezone.utc)
        return parsed_datetime.astimezone(timezone.utc)

    bound_time = time.max if is_end else time.min
    return datetime.combine(parsed_date, bound_time, tzinfo=timezone.utc)


def _render_success(response, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        if isinstance(response, ReviewListResponse):
            return render_review_list_markdown(response)
        if isinstance(response, ReviewDetailResponse):
            from hkipo_next.renderers.markdown_renderer import render_review_detail_markdown

            return render_review_detail_markdown(response)
        if isinstance(response, SuggestionImportResponse):
            from hkipo_next.renderers.markdown_renderer import render_suggestion_import_markdown

            return render_suggestion_import_markdown(response)
        if isinstance(response, SuggestionListResponse):
            from hkipo_next.renderers.markdown_renderer import render_suggestion_list_markdown

            return render_suggestion_list_markdown(response)
        return render_review_export_markdown(response)
    if isinstance(response, ReviewListResponse):
        return render_review_list_response(response)
    if isinstance(response, ReviewDetailResponse):
        from hkipo_next.renderers.text_renderer import render_review_detail_response

        return render_review_detail_response(response)
    if isinstance(response, SuggestionImportResponse):
        from hkipo_next.renderers.text_renderer import render_suggestion_import_response

        return render_suggestion_import_response(response)
    if isinstance(response, SuggestionListResponse):
        from hkipo_next.renderers.text_renderer import render_suggestion_list_response

        return render_suggestion_list_response(response)
    return render_review_export_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
