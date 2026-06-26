"""Tech stack detection for codebases."""

import json
from pathlib import Path
from typing import List, Set

# Directories that should always be excluded from analysis
EXCLUDE_DIRS: Set[str] = {
    '.venv', 'venv', '.env', '__pycache__', '.pytest_cache', '.coverage',
    '.git', '.hg', '.svn', 'node_modules', 'dist', 'build', 'target',
    'vendor', '.deps', 'tests', 'test', 'spec', 'specs', 'docs', 'doc',
    'example', 'examples', 'scripts'
}


def _should_exclude(path: Path) -> bool:
    """Check if a path or any of its parents should be excluded."""
    parts = set(path.parts)
    return any(excluded in parts for excluded in EXCLUDE_DIRS)


def detect_stack(root: str) -> str:
    """Detect the primary tech stack of a repository."""
    root_path = Path(root)

    # Python (Django, FastAPI, plain) - Prioritize Python to avoid misidentification in hybrid projects
    python_indicators = ['requirements.txt', 'pyproject.toml', 'setup.py', 'Pipfile', 'poetry.lock']
    if any((root_path / f).exists() for f in python_indicators):
        return 'python'

    # Node.js / TypeScript / React
    node_indicators = ['package.json', 'tsconfig.json', 'vite.config.ts', 'next.config.js']
    package_json = root_path / 'package.json'
    if package_json.exists():
        try:
            with open(package_json, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # If it's an OpenClaw skill metadata, return 'unknown' to allow other checks
                if 'openclaw' in data:
                    return 'unknown'
        except Exception:
            pass

    if any((root_path / f).exists() for f in node_indicators):
        return 'node'

    # Go
    if any((root_path / f).exists() for f in ['go.mod', 'go.sum']):
        return 'go'

    return 'unknown'


def find_files(root: str, extensions: List[str]) -> List[str]:
    """Recursively find files with given extensions, excluding common noise directories."""
    root_path = Path(root)
    all_files = []
    for ext in extensions:
        for f in root_path.rglob(f"*{ext}"):
            if not _should_exclude(f.relative_to(root_path)):
                all_files.append(str(f))
    return sorted(all_files)
