#!/usr/bin/env python3
import os
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'graymatter.skill'
REQUIRED = [
    'SKILL.md',
    'graymatter-bootstrap',
    '.mcp.json',
    'scripts/gm-query',
    'scripts/gm-graph',
    'scripts/gm-write',
    'scripts/gm-login',
    'scripts/gm-activate',
    'scripts/gm-install-check',
    'scripts/gm-smoke',
    'scripts/gm-openapi-sync',
    'scripts/gm-openapi-summary',
    'scripts/gm-entity',
    'scripts/gm-register-agent',
    'scripts/gm-light-bootstrap',
    'scripts/gm-light-up',
    'scripts/gm-light-env',
    'scripts/package-local-server',
    'scripts/graymatter_api.sh',
    'mcp-server/index.js',
    'mcp-server/package.json',
    'mcp-server/README.md',
    'examples/graymatter-light-thorapi-bundle.yaml',
    'references/public-release-checklist.md',
    'references/multi-agent-conventions.md',
]

OPTIONAL_REPO_ONLY = [
    'scripts/gm-light-json-smoke',
    'examples/memoryentry-basic.json',
    'examples/memoryentry-decision.json',
    'examples/memoryentry-todo.json',
    'examples/memoryentry-artifact.json',
    'examples/graymatter-light-memoryentry.yaml',
]

missing = [rel for rel in REQUIRED if not (ROOT / rel).is_file()]
if missing:
    print('Missing required files:', file=sys.stderr)
    for rel in missing:
        print(f'  - {rel}', file=sys.stderr)
    sys.exit(1)

for rel in REQUIRED:
    path = ROOT / rel
    if path.is_symlink():
        print(f'Symlink not allowed in package: {rel}', file=sys.stderr)
        sys.exit(1)

skill_md = (ROOT / 'SKILL.md').read_text(encoding='utf-8', errors='strict')
if 'name: graymatter' not in skill_md or 'description:' not in skill_md:
    print('SKILL.md is missing expected frontmatter fields', file=sys.stderr)
    sys.exit(1)

def add_file(zf: zipfile.ZipFile, rel: str) -> None:
    src = ROOT / rel
    arcname = str(Path('graymatter') / rel)
    info = zipfile.ZipInfo.from_file(src, arcname=arcname)
    info.date_time = (1980, 1, 1, 0, 0, 0)
    info.compress_type = zipfile.ZIP_DEFLATED

    # Ensure shell entrypoints remain executable after install/unzip.
    if rel.startswith('scripts/') or rel == 'graymatter-bootstrap':
        info.external_attr = (0o100755 << 16)

    with src.open('rb') as fh:
        zf.writestr(info, fh.read())


with zipfile.ZipFile(OUT, 'w') as zf:
    for rel in REQUIRED:
        add_file(zf, rel)

with zipfile.ZipFile(OUT) as zf:
    packaged = sorted(zf.namelist())

expected = sorted(str(Path('graymatter') / rel) for rel in REQUIRED)
if packaged != expected:
    print('Packaged archive contents did not match expected manifest', file=sys.stderr)
    print('Expected:', *expected, sep='\n  ', file=sys.stderr)
    print('Actual:', *packaged, sep='\n  ', file=sys.stderr)
    sys.exit(1)

print(f'Packaged {OUT}')
print('Archive contents verified:')
for name in packaged:
    print(f'  - {name}')

missing_optional = [rel for rel in OPTIONAL_REPO_ONLY if not (ROOT / rel).exists()]
if missing_optional:
    print('Optional repo assets missing:', file=sys.stderr)
    for rel in missing_optional:
        print(f'  - {rel}', file=sys.stderr)
else:
    print('Optional repo assets present:')
    for rel in OPTIONAL_REPO_ONLY:
        print(f'  - {rel}')
