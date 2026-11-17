from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReusablePolicyTests(unittest.TestCase):
    def test_default_watermark_is_opt_in_and_not_user_specific(self):
        preset = json.loads((ROOT / "presets" / "travel-food-journal.json").read_text(encoding="utf-8"))
        watermark = preset["modules"]["watermark"]
        self.assertFalse(watermark["enabled"])
        self.assertEqual(watermark["text"], "")
        self.assertTrue(watermark["project_override_required_to_enable"])
        self.assertEqual(set(watermark), {"enabled", "text", "position", "project_override_required_to_enable"})
        workflow = preset["workflow_defaults"]
        self.assertFalse(workflow["renderer"]["backend_configured_by_default"])
        self.assertTrue(workflow["renderer"]["validated_receipt_required_for_rendered_output"])
        self.assertTrue(workflow["renderer"]["external_reference_processing_requires_explicit_consent"])
        self.assertTrue(workflow["composition"]["strip_exif_gps_xmp"])

    def test_private_reference_storage_and_external_processing_are_separate(self):
        policy = (ROOT / "references" / "style-packs.md").read_text(encoding="utf-8").lower()
        self.assertIn("local storage consent", policy)
        self.assertIn("external processing consent", policy)
        self.assertIn("never infer", policy)

    def test_frontmatter_is_versioned_and_has_explicit_trigger_language(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = skill.split("---", 2)[1]
        self.assertIn('version: "1.5.0"', frontmatter)
        self.assertIn("Use when", frontmatter)
        self.assertIn("照片转手绘轮播", frontmatter)


if __name__ == "__main__":
    unittest.main()
