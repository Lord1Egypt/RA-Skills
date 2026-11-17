#!/usr/bin/env python3
"""Unit tests for scripts/query.py.

Run from the skill directory:
    python3 -m unittest discover -s tests -v
or:
    python3 tests/test_query.py
"""

import importlib.util
import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(HERE)
SCRIPTS_DIR = os.path.join(SKILL_DIR, "scripts")
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "query.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("query", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


q = _load_module()


class LoadDataTests(unittest.TestCase):
    def test_dataset_has_records_and_genders(self):
        data = q.load_data()
        self.assertGreater(len(data["records"]), 0)
        self.assertEqual(set(data["genders"]), {"男", "女"})
        self.assertIn("广东", data["provinces"])
        for record in data["records"]:
            self.assertIsInstance(record["count"], int)
            self.assertGreaterEqual(record["count"], 0)

    def test_missing_file_raises(self):
        with self.assertRaises(OSError):
            q.load_data(os.path.join(HERE, "does-not-exist.json"))


class QueryTests(unittest.TestCase):
    def test_total_for_known_name(self):
        result = q.query("张伟")
        self.assertTrue(result["found"])
        self.assertTrue(result["matched"])
        self.assertEqual(result["total"], 6901)
        self.assertEqual(result["message"], "")

    def test_by_province_breakdown_sums_to_total(self):
        result = q.query("张伟")
        self.assertEqual(sum(result["by_province"].values()), result["total"])
        self.assertEqual(result["by_province"]["北京"], 1345)

    def test_gender_filter_is_applied(self):
        male = q.query("刘洋", gender="男")
        female = q.query("刘洋", gender="女")
        self.assertEqual(male["total"], 2210)
        self.assertEqual(female["total"], 2108)
        self.assertEqual(male["by_gender"], {"男": 2210})
        self.assertEqual(female["by_gender"], {"女": 2108})

    def test_province_filter_is_applied(self):
        result = q.query("张伟", province="广东")
        self.assertEqual(result["total"], 1688)
        self.assertEqual(result["by_province"], {"广东": 1688})

    def test_combined_filter(self):
        result = q.query("李娜", gender="女", province="四川")
        self.assertEqual(result["total"], 540)

    def test_absent_name_reports_no_result(self):
        result = q.query("不存在的名字")
        self.assertFalse(result["found"])
        self.assertFalse(result["matched"])
        self.assertEqual(result["total"], 0)
        self.assertTrue(result["message"])
        self.assertIn("不存在的名字", result["message"])

    def test_filter_excludes_all_reports_no_result(self):
        # 张伟 exists (男 only) -> a 女 filter must yield an explicit no-result.
        result = q.query("张伟", gender="女")
        self.assertTrue(result["found"])
        self.assertFalse(result["matched"])
        self.assertEqual(result["total"], 0)
        self.assertTrue(result["message"])
        self.assertIn("张伟", result["message"])
        self.assertEqual(result["available_genders"], ["男"])

    def test_gender_alias_and_case(self):
        result = q.query("刘洋", gender="Female")
        self.assertEqual(result["filters"]["gender"], "女")
        self.assertEqual(result["total"], 2108)

    def test_province_alias(self):
        result = q.query("李娜", province="广东省")
        self.assertEqual(result["filters"]["province"], "广东")
        self.assertEqual(result["total"], 1240)

    def test_unknown_gender_rejected(self):
        with self.assertRaises(ValueError):
            q.query("张伟", gender="不明")

    def test_unknown_province_rejected(self):
        with self.assertRaises(ValueError):
            q.query("张伟", province="未知省")

    def test_empty_name_rejected(self):
        with self.assertRaises(ValueError):
            q.query("   ")


class RenderTests(unittest.TestCase):
    def test_markdown_contains_totals_and_breakdown(self):
        result = q.query("张伟", province="广东")
        md = q.render_markdown(result)
        self.assertIn("# 同名人数查询", md)
        self.assertIn("张伟", md)
        self.assertIn("1,688", md)
        self.assertIn("按省份", md)

    def test_markdown_no_match_shows_message(self):
        md = q.render_markdown(q.query("不存在的名字"))
        self.assertIn("未找到匹配记录", md)
        self.assertIn("不存在的名字", md)

    def test_text_render(self):
        text = q.render_text(q.query("刘洋"))
        self.assertIn("Same-Name Count", text)
        self.assertIn("Total: 4,318", text)

    def test_json_render_round_trips(self):
        parsed = json.loads(q.render(q.query("张伟", gender="男"), "json"))
        self.assertEqual(parsed["total"], 6901)
        self.assertTrue(parsed["matched"])

    def test_json_no_match_carries_message(self):
        parsed = json.loads(q.render(q.query("不存在的名字"), "json"))
        self.assertFalse(parsed["matched"])
        self.assertTrue(parsed["message"])


class CliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT_PATH, *args],
            capture_output=True,
            text=True,
            cwd=SKILL_DIR,
        )

    def test_cli_default_markdown(self):
        result = self._run("--name", "张伟")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("同名人数查询", result.stdout)
        self.assertIn("6,901", result.stdout)

    def test_cli_json_is_parseable(self):
        result = self._run("--name", "张伟", "--gender", "男", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["total"], 6901)

    def test_cli_no_match_exits_zero_with_message(self):
        result = self._run("--name", "不存在的名字")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("未找到匹配记录", result.stdout)

    def test_cli_filter_excludes_all_message(self):
        result = self._run("--name", "张伟", "--gender", "女")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("未找到", result.stdout)

    def test_cli_unknown_gender_fails(self):
        result = self._run("--name", "张伟", "--gender", "不明")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown gender", result.stderr)

    def test_cli_missing_name_fails(self):
        result = self._run("--format", "json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--name is required", result.stderr)

    def test_cli_list_provinces(self):
        result = self._run("--list-provinces")
        self.assertEqual(result.returncode, 0)
        self.assertIn("广东", result.stdout)

    def test_cli_list_genders(self):
        result = self._run("--list-genders")
        self.assertEqual(result.returncode, 0)
        self.assertIn("男", result.stdout)

    def test_cli_help(self):
        result = self._run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--name", result.stdout)
        self.assertIn("--province", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)