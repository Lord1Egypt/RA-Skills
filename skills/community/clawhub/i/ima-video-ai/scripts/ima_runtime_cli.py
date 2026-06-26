#!/usr/bin/env python3
from __future__ import annotations

import sys

from ima_logger import cleanup_old_logs, setup_logger
from ima_runtime.cli_flow import run_cli as _run_cli_impl
from ima_runtime.cli_parser import build_parser as _build_parser_impl


def _get_logger():
    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
    return logger


def build_parser():
    return _build_parser_impl()


def main():
    return _run_cli_impl(build_parser().parse_args(), logger=_get_logger())


if __name__ == "__main__":
    sys.exit(main())
