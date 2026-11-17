#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v2 模块回归测试：M3b 用户理解、M4 语气与 Humanizer 守门

运行：python tests/test_v3.py
"""

import json
import os
import re
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.user.profile import UserProfileStore, signal_from_message  # noqa: E402
from scripts.user.guide import infer_attachment, compile_guide  # noqa: E402
from scripts.style.humanizer import scan, is_clean  # noqa: E402
from scripts.style.voice import shape, split_short, is_night  # noqa: E402
from scripts.pipeline.injector import estimate_tokens  # noqa: E402


class UserProfileTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lc_v3_")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.tmp
        self.store = UserProfileStore(self.tmp)

    def test_signal_extraction_no_raw_text(self):
        sig = signal_from_message("今天加班好累，压力好大")
        self.assertNotIn("加班", json.dumps(sig, ensure_ascii=False),
                         "信号里不应保留原始文本")
        self.assertEqual(sig["emotion"], "疲惫")
        self.assertIn("工作", sig["topics"])

    def test_privacy_filtered_signal(self):
        sig = signal_from_message("我的手机号是13812345678")
        self.assertNotIn("13812345678", json.dumps(sig, ensure_ascii=False))

    def test_two_level_analysis(self):
        # 轻量：每 5 条
        for i in range(5):
            self.store.ingest("今天好累，工作好烦")
        self.assertGreater(len(self.store.get()["情绪模式"]["常见情绪"]), 0)
        # 深度：每 50 条
        for i in range(45):
            self.store.ingest("在吗，怎么不回我，是不是不在乎我了")
        persona = self.store.get()
        self.assertIn(persona["依恋类型"]["判断"], ["焦虑型", "回避型", "安全型", "恐惧型"])
        self.assertGreater(persona["大五人格"]["置信度"], 0)

    def test_feedback_loop(self):
        self.store.apply_feedback("别发这么长，也别用 emoji")
        persona = self.store.get()
        self.assertEqual(persona["互动偏好"]["回复长度偏好"], "短")
        self.assertEqual(persona["沟通风格"]["emoji频率"], 0.0)

    def test_clear(self):
        self.store.ingest("测试")
        self.store.clear()
        self.assertFalse((Path(self.tmp) / "user_persona.json").exists())


class GuideTests(unittest.TestCase):
    def test_attachment_inference(self):
        anxious = [{"emotion": "焦虑", "question": True, "length": 8, "emoji": 0} for _ in range(30)]
        avoidant = [{"emotion": None, "question": False, "length": 4, "emoji": 0} for _ in range(30)]
        secure = [{"emotion": "开心", "question": False, "length": 25, "emoji": 1} for _ in range(30)]
        self.assertEqual(infer_attachment(anxious)["判断"], "焦虑型")
        self.assertEqual(infer_attachment(avoidant)["判断"], "回避型")
        self.assertEqual(infer_attachment(secure)["判断"], "安全型")

    def test_empty_signals(self):
        self.assertEqual(infer_attachment([])["判断"], "未知")

    def test_guide_within_budget(self):
        persona = {
            "依恋类型": {"判断": "焦虑型"},
            "沟通风格": {"句式长度": "短句"},
            "情绪模式": {"常见情绪": ["疲惫", "焦虑"]},
            "互动偏好": {"喜欢的话题": ["工作"], "回复长度偏好": "短", "主动程度偏好": "高"},
        }
        guide = compile_guide(persona)
        self.assertLessEqual(estimate_tokens(guide), 200, "相处指南必须 <200 Token")
        self.assertIn("焦虑型", guide)

    def test_guide_truncated_when_overflow(self):
        persona = {
            "依恋类型": {"判断": "焦虑型"},
            "互动偏好": {"喜欢的话题": ["话题" * 30]},
        }
        guide = compile_guide(persona, budget=200)
        self.assertLessEqual(estimate_tokens(guide), 200)


class HumanizerTests(unittest.TestCase):
    def test_detects_l1_words(self):
        result = scan("首先，你需要理解情绪；其次，可以深呼吸；最后，保持作息。")
        self.assertTrue(result["l1"], "L1 禁用词应被命中")
        self.assertFalse(result["clean"])

    def test_detects_numbered_list(self):
        result = scan("1. 早点睡\n2. 多喝热水\n3. 别想太多")
        self.assertIn("逐条编号", result["l2"])

    def test_detects_missing_modal_particles(self):
        result = scan("根据目前的描述，建议你可以尝试调整作息并保持规律的饮食结构。")
        self.assertTrue(any("语气词" in x for x in result["l3"]))

    def test_clean_text_passes(self):
        self.assertTrue(is_clean("辛苦啦，早点睡呀～我在这儿呢。"))

    def test_score_bounded(self):
        self.assertLessEqual(scan("首先其次最后综上所述")["score"], 1.0)


class VoiceTests(unittest.TestCase):
    def test_split_short(self):
        text = "今天辛苦啦，我听你说项目很紧，先别硬撑，喝口热水，早点休息，我在这儿陪着你。"
        pieces = split_short(text, max_len=22)
        self.assertGreater(len(pieces), 1)
        self.assertTrue(all(len(p) <= 30 for p in pieces))

    def test_levels_produce_different_output(self):
        text = "今天辛苦啦，先别硬撑，喝口热水，早点休息，我在这儿陪着你。"
        off = shape(text, level="关闭")
        std = shape(text, level="标准")
        deep = shape(text, level="深度", nickname="宝贝")
        self.assertEqual(len(off), 1, "关闭档应原样返回")
        self.assertGreaterEqual(len(std), len(off))
        self.assertTrue(
            any("宝贝" in s or re.search(r"[呀呢嘛哦啦]$|～", s) for s in deep),
            "深度档应带称呼或语气词",
        )

    def test_night_mode_shorter_and_softer(self):
        text = "今天很累吧，我陪你聊会儿，然后早点睡，明天会好一点的"
        day = shape(text, level="标准", hour=14)
        night = shape(text, level="标准", hour=23)
        self.assertTrue(is_night(23))
        self.assertFalse(is_night(14))
        self.assertLessEqual(
            sum(len(s) for s in night) / max(1, len(night)),
            sum(len(s) for s in day) / max(1, len(day)) + 1,
        )

    def test_empty_input(self):
        self.assertEqual(shape("", level="深度"), [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
