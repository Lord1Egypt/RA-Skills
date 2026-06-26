#!/usr/bin/env python3
import json
import subprocess
from pathlib import Path

INSPECT = Path('/root/.openclaw/workspace/skills/cli-anything/scripts/inspect_cli_anything.py')


def score(item):
    s = 0
    if item.get('has_setup_py'):
        s += 3
    if item.get('has_pkg_dir'):
        s += 3
    if item.get('has_readme'):
        s += 2
    if item.get('has_e2e_tests'):
        s += 2
    name = item.get('name', '')
    if name in {'gimp', 'inkscape', 'libreoffice'}:
        s += 2
    if name in {'zoom', 'obs-studio', 'anygen'}:
        s -= 1
    return s


def main():
    raw = subprocess.check_output(['python3', str(INSPECT)], text=True)
    data = json.loads(raw)
    harnesses = data.get('harnesses', [])
    ranked = []
    for item in harnesses:
        item = dict(item)
        item['score'] = score(item)
        ranked.append(item)
    ranked.sort(key=lambda x: (-x['score'], x['name']))
    out = {
        'repo_exists': data.get('repo_exists', False),
        'recommended': ranked[:5],
        'best': ranked[0] if ranked else None,
    }
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
