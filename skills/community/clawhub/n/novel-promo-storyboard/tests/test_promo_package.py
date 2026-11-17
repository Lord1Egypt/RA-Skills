import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("promo_tool", ROOT / "scripts/self_test.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class PromoPackageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = json.loads((ROOT / "examples/success-output.json").read_text(encoding="utf-8"))

    def test_authored_package_renders_user_intent_and_timed_audio_visuals(self):
        data = module.validate_package(self.sample)
        rendered = module.render_markdown(data)
        self.assertIn("平台：未提供", rendered)
        self.assertIn("P01｜0–3 秒", rendered)
        self.assertIn("VO01｜0–3 秒", rendered)
        self.assertIn("原文锚点：苏棠把伞留在咖啡馆，雨停后才发现伞柄里藏着一张旧车票。", rendered)
        self.assertIn("CTA 偏好：未提供", rendered)
        self.assertIn("结尾行动引导", rendered)
        self.assertIn("未添加", rendered)

    def test_no_mechanical_build_or_fixed_cta_generator_remains(self):
        self.assertFalse(hasattr(module, "build"))
        self.assertFalse(hasattr(module, "_source_parts"))
        self.assertFalse(hasattr(module, "_find_hero"))
        rendered = module.render_markdown(self.sample)
        self.assertNotIn("想看后续发展，先收藏这条", rendered)

    def test_source_text_is_not_accepted_as_generated_package(self):
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / "out"
            command = ["python3", "-B", str(ROOT / "scripts/self_test.py"), "render", "--input", str(ROOT / "examples/success-input.md"), "--output", str(output)]
            result = __import__("subprocess").run(command, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse(output.exists())

    def test_missing_source_is_structured_and_requires_message(self):
        failure = json.loads((ROOT / "examples/failure-output.json").read_text(encoding="utf-8"))
        self.assertEqual(module.validate_package(failure)["status"], "needs_more_source")
        self.assertIn("当前只有标题", module.render_markdown(failure))
        for value in (None, 3, " "):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "message 必须"):
                module.validate_package({"status": "needs_more_source", "message": value})

    def test_malformed_enum_types_return_value_error(self):
        with self.assertRaisesRegex(ValueError, "status 必须"):
            module.validate_package({"status": []})
        data = json.loads(json.dumps(self.sample)); data["voiceover"][0]["origin"] = []
        with self.assertRaisesRegex(ValueError, "origin 必须"):
            module.validate_package(data)
        data = json.loads(json.dumps(self.sample)); data["ending_action"]["status"] = {}
        with self.assertRaisesRegex(ValueError, "ending_action.status"):
            module.validate_package(data)

    def test_invalid_shot_reference_and_time_are_rejected(self):
        data = json.loads(json.dumps(self.sample)); data["shots"][0]["voiceover_ref"] = "missing"
        with self.assertRaisesRegex(ValueError, "voiceover_ref"):
            module.validate_package(data)
        data = json.loads(json.dumps(self.sample)); data["shots"][0]["end"] = 2
        with self.assertRaisesRegex(ValueError, "duration_seconds 必须等于 end-start"):
            module.validate_package(data)
        data = json.loads(json.dumps(self.sample)); data["shots"][0]["start"] = 20; data["shots"][0]["end"] = 23
        with self.assertRaisesRegex(ValueError, "不能重叠或倒序"):
            module.validate_package(data)

    def test_promo_package_requires_at_least_one_shot(self):
        data = json.loads(json.dumps(self.sample))
        data["shots"] = []
        with self.assertRaisesRegex(ValueError, "至少需要一个镜头"):
            module.validate_package(data)

    def test_voiceover_can_be_empty_when_all_shots_are_visual_only(self):
        data = json.loads(json.dumps(self.sample))
        data["voiceover"] = []
        for shot in data["shots"]:
            shot["voiceover_ref"] = None
        self.assertEqual(module.validate_package(data)["voiceover"], [])

    def test_dialogue_markdown_keeps_anchor_and_creative_note(self):
        data = json.loads(json.dumps(self.sample))
        data["scenes"][0]["dialogue"] = [{
            "speaker": "苏棠", "line": "这张票是哪天的？",
            "source_anchor": "苏棠抬头问。", "creative_note": "新增对白，用于串联查看日期的动作。"
        }]
        rendered = module.render_markdown(data)
        self.assertIn("原文锚点：苏棠抬头问。", rendered)
        self.assertIn("创作补充：新增对白，用于串联查看日期的动作。", rendered)

    def test_duplicate_timeline_ids_and_overlapping_entries_are_rejected(self):
        data = json.loads(json.dumps(self.sample)); data["shots"][1]["shot_id"] = data["shots"][0]["shot_id"]
        with self.assertRaisesRegex(ValueError, "重复 shot_id"):
            module.validate_package(data)
        data = json.loads(json.dumps(self.sample)); data["voiceover"][1]["start"] = 2
        with self.assertRaisesRegex(ValueError, "不能重叠"):
            module.validate_package(data)

    def test_cta_must_record_whether_user_requested_or_agent_suggested(self):
        data = json.loads(json.dumps(self.sample))
        data["user_intent"]["cta_preference"] = "引导关注后续"
        data["voiceover"].append({"segment_id":"VO04","start":12,"end":14,"text":"关注后续","source_anchor":"","origin":"cta_requested","creative_note":"用户要求"})
        data["shots"].append({"shot_id":"P04","start":12,"end":14,"duration_seconds":2,"visual":"结束卡显示关注后续","caption":"关注后续","voiceover_ref":"VO04","sound":"收尾音","source_anchor":"","creative_note":"依据用户 CTA 要求添加结束卡"})
        data["duration_seconds"] = 14
        data["ending_action"] = {"status": "user_requested", "text": "关注后续", "note": "用户明确要求"}
        module.validate_package(data)
        data["ending_action"]["status"] = "none"
        with self.assertRaisesRegex(ValueError, "为 none 时 text 必须为空"):
            module.validate_package(data)

    def test_complete_cannot_hide_source_gaps(self):
        data = json.loads(json.dumps(self.sample)); data["status"] = "complete"
        with self.assertRaisesRegex(ValueError, "待确认 gaps"):
            module.validate_package(data)

    def test_nonfinite_json_numbers_are_rejected(self):
        for value in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(value=value), self.assertRaisesRegex(ValueError, "不允许 NaN 或 Infinity"):
                json.loads('{"duration_seconds":' + value + '}', parse_constant=module.reject_nonfinite, parse_float=module.parse_finite_float)

    def test_existing_output_is_not_overwritten_or_left_partial(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp); (out/"promo-package.md").write_text("preserve",encoding="utf-8")
            with self.assertRaisesRegex(ValueError,"output_exists"):
                module.write_outputs(self.sample,out)
            self.assertEqual((out/"promo-package.md").read_text(encoding="utf-8"),"preserve")
            self.assertFalse((out/"promo-package.json").exists())

    def test_rendered_files_match_structured_input(self):
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/"new"; module.write_outputs(self.sample,out)
            self.assertEqual(json.loads((out/"promo-package.json").read_text(encoding="utf-8")),self.sample)
            self.assertEqual((out/"promo-package.md").read_text(encoding="utf-8"),module.render_markdown(self.sample))

if __name__ == "__main__":
    unittest.main()
