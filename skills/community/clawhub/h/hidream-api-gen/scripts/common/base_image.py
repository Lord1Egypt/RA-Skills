#!/usr/bin/env python3
"""Shared OpenClaw video request runner."""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from typing import Any

from .task_client import parse_common_args, submit_task_and_poll_result


DEFAULT_TIMEOUT = 60 * 5
DEFAULT_POLL_INTERVAL = 5


def run_task(payload: dict[str, Any], authorization: str | None = None) -> dict[str, Any]:
    """Run image generation task."""
    path = f"/api-pub/gw/v4/image/{payload['module']}/async"
    return submit_task_and_poll_result(
        payload, path, authorization, DEFAULT_TIMEOUT
    )


def main(payload: dict[str, Any], args: argparse.Namespace) -> int:
    try:
        result = run_task(payload, args.authorization)
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
