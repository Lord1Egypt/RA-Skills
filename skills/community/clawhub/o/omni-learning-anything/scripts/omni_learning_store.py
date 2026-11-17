"""Guarded owner-only assessment files. Callers serialize writes with the course lock."""
import hashlib
import json
import os
import tempfile
from pathlib import Path
import omni_core as c


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False).encode()).hexdigest()


def path(root, *parts):
    root = Path(root).resolve(); base = root/'learning'; target = base.joinpath(*parts)
    if not target.resolve().is_relative_to(base.resolve()) or not base.resolve().is_relative_to(root):
        raise ValueError('Assessment path escapes the course archive.')
    for item in [base, target, *target.parents]:
        if item == root: break
        if item.is_symlink(): raise ValueError('Assessment storage cannot use symlinks.')
    return target


def save(root, parts, value):
    target = path(root, *parts)
    # Only the private assessment subtree is created; course files are untouched.
    parent = Path(root).resolve()/'learning'; parent.mkdir(mode=0o700, exist_ok=True)
    for part in target.relative_to(parent).parts[:-1]:
        parent = parent/part; parent.mkdir(mode=0o700, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=target.parent, delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2, allow_nan=False); stream.write('\n')
        os.replace(temporary, target)
    finally:
        if temporary and temporary.exists(): temporary.unlink()


def records(root):
    target = path(root, 'records.json')
    if not target.exists(): return {'schema': 1, 'attempts': {}}
    value = c.read(target)
    if not isinstance(value, dict) or set(value) != {'schema', 'attempts'} or value['schema'] != 1 or not isinstance(value['attempts'], dict):
        raise ValueError('Invalid assessment records; preserve/export the file for recovery.')
    return value


def quizzes(root):
    folder = path(root, 'quizzes')
    return sorted(folder.glob('Day*.v*.json')) if folder.exists() else []
