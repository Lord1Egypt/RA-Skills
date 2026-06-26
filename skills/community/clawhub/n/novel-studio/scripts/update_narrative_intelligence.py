#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from narrative_checker import refresh_cliche_findings, refresh_consistency_findings
from narrative_intelligence_utils import sync_narrative_intelligence
from revision_utils import load_state, save_state
from stage_execution_utils import ensure_project


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Refresh additive narrative intelligence metadata.')
    parser.add_argument('project')
    parser.add_argument('--stage', required=True, choices=['drafting', 'polishing', 'proofreading'])
    parser.add_argument('--chapter-label', dest='chapter_labels', action='append', default=[])
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    try:
        project = ensure_project(Path(args.project))
        state = load_state(project)
        sync_narrative_intelligence(
            project,
            state,
            stage=args.stage,
            chapter_labels=args.chapter_labels,
        )
        if args.stage == 'proofreading':
            refresh_consistency_findings(project, state)
            refresh_cliche_findings(project, state)
        save_state(project, state)
        saved = load_state(project)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        sys.exit(2)

    print(json.dumps(saved, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
