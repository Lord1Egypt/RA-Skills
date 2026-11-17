import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("storyboard_tool", ROOT / "scripts/self_test.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class StoryboardValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = json.loads((ROOT / "examples/success-output.json").read_text(encoding="utf-8"))

    def test_ai_authored_storyboard_validates_and_renders(self):
        data = module.validate_storyboard(self.sample)
        rendered = module.render_markdown(data)
        self.assertIn("原文未说明", rendered)
        self.assertIn("S01-03", rendered)
        self.assertIn("结构校验不证明原文引用", rendered)

    def test_render_includes_all_shot_fields_and_handles_table_characters(self):
        data = json.loads(json.dumps(self.sample))
        shot = data["scenes"][0]["shots"][0]
        shot.update({
            "visual": "画面左侧 | 长椅\n镜头继续",
            "action": "林舟抬头 | 收起信封",
            "sound": "雨声 | 列车声",
            "source_anchor": "原文第1句 | 林舟在车站等车",
            "creative_note": "镜头补充 | 不作为原文事实",
        })
        rendered = module.render_markdown(data)
        for value in ("画面左侧 | 长椅<br>\n  镜头继续", "林舟抬头 | 收起信封", "雨声 | 列车声", "原文第1句 | 林舟在车站等车", "镜头补充 | 不作为原文事实"):
            self.assertIn(value, rendered)
        self.assertNotIn("|---", rendered)

    def test_duplicate_scene_ids_are_rejected(self):
        data = json.loads(json.dumps(self.sample))
        duplicate = json.loads(json.dumps(data["scenes"][0]))
        data["scenes"].append(duplicate)
        data["duration_seconds"] *= 2
        with self.assertRaisesRegex(ValueError, "重复 scene_id"):
            module.validate_storyboard(data)

    def test_duplicate_shot_ids_are_rejected_across_scenes(self):
        data = json.loads(json.dumps(self.sample))
        data["scenes"][0]["shots"][1]["shot_id"] = data["scenes"][0]["shots"][0]["shot_id"]
        with self.assertRaisesRegex(ValueError, "重复 shot_id"):
            module.validate_storyboard(data)

    def test_tool_does_not_expose_source_to_storyboard_conversion(self):
        self.assertFalse(hasattr(module, "convert"))
        self.assertFalse(hasattr(module, "_hero"))

    def test_missing_source_is_a_structured_non_scored_result(self):
        payload = json.loads((ROOT / "examples/failure-output.json").read_text(encoding="utf-8"))
        self.assertEqual(module.validate_storyboard(payload)["status"], "needs_more_source")
        self.assertIn("目前只有标题", module.render_markdown(payload))
        for message in (None, 4, " "):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, "message 必须"):
                module.validate_storyboard({"status": "needs_more_source", "message": message})

    def test_missing_required_shot_fields_fail_cleanly(self):
        data = json.loads(json.dumps(self.sample)); del data["scenes"][0]["shots"][0]["action"]
        with self.assertRaisesRegex(ValueError, r"shots\[0\]\.action"):
            module.validate_storyboard(data)

    def test_duration_must_match_shot_durations(self):
        data = json.loads(json.dumps(self.sample)); data["duration_seconds"] = 20
        with self.assertRaisesRegex(ValueError, "所有镜头时长之和"):
            module.validate_storyboard(data)

    def test_complete_is_rejected_when_gaps_remain(self):
        data = json.loads(json.dumps(self.sample)); data["status"] = "complete"
        with self.assertRaisesRegex(ValueError, "存在未解决 gaps"):
            module.validate_storyboard(data)
        data["gaps"] = []
        with self.assertRaisesRegex(ValueError, "存在未解决 gaps"):
            module.validate_storyboard(data)

    def test_nonfinite_json_numbers_are_rejected(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, "不允许 NaN 或 Infinity"):
                json.loads('{"duration_seconds":' + token + '}', parse_constant=module.reject_nonfinite, parse_float=module.parse_finite_float)

    def test_existing_file_is_not_overwritten_or_left_partial(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp); (out / "storyboard.md").write_text("keep", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "output_exists"):
                module.write_outputs(self.sample, out)
            self.assertEqual((out / "storyboard.md").read_text(encoding="utf-8"), "keep")
            self.assertFalse((out / "storyboard.json").exists())

    def test_successful_write_produces_matching_files(self):
        with tempfile.TemporaryDirectory() as temp:
            out = Path(temp) / "new"
            module.write_outputs(self.sample, out)
            self.assertEqual(json.loads((out / "storyboard.json").read_text(encoding="utf-8")), self.sample)
            self.assertEqual((out / "storyboard.md").read_text(encoding="utf-8"), module.render_markdown(self.sample))

if __name__ == "__main__":
    unittest.main()
