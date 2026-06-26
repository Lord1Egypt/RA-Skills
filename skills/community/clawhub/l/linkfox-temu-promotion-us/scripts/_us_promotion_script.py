#!/usr/bin/env python3
"""Factory for thin US Promotion API CLI scripts."""

import sys

import _temu_us_common  # noqa: F401 — gateway helpers in scripts/

from _temu_common import load_json_arg
from _temu_us_common import extract_business_params, run_and_print

def run_cli(api_type: str, usage: str) -> None:
    if len(sys.argv) < 2:
        print(f"Usage: {usage}", file=sys.stderr)
        sys.exit(1)
    params = load_json_arg(sys.argv)
    run_and_print(params, api_type, extract_business_params(params))
