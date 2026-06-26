#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'references' / 'fy-2026-27' / 'source-manifest.json'

TOPIC_HINTS = {
    'ais': ['ais', 'tis', '26as'],
    'itr': ['itr', 'return', 'return applicable', 'downloads'],
    'forms': ['form 12bb', 'form 15g', 'form 15h', 'income tax forms'],
    'salary': ['salaried', 'tax slabs', 'regime'],
}


def pick(topic: str, data: dict):
    t = topic.lower()
    out = []
    for src in data.get('sources', []):
        blob = ' '.join([src.get('id', ''), src.get('url', ''), ' '.join(src.get('use_for', []))]).lower()
        if any(k in t for k in TOPIC_HINTS):
            for _, keys in TOPIC_HINTS.items():
                if any(k in blob for k in keys) and any(k in t for k in keys):
                    out.append(src)
                    break
        elif t in blob:
            out.append(src)
    return out or data.get('sources', [])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--topic', required=True)
    args = ap.parse_args()
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    print(json.dumps({
        'fy': data.get('fy'),
        'verified': data.get('verified'),
        'topic': args.topic,
        'candidate_sources': pick(args.topic, data)
    }, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
