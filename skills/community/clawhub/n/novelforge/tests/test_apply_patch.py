import hashlib
import tempfile
import unittest
from pathlib import Path

from importlib.util import module_from_spec, spec_from_file_location

PATCH_PATH = Path(__file__).resolve().parents[1] / "scripts" / "apply_patch.py"
spec = spec_from_file_location("apply_patch", PATCH_PATH)
module = module_from_spec(spec)
spec.loader.exec_module(module)


class ApplyPatchTests(unittest.TestCase):
    def test_mismatch_does_not_write_any_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_bytes(b"one\ntwo\n")
            before = path.read_bytes()
            patch = "<<<< 1-1\nWRONG\n====\nnew\n>>>>"
            self.assertFalse(module.apply_patch(str(path), patch))
            self.assertEqual(path.read_bytes(), before)

    def test_matching_hash_and_text_replaces_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "chapter.txt"
            path.write_bytes(b"one\ntwo\n")
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            patch = "<<<< 1-1\none\n====\nONE\n>>>>"
            self.assertTrue(module.apply_patch(str(path), patch, expected_sha256=digest))
            self.assertEqual(path.read_bytes(), b"ONE\ntwo\n")

    def test_project_chapter_patch_invalidates_downstream_state(self):
        import json
        import sys

        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from novelforge_engine.context import build_context
        from novelforge_engine.state import init_project, transition_chapter

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n', encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one\n", encoding="utf-8")
            digest = hashlib.sha256(body.read_bytes()).hexdigest()
            patch = "<<<< 1-1\none\n====\ntwo\n>>>>"
            self.assertTrue(module.apply_patch(str(body), patch, expected_sha256=digest))
            state = json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c01.json").read_text(encoding="utf-8"))
            ticket = json.loads((root / ".novelforge" / "context" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "PLANNED")
            self.assertEqual(ticket["status"], "STALE")


if __name__ == "__main__":
    unittest.main()
