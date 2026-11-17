import json
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]

import sys
sys.path.insert(0, str(SKILL_ROOT))

from novelforge_engine.engine import EngineValidationError, load_engine, select_cards


class EngineTests(unittest.TestCase):
    def test_embedded_jin_yong_engine_is_self_contained_and_selective(self):
        engine_root = SKILL_ROOT / "engines" / "jin-yong"
        engine = load_engine(engine_root)
        self.assertEqual(engine["id"], "jin-yong")
        self.assertNotIn("jin-yong-writing-perspective", json.dumps(engine, ensure_ascii=False))
        cards = select_cards(engine_root, {
            "phase": "scene",
            "scene_type": "relationship",
            "long_form": True,
            "emotional_change": True,
        })
        card_ids = {card["id"] for card in cards}
        self.assertIn("JY-M2", card_ids)
        self.assertNotIn("JY-T8", card_ids)

    def test_invalid_engine_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bad"
            root.mkdir()
            (root / "engine.json").write_text(json.dumps({"name": "bad"}), encoding="utf-8")
            with self.assertRaises(EngineValidationError):
                load_engine(root)

    def test_method_card_requires_contract_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bad"
            (root / "cards").mkdir(parents=True)
            (root / "engine.json").write_text(
                json.dumps({"id": "demo", "version": 1, "card_files": ["cards/cards.json"]}),
                encoding="utf-8",
            )
            (root / "cards" / "cards.json").write_text(
                json.dumps([{"id": "D-1", "kind": "model", "name": "incomplete", "when": {}}]),
                encoding="utf-8",
            )
            with self.assertRaises(EngineValidationError):
                load_engine(root)

    def test_engine_rejects_non_list_card_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "engine.json").write_text(
                json.dumps({"id": "demo", "version": 1, "card_files": "cards.json"}),
                encoding="utf-8",
            )
            with self.assertRaises(EngineValidationError):
                load_engine(root)

    def test_engine_validation_requires_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "engine.json").write_text(
                json.dumps({"id": "demo", "version": 1, "kind": "narrative-engine", "card_files": []}),
                encoding="utf-8",
            )
            (root / "applicability.md").write_text("applicability", encoding="utf-8")
            (root / "limits.md").write_text("limits", encoding="utf-8")
            with self.assertRaises(EngineValidationError):
                load_engine(root)

    def test_engine_rejects_malformed_predicates_and_manifest_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "bad"
            (root / "cards").mkdir(parents=True)
            (root / "engine.json").write_text(
                json.dumps({"id": "demo", "version": 1, "card_files": ["cards/cards.json"]}), encoding="utf-8"
            )
            (root / "cards" / "cards.json").write_text(
                json.dumps([{
                    "id": "D-1", "kind": "model", "name": "bad", "when": {"requires": "character"},
                    "hardness": "optional", "prompt": "bad",
                }]),
                encoding="utf-8",
            )
            with self.assertRaises(EngineValidationError):
                load_engine(root)

            (root / "cards" / "cards.json").write_text(
                json.dumps([{"id": "D-1", "kind": "model", "name": "ok", "when": {}, "hardness": "optional", "prompt": "ok"}]),
                encoding="utf-8",
            )
            (root / "manifest.json").write_text(json.dumps({"schema": 2, "engine": "demo", "files": {}}), encoding="utf-8")
            with self.assertRaises(EngineValidationError):
                load_engine(root)


if __name__ == "__main__":
    unittest.main()
