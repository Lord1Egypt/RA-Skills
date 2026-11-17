from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
import sys

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from scripts.novelforgectl import main
from novelforge_engine.pipeline import (
    advance_pipeline,
    get_pipeline_status,
    interrupt_pipeline,
    resume_pipeline,
)


class PipelineTests(unittest.TestCase):
    def test_pipeline_status_uninitialized(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            status = get_pipeline_status(root)
            self.assertEqual(status["status"], "UNINITIALIZED")
            self.assertEqual(status["next_action"], "INIT_PROJECT")

    def test_pipeline_end_to_end_advance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = "v01-c01"

            # 1. First advance: auto-inits project, stops because blueprint is missing
            res1 = advance_pipeline(root, chapter)
            self.assertEqual(res1["state"], "PLANNED")
            self.assertEqual(res1["stage"], "BLUEPRINT")
            self.assertEqual(res1["next_action"], "WRITE_BLUEPRINT")
            self.assertTrue(res1["interrupted"])

            # 2. Write blueprint and advance: moves to BLUEPRINT_VALID, then automatically builds context -> CONTEXT_LOCKED
            bp = {
                "id": chapter,
                "phase": "scene",
                "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []},
            }
            (root / "blueprints" / f"{chapter}.json").write_text(
                json.dumps(bp, ensure_ascii=False, indent=2), encoding="utf-8"
            )
            res2 = advance_pipeline(root, chapter)
            self.assertEqual(res2["state"], "CONTEXT_LOCKED")
            self.assertEqual(res2["stage"], "DRAFT")
            self.assertEqual(res2["next_action"], "WRITE_DRAFT")

            # 3. Write chapter draft and advance: moves to DRAFTED, stops for text review
            chapter_file = root / "chapters" / f"{chapter}.md"
            chapter_text = "夜色如墨。江面泛起一层薄雾，孤舟破水前行。\n陆沉立于船头，手中握着那枚冰凉的残玉。"
            chapter_file.write_text(chapter_text, encoding="utf-8")
            body_hash = hashlib.sha256(chapter_file.read_bytes()).hexdigest()

            res3 = advance_pipeline(root, chapter)
            self.assertEqual(res3["state"], "DRAFTED")
            self.assertEqual(res3["stage"], "TEXT_REVIEW")
            self.assertEqual(res3["next_action"], "PERFORM_TEXT_REVIEW")

            # 4. Write text review and advance: moves to TEXT_PASS, stops for engine review
            text_review = {
                "chapter": chapter,
                "kind": "text",
                "source_hash": body_hash,
                "result": "PASS",
                "checks": [{"rule": "style", "status": "PASS", "evidence": []}],
            }
            (root / ".novelforge" / "reviews" / f"{chapter}-text.json").write_text(
                json.dumps(text_review), encoding="utf-8"
            )

            res4 = advance_pipeline(root, chapter)
            self.assertEqual(res4["state"], "TEXT_PASS")
            self.assertEqual(res4["stage"], "ENGINE_REVIEW")
            self.assertEqual(res4["next_action"], "PERFORM_ENGINE_REVIEW")

            # 5. Write engine review and advance: moves to ENGINE_PASS, stops for settlement
            engine_review = {
                "chapter": chapter,
                "kind": "engine",
                "source_hash": body_hash,
                "result": "PASS",
                "checks": [{"rule": "continuity", "status": "PASS", "evidence": []}],
            }
            (root / ".novelforge" / "reviews" / f"{chapter}-engine.json").write_text(
                json.dumps(engine_review), encoding="utf-8"
            )

            res5 = advance_pipeline(root, chapter)
            self.assertEqual(res5["state"], "ENGINE_PASS")
            self.assertEqual(res5["stage"], "SETTLEMENT")
            self.assertEqual(res5["next_action"], "WRITE_SETTLEMENT")

            # 6. Write settlement and advance: moves to SETTLED -> rebuilds wiki -> DELIVERABLE
            settlement = {
                "schema": 1,
                "chapter": chapter,
                "source_hash": body_hash,
                "facts": [],
            }
            (root / ".novelforge" / "settlements" / f"{chapter}.json").write_text(
                json.dumps(settlement), encoding="utf-8"
            )

            res6 = advance_pipeline(root, chapter)
            self.assertEqual(res6["state"], "DELIVERABLE")
            self.assertEqual(res6["stage"], "COMPLETED")
            self.assertEqual(res6["next_action"], "COMPLETED")
            self.assertEqual(res6["status"], "COMPLETED")

    def test_pipeline_stop_at(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = "v01-c01"
            bp = {
                "id": chapter,
                "phase": "scene",
                "dependencies": {"entities": [], "hooks": [], "relations": [], "events": []},
            }
            root.mkdir(parents=True, exist_ok=True)
            (root / "blueprints").mkdir(parents=True, exist_ok=True)
            (root / "blueprints" / f"{chapter}.json").write_text(json.dumps(bp), encoding="utf-8")

            res = advance_pipeline(root, chapter, stop_at="BLUEPRINT_VALID")
            self.assertEqual(res["state"], "BLUEPRINT_VALID")
            self.assertTrue(res["interrupted"])
            self.assertIn("BLUEPRINT_VALID", res["interruption_reason"])

    def test_pipeline_cli_commands(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            chapter = "v01-c01"

            # CLI: status
            self.assertEqual(main(["pipeline", "status", str(root)]), 0)

            # CLI: advance (inits project)
            self.assertEqual(main(["pipeline", "advance", str(root), chapter]), 0)

            # CLI: interrupt
            self.assertEqual(
                main(["pipeline", "interrupt", str(root), chapter, "--reason", "Manual user pause"]), 0
            )
            status = get_pipeline_status(root, chapter)
            self.assertTrue(status["interrupted"])
            self.assertEqual(status["interruption_reason"], "Manual user pause")

            # CLI: resume
            self.assertEqual(main(["pipeline", "resume", str(root), chapter]), 0)


if __name__ == "__main__":
    unittest.main()
