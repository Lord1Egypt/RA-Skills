#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from ima_logger import cleanup_old_logs, setup_logger
from ima_runtime.doctor_flow import run_doctor as _run_doctor_impl
from ima_runtime.shared.config import DEFAULT_BASE_URL, VIDEO_TASK_TYPES


def _get_logger():
    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
    return logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA Video doctor: low-cost environment and connectivity check without creating a paid task",
    )
    parser.add_argument("--api-key", help="IMA Open API key (optional; falls back to IMA_API_KEY)")
    parser.add_argument("--task-type", default="text_to_video", choices=list(VIDEO_TASK_TYPES), help="Task type to probe")
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    return parser


def main() -> int:
    return _run_doctor_impl(build_parser().parse_args(), logger=_get_logger())


if __name__ == "__main__":
    sys.exit(main())
