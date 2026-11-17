import json
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.context import build_context
from novelforge_engine.io import sha256_file
from novelforge_engine.state import init_project, transition_chapter


class ContextTests(unittest.TestCase):
    def test_context_loads_only_explicit_dependency_ids(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "characters" / "char.a.md").write_text("---\nid: char.a\nname: A\ntype: character\n---\n", encoding="utf-8")
            (root / "characters" / "char.unrelated.md").write_text("---\nid: char.unrelated\nname: U\ntype: character\n---\n", encoding="utf-8")
            blueprint = {
                "id": "v01-c01", "phase": "scene",
                "dependencies": {"entities": ["char.a"], "hooks": [], "relations": []},
            }
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            ticket = build_context(root, "v01-c01")
            self.assertEqual(ticket["dependencies"]["entities"], ["char.a"])
            self.assertNotIn("char.unrelated", json.dumps(ticket))
            self.assertEqual(ticket["status"], "LOCKED")

    def test_context_hashes_are_namespaced_by_dependency_collection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "entities" / "shared.md").write_text("---\nid: shared\ntype: entity\n---\n", encoding="utf-8")
            (root / "hooks" / "shared.md").write_text("---\nid: shared\ntype: hook\n---\n", encoding="utf-8")
            blueprint = {
                "id": "v01-c01",
                "phase": "scene",
                "dependencies": {"entities": ["shared"], "hooks": ["shared"], "relations": [], "events": []},
            }
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            ticket = build_context(root, "v01-c01")

            self.assertIn("entities:shared", ticket["dependency_hashes"])
            self.assertIn("hooks:shared", ticket["dependency_hashes"])

    def test_context_records_only_engine_cards_matching_chapter_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            blueprint = {
                "id": "v01-c01",
                "phase": "scene",
                "scene_types": ["relationship"],
                "state": {"character": True, "emotional_change": True},
                "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []},
            }
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            ticket = build_context(root, "v01-c01")
            self.assertEqual(ticket["engine_snapshot"]["id"], "jin-yong")
            self.assertIn("JY-M2", ticket["engine_snapshot"]["active_cards"])
            self.assertNotIn("JY-T8", ticket["engine_snapshot"]["active_cards"])
            self.assertEqual(
                ticket["engine_snapshot"]["source_hashes"]["engine.json"],
                sha256_file(SKILL_ROOT / "engines" / "jin-yong" / "engine.json"),
            )


if __name__ == "__main__":
    unittest.main()
