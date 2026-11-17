"""Tests for character pressure accumulation in settlement."""

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
from novelforge_engine.io import sha256_text, read_frontmatter, write_frontmatter_atomic


def _setup_chapter(root, chapter_id, body_text):
    """Run full pipeline up to ENGINE_PASS and return source_hash."""
    (root / "blueprints" / (chapter_id + ".md")).write_text(
        f"---\nid: {chapter_id}\nphase: scene\ndependencies: {{}}\n---\n# Scene\n",
        encoding="utf-8",
    )
    body = root / "chapters" / (chapter_id + ".md")
    body.write_text(body_text, encoding="utf-8")
    digest = sha256_text(body_text)
    transition_chapter(root, chapter_id, "BLUEPRINT_VALID")
    build_context(root, chapter_id)
    transition_chapter(root, chapter_id, "DRAFTED")
    for kind in ("text", "engine"):
        apply_review(root, {"chapter": chapter_id, "kind": kind, "source_hash": digest, "result": "PASS"})
    return digest


class TestSettlementPressure(unittest.TestCase):

    def test_pressure_event_appended_to_log(self):
        """A character fact with pressure_event should append to pressure_log."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            chapter = "v01-c01"
            digest = _setup_chapter(root, chapter, "Chapter one text.")

            # Pre-seed a character entity with empty pressure_log
            write_frontmatter_atomic(
                root / "characters" / "character.hero.md",
                {
                    "id": "character.hero",
                    "type": "character",
                    "name": "Hero",
                    "personality": {
                        "core_temperament": "stubborn",
                        "current_flaw": "distrust",
                        "arc_direction": "distrust→trust",
                        "resistance": 0.8,
                        "pressure_log": [],
                    },
                },
                "# Hero\n",
            )

            settlement = {
                "chapter": chapter,
                "source_hash": digest,
                "facts": [
                    {
                        "id": "character.hero",
                        "type": "character",
                        "name": "Hero",
                        "pressure_event": {
                            "event": "被同伴舍命相救",
                            "weight": 0.3,
                            "toward": "distrust→trust",
                        },
                    }
                ],
            }
            result = apply_settlement(root, settlement)
            self.assertFalse(result["idempotent"])

            projected, _ = read_frontmatter(
                root / "characters" / "character.hero.md"
            )
            self.assertIn("personality", projected)
            log = projected["personality"]["pressure_log"]
            self.assertEqual(len(log), 1)
            self.assertEqual(log[0]["chapter"], chapter)
            self.assertEqual(log[0]["event"], "被同伴舍命相救")
            self.assertAlmostEqual(log[0]["weight"], 0.3)
            self.assertEqual(log[0]["toward"], "distrust→trust")
            # pressure_event should NOT appear in projection
            self.assertNotIn("pressure_event", projected)

    def test_pressure_accumulates_across_chapters(self):
        """Pressure from multiple chapters should accumulate in the log."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)

            # Chapter 1
            ch1 = "v01-c01"
            h1 = _setup_chapter(root, ch1, "Chapter 1.")

            write_frontmatter_atomic(
                root / "characters" / "character.hero.md",
                {
                    "id": "character.hero",
                    "type": "character",
                    "personality": {
                        "core_temperament": "stubborn",
                        "current_flaw": "distrust",
                        "arc_direction": "distrust→trust",
                        "resistance": 0.8,
                        "pressure_log": [],
                    },
                },
                "# Hero\n",
            )

            apply_settlement(root, {
                "chapter": ch1,
                "source_hash": h1,
                "facts": [{
                    "id": "character.hero", "type": "character",
                    "pressure_event": {"event": "event-1", "weight": 0.2, "toward": "distrust→trust"},
                }],
            })

            # Chapter 2
            ch2 = "v01-c02"
            h2 = _setup_chapter(root, ch2, "Chapter 2.")

            apply_settlement(root, {
                "chapter": ch2,
                "source_hash": h2,
                "facts": [{
                    "id": "character.hero", "type": "character",
                    "pressure_event": {"event": "event-2", "weight": 0.15, "toward": "distrust→trust"},
                }],
            })

            projected, _ = read_frontmatter(
                root / "characters" / "character.hero.md"
            )
            log = projected["personality"]["pressure_log"]
            self.assertEqual(len(log), 2)
            self.assertEqual(log[0]["event"], "event-1")
            self.assertEqual(log[1]["event"], "event-2")
            total = sum(e["weight"] for e in log)
            self.assertAlmostEqual(total, 0.35)

    def test_no_pressure_event_leaves_log_absent(self):
        """A character fact without pressure_event should not create pressure_log."""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            init_project(root)
            chapter = "v01-c01"
            digest = _setup_chapter(root, chapter, "Text.")

            settlement = {
                "chapter": chapter,
                "source_hash": digest,
                "facts": [{"id": "character.hero", "type": "character", "name": "Hero"}],
            }
            apply_settlement(root, settlement)

            projected, _ = read_frontmatter(
                root / "characters" / "character.hero.md"
            )
            self.assertNotIn("pressure_event", projected)


if __name__ == "__main__":
    unittest.main()

