#!/usr/bin/env python3
"""Apply exact line patches with an optional source hash precondition."""

import hashlib
import os
import re
import sys
import tempfile
from pathlib import Path


_BLOCK = re.compile(r"<<<<\s*(\d+)-(\d+)\s*\n(.*?)\n====\n(.*?)\n>>>>", re.DOTALL)


def parse_patch(patch_text):
    """Parse all exact replacement blocks from a patch document."""
    blocks = []
    for start, end, original, replacement in _BLOCK.findall(patch_text):
        blocks.append({"start": int(start), "end": int(end), "orig": original, "new": replacement})
    return blocks


def _sha256(data):
    return hashlib.sha256(data).hexdigest()


def _invalidate_project_chapter(file_path):
    """Invalidate a project chapter after a successful body replacement."""
    target = Path(file_path).resolve()
    if target.suffix not in (".txt", ".md") or target.parent.name != "chapters":
        return True
    project_root = target.parent.parent
    if project_root.name == "wiki":
        project_root = project_root.parent
    profile = project_root / ".novelforge" / "state" / "project.json"
    if not profile.is_file():
        return True
    if target.parent.is_symlink():
        print("error: project chapters directory must not be a symlink")
        return False
    skill_root = Path(__file__).resolve().parents[1]
    if str(skill_root) not in sys.path:
        sys.path.insert(0, str(skill_root))
    try:
        from novelforge_engine.state import invalidate_chapter

        invalidate_chapter(project_root, target.stem, "chapter body changed by apply_patch")
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print("error: project chapter invalidation failed: {}".format(exc))
        return False
    return True


def apply_patch(file_path, patch_text, expected_sha256=None):
    """Apply every block or leave the original file byte-for-byte unchanged."""
    if not os.path.exists(file_path):
        print("error: target file does not exist: {}".format(file_path))
        return False
    try:
        with open(file_path, "rb") as handle:
            original_bytes = handle.read()
        original_text = original_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        print("error: target is not readable UTF-8: {}".format(exc))
        return False
    if expected_sha256 and _sha256(original_bytes) != expected_sha256:
        print("error: source SHA-256 does not match")
        return False
    lines = original_text.splitlines(keepends=True)
    blocks = sorted(parse_patch(patch_text), key=lambda item: item["start"], reverse=True)
    if not blocks:
        print("error: no patch blocks found")
        return False
    for block in blocks:
        start = block["start"] - 1
        end = block["end"] - 1
        if start < 0 or end >= len(lines) or start > end:
            print("error: patch range is outside the file: {}-{}".format(block["start"], block["end"]))
            return False
        expected = block["orig"]
        actual = "".join(lines[start : end + 1])
        if actual.endswith("\n") and not expected.endswith("\n"):
            expected += "\n"
        if expected != actual:
            print("error: patch source does not match lines {}-{}".format(block["start"], block["end"]))
            return False
        replacement = [line if line.endswith("\n") else line + "\n" for line in block["new"].splitlines(keepends=True)]
        lines[start : end + 1] = replacement
    updated_bytes = "".join(lines).encode("utf-8")
    directory = os.path.dirname(os.path.abspath(file_path)) or "."
    descriptor, temp_path = tempfile.mkstemp(prefix=".patch-", dir=directory)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(updated_bytes)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, file_path)
    except OSError as exc:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        print("error: atomic patch write failed: {}".format(exc))
        return False
    if not _invalidate_project_chapter(file_path):
        return False
    return True


def main():
    if len(sys.argv) < 3:
        print("usage: python apply_patch.py <file> <patch-file-or-text> [source-sha256]")
        return 1
    file_path, patch_source = sys.argv[1:3]
    if os.path.exists(patch_source):
        with open(patch_source, "r", encoding="utf-8") as handle:
            patch_text = handle.read()
    else:
        patch_text = patch_source
    return 0 if apply_patch(file_path, patch_text, sys.argv[3] if len(sys.argv) > 3 else None) else 1


if __name__ == "__main__":
    sys.exit(main())
