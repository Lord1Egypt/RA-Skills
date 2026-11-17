import json
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.review import apply_review
from novelforge_engine.context import build_context
from novelforge_engine.state import init_project, transition_chapter
from novelforge_engine.io import sha256_file


class ReviewTests(unittest.TestCase):
    def test_review_requires_matching_body_and_advances_one_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("draft", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            review = {"chapter": "v01-c01", "kind": "text", "source_hash": sha256_file(body), "result": "PASS", "checks": []}
            result = apply_review(root, review)
            self.assertEqual(result["status"], "TEXT_PASS")

    def test_review_rejects_path_escape_chapter_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            review = {"chapter": "../outside", "kind": "text", "source_hash": "0" * 64, "result": "PASS"}
            with self.assertRaises(ValueError):
                apply_review(root, review)


if __name__ == "__main__":
    unittest.main()
