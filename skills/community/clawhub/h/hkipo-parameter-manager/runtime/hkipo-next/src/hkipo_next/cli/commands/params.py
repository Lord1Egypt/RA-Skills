"""Parameter version management command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from pydantic import ValidationError

from hkipo_next.adapters.legacy_snapshot import LegacySnapshotAdapter
from hkipo_next.config.loader import ProfileLoader, resolve_runtime_paths
from hkipo_next.config.parameters import ParameterRepository, build_parameter_set_from_args
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.scoring import (
    ParameterComparisonResponse,
    ParametersData,
    ParametersResponse,
)
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import (
    render_error_markdown,
    render_parameter_comparison_markdown,
    render_parameters_markdown,
)
from hkipo_next.renderers.text_renderer import (
    render_error_response,
    render_parameter_comparison_response,
    render_parameters_response,
)
from hkipo_next.services.scoring_service import ScoringService
from hkipo_next.services.snapshot_service import SnapshotService
from hkipo_next.storage.sqlite_store import SQLiteStore


PROFILE_COMPARE_FIELDS = (
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
    parameter_repository = ParameterRepository(SQLiteStore(runtime_paths.sqlite_file))

    try:
        if args.params_action == "save":
            record = parameter_repository.save(
                build_parameter_set_from_args(args),
                activate=args.activate or None,
            )
            response = ParametersResponse(
                data=ParametersData(
                    operation="save",
                    active_version=_active_version(parameter_repository),
                    parameter_set=record,
                    versions=parameter_repository.list(),
                    storage_path=parameter_repository.storage_path,
                ),
                meta=run_context.meta(degraded=False, data_status="complete"),
            )
            rendered = _render_parameters_success(response, args.format)
        elif args.params_action == "list":
            response = ParametersResponse(
                data=ParametersData(
                    operation="list",
                    active_version=_active_version(parameter_repository),
                    versions=parameter_repository.list(),
                    storage_path=parameter_repository.storage_path,
                ),
                meta=run_context.meta(degraded=False, data_status="complete"),
            )
            rendered = _render_parameters_success(response, args.format)
        elif args.params_action == "show":
            record = _require_record(parameter_repository, args.version or _active_version(parameter_repository))
            response = ParametersResponse(
                data=ParametersData(
                    operation="show",
                    active_version=_active_version(parameter_repository),
                    parameter_set=record,
                    versions=[record],
                    storage_path=parameter_repository.storage_path,
                ),
                meta=run_context.meta(degraded=False, data_status="complete"),
            )
            rendered = _render_parameters_success(response, args.format)
        elif args.params_action == "use":
            record = parameter_repository.use(args.version)
            response = ParametersResponse(
                data=ParametersData(
                    operation="use",
                    active_version=record.parameter_version,
                    parameter_set=record,
                    versions=parameter_repository.list(),
                    storage_path=parameter_repository.storage_path,
                ),
                meta=run_context.meta(degraded=False, data_status="complete"),
            )
            rendered = _render_parameters_success(response, args.format)
        elif args.params_action == "compare":
            if args.baseline_version == args.candidate_version:
                raise AppException(AppError.arg("compare 需要两个不同的参数版本。"))
            baseline = _require_record(parameter_repository, args.baseline_version)
            candidate = _require_record(parameter_repository, args.candidate_version)
            profile = ProfileLoader(runtime_paths=runtime_paths).load(
                cli_overrides=_profile_compare_overrides(args)
            ).to_view()
            comparison = ScoringService(
                SnapshotService(adapter=LegacySnapshotAdapter())
            ).compare_symbol(
                symbol=args.symbol,
                baseline_version=baseline,
                candidate_version=candidate,
                profile=profile,
                active_version=_active_version(parameter_repository),
                storage_path=parameter_repository.storage_path,
            )
            response = ParameterComparisonResponse(
                data=comparison,
                meta=run_context.meta(degraded=False, data_status="complete"),
            )
            rendered = _render_compare_success(response, args.format)
        else:
            raise AppException(AppError.arg("未识别的 params 子命令。"))

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
        target = stdout if args.format == "json" else stderr
        rendered = _render_error(response, args.format)
        print(rendered, file=target)
        return exit_code_for(error.code)
    except AppException as exc:
        response = build_error_response(
            exc.error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        rendered = _render_error(response, args.format)
        print(rendered, file=target)
        return exit_code_for(exc.error.code)
    except ValidationError as exc:
        error = AppError.arg(
            "参数集配置无效。",
            details={"reason": exc.errors()},
        )
        response = build_error_response(
            error,
            run_context.meta(degraded=True, data_status="error"),
        )
        target = stdout if args.format == "json" else stderr
        rendered = _render_error(response, args.format)
        print(rendered, file=target)
        return exit_code_for(error.code)
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "params 命令执行失败。",
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


def _active_version(repository: ParameterRepository) -> str | None:
    active = repository.get_active()
    return active.parameter_version if active is not None else None


def _require_record(repository: ParameterRepository, version_id: str | None):
    if version_id is None:
        raise AppException(AppError.arg("当前没有 active 参数版本，请先保存或切换参数集。"))
    record = repository.get(version_id)
    if record is None:
        raise KeyError(version_id)
    return record


def _profile_compare_overrides(args: Namespace) -> dict[str, object]:
    return {
        field_name: getattr(args, field_name, None)
        for field_name in PROFILE_COMPARE_FIELDS
    }


def _render_parameters_success(response: ParametersResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_parameters_markdown(response)
    return render_parameters_response(response)


def _render_compare_success(response: ParameterComparisonResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_parameter_comparison_markdown(response)
    return render_parameter_comparison_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
