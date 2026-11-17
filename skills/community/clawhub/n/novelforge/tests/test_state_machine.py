import json
import hashlib
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.state import InvalidTransition, init_project, read_chapter_state, transition_chapter
from novelforge_engine.context import build_context
from novelforge_engine.review import apply_review
from novelforge_engine.io import sha256_file


class StateMachineTests(unittest.TestCase):
    def test_chapter_cannot_skip_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            with self.assertRaises(InvalidTransition):
                transition_chapter(root, "v01-c01", "DELIVERABLE")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            with self.assertRaises(InvalidTransition):
                transition_chapter(root, "v01-c01", "DRAFTED")
            build_context(root, "v01-c01")
            self.assertEqual(read_chapter_state(root, "v01-c01")["status"], "CONTEXT_LOCKED")

    def test_stale_upstream_review_invalidates_before_engine_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            blueprint = root / "blueprints" / "v01-c01.md"
            blueprint.write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            digest = sha256_file(body)
            apply_review(root, {"chapter": "v01-c01", "kind": "text", "source_hash": digest, "result": "PASS"})
            body.write_text("two", encoding="utf-8")
            new_digest = sha256_file(body)
            (root / ".novelforge" / "reviews" / "v01-c01-engine.json").write_text(
                json.dumps({"chapter": "v01-c01", "kind": "engine", "source_hash": new_digest, "result": "PASS"}), encoding="utf-8"
            )

            with self.assertRaises(InvalidTransition):
                transition_chapter(root, "v01-c01", "ENGINE_PASS")
            self.assertEqual(read_chapter_state(root, "v01-c01")["status"], "PLANNED")
            stale = json.loads((root / ".novelforge" / "reviews" / "v01-c01-text.json").read_text(encoding="utf-8"))
            self.assertEqual(stale["status"], "STALE")

    def test_transition_is_audited_and_reproducible(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            audit = (root / ".novelforge" / "audit.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertTrue(audit)
            self.assertEqual(json.loads(audit[-1])["to"], "BLUEPRINT_VALID")

    def test_transition_requires_artifact_for_drafted_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")

            with self.assertRaises(InvalidTransition):
                transition_chapter(root, "v01-c01", "DRAFTED")

    def test_settlement_gate_rejects_hand_written_unapplied_artifact(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.md").write_text('---\nid: v01-c01\nphase: scene\ndependencies: {}\n---\n# Scene\n', encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("draft", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            digest = sha256_file(body)
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            review_hashes = {
                kind: hashlib.sha256((root / ".novelforge" / "reviews" / ("v01-c01-" + kind + ".json")).read_bytes()).hexdigest()
                for kind in ("text", "engine")
            }
            (root / ".novelforge" / "settlements" / "v01-c01.json").write_text(
                json.dumps({"schema": 1, "chapter": "v01-c01", "source_hash": digest, "facts": [], "review_hashes": review_hashes}),
                encoding="utf-8",
            )
            with self.assertRaises(InvalidTransition):
                transition_chapter(root, "v01-c01", "SETTLED")


if __name__ == "__main__":
    unittest.main()
