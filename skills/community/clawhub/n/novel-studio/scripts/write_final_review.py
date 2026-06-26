#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from revision_utils import load_state, save_state

FINAL_REVIEW_DOC = '07_终审报告.md'
FINAL_REVIEW_BLOCKER_PREFIX = 'Final review blocker:'
VALID_DECISIONS = {'pass', 'conditional pass', 'rework required'}


def parse_bool(value: str) -> bool:
    lowered = value.strip().lower()
    if lowered == 'true':
        return True
    if lowered == 'false':
        return False
    raise argparse.ArgumentTypeError('delivery-ready must be true or false')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Write final review report for a novel project.')
    parser.add_argument('project')
    parser.add_argument('--decision', required=True, choices=sorted(VALID_DECISIONS))
    parser.add_argument('--delivery-ready', required=True, type=parse_bool)
    parser.add_argument('--strengths', action='append', default=[])
    parser.add_argument('--issues', action='append', default=[])
    parser.add_argument('--blockers', action='append', default=[])
    parser.add_argument('--actions', action='append', default=[])
    parser.add_argument('--summary', required=True)
    return parser.parse_args()


def render_list(items: list[str]) -> str:
    if not items:
        return '- 无\n'
    return ''.join(f'- {item}\n' for item in items)


def render_report(args: argparse.Namespace, blockers: list[str]) -> str:
    return (
        '# 07_终审报告\n\n'
        '## 最终结论\n'
        f'- {args.decision}\n'
        f'- 摘要：{args.summary}\n\n'
        '## 是否可交付\n'
        f'- {"true" if args.delivery_ready else "false"}\n\n'
        '## 主要优点\n'
        f'{render_list(args.strengths)}\n'
        '## 主要问题\n'
        f'{render_list(args.issues)}\n'
        '## 阻塞问题\n'
        f'{render_list(blockers)}\n'
        '## 建议动作\n'
        f'{render_list(args.actions)}'
    )


def clear_final_review_blockers(data: dict) -> None:
    blockers = data.setdefault('blockingIssues', [])
    data['blockingIssues'] = [b for b in blockers if not b.startswith(FINAL_REVIEW_BLOCKER_PREFIX)]


def add_final_review_blockers(data: dict, blockers: list[str]) -> None:
    clear_final_review_blockers(data)
    for blocker in blockers:
        data['blockingIssues'].append(f'{FINAL_REVIEW_BLOCKER_PREFIX} {blocker}')


def main() -> None:
    args = parse_args()
    project = Path(args.project).expanduser()

    try:
        data = load_state(project)
    except FileNotFoundError as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    open_critical_issues = list(
        data.get('narrativeIntelligence', {}).get('consistency', {}).get('openCriticalIssues', [])
    )
    merged_blockers = list(dict.fromkeys([*args.blockers, *open_critical_issues]))

    if args.decision == 'pass' and merged_blockers:
        print('ERROR: pass cannot be combined with blockers', file=sys.stderr)
        sys.exit(2)
    if args.delivery_ready and merged_blockers:
        print('ERROR: delivery-ready=true cannot be used with blockers', file=sys.stderr)
        sys.exit(2)
    if args.decision == 'rework required' and args.delivery_ready:
        print(
            'ERROR: rework required cannot be combined with delivery-ready=true',
            file=sys.stderr,
        )
        sys.exit(2)
    if not args.summary.strip():
        print('ERROR: summary is required', file=sys.stderr)
        sys.exit(2)

    report = render_report(args, merged_blockers)
    (project / FINAL_REVIEW_DOC).write_text(report, encoding='utf-8')

    review = data['review']
    review['finalDecision'] = args.decision
    review['finalDeliveryReady'] = args.delivery_ready
    review['finalBlockingIssues'] = merged_blockers
    review['finalReviewSummary'] = args.summary.strip()
    add_final_review_blockers(data, review['finalBlockingIssues'])

    save_state(project, data)
    saved = load_state(project)
    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
