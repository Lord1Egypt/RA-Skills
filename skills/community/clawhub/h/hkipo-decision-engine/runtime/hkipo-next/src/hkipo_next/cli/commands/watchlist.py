"""Watchlist management command handler."""

from __future__ import annotations

from argparse import Namespace
from typing import TextIO

from hkipo_next.config.loader import resolve_runtime_paths
from hkipo_next.config.watchlist import WatchlistRepository
from hkipo_next.contracts.errors import AppError, AppException, build_error_response, exit_code_for
from hkipo_next.contracts.preferences import WatchlistData, WatchlistResponse
from hkipo_next.observability.run_context import RunContext
from hkipo_next.renderers.json_renderer import render_model_as_json
from hkipo_next.renderers.markdown_renderer import render_error_markdown, render_watchlist_markdown
from hkipo_next.renderers.text_renderer import render_error_response, render_watchlist_response
from hkipo_next.utils.normalization import normalize_symbol


def execute(
    args: Namespace,
    *,
    stdout: TextIO,
    stderr: TextIO,
    run_context: RunContext | None = None,
) -> int:
    run_context = run_context or RunContext.create()
    paths = resolve_runtime_paths()
    repository = WatchlistRepository(paths.watchlist_file)

    try:
        if args.watchlist_action == "list":
            state = repository.read()
            changed_symbols: list[str] = []
        elif args.watchlist_action == "add":
            _ensure_symbols(args.symbols)
            state, changed_symbols = repository.add(args.symbols)
        elif args.watchlist_action == "remove":
            _ensure_symbols(args.symbols)
            state, changed_symbols = repository.remove(args.symbols)
        else:
            raise AppException(AppError.arg("未识别的 watchlist 子命令。"))

        response = WatchlistResponse(
            data=WatchlistData(
                operation=args.watchlist_action,
                symbols=state.symbols,
                changed_symbols=changed_symbols,
                total_items=len(state.symbols),
                storage_path=str(paths.watchlist_file),
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
    except Exception as exc:  # pragma: no cover - defensive path
        error = AppError.system(
            "watchlist 命令执行失败。",
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


def _ensure_symbols(symbols: list[str]) -> None:
    invalid_symbols = [symbol for symbol in symbols if normalize_symbol(symbol) is None]
    if invalid_symbols:
        raise AppException(
            AppError.arg(
                "watchlist 命令需要有效的 IPO 代码。",
                details={"symbols": invalid_symbols},
            )
        )


def _render_success(response: WatchlistResponse, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_watchlist_markdown(response)
    return render_watchlist_response(response)


def _render_error(response: object, output_format: str) -> str:
    if output_format == "json":
        return render_model_as_json(response)
    if output_format == "markdown":
        return render_error_markdown(response)
    return render_error_response(response)
