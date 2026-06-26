#!/usr/bin/env python3
"""Prepare synthetic inputs for testing one MBTI stage in isolation."""

from __future__ import annotations

import argparse
import json

from dev_fixtures import STAGES, write_stage_fixture
from mbti_common import resolve_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare synthetic MBTI stage fixtures.")
    parser.add_argument("--stage", required=True, choices=STAGES, help="Which stage fixture to prepare.")
    parser.add_argument("--output-dir", required=True, help="Directory where fixture files should be written.")
    args = parser.parse_args()

    payload = write_stage_fixture(args.stage, resolve_path(args.output_dir))
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

