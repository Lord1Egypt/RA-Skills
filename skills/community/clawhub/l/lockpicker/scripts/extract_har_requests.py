from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description='Extract and summarize HAR requests, optionally filtering by substring.')
    ap.add_argument('har_file')
    ap.add_argument('--contains', action='append', default=[], help='Keep only requests whose URL contains this text. Repeatable.')
    ap.add_argument('--method', action='append', default=[], help='Keep only requests with this HTTP method. Repeatable.')
    ap.add_argument('--out', default='')
    args = ap.parse_args()

    data = json.loads(Path(args.har_file).read_text(encoding='utf-8'))
    entries = data.get('log', {}).get('entries', [])
    out = []
    methods = {m.upper() for m in args.method}
    needles = args.contains
    for i, entry in enumerate(entries, start=1):
        req = entry.get('request', {})
        url = req.get('url', '')
        method = req.get('method', '').upper()
        if methods and method not in methods:
            continue
        if needles and not all(n.lower() in url.lower() for n in needles):
            continue
        headers = {h.get('name', ''): h.get('value', '') for h in req.get('headers', [])}
        out.append({
            'index': i,
            'method': method,
            'url': url,
            'status': entry.get('response', {}).get('status'),
            'content_type': headers.get('content-type', headers.get('Content-Type', '')),
            'has_cookie': 'cookie' in {k.lower() for k in headers.keys()},
            'has_authorization': 'authorization' in {k.lower() for k in headers.keys()},
            'post_data_text': (req.get('postData', {}) or {}).get('text', ''),
        })
    text = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).write_text(text + '\n', encoding='utf-8')
    print(text)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
