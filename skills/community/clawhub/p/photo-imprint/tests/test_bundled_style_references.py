from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"
STYLE_CASES = {
    "blue-lavender-watercolor": {
        "reference_id": "watercolor-no-73-blue-and-lavender",
        "title": "Watercolor no. 73, Blue and Lavender",
        "object_number": "1966.34.7",
        "medium": "watercolor",
        "date": "1928",
        "item_record_url": "https://americanart.si.edu/artwork/watercolor-no-73-blue-and-lavender-24276",
        "official_image_url": "https://ids.si.edu/ids/download?id=SAAM-1966.34.7_1.tif",
        "sha256": "2eaaba5baf916b35f198a9be907fdf9126dab8a89725111148d8005f051c1b10",
        "size": (1600, 1107),
        "bytes": 242272,
        "required_roles": {"transparent watercolor wash and material handling", "cool blue and lavender value grouping"},
        "required_exclusions": {"seascape", "shoreline", "water horizon"},
    },
    "highway-485-lithograph": {
        "reference_id": "highway-485",
        "title": "Highway 485",
        "object_number": "1966.34.9",
        "medium": "lithograph",
        "date": "n.d.",
        "item_record_url": "https://americanart.si.edu/artwork/highway-485-24266",
        "official_image_url": "https://ids.si.edu/ids/download?id=SAAM-1966.34.9_1.tif",
        "sha256": "8ac8a779fa4d1501fb9cb6e399bf2c520304ff6ac2a7b3e01d5f41c62a487439",
        "size": (1600, 1113),
        "bytes": 83298,
        "required_roles": {"sparse broken dry-crayon and contour-line construction", "radical subject simplification"},
        "required_exclusions": {"road", "road sign", "utility poles", "wires"},
    },
}
RIGHTS = (
    "This media is in the public domain (free of copyright restrictions). "
    "You can copy, modify, and distribute this work without contacting the Smithsonian."
)


class BundledStyleReferenceTests(unittest.TestCase):
    def test_bundled_derivatives_and_provenance_are_exact(self):
        for style_id, expected in STYLE_CASES.items():
            with self.subTest(style=style_id):
                directory = ROOT / "assets" / "style-packs" / style_id
                image_path = directory / "reference.webp"
                source = json.loads((directory / "source.json").read_text(encoding="utf-8"))
                profile = json.loads((ROOT / "profiles" / "styles" / f"{style_id}.json").read_text(encoding="utf-8"))
                reference = profile["references"][0]

                self.assertEqual(profile["id"], style_id)
                self.assertEqual(profile["reference_status"], "approved-bundled")
                self.assertEqual(reference["id"], expected["reference_id"])
                self.assertEqual(source["title"], expected["title"])
                self.assertEqual(source["creator"], "Allen Tucker")
                self.assertEqual(source["institution"], "Smithsonian American Art Museum")
                self.assertEqual(source["object_number"], expected["object_number"])
                self.assertEqual(source["medium"], expected["medium"])
                self.assertEqual(source["date"], expected["date"])
                self.assertEqual(source["item_record_url"], expected["item_record_url"])
                self.assertEqual(source["official_image_url"], expected["official_image_url"])
                self.assertEqual(source["rights_status"], "FREE TO USE")
                self.assertEqual(source["rights_statement"], RIGHTS)
                self.assertEqual(source["retrieval_date"], "2026-08-27")
                self.assertTrue(source["redistributable"])
                self.assertTrue(source["bundled"])
                self.assertEqual(source["technique_roles"], reference["technique_roles"])
                self.assertEqual(source["subject_exclusions"], reference["subject_exclusions"])
                self.assertTrue(expected["required_roles"].issubset(set(reference["technique_roles"])))
                self.assertTrue(expected["required_exclusions"].issubset(set(reference["subject_exclusions"])))

                raw = image_path.read_bytes()
                self.assertEqual(len(raw), expected["bytes"])
                self.assertEqual(hashlib.sha256(raw).hexdigest(), expected["sha256"])
                self.assertLessEqual(len(raw), 750 * 1024)
                self.assertTrue(raw.startswith(b"RIFF"))
                self.assertEqual(raw[8:12], b"WEBP")
                with Image.open(image_path) as image:
                    image.load()
                    self.assertEqual(image.format, "WEBP")
                    self.assertEqual(image.size, expected["size"])
                    self.assertLessEqual(max(image.size), 1600)
                    self.assertFalse(image.getexif())
                    self.assertFalse(any("xmp" in str(key).lower() for key in image.info))
                derivative = source["derivative"]
                self.assertEqual(derivative["sha256"], expected["sha256"])
                self.assertEqual((derivative["width"], derivative["height"]), expected["size"])
                self.assertEqual(derivative["bytes"], expected["bytes"])
                self.assertTrue({"EXIF", "GPS", "XMP"}.issubset(set(derivative["metadata_stripped"])))

    def test_each_new_style_resolves_independently_without_changing_default(self):
        default = json.loads((ROOT / "presets" / "travel-food-journal.json").read_text(encoding="utf-8"))
        self.assertEqual(default["profiles"]["style"], "watercolor-journal")
        for style_id in STYLE_CASES:
            with self.subTest(style=style_id), tempfile.TemporaryDirectory() as temp:
                preset = json.loads(json.dumps(default))
                preset["profiles"]["style"] = style_id
                preset_path = Path(temp) / f"{style_id}.json"
                output_path = Path(temp) / "resolved.json"
                preset_path.write_text(json.dumps(preset), encoding="utf-8")
                result = subprocess.run(
                    [sys.executable, str(BIN / "resolve_config.py"), "--preset", str(preset_path), "--output", str(output_path)],
                    cwd=ROOT, text=True, capture_output=True,
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                resolved = json.loads(output_path.read_text(encoding="utf-8"))
                self.assertEqual(resolved["profiles"]["style"]["id"], style_id)
                self.assertEqual(len(resolved["profiles"]["style"]["references"]), 1)

    def test_subject_exclusions_propagate_to_plan_and_prompt(self):
        with tempfile.TemporaryDirectory() as temp:
            work = Path(temp)
            preset = json.loads((ROOT / "presets" / "travel-food-journal.json").read_text(encoding="utf-8"))
            preset["profiles"]["style"] = "highway-485-lithograph"
            preset_path = work / "preset.json"
            config_path = work / "resolved.json"
            preset_path.write_text(json.dumps(preset), encoding="utf-8")
            resolved = subprocess.run(
                [sys.executable, str(BIN / "resolve_config.py"), "--preset", str(preset_path), "--output", str(config_path)],
                cwd=ROOT, text=True, capture_output=True,
            )
            self.assertEqual(resolved.returncode, 0, resolved.stdout + resolved.stderr)
            source_path = work / "source.jpg"
            Image.new("RGB", (16, 16), "white").save(source_path)
            manifest = {
                "preset": "travel-food-journal",
                "items": [{
                    "page": 1,
                    "source_path": str(source_path),
                    "sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
                    "capture_time": "2026-08-27T12:00:00",
                    "location": "confirmed place",
                    "subject": "confirmed subject",
                    "date_label": "2026-08-27",
                    "caption_status": {"location": "confirmed", "subject": "confirmed", "date": "confirmed"},
                    "production_brief": {
                        "subject_priority": "source subject",
                        "thumbnail_read": "source subject",
                        "preserve_anchors": ["source anchor"],
                        "abstract_or_omit": ["incidental detail"],
                        "material_depth_cues": ["source depth"],
                        "structural_lines": [{"element": "source line", "operation": "retain"}],
                        "forbidden_inventions": ["invented object"],
                    },
                }],
            }
            manifest_path = work / "manifest.json"
            plan_path = work / "plan.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            planned = subprocess.run(
                [sys.executable, str(BIN / "build_render_plan.py"), "--config", str(config_path), "--manifest", str(manifest_path), "--output", str(plan_path)],
                cwd=ROOT, text=True, capture_output=True,
            )
            self.assertEqual(planned.returncode, 0, planned.stdout + planned.stderr)
            plan = json.loads(plan_path.read_text(encoding="utf-8"))
            exclusions = plan["style_reference_locks"][0]["subject_exclusions"]
            self.assertTrue({"road", "road sign", "utility poles", "wires"}.issubset(set(exclusions)))
            negative_prompt = plan["pages"][0]["negative_prompt"]
            for value in ("road", "road sign", "utility poles", "wires"):
                self.assertIn(value, negative_prompt)

    def test_full_validator_counts_both_bundled_references(self):
        result = subprocess.run(
            [sys.executable, str(BIN / "validate_skill.py"), "--json"],
            cwd=ROOT, text=True, capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        report = json.loads(result.stdout)
        self.assertTrue(report["ok"])
        self.assertGreaterEqual(report["counts"]["style_references"], 2)
        self.assertEqual(report["errors"], [])


if __name__ == "__main__":
    unittest.main()
