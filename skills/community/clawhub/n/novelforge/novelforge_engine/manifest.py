"""Create and verify content hashes for an embedded engine snapshot."""

import hashlib
import json
from pathlib import Path

from .io import read_json, write_json_atomic


def _hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _files(root):
    for path in sorted(Path(root).rglob("*")):
        if path.is_file() and path.name != "manifest.json":
            yield path


def build_manifest(root):
    root = Path(root).resolve()
    engine = read_json(root / "engine.json")
    return {
        "schema": 1,
        "engine": engine.get("id"),
        "files": {str(path.relative_to(root)): _hash(path) for path in _files(root)},
    }


def write_manifest(root):
    manifest = build_manifest(root)
    write_json_atomic(Path(root) / "manifest.json", manifest)
    return manifest


def verify_manifest(root, manifest=None):
    root = Path(root).resolve()
    if manifest is None:
        try:
            manifest = read_json(root / "manifest.json")
        except (OSError, ValueError):
            return False
    if not isinstance(manifest, dict) or manifest.get("schema") != 1 or not isinstance(manifest.get("engine"), str):
        return False
    expected = manifest.get("files", {})
    if not isinstance(expected, dict) or any(
        not isinstance(relative, str) or not isinstance(digest, str) or len(digest) != 64
        for relative, digest in expected.items()
    ):
        return False
    actual = {str(path.relative_to(root)): _hash(path) for path in _files(root)}
    try:
        engine_id = read_json(root / "engine.json").get("id")
    except (OSError, ValueError, AttributeError):
        return False
    return expected == actual and manifest.get("engine") == engine_id
