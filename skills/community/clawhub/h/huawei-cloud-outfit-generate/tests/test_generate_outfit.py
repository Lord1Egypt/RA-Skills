#!/usr/bin/env python3
"""Unit tests for scripts/generate_outfit.py.

Run from the skill directory:
    python3 -m unittest discover -s tests -v
or:
    python3 tests/test_generate_outfit.py
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
SCRIPT_PATH = os.path.join(SCRIPTS_DIR, "generate_outfit.py")


def _load_module():
    spec = importlib.util.spec_from_file_location("generate_outfit", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


go = _load_module()

CATEGORIES = ("top", "bottom", "footwear", "accessory")


class LoadWardrobeTests(unittest.TestCase):
    def test_categories_present(self):
        wardrobe = go.load_wardrobe()
        for category in CATEGORIES:
            self.assertIn(category, wardrobe["items"])
            self.assertGreater(len(wardrobe["items"][category]), 0)

    def test_style_and_season_coverage(self):
        wardrobe = go.load_wardrobe()
        styles = wardrobe["styles"]
        seasons = wardrobe["seasons"]
        self.assertTrue(styles)
        self.assertTrue(seasons)
        for category in CATEGORIES:
            pool = wardrobe["items"][category]
            for style in styles:
                self.assertTrue(
                    any(style in it["styles"] for it in pool),
                    "no %s item for style %s" % (category, style),
                )
            for season in seasons:
                self.assertTrue(
                    any(season in it["seasons"] for it in pool),
                    "no %s item for season %s" % (category, season),
                )

    def test_missing_file_raises(self):
        with self.assertRaises(OSError):
            go.load_wardrobe(os.path.join(HERE, "does-not-exist.json"))


class PickOutfitTests(unittest.TestCase):
    def test_default_shape(self):
        outfit = go.pick_outfit(seed=1234)
        self.assertEqual(set(outfit["items"]), set(CATEGORIES))
        for category in CATEGORIES:
            self.assertTrue(outfit["items"][category]["name"])
        self.assertIn(outfit["style"], go.load_wardrobe()["styles"])
        self.assertIn(outfit["season"], go.load_wardrobe()["seasons"])

    def test_same_seed_is_reproducible(self):
        first = go.pick_outfit(seed=20240501)
        second = go.pick_outfit(seed=20240501)
        self.assertEqual(go.render_markdown(first), go.render_markdown(second))
        self.assertEqual(first["items"], second["items"])

    def test_different_seeds_differ(self):
        first = go.pick_outfit(seed=1)
        second = go.pick_outfit(seed=2)
        self.assertNotEqual(first["items"], second["items"])

    def test_no_seed_generates_concrete_seed(self):
        outfit = go.pick_outfit()
        self.assertIsInstance(outfit["seed"], int)
        self.assertFalse(outfit["explicit_seed"])

    def test_style_filter_is_applied(self):
        # 休闲 + 秋 is fully covered by the built-in wardrobe.
        wardrobe = go.load_wardrobe()
        outfit = go.pick_outfit(seed=7, style="休闲", season="秋", wardrobe=wardrobe)
        self.assertEqual(outfit["style"], "休闲")
        self.assertEqual(outfit["season"], "秋")
        self.assertEqual(outfit["fallbacks"], [])
        picked = {outfit["items"][c]["name"] for c in CATEGORIES}
        for category in CATEGORIES:
            name = outfit["items"][category]["name"]
            candidates = [
                it for it in wardrobe["items"][category]
                if "休闲" in it["styles"] and "秋" in it["seasons"]
            ]
            self.assertTrue(candidates)
            self.assertIn(name, [it["name"] for it in candidates])
        self.assertEqual(len(picked), len(CATEGORIES))

    def test_season_filter_is_applied(self):
        wardrobe = go.load_wardrobe()
        outfit = go.pick_outfit(seed=11, style="简约", season="冬", wardrobe=wardrobe)
        self.assertEqual(outfit["style"], "简约")
        self.assertEqual(outfit["season"], "冬")
        self.assertEqual(outfit["fallbacks"], [])
        for category in CATEGORIES:
            name = outfit["items"][category]["name"]
            candidates = [
                it for it in wardrobe["items"][category]
                if "简约" in it["styles"] and "冬" in it["seasons"]
            ]
            self.assertTrue(candidates)
            self.assertIn(name, [it["name"] for it in candidates])

    def test_style_alias_and_case(self):
        outfit = go.pick_outfit(seed=3, style="Casual", season="autumn")
        self.assertEqual(outfit["style"], "休闲")
        self.assertEqual(outfit["season"], "秋")

    def test_unknown_style_rejected(self):
        with self.assertRaises(ValueError):
            go.pick_outfit(seed=1, style="不存在的风格")

    def test_unknown_season_rejected(self):
        with self.assertRaises(ValueError):
            go.pick_outfit(seed=1, season="雨季")

    def test_style_source_marks_cli(self):
        outfit = go.pick_outfit(seed=1, style="运动")
        self.assertEqual(outfit["style_source"], "cli")
        self.assertEqual(outfit["season_source"], "random")


class RenderTests(unittest.TestCase):
    def test_markdown_contains_sections(self):
        outfit = go.pick_outfit(seed=42)
        md = go.render_markdown(outfit)
        self.assertIn("# 今日穿搭", md)
        self.assertIn("风格 Style", md)
        self.assertIn("季节 Season", md)
        for label in ("上装", "下装", "鞋履", "配饰"):
            self.assertIn("**%s**" % label, md)

    def test_text_render(self):
        outfit = go.pick_outfit(seed=42)
        text = go.render_text(outfit)
        self.assertIn("Outfit of the Day", text)
        self.assertIn("上装:", text)
        self.assertIn("配饰:", text)

    def test_json_render_round_trips(self):
        outfit = go.pick_outfit(seed=42, style="简约", season="春")
        parsed = json.loads(go.render(outfit, "json"))
        self.assertEqual(set(parsed["items"]), set(CATEGORIES))
        self.assertEqual(parsed["style"], "简约")
        self.assertEqual(parsed["season"], "春")


class CliTests(unittest.TestCase):
    def _run(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT_PATH, *args],
            capture_output=True,
            text=True,
            cwd=SKILL_DIR,
        )

    def test_cli_markdown_seed_reproducible(self):
        first = self._run("--seed", "555", "--format", "markdown")
        second = self._run("--seed", "555", "--format", "markdown")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(first.stdout, second.stdout)

    def test_cli_json_is_parseable(self):
        result = self._run("--seed", "42", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertIn("items", parsed)
        self.assertEqual(parsed["seed"], 42)

    def test_cli_style_and_season_filters(self):
        result = self._run("--seed", "9", "--style", "casual", "--season", "秋", "--format", "json")
        self.assertEqual(result.returncode, 0, result.stderr)
        parsed = json.loads(result.stdout)
        self.assertEqual(parsed["style"], "休闲")
        self.assertEqual(parsed["season"], "秋")

    def test_cli_invalid_style_fails(self):
        result = self._run("--style", "unknown-style")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown style", result.stderr)

    def test_cli_list_styles(self):
        result = self._run("--list-styles")
        self.assertEqual(result.returncode, 0)
        self.assertIn("休闲", result.stdout)

    def test_cli_help(self):
        result = self._run("--help")
        self.assertEqual(result.returncode, 0)
        self.assertIn("--seed", result.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)