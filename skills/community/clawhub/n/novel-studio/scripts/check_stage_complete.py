#!/usr/bin/env python3
from pathlib import Path
import json
import re
import sys

from stage_persistence_utils import PROOFREADING_REPORT


VALID_FINAL_DECISIONS = {'pass', 'conditional pass', 'rework required'}
REQUIRED_FINAL_REVIEW_SECTIONS = [
    '## 最终结论',
    '## 是否可交付',
    '## 主要优点',
    '## 主要问题',
    '## 阻塞问题',
    '## 建议动作',
]


def exists_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.read_text(encoding='utf-8').strip() != ''


def contains_all(path: Path, needles):
    if not path.exists() or not path.is_file():
        return False
    text = path.read_text(encoding='utf-8')
    return all(n in text for n in needles)


def count_md(dirpath: Path) -> int:
    return len(list(dirpath.glob('*.md'))) if dirpath.is_dir() else 0


def load_state(project: Path):
    state_file = project / '.novel-state.json'
    if not state_file.exists():
        return None
    try:
        return json.loads(state_file.read_text(encoding='utf-8'))
    except Exception:
        return None


def extract_section_value(report_text: str, heading: str):
    pattern = rf'^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, report_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return None

    lines = [line.strip() for line in match.group(1).splitlines()]
    values = []
    for line in lines:
        if not line:
            continue
        if line.startswith('- '):
            values.append(line[2:].strip())
        elif line.startswith('-'):
            values.append(line[1:].strip())
        else:
            values.append(line)
    return values


def normalize_report_list(values):
    normalized = []
    for value in values or []:
        item = value.strip()
        if not item or item == '无':
            continue
        normalized.append(item)
    return normalized


def extract_summary(decision_values):
    for value in decision_values or []:
        if value.startswith('摘要：'):
            return value.split('：', 1)[1].strip()
    return None


def parse_explicit_bool(value: str):
    lowered = value.strip().lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    return None


def check_discovery(project: Path, errors):
    f00a = project / '00A_热点扫描.md'
    f00b = project / '00B_用户偏好.md'
    f00 = project / '00_选题报告.md'
    if not exists_nonempty(f00a):
        errors.append('00A_热点扫描.md is missing or empty')
    if not exists_nonempty(f00b):
        errors.append('00B_用户偏好.md is missing or empty')
    if not exists_nonempty(f00):
        errors.append('00_选题报告.md is missing or empty')
    else:
        needed = ['最终推荐题材', '最终标题', '一句话核心钩子', '项目方向结论', '风险提醒']
        missing = [x for x in needed if not contains_all(f00, [x])]
        if missing:
            errors.append('00_选题报告.md missing required sections: ' + ', '.join(missing))


def check_planning(project: Path, errors):
    f01 = project / '01_想法.md'
    f02 = project / '02_大纲.md'
    if not exists_nonempty(f01):
        errors.append('01_想法.md is missing or empty')
    if not exists_nonempty(f02):
        errors.append('02_大纲.md is missing or empty')
    else:
        needed = ['剧情', '冲突']
        missing = [x for x in needed if not contains_all(f02, [x])]
        if missing:
            errors.append('02_大纲.md may be incomplete; missing markers: ' + ', '.join(missing))


def check_character(project: Path, errors):
    f03 = project / '03_人物小传.md'
    chars = project / 'characters'
    if not exists_nonempty(f03) and count_md(chars) == 0:
        errors.append('No character package found (03_人物小传.md or characters/*.md)')


def check_drafting(project: Path, errors):
    plan = project / '05_本轮章节规划.md'
    opening = project / '04A_开篇设计.md'
    manu = project / 'manuscript'
    for required in [
        project / '00C_底盘与切口决策.md',
        project / '01A_风格圣经.md',
        project / '01B_总主线与卷级推进.md',
        project / '05B_世界规则账本.md',
        project / '05C_伏笔回收台账.md',
        project / '05D_关系状态表.md',
        project / '05E_能力与资源变化表.md',
    ]:
        if not exists_nonempty(required):
            errors.append(f'{required.name} is missing or empty')
    if not exists_nonempty(opening):
        errors.append('04A_开篇设计.md is missing or empty')
    if not exists_nonempty(plan):
        errors.append('05_本轮章节规划.md is missing or empty')
    else:
        needed = ['本轮范围', '本轮写作重点', '逐章规划', '本章目标', '出场人物', '高潮点', '吸引点']
        missing = [x for x in needed if not contains_all(plan, [x])]
        if missing:
            errors.append('05_本轮章节规划.md missing required sections: ' + ', '.join(missing))
    if count_md(manu) == 0:
        errors.append('No manuscript files found in manuscript/')


def check_polishing(project: Path, errors):
    manu = project / 'manuscript'
    if count_md(manu) == 0:
        errors.append('No manuscript files found in manuscript/')


def check_proofreading(project: Path, errors):
    report = project / PROOFREADING_REPORT
    if not exists_nonempty(report):
        errors.append(f'{PROOFREADING_REPORT} is missing or empty')


def check_final_review(project: Path, errors):
    report = project / '07_终审报告.md'
    if not exists_nonempty(report):
        errors.append('07_终审报告.md is missing or empty')
        return

    report_text = report.read_text(encoding='utf-8')
    missing_sections = [section for section in REQUIRED_FINAL_REVIEW_SECTIONS if section not in report_text]
    if missing_sections:
        errors.append('07_终审报告.md missing required sections: ' + ', '.join(missing_sections))

    decision_values = extract_section_value(report_text, '## 最终结论')
    decision = decision_values[0] if decision_values else None
    if decision not in VALID_FINAL_DECISIONS:
        allowed = ', '.join(sorted(VALID_FINAL_DECISIONS))
        errors.append(f'最终结论 must be one of: {allowed}')

    delivery_values = extract_section_value(report_text, '## 是否可交付')
    delivery_raw = delivery_values[0] if delivery_values else None
    delivery_ready = parse_explicit_bool(delivery_raw) if delivery_raw else None
    if delivery_ready is None:
        errors.append('是否可交付 must explicitly be true or false')

    state = load_state(project)
    review = state.get('review', {}) if state else {}
    state_decision = review.get('finalDecision')
    state_delivery_ready = review.get('finalDeliveryReady')
    state_blocking_issues = list(review.get('finalBlockingIssues') or [])
    state_review_summary = review.get('finalReviewSummary')
    blockers = normalize_report_list(extract_section_value(report_text, '## 阻塞问题'))
    summary = extract_summary(decision_values)

    if summary is None:
        errors.append('最终结论 must include "- 摘要：..."')

    if decision in VALID_FINAL_DECISIONS and state_decision != decision:
        errors.append(
            f'review.finalDecision mismatch: state={state_decision!r}, report={decision!r}'
        )
    if delivery_ready is not None and state_delivery_ready != delivery_ready:
        errors.append(
            f'review.finalDeliveryReady mismatch: state={state_delivery_ready!r}, report={delivery_ready!r}'
        )
    if state_blocking_issues != blockers:
        errors.append(
            f'review.finalBlockingIssues mismatch: state={state_blocking_issues!r}, report={blockers!r}'
        )
    if summary is not None and state_review_summary != summary:
        errors.append(
            f'review.finalReviewSummary mismatch: state={state_review_summary!r}, report={summary!r}'
        )
    if decision == 'pass' and blockers:
        errors.append('Invalid final-review result: pass cannot be combined with blockers')
    if decision == 'rework required' and delivery_ready is True:
        errors.append('Invalid final-review result: rework required cannot be combined with delivery-ready=true')
    if blockers and delivery_ready is True:
        errors.append('Invalid final-review result: blockers cannot be combined with delivery-ready=true')


def check(project: Path, stage: str):
    errors = []
    stage = stage.lower()
    if stage == 'discovery':
        check_discovery(project, errors)
    elif stage == 'story-planning':
        check_planning(project, errors)
    elif stage == 'character-system':
        check_character(project, errors)
    elif stage == 'drafting':
        check_drafting(project, errors)
    elif stage == 'polishing':
        check_polishing(project, errors)
    elif stage == 'proofreading':
        check_proofreading(project, errors)
    elif stage == 'final-review':
        check_final_review(project, errors)
    else:
        errors.append(f'Unknown stage: {stage}')
    return errors


def main():
    if len(sys.argv) < 3:
        print('Usage: check_stage_complete.py <项目目录> <stage>')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    stage = sys.argv[2]

    if not project.exists():
        print(f'ERROR: project not found: {project}')
        sys.exit(2)

    errors = check(project, stage)
    print(f'Project: {project}')
    print(f'Stage: {stage}')
    if errors:
        print('COMPLETE: NO')
        print('Reasons:')
        for e in errors:
            print(f'- {e}')
        sys.exit(2)
    else:
        print('COMPLETE: YES')
        sys.exit(0)


if __name__ == '__main__':
    main()
