#!/usr/bin/env python3
import argparse
import os
from pathlib import Path

REQUIRED_FILES = ['README.md', 'STATE.md', 'TODO.md']


def main():
    ap = argparse.ArgumentParser(description='Check if a project is ready for heartbeat-style continuation')
    ap.add_argument('project_dir')
    args = ap.parse_args()

    project_dir = Path(os.path.expanduser(args.project_dir)).resolve()
    print(f'Project: {project_dir}')

    missing = [f for f in REQUIRED_FILES if not (project_dir / f).exists()]
    if missing:
        print('Verdict: not-ready')
        print('Reasons:')
        print('- Missing canonical project files: ' + ', '.join(missing))
        print('Recommendation: create the missing files before using a heartbeat loop.')
        return

    state = (project_dir / 'STATE.md').read_text(encoding='utf-8')
    todo = (project_dir / 'TODO.md').read_text(encoding='utf-8')
    has_focus = 'Current focus' in state or 'Current Focus' in state
    has_next = 'Next steps' in state or '## Active' in todo

    if has_focus and has_next:
        print('Verdict: ready')
        print('Reasons:')
        print('- canonical project files exist')
        print('- state/todo contain active execution context')
        print('Recommendation: safe to design a heartbeat loop for this project.')
    else:
        print('Verdict: review-before-use')
        print('Reasons:')
        if not has_focus:
            print('- STATE.md lacks a clear current focus section')
        if not has_next:
            print('- no clear next-step section found in STATE.md or TODO.md')
        print('Recommendation: clarify the current focus and next steps before using heartbeat automation.')


if __name__ == '__main__':
    main()
