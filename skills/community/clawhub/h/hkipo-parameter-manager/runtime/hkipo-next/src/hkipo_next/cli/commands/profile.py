"""Profile management command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from pydantic import ValidationError

from hkipo_next.config.loader import ProfileLoader
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.preferences import ProfileData, ProfileResponse
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import render_error_markdown, render_profile_markdown
from hkipo_next.renderers.text_renderer import render_error_response, render_profile_response


PROFILE_OVERRIDE_FIELDS = (
    "risk_profile",
    "default_output_format",
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
    loader = ProfileLoader()
    cli_overrides = _cli_overrides(args) if args.profile_action == "show" else None

    try:
        if args.profile_action == "set":
            _update_profile(args, loader)

        loaded = loader.load(cli_overrides=cli_overrides)
        response = ProfileResponse(
            data=ProfileData(
                profile=loaded.to_view(),
                sources=loaded.sources,
                config_file=loaded.config_file,
                notes=_build_notes(loaded),
            ),
            meta=run_context.meta(degraded=False, data_status="complete"),
        )
        rendered = _render_success(response, args.format)
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
    except ValidationError as exc:
        error = AppError.arg(
            "profile 配置无效。",
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
            "profile 命令执行失败。",
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


def _cli_overrides(args: Namespace) -> dict[str, object]:
    return {
        field_name: getattr(args, field_name, None)
        for field_name in PROFILE_OVERRIDE_FIELDS
    }


def _update_profile(args: Namespace, loader: ProfileLoader) -> None:
    updates = _cli_overrides(args)
    updates = {field_name: value for field_name, value in updates.items() if value is not None}
    if not updates:
        raise AppException(
            AppError.arg("profile set 至少需要提供一个可更新字段。")
        )
    loader.repository.update(updates)


def _build_notes(loaded_profile: object) -> list[str]:
    profile = loaded_profile
    notes = [
        "敏感字段仅通过环境变量加载，不写入普通配置文件。",
    ]
    if getattr(profile, "api_token", None) is not None:
        notes.append("已检测到环境变量敏感配置，输出中仅展示“已配置”。")
    return notes


def _render_success(response: ProfileResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_profile_markdown(response)
    return render_profile_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
