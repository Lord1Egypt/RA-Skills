import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("review_tool", ROOT / "scripts/self_test.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class ReviewValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sample = json.loads((ROOT / "examples/success-output.json").read_text(encoding="utf-8"))

    def test_valid_review_keeps_distinct_evidence_and_pending_status(self):
        data = module.validate_review(self.sample)
        self.assertEqual(data["status"], "needs_review")
        self.assertEqual(len({x["evidence"][0]["text"] for x in data["dimensions"]}), 6)
        self.assertIn("## 待确认", module.render(data))

    def test_quoted_source_can_contain_placeholder_words_without_rejection(self):
        data = json.loads(json.dumps(self.sample))
        data["dimensions"][0]["evidence"][0]["text"] = "他发现这份虚构记录被人改过。"
        self.assertEqual(module.validate_review(data)["status"], "needs_review")

    def test_unscored_dimension_requires_null_average_and_renders_as_unscored(self):
        data = json.loads(json.dumps(self.sample))
        data["dimensions"][0]["score"] = None
        data["dimensions"][0]["status"] = "needs_review"
        data["average"] = None
        module.validate_review(data)
        rendered = module.render(data)
        self.assertIn("六维平均分：未评分（至少一项待确认）", rendered)
        self.assertIn("## 开篇与钩子：未评分（needs_review）", rendered)

    def test_unscored_complete_review_is_rejected(self):
        data = json.loads(json.dumps(self.sample))
        data["dimensions"][0]["score"] = None
        data["average"] = None
        data["status"] = "complete"
        with self.assertRaisesRegex(ValueError, "才能标记 complete"):
            module.validate_review(data)

    def test_malformed_nested_values_raise_value_error(self):
        data = json.loads(json.dumps(self.sample))
        data["dimensions"][0]["evidence"][0]["text"] = 42
        with self.assertRaisesRegex(ValueError, "每条证据"):
            module.validate_review(data)
        data = json.loads(json.dumps(self.sample))
        data["dimensions"][0]["suggestions"] = ["not an object"]
        with self.assertRaisesRegex(ValueError, "修改建议"):
            module.validate_review(data)

    def test_needs_more_source_requires_nonempty_string_message(self):
        for message in (None, 7, {}, "  "):
            with self.subTest(message=message), self.assertRaisesRegex(ValueError, "必须说明缺少"):
                module.validate_review({"status": "needs_more_source", "message": message})

    def test_metadata_and_list_items_must_be_nonempty_strings(self):
        for key, value in (("work", 7), ("scope", None), ("audience", " "), ("version", [])):
            data = json.loads(json.dumps(self.sample)); data[key] = value
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, f"缺少 {key}"):
                module.validate_review(data)
        for key in ("pending_questions", "top_actions"):
            for values in (["ok", None], ["  "], "not a list"):
                data = json.loads(json.dumps(self.sample)); data[key] = values
                with self.subTest(key=key, values=values), self.assertRaisesRegex(ValueError, f"{key} 必须是非空字符串数组"):
                    module.validate_review(data)

    def test_nonfinite_json_numbers_are_rejected(self):
        for token in ("NaN", "Infinity", "-Infinity", "1e999"):
            with self.subTest(token=token), self.assertRaisesRegex(ValueError, "不允许 NaN 或 Infinity"):
                json.loads(
                    '{"average":' + token + '}',
                    parse_constant=module.reject_nonfinite,
                    parse_float=module.parse_finite_float,
                )
        data = json.loads(json.dumps(self.sample)); data["average"] = 10 ** 1000
        with self.assertRaisesRegex(ValueError, "average 必须是有限数值或 null"):
            module.validate_review(data)

    def test_scaffold_cannot_pass_as_review(self):
        with self.assertRaisesRegex(ValueError, "scaffold_not_review"):
            module.validate_review({"status": "scaffold"})

    def test_missing_dimension_evidence_rejected(self):
        data = json.loads(json.dumps(self.sample)); data["dimensions"][2]["evidence"] = []
        with self.assertRaisesRegex(ValueError, "缺少证据"):
            module.validate_review(data)

    def test_complete_rejected_if_any_dimension_needs_review(self):
        data = json.loads(json.dumps(self.sample)); data["status"] = "complete"
        with self.assertRaisesRegex(ValueError, "才能标记 complete"):
            module.validate_review(data)

    def test_does_not_overwrite_existing_results(self):
        with tempfile.TemporaryDirectory() as tmp:
            inp = Path(tmp) / "review.json"; inp.write_text(json.dumps(self.sample), encoding="utf-8")
            out = Path(tmp) / "out"; out.mkdir(); (out / "review.md").write_text("keep", encoding="utf-8")
            old_argv = __import__("sys").argv
            try:
                __import__("sys").argv = ["self_test.py", "render", "--input", str(inp), "--output", str(out)]
                self.assertEqual(module.main(), 1)
            finally:
                __import__("sys").argv = old_argv
            self.assertEqual((out / "review.md").read_text(encoding="utf-8"), "keep")
            self.assertFalse((out / "review.json").exists())

if __name__ == "__main__":
    unittest.main()
