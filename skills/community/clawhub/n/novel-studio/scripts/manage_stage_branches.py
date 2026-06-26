#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from revision_utils import load_state, save_state
from stage_persistence_utils import (
    branch_state_key,
    gate_for_stage,
    now_iso,
    validate_artifact_updates,
)

SUBCOMMANDS = {'create', 'promote', 'prune'}
CLICHE_EXHAUSTION_FILES = (
    '00_脑暴任务卡.md',
    '01_直觉俗套清单.md',
    '02_反驳与否认.md',
    '03_变异候选.md',
    '04_保留候选.md',
    '05_定稿结论.md',
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Manage explicit staging branches for novel-studio.')
    subparsers = parser.add_subparsers(dest='command', required=True)

    create = subparsers.add_parser('create')
    create.add_argument('project')
    create.add_argument('stage')
    create.add_argument('branch_id')
    create.add_argument('--mode', choices=('standard', 'cliche_exhaustion'), default='standard')
    create.add_argument('--focus')
    create.add_argument('--round')

    promote = subparsers.add_parser('promote')
    promote.add_argument('project')
    promote.add_argument('stage')
    promote.add_argument('branch_id')
    promote.add_argument('--copy-file', action='append', dest='copy_files', required=True)

    prune = subparsers.add_parser('prune')
    prune.add_argument('project')
    prune.add_argument('stage')

    return parser


def branch_dir(project: Path, stage: str, branch_id: str) -> Path:
    return project / 'staging' / stage / branch_id


def scaffold_cliche_exhaustion_branch(branch_path: Path) -> None:
    for filename in CLICHE_EXHAUSTION_FILES:
        target = branch_path / filename
        if not target.exists():
            target.write_text('', encoding='utf-8')


def parse_novelty_axes(branch_path: Path) -> list[str]:
    conclusion = branch_path / '05_定稿结论.md'
    if not conclusion.exists():
        return []

    axes: list[str] = []
    in_section = False
    for raw_line in conclusion.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()
        if in_section and line.startswith('## '):
            break
        if line == '## Novelty Axes':
            in_section = True
            continue
        if in_section and line.startswith('- '):
            value = line[2:].strip()
            if value:
                axes.append(value)
    return axes


def promote_branch(project: Path, stage: str, branch_id: str, copy_files: list[str]) -> dict:
    data = load_state(project)
    workflow = data.setdefault('workflow', {})
    review = data.setdefault('review', {})
    style_risk = data.setdefault('narrativeIntelligence', {}).setdefault('styleRisk', {})
    substage = workflow.get('currentSubstage')
    selected_branch = branch_dir(project, stage, branch_id)
    if not selected_branch.exists():
        raise ValueError(f'branch not found: staging/{stage}/{branch_id}')

    artifact_updates = {}
    for relpath in copy_files:
        source = selected_branch / relpath
        if not source.exists():
            raise ValueError(f'branch artifact not found: staging/{stage}/{branch_id}/{relpath}')
        artifact_updates[relpath] = source.read_text(encoding='utf-8')

    validated = validate_artifact_updates(stage, artifact_updates, substage)
    novelty_axes = parse_novelty_axes(selected_branch)
    for relpath, text in validated.items():
        target = project / relpath
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    shutil.rmtree(project / 'staging' / stage, ignore_errors=True)
    review['activeBranches'] = []
    review['brainstormActive'] = False
    review['selectedBranch'] = branch_state_key(stage, branch_id)
    review['currentGate'] = gate_for_stage(stage, substage)
    review['pendingArtifactPaths'] = sorted(validated)
    review['lastPersistedStage'] = stage
    review['lastPersistedAt'] = now_iso()
    style_risk['noveltyAxes'] = novelty_axes
    workflow['status'] = 'awaiting_user_approval'
    save_state(project, data)
    return load_state(project)


def create_branch(
    project: Path,
    stage: str,
    branch_id: str,
    mode: str,
    focus: str | None,
    round_label: str | None,
) -> dict:
    data = load_state(project)
    workflow = data.setdefault('workflow', {})
    review = data.setdefault('review', {})
    branch_path = branch_dir(project, stage, branch_id)
    branch_path.mkdir(parents=True, exist_ok=True)
    if mode == 'cliche_exhaustion':
        scaffold_cliche_exhaustion_branch(branch_path)
    review['brainstormActive'] = True
    review['brainstormMode'] = mode
    review['brainstormFocus'] = focus
    review['brainstormRound'] = round_label
    workflow['status'] = 'brainstorming'
    key = branch_state_key(stage, branch_id)
    active_branches = list(review.get('activeBranches') or [])
    if key not in active_branches:
        active_branches.append(key)
    review['activeBranches'] = active_branches
    save_state(project, data)
    return load_state(project)


def prune_stage(project: Path, stage: str) -> dict:
    data = load_state(project)
    review = data.setdefault('review', {})
    stage_root = project / 'staging' / stage
    active = {
        entry.split('/', 1)[1]
        for entry in list(review.get('activeBranches') or [])
        if entry.startswith(f'{stage}/') and '/' in entry
    }

    if stage_root.exists():
        for child in stage_root.iterdir():
            if child.name not in active:
                shutil.rmtree(child, ignore_errors=True)
        if not active and stage_root.exists():
            shutil.rmtree(stage_root, ignore_errors=True)

    save_state(project, data)
    return load_state(project)


def main() -> int:
    args = build_parser().parse_args()
    project = Path(args.project).expanduser()
    if not project.exists():
        print(f'ERROR: project not found: {project}', file=sys.stderr)
        return 2

    try:
        if args.command == 'create':
            state = create_branch(
                project,
                args.stage,
                args.branch_id,
                args.mode,
                args.focus,
                args.round,
            )
        elif args.command == 'promote':
            state = promote_branch(project, args.stage, args.branch_id, args.copy_files)
        elif args.command == 'prune':
            state = prune_stage(project, args.stage)
        else:
            raise ValueError(f'unsupported command: {args.command}')
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
