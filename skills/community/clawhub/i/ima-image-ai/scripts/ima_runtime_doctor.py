#!/usr/bin/env python3
from __future__ import annotations

import os
import sys

from ima_runtime.doctor import build_parser as _build_parser_impl
from ima_runtime.doctor import run_doctor as _run_doctor_impl


def build_parser():
    return _build_parser_impl()


def main():
    args = build_parser().parse_args()
    return _run_doctor_impl(
        api_key=args.api_key or os.getenv("IMA_API_KEY"),
        base_url=args.base_url,
        language=args.language,
        output_json=args.output_json,
    )


if __name__ == "__main__":
    sys.exit(main())
