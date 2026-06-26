"""CLI entry point for memory_consolidate package."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path


def _parse_args():
    parser = argparse.ArgumentParser(
        description="Incremental memory consolidation for OpenClaw workspace."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze only, do not write any files.",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed output.",
    )
    parser.add_argument(
        "--config",
        metavar="PATH",
        help="Path to config.yaml (overrides default search path).",
    )
    parser.add_argument(
        "--workspace",
        metavar="PATH",
        help="Path to workspace root (overrides OPENCLAW_WORKSPACE env var).",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    if args.workspace:
        os.environ["OPENCLAW_WORKSPACE"] = str(Path(args.workspace).resolve())

    if args.config:
        os.environ["MEMORY_CONSOLIDATE_CONFIG"] = str(Path(args.config).resolve())

    if args.dry_run:
        print("[dry-run] Analysis only — no files will be written.")
        # Import and run in dry-run mode (currently just exits cleanly)
        return 0

    from .main import main as _main
    return _main()


if __name__ == "__main__":
    raise SystemExit(main())
