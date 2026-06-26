#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from apply_stage_execution_result import apply_validated_state
from revision_utils import load_state, save_state
from stage_execution_utils import (
    dispatch_layout,
    ensure_outside_project,
    ensure_project,
    read_json_file,
    validate_bundle_and_result,
    validate_bundle_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Validate and apply a parent-side subagent dispatch result.')
    parser.add_argument('project')
    parser.add_argument('--dispatch-dir')
    parser.add_argument('--bundle-file')
    parser.add_argument('--manifest-file')
    parser.add_argument('--result-file')
    parser.add_argument('--validated-file')
    return parser.parse_args()


def write_json(path: Path, payload: object) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')


def finalize_dispatch_result(
    project_root: str | Path,
    *,
    dispatch_dir: str | Path | None = None,
    bundle_file: str | Path | None = None,
    manifest_file: str | Path | None = None,
    result_file: str | Path | None = None,
    validated_file: str | Path | None = None,
) -> dict[str, object]:
    project = ensure_project(Path(project_root))
    resolved_dispatch_dir = (
        ensure_outside_project(project, Path(dispatch_dir), 'dispatch dir')
        if dispatch_dir is not None
        else None
    )
    layout = dispatch_layout(resolved_dispatch_dir) if resolved_dispatch_dir is not None else None
    bundle_path = bundle_file or (str(layout['bundleFile']) if layout is not None else None)
    result_path = result_file or (str(layout['resultFile']) if layout is not None else None)
    if bundle_path is None:
        raise ValueError('--bundle-file or --dispatch-dir is required')
    if result_path is None:
        raise ValueError('--result-file or --dispatch-dir is required')

    resolved_bundle_file = ensure_outside_project(project, Path(bundle_path), 'bundle file')
    manifest_path = manifest_file or (str(layout['manifestFile']) if layout is not None else None)
    resolved_manifest_file = (
        ensure_outside_project(project, Path(manifest_path), 'manifest file')
        if manifest_path
        else None
    )
    resolved_result_file = ensure_outside_project(project, Path(result_path), 'result file')
    validated_path = validated_file or (str(layout['validatedFile']) if layout is not None else None)
    resolved_validated_file = (
        ensure_outside_project(project, Path(validated_path), 'validated file')
        if validated_path
        else None
    )
    bundle = read_json_file(resolved_bundle_file)
    manifest = read_json_file(resolved_manifest_file) if resolved_manifest_file is not None else None
    if manifest is not None:
        validate_bundle_manifest(manifest, resolved_bundle_file, bundle)
    result = read_json_file(resolved_result_file)
    validated = validate_bundle_and_result(project, bundle, result)
    if resolved_validated_file is not None:
        write_json(resolved_validated_file, validated)

    data = load_state(project)
    apply_validated_state(data, validated, project)
    save_state(project, data)
    saved = load_state(project)
    return {
        'validated': validated,
        'savedState': saved,
    }


def main() -> None:
    args = parse_args()
    try:
        payload = finalize_dispatch_result(
            args.project,
            dispatch_dir=args.dispatch_dir,
            bundle_file=args.bundle_file,
            manifest_file=args.manifest_file,
            result_file=args.result_file,
            validated_file=args.validated_file,
        )
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
