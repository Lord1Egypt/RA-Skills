"""Create an inactive synthetic n8n scaffold without contacting an instance."""
import argparse
import json
import re
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path)
    parser.add_argument('--pattern', choices=['manual', 'webhook'], default='manual')
    parser.add_argument('--name')
    parser.add_argument('--webhook-path', help='Optional relative path; defaults to a unique example path')
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Output already exists; choose a new path instead of overwriting')
    path = args.webhook_path or 'example-' + uuid.uuid4().hex[:12]
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_/-]{0,150}', path) or '..' in path or '//' in path:
        parser.error('Invalid relative webhook path')
    workflow = json.loads((ROOT / 'assets' / ('template-' + args.pattern + '.json')).read_text(encoding='utf-8'))
    workflow['name'] = args.name or workflow['name']
    for node in workflow['nodes']:
        node['id'] = str(uuid.uuid4())
        if node['type'] == 'n8n-nodes-base.webhook':
            node['parameters']['path'] = path
            node['webhookId'] = str(uuid.uuid4())
    workflow['active'] = False
    workflow['pinData'] = {}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(workflow, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': 'offline_candidate', 'pattern': args.pattern,
                      'nodes': len(workflow['nodes']), 'live_imported': False, 'live_executed': False}))


if __name__ == '__main__':
    main()
