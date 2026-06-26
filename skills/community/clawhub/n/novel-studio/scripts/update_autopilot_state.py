#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from autopilot_utils import (
    is_acknowledgement_message,
    is_explicit_autopilot_request,
    is_non_substantive_user_message,
    resolve_explicit_autopilot_goal,
    start_autopilot_with_goal,
    stop_autopilot,
)
from revision_utils import load_state, save_state


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Apply a user message to the saved autopilot state.')
    parser.add_argument('project')
    parser.add_argument('--message', required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser()
    state = load_state(project)
    message = args.message.strip()
    auto_pilot = state['autoPilot']
    active = bool(auto_pilot.get('active'))
    previous_stop_reason = None
    resolved_goal = resolve_explicit_autopilot_goal(message, active=active)

    if resolved_goal is not None and is_explicit_autopilot_request(message, active=active):
        action = 'superseded' if active else 'activated'
        if active:
            previous_stop_reason = stop_autopilot(state, 'superseded_by_new_user_goal')['stopReason']
        start_autopilot_with_goal(state, message, goal_chapter=resolved_goal)
        save_state(project, state)
        print(
            json.dumps(
                {
                    'action': action,
                    'previousStopReason': previous_stop_reason,
                    'savedState': load_state(project),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    if auto_pilot.get('active') and not (
        is_acknowledgement_message(message) or is_non_substantive_user_message(message)
    ):
        stop_autopilot(state, 'user_interruption')
        save_state(project, state)
        print(
            json.dumps(
                {
                    'action': 'stopped',
                    'savedState': load_state(project),
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    save_state(project, state)
    print(
        json.dumps(
            {
                'action': 'noop',
                'savedState': load_state(project),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
