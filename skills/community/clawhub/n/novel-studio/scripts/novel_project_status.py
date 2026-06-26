#!/usr/bin/env python3
from pathlib import Path
import json, sys

from chapter_progress_utils import build_progress_report, render_chapter_progress
from revision_utils import normalize_state


def load_state(project: Path):
    state_file = project / '.novel-state.json'
    if not state_file.exists():
        return None
    return normalize_state(json.loads(state_file.read_text(encoding='utf-8')), project)


def exists(path: Path):
    return path.exists() and path.is_file() and path.read_text(encoding='utf-8').strip() != ''


def count_md(path: Path):
    return len(list(path.glob('*.md'))) if path.is_dir() else 0


def yn(v):
    return '是' if v else '否'


def gate_text(gate):
    mapping = {
        'waiting_discovery_feedback': '等待你确认 Discovery 阶段结果',
        'waiting_planning_feedback': '等待你确认 Planning 阶段结果',
        'waiting_character_feedback': '等待你确认人物体系结果',
        'waiting_opening_feedback': '等待你确认 Opening Gate',
        'waiting_opening_gate_approval': '等待你确认 Opening Gate',
        'waiting_draft_feedback': '等待你确认本轮初稿结果',
        'waiting_chapter_plan_approval': '等待你确认本轮章节规划',
        'waiting_polishing_feedback': '等待你确认本轮润色结果',
        'waiting_proofreading_feedback': '等待你确认本轮校对结果',
        'waiting_final_review_feedback': '等待你确认终审结果',
        'awaiting_revision_scope_confirmation': '等待你确认修订范围',
        'awaiting_revision_plan_approval': '等待你确认修订计划',
        'awaiting_revision_result_approval': '等待你确认修订结果',
    }
    return mapping.get(gate, gate or '无')


def review_decision_text(review):
    return review.get('finalDecision') or '无'


def review_delivery_text(review):
    return yn(review.get('finalDeliveryReady', False))


def review_summary_text(review):
    return review.get('finalReviewSummary') or '无'


def review_blockers(review):
    return list(review.get('finalBlockingIssues') or [])


def narrative_summary_text(state: dict) -> str:
    intelligence = state.get('narrativeIntelligence', {})
    critical = len(intelligence.get('consistency', {}).get('openCriticalIssues', []))
    temporal = len(intelligence.get('timeline', {}).get('openTemporalRisks', []))
    return f'{critical} 条关键问题 / {temporal} 条时间风险'


def brainstorm_focus_text(review: dict) -> str:
    focus = review.get('brainstormFocus') or '无'
    round_label = review.get('brainstormRound') or '无'
    return f'{focus} / {round_label}'


def style_risk_summary_text(state: dict) -> str:
    style_risk = state.get('narrativeIntelligence', {}).get('styleRisk', {})
    cliche_count = len(style_risk.get('clichePatterns', []))
    novelty_count = len(style_risk.get('noveltyAxes', []))
    return f'{cliche_count} 条 / 新意轴：{novelty_count} 条'


def delegation_text(batch):
    stage = batch.get('lastDelegatedStage')
    status = batch.get('lastDelegationStatus')
    scope = batch.get('lastDelegatedScope')
    if not stage or not status:
        return '无'
    return f'{stage} / {status} / {scope or "无范围"}'


def autopilot_state_text(auto_pilot):
    if auto_pilot.get('active'):
        return '运行中'
    if auto_pilot.get('awaitingManualResume'):
        return '已停止'
    return '未开启'


def autopilot_goal_text(auto_pilot):
    goal_chapter = auto_pilot.get('goalChapter')
    if goal_chapter is None:
        return '无'
    if str(goal_chapter).endswith('结束'):
        return str(goal_chapter)
    return f'{goal_chapter}结束'


def rollback_stage_text(state):
    revision = state.get('revision', {})
    affected_stages = list(revision.get('affectedStages') or [])
    if affected_stages:
        return affected_stages[0]

    workflow = state.get('workflow', {})
    return workflow.get('lastCompletedStage') or workflow.get('currentStage') or '上游阶段'


def next_step(state, project: Path):
    workflow = state.get('workflow', {})
    batch = state.get('batch', {})
    review = state.get('review', {})
    revision = state.get('revision', {})
    approvals = state.get('approvals', {})

    if revision.get('active') and revision.get('awaitingUserApproval'):
        return f"先处理修订模式：{gate_text(revision.get('currentRevisionGate'))}"

    final_decision = review.get('finalDecision')
    final_blockers = review_blockers(review)
    final_delivery_ready = review.get('finalDeliveryReady', False)

    if final_decision == 'rework required':
        return f'终审要求返工：请回退到 {rollback_stage_text(state)} 阶段处理后再重新进入终审。'
    if final_decision == 'conditional pass':
        if final_blockers:
            return '先解决终审阻塞项，再请求最终交付确认。'
        if final_delivery_ready and not approvals.get('finalApproved', False):
            return '请确认最终交付。'
        return '请先完成终审收尾项，再请求最终交付确认。'
    if final_decision == 'pass' and final_delivery_ready and not approvals.get('finalApproved', False):
        return '请确认最终交付。'
    if final_decision == 'pass' and not final_delivery_ready:
        return '终审已通过，但当前版本尚不可交付：请先补齐交付前收尾项。'

    if workflow.get('currentStage') == 'drafting' and not approvals.get('openingApproved', False):
        if not exists(project / '04A_开篇设计.md'):
            return '请先完成 04A_开篇设计.md 并确认 Opening Gate，再进入本轮章节规划与正文。'
        return '请先完成并确认 Opening Gate，再进入本轮章节规划与正文。'

    if review.get('currentGate'):
        return gate_text(review.get('currentGate'))
    if workflow.get('currentStage') == 'discovery' and not state.get('approvals', {}).get('discoveryApproved', False):
        return '请先确认 Discovery stage 的结论报告，再进入 Story planning stage。'
    if workflow.get('currentStage') == 'story-planning' and not state.get('approvals', {}).get('planningApproved', False):
        return '请先确认想法与大纲，再进入 Character system stage。'
    if workflow.get('currentStage') == 'character-system' and not state.get('approvals', {}).get('characterApproved', False):
        return '请先确认人物体系，再进入 Drafting stage。'
    if workflow.get('currentStage') == 'drafting':
        if not batch.get('scopeConfirmed', False):
            return '请先确认本轮要写的章节范围与章节数。'
        if not batch.get('chapterPlanApproved', False):
            return '请先确认本轮章节规划，再进入初稿阶段。'
        if not batch.get('draftComplete', False):
            return '进入当前批次初稿撰写。'
        if not batch.get('polishingComplete', False):
            return '进入当前批次润色与实质性点评。'
        if not batch.get('proofreadingComplete', False):
            return '进入当前批次一致性审查与终审。'
        if not batch.get('recapUpdated', False):
            return '更新 05_前情回顾.md，关闭本轮批次。'
        if batch.get('awaitingNextBatchDecision', False):
            return '请决定是否继续下一轮批次写作。'
    return '按当前阶段继续推进，或先查看最近阻塞项。'


def main():
    if len(sys.argv) < 2:
        print('Usage: novel_project_status.py <项目目录> [--brief|--json]')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    mode = sys.argv[2] if len(sys.argv) >= 3 else '--full'

    if not project.exists():
        print(f'ERROR: project not found: {project}')
        sys.exit(2)

    state = load_state(project)
    if not state:
        print('No .novel-state.json found. Run load_project_state.py first.')
        sys.exit(2)

    if mode == '--json':
        print(json.dumps(state, ensure_ascii=False, indent=2))
        return

    project_title = state.get('project', {}).get('title', project.name)
    current_title = state.get('notes', {}).get('finalTitle') or state.get('notes', {}).get('workingTitle') or project_title
    updated_at = state.get('updatedAt', '未知')
    workflow = state.get('workflow', {})
    approvals = state.get('approvals', {})
    batch = state.get('batch', {})
    review = state.get('review', {})
    revision = state.get('revision', {})
    auto_pilot = state.get('autoPilot', {})
    blockers = state.get('blockingIssues', [])
    current_gate = review.get('currentGate') or revision.get('currentRevisionGate')
    if workflow.get('currentStage') == 'drafting' and not approvals.get('openingApproved', False):
        current_gate = 'waiting_opening_gate_approval'

    if mode == '--brief':
        print(f'项目：{project_title}')
        print(f'当前阶段：{workflow.get("currentStage", "未知")}')
        print(f'当前子阶段：{workflow.get("currentSubstage") or "无"}')
        print(f'当前状态：{workflow.get("status") or "未知"}')
        print(f'当前卡点：{gate_text(current_gate)}')
        pending_artifacts = list(review.get('pendingArtifactPaths') or [])
        if pending_artifacts:
            print(f'待审批文件：{", ".join(pending_artifacts)}')
        if review.get('brainstormActive'):
            print(f'脑暴模式：{review.get("brainstormMode") or "无"}')
            print(f'脑暴焦点：{brainstorm_focus_text(review)}')
        print(f'当前批次范围：{batch.get("chapterRange") or "无"}')
        print(f'章节进度：{render_chapter_progress(batch)}')
        print(f'自动流程：{autopilot_state_text(auto_pilot)}')
        print(f'自动目标：{autopilot_goal_text(auto_pilot)}')
        print(f'自动流程最近进度：{auto_pilot.get("lastProgressSummary") or "无"}')
        print(f'自动流程停止原因：{auto_pilot.get("stopReason") or "无"}')
        print(f'叙事智能：{narrative_summary_text(state)}')
        print(f'套路风险：{style_risk_summary_text(state)}')
        pending_report = build_progress_report(batch.get('pendingProgressItems', []))
        if pending_report['summary']:
            print(f'待汇报变更：{pending_report["summary"]}')
        print(f'终审结论：{review_decision_text(review)}')
        print(f'可交付：{review_delivery_text(review)}')
        print(f'终审摘要：{review_summary_text(review)}')
        print(f'最近委派：{delegation_text(batch)}')
        print(f'最近正式反馈：{revision.get("feedbackSummary") or review.get("lastUserFeedbackSummary") or "无"}')
        print(f'建议下一步：{next_step(state, project)}')
        return

    print('[项目基础]')
    print(f'项目：{project_title}')
    print(f'当前标题：{current_title}')
    print(f'项目路径：{project}')
    print(f'最近更新时间：{updated_at}')
    print()

    print('[流程位置]')
    print(f'当前阶段：{workflow.get("currentStage", "未知")}')
    print(f'当前子阶段：{workflow.get("currentSubstage") or "无"}')
    print(f'上一个完成阶段：{workflow.get("lastCompletedStage") or "无"}')
    print(f'下一阶段：{workflow.get("nextStage") or "无"}')
    print(f'当前状态：{workflow.get("status") or "未知"}')
    print()

    print('[当前批次]')
    print(f'当前批次是否激活：{yn(batch.get("active", False))}')
    print(f'范围：{batch.get("chapterRange") or "无"}')
    print(f'章节数：{batch.get("chapterCount") or "无"}')
    print(f'focus：{batch.get("focus") or "无"}')
    print(f'attraction points：{", ".join(batch.get("attractionPoints", [])) or "无"}')
    print(f'climax target：{batch.get("climaxTarget") or "无"}')
    print(f'最近委派：{delegation_text(batch)}')
    print(f'委派摘要：{batch.get("lastDelegationSummary") or "无"}')
    print(f'委派阻塞：{", ".join(batch.get("lastDelegationBlockers", [])) or "无"}')
    print(f'委派风险：{", ".join(batch.get("lastDelegationRisks", [])) or "无"}')
    print(f'自动流程：{autopilot_state_text(auto_pilot)}')
    print(f'自动目标：{autopilot_goal_text(auto_pilot)}')
    print(f'自动流程最近进度：{auto_pilot.get("lastProgressSummary") or "无"}')
    print(f'自动流程停止原因：{auto_pilot.get("stopReason") or "无"}')
    print()

    print('[章节进度]')
    print(f'当前章节摘要：{render_chapter_progress(batch)}')
    pending_report = build_progress_report(batch.get('pendingProgressItems', []))
    print(f'待汇报变更：{pending_report["summary"] or "无"}')
    print()

    print('[审批状态]')
    print(f'discovery：{yn(approvals.get("discoveryApproved", False))}')
    print(f'planning：{yn(approvals.get("planningApproved", False))}')
    print(f'character：{yn(approvals.get("characterApproved", False))}')
    print(f'opening gate：{yn(approvals.get("openingApproved", False))}')
    print(f'batch scope：{yn(batch.get("scopeConfirmed", False))}')
    print(f'chapter plan：{yn(batch.get("chapterPlanApproved", False))}')
    print(f'draft：{yn(batch.get("draftComplete", False))}')
    print(f'polishing：{yn(batch.get("polishingComplete", False))}')
    print(f'proofreading：{yn(batch.get("proofreadingComplete", False))}')
    print(f'final：{yn(approvals.get("finalApproved", False))}')
    print()

    closed_revision = revision.get('lastClosedRevision') or {}

    print('[修订状态]')
    print(f'当前 review gate：{gate_text(current_gate)}')
    print(f'最近正式反馈：{revision.get("feedbackSummary") or review.get("lastUserFeedbackSummary") or "无"}')
    print(f'反馈类型：{revision.get("feedbackType") or "无"}')
    print(f'处理模式：{revision.get("overrideMode") or "无"}')
    print(f'影响阶段：{", ".join(revision.get("affectedStages", [])) or "无"}')
    print(f'影响范围：{", ".join(revision.get("affectedFiles", [])) or "无"}')
    print(f'范围说明：{revision.get("scopeSummary") or "无"}')
    print(f'冲突说明：{revision.get("conflictSummary") or "无"}')
    print(f'修订计划：{revision.get("revisionPlanSummary") or "无"}')
    print(f'修订结果：{revision.get("resultSummary") or "无"}')
    print(f'当前是否修订模式：{yn(revision.get("active", False))}')
    print(f'当前修订 gate：{gate_text(revision.get("currentRevisionGate"))}')
    print(f'最近关闭修订：{closed_revision.get("feedbackSummary") or "无"}')
    print(f'最近关闭结果：{closed_revision.get("resultSummary") or "无"}')
    print()

    print('[终审状态]')
    print(f'终审结论：{review_decision_text(review)}')
    print(f'终审可交付：{review_delivery_text(review)}')
    print(f'终审摘要：{review_summary_text(review)}')
    print('终审阻塞项：')
    final_blockers = review_blockers(review)
    if final_blockers:
        for blocker in final_blockers:
            print(f'- {blocker}')
    else:
        print('- 无')
    print()

    intelligence = state.get('narrativeIntelligence', {})
    print('[叙事智能]')
    print(f'关键问题：{len(intelligence.get("consistency", {}).get("openCriticalIssues", []))}')
    print(f'时间风险：{len(intelligence.get("timeline", {}).get("openTemporalRisks", []))}')
    print()

    print('[阻塞项]')
    if blockers:
        for b in blockers:
            print(f'- {b}')
    else:
        print('- 无')
    print()

    print('[文件状态]')
    checks = [
        '00A_热点扫描.md', '00B_用户偏好.md', '00_选题报告.md', '00C_底盘与切口决策.md',
        '01_想法.md', '01A_风格圣经.md', '01B_总主线与卷级推进.md', '02_大纲.md',
        '03_人物小传.md', '04_章节骨架.md', '04A_开篇设计.md', '05_本轮章节规划.md',
        '05_前情回顾.md', '05B_世界规则账本.md', '05C_伏笔回收台账.md',
        '05D_关系状态表.md', '05E_能力与资源变化表.md'
    ]
    for name in checks:
        print(f'{name}：{"已生成" if exists(project / name) else "未生成"}')
    print(f'characters/：{count_md(project / "characters")}')
    print(f'manuscript/：{count_md(project / "manuscript")}')
    print()

    print('[建议下一步]')
    print(next_step(state, project))


if __name__ == '__main__':
    main()
