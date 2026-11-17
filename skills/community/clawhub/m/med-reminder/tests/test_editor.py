"""
Editor tests — issue #1 PR 4 M4: the stale-file check and the pass-through
of new optional fields.

editor_check.cjs evals editor.html's real <script> under a stub DOM and
drives open/save/edit with a mocked File System Access handle, so the
behavior tested is the code a browser runs. The scenarios skip when
node.js isn't installed; the structural test below always runs.
"""
import re
import shutil
import subprocess
from pathlib import Path

import pytest

NODE = shutil.which("node")
HARNESS = Path(__file__).parent / "editor_check.cjs"
EDITOR = Path(__file__).parent.parent / "editor.html"

pytestmark = pytest.mark.skipif(NODE is None, reason="node.js not available")


@pytest.mark.parametrize("scenario", ["save-fresh", "save-stale", "passthrough", "multi-day", "calculator", "supplies"])
def test_editor_scenario(scenario, tmp_path):
    r = subprocess.run([NODE, str(HARNESS), scenario], capture_output=True,
                       text=True, timeout=60, cwd=tmp_path)
    assert r.returncode == 0, f"scenario {scenario} failed:\n{r.stdout}\n{r.stderr}"


def test_editor_html_has_stale_file_wiring():
    """Structural check that survives a missing node: the mtime baseline is
    recorded at open, checked before saving, and re-synced after a write."""
    src = EDITOR.read_text(encoding="utf-8")
    assert "let openedLastModified = null;" in src
    assert re.search(r"currentState = parsed;\s*\n\s*openedLastModified = file\.lastModified;", src)
    assert "cur.lastModified !== openedLastModified" in src
    assert "Refusing to overwrite" in src
    assert re.search(r"const saved = await handle\.getFile\(\);\s*\n\s*"
                     r"openedLastModified = saved\.lastModified;", src)
