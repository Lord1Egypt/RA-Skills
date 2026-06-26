#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
WORKSPACE = SKILL_DIR.parent.parent
DEFAULT_OUTPUT = WORKSPACE / 'backups'


def resolve_package_script() -> Path:
    candidates = [
        WORKSPACE / 'skills' / 'skill-creator' / 'scripts' / 'package_skill.py',
        Path.home() / '.openclaw' / 'workspace' / 'skills' / 'skill-creator' / 'scripts' / 'package_skill.py',
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    pnpm_roots = [
        Path.home() / '.local' / 'share' / 'pnpm' / 'global',
    ]
    if Path.home() == Path('/root'):
        pnpm_roots.append(Path('/root/.local/share/pnpm/global'))
    for root in pnpm_roots:
        if not root.exists():
            continue
        matches = sorted(root.glob('**/node_modules/openclaw/skills/skill-creator/scripts/package_skill.py'))
        if matches:
            return matches[0]

    raise FileNotFoundError('package_skill.py not found; install skill-creator locally or set workspace skill path')

EXCLUDE_PREFIXES = [
    'skill-data/state',
    'skill-data/profiles',
    'skill-data/runtime',
    'dist',
]
EXACT_EXCLUDES = set()
FORBIDDEN_NAMES = {
    'auth-profile.json',
    'callback.txt',
    'result.json',
}


def reset_dir(path: Path) -> None:
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def should_skip(rel: Path) -> bool:
    rel_str = rel.as_posix()
    if any(part == '__pycache__' for part in rel.parts):
        return True
    if rel.name in FORBIDDEN_NAMES:
        return True
    if rel_str in EXACT_EXCLUDES:
        return True
    return any(rel_str == prefix or rel_str.startswith(prefix + '/') for prefix in EXCLUDE_PREFIXES)


def copy_filtered(src: Path, dst: Path) -> None:
    for item in src.rglob('*'):
        rel = item.relative_to(src)
        if should_skip(rel):
            continue
        target = dst / rel
        if item.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif item.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, target)


def main() -> int:
    output_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else DEFAULT_OUTPUT
    output_dir.mkdir(parents=True, exist_ok=True)

    staging_root = WORKSPACE / 'tmp' / 'skill-package-staging-public'
    staging_dir = staging_root / SKILL_DIR.name
    reset_dir(staging_root)
    staging_dir.mkdir(parents=True, exist_ok=True)

    copy_filtered(SKILL_DIR, staging_dir)

    package_script = resolve_package_script()
    cmd = ['python3', str(package_script), str(staging_dir), str(output_dir)]
    proc = subprocess.run(cmd)
    return proc.returncode


if __name__ == '__main__':
    raise SystemExit(main())
