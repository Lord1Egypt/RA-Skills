#!/usr/bin/env python3
from pathlib import Path
import json, sys
import re

from autopilot_utils import default_autopilot
from narrative_intelligence_utils import (
    CONSISTENCY_ARTIFACT,
    FORESHADOW_TRIPLES_ARTIFACT,
    THEORY_OF_MIND_ARTIFACT,
    TIMELINE_ARTIFACT,
)
from revision_utils import (
    default_batch,
    default_narrative_intelligence,
    default_review,
    default_revision,
    normalize_state,
    set_revision_blocker,
)
from stage_persistence_utils import PROOFREADING_REPORT, WORKFLOW_STATUSES, normalize_path_list


def exists_nonempty(path: Path) -> bool:
    return path.exists() and path.is_file() and path.read_text(encoding='utf-8').strip() != ''


def count_md(dirpath: Path) -> int:
    return len(list(dirpath.glob('*.md'))) if dirpath.is_dir() else 0


def extract_section_value(report_text: str, heading: str):
    pattern = rf'^{re.escape(heading)}\s*$\n(.*?)(?=^##\s|\Z)'
    match = re.search(pattern, report_text, flags=re.MULTILINE | re.DOTALL)
    if not match:
        return []

    values = []
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith('- '):
            values.append(stripped[2:].strip())
        elif stripped.startswith('-'):
            values.append(stripped[1:].strip())
        else:
            values.append(stripped)
    return values


def normalize_report_list(values):
    normalized = []
    for value in values or []:
        item = value.strip()
        if not item or item == '无':
            continue
        normalized.append(item)
    return normalized


def parse_explicit_bool(value: str):
    lowered = value.strip().lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    return False


def extract_summary(decision_values):
    for value in decision_values or []:
        if value.startswith('摘要：'):
            return value.split('：', 1)[1].strip()
    return None


def parse_label_values(values):
    parsed = {}
    for value in values or []:
        if value.startswith('### '):
            parsed['__heading__'] = value[4:].strip()
            continue
        if '：' not in value:
            continue
        label, raw = value.split('：', 1)
        parsed[label.strip()] = raw.strip()
    return parsed


def normalize_optional_text(value):
    if value is None:
        return None
    normalized = value.strip()
    if not normalized or normalized == '无':
        return None
    return normalized


def parse_csv_text(value):
    normalized = normalize_optional_text(value)
    if normalized is None:
        return []
    return [item.strip() for item in normalized.split(',') if item.strip()]


def detect_first_keyword(text: str | None, candidates: tuple[str, ...]) -> str | None:
    if not text:
        return None
    for candidate in candidates:
        if candidate in text:
            return candidate
    return None


def apply_revision_doc_state(project: Path, state: dict):
    revision_doc = project / '06_反馈与修订.md'
    if not exists_nonempty(revision_doc):
        return

    revision_text = revision_doc.read_text(encoding='utf-8')
    current_fields = parse_label_values(extract_section_value(revision_text, '## 当前正式修订'))
    current_gate = normalize_optional_text(current_fields.get('当前修订 gate'))

    if current_gate:
        revision = state['revision']
        revision['active'] = True
        revision['feedbackType'] = normalize_optional_text(current_fields.get('反馈类型'))
        revision['feedbackSummary'] = normalize_optional_text(current_fields.get('反馈摘要'))
        revision['affectedStages'] = parse_csv_text(current_fields.get('影响阶段'))
        revision['affectedFiles'] = parse_csv_text(current_fields.get('影响文件'))
        revision['overrideMode'] = normalize_optional_text(current_fields.get('处理模式'))
        revision['scopeSummary'] = normalize_optional_text(current_fields.get('范围说明'))
        revision['conflictSummary'] = normalize_optional_text(current_fields.get('冲突说明'))
        revision['revisionPlanSummary'] = normalize_optional_text(current_fields.get('修订计划'))
        revision['resultSummary'] = normalize_optional_text(current_fields.get('修订结果'))
        revision['currentRevisionGate'] = current_gate
        revision['awaitingUserApproval'] = True
        if revision['feedbackSummary']:
            state['review']['lastUserFeedbackSummary'] = revision['feedbackSummary']
        set_revision_blocker(state, current_gate)

    closed_fields = parse_label_values(extract_section_value(revision_text, '## 最近关闭的修订'))
    heading = normalize_optional_text(closed_fields.get('__heading__'))
    if heading:
        parts = heading.split(' ', 1)
        closed_at = parts[0].strip() if parts else None
        feedback_type = parts[1].strip() if len(parts) > 1 else None
        state['revision']['lastClosedRevision'] = {
            'feedbackType': normalize_optional_text(feedback_type),
            'feedbackSummary': normalize_optional_text(closed_fields.get('反馈摘要')),
            'affectedFiles': parse_csv_text(closed_fields.get('影响范围')),
            'resultSummary': normalize_optional_text(closed_fields.get('修订结果')),
            'closedAt': normalize_optional_text(closed_at),
            'closeMode': normalize_optional_text(closed_fields.get('关闭方式')),
        }
        if not state['review'].get('lastUserFeedbackSummary'):
            state['review']['lastUserFeedbackSummary'] = state['revision']['lastClosedRevision'].get('feedbackSummary')


def reconstruct(project: Path):
    track_decision = project / '00C_底盘与切口决策.md'
    style_bible = project / '01A_风格圣经.md'
    mainline_spec = project / '01B_总主线与卷级推进.md'
    opening_design = project / '04A_开篇设计.md'
    world_ledger = project / '05B_世界规则账本.md'
    foreshadow_ledger = project / '05C_伏笔回收台账.md'
    relationship_ledger = project / '05D_关系状态表.md'
    resource_ledger = project / '05E_能力与资源变化表.md'
    timeline_artifact = project / TIMELINE_ARTIFACT
    foreshadow_triples_artifact = project / FORESHADOW_TRIPLES_ARTIFACT
    theory_of_mind_artifact = project / THEORY_OF_MIND_ARTIFACT
    consistency_artifact = project / CONSISTENCY_ARTIFACT

    track_text = track_decision.read_text(encoding='utf-8') if exists_nonempty(track_decision) else None
    style_text = style_bible.read_text(encoding='utf-8') if exists_nonempty(style_bible) else None

    state = {
        'project': {
            'title': project.name,
            'rootPath': str(project),
        },
        'workflow': {
            'currentStage': 'discovery',
            'currentSubstage': None,
            'lastCompletedStage': None,
            'nextStage': 'discovery',
            'status': 'reconstructed',
        },
        'approvals': {
            'discoveryApproved': False,
            'planningApproved': False,
            'characterApproved': False,
            'openingApproved': False,
            'draftingApproved': False,
            'polishingApproved': False,
            'proofreadingApproved': False,
            'finalApproved': False,
            'titleConfirmed': False,
            'workingTitleApproved': False,
        },
        'artifacts': {
            'hotSearchScan': exists_nonempty(project / '00A_热点扫描.md'),
            'userPreference': exists_nonempty(project / '00B_用户偏好.md'),
            'topicReport': exists_nonempty(project / '00_选题报告.md'),
            'trackDecision': exists_nonempty(track_decision),
            'ideaDoc': exists_nonempty(project / '01_想法.md'),
            'styleBible': exists_nonempty(style_bible),
            'mainlineSpec': exists_nonempty(mainline_spec),
            'outlineDoc': exists_nonempty(project / '02_大纲.md'),
            'characterSummary': exists_nonempty(project / '03_人物小传.md'),
            'chapterSkeleton': exists_nonempty(project / '04_章节骨架.md'),
            'openingDesign': exists_nonempty(opening_design),
            'recapDoc': exists_nonempty(project / '05_前情回顾.md'),
            'proofreadingReport': exists_nonempty(project / PROOFREADING_REPORT),
            'worldLedger': exists_nonempty(world_ledger),
            'foreshadowLedger': exists_nonempty(foreshadow_ledger),
            'relationshipLedger': exists_nonempty(relationship_ledger),
            'resourceLedger': exists_nonempty(resource_ledger),
            'characterFiles': count_md(project / 'characters') > 0,
            'manuscriptFiles': count_md(project / 'manuscript') > 0,
            'feishuSynced': False,
        },
        'batch': {
            **default_batch(),
            'chapterPlanExists': exists_nonempty(project / '05_本轮章节规划.md'),
            'recapUpdated': exists_nonempty(project / '05_前情回顾.md'),
        },
        'review': {
            **default_review(),
        },
        'revision': {
            **default_revision(),
        },
        'autoPilot': {
            **default_autopilot(),
        },
        'narrativeIntelligence': {
            **default_narrative_intelligence(),
        },
        'blockingIssues': [],
        'notes': {
            'platformProfile': detect_first_keyword(style_text or track_text, ('起点模式', '番茄模式', '通用模式')),
            'primaryTrack': detect_first_keyword(
                track_text,
                ('规则异变都市', '家族势力成长修仙', '高设定悬疑奇幻'),
            ),
            'secondaryFlavor': detect_first_keyword(
                track_text,
                ('悬疑调查', '势力经营', '认知博弈'),
            ),
            'styleBibleVersion': 'v1' if exists_nonempty(style_bible) else None,
        },
    }

    if all(
        exists_nonempty(artifact)
        for artifact in (
            timeline_artifact,
            foreshadow_triples_artifact,
            theory_of_mind_artifact,
            consistency_artifact,
        )
    ):
        state['narrativeIntelligence']['timeline']['enabled'] = True

    a = state['artifacts']
    if a['topicReport']:
        state['workflow']['lastCompletedStage'] = 'discovery'
        state['workflow']['currentStage'] = 'story-planning'
        state['workflow']['nextStage'] = 'story-planning'
    if a['outlineDoc']:
        state['workflow']['lastCompletedStage'] = 'story-planning'
        state['workflow']['currentStage'] = 'character-system'
        state['workflow']['nextStage'] = 'character-system'
    if a['characterFiles'] or a['characterSummary']:
        state['workflow']['lastCompletedStage'] = 'character-system'
        state['workflow']['currentStage'] = 'drafting'
        state['workflow']['nextStage'] = 'drafting'
        state['workflow']['currentSubstage'] = 'opening-design'
    if a['openingDesign'] and not a['manuscriptFiles']:
        state['workflow']['currentSubstage'] = 'opening-review'
    if a['manuscriptFiles']:
        state['workflow']['lastCompletedStage'] = 'drafting'
        state['workflow']['currentStage'] = 'polishing'
        state['workflow']['nextStage'] = 'polishing'
        state['workflow']['currentSubstage'] = None
        state['approvals']['openingApproved'] = True
        state['batch']['active'] = True
        state['batch']['draftComplete'] = True
    if a['recapDoc']:
        state['workflow']['lastCompletedStage'] = 'proofreading'
        state['workflow']['currentStage'] = 'final-review'
        state['workflow']['nextStage'] = 'final-review'
        state['workflow']['currentSubstage'] = None
        state['approvals']['openingApproved'] = True
        state['batch']['active'] = True
        state['batch']['draftComplete'] = True
        state['batch']['polishingComplete'] = True
        state['batch']['proofreadingComplete'] = True

    report = project / '07_终审报告.md'
    if exists_nonempty(report):
        report_text = report.read_text(encoding='utf-8')
        decision_values = extract_section_value(report_text, '## 最终结论')
        delivery_values = extract_section_value(report_text, '## 是否可交付')
        blockers = normalize_report_list(extract_section_value(report_text, '## 阻塞问题'))
        summary = extract_summary(decision_values)

        state['review']['finalDecision'] = decision_values[0] if decision_values else None
        state['review']['finalDeliveryReady'] = parse_explicit_bool(delivery_values[0]) if delivery_values else False
        state['review']['finalBlockingIssues'] = blockers
        state['review']['finalReviewSummary'] = summary
        state['workflow']['lastCompletedStage'] = 'proofreading'
        state['workflow']['currentStage'] = 'final-review'
        state['workflow']['nextStage'] = None
        state['workflow']['currentSubstage'] = None
        state['approvals']['openingApproved'] = True
        state['batch']['active'] = True
        state['batch']['draftComplete'] = True
        state['batch']['polishingComplete'] = True
        state['batch']['proofreadingComplete'] = True

    apply_revision_doc_state(project, state)
    return state


def normalize_supervisor_state(normalized: dict):
    workflow = normalized.setdefault('workflow', {})
    if workflow.get('status') not in WORKFLOW_STATUSES:
        workflow['status'] = 'collecting_inputs'

    review = default_review()
    review.update(normalized.get('review', {}))
    review['pendingArtifactPaths'] = normalize_path_list(review.get('pendingArtifactPaths'))
    review['activeBranches'] = normalize_path_list(review.get('activeBranches'))
    review['brainstormActive'] = bool(review.get('brainstormActive', False))
    normalized['review'] = review

    artifacts = normalized.setdefault('artifacts', {})
    artifacts['proofreadingReport'] = bool(artifacts.get('proofreadingReport'))

    if review['pendingArtifactPaths']:
        workflow['status'] = 'awaiting_user_approval'

    return normalized


def main():
    if len(sys.argv) < 2:
        print('Usage: load_project_state.py <项目目录>')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    state_file = project / '.novel-state.json'
    if state_file.exists():
        data = normalize_supervisor_state(normalize_state(json.loads(state_file.read_text(encoding='utf-8')), project))
        state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return

    data = normalize_supervisor_state(normalize_state(reconstruct(project), project))
    state_file.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
