import json
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.settlement import apply_settlement
from novelforge_engine.context import build_context
from novelforge_engine.review import apply_review
from novelforge_engine.state import init_project, transition_chapter
from novelforge_engine.settlement import SettlementError
from novelforge_engine.io import sha256_file, sha256_text


class SettlementTests(unittest.TestCase):
    def test_settlement_application_is_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            chapter = root / "chapters"
            body = chapter / "v01-c01.md"
            body.write_text("A chooses.", encoding="utf-8")
            digest = sha256_text(body.read_text(encoding="utf-8"))
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            settlement = {
                "chapter": "v01-c01", "source_hash": sha256_text(body.read_text(encoding="utf-8")),
                "facts": [{"id": "event.a", "type": "event", "summary": "A chooses."}],
            }
            first = apply_settlement(root, settlement)
            second = apply_settlement(root, settlement)
            self.assertFalse(first["idempotent"])
            self.assertTrue(second["idempotent"])
            self.assertEqual(len(list((root / "timeline").glob("*.md"))), 1)
            review_path = root / ".novelforge" / "reviews" / "v01-c01-text.json"
            review = json.loads(review_path.read_text(encoding="utf-8"))
            review["tampered"] = True
            review_path.write_text(json.dumps(review), encoding="utf-8")
            with self.assertRaises(SettlementError):
                apply_settlement(root, settlement)
            self.assertEqual(json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c01.json").read_text(encoding="utf-8"))["status"], "PLANNED")

    def test_settlement_rejects_path_escape_fact_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("draft", encoding="utf-8")
            digest = sha256_text("draft")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            settlement = {
                "chapter": "v01-c01",
                "source_hash": sha256_text("draft"),
                "facts": [{"id": "../escape", "type": "event"}],
            }
            with self.assertRaises(SettlementError):
                apply_settlement(root, settlement)

    def test_idempotent_settlement_rejects_changed_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one", encoding="utf-8")
            digest = sha256_text("one")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            settlement = {
                "chapter": "v01-c01",
                "source_hash": digest,
                "facts": [{"id": "event.old", "type": "event", "summary": "old"}],
            }
            apply_settlement(root, settlement)
            body.write_text("two", encoding="utf-8")

            with self.assertRaises(SettlementError):
                apply_settlement(root, settlement)
            marked = json.loads((root / ".novelforge" / "settlements" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(marked["status"], "STALE")
            review = json.loads((root / ".novelforge" / "reviews" / "v01-c01-text.json").read_text(encoding="utf-8"))
            self.assertEqual(review["status"], "STALE")

            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            new_digest = sha256_file(body)
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": new_digest, "result": "PASS"})
            apply_settlement(root, {"chapter": "v01-c01", "source_hash": new_digest, "facts": []})
            self.assertFalse((root / "timeline" / "event.old.md").exists())

    def test_new_settlement_after_review_source_change_invalidates_review_chain(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            old_digest = sha256_file(body)
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": old_digest, "result": "PASS"})
            body.write_text("two", encoding="utf-8")
            with self.assertRaises(SettlementError):
                apply_settlement(root, {"chapter": "v01-c01", "source_hash": old_digest, "facts": []})
            self.assertEqual(json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c01.json").read_text(encoding="utf-8"))["status"], "PLANNED")
            for kind in ("text", "engine"):
                review = json.loads((root / ".novelforge" / "reviews" / ("v01-c01-" + kind + ".json")).read_text(encoding="utf-8"))
                self.assertEqual(review["status"], "STALE")


if __name__ == "__main__":
    unittest.main()
