#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from revision_utils import load_state, parse_csv, save_state, set_revision_blocker, write_revision_doc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('project')
    parser.add_argument('--affected-stages', required=True)
    parser.add_argument('--affected-files', required=True)
    parser.add_argument('--scope-summary', required=True)
    parser.add_argument('--conflict-summary', required=True)
    parser.add_argument('--plan-summary', required=True)
    args = parser.parse_args()

    project = Path(args.project).expanduser()

    try:
        data = load_state(project)
    except FileNotFoundError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    revision = data['revision']
    if not revision.get('active'):
        print('ERROR: no active revision', file=sys.stderr)
        sys.exit(2)
    if revision.get('currentRevisionGate') != 'awaiting_revision_scope_confirmation':
        print('ERROR: revision is not waiting for scope confirmation', file=sys.stderr)
        sys.exit(2)

    affected_stages = parse_csv(args.affected_stages)
    affected_files = parse_csv(args.affected_files)
    if not affected_stages:
        print('ERROR: affected stages cannot be empty', file=sys.stderr)
        sys.exit(2)
    if not affected_files:
        print('ERROR: affected files cannot be empty', file=sys.stderr)
        sys.exit(2)

    revision['affectedStages'] = affected_stages
    revision['affectedFiles'] = affected_files
    revision['scopeSummary'] = args.scope_summary.strip()
    revision['conflictSummary'] = args.conflict_summary.strip()
    revision['revisionPlanSummary'] = args.plan_summary.strip()
    revision['currentRevisionGate'] = 'awaiting_revision_plan_approval'
    revision['awaitingUserApproval'] = True
    set_revision_blocker(data, revision['currentRevisionGate'])

    save_state(project, data)
    saved = load_state(project)
    write_revision_doc(project, saved)
    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
