#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

from autopilot_utils import default_autopilot, normalize_autopilot
from chapter_progress_utils import (
    default_progress_fields,
    extract_chapter_labels_from_plan,
    initialize_chapter_tasks,
    normalize_progress_batch,
)
from stage_persistence_utils import now_iso

REVISION_DOC = '06_反馈与修订.md'
REVISION_BLOCKER_PREFIX = 'Formal revision active:'


def default_review() -> dict:
    return {
        'currentGate': None,
        'pendingArtifactPaths': [],
        'lastPersistedStage': None,
        'lastPersistedAt': None,
        'brainstormActive': False,
        'brainstormMode': None,
        'brainstormFocus': None,
        'brainstormRound': None,
        'selectedBranch': None,
        'activeBranches': [],
        'lastUserFeedbackSummary': None,
        'lastRevisionFocus': None,
        'lastRejectedReason': None,
        'lastDriftRiskSummary': None,
        'lastLedgerRiskSummary': None,
        'finalDecision': None,
        'finalDeliveryReady': False,
        'finalBlockingIssues': [],
        'finalReviewSummary': None,
    }


def default_batch() -> dict:
    return {
        'active': False,
        'chapterRange': None,
        'chapterCount': None,
        'scopeConfirmed': False,
        'chapterPlanExists': False,
        'chapterPlanApproved': False,
        'draftComplete': False,
        'polishingComplete': False,
        'proofreadingComplete': False,
        'recapUpdated': False,
        'awaitingNextBatchDecision': False,
        'focus': None,
        'attractionPoints': [],
        'climaxTarget': None,
        'lastDelegatedStage': None,
        'lastDelegatedScope': None,
        'lastDelegationStatus': None,
        'lastDelegationSummary': None,
        'lastDelegationBlockers': [],
        'lastDelegationRisks': [],
        'lastDelegatedAt': None,
        **default_progress_fields(),
    }


def default_approvals() -> dict:
    return {
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
    }


def default_artifacts() -> dict:
    return {
        'hotSearchScan': False,
        'userPreference': False,
        'topicReport': False,
        'trackDecision': False,
        'ideaDoc': False,
        'styleBible': False,
        'mainlineSpec': False,
        'outlineDoc': False,
        'characterSummary': False,
        'chapterSkeleton': False,
        'openingDesign': False,
        'recapDoc': False,
        'proofreadingReport': False,
        'worldLedger': False,
        'foreshadowLedger': False,
        'relationshipLedger': False,
        'resourceLedger': False,
        'characterFiles': False,
        'manuscriptFiles': False,
        'feishuSynced': False,
    }


def default_notes() -> dict:
    return {
        'workingTitle': None,
        'finalTitle': None,
        'platformProfile': None,
        'primaryTrack': None,
        'secondaryFlavor': None,
        'styleBibleVersion': None,
    }


def default_narrative_intelligence() -> dict:
    return {
        'timeline': {
            'enabled': False,
            'lastUpdatedBatch': None,
            'lastTouchedChapters': [],
            'openTemporalRisks': [],
        },
        'cfpg': {
            'foreshadowTriples': [],
            'tripleCounts': {
                'total': 0,
                'pending': 0,
                'fulfilled': 0,
                'broken': 0,
                'expired': 0,
            },
            'lastUpdatedBatch': None,
        },
        'theoryOfMind': {
            'characterBeliefs': [],
            'beliefConflicts': [],
            'lastUpdatedBatch': None,
        },
        'consistency': {
            'contradictionCandidates': [],
            'evidenceChains': [],
            'lastCheckStage': None,
            'openCriticalIssues': [],
        },
        'revisionActions': [],
        'styleRisk': {
            'clichePatterns': [],
            'lastCokeScore': None,
            'noveltyAxes': [],
            'lastClicheScanStage': None,
        },
    }


def base_state(project: Path) -> dict:
    return {
        'project': {'title': project.name, 'rootPath': str(project)},
        'workflow': {
            'currentStage': None,
            'currentSubstage': None,
            'lastCompletedStage': None,
            'nextStage': None,
            'status': 'collecting_inputs',
        },
        'approvals': default_approvals(),
        'artifacts': default_artifacts(),
        'batch': default_batch(),
        'review': default_review(),
        'revision': {},
        'autoPilot': default_autopilot(),
        'narrativeIntelligence': default_narrative_intelligence(),
        'blockingIssues': [],
        'notes': default_notes(),
        'updatedAt': now_iso(),
    }


def default_revision() -> dict:
    return {
        'active': False,
        'feedbackType': None,
        'feedbackSummary': None,
        'affectedStages': [],
        'affectedFiles': [],
        'overrideMode': None,
        'scopeSummary': None,
        'conflictSummary': None,
        'revisionPlanSummary': None,
        'resultSummary': None,
        'currentRevisionGate': None,
        'awaitingUserApproval': False,
        'lastClosedRevision': None,
    }


def normalize_state(data: dict, project: Path) -> dict:
    normalized = base_state(project)
    normalized.update(data)
    raw_approvals = data.get('approvals') if isinstance(data.get('approvals'), dict) else {}

    approvals = default_approvals()
    approvals.update(normalized.get('approvals', {}))

    artifacts = default_artifacts()
    artifacts.update(normalized.get('artifacts', {}))
    normalized['artifacts'] = artifacts

    review = default_review()
    review.update(normalized.get('review', {}))
    review['finalBlockingIssues'] = list(review.get('finalBlockingIssues', []))
    normalized['review'] = review

    revision = default_revision()
    revision.update(normalized.get('revision', {}))
    normalized['revision'] = revision

    normalized['autoPilot'] = normalize_autopilot(normalized.get('autoPilot'))

    batch = default_batch()
    batch.update(normalized.get('batch', {}))
    batch['attractionPoints'] = list(batch.get('attractionPoints', []))
    batch['lastDelegationBlockers'] = list(batch.get('lastDelegationBlockers', []))
    batch['lastDelegationRisks'] = list(batch.get('lastDelegationRisks', []))
    normalize_progress_batch(batch)
    chapter_plan = project / '05_本轮章节规划.md'
    plan_text = chapter_plan.read_text(encoding='utf-8') if chapter_plan.exists() else ''
    batch['chapterPlanExists'] = bool(plan_text.strip())
    if batch.get('chapterPlanApproved'):
        chapter_labels = extract_chapter_labels_from_plan(plan_text)
        if chapter_labels and not batch.get('chapterTasks'):
            initialize_chapter_tasks(batch, plan_text)
    normalized['batch'] = batch

    notes = default_notes()
    notes.update(normalized.get('notes', {}))
    normalized['notes'] = notes

    narrative_intelligence = default_narrative_intelligence()
    narrative_intelligence.update(normalized.get('narrativeIntelligence', {}))

    timeline = default_narrative_intelligence()['timeline']
    timeline.update(narrative_intelligence.get('timeline', {}))
    timeline['lastTouchedChapters'] = list(timeline.get('lastTouchedChapters', []))
    timeline['openTemporalRisks'] = list(timeline.get('openTemporalRisks', []))
    narrative_intelligence['timeline'] = timeline

    cfpg = default_narrative_intelligence()['cfpg']
    cfpg.update(narrative_intelligence.get('cfpg', {}))
    cfpg['foreshadowTriples'] = list(cfpg.get('foreshadowTriples', []))
    triple_counts = default_narrative_intelligence()['cfpg']['tripleCounts']
    triple_counts.update(cfpg.get('tripleCounts', {}))
    cfpg['tripleCounts'] = triple_counts
    narrative_intelligence['cfpg'] = cfpg

    theory_of_mind = default_narrative_intelligence()['theoryOfMind']
    theory_of_mind.update(narrative_intelligence.get('theoryOfMind', {}))
    theory_of_mind['characterBeliefs'] = list(theory_of_mind.get('characterBeliefs', []))
    theory_of_mind['beliefConflicts'] = list(theory_of_mind.get('beliefConflicts', []))
    narrative_intelligence['theoryOfMind'] = theory_of_mind

    consistency = default_narrative_intelligence()['consistency']
    consistency.update(narrative_intelligence.get('consistency', {}))
    consistency['contradictionCandidates'] = list(consistency.get('contradictionCandidates', []))
    consistency['evidenceChains'] = list(consistency.get('evidenceChains', []))
    consistency['openCriticalIssues'] = list(consistency.get('openCriticalIssues', []))
    narrative_intelligence['consistency'] = consistency

    narrative_intelligence['revisionActions'] = list(narrative_intelligence.get('revisionActions', []))

    style_risk = default_narrative_intelligence()['styleRisk']
    style_risk.update(narrative_intelligence.get('styleRisk', {}))
    style_risk['clichePatterns'] = list(style_risk.get('clichePatterns', []))
    style_risk['noveltyAxes'] = list(style_risk.get('noveltyAxes', []))
    narrative_intelligence['styleRisk'] = style_risk

    normalized['narrativeIntelligence'] = narrative_intelligence

    if (
        'openingApproved' not in raw_approvals
        and (
            batch.get('draftComplete')
            or artifacts.get('manuscriptFiles')
            or normalized.get('workflow', {}).get('currentStage') in {'polishing', 'proofreading', 'final-review'}
        )
    ):
        approvals['openingApproved'] = True

    normalized['approvals'] = approvals
    normalized.setdefault('blockingIssues', [])
    return normalized


def load_state(project: Path) -> dict:
    if not project.exists() or not project.is_dir():
        raise FileNotFoundError(f'project not found: {project}')

    state_file = project / '.novel-state.json'
    if state_file.exists():
        data = json.loads(state_file.read_text(encoding='utf-8'))
    else:
        data = base_state(project)
    return normalize_state(data, project)


def save_state(project: Path, data: dict) -> None:
    data = normalize_state(data, project)
    data['updatedAt'] = now_iso()
    (project / '.novel-state.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')


def parse_csv(value: str) -> list[str]:
    return [item.strip() for item in value.split(',') if item.strip()]


def reset_active_revision_fields(revision: dict) -> None:
    last_closed = revision.get('lastClosedRevision')
    revision.clear()
    revision.update(default_revision())
    revision['lastClosedRevision'] = last_closed


def gate_blocker(gate: str | None) -> str | None:
    if not gate:
        return None
    return f'{REVISION_BLOCKER_PREFIX} {gate}'


def clear_revision_blockers(data: dict) -> None:
    blockers = data.setdefault('blockingIssues', [])
    data['blockingIssues'] = [b for b in blockers if not b.startswith(REVISION_BLOCKER_PREFIX)]


def set_revision_blocker(data: dict, gate: str | None) -> None:
    clear_revision_blockers(data)
    blocker = gate_blocker(gate)
    if blocker:
        data.setdefault('blockingIssues', []).append(blocker)


def format_list(items: list[str]) -> str:
    return ', '.join(items) if items else '无'


def render_revision_doc(data: dict) -> str:
    revision = data['revision']
    if revision.get('active'):
        if revision.get('currentRevisionGate') == 'awaiting_revision_scope_confirmation':
            status = '等待确认范围'
        elif revision.get('currentRevisionGate') == 'awaiting_revision_plan_approval':
            status = '等待确认修订计划'
        elif revision.get('currentRevisionGate') == 'awaiting_revision_result_approval':
            status = '等待确认修订结果'
        else:
            status = '进行中'
    else:
        status = '已关闭'

    closed = revision.get('lastClosedRevision') or {}
    return f"""# 06_反馈与修订

## 当前正式修订
- 状态：{status}
- 反馈类型：{revision.get('feedbackType') or '无'}
- 反馈摘要：{revision.get('feedbackSummary') or '无'}
- 处理模式：{revision.get('overrideMode') or '无'}
- 影响阶段：{format_list(revision.get('affectedStages', []))}
- 影响文件：{format_list(revision.get('affectedFiles', []))}
- 范围说明：{revision.get('scopeSummary') or '无'}
- 冲突说明：{revision.get('conflictSummary') or '无'}
- 修订计划：{revision.get('revisionPlanSummary') or '无'}
- 修订结果：{revision.get('resultSummary') or '无'}
- 当前修订 gate：{revision.get('currentRevisionGate') or '无'}
- 最近更新时间：{data.get('updatedAt', '未知')}

## 最近关闭的修订
### {closed.get('closedAt') or '无'} {closed.get('feedbackType') or ''}
- 反馈摘要：{closed.get('feedbackSummary') or '无'}
- 影响范围：{format_list(closed.get('affectedFiles', []))}
- 修订结果：{closed.get('resultSummary') or '无'}
- 关闭方式：{closed.get('closeMode') or '无'}
"""


def write_revision_doc(project: Path, data: dict) -> None:
    (project / REVISION_DOC).write_text(render_revision_doc(data), encoding='utf-8')
