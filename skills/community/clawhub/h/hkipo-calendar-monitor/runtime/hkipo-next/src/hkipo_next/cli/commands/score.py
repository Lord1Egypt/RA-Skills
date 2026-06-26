"""Single-IPO score command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from pydantic import ValidationError

from hkipo_next.adapters.legacy_snapshot import LegacySnapshotAdapter
from hkipo_next.config.loader import ProfileLoader, resolve_runtime_paths
from hkipo_next.config.parameters import ParameterRepository
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.review import ReviewRecord
from hkipo_next.contracts.scoring import ScoreResponse
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import render_error_markdown, render_score_markdown
from hkipo_next.renderers.text_renderer import render_error_response, render_score_response
from hkipo_next.services.review_service import ReviewService
from hkipo_next.services.scoring_service import ScoringService
from hkipo_next.services.snapshot_service import SnapshotService
from hkipo_next.storage.review_store import ReviewStore
from hkipo_next.storage.sqlite_store import SQLiteStore


PROFILE_SCORE_FIELDS = (
    "risk_profile",
    "max_budget_hkd",
    "financing_preference",
)


def execute(
    args: Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
    run_context: RunContext | None = None,
) -> int:
    run_context = run_context or RunContext.create()
    runtime_paths = resolve_runtime_paths()
    profile_loader = ProfileLoader(runtime_paths=runtime_paths)
    resolved_format = args.format or "text"

    try:
        loaded_profile = profile_loader.load(cli_overrides=_profile_overrides(args))
        resolved_format = args.format or loaded_profile.default_output_format
        parameter_repository = ParameterRepository(SQLiteStore(runtime_paths.sqlite_file))
        parameter_version = _resolve_parameter_version(parameter_repository, args.parameter_version)
        summary = ScoringService(SnapshotService(adapter=LegacySnapshotAdapter())).score_symbol(
            symbol=args.symbol,
            parameter_version=parameter_version,
            profile=loaded_profile.to_view(),
        )
        response = ScoreResponse(
            data=summary,
            meta=run_context.meta(
                degraded=summary.source_issue_count > 0,
                data_status="partial" if summary.source_issue_count > 0 else "complete",
            ),
        )
        _persist_review_record(response, runtime_paths)
        rendered = _render_success(response, resolved_format)
        print(rendered, file=stdout)
        return 0
    except KeyError as exc:
        error = AppError.arg(
            "未找到指定的参数版本。",
            details={"parameter_version": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if resolved_format == "json" else stderr
        rendered = _render_error(response, resolved_format)
        print(rendered, file=target)
        return exit_code_for(error.code)
    except AppException as exc:
        response = build_error_response(
            exc.error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if resolved_format == "json" else stderr
        rendered = _render_error(response, resolved_format)
        print(rendered, file=target)
        return exit_code_for(exc.error.code)
    except ValidationError as exc:
        error = AppError.arg(
            "score 配置无效。",
            details={"reason": exc.errors()},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if resolved_format == "json" else stderr
        rendered = _render_error(response, resolved_format)
        print(rendered, file=target)
        return exit_code_for(error.code)
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "score 命令执行失败。",
            details={"reason": str(exc)},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if resolved_format == "json" else stderr
        rendered = _render_error(response, resolved_format)
        print(rendered, file=target)
        return exit_code_for(error.code)


def _resolve_parameter_version(repository: ParameterRepository, version_id: str | None):
    resolved_version = version_id
    if resolved_version is None:
        active = repository.get_active()
        if active is None:
            raise AppException(AppError.arg("当前没有 active 参数版本，请先保存或切换参数集。"))
        return active
    record = repository.get(resolved_version)
    if record is None:
        raise KeyError(resolved_version)
    return record


def _profile_overrides(args: Namespace) -> dict[str, object]:
    return {
        field_name: getattr(args, field_name, None)
        for field_name in PROFILE_SCORE_FIELDS
    }


def _build_review_service(runtime_paths) -> ReviewService:
    return ReviewService(
        ReviewStore(runtime_paths.sqlite_file),
        review_artifacts_dir=runtime_paths.review_artifacts_dir,
    )


def _persist_review_record(response: ScoreResponse, runtime_paths) -> ReviewRecord:
    try:
        return _build_review_service(runtime_paths).record_score_response(response)
    except Exception as exc:  # pragma: no cover - exercised via CLI path
        raise AppException(
            AppError.system(
                "score 结果已生成，但历史记录写入失败。",
                details={"reason": str(exc)},
            )
        ) from exc


def _render_success(response: ScoreResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_score_markdown(response)
    return render_score_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
