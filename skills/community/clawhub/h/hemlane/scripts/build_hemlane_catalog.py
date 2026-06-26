#!/usr/bin/env python3
import json, csv, os, re, sys
from pathlib import Path

def extract_ops(paths):
    ops = {}
    for path in paths:
        name = os.path.basename(path)
        data = json.load(open(path))
        for e in data.get('log', {}).get('entries', []):
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
                continue
            op = payload.get('operationName')
            q = payload.get('query') or ''
            if not op:
                m = re.search(r'(query|mutation)\s+(\w+)', q)
                if m:
                    op = m.group(2)
            if not op:
                continue
            row = ops.setdefault(op, {
                'operationName': op,
                'kind': 'mutation' if q.lstrip().startswith('mutation') else 'query',
                'files': [],
                'count': 0,
                'sampleVariables': payload.get('variables'),
                'queryExcerpt': q[:2000],
            })
            row['count'] += 1
            if name not in row['files']:
                row['files'].append(name)
    return sorted(ops.values(), key=lambda x: x['operationName'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: build_hemlane_catalog.py file1.har [file2.har ...]')
        sys.exit(1)
    rows = extract_ops(sys.argv[1:])
    print(json.dumps(rows, indent=2))
