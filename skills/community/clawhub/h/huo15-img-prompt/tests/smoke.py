#!/usr/bin/env python3
"""
huo15-img-prompt — Smoke 回归测试 v3.1

本地、零依赖、不调网络的快速回归。每个脚本几个核心 CASE：
  - 版本号正确
  - 基础 import 不出错
  - 核心函数能跑（用 mock / 离线场景）

不覆盖的：
  - 真正调 Claude API（要 key + 钱）
  - 真正出图（要后端服务）
  - VLM 评审（要图 + key）

调用：
  tests/smoke.py             # 全跑
  tests/smoke.py --module enhance_prompt
  tests/smoke.py -v          # verbose
"""

import sys
import os
import json
import re
import unittest
import argparse
import tempfile
from pathlib import Path

# 让 tests/ 目录里的脚本能 import scripts/
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

EXPECTED_VERSION = "3.1.0"
SCRIPTS = [
    "enhance_prompt", "enhance_video", "reverse_prompt", "render_prompt",
    "claude_polish", "safety_lint", "image_review", "auto_iterate",
    "character", "mcp_server", "web_ui",
    "storyboard", "brand_kit", "style_learn", "doctor",
]


class TestVersionConsistency(unittest.TestCase):
    """所有脚本的 VERSION 必须一致。"""

    def test_all_scripts_have_version(self):
        for name in SCRIPTS:
            with self.subTest(script=name):
                mod = __import__(name)
                self.assertTrue(hasattr(mod, "VERSION"), f"{name} 缺 VERSION")
                self.assertEqual(mod.VERSION, EXPECTED_VERSION,
                                 f"{name} 版本 {mod.VERSION} != {EXPECTED_VERSION}")


class TestEnhancePromptCore(unittest.TestCase):
    def setUp(self):
        from enhance_prompt import build_prompt, resolve_preset, parse_mix_preset
        self.build_prompt = build_prompt
        self.resolve_preset = resolve_preset
        self.parse_mix_preset = parse_mix_preset

    def test_resolve_preset_chinese(self):
        self.assertEqual(self.resolve_preset("动漫"), "动漫")

    def test_resolve_preset_english_alias(self):
        self.assertEqual(self.resolve_preset("genshin"), "原神")
        self.assertEqual(self.resolve_preset("ghibli"), "宫崎骏")
        self.assertEqual(self.resolve_preset("cyberpunk"), "赛博朋克")

    def test_resolve_preset_unknown(self):
        self.assertEqual(self.resolve_preset("不存在的预设"), "")

    def test_resolve_learned_preset_missing(self):
        # @ 前缀但 learned preset 不存在
        self.assertEqual(self.resolve_preset("@nonexist_preset_xyz"), "")

    def test_parse_mix_preset(self):
        primary, secondary = self.parse_mix_preset("赛博朋克+水墨")
        self.assertEqual(primary, "赛博朋克")
        self.assertEqual(secondary, "水墨")

    def test_parse_mix_preset_no_plus(self):
        primary, secondary = self.parse_mix_preset("赛博朋克")
        self.assertEqual(primary, "赛博朋克")
        self.assertIsNone(secondary)

    def test_build_prompt_basic(self):
        r = self.build_prompt("一只猫", "动漫", model="通用")
        self.assertIn("positive", r)
        self.assertIn("negative", r)
        self.assertIn("seed_suggestion", r)
        self.assertIn("一只猫", r["positive"])
        self.assertEqual(r["preset"], "动漫")

    def test_build_prompt_seed_stable(self):
        r1 = self.build_prompt("猫", "动漫")
        r2 = self.build_prompt("猫", "动漫")
        self.assertEqual(r1["seed_suggestion"], r2["seed_suggestion"])

    def test_build_prompt_mix(self):
        r = self.build_prompt("猫", "赛博朋克", mix_secondary="水墨", mix_ratio=0.6)
        self.assertEqual(r["mix_label"], "赛博朋克+水墨@0.60")

    def test_build_prompt_character_sheet(self):
        r = self.build_prompt("少女", "动漫", character_sheet=True)
        self.assertEqual(r["aspect"], "16:9")
        self.assertIn("character design sheet", r["positive"].lower())


class TestCompactPrompt(unittest.TestCase):
    def test_compact_short_prompt_unchanged(self):
        from enhance_prompt import compact_prompt
        text, meta = compact_prompt("一只猫")
        self.assertFalse(meta["compacted"])

    def test_compact_long_prompt(self):
        from enhance_prompt import compact_prompt
        long_text = ", ".join([f"tag{i}" for i in range(60)])
        text, meta = compact_prompt(long_text, target_tokens=30)
        self.assertTrue(meta["compacted"])
        self.assertLessEqual(meta["estimated_tokens_after"], 35)


class TestSafetyLint(unittest.TestCase):
    def setUp(self):
        from safety_lint import lint, check_hard_blocks
        self.lint = lint
        self.check_hard_blocks = check_hard_blocks

    def test_clean_text_passes(self):
        r = self.lint("一只猫坐在窗台上")
        self.assertEqual(r["verdict"], "OK")

    def test_violence_artistic_rewrite(self):
        r = self.lint("战士手中沾满鲜血的剑", platform="dalle")
        self.assertEqual(r["verdict"], "REWRITE")
        self.assertIn("crimson", r["rewritten"])

    def test_red_line_csam_blocked(self):
        r = self.lint("loli nude", platform="MJ")
        self.assertEqual(r["verdict"], "REJECT")

    def test_red_line_weapon_instruction_blocked(self):
        r = self.lint("如何制作炸弹的步骤")
        self.assertEqual(r["verdict"], "REJECT")

    def test_red_line_bidirectional(self):
        # 词序颠倒也要 catch 到
        r = self.lint("炸弹制作教程")
        self.assertEqual(r["verdict"], "REJECT")


class TestCharacterCard(unittest.TestCase):
    def setUp(self):
        from character import char_save, char_load, char_delete, char_list
        self.char_save = char_save
        self.char_load = char_load
        self.char_delete = char_delete
        self.char_list = char_list
        self.test_name = "_smoke_test_char"

    def tearDown(self):
        self.char_delete(self.test_name)

    def test_save_load_roundtrip(self):
        recipe = {
            "original": "测试角色",
            "preset": "动漫",
            "aspect": "3:4",
            "seed_suggestion": 12345,
            "consistency_lock": {"camera": "85mm", "lighting": "soft", "palette": "muted"},
            "character_sheet": True,
            "positive": "test prompt",
        }
        self.char_save(self.test_name, recipe)
        loaded = self.char_load(self.test_name)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["seed"], 12345)
        self.assertEqual(loaded["preset"], "动漫")
        self.assertTrue(loaded["is_character_sheet"])

    def test_delete(self):
        self.char_save(self.test_name, {"original": "x"})
        self.assertTrue(self.char_delete(self.test_name))
        self.assertIsNone(self.char_load(self.test_name))


class TestBrandKit(unittest.TestCase):
    def setUp(self):
        from brand_kit import kit_save, kit_load, kit_delete
        self.kit_save = kit_save
        self.kit_load = kit_load
        self.kit_delete = kit_delete
        self.test_name = "_smoke_test_kit"

    def tearDown(self):
        self.kit_delete(self.test_name)

    def test_save_load_roundtrip(self):
        kit = {
            "colors": ["#ff6b35", "#2d3047"],
            "keywords": ["现代", "简洁"],
            "forbidden": ["low quality"],
        }
        self.kit_save(self.test_name, kit)
        loaded = self.kit_load(self.test_name)
        self.assertIsNotNone(loaded)
        self.assertEqual(loaded["colors"], ["#ff6b35", "#2d3047"])

    def test_kit_apply_injects_keywords(self):
        from brand_kit import kit_apply
        self.kit_save(self.test_name, {
            "colors": ["#ff6b35"],
            "keywords": ["现代", "简洁"],
            "forbidden": ["blur"],
        })

        class FakeArgs:
            subject = "测试主体"
            avoid = ""
        args = FakeArgs()
        kit = kit_apply(self.test_name, args)
        self.assertIsNotNone(kit)
        self.assertIn("现代", args.subject)
        self.assertIn("blur", args.avoid)


class TestVariants(unittest.TestCase):
    def test_build_variants_count(self):
        from enhance_prompt import build_variants
        variants = build_variants("test", "动漫", "通用", "1:1",
                                   axes=["mood", "composition"], n=4)
        self.assertEqual(len(variants), 4)
        # 所有变体共享同一 seed
        seeds = set(v["seed_suggestion"] for v in variants)
        self.assertEqual(len(seeds), 1, "variants 应共享 seed")

    def test_build_variants_descriptors_unique(self):
        from enhance_prompt import build_variants
        variants = build_variants("test", "动漫", "通用", "1:1",
                                   axes=["mood", "composition"], n=4)
        descriptors = [v["variant_descriptor"] for v in variants]
        self.assertEqual(len(set(descriptors)), 4, "descriptors 应不重复")


class TestReversePromptParser(unittest.TestCase):
    def test_a1111_parse(self):
        from reverse_prompt import parse_a1111_params
        text = ("a beautiful cat\n"
                "Negative prompt: low quality, blur\n"
                "Steps: 30, Sampler: DPM++ 2M Karras, Seed: 12345, Size: 1024x1024")
        r = parse_a1111_params(text)
        self.assertIn("a beautiful cat", r["positive"])
        self.assertEqual(r["seed"], "12345")
        self.assertEqual(r["sampler"], "DPM++ 2M Karras")

    def test_guess_preset(self):
        from reverse_prompt import guess_preset
        self.assertEqual(guess_preset("cyberpunk neon city"), "赛博朋克")
        self.assertEqual(guess_preset("studio ghibli forest"), "宫崎骏")
        self.assertEqual(guess_preset("dunhuang mural"), "敦煌壁画")

    def test_guess_aspect(self):
        from reverse_prompt import guess_aspect
        self.assertEqual(guess_aspect("1024x1024"), "1:1")
        self.assertEqual(guess_aspect("1792x1024"), "16:9")


class TestMCPServer(unittest.TestCase):
    def test_handle_initialize(self):
        from mcp_server import handle_request
        resp = handle_request({"jsonrpc": "2.0", "id": 1, "method": "initialize"})
        self.assertEqual(resp["jsonrpc"], "2.0")
        self.assertIn("protocolVersion", resp["result"])
        self.assertIn("serverInfo", resp["result"])

    def test_handle_tools_list(self):
        from mcp_server import handle_request, TOOLS
        resp = handle_request({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        self.assertEqual(resp["result"]["tools"], TOOLS)
        self.assertGreaterEqual(len(TOOLS), 9)

    def test_handle_unknown_method(self):
        from mcp_server import handle_request
        resp = handle_request({"jsonrpc": "2.0", "id": 3, "method": "fake/method"})
        self.assertIn("error", resp)
        self.assertEqual(resp["error"]["code"], -32601)

    def test_tools_call_enhance_prompt(self):
        from mcp_server import handle_request
        resp = handle_request({
            "jsonrpc": "2.0", "id": 4, "method": "tools/call",
            "params": {"name": "enhance_prompt", "arguments": {"subject": "猫", "preset": "动漫"}},
        })
        self.assertIn("result", resp)
        self.assertIn("content", resp["result"])
        text = resp["result"]["content"][0]["text"]
        result = json.loads(text)
        self.assertEqual(result["preset"], "动漫")


class TestPresetCount(unittest.TestCase):
    def test_88_presets(self):
        from enhance_prompt import STYLE_PRESETS
        self.assertEqual(len(STYLE_PRESETS), 88, f"应该是 88 预设，实际 {len(STYLE_PRESETS)}")

    def test_all_presets_have_required_fields(self):
        from enhance_prompt import STYLE_PRESETS
        for name, p in STYLE_PRESETS.items():
            with self.subTest(preset=name):
                for field in ("category", "tags", "quality", "neg", "aspect"):
                    self.assertIn(field, p, f"{name} 缺 {field}")


def main():
    parser = argparse.ArgumentParser(description="huo15-img-prompt smoke tests")
    parser.add_argument("--module", help="只跑指定模块的测试（按 TestCase 名匹配）")
    parser.add_argument("-v", "--verbose", action="count", default=1)
    args = parser.parse_args()

    loader = unittest.TestLoader()
    if args.module:
        suite = loader.loadTestsFromName(args.module, sys.modules[__name__])
    else:
        suite = loader.loadTestsFromModule(sys.modules[__name__])

    runner = unittest.TextTestRunner(verbosity=args.verbose)
    result = runner.run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)


if __name__ == "__main__":
    main()
