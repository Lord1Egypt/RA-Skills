#!/usr/bin/env python3
import json, re, sys, os
from pathlib import Path

def extract(path):
    data = json.load(open(path))
    entries = data.get('log', {}).get('entries', [])
    ops = []
    for e in entries:
        req = e.get('request', {})
        url = req.get('url', '')
        if 'hemlane.com' not in url or '/graphql' not in url:
            continue
        text = ((req.get('postData') or {}).get('text') or '').strip()
        if not text:
            continue
        try:
            payload = json.loads(text)
        except Exception:
            payload = {'raw': text}
        op = None
        query = payload.get('query','') if isinstance(payload, dict) else ''
        if isinstance(payload, dict):
            op = payload.get('operationName')
        if not op and query:
            m = re.search(r'(query|mutation)\s+(\w+)', query)
            if m:
                op = m.group(2)
        ops.append({
            'file': os.path.basename(path),
            'method': req.get('method'),
            'url': url,
            'operationName': op,
            'variables': payload.get('variables') if isinstance(payload, dict) else None,
            'query': query if query else None,
        })
    return ops

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: extract_hemlane_graphql.py file1.har [file2.har ...]')
        sys.exit(1)
    out = []
    for arg in sys.argv[1:]:
        out.extend(extract(arg))
    print(json.dumps(out, indent=2))
