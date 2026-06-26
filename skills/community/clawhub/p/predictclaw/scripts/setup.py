#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from collections.abc import Mapping
from dataclasses import asdict
from pathlib import Path

from lib.mandated_mcp_setup import (
    configure_mandated_mcp,
)

SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent

HELP_TEXT = """PredictClaw setup helpers.

Usage:
    predictclaw setup mandated-mcp [--json]

Notes:
    - mandated-mcp uses the external erc-mandated-mcp runtime.
    - PredictClaw does not globally install packages in the default path.
    - PredictClaw does not auto-edit `.env` in the default path.
    - Install the external runtime yourself, then set ERC_MANDATED_MCP_COMMAND manually.
"""


def print_help() -> None:
    print(HELP_TEXT.strip())


def _emit_json(success: bool, payload: Mapping[str, object]) -> int:
    print(json.dumps({"success": success, **payload}, indent=2))
    return 0 if success else 1


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"--help", "-h", "help"}:
        print_help()
        return 0

    target = args.pop(0)
    if target != "mandated-mcp":
        print(f"Unknown setup target: {target}")
        print_help()
        return 1

    as_json = False
    for arg in args:
        if arg == "--json":
            as_json = True
        elif arg in {"--help", "-h", "help"}:
            print_help()
            return 0
        else:
            print(f"Unknown setup flag: {arg}")
            print_help()
            return 1

    try:
        result = configure_mandated_mcp(
            skill_dir=SKILL_DIR,
        )
    except RuntimeError as error:
        payload = {"error": type(error).__name__, "message": str(error)}
        if as_json:
            return _emit_json(False, payload)
        print(str(error))
        return 1

    payload = asdict(result)
    if as_json:
        return _emit_json(result.status == "ready", payload)

    print(result.message)
    if result.status != "ready":
        print(
            "Install the external erc-mandated-mcp runtime yourself, then set ERC_MANDATED_MCP_COMMAND in your local .env manually."
        )
    return 0 if result.status == "ready" else 1


if __name__ == "__main__":
    raise SystemExit(main())
