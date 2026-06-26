#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from extract_stage_subagent_result import extract_dispatch_result
from finalize_stage_subagent_dispatch import finalize_dispatch_result
from prepare_stage_subagent_dispatch import build_prepare_namespace, prepare_dispatch_payload
from stage_execution_utils import dispatch_layout, ensure_outside_project, ensure_project


def prepare_dispatch(
    project_root: str | Path,
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
) -> dict[str, object]:
    args = build_prepare_namespace(
        project_root,
        stage,
        batch_range=batch_range,
        target_files=target_files,
        overwrite=overwrite,
        polishing_focus=polishing_focus,
        dispatch_dir=dispatch_dir,
        bundle_file=bundle_file,
        prompt_file=prompt_file,
        manifest_file=manifest_file,
    )
    return prepare_dispatch_payload(args)


def record_child_output(
    project_root: str | Path,
    raw_text: str,
    *,
    dispatch_dir: str | Path | None = None,
    raw_file: str | Path | None = None,
) -> Path:
    if not isinstance(raw_text, str):
        raise ValueError('raw_text must be a string')

    project = ensure_project(Path(project_root))
    resolved_dispatch_dir = (
        ensure_outside_project(project, Path(dispatch_dir), 'dispatch dir')
        if dispatch_dir is not None
        else None
    )
    layout = dispatch_layout(resolved_dispatch_dir) if resolved_dispatch_dir is not None else None
    raw_path = raw_file or (str(layout['rawFile']) if layout is not None else None)
    if raw_path is None:
        raise ValueError('raw_file or dispatch_dir is required')

    resolved_raw_file = ensure_outside_project(project, Path(raw_path), 'raw child response file')
    resolved_raw_file.parent.mkdir(parents=True, exist_ok=True)
    resolved_raw_file.write_text(raw_text, encoding='utf-8')
    return resolved_raw_file


def finalize_dispatch(
    project_root: str | Path,
    *,
    dispatch_dir: str | Path | None = None,
    raw_file: str | Path | None = None,
    result_file: str | Path | None = None,
    bundle_file: str | Path | None = None,
    manifest_file: str | Path | None = None,
    validated_file: str | Path | None = None,
) -> dict[str, object]:
    extract_dispatch_result(
        project_root,
        dispatch_dir=dispatch_dir,
        raw_file=raw_file,
        result_file=result_file,
    )
    return finalize_dispatch_result(
        project_root,
        dispatch_dir=dispatch_dir,
        bundle_file=bundle_file,
        manifest_file=manifest_file,
        result_file=result_file,
        validated_file=validated_file,
    )
