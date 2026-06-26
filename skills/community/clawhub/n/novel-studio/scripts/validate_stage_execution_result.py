#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from stage_execution_utils import ensure_project, read_json_file, validate_bundle_and_result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate a subagent stage execution result.')
    parser.add_argument('project')
    parser.add_argument('--bundle-file', required=True)
    parser.add_argument('--result-file', required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        project = ensure_project(Path(args.project))
        bundle = read_json_file(Path(args.bundle_file))
        result = read_json_file(Path(args.result_file))
        validated = validate_bundle_and_result(project, bundle, result)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(validated, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()

