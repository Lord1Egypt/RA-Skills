#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from ima_logger import cleanup_old_logs, setup_logger
from ima_runtime.setup_flow import run_setup as _run_setup_impl
from ima_runtime.shared.config import DEFAULT_BASE_URL, VIDEO_TASK_TYPES


def _get_logger():
    logger = setup_logger("ima_skills")
    cleanup_old_logs(days=7)
    return logger


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="IMA Video onboarding helper: configure a first model preference without storing API keys",
    )
    parser.add_argument("--api-key", help="IMA Open API key (optional; falls back to IMA_API_KEY)")
    parser.add_argument("--task-type", choices=list(VIDEO_TASK_TYPES), help="Task type to configure")
    parser.add_argument("--model-id", help="Optional explicit model_id to save without interactive selection")
    parser.add_argument("--language", default="en", help="Language for product labels (en/zh)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="API base URL")
    parser.add_argument("--user-id", default="default", help="User ID for preference memory")
    return parser


def main() -> int:
    return _run_setup_impl(build_parser().parse_args(), logger=_get_logger())


if __name__ == "__main__":
    sys.exit(main())
