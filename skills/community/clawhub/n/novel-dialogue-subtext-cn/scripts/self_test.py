#!/usr/bin/env python3
"""Dependency-free release checks for this standalone skill."""
from pathlib import Path
import struct
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
errors = []

def need(condition, message):
    if not condition:
        errors.append(message)

def png_size(path):
    data = path.read_bytes()
    need(data[:8] == b'\x89PNG\r\n\x1a\n', f'{path.name} is not a PNG')
    need(len(data) >= 24 and data[12:16] == b'IHDR', f'{path.name} lacks IHDR')
    return struct.unpack('>II', data[16:24]) if len(data) >= 24 else (0, 0)

required = ['SKILL.md', 'manifest.yaml', 'agents/openai.yaml', 'README.md', 'README.en.md',
            'LICENSE', 'fixtures/success-example.md', 'fixtures/failure-missing-input.md',
            'icon-512.png', 'assets/promo-1600x900.png']
for name in required:
    need((ROOT / name).is_file(), f'missing {name}')

if not errors:
    skill = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
    manifest = (ROOT / 'manifest.yaml').read_text(encoding='utf-8')
    agent = (ROOT / 'agents/openai.yaml').read_text(encoding='utf-8')
    readme = (ROOT / 'README.md').read_text(encoding='utf-8')
    need('name: novel-dialogue-subtext-cn' in skill.split('---', 2)[1], 'SKILL name mismatch')
    need('name: novel-dialogue-subtext-cn' in manifest and 'slug: novel-dialogue-subtext-cn' in manifest, 'manifest identity mismatch')
    need('icon: icon-512.png' in manifest, 'manifest icon missing')
    need('allow_implicit_invocation: true' in agent and 'policy:' in agent, 'agent policy invalid')
    for field in ('display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large'):
        found = re.search(r'^  ' + field + r': "([^"\n]+)"$', agent, re.M)
        need(bool(found), f'agent field must be quoted: {field}')
        if not found:
            continue
        value = found.group(1)
        if field == 'short_description':
            need(25 <= len(value) <= 64, 'actual short description length invalid')
        elif field == 'default_prompt':
            need('$novel-dialogue-subtext-cn' in value, 'default_prompt must reference this Skill')
        elif field.startswith('icon_'):
            target = (ROOT / value).resolve()
            need(target.is_relative_to(ROOT.resolve()) and target.is_file(), 'agent icon must exist inside Skill directory')
    need('assets/promo-1600x900.png' in readme, 'README does not show promo')
    need(png_size(ROOT / 'icon-512.png') == (512, 512), 'icon must be 512x512')
    need(png_size(ROOT / 'assets/promo-1600x900.png') == (1600, 900), 'promo must be 1600x900')

if errors:
    print('SELF-TEST FAILED')
    print('\n'.join(f'- {item}' for item in errors))
    sys.exit(1)
print('SELF-TEST PASSED: structure, fixtures, metadata, and image dimensions are valid.')
