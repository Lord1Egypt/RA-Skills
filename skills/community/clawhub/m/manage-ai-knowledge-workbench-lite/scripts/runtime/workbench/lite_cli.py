"""Restricted command-line entrypoint for the public Lite distribution.

The Lite runtime deliberately exposes only metadata-only, foreground operations.
Background services, filesystem watching, semantic/model tasks, and a persistent
HTTP server are not imported or registered here. Read-only status and fail-closed
uninstall remain available so Lite users can inspect and safely remove runtime state.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .doctor import diagnose
from .lifecycle import initialize, status, uninstall
from .orchestrator import run_auto, validated_host_gate
from .pipeline import build, render, scan, validate
from .result import render_result
from .updater import incremental_update


def _common_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--workspace", type=Path, default=Path.cwd())
    parser.add_argument("--config", type=Path)
    parser.add_argument("--json", action="store_true", help="Emit the stable JSON command contract.")
    return parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="workbench-lite",
        description="Metadata-only foreground knowledge-workbench runtime.",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    common = _common_parser()

    doctor = sub.add_parser("doctor", parents=[common])
    doctor.add_argument("--source", type=Path, action="append")
    doctor.add_argument("--port", type=int, default=8765)
    doctor.add_argument("--max-vault-depth", type=int, default=3)

    init = sub.add_parser("init", parents=[common])
    init.add_argument("--source", type=Path, action="append")
    init.add_argument("--mode", choices=("auto", "markdown", "obsidian", "hybrid"), default="auto")
    init.add_argument("--port", type=int, default=8765)
    init.add_argument("--max-vault-depth", type=int, default=3)

    run = sub.add_parser("run", parents=[common])
    run.add_argument("--source", type=Path, action="append")
    run.add_argument("--mode", choices=("auto", "markdown", "obsidian", "hybrid"), default="auto")
    run.add_argument("--port", type=int, default=8765)
    run.add_argument("--max-vault-depth", type=int, default=3)
    run.add_argument("--resume", action="store_true")
    run.add_argument("--validated-host")

    sub.add_parser("scan", parents=[common])
    sub.add_parser("build", parents=[common])
    sub.add_parser("validate", parents=[common])
    sub.add_parser("render", parents=[common])
    sub.add_parser("status", parents=[common])

    update = sub.add_parser("update", parents=[common])
    update.add_argument("--max-batch", type=int)

    remove = sub.add_parser("uninstall", parents=[common])
    remove.add_argument("--remove-outputs", action="store_true")
    remove.add_argument("--confirm-remove-outputs", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    workspace = args.workspace.expanduser().resolve(strict=False)

    if args.command == "doctor":
        payload, exit_code = diagnose(
            workspace=workspace,
            sources=args.source or [workspace],
            preferred_port=args.port,
            max_vault_depth=args.max_vault_depth,
        )
    elif args.command == "init":
        payload, exit_code = initialize(
            workspace=workspace,
            sources=args.source or [workspace],
            requested_config=args.config,
            mode=args.mode,
            privacy_mode="metadata-only",
            preferred_port=args.port,
            max_vault_depth=args.max_vault_depth,
        )
    elif args.command == "run":
        host_gate = validated_host_gate(args.validated_host)
        if host_gate is not None:
            payload, exit_code = host_gate
        else:
            payload, exit_code = run_auto(
                workspace=workspace,
                sources=args.source or [],
                requested_config=args.config,
                mode=args.mode,
                privacy_mode="metadata-only",
                preferred_port=args.port,
                max_vault_depth=args.max_vault_depth,
                resume=args.resume,
                validated_host=args.validated_host,
            )
    elif args.command == "scan":
        payload, exit_code = scan(workspace=workspace, requested_config=args.config)
    elif args.command == "build":
        payload, exit_code = build(workspace=workspace, requested_config=args.config)
    elif args.command == "validate":
        payload, exit_code = validate(workspace=workspace, requested_config=args.config)
    elif args.command == "render":
        payload, exit_code = render(workspace=workspace, requested_config=args.config)
    elif args.command == "update":
        payload, exit_code = incremental_update(
            workspace=workspace,
            requested_config=args.config,
            max_batch=args.max_batch,
        )
    elif args.command == "status":
        payload, exit_code = status(workspace=workspace, requested_config=args.config)
    elif args.command == "uninstall":
        payload, exit_code = uninstall(
            workspace=workspace,
            requested_config=args.config,
            remove_outputs=args.remove_outputs,
            confirm_remove_outputs=args.confirm_remove_outputs,
        )
    else:  # pragma: no cover - argparse guarantees a registered command
        raise AssertionError(f"Unhandled command: {args.command}")

    sys.stdout.write(render_result(payload) + "\n")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
