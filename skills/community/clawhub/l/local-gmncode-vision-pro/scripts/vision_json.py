#!/usr/bin/env python3
import os, sys, json, base64, requests

if len(sys.argv) < 2:
    print('Usage: vision_json.py <image_path> [prompt]', file=sys.stderr)
    sys.exit(2)

image_path = sys.argv[1]
prompt = sys.argv[2] if len(sys.argv) > 2 else (
    'Analyze this image and return strict JSON with keys: '
    'summary, detected_entities, style, confidence, uncertainty_notes.'
)
api_key = os.environ.get('GMNCODE_API_KEY')
if not api_key:
    print('GMNCODE_API_KEY not set', file=sys.stderr)
    sys.exit(3)

with open(image_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode()

payload = {
    'model': 'gpt-5.4',
    'input': [{
        'role': 'user',
        'content': [
            {'type': 'input_text', 'text': prompt},
            {'type': 'input_image', 'image_url': f'data:image/jpeg;base64,{b64}'}
        ]
    }],
    'text': {
        'format': {
            'type': 'json_schema',
            'name': 'vision_result',
            'schema': {
                'type': 'object',
                'properties': {
                    'summary': {'type': 'string'},
                    'detected_entities': {'type': 'array', 'items': {'type': 'string'}},
                    'style': {'type': 'string'},
                    'confidence': {'type': 'number'},
                    'uncertainty_notes': {'type': 'array', 'items': {'type': 'string'}}
                },
                'required': ['summary', 'detected_entities', 'style', 'confidence', 'uncertainty_notes'],
                'additionalProperties': False
            }
        }
    }
}
headers = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}
r = requests.post('https://gmncode.cn/v1/responses', headers=headers, json=payload, timeout=180)
r.raise_for_status()
data = r.json()
for item in data.get('output', []):
    for c in item.get('content', []):
        if c.get('type') == 'output_text':
            print(c.get('text', '').strip())
            raise SystemExit(0)
print('{}')
