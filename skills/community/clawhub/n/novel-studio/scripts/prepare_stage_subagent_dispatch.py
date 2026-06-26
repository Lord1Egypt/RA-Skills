#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

from build_stage_execution_package import build_bundle
from chapter_progress_utils import mark_dispatch_started
from revision_utils import load_state, save_state
from stage_execution_utils import (
    bundle_fingerprint_payload,
    build_bundle_manifest,
    build_child_prompt,
    dispatch_layout,
    ensure_outside_project,
    ensure_project,
    payload_digest,
    snapshot_project,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Prepare a parent-side subagent dispatch bundle and prompt.')
    parser.add_argument('project')
    parser.add_argument('stage')
    parser.add_argument('--batch-range')
    parser.add_argument('--target-file', action='append', default=[])
    parser.add_argument('--overwrite', default=None)
    parser.add_argument('--polishing-focus')
    parser.add_argument('--dispatch-dir')
    parser.add_argument('--bundle-file')
    parser.add_argument('--prompt-file')
    parser.add_argument('--manifest-file')
    return parser.parse_args()


def ensure_parent_dir(path: Path) -> Path:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def default_output_dir() -> Path:
    return Path(tempfile.mkdtemp(prefix='novel-stage-dispatch-')).resolve()


def ensure_dispatch_dir(project: Path, path: Path) -> Path:
    resolved = path.expanduser().resolve()
    ensure_outside_project(project, resolved, 'dispatch dir')
    resolved.mkdir(parents=True, exist_ok=True)
    return resolved


def infer_dispatch_dir(args: argparse.Namespace, fallback_dir: Path) -> Path:
    if args.dispatch_dir:
        return Path(args.dispatch_dir)
    explicit_paths = [Path(value).expanduser().resolve() for value in [args.bundle_file, args.prompt_file, args.manifest_file] if value]
    if explicit_paths:
        parents = {path.parent for path in explicit_paths}
        if len(parents) == 1:
            return next(iter(parents))
    return fallback_dir


def build_prepare_namespace(
    project: str | Path,
    stage: str,
    *,
    batch_range: str | None = None,
    target_files: list[str] | None = None,
    overwrite: bool | None = None,
    polishing_focus: str | None = None,
    dispatch_dir: str | Path | None = None,
    bundle_file: str | Path | None = None,
    prompt_file: str | Path | None = None,
    manifest_file: str | Path | None = None,
) -> argparse.Namespace:
    return argparse.Namespace(
        project=str(project),
        stage=stage,
        batch_range=batch_range,
        target_file=list(target_files or []),
        overwrite=None if overwrite is None else ('true' if overwrite else 'false'),
        polishing_focus=polishing_focus,
        dispatch_dir=None if dispatch_dir is None else str(dispatch_dir),
        bundle_file=None if bundle_file is None else str(bundle_file),
        prompt_file=None if prompt_file is None else str(prompt_file),
        manifest_file=None if manifest_file is None else str(manifest_file),
    )


def refresh_bundle_validation_context(project: Path, bundle: dict[str, object]) -> None:
    validation = bundle['validationContext']
    baseline_files = snapshot_project(project)
    validation['baselineFiles'] = baseline_files
    validation['baselineFilesDigest'] = payload_digest(baseline_files)
    validation['executionPackageDigest'] = payload_digest(bundle['executionPackage'])
    validation['bundleFingerprint'] = payload_digest(bundle_fingerprint_payload(validation))


def prepare_dispatch_payload(args: argparse.Namespace) -> dict[str, object]:
    project = ensure_project(Path(args.project))
    bundle = build_bundle(args)
    prompt = build_child_prompt(bundle['executionPackage'])

    output_dir = default_output_dir()
    dispatch_dir = ensure_dispatch_dir(project, infer_dispatch_dir(args, output_dir))
    layout = dispatch_layout(dispatch_dir)
    bundle_file = (
        ensure_outside_project(project, ensure_parent_dir(Path(args.bundle_file)), 'bundle file')
        if args.bundle_file
        else layout['bundleFile']
    )
    prompt_file = (
        ensure_outside_project(project, ensure_parent_dir(Path(args.prompt_file)), 'prompt file')
        if args.prompt_file
        else layout['promptFile']
    )
    manifest_file = (
        ensure_outside_project(project, ensure_parent_dir(Path(args.manifest_file)), 'manifest file')
        if args.manifest_file
        else layout['manifestFile']
    )

    state = load_state(project)
    package = bundle['executionPackage']
    mark_dispatch_started(
        state['batch'],
        package['stage'],
        package['requiredInputs']['chapterLabels'],
        package['targetFiles'],
    )
    save_state(project, state)
    refresh_bundle_validation_context(project, bundle)

    bundle_file.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding='utf-8')
    prompt_file.write_text(prompt, encoding='utf-8')
    manifest = build_bundle_manifest(bundle_file, bundle, prompt_file=prompt_file, prompt_text=prompt)
    manifest_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')

    return {
        'dispatchDir': str(dispatch_dir),
        'bundleFile': str(bundle_file),
        'promptFile': str(prompt_file),
        'manifestFile': str(manifest_file),
        'rawFile': str(layout['rawFile']),
        'resultFile': str(layout['resultFile']),
        'validatedFile': str(layout['validatedFile']),
        'executionPackage': bundle['executionPackage'],
        'childPrompt': prompt,
    }


def main() -> None:
    args = parse_args()
    try:
        payload = prepare_dispatch_payload(args)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
