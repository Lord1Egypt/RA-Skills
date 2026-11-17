import json
import hashlib
import tempfile
import unittest
from pathlib import Path

import sys
SKILL_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SKILL_ROOT))

from scripts.novelforgectl import main


class CliTests(unittest.TestCase):
    def test_cli_initializes_project_and_validates_blueprint(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            blueprint = {"id": "v01-c01", "phase": "scene", "dependencies": {"entities": [], "hooks": [], "relations": []}}
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 0)
            state = json.loads((root / ".novelforge" / "state" / "chapters" / "v01-c01.json").read_text(encoding="utf-8"))
            self.assertEqual(state["status"], "BLUEPRINT_VALID")

    def test_blueprint_rejects_empty_phase(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            blueprint = {"id": "v01-c01", "phase": "", "dependencies": {}}
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 1)

    def test_blueprint_rejects_malformed_optional_scene(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            blueprint = {"id": "v01-c01", "phase": "scene", "dependencies": {}, "scenes": [{"id": "scene-1"}]}
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 1)

    def test_engine_install_does_not_run_style_detector(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "engine"
            source.mkdir()
            (source / "engine.json").write_text(json.dumps({"id": "custom", "version": 1, "kind": "narrative-engine", "card_files": []}), encoding="utf-8")
            (source / "applicability.md").write_text("custom applicability", encoding="utf-8")
            (source / "limits.md").write_text("custom limits", encoding="utf-8")
            project = root / "project"
            self.assertEqual(main(["project", "init", str(project)]), 0)
            self.assertEqual(main(["engine", "install", str(project), str(source)]), 0)
            self.assertTrue((project / ".novelforge" / "engines" / "custom" / "engine.json").exists())

    def test_engine_use_activates_installed_engine_through_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "engine"
            source.mkdir()
            (source / "engine.json").write_text(
                json.dumps({"id": "custom", "version": 1, "kind": "narrative-engine", "card_files": []}),
                encoding="utf-8",
            )
            (source / "applicability.md").write_text("custom applicability", encoding="utf-8")
            (source / "limits.md").write_text("custom limits", encoding="utf-8")
            project = root / "project"
            self.assertEqual(main(["project", "init", str(project)]), 0)
            self.assertEqual(main(["engine", "install", str(project), str(source)]), 0)
            self.assertEqual(main(["engine", "use", str(project), "custom"]), 0)
            profile = json.loads((project / ".novelforge" / "state" / "project.json").read_text(encoding="utf-8"))
            self.assertEqual(profile["engine"], "custom")

    def test_cli_completes_review_settlement_and_wiki_delivery_gates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            blueprint = {
                "id": "v01-c01",
                "phase": "scene",
                "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []},
            }
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 0)
            self.assertEqual(main(["context", "build", str(root), "v01-c01"]), 0)
            body = root / "chapters" / "v01-c01.md"
            body.write_text("A chooses.", encoding="utf-8")
            self.assertEqual(main(["chapter", "transition", str(root), "v01-c01", "DRAFTED"]), 0)
            source_hash = hashlib.sha256(body.read_bytes()).hexdigest()
            text_review = root / "text-review.json"
            text_review.write_text(json.dumps({
                "chapter": "v01-c01", "kind": "text", "source_hash": source_hash,
                "result": "PASS", "checks": []
            }), encoding="utf-8")
            self.assertEqual(main(["review", "apply", str(root), str(text_review)]), 0)
            engine_review = root / "engine-review.json"
            engine_review.write_text(json.dumps({
                "chapter": "v01-c01", "kind": "engine", "source_hash": source_hash,
                "result": "PASS", "checks": []
            }), encoding="utf-8")
            self.assertEqual(main(["review", "apply", str(root), str(engine_review)]), 0)
            settlement = root / "settlement.json"
            settlement.write_text(json.dumps({
                "chapter": "v01-c01", "source_hash": source_hash,
                "facts": [{"id": "event.a", "type": "event", "summary": "A chooses."}]
            }), encoding="utf-8")
            self.assertEqual(main(["settlement", "apply", str(root), str(settlement)]), 0)
            self.assertEqual(main(["wiki", "rebuild", str(root)]), 0)
            self.assertEqual(main(["chapter", "transition", str(root), "v01-c01", "DELIVERABLE"]), 0)
            self.assertEqual(main(["project", "verify", str(root)]), 0)

    def test_project_verify_rejects_manually_changed_wiki_page(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            blueprint = {"id": "v01-c01", "phase": "scene", "dependencies": {}}
            (root / "blueprints" / "v01-c01.json").write_text(json.dumps(blueprint), encoding="utf-8")
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 0)
            self.assertEqual(main(["context", "build", str(root), "v01-c01"]), 0)
            (root / "chapters" / "v01-c01.md").write_text("A chooses.", encoding="utf-8")
            self.assertEqual(main(["chapter", "transition", str(root), "v01-c01", "DRAFTED"]), 0)
            digest = hashlib.sha256(b"A chooses.").hexdigest()
            for kind in ("text", "engine"):
                artifact = root / (kind + "-review.json")
                artifact.write_text(json.dumps({"chapter": "v01-c01", "kind": kind, "source_hash": digest, "result": "PASS"}), encoding="utf-8")
                self.assertEqual(main(["review", "apply", str(root), str(artifact)]), 0)
            settlement = root / "settlement.json"
            settlement.write_text(json.dumps({"chapter": "v01-c01", "source_hash": digest, "facts": []}), encoding="utf-8")
            self.assertEqual(main(["settlement", "apply", str(root), str(settlement)]), 0)
            self.assertEqual(main(["wiki", "rebuild", str(root)]), 0)
            self.assertEqual(main(["chapter", "transition", str(root), "v01-c01", "DELIVERABLE"]), 0)
            index = root / "index.md"
            index.write_text(index.read_text(encoding="utf-8") + "tampered\n", encoding="utf-8")
            self.assertEqual(main(["project", "verify", str(root)]), 1)

    def test_project_verify_rejects_context_ticket_with_blueprint_dependency_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            (root / "blueprints" / "v01-c01.json").write_text(
                json.dumps({"id": "v01-c01", "phase": "scene", "dependencies": {"entities": []}}),
                encoding="utf-8",
            )
            self.assertEqual(main(["blueprint", "validate", str(root), "v01-c01"]), 0)
            self.assertEqual(main(["context", "build", str(root), "v01-c01"]), 0)
            context_path = root / ".novelforge" / "context" / "v01-c01.json"
            context = json.loads(context_path.read_text(encoding="utf-8"))
            context["dependencies"] = {"entities": [], "hooks": ["hook.missing"]}
            context_path.write_text(json.dumps(context), encoding="utf-8")
            self.assertEqual(main(["project", "verify", str(root)]), 1)

    def test_cli_project_verify_accepts_initialized_project(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            self.assertEqual(main(["project", "verify", str(root)]), 0)

    def test_project_verify_rejects_missing_active_engine(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            project_file = root / ".novelforge" / "state" / "project.json"
            project = json.loads(project_file.read_text(encoding="utf-8"))
            project["engine"] = "missing"
            project_file.write_text(json.dumps(project), encoding="utf-8")
            self.assertEqual(main(["project", "verify", str(root)]), 1)

    def test_style_detection_is_advisory_until_project_promotes_rule(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = root / "chapter.txt"
            chapter.write_text("猫腻式的示例文本", encoding="utf-8")
            self.assertEqual(main(["style", "detect", str(chapter)]), 0)

            (root / ".novelforge" / "state").mkdir(parents=True)
            (root / ".novelforge" / "state" / "project.json").write_text(
                json.dumps({"schema": 1, "engine": "jin-yong", "blocking_rules": ["author-reference"]}),
                encoding="utf-8",
            )
            self.assertEqual(main(["style", "detect", str(chapter)]), 1)

    def test_project_verify_reports_changed_body_after_settlement(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            body = root / "chapters" / "v01-c01.md"
            body.write_text("one", encoding="utf-8")
            chapter_state = root / ".novelforge" / "state" / "chapters" / "v01-c01.json"
            chapter_state.write_text(json.dumps({"chapter": "v01-c01", "status": "DELIVERABLE", "version": 7}), encoding="utf-8")
            settlement = root / ".novelforge" / "settlements" / "v01-c01.json"
            settlement.write_text(json.dumps({"chapter": "v01-c01", "source_hash": hashlib.sha256(b"old").hexdigest(), "facts": []}), encoding="utf-8")

            self.assertEqual(main(["project", "verify", str(root)]), 1)

    def test_project_verify_rejects_malformed_profile_collections(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            project_file = root / ".novelforge" / "state" / "project.json"
            project = json.loads(project_file.read_text(encoding="utf-8"))
            project["engines"] = "jin-yong"
            project["style_detectors"] = "disabled"
            project_file.write_text(json.dumps(project), encoding="utf-8")

            self.assertEqual(main(["project", "verify", str(root)]), 1)

    def test_project_verify_rejects_forged_drafted_state_without_upstream_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.assertEqual(main(["project", "init", str(root)]), 0)
            (root / "chapters" / "v01-c01.md").write_text("draft", encoding="utf-8")
            (root / ".novelforge" / "state" / "chapters" / "v01-c01.json").write_text(
                json.dumps({"chapter": "v01-c01", "status": "DRAFTED", "version": 1}), encoding="utf-8"
            )
            self.assertEqual(main(["project", "verify", str(root)]), 1)


if __name__ == "__main__":
    unittest.main()
