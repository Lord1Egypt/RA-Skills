#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from autopilot_utils import record_autopilot_progress, stop_autopilot_with_blockers, summarize_chapter_progress
from chapter_progress_utils import apply_result_to_chapters
from narrative_checker import refresh_cliche_findings, refresh_consistency_findings
from narrative_intelligence_utils import sync_narrative_intelligence
from revision_utils import load_state, save_state
from stage_execution_utils import (
    base_result_summary_fields,
    ensure_project,
    now_iso,
    read_json_file,
    validate_bundle_and_result,
)
from stage_persistence_utils import PROOFREADING_REPORT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Apply a validated subagent stage result into project state.')
    parser.add_argument('project')
    parser.add_argument('--bundle-file', required=True)
    parser.add_argument('--result-file', required=True)
    return parser.parse_args()


def stage_gate(stage: str) -> str:
    return {
        'drafting': 'waiting_draft_feedback',
        'polishing': 'waiting_polishing_feedback',
        'proofreading': 'waiting_proofreading_feedback',
    }[stage]


def delegation_blockers(validated: dict[str, object]) -> list[str]:
    result = validated['result']
    if validated['stage'] == 'proofreading' and result.get('status') == 'completed':
        return list(result.get('blockers') or [])
    return list(result.get('blockedReasons') or [])


def should_sync_narrative_intelligence(stage: str, result: dict[str, object], batch: dict) -> bool:
    if result.get('status') != 'completed':
        return False
    if stage != 'proofreading':
        return True
    return bool(batch.get('proofreadingComplete'))


def apply_validated_state(data: dict, validated: dict[str, object], project: Path | None = None) -> None:
    stage = validated['stage']
    package = validated['package']
    result = validated['result']
    chapter_labels = list(package['requiredInputs']['chapterLabels'])

    batch = data.setdefault('batch', {})
    for key, value in base_result_summary_fields().items():
        batch.setdefault(key, value if not isinstance(value, list) else list(value))

    apply_result_to_chapters(
        batch,
        stage,
        chapter_labels,
        package['targetFiles'],
        result,
    )
    autopilot_progress_summary = summarize_chapter_progress(batch, chapter_labels)
    blockers = delegation_blockers(validated)
    batch['lastDelegatedStage'] = stage
    batch['lastDelegatedScope'] = package.get('batchRange')
    batch['lastDelegationStatus'] = result.get('status')
    batch['lastDelegationSummary'] = result.get('summary')
    batch['lastDelegationBlockers'] = blockers
    batch['lastDelegationRisks'] = list(result.get('risks') or [])
    batch['lastDelegatedAt'] = now_iso()

    workflow = data.setdefault('workflow', {})
    review = data.setdefault('review', {})
    artifacts = data.setdefault('artifacts', {})
    workflow['status'] = 'awaiting_user_approval' if result['status'] == 'completed' else 'blocked'

    if stage == 'drafting' and result['status'] == 'completed':
        batch['draftComplete'] = True
        review['currentGate'] = stage_gate(stage)
    elif stage == 'polishing' and result['status'] == 'completed':
        batch['polishingComplete'] = True
        review['currentGate'] = stage_gate(stage)
    elif stage == 'proofreading' and result['status'] == 'completed':
        batch['proofreadingComplete'] = result.get('judgment') != 'needs revision'
        review['currentGate'] = stage_gate(stage)
        review['pendingArtifactPaths'] = [PROOFREADING_REPORT]
        review['lastPersistedStage'] = 'proofreading'
        review['lastPersistedAt'] = now_iso()
        artifacts['proofreadingReport'] = True

    if should_sync_narrative_intelligence(stage, result, batch):
        sync_project = Path(project) if project is not None else None
        project_root = data.get('project', {}).get('rootPath')
        if sync_project is None and project_root:
            sync_project = Path(project_root)
        if sync_project is not None:
            sync_narrative_intelligence(
                sync_project,
                data,
                stage=stage,
                chapter_labels=chapter_labels,
            )
            if stage == 'proofreading':
                refresh_consistency_findings(sync_project, data)
                refresh_cliche_findings(sync_project, data)

    if result['status'] == 'completed':
        record_autopilot_progress(data, autopilot_progress_summary)
    elif result['status'] in {'blocked', 'needs_clarification'}:
        stop_autopilot_with_blockers(
            data,
            blocked_reasons=blockers,
            summary=result.get('summary'),
        )


def main() -> None:
    args = parse_args()
    try:
        project = ensure_project(Path(args.project))
        bundle = read_json_file(Path(args.bundle_file))
        result = read_json_file(Path(args.result_file))
        validated = validate_bundle_and_result(project, bundle, result)
        data = load_state(project)
        apply_validated_state(data, validated, project)
        save_state(project, data)
        saved = load_state(project)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)
    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
