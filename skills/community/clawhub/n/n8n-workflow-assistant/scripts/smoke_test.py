"""Test an extracted package with safe synthetic workflows; no live calls."""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    version = json.loads((ROOT / 'assets/skill-version.json').read_text(encoding='utf-8'))
    assert version['skill_name'] == 'n8n-workflow-assistant' and not version['external_skill_dependencies']
    assert 'v' + version['version'] in (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    node = os.environ.get('N8N_SKILL_NODE') or shutil.which('node')
    if not node:
        raise RuntimeError('Node.js >=18 is required for this JavaScript validation smoke test')
    with tempfile.TemporaryDirectory() as tmp:
        for pattern in ['manual', 'webhook']:
            workflow = Path(tmp) / (pattern + '.json')
            subprocess.run([sys.executable, str(ROOT / 'scripts/create_workflow.py'), str(workflow), '--pattern', pattern], check=True, capture_output=True, timeout=30)
            result = subprocess.run([node, str(ROOT / 'scripts/validate_workflow.mjs'), str(workflow)], check=True, capture_output=True, text=True, encoding='utf-8', timeout=30)
            report = json.loads(result.stdout)
            assert not [i for i in report['issues'] if i['severity'] == 'error']
            assert report['live_imported'] is False and report['live_executed'] is False
            result = subprocess.run([sys.executable, str(ROOT / 'scripts/compare_workflows.py'), str(workflow), str(workflow)], check=True, capture_output=True, text=True, encoding='utf-8', timeout=30)
            assert json.loads(result.stdout)['changedNodes'] == []
    print(json.dumps({'skill': version['skill_name'], 'version': version['version'], 'smoke_test': 'passed', 'live_calls': False}))


if __name__ == '__main__':
    main()
