#!/usr/bin/env python3
import json
import sys
from pathlib import Path

from revision_utils import clear_revision_blockers, load_state, now_iso, reset_active_revision_fields, save_state, set_revision_blocker, write_revision_doc


def main():
    if len(sys.argv) < 3:
        print('Usage: complete_revision_cycle.py <项目目录> <result_pending|close|reject> [summary]')
        sys.exit(1)

    project = Path(sys.argv[1]).expanduser()
    action = sys.argv[2]
    summary = ' '.join(sys.argv[3:]).strip() if len(sys.argv) > 3 else ''

    try:
        data = load_state(project)
    except FileNotFoundError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    revision = data['revision']
    if not revision.get('active'):
        print('ERROR: no active revision', file=sys.stderr)
        sys.exit(2)

    if action == 'result_pending':
        if revision.get('currentRevisionGate') != 'awaiting_revision_plan_approval':
            print('ERROR: revision is not waiting for plan approval', file=sys.stderr)
            sys.exit(2)
        if not summary:
            print('ERROR: result summary is required', file=sys.stderr)
            sys.exit(2)
        revision['resultSummary'] = summary
        revision['currentRevisionGate'] = 'awaiting_revision_result_approval'
        revision['awaitingUserApproval'] = True
        set_revision_blocker(data, revision['currentRevisionGate'])
    elif action == 'close':
        if revision.get('currentRevisionGate') != 'awaiting_revision_result_approval':
            print('ERROR: revision result is not awaiting approval', file=sys.stderr)
            sys.exit(2)
        if not revision.get('resultSummary'):
            print('ERROR: result summary is missing', file=sys.stderr)
            sys.exit(2)

        last_closed = {
            'feedbackType': revision.get('feedbackType'),
            'feedbackSummary': revision.get('feedbackSummary'),
            'affectedStages': list(revision.get('affectedStages', [])),
            'affectedFiles': list(revision.get('affectedFiles', [])),
            'overrideMode': revision.get('overrideMode'),
            'scopeSummary': revision.get('scopeSummary'),
            'conflictSummary': revision.get('conflictSummary'),
            'revisionPlanSummary': revision.get('revisionPlanSummary'),
            'resultSummary': revision.get('resultSummary'),
            'closedAt': now_iso(),
            'closeMode': '用户确认',
        }
        data['review']['lastRevisionFocus'] = revision.get('feedbackSummary')
        reset_active_revision_fields(revision)
        revision['lastClosedRevision'] = last_closed
        clear_revision_blockers(data)
    elif action == 'reject':
        if revision.get('currentRevisionGate') != 'awaiting_revision_result_approval':
            print('ERROR: revision result is not awaiting approval', file=sys.stderr)
            sys.exit(2)
        if not summary:
            print('ERROR: rejection reason is required', file=sys.stderr)
            sys.exit(2)
        data['review']['lastRejectedReason'] = summary
        revision['resultSummary'] = None
        revision['currentRevisionGate'] = 'awaiting_revision_plan_approval'
        revision['awaitingUserApproval'] = True
        set_revision_blocker(data, revision['currentRevisionGate'])
    else:
        print(f'ERROR: unknown action: {action}', file=sys.stderr)
        sys.exit(2)

    save_state(project, data)
    saved = load_state(project)
    write_revision_doc(project, saved)
    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
