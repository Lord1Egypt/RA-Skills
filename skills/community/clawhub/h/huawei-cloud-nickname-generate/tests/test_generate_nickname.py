#!/usr/bin/env python3
"""Unit tests for scripts/generate_nickname.py.

Run from the skill directory:
    python3 -m unittest discover -s tests -v
or:
    python3 tests/test_generate_nickname.py
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
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "generate_nickname.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_nickname", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


gn = _load_module()

SLOTS = ("prefix", "modifier", "core", "suffix")


class LoadDataTests(unittest.TestCase):
    def test_core_pools_present(self):
        data = gn.load_data()
        for slot in ("prefix", "modifier", "core", "suffix"):
            self.assertIn(slot, data["parts"])
            self.assertGreater(len(data["parts"][slot]), 0)

    def test_style_coverage_per_slot(self):
        data = gn.load_data()
        for style in data["styles"]:
            for slot in SLOTS:
                self.assertTrue(
                    any(style in it["styles"] for it in data["parts"][slot]),
                    "no %s part for style %s" % (slot, style),
                )

    def test_length_buckets_and_ranges(self):
        data = gn.load_data()
        for key in ("short", "medium", "long"):
            spec = data["lengths"][key]
            self.assertIn("patterns", spec)
            self.assertLessEqual(spec["min"], spec["max"])
            for pattern in spec["patterns"]:
                self.assertTrue(pattern)
                for slot in pattern:
                    self.assertIn(slot, data["parts"])

    def test_missing_file_raises(self):
        with self.assertRaises(OSError):
            gn.load_data(os.path.join(HERE, "does-not-exist.json"))


class NormalizeTests(unittest.TestCase):
    def test_style_alias_and_case(self):
        styles = gn.load_data()["styles"]
        self.assertEqual(gn.normalize_style("neutral", styles), "中性")
        self.assertEqual(gn.normalize_style("CUTE", styles), "可爱")
        self.assertEqual(gn.normalize_style("简约", styles), "简约")

    def test_unknown_style_rejected(self):
        with self.assertRaises(ValueError):
            gn.normalize_style("不存在的风格", gn.load_data()["styles"])

    def test_length_alias(self):
        lengths = list(gn.load_data()["lengths"].keys())
        self.assertEqual(gn.normalize_length("短", lengths), "short")
        self.assertEqual(gn.normalize_length("LONG", lengths), "long")

    def test_unknown_length_rejected(self):
        with self.assertRaises(ValueError):
            gn.normalize_length("超长", list(gn.load_data()["lengths"].keys()))


class GenerateTests(unittest.TestCase):
    def test_default_shape(self):
        result = gn.generate_nicknames(seed=1234)
        self.assertEqual(result["requested_count"], 1)
        self.assertEqual(result["generated_count"], 1)
        self.assertEqual(len(result["nicknames"]), 1)
        self.assertTrue(result["nicknames"][0]["name"])
        self.assertIn(result["style"], gn.load_data()["styles"])

    def test_default_count_is_one(self):
        self.assertEqual(gn.DEFAULT_COUNT, 1)

    def test_same_seed_is_reproducible(self):
        first = gn.generate_nicknames(count=5, seed=20240501)
        second = gn.generate_nicknames(count=5, seed=20240501)
        self.assertEqual(first["nicknames"], second["nicknames"])
        self.assertEqual(gn.render_markdown(first), gn.render_markdown(second))

    def test_different_seeds_differ(self):
        first = gn.generate_nicknames(count=5, seed=1)
        second = gn.generate_nicknames(count=5, seed=2)
        self.assertNotEqual(
            [n["name"] for n in first["nicknames"]],
            [n["name"] for n in second["nicknames"]],
        )

    def test_no_seed_generates_concrete_seed(self):
        result = gn.generate_nicknames()
        self.assertIsInstance(result["seed"], int)
        self.assertFalse(result["explicit_seed"])

    def test_count_returns_distinct_names(self):
        result = gn.generate_nicknames(count=15, seed=99)
        names = [n["name"] for n in result["nicknames"]]
        self.assertEqual(len(names), 15)
        self.assertEqual(len(set(names)), 15)
        self.assertFalse(result["shortfall"])

    def test_count_above_max_rejected(self):
        with self.assertRaises(ValueError):
            gn.generate_nicknames(count=gn.MAX_COUNT + 1, seed=1)

    def test_count_below_one_rejected(self):
        with self.assertRaises(ValueError):
            gn.generate_nicknames(count=0, seed=1)

    def test_style_filter_is_applied(self):
        data = gn.load_data()
        result = gn.generate_nicknames(count=8, seed=7, style="文艺", data=data)
        self.assertEqual(result["style"], "文艺")
        self.assertEqual(result["fallbacks"], [])
        for item in result["nicknames"]:
            self.assertTrue(item["strict"])
            self.assertEqual(item["relaxed_slots"], [])
            for part in item["parts"]:
                self.assertIn("文艺", part["styles"])

    def test_style_filter_cute_medium(self):
        result = gn.generate_nicknames(count=8, seed=11, style="可爱", length="medium")
        self.assertEqual(result["style"], "可爱")
        self.assertEqual(result["length"], "medium")
        self.assertEqual(result["fallbacks"], [])
        for item in result["nicknames"]:
            self.assertTrue(4 <= item["chars"] <= 6)
            for part in item["parts"]:
                self.assertIn("可爱", part["styles"])

    def test_length_filter_is_applied(self):
        data = gn.load_data()
        for key in ("short", "medium", "long"):
            spec = data["lengths"][key]
            result = gn.generate_nicknames(count=10, seed=3, length=key, data=data)
            self.assertEqual(result["length"], key)
            self.assertEqual(result["fallbacks"], [])
            for item in result["nicknames"]:
                self.assertTrue(
                    spec["min"] <= item["chars"] <= spec["max"],
                    "%s (%d chars) out of %s range" % (item["name"], item["chars"], key),
                )

    def test_style_and_length_combined(self):
        result = gn.generate_nicknames(count=5, seed=21, style="简约", length="long")
        self.assertEqual(result["style"], "简约")
        self.assertEqual(result["length"], "long")
        self.assertEqual(result["fallbacks"], [])
        for item in result["nicknames"]:
            self.assertTrue(7 <= item["chars"] <= 10)

    def test_style_source_marks_cli(self):
        explicit = gn.generate_nicknames(count=3, seed=1, style="中性", length="short")
        self.assertEqual(explicit["style_source"], "cli")
        self.assertEqual(explicit["length_source"], "cli")
        auto = gn.generate_nicknames(count=3, seed=1)
        self.assertEqual(auto["style_source"], "random")
        self.assertEqual(auto["length_source"], "random")

    def test_unknown_style_and_length_rejected(self):
        with self.assertRaises(ValueError):
            gn.generate_nicknames(seed=1, style="不存在")
        with self.assertRaises(ValueError):
            gn.generate_nicknames(seed=1, length="超长")


class RenderTests(unittest.TestCase):
    def test_markdown_contains_sections(self):
        result = gn.generate_nicknames(count=3, seed=42)
        md = gn.render_markdown(result)
        self.assertIn("# 随机昵称", md)
        self.assertIn("风格 Style", md)
        self.assertIn("长度 Length", md)
        self.assertIn("## 昵称", md)
        for item in result["nicknames"]:
            self.assertIn(item["name"], md)

    def test_text_render(self):
        result = gn.generate_nicknames(count=2, seed=42)
        text = gn.render_text(result)
        self.assertIn("Nickname Generator", text)
        for item in result["nicknames"]:
            self.assertIn(item["name"], text)

    def test_json_render_round_trips(self):
        result = gn.generate_nicknames(count=4, seed=42, style="简约", length="short")
        parsed = json.loads(gn.render(result, "json"))
        self.assertEqual(parsed["style"], "简约")
        self.assertEqual(parsed["length"], "short")
        self.assertEqual(len(parsed["nicknames"]), 4)
        self.assertEqual(
            len(set(n["name"] for n in parsed["nicknames"])), 4
        )


class CliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT_PATH, *args],
            capture_output=True,
            text=True,
            cwd=SKILL_DIR,
        )

    def test_cli_markdown_seed_reproducible(self):
        first = self._run("--seed", "555", "--count", "3", "--format", "markdown")
        second = self._run("--seed", "555", "--count", "3", "--format", "markdown")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_cli_json_is_parseable(self):
        result = self._run("--seed", "42", "--count", "5", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertIn("nicknames", parsed)
        self.assertEqual(parsed["seed"], 42)
        self.assertEqual(len(parsed["nicknames"]), 5)

    def test_cli_style_and_length_filters(self):
        result = self._run(
            "--seed", "9", "--count", "3", "--style", "文艺", "--length", "long",
            "--format", "json",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["style"], "文艺")
        self.assertEqual(parsed["length"], "long")
        for item in parsed["nicknames"]:
            self.assertTrue(7 <= item["chars"] <= 10)

    def test_cli_default_count(self):
        result = self._run("--seed", "1")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("数量 Count: 1", result.stdout)

    def test_cli_count_above_max_fails(self):
        result = self._run("--count", "21")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--count must be <= 20", result.stderr)

    def test_cli_invalid_style_fails(self):
        result = self._run("--style", "unknown-style")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown style", result.stderr)

    def test_cli_output_writes_file(self):
        out_path = os.path.join(HERE, "_out_test.md")
        try:
            result = self._run("--seed", "2", "--count", "2", "--output", out_path)
            self.assertEqual(result.returncode, 0, result.stderr)
            with open(out_path, "r", encoding="utf-8") as handle:
                body = handle.read()
            self.assertIn("# 随机昵称", body)
        finally:
            if os.path.exists(out_path):
                os.remove(out_path)

    def test_cli_list_styles_and_lengths(self):
        styles = self._run("--list-styles")
        self.assertEqual(styles.returncode, 0)
        self.assertIn("文艺", styles.stdout)
        lengths = self._run("--list-lengths")
        self.assertEqual(lengths.returncode, 0)
        self.assertIn("short", lengths.stdout)

    def test_cli_help(self):
        result = self._run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--count", result.stdout)
        self.assertIn("--seed", result.stdout)


class NoExternalDependencyTests(unittest.TestCase):
    def test_no_cloud_or_third_party_imports(self):
        with open(SCRIPT_PATH, "r", encoding="utf-8") as handle:
            source = handle.read()
        for forbidden in ("huaweicloudsdk", "hcloud", "requests", "urllib.request"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main(verbosity=2)