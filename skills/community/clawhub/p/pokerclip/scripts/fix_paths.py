#!/usr/bin/env python3
from pathlib import Path

SCRIPTS = Path(__file__).parent

fixes = {
    'poker_clipper.py': [
        (
            'WORKDIR  = Path(r"C:\\Users\\user\\.openclaw\\workspace-poker")',
            'WORKDIR  = Path(__file__).parent.parent.parent  # dynamic: skills/pokerclip/scripts -> workspace'
        ),
    ],
    'patch_hooks.py': [
        (
            "WORKDIR = Path(r'C:\\Users\\user\\.openclaw\\workspace-poker')",
            "WORKDIR = Path(__file__).parent.parent.parent  # dynamic"
        ),
    ],
    'gen_hooks.py': [
        (
            "OUT = Path(r'C:\\Users\\user\\.openclaw\\workspace-poker\\clips')",
            "OUT = Path(__file__).parent.parent.parent / 'clips'  # dynamic"
        ),
    ],
}

for fname, replacements in fixes.items():
    fp = SCRIPTS / fname
    content = fp.read_text(encoding='utf-8')
    for old, new in replacements:
        if old in content:
            content = content.replace(old, new)
            print(f'Fixed {fname}')
        else:
            print(f'WARNING: not found in {fname}: {old[:60]}')
    fp.write_text(content, encoding='utf-8')

print('Done')
