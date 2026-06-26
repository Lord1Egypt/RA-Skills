#!/usr/bin/env python3
from pathlib import Path
import sys, json

from check_stage_complete import check as check_stage_complete
from load_project_state import reconstruct
from revision_utils import normalize_state


def exists_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.read_text(encoding='utf-8').strip() != ''


def count_md(dirpath: Path) -> int:
    return len(list(dirpath.glob('*.md'))) if dirpath.is_dir() else 0


def contains_all(path: Path, needles) -> bool:
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding='utf-8')
    return all(needle in text for needle in needles)


def load_state(project: Path):
    state_file = project / '.novel-state.json'
    if state_file.exists():
        try:
            return json.loads(state_file.read_text(encoding='utf-8')), None
        except Exception:
            return None, f'.novel-state.json is not valid JSON: {state_file}'
    return normalize_state(reconstruct(project), project), None


def state_gate_errors(state, stage):
    errs = []
    if not state:
        return errs
    review = state.get('review', {})
    batch = state.get('batch', {})
    approvals = state.get('approvals', {})
    revision = state.get('revision', {})

    gate = review.get('currentGate')
    if gate:
        errs.append(f'Current review gate is still open: {gate}')
    pending_artifacts = list(review.get('pendingArtifactPaths') or [])
    if pending_artifacts:
        errs.append(f'Pending artifacts still await approval: {", ".join(pending_artifacts)}')

    revision_gate = revision.get('currentRevisionGate') or revision.get('currentGate')
    if revision_gate and stage == 'final-review':
        errs.append(f'Current revision gate is still open: {revision_gate}')

    if stage == 'story-planning' and not approvals.get('discoveryApproved', False):
        errs.append('Discovery stage not explicitly approved yet')
    if stage == 'character-system' and not approvals.get('planningApproved', False):
        errs.append('Story planning stage not explicitly approved yet')
    if stage == 'drafting' and not approvals.get('characterApproved', False):
        errs.append('Character system stage not explicitly approved yet')
    if stage == 'drafting' and not approvals.get('openingApproved', False):
        errs.append('Opening gate not explicitly approved yet')
    if stage == 'polishing' and not batch.get('draftComplete', False):
        errs.append('Current batch draft is not marked complete yet')
    if stage == 'proofreading' and not batch.get('polishingComplete', False):
        errs.append('Current batch polishing is not marked complete yet')
    if stage == 'final-review' and not batch.get('proofreadingComplete', False):
        errs.append('Current batch proofreading is not marked complete yet')
    if stage == 'drafting' and batch.get('active') and not batch.get('scopeConfirmed', False):
        errs.append('Current batch scope is not confirmed yet')
    if stage == 'drafting' and batch.get('active') and not batch.get('chapterPlanApproved', False):
        errs.append('Current batch chapter plan is not approved yet')
    return errs


def file_gate_errors(project: Path, stage: str):
    errors = []
    stage = stage.lower()
    f00 = project / '00_选题报告.md'
    f00c = project / '00C_底盘与切口决策.md'
    f01 = project / '01_想法.md'
    f01a = project / '01A_风格圣经.md'
    f01b = project / '01B_总主线与卷级推进.md'
    f02 = project / '02_大纲.md'
    f03 = project / '03_人物小传.md'
    f04a = project / '04A_开篇设计.md'
    f05b = project / '05B_世界规则账本.md'
    f05c = project / '05C_伏笔回收台账.md'
    f05d = project / '05D_关系状态表.md'
    f05e = project / '05E_能力与资源变化表.md'
    chars = project / 'characters'
    manu = project / 'manuscript'

    strategic_docs = [
        (f00c, '00C_底盘与切口决策.md'),
        (f01a, '01A_风格圣经.md'),
        (f01b, '01B_总主线与卷级推进.md'),
        (f04a, '04A_开篇设计.md'),
        (f05b, '05B_世界规则账本.md'),
        (f05c, '05C_伏笔回收台账.md'),
        (f05d, '05D_关系状态表.md'),
        (f05e, '05E_能力与资源变化表.md'),
    ]

    if stage == 'discovery':
        pass
    elif stage == 'story-planning':
        if not exists_nonempty(f00):
            errors.append('00_选题报告.md is missing or empty')
    elif stage == 'character-system':
        if not exists_nonempty(f02):
            errors.append('02_大纲.md is missing or empty')
    elif stage == 'drafting':
        for path, label in strategic_docs:
            if not exists_nonempty(path):
                errors.append(f'{label} is missing or empty')
        if not exists_nonempty(f02):
            errors.append('02_大纲.md is missing or empty')
        if count_md(chars) == 0 and not exists_nonempty(f03):
            errors.append('No usable character package found')
    elif stage == 'polishing':
        for path, label in strategic_docs:
            if not exists_nonempty(path):
                errors.append(f'{label} is missing or empty')
        if count_md(manu) == 0:
            errors.append('No manuscript files found in manuscript/')
    elif stage == 'proofreading':
        for path, label in strategic_docs:
            if not exists_nonempty(path):
                errors.append(f'{label} is missing or empty')
        if count_md(manu) == 0:
            errors.append('No manuscript files found in manuscript/')
    elif stage == 'final-review':
        if count_md(manu) == 0:
            errors.append('No manuscript files found in manuscript/')
        recap = project / '05_前情回顾.md'
        if not exists_nonempty(recap):
            errors.append('05_前情回顾.md is missing or empty')
        else:
            needed = ['当前已推进到的位置', '最近一轮发生的关键事件', '当前未回收的伏笔 / 悬念', '下一轮写作必须记住的点']
            missing = [item for item in needed if not contains_all(recap, [item])]
            if missing:
                errors.append('05_前情回顾.md missing required sections: ' + ', '.join(missing))
    else:
        errors.append(f'Unknown stage: {stage}')
    return errors


def main():
    if len(sys.argv) < 3:
        print('Usage: check_stage_ready.py <项目目录> <stage>')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    stage = sys.argv[2].lower()

    if not project.exists():
        print(f'ERROR: project not found: {project}')
        sys.exit(2)

    state, state_error = load_state(project)
    errors = []
    if stage == 'final-review':
        if state_error:
            errors.append(state_error)
        report = project / '07_终审报告.md'
        if exists_nonempty(report):
            errors.append('Stage is already completed: final-review (07_终审报告.md already exists)')
        proofreading_errors = check_stage_complete(project, 'proofreading')
        errors.extend(proofreading_errors)
    errors.extend(file_gate_errors(project, stage))
    errors.extend(state_gate_errors(state, stage))

    print(f'Project: {project}')
    print(f'Stage: {stage}')
    if errors:
        print('READY: NO')
        print('Reasons:')
        for e in errors:
            print(f'- {e}')
        sys.exit(2)
    else:
        print('READY: YES')
        sys.exit(0)


if __name__ == '__main__':
    main()
