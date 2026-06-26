#!/usr/bin/env python3

import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS_DIR))

import file_workflow  # noqa: E402


class TestFileWorkflow(unittest.TestCase):
    def test_default_output_path_uses_tag_and_collision_suffix(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            source = Path(tmpdir) / "incident.txt"
            source.write_text("x", encoding="utf-8")

            first = file_workflow.resolve_output_path(
                input_path=str(source),
                output_path=None,
                in_place=False,
                output_tag="redacted",
            )
            self.assertEqual(first.name, "incident.redacted.txt")

            first.write_text("existing", encoding="utf-8")
            second = file_workflow.resolve_output_path(
                input_path=str(source),
                output_path=None,
                in_place=False,
                output_tag="redacted",
            )
            self.assertEqual(second.name, "incident.redacted.1.txt")

    def test_in_place_requires_file_input(self):
        with self.assertRaises(ValueError):
            file_workflow.resolve_output_path(
                input_path=None,
                output_path=None,
                in_place=True,
                output_tag="redacted",
            )

    def test_embed_extract_and_strip_marker_for_markdown(self):
        content = "Hello [EMAIL_1]"
        mapped = file_workflow.embed_map_marker(content, map_id="abc123", suffix=".md")
        self.assertTrue(mapped.startswith("<!-- privacy-protector-map-id: abc123 -->"))
        self.assertEqual(file_workflow.extract_embedded_map_id(mapped), "abc123")
        self.assertEqual(file_workflow.strip_embedded_map_marker(mapped), content)

    def test_extract_and_strip_legacy_marker_for_markdown(self):
        content = "Hello [EMAIL_1]"
        mapped = "<!-- modeio-redact-map-id: abc123 -->\nHello [EMAIL_1]"
        self.assertEqual(file_workflow.extract_embedded_map_id(mapped), "abc123")
        self.assertEqual(file_workflow.strip_embedded_map_marker(mapped), content)

    def test_embed_extract_and_strip_marker_for_text(self):
        content = "Hello [EMAIL_1]"
        mapped = file_workflow.embed_map_marker(content, map_id="abc123", suffix=".txt")
        self.assertTrue(mapped.startswith("# privacy-protector-map-id: abc123"))
        self.assertEqual(file_workflow.extract_embedded_map_id(mapped), "abc123")
        self.assertEqual(file_workflow.strip_embedded_map_marker(mapped), content)

    def test_extract_and_strip_legacy_marker_for_text(self):
        content = "Hello [EMAIL_1]"
        mapped = "# modeio-redact-map-id: abc123\nHello [EMAIL_1]"
        self.assertEqual(file_workflow.extract_embedded_map_id(mapped), "abc123")
        self.assertEqual(file_workflow.strip_embedded_map_marker(mapped), content)

    def test_embed_marker_uses_sidecar_only_for_json(self):
        content = '{"email":"[EMAIL_1]"}'
        mapped = file_workflow.embed_map_marker(content, map_id="abc123", suffix=".json")
        self.assertEqual(mapped, content)
        self.assertIsNone(file_workflow.extract_embedded_map_id(mapped))

    def test_sidecar_write_and_read_reference(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            content_path = Path(tmpdir) / "incident.redacted.txt"
            content_path.write_text("x", encoding="utf-8")

            sidecar_path = file_workflow.write_sidecar_map(
                content_path,
                {
                    "mapId": "abc123",
                    "mapPath": "/tmp/abc123.json",
                    "entryCount": 1,
                },
            )
            self.assertEqual(sidecar_path.name, "incident.redacted.map.json")

            ref, returned_path = file_workflow.read_sidecar_map_reference(content_path)
            self.assertEqual(ref, "/tmp/abc123.json")
            self.assertEqual(returned_path, sidecar_path)


if __name__ == "__main__":
    unittest.main()
