#!/usr/bin/env python3
import argparse
import json
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
RECOMMENDER = SCRIPT_DIR / 'recommend_checks.py'


def run(cmd):
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or result.stdout.strip() or f'command failed: {cmd}')
    return result.stdout


def get_plan(repo: str, base: str | None, head: str) -> dict:
    cmd = ['python3', str(RECOMMENDER), '--repo', repo, '--head', head, '--json']
    if base:
        cmd.extend(['--base', base])
    return json.loads(run(cmd))


def bullets(lines):
    return '\n'.join(f'- {line}' for line in lines) if lines else '- none'


def main():
    parser = argparse.ArgumentParser(description='Generate an OpenClaw-flavored PR body from a repo diff.')
    parser.add_argument('--repo', required=True, help='Path to the OpenClaw git repo')
    parser.add_argument('--base', help='Base ref for git diff')
    parser.add_argument('--head', default='HEAD', help='Head ref for git diff')
    parser.add_argument('--title', required=True, help='Planned PR title')
    parser.add_argument('--summary', action='append', default=[], help='Summary bullet (repeatable)')
    parser.add_argument('--why', action='append', default=[], help='Why bullet (repeatable)')
    parser.add_argument('--issue', help='Issue/Discussion/PR reference to mention')
    parser.add_argument('--testing-level', default='lightly tested', choices=['untested', 'lightly tested', 'fully tested'])
    parser.add_argument('--ai-assisted', default='yes', choices=['yes', 'no'])
    parser.add_argument('--output', help='Write markdown to a file instead of stdout')
    args = parser.parse_args()

    plan = get_plan(args.repo, args.base, args.head)

    lines = []
    lines.append(f'# {args.title}')
    lines.append('')
    if args.issue:
        lines.append(f'Related: {args.issue}')
        lines.append('')
    lines.append('## Summary')
    lines.append(bullets(args.summary or ['TODO: summarize the change in 1-2 bullets.']))
    lines.append('')
    lines.append('## Why')
    lines.append(bullets(args.why or ['TODO: explain what was broken or brittle and why this fix is the right scope.']))
    lines.append('')
    lines.append('## Files touched')
    lines.append(bullets(plan.get('changedFiles', [])))
    lines.append('')
    lines.append('## Validation')
    lines.append(bullets(plan.get('recommendedCommands', [])))
    lines.append('')
    lines.append('## Maintainer routing hints')
    lines.append(bullets(plan.get('maintainersToConsider', [])))
    lines.append('')
    lines.append('## Screenshots')
    lines.append('- Add before/after screenshots for UI or visual changes if applicable.')
    lines.append('')
    lines.append('## AI assistance')
    lines.append(f'- AI-assisted: {args.ai_assisted}')
    lines.append(f'- Testing level: {args.testing_level}')
    lines.append('- I reviewed the code and understand what it does.')
    lines.append('')
    lines.append('## Notes')
    lines.append(bullets(plan.get('warnings', [])))
    body = '\n'.join(lines) + '\n'

    if args.output:
        Path(args.output).write_text(body)
    else:
        print(body)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(f'error: {exc}', file=sys.stderr)
        sys.exit(1)
