#!/usr/bin/env python3
# Copyright (c) 2026 ratingtesting — MIT-0 (see LICENSE). Free to use/modify/redistribute, no attribution required.
"""Tests for scripts/build_skill.py (v1.10.2).

Covers:
- --check passes when SKILL.full.md is up to date
- --check fails when index changed but full not rebuilt
- recursive glob (bindings/, bootstrap/ included in full)
- idempotent output (rebuild == rebuild)
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "scripts" / "build_skill.py"
SKILL_MD = ROOT / "SKILL.md"
FULL_MD = ROOT / "SKILL.full.md"


def _run(args, cwd=ROOT):
    return subprocess.run(
        [sys.executable, str(BUILD)] + args,
        cwd=str(cwd), capture_output=True, text=True,
    )


def test_build_check_passes_when_fresh():
    """If SKILL.full.md exists and matches, --check exits 0."""
    # ensure full is built
    r = _run([])
    assert r.returncode == 0, r.stderr
    r = _run(["--check"])
    assert r.returncode == 0, r.stderr


def test_build_check_fails_when_index_changed():
    """If we touch SKILL.md, --check must exit 1 (drift detection)."""
    backup = SKILL_MD.read_text(encoding="utf-8")
    try:
        SKILL_MD.write_text(backup + "\n<!-- drift probe -->\n", encoding="utf-8")
        r = _run(["--check"])
        assert r.returncode == 1, f"--check should fail on drift, got rc={r.returncode}: {r.stderr}"
    finally:
        SKILL_MD.write_text(backup, encoding="utf-8")


def test_recursive_glob_includes_bindings():
    """bindings/*.md must be inlined into SKILL.full.md (was M3: glob was non-recursive)."""
    _run([])  # rebuild
    full = FULL_MD.read_text(encoding="utf-8")
    assert "references/bindings/" in full, "bindings/ not inlined — rglob regression"


def test_recursive_glob_includes_bootstrap():
    """bootstrap/*.md must be inlined into SKILL.full.md."""
    _run([])
    full = FULL_MD.read_text(encoding="utf-8")
    assert "references/bootstrap/" in full, "bootstrap/ not inlined — rglob regression"


def test_full_doc_has_no_appendix_in_index():
    """The index (SKILL.md) must NOT contain the APPENDIX marker (C1 fix)."""
    idx = SKILL_MD.read_text(encoding="utf-8")
    assert "APPENDIX" not in idx, "SKILL.md still contains APPENDIX — index broken"


def test_output_idempotent():
    """Two consecutive builds produce byte-identical SKILL.full.md."""
    _run([])
    h1 = FULL_MD.read_bytes()
    _run([])
    h2 = FULL_MD.read_bytes()
    assert h1 == h2, "build_skill output is not idempotent"
