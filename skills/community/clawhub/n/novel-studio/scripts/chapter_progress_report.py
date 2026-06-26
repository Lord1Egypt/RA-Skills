#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from chapter_progress_utils import build_progress_report, mark_progress_items_reported
from revision_utils import load_state, save_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Read or ack persisted chapter progress events.')
    parser.add_argument('project')
    parser.add_argument('--ack', action='append', default=[])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser()
    if not project.exists():
        print(f'ERROR: project not found: {project}', file=sys.stderr)
        return 2

    state = load_state(project)
    batch = state['batch']
    if args.ack:
        marked = mark_progress_items_reported(batch, args.ack)
        save_state(project, state)
        print(json.dumps({'ackedEventIds': marked}, ensure_ascii=False, indent=2))
        return 0

    print(json.dumps(build_progress_report(batch.get('pendingProgressItems', [])), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
