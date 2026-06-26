#!/usr/bin/env python3
import json
import sys
import urllib.request
from pathlib import Path

ENDPOINT = "https://api.kie.ai/api/v1/jobs/createTask"


def load_config():
    obj = json.loads(Path('/root/.openclaw/credentials/kie.json').read_text())
    return {
        'api_key': obj['api_key'],
        'model': obj.get('model', 'nano-banana-2'),
        'aspect_ratio': obj.get('default_aspect_ratio', '16:9'),
        'resolution': obj.get('default_resolution', '1K'),
        'output_format': str(obj.get('default_output_format', 'PNG')).lower(),
    }


def main():
    if len(sys.argv) < 2:
        print('Usage: kie-create-task.py <prompt> [callback_url] [image_url ...]', file=sys.stderr)
        sys.exit(2)
    prompt = sys.argv[1]
    callback = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] != '-' else None
    image_urls = sys.argv[3:] if len(sys.argv) > 3 else []
    cfg = load_config()
    body = {
        'model': cfg['model'],
        'input': {
            'prompt': prompt,
            'aspect_ratio': cfg['aspect_ratio'],
            'google_search': False,
            'resolution': cfg['resolution'],
            'output_format': cfg['output_format'],
        }
    }
    if image_urls:
        body['input']['image_input'] = image_urls
    if callback:
        body['callBackUrl'] = callback
    data = json.dumps(body).encode()
    req = urllib.request.Request(
        ENDPOINT,
        data=data,
        headers={
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {cfg['api_key']}"
        },
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        print(r.read().decode())


if __name__ == '__main__':
    main()
