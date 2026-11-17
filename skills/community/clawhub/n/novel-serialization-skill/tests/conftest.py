"""Shared fixtures for the script test suite.

The scripts under ``scripts/`` are standalone CLI tools, not an installed
package, so they are imported by path rather than by module name. This file
puts them on ``sys.path`` once and provides a small builder for throwaway
repository trees.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent.parent / "scripts"
sys.path.insert(0, str(SCRIPTS))


def _write(root: Path, rel: str, text: str) -> Path:
    """Write ``text`` at ``root/rel`` with LF endings and UTF-8; return the path."""
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(text.encode("utf-8"))
    return p


@pytest.fixture
def tree(tmp_path):
    """Return a ``write(rel, text)`` callable rooted at a fresh directory."""
    root = tmp_path / "repo"
    root.mkdir()

    def write(rel: str, text: str) -> Path:
        return _write(root, rel, text)

    write.root = root  # type: ignore[attr-defined]
    return write
