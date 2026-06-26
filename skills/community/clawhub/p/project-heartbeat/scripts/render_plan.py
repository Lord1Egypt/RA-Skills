#!/usr/bin/env python3
import argparse
import os
from pathlib import Path


def cadence_label(minutes: int) -> str:
    if minutes <= 10:
        return 'high-intensity build'
    if minutes <= 30:
        return 'active continuation'
    if minutes <= 120:
        return 'steady maintenance'
    return 'low-frequency research'


def main():
    ap = argparse.ArgumentParser(description='Render a controlled project-heartbeat plan')
    ap.add_argument('project_dir')
    ap.add_argument('--every-min', type=int, default=30)
    args = ap.parse_args()

    project_dir = Path(os.path.expanduser(args.project_dir)).resolve()
    backlog = project_dir / 'PENDING-DECISIONS.md'
    progress = project_dir / 'HEARTBEAT-LOG.md'

    print(f'Project: {project_dir}')
    print(f'Cadence: every {args.every_min} minutes ({cadence_label(args.every_min)})')
    print('\nContinue conditions:')
    print('- a clear next concrete step exists in project artifacts')
    print('- work can continue locally without requiring an external action right now')
    print('- the last few cycles still produced meaningful progress')

    print('\nHard stop boundaries:')
    print('- budget or quota exhausted')
    print('- safety / human-only boundary reached with no meaningful bypass path')
    print('- no clear next step for repeated cycles')
    print('- repeated no-progress cycles')

    print('\nSoft block boundaries:')
    print('- external approval pending')
    print('- repository creation or publishing is blocked but internal work can continue')
    print('- one path is blocked while another concrete path remains')

    print('\nArtifacts to maintain:')
    print(f'- pending decision backlog: {backlog.name}')
    print(f'- heartbeat progress log: {progress.name}')
    print('- canonical project truth: STATE.md / TODO.md / DECISIONS.md')

    print('\nContinuation integrity:')
    print('- no artifact, no progress')
    print('- a cycle should update at least one durable artifact')
    print('- repeated no-op cycles should escalate toward stopping the loop')

    print('\nResume protocol:')
    print('1. Read STATE.md')
    print('2. Read TODO.md')
    print(f'3. Read {backlog.name}')
    print(f'4. Read {progress.name}')
    print('5. Continue from the smallest clear next step')


if __name__ == '__main__':
    main()
