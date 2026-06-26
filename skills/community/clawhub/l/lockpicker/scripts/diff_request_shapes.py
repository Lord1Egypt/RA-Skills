from __future__ import annotations

import argparse
import json
from pathlib import Path


def flatten_json(prefix: str, obj, out: set[str]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f'{prefix}.{k}' if prefix else k
            out.add(key)
            flatten_json(key, v, out)
    elif isinstance(obj, list):
        out.add(prefix + '[]')
        for v in obj[:5]:
            flatten_json(prefix + '[]', v, out)


def load_req(path: str) -> dict:
    data = json.loads(Path(path).read_text(encoding='utf-8'))
    if 'request' in data:
        return data['request']
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description='Compare two captured request JSON shapes.')
    ap.add_argument('request_a')
    ap.add_argument('request_b')
    args = ap.parse_args()

    a = load_req(args.request_a)
    b = load_req(args.request_b)
    sa, sb = set(), set()
    flatten_json('', a, sa)
    flatten_json('', b, sb)
    out = {
        'only_in_a': sorted(sa - sb),
        'only_in_b': sorted(sb - sa),
        'in_both': sorted(sa & sb),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
