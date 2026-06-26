#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from chapter_progress_utils import resolve_dispatch_chapter_labels
from stage_persistence_utils import PROOFREADING_REPORT
from stage_execution_utils import (
    base_output_contract,
    bundle_fingerprint_payload,
    canonical_acceptance_hints,
    ensure_project,
    ensure_stage_ready,
    exists_nonempty,
    load_character_package,
    load_manuscript_inputs,
    load_or_reconstruct_state,
    normalize_relpaths,
    normalize_stage,
    parse_bool,
    payload_digest,
    project_files,
    read_optional,
    read_text,
    snapshot_project,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Build a stage execution bundle for novel-studio.')
    parser.add_argument('project')
    parser.add_argument('stage')
    parser.add_argument('--batch-range')
    parser.add_argument('--target-file', action='append', default=[])
    parser.add_argument('--overwrite', default=None)
    parser.add_argument('--polishing-focus')
    return parser.parse_args()


def explicit_target_files(args: argparse.Namespace) -> list[str]:
    return normalize_relpaths(list(args.target_file or []), 'targetFiles')


def resolve_batch_range(state: dict, arg_value: str | None) -> str:
    if arg_value:
        return arg_value.strip()
    return state.get('batch', {}).get('chapterRange') or '未指定批次'


def build_must_not_modify(project: Path, target_files: list[str]) -> list[str]:
    target_set = set(target_files)
    return [relpath for relpath in project_files(project) if relpath not in target_set]


def resolve_overwrite(stage: str, args: argparse.Namespace) -> bool:
    if args.overwrite is not None:
        return parse_bool(args.overwrite)
    if stage == 'polishing':
        return True
    return False


def require_file(path: Path, label: str) -> str:
    if not exists_nonempty(path):
        raise ValueError(f'{label} is missing or empty: {path.name}')
    return read_text(path)


def resolve_platform_profile(state: dict, project: Path) -> str:
    notes = state.get('notes', {})
    profile = (notes.get('platformProfile') or '').strip()
    if profile:
        return profile

    for path in (project / '01A_风格圣经.md', project / '00C_底盘与切口决策.md'):
        text = read_optional(path)
        if not text:
            continue
        for candidate in ('起点模式', '番茄模式', '通用模式'):
            if candidate in text:
                return candidate

    return '通用模式'


def build_ledger_snapshot(project: Path) -> dict[str, str]:
    ledgers = {}
    for relpath, label in [
        ('05B_世界规则账本.md', 'world ledger'),
        ('05C_伏笔回收台账.md', 'foreshadow ledger'),
        ('05D_关系状态表.md', 'relationship ledger'),
        ('05E_能力与资源变化表.md', 'resource ledger'),
    ]:
        ledgers[relpath] = require_file(project / relpath, label)
    return ledgers


def build_required_inputs(project: Path, state: dict, stage: str, batch_range: str, target_files: list[str], polishing_focus: str | None) -> dict[str, object]:
    outline = require_file(project / '02_大纲.md', 'outline')
    batch_plan = require_file(project / '05_本轮章节规划.md', 'chapter plan')
    character_package = load_character_package(project)
    if not character_package:
        raise ValueError('character package is missing')

    common = {
        'batchRange': batch_range,
        'outline': outline,
        'batchPlan': batch_plan,
        'chapterLabels': resolve_dispatch_chapter_labels(stage, batch_plan, target_files),
        'characterFiles': character_package,
        'styleBible': require_file(project / '01A_风格圣经.md', 'style bible'),
        'mainlineSpec': require_file(project / '01B_总主线与卷级推进.md', 'mainline spec'),
        'openingDesign': require_file(project / '04A_开篇设计.md', 'opening design'),
        'platformProfile': resolve_platform_profile(state, project),
        'trackGuide': require_file(project / '00C_底盘与切口决策.md', 'track decision'),
        'ledgerSnapshot': build_ledger_snapshot(project),
        'recap': read_optional(project / '05_前情回顾.md'),
    }

    if stage == 'drafting':
        return common
    if stage == 'polishing':
        if not polishing_focus or not polishing_focus.strip():
            raise ValueError('polishingFocus is required for polishing')
        common['polishingFocus'] = polishing_focus.strip()
        common['manuscriptFiles'] = load_manuscript_inputs(project, target_files)
        common['styleBaseline'] = read_optional(project / '01_想法.md')
        return common

    common['manuscriptFiles'] = load_manuscript_inputs(project)
    return common


def build_bundle(args: argparse.Namespace) -> dict[str, object]:
    project = ensure_project(Path(args.project))
    stage = normalize_stage(args.stage)
    state = load_or_reconstruct_state(project)
    ensure_stage_ready(project, state, stage)

    batch_range = resolve_batch_range(state, args.batch_range)
    target_files = explicit_target_files(args)
    overwrite_flag = resolve_overwrite(stage, args)

    if stage == 'drafting':
        if not target_files:
            raise ValueError('drafting requires at least one --target-file')
        if any(not relpath.startswith('manuscript/') for relpath in target_files):
            raise ValueError('drafting target files must stay under manuscript/')
        if not overwrite_flag:
            existing = [relpath for relpath in target_files if (project / relpath).exists()]
            if existing:
                raise ValueError(
                    'drafting target files already exist but overwrite is false: ' + ', '.join(existing)
                )
    elif stage == 'polishing':
        if not target_files:
            target_files = [
                path.relative_to(project).as_posix()
                for path in sorted((project / 'manuscript').glob('*.md'))
            ]
        if not target_files:
            raise ValueError('polishing requires manuscript target files')
    else:
        target_files = [PROOFREADING_REPORT]
        overwrite_flag = True

    required_inputs = build_required_inputs(
        project,
        state,
        stage,
        batch_range,
        target_files,
        args.polishing_focus,
    )

    must_not_modify = build_must_not_modify(project, target_files)

    execution_package = {
        'taskType': stage,
        'projectRoot': str(project),
        'stage': stage,
        'batchRange': batch_range,
        'targetFiles': target_files,
        'overwriteFlag': overwrite_flag,
        'requiredInputs': required_inputs,
        'mustNotModify': must_not_modify,
        'outputContract': base_output_contract(stage, target_files),
        'acceptanceHints': canonical_acceptance_hints(stage),
    }

    baseline_files = snapshot_project(project)
    validation_context = {
        'projectRoot': str(project),
        'stage': stage,
        'batchRange': batch_range,
        'baselineFiles': baseline_files,
        'executionPackageDigest': payload_digest(execution_package),
        'baselineFilesDigest': payload_digest(baseline_files),
    }
    validation_context['bundleFingerprint'] = payload_digest(bundle_fingerprint_payload(validation_context))

    return {
        'executionPackage': execution_package,
        'validationContext': validation_context,
    }


def main() -> None:
    args = parse_args()
    try:
        bundle = build_bundle(args)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(bundle, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
