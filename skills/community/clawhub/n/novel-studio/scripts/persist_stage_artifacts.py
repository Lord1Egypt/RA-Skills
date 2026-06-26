#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from revision_utils import load_state, save_state
from stage_persistence_utils import gate_for_stage, now_iso, validate_artifact_updates


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Persist parent-owned stage artifacts into canonical project files.')
    parser.add_argument('project')
    parser.add_argument('stage')
    parser.add_argument('--substage')
    parser.add_argument('--artifact-file', required=True)
    return parser.parse_args()


def read_payload(path: Path) -> dict:
    return json.loads(path.read_text(encoding='utf-8'))


def main() -> int:
    args = parse_args()
    project = Path(args.project).expanduser()
    artifact_file = Path(args.artifact_file).expanduser()

    if not project.exists():
        print(f'ERROR: project not found: {project}', file=sys.stderr)
        return 2
    if not artifact_file.exists():
        print(f'ERROR: artifact file not found: {artifact_file}', file=sys.stderr)
        return 2

    try:
        payload = read_payload(artifact_file)
        if payload.get('status') != 'completed':
            raise ValueError('artifact payload status must be completed')

        data = load_state(project)
        workflow = data.setdefault('workflow', {})
        review = data.setdefault('review', {})
        substage = args.substage or workflow.get('currentSubstage')
        validated = validate_artifact_updates(args.stage, payload.get('artifactUpdates', {}), substage)

        for relpath, text in validated.items():
            path = project / relpath
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')

        review['currentGate'] = gate_for_stage(args.stage, substage)
        review['pendingArtifactPaths'] = sorted(validated)
        review['lastPersistedStage'] = args.stage
        review['lastPersistedAt'] = now_iso()
        workflow['status'] = 'awaiting_user_approval'

        save_state(project, data)
    except Exception as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        return 2

    print(json.dumps(load_state(project), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
