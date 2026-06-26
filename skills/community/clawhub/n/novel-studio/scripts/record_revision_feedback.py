#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from narrative_checker import build_revision_actions
from revision_utils import load_state, reset_active_revision_fields, save_state, set_revision_blocker, write_revision_doc


def main():
    if len(sys.argv) < 5:
        print('Usage: record_revision_feedback.py <项目目录> <feedbackType> <overrideMode:add_on|override> <feedbackSummary>')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    feedback_type = sys.argv[2]
    override_mode = sys.argv[3]
    summary = ' '.join(sys.argv[4:]).strip()

    if override_mode not in {'add_on', 'override'}:
        print('ERROR: overrideMode must be add_on or override', file=sys.stderr)
        sys.exit(2)
    if not summary:
        print('ERROR: feedbackSummary is required', file=sys.stderr)
        sys.exit(2)

    try:
        data = load_state(project)
    except FileNotFoundError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    revision = data['revision']
    if revision.get('active'):
        print('ERROR: active revision already exists', file=sys.stderr)
        sys.exit(2)

    reset_active_revision_fields(revision)
    revision.update({
        'active': True,
        'feedbackType': feedback_type,
        'feedbackSummary': summary,
        'affectedStages': [],
        'affectedFiles': [],
        'overrideMode': override_mode,
        'scopeSummary': None,
        'conflictSummary': None,
        'revisionPlanSummary': None,
        'resultSummary': None,
        'currentRevisionGate': 'awaiting_revision_scope_confirmation',
        'awaitingUserApproval': True,
    })
    actions = build_revision_actions(data)
    if actions:
        data.setdefault('narrativeIntelligence', {})['revisionActions'] = actions
        revision['scopeSummary'] = '；'.join(action['summary'] for action in actions[:3])
        revision['revisionPlanSummary'] = '；'.join(action['action'] for action in actions[:3])
        revision['affectedFiles'] = sorted(
            {
                *revision.get('affectedFiles', []),
                *(action['targetFile'] for action in actions if action.get('targetFile')),
            }
        )
    data['review']['lastUserFeedbackSummary'] = summary
    data['review']['lastRejectedReason'] = None
    set_revision_blocker(data, revision['currentRevisionGate'])

    save_state(project, data)
    saved = load_state(project)
    write_revision_doc(project, saved)
    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
