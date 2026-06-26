#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from autopilot_utils import (
    is_goal_chapter_proofreading_completed,
    normalize_bool,
    record_autopilot_progress,
    stop_autopilot,
    summarize_chapter_progress,
)
from chapter_progress_utils import advance_chapters_after_gate
from narrative_intelligence_utils import ensure_narrative_artifacts
from revision_utils import load_state, save_state

APPROVAL_TRANSITIONS = {
    'waiting_discovery_feedback': ('discovery', 'discoveryApproved', 'story-planning'),
    'waiting_planning_feedback': ('story-planning', 'planningApproved', 'character-system'),
    'waiting_character_feedback': ('character-system', 'characterApproved', 'drafting'),
    'waiting_opening_feedback': ('drafting', 'openingApproved', 'drafting'),
    'waiting_draft_feedback': ('drafting', 'draftingApproved', 'polishing'),
    'waiting_polishing_feedback': ('polishing', 'polishingApproved', 'proofreading'),
    'waiting_proofreading_feedback': ('proofreading', 'proofreadingApproved', 'final-review'),
    'waiting_final_review_feedback': ('final-review', 'finalApproved', None),
}


def final_review_ready_for_approval(review: dict) -> bool:
    decision = review.get('finalDecision')
    if decision not in {'pass', 'conditional pass'}:
        return False
    if not review.get('finalDeliveryReady', False):
        return False
    return not list(review.get('finalBlockingIssues') or [])


def proofreading_ready_for_approval(batch: dict) -> bool:
    return normalize_bool(batch.get('proofreadingComplete'), default=False)


def gate_approval_error(state: dict, gate: str) -> str | None:
    if gate not in APPROVAL_TRANSITIONS:
        return f'unsupported gate: {gate}'

    review = state['review']
    current_gate = review.get('currentGate')
    if current_gate != gate:
        return f'gate mismatch, expected currentGate={current_gate or "None"}, got {gate}'

    if gate == 'waiting_final_review_feedback' and not final_review_ready_for_approval(review):
        return 'final review is not ready for approval'
    if gate == 'waiting_proofreading_feedback' and not proofreading_ready_for_approval(state.get('batch', {})):
        return 'proofreading is not ready for approval'
    return None


def approve_gate_in_state(state: dict, gate: str) -> dict:
    error = gate_approval_error(state, gate)
    if error:
        raise ValueError(error)

    review = state['review']
    stage, approval_key, next_stage = APPROVAL_TRANSITIONS[gate]
    approved_chapter_labels = [
        task.get('chapterLabel')
        for task in state.get('batch', {}).get('chapterTasks', [])
        if isinstance(task, dict)
        and task.get('phase') == stage
        and task.get('phaseStatus') == 'awaiting_user_review'
        and task.get('chapterLabel')
    ]
    proofreading_accepted = gate != 'waiting_proofreading_feedback' or proofreading_ready_for_approval(
        state.get('batch', {})
    )

    state['approvals'][approval_key] = True
    if proofreading_accepted:
        advance_chapters_after_gate(state['batch'], gate)

    workflow = state['workflow']
    if gate == 'waiting_opening_feedback':
        workflow['currentSubstage'] = None
    else:
        workflow['lastCompletedStage'] = stage
    workflow['currentStage'] = next_stage
    workflow['nextStage'] = next_stage
    workflow['status'] = 'collecting_inputs'

    review['currentGate'] = None
    review['pendingArtifactPaths'] = []

    if proofreading_accepted:
        record_autopilot_progress(state, summarize_chapter_progress(state.get('batch', {}), approved_chapter_labels))
    if gate == 'waiting_proofreading_feedback' and proofreading_accepted and is_goal_chapter_proofreading_completed(state):
        stop_autopilot(state, 'goal_reached')

    return state


def approve_gate(project: Path, gate: str) -> dict:
    project = Path(project).expanduser()
    if not project.exists():
        raise FileNotFoundError(f'project not found: {project}')

    state = load_state(project)
    approve_gate_in_state(state, gate)
    if gate == 'waiting_planning_feedback':
        ensure_narrative_artifacts(project)
        state['narrativeIntelligence']['timeline']['enabled'] = True
    save_state(project, state)
    return load_state(project)


def main() -> int:
    if len(sys.argv) < 3:
        print('Usage: approve_stage_gate.py <项目目录> <gate>')
        return 1

    project = Path(sys.argv[1]).expanduser()
    gate = sys.argv[2].strip()

    try:
        approve_gate(project, gate)
    except FileNotFoundError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    print(f'APPROVED: {gate}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
