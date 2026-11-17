from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

from project_state import command_compose, command_init, command_record  # noqa: E402


class Args:
    def __init__(self, **values):
        self.__dict__.update(values)


class ProjectStateTests(unittest.TestCase):
    def test_init_creates_expected_layout(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            result = command_init(Args(root=temp_dir, name="story", force=False))
            project = Path(result["project_dir"])
            self.assertTrue((project / "project.json").is_file())
            self.assertTrue((project / "chapters").is_dir())
            self.assertTrue((project / "images").is_dir())
            self.assertTrue((project / "metadata/generations").is_dir())

    def test_compose_includes_context_and_preserves_task(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            init = command_init(Args(root=temp_dir, name="story", force=False))
            project = Path(init["project_dir"])
            (project / "canon.md").write_text("The city floats above the sea.", encoding="utf-8")
            (project / "memory.md").write_text("The lantern is broken.", encoding="utf-8")
            result = command_compose(
                Args(
                    project_dir=str(project),
                    task="Continue from the last scene.",
                    context_file=[],
                    author_note="Keep the pace tense.",
                    max_chars=2000,
                )
            )
            self.assertIn("The city floats above the sea.", result["prompt"])
            self.assertIn("The lantern is broken.", result["prompt"])
            self.assertIn("Continue from the last scene.", result["prompt"])
            self.assertEqual(result["truncated"], False)

    def test_compose_is_bounded(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            init = command_init(Args(root=temp_dir, name="story", force=False))
            project = Path(init["project_dir"])
            (project / "canon.md").write_text("x" * 2000, encoding="utf-8")
            task = "Keep this task."
            result = command_compose(
                Args(
                    project_dir=str(project),
                    task=task,
                    context_file=[],
                    author_note="",
                    max_chars=128,
                )
            )
            self.assertLessEqual(result["characters"], 128)
            self.assertIn(task, result["prompt"])
            self.assertTrue(result["truncated"])

    def test_record_redacts_sensitive_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            init = command_init(Args(root=temp_dir, name="story", force=False))
            project = Path(init["project_dir"])
            metadata_file = project / "metadata-input.json"
            metadata_file.write_text(
                json.dumps({"width": 832, "api_key": "do-not-store"}),
                encoding="utf-8",
            )
            result = command_record(
                Args(
                    project_dir=str(project),
                    kind="image",
                    model="nai-diffusion-5-full",
                    seed=42,
                    prompt="a moonlit harbor",
                    negative_prompt="blurry",
                    asset=str(project / "images" / "scene.png"),
                    metadata_file=str(metadata_file),
                )
            )
            record_path = Path(result["record_file"])
            stored = json.loads(record_path.read_text(encoding="utf-8"))
            self.assertEqual(stored["parameters"]["api_key"], "[REDACTED]")
            self.assertEqual(stored["asset"]["path"], "images/scene.png")
            self.assertNotIn("do-not-store", record_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
