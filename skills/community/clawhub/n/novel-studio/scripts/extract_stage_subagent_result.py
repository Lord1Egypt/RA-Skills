#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from stage_execution_utils import dispatch_layout, ensure_outside_project, ensure_project, extract_single_json_object


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Extract exactly one JSON result object from child raw output.')
    parser.add_argument('--dispatch-dir')
    parser.add_argument('--raw-file')
    parser.add_argument('--result-file')
    parser.add_argument('--project-root', required=True)
    return parser.parse_args()


def write_json(path: Path, payload: object) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def extract_dispatch_result(
    project_root: str | Path,
    *,
    dispatch_dir: str | Path | None = None,
    raw_file: str | Path | None = None,
    result_file: str | Path | None = None,
) -> dict:
    project = ensure_project(Path(project_root))
    resolved_dispatch_dir = (
        ensure_outside_project(project, Path(dispatch_dir), 'dispatch dir')
        if dispatch_dir is not None
        else None
    )
    layout = dispatch_layout(resolved_dispatch_dir) if resolved_dispatch_dir is not None else None
    raw_path = raw_file or (str(layout['rawFile']) if layout is not None else None)
    if raw_path is None:
        raise ValueError('--raw-file or --dispatch-dir is required')
    resolved_raw_file = ensure_outside_project(project, Path(raw_path), 'raw child response file')
    raw_text = resolved_raw_file.read_text(encoding='utf-8')
    result = extract_single_json_object(raw_text)
    result_path = result_file or (str(layout['resultFile']) if layout is not None else None)
    if result_path:
        resolved_result_file = ensure_outside_project(project, Path(result_path), 'result file')
        write_json(resolved_result_file, result)
    return result


def main() -> None:
    args = parse_args()
    try:
        result = extract_dispatch_result(
            args.project_root,
            dispatch_dir=args.dispatch_dir,
            raw_file=args.raw_file,
            result_file=args.result_file,
        )
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
