from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser(description='Extract Cookie / csrf / Authorization headers from matching HAR requests.')
    ap.add_argument('har_file')
    ap.add_argument('--contains', required=True, help='URL substring to match the target request')
    ap.add_argument('--out-dir', required=True)
    args = ap.parse_args()

    data = json.loads(Path(args.har_file).read_text(encoding='utf-8'))
    entries = data.get('log', {}).get('entries', [])
    target = None
    for entry in entries:
        req = entry.get('request', {})
        if args.contains.lower() in req.get('url', '').lower():
            target = req
            break
    if target is None:
        raise SystemExit(f'No request URL contained: {args.contains}')

    headers = {h.get('name', ''): h.get('value', '') for h in target.get('headers', [])}
    lowered = {k.lower(): v for k, v in headers.items()}
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    written = {}
    if 'cookie' in lowered:
        p = out_dir / 'cookie-header.txt'
        p.write_text(lowered['cookie'].strip(), encoding='utf-8')
        written['cookie'] = str(p)
    if 'x-csrf-token' in lowered:
        p = out_dir / 'csrf-token.txt'
        p.write_text(lowered['x-csrf-token'].strip(), encoding='utf-8')
        written['csrf'] = str(p)
    if 'authorization' in lowered:
        p = out_dir / 'authorization.txt'
        p.write_text(lowered['authorization'].strip(), encoding='utf-8')
        written['authorization'] = str(p)
    print(json.dumps({'matched_url': target.get('url', ''), 'written': written}, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
