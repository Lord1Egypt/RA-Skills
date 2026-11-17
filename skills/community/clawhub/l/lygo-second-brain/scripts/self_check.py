#!/usr/bin/env python3
"""Self-check LYGO second brain (no live Ollama required)."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

STACK = Path(__file__).resolve().parents[4]
SCRIPTS = STACK / "lygo_second_brain" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from vault_lib import git_commit, sha256_of_file, slugify, write_note, read_note  # noqa: E402


def main() -> int:
    assert slugify("Hello, LYGO!") == "hello-lygo"
    with tempfile.TemporaryDirectory() as td:
        p = Path(td) / "t.txt"
        p.write_text("lygo", encoding="utf-8")
        h = sha256_of_file(p)
        assert len(h) == 64
        note = Path(td) / "n.md"
        write_note(note, {"title": "T", "tags": ["a", "b"]}, "body")
        fm, body = read_note(note)
        assert fm.get("title") == "T"
        assert body == "body"
        assert git_commit(Path(td), "test") in ("ok", "nothing-to-commit", "not-a-git-repo")
    vault = STACK / "lygo_second_brain" / "vault"
    for d in ("raw", "permanent", "wiki", "archive"):
        if not (vault / d).is_dir():
            print(f"FAIL missing {vault / d}")
            return 1
    print("OK lygo-second-brain self_check")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())