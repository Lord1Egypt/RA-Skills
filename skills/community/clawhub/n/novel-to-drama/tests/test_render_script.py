import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from render_script import render, validate  # noqa: E402


class RenderScriptTests(unittest.TestCase):
    def setUp(self):
        self.sample = json.loads((ROOT / "examples/success-output.json").read_text(encoding="utf-8"))

    def test_renders_all_scenes_and_preserves_the_agent_written_json(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/render_script.py"), "--input", str(ROOT / "examples/success-output.json"), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads((output / "drama-script.json").read_text(encoding="utf-8")), self.sample)
            text = (output / "drama-script.md").read_text(encoding="utf-8")
            for expected in ("E01-S01", "E01-S02", "林舟", "哥？", "广播突然播出他的名字", "待用户确认"):
                self.assertIn(expected, text)

    def test_missing_required_field_and_duplicate_scene_are_rejected(self):
        incomplete = copy.deepcopy(self.sample)
        del incomplete["scenes"][0]["conflict"]["result"]
        with self.assertRaisesRegex(ValueError, "conflict.result"):
            validate(incomplete)
        duplicate = copy.deepcopy(self.sample)
        duplicate["scenes"][1]["scene_id"] = duplicate["scenes"][0]["scene_id"]
        with self.assertRaisesRegex(ValueError, "重复"):
            validate(duplicate)

    def test_ordered_beats_preserve_interleaving_and_reject_mismatch(self):
        data = copy.deepcopy(self.sample)
        scene = data["scenes"][0]
        scene["beats"] = [
            {"type": "action", "text": scene["actions"][0]},
            {"type": "dialogue", **scene["dialogue"][0]},
            {"type": "action", "text": scene["actions"][1]},
        ]
        with tempfile.TemporaryDirectory() as directory:
            render(data, directory)
            text = (Path(directory) / "drama-script.md").read_text(encoding="utf-8")
            self.assertLess(text.index(scene["actions"][0]), text.index("**林舟**：哥？"))
            self.assertLess(text.index("**林舟**：哥？"), text.index(scene["actions"][1]))
        scene["beats"][0]["text"] = "与动作清单不一致"
        with self.assertRaisesRegex(ValueError, "一致"):
            validate(data)

    def test_existing_outputs_are_not_overwritten(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)
            existing = output / "drama-script.md"
            existing.write_text("用户已有剧本", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "已存在"):
                render(self.sample, output)
            self.assertEqual(existing.read_text(encoding="utf-8"), "用户已有剧本")
            self.assertFalse((output / "drama-script.json").exists())

    def test_invalid_input_does_not_create_output(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "bad.json"
            source.write_text('{"scenes":[]}', encoding="utf-8")
            output = Path(directory) / "out"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/render_script.py"), "--input", str(source), "--output", str(output)], capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

    def test_legacy_convert_is_explicitly_a_scaffold(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "out"
            result = subprocess.run([sys.executable, str(ROOT / "scripts/self_test.py"), "convert", "--input", str(ROOT / "examples/success-input.md"), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("不是完整剧本", result.stderr)
            data = json.loads((output / "drama-script.json").read_text(encoding="utf-8"))
            self.assertEqual(data["status"], "scaffold")
            self.assertIn("占位示例", (output / "drama-script.md").read_text(encoding="utf-8"))
            with self.assertRaisesRegex(ValueError, "占位示例"):
                validate(data)


if __name__ == "__main__":
    unittest.main()
