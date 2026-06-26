#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from approve_stage_gate import approve_gate, gate_approval_error
from autopilot_utils import AUTO_APPROVABLE_GATES, build_autopilot_report, resolve_next_autopilot_action
from revision_utils import load_state, save_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Advance autopilot by one safe step.')
    parser.add_argument('project')
    return parser.parse_args()


def eligible_autopilot_gate(state: dict) -> str | None:
    review = state.get('review') if isinstance(state.get('review'), dict) else {}
    gate = review.get('currentGate')
    if gate not in AUTO_APPROVABLE_GATES:
        return None
    if gate_approval_error(state, gate) is not None:
        return None
    return gate


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser()
    if not project.exists():
        print(f'ERROR: project not found: {project}', file=sys.stderr)
        return 2

    state = load_state(project)
    payload = resolve_next_autopilot_action(
        state,
        project_path=project,
        eligible_gate=eligible_autopilot_gate(state),
    )

    if payload['action'] == 'approve_gate':
        saved_state = approve_gate(project, payload['gate'])
    else:
        save_state(project, state)
        saved_state = load_state(project)

    payload['savedState'] = saved_state
    payload['report'] = build_autopilot_report(saved_state, payload)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
