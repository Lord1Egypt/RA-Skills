"""CLI argument parsing and entry point.

Uses argparse to mirror the Go cobra flags exactly.
"""

from __future__ import annotations

import argparse
import sys

from .app import Options, TwistApp
from .observe import ObserveOptions, parse_filter


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="twist",
        description="Intercept and modify browser network requests/responses via CDP",
    )

    p.add_argument("-H", "--host", default="127.0.0.1", help="Browser CDP listening address")
    p.add_argument("-p", "--port", type=int, default=9222, help="Browser CDP debugging port")
    p.add_argument("--launch", action="store_true", help="Auto-launch a new browser instance")
    p.add_argument("--launch-browser", default="chrome", choices=["chrome", "chromium", "edge"], help="Browser type to launch")
    p.add_argument("--launch-args", action="append", default=[], help="Extra arguments passed to browser (repeatable)")
    p.add_argument("-u", "--url", default="", help="URL to open in the browser")
    p.add_argument("-c", "--config", default="", help="Path to rule configuration file")
    p.add_argument("--list-targets", action="store_true", help="List all available browser tab targets")
    p.add_argument("-t", "--target", default="", help="Attach to a specific tab target by ID")
    p.add_argument("--observe", action="store_true", help="Observe network requests and responses, output JSONL to stdout (blocks until interrupted)")
    p.add_argument("--observe-filter", action="append", default=[], help="Filter observed events (repeatable, format: key=value1,value2)")
    p.add_argument("--observe-full-body", action="store_true", help="Include full response body without truncation")
    p.add_argument("-v", "--verbose", action="store_true", help="Enable verbose logging output")
    p.add_argument("--timeout", type=int, default=15, help="CDP connection timeout in seconds")
    return p


def _resolve_config(args: argparse.Namespace) -> bytes:
    if args.config:
        with open(args.config, "rb") as f:
            return f.read()

    if not sys.stdin.isatty():
        data = sys.stdin.buffer.read()
        if data:
            return data

    import os
    for name in (".twist.json", "twist.json"):
        if os.path.isfile(name):
            with open(name, "rb") as f:
                return f.read()

    return b""


async def _run_app(app: TwistApp) -> None:
    """Run the app and shut down cleanly on any termination."""
    try:
        await app.run()
    finally:
        try:
            await app.shutdown()
        except Exception:
            pass


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()

    # Validation
    if args.observe and args.config:
        print("error: --observe and --config are mutually exclusive", file=sys.stderr)
        sys.exit(1)
    if args.observe and args.list_targets:
        print("error: --observe and --list-targets are mutually exclusive", file=sys.stderr)
        sys.exit(1)

    has_observe_flags = bool(args.observe_full_body or args.observe_filter)
    if not args.observe and has_observe_flags:
        print("error: --observe-full-body and --observe-filter require --observe", file=sys.stderr)
        sys.exit(1)

    need_config = not args.list_targets and not args.observe
    config_data = _resolve_config(args) if need_config else None
    if need_config and not config_data:
        print(
            "error: no mode specified: use --observe to watch network requests, "
            "--config to modify them, or --list-targets to list tabs",
            file=sys.stderr,
        )
        sys.exit(1)

    opts = Options(
        host=args.host,
        port=args.port,
        launch=args.launch,
        launch_browser=args.launch_browser,
        launch_args=args.launch_args,
        url=args.url,
        config_file=args.config,
        config_data=config_data,
        list_targets=args.list_targets,
        target=args.target,
        verbose=args.verbose,
        timeout=args.timeout,
        observe=ObserveOptions(
            enabled=args.observe,
            full_body=args.observe_full_body,
            filter=parse_filter(args.observe_filter),
        ),
    )

    app = TwistApp(opts)
    try:
        import asyncio
        asyncio.run(_run_app(app))
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
