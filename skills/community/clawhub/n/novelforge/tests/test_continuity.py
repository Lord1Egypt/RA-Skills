import json
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.context import ContextError, build_context
from novelforge_engine.review import apply_review
from novelforge_engine.engine import EngineValidationError, load_engine
from novelforge_engine.settlement import SettlementError, apply_settlement
from novelforge_engine.state import init_project, invalidate_chapter, transition_chapter
from novelforge_engine.wiki import rebuild_wiki
from novelforge_engine.io import read_frontmatter, sha256_file, sha256_text, write_frontmatter_atomic
from scripts.novelforgectl import main


class ContinuityTests(unittest.TestCase):
    def test_engine_rejects_card_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "engine"
            root.mkdir()
            (root / "engine.json").write_text(json.dumps({"id": "demo", "version": 1, "card_files": ["../outside.json"]}), encoding="utf-8")
            (Path(tmp) / "outside.json").write_text("[]", encoding="utf-8")
            with self.assertRaises(EngineValidationError):
                load_engine(root)

    def test_changed_blueprint_invalidates_locked_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps({"id": "v01-c01", "phase": "scene", "dependencies": {"entities": [], "hooks": [], "relations": []}}), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            path = root / "blueprints" / "v01-c01.json"
            path.write_text(path.read_text(encoding="utf-8").replace("scene", "choice"), encoding="utf-8")
            with self.assertRaises(ContextError):
                build_context(root, "v01-c01")
            self.assertEqual(json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c01.json").read_text(encoding="utf-8"))["status"], "PLANNED")

    def test_changed_dependency_invalidates_locked_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            entity = root / "characters" / "char.a.md"
            entity.write_text("---\nid: char.a\nname: A\ntype: character\n---\n", encoding="utf-8")
            blueprint = {
                "id": "v01-c01",
                "phase": "scene",
                "dependencies": {"entities": ["char.a"], "hooks": [], "relations": [], "events": []},
            }
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            entity.write_text("---\nid: char.a\nname: Changed\ntype: character\n---\n", encoding="utf-8")

            with self.assertRaises(ContextError):
                build_context(root, "v01-c01")
            stale = json.loads((root / ".novelforge" / "context" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(stale["status"], "STALE")

    def test_changed_engine_snapshot_invalidates_locked_context(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project = root / "project"
            source = root / "engine"
            (source / "cards").mkdir(parents=True)
            (source / "engine.json").write_text(json.dumps({"id": "custom", "version": 1, "kind": "narrative-engine", "card_files": ["cards/cards.json"]}), encoding="utf-8")
            (source / "applicability.md").write_text("custom applicability", encoding="utf-8")
            (source / "limits.md").write_text("custom limits", encoding="utf-8")
            (source / "cards" / "cards.json").write_text(
                json.dumps([{"id": "C-1", "kind": "model", "name": "choice", "when": {}, "hardness": "optional", "prompt": "choice"}]),
                encoding="utf-8",
            )
            main(["project", "init", str(project)])
            main(["engine", "install", str(project), str(source)])
            main(["engine", "use", str(project), "custom"])
            blueprint = {"id": "v01-c01", "phase": "scene", "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []}}
            (project / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            main(["blueprint", "validate", str(project), "v01-c01"])
            ticket = build_context(project, "v01-c01")
            self.assertIn("C-1", ticket["engine_snapshot"]["active_cards"])
            card_path = project / ".novelforge" / "engines" / "custom" / "cards" / "cards.json"
            card_path.write_text(card_path.read_text(encoding="utf-8").replace("choice", "changed"), encoding="utf-8")
            main(["engine", "manifest", str(project / ".novelforge" / "engines" / "custom")])

            with self.assertRaises(ContextError):
                build_context(project, "v01-c01")
            stale = json.loads((project / ".novelforge" / "context" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(stale["status"], "STALE")

    def test_context_rejects_unsafe_active_engine_id(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            project = root / ".novelforge" / "state" / "project.json"
            profile = json.loads(project.read_text(encoding="utf-8"))
            profile["engine"] = "../outside"
            project.write_text(json.dumps(profile), encoding="utf-8")
            blueprint = root / "blueprints" / "v01-c01.json"
            blueprint.write_text(json.dumps({"id": "v01-c01", "phase": "scene", "dependencies": {}}), encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            with self.assertRaises(ContextError):
                build_context(root, "v01-c01")

    def test_stale_settlement_is_flagged_when_body_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one", encoding="utf-8")
            (root / "blueprints" / "v01-c01.json").write_text('{"id":"v01-c01","phase":"scene","dependencies":{}}', encoding="utf-8")
            digest = sha256_file(body)
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            settlement = {"chapter": "v01-c01", "source_hash": sha256_file(body), "facts": []}
            apply_settlement(root, settlement)
            body.write_text("two", encoding="utf-8")
            with self.assertRaises(SettlementError):
                apply_settlement(root, {"chapter": "v01-c01", "source_hash": sha256_file(body), "facts": []})
            marked = json.loads((root / ".novelforge" / "settlements" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(marked["status"], "STALE")

    def test_next_chapter_rejects_projection_when_source_body_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            first_blueprint = root / "blueprints" / "v01-c01.json"
            first_blueprint.write_text(json.dumps({"id": "v01-c01", "phase": "scene", "dependencies": {}}), encoding="utf-8")
            first_body = root / "chapters" / "v01-c01.md"
            first_body.write_text("first", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            digest = sha256_file(first_body)
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            apply_settlement(root, {"chapter": "v01-c01", "source_hash": digest, "facts": [{"id": "char.a", "type": "character", "name": "A"}]})

            second_blueprint = root / "blueprints" / "v01-c02.json"
            second_blueprint.write_text(
                json.dumps({"id": "v01-c02", "phase": "scene", "dependencies": {"entities": ["char.a"]}}),
                encoding="utf-8",
            )
            transition_chapter(root, "v01-c02", "BLUEPRINT_VALID")
            build_context(root, "v01-c02")
            first_body.write_text("rewritten", encoding="utf-8")
            with self.assertRaises(ContextError):
                build_context(root, "v01-c02")
            self.assertEqual(json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c02.json").read_text(encoding="utf-8"))["status"], "PLANNED")
            self.assertEqual(json.loads((root / ".novelforge" / "context" / "v01-c02.json").read_text(encoding="utf-8"))["status"], "STALE")

    def test_next_chapter_rejects_tampered_source_projection(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            blueprint = root / "blueprints" / "v01-c01.json"
            blueprint.write_text(json.dumps({"id": "v01-c01", "phase": "scene", "dependencies": {}}), encoding="utf-8")
            body = root / "chapters" / "v01-c01.md"
            body.write_text("first", encoding="utf-8")
            transition_chapter(root, "v01-c01", "BLUEPRINT_VALID")
            build_context(root, "v01-c01")
            transition_chapter(root, "v01-c01", "DRAFTED")
            digest = sha256_file(body)
            for kind in ("text", "engine"):
                apply_review(root, {"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"})
            apply_settlement(root, {"chapter": "v01-c01", "source_hash": digest, "facts": [{"id": "char.a", "type": "character", "name": "A"}]})
            second = root / "blueprints" / "v01-c02.json"
            second.write_text(json.dumps({"id": "v01-c02", "phase": "scene", "dependencies": {"entities": ["char.a"]}}), encoding="utf-8")
            transition_chapter(root, "v01-c02", "BLUEPRINT_VALID")
            build_context(root, "v01-c02")
            projection = root / "characters" / "char.a.md"
            meta, pbody = read_frontmatter(projection)
            meta["name"] = "tampered"
            write_frontmatter_atomic(projection, meta, pbody)
            with self.assertRaises(ContextError):
                build_context(root, "v01-c02")
            self.assertEqual(json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c02.json").read_text(encoding="utf-8"))["status"], "PLANNED")

    def test_wiki_rebuild_is_deterministic_and_wiki_readable(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            entity = root / "characters" / "char.a.md"
            entity.write_text("---\nid: char.a\nname: A\nsummary: choice\ntype: character\n---\n", encoding="utf-8")
            first = rebuild_wiki(root)
            first_bytes = (root / "characters" / "char.a.md").read_bytes()
            second = rebuild_wiki(root)
            self.assertEqual(first, second)
            self.assertEqual(first_bytes, (root / "characters" / "char.a.md").read_bytes())
            self.assertIn("[[characters/char.a]]", (root / "index.md").read_text(encoding="utf-8"))

    def test_wiki_rebuild_indexes_and_cleans_deleted_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            entity = root / "characters" / "char.a.md"
            entity.write_text("---\nid: char.a\nname: A\ntype: character\n---\n", encoding="utf-8")
            rebuild_wiki(root)
            self.assertIn("[[characters/char.a]]", (root / "index.md").read_text(encoding="utf-8"))
            entity.unlink()
            rebuild_wiki(root)
            self.assertNotIn("[[characters/char.a]]", (root / "index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
