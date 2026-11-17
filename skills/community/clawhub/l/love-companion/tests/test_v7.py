#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定制化回归测试（守住 love-companion 自身的设计决策）

这一组专门守住几条容易走偏的边界：
- adapt        三层提取必须回写进 v1 人设字段；安全字段蒸馏无权改
- humanizer    检测的是**中文恋爱对话**的 AI 腔，不是论文腔
- care         依恋差异化（方案 4.3）：焦虑型给确定性 / 回避型给空间
- trends       按「适不适合跟恋人聊」取舍，不做平台全覆盖的注册表
- multimodal   由 v1 关心方式 / 亲密尺度 / 内容边界决定，不是通用审美
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import schema  # noqa: E402
from scripts.persona import adapt, extract, library, parser  # noqa: E402
from scripts.pipeline.injector import estimate_tokens  # noqa: E402


DEMO = "\n".join([
    "小美: 在吗 想你了呀",
    "小美: 今天加班累死了 想吃点甜的～",
    "小美: 你定吧 我都行啦",
    "小美: 算了 不想说了",
    "小美: 宝贝晚安呀",
    "小美: 我就是说我觉得这个挺好的嘛",
] * 4)


class TempDataMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.data_dir = self._tmp.name
        self._old_env = os.environ.get("LOVE_COMPANION_DATA_DIR")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.data_dir
        self.addCleanup(self._restore)

    def _restore(self) -> None:
        if self._old_env is None:
            os.environ.pop("LOVE_COMPANION_DATA_DIR", None)
        else:
            os.environ["LOVE_COMPANION_DATA_DIR"] = self._old_env
        self._tmp.cleanup()

    def extracted(self):
        corpus = parser.only(parser.parse_text(DEMO), "小美")
        return extract.extract_persona(corpus, name="小美", nickname="美美")


# ==================== adapt：三层 → v1 人设 ====================

class TestAdaptToV1(unittest.TestCase):
    def setUp(self):
        self.p = self._extract()

    def _extract(self):
        corpus = parser.only(parser.parse_text(DEMO), "小美")
        return extract.extract_persona(corpus, name="小美", nickname="美美")

    def test_maps_voice_to_dialog_style(self):
        v1 = adapt.apply_to_v1({}, self.p)
        self.assertTrue(v1["对话风格"]["口头禅"])
        self.assertTrue(v1["对话风格"]["语气"] or v1["对话风格"]["语言习惯"])

    def test_maps_character_to_persona_char(self):
        v1 = adapt.apply_to_v1({}, self.p)
        self.assertTrue(v1["性格"]["核心特质"])
        self.assertTrue(v1["性格"]["小脾气"], "冲突对应映射到小脾气")
        self.assertTrue(v1["性格"]["情绪表达"])

    def test_maps_thinking_to_relation_and_background(self):
        v1 = adapt.apply_to_v1({}, self.p)
        self.assertTrue(v1["相处模式"]["主动程度"])
        self.assertTrue(v1["相处模式"]["关心方式"])
        self.assertTrue(v1["背景故事"])

    def test_immutable_fields_preserved(self):
        base = {"亲密尺度": 1, "内容边界": ["不谈前任"], "对用户的称呼": "宝宝",
                "姓名": "小雨", "性别": "女", "年龄": 22}
        v1 = adapt.apply_to_v1(base, self.p)
        for k, want in base.items():
            self.assertEqual(v1[k], want, f"{k} 被蒸馏改动了")

    def test_no_overwrite_by_default(self):
        base = {"对话风格": {"语气": "手写值", "口头禅": ["手写"], "语言习惯": "手写"}}
        v1 = adapt.apply_to_v1(base, self.p)
        self.assertEqual(v1["对话风格"]["语气"], "手写值")

    def test_overwrite_true_replaces(self):
        base = {"对话风格": {"语气": "手写值", "口头禅": ["手写"], "语言习惯": ""}}
        v1 = adapt.apply_to_v1(base, self.p, overwrite=True)
        self.assertNotEqual(v1["对话风格"]["语气"], "手写值")

    def test_lover_card_uses_v1_fields(self):
        v1 = adapt.apply_to_v1({"姓名": "小雨", "对用户的称呼": "宝宝",
                                "亲密尺度": 2, "内容边界": ["不谈前任"]}, self.p)
        card = adapt.lover_card(v1)
        self.assertIn("小雨", card)
        self.assertIn("宝宝", card)
        self.assertIn("亲密尺度 2", card)
        self.assertIn("不谈前任", card)

    def test_lover_card_within_budget(self):
        v1 = adapt.apply_to_v1({"姓名": "小雨", "对用户的称呼": "宝宝"}, self.p)
        self.assertLessEqual(estimate_tokens(adapt.lover_card(v1)),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])

    def test_lover_card_handles_empty_persona(self):
        self.assertEqual(adapt.lover_card({}), "")


class TestLibraryV1Bridge(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.lib = library.PersonaLibrary(self.data_dir)
        self.lib.create(self.extracted(), "美美")

    def test_stores_v1_persona(self):
        v1 = self.lib.v1_persona("美美")
        self.assertTrue(v1.get("对话风格"))
        self.assertTrue(v1.get("性格"))

    def test_push_to_v1_writes_manager_persona(self):
        from scripts.manager import LoveCompanionManager
        # 先放一份用户手写的 v1 人设，含安全字段
        manager = LoveCompanionManager(self.data_dir)
        manager.set_persona({"姓名": "小雨", "对用户的称呼": "宝宝",
                             "亲密尺度": 2, "内容边界": ["不谈前任"]})
        self.lib.push_to_v1("美美")
        after = manager.get_persona()
        self.assertTrue(after["对话风格"]["口头禅"], "蒸馏的口头禅应写进 v1 人设")
        self.assertEqual(after["亲密尺度"], 2, "亲密尺度不得被蒸馏改动")
        self.assertEqual(after["内容边界"], ["不谈前任"])
        self.assertEqual(after["对用户的称呼"], "宝宝")

    def test_push_to_v1_missing_slug(self):
        with self.assertRaises(KeyError):
            self.lib.push_to_v1("不存在")

    def test_compile_summary_uses_lover_card(self):
        card = self.lib.compile_summary("美美")
        self.assertTrue(card)
        self.assertLessEqual(estimate_tokens(card),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])

    def test_from_preset_returns_v1_structure(self):
        from scripts.manager import LoveCompanionManager
        presets = LoveCompanionManager().list_presets()
        if presets:
            preset = self.lib.from_preset(1)
            self.assertTrue(preset)
            self.assertIn("对话风格", preset, "预设应是 v1 人设结构")


# ==================== humanizer：中文恋爱对话的 AI 腔 ====================

class TestHumanizerLoverTone(unittest.TestCase):
    def setUp(self):
        from scripts.style import humanizer
        self.h = humanizer

    def test_cliched_comfort_flagged(self):
        for text in ["我理解你的感受，别难过了",
                     "抱抱你，一切都会好起来的",
                     "记得照顾好自己哦",
                     "你一定很难过吧"]:
            with self.subTest(text=text):
                self.assertFalse(self.h.is_clean(text), f"未检出 AI 腔：{text}")

    def test_asserting_users_feelings_flagged(self):
        self.assertFalse(self.h.is_clean("听到你这么说，我也能感受到你的难过"))

    def test_open_question_barrage_flagged(self):
        self.assertFalse(self.h.is_clean("怎么了？为什么不开心？跟我说说？"))

    def test_nickname_stacking_flagged(self):
        self.assertFalse(self.h.is_clean("宝贝你听我说，宝贝乖"))

    def test_natural_lover_reply_is_clean(self):
        for text in ["在干嘛呀", "刚下班，累死了～", "想吃火锅，一起？", "晚安呀，早点睡"]:
            with self.subTest(text=text):
                self.assertTrue(self.h.is_clean(text), f"误报 AI 腔：{text}")

    def test_emoji_per_sentence_flagged(self):
        result = self.h.scan("好呀🎉。真的吗✨。太棒了🌟")
        self.assertTrue(any("句句带表情" in x for x in result["l3"]))

    def test_long_sentence_flagged_for_lover_talk(self):
        result = self.h.scan("今天发生了一件事情让我觉得特别纠结，我想了很久也没想明白到底应该怎么处理才比较合适。")
        self.assertTrue(any("过长" in x for x in result["l3"]))


# ==================== care：依恋差异化（方案 4.3） ====================

class TestAttachmentDifferentiation(unittest.TestCase):
    def setUp(self):
        from scripts.care import templates
        self.t = templates

    def test_anxious_gets_certainty(self):
        out = self.t.render("久未联系", nickname="宝贝", attachment="焦虑型", seed=0)
        self.assertTrue(any(s in out for s in ("我在，看到就回你", "不是客气，是真的在")))

    def test_avoidant_gets_space(self):
        out = self.t.render("久未联系", nickname="宝贝", attachment="回避型", seed=0)
        self.assertTrue(any(s in out for s in ("不用回我", "忙你的")))

    def test_avoidant_no_pressing_question(self):
        out = self.t.render("低落陪伴", nickname="宝贝", attachment="回避型", seed=0)
        self.assertNotIn("为什么不", out)
        self.assertNotIn("怎么不回", out)

    def test_anxious_removes_open_question(self):
        out = self.t.render("久未联系", nickname="宝贝", attachment="焦虑型", seed=0)
        self.assertNotIn("在吗", out)

    def test_fearful_gets_certainty_and_exit(self):
        out = self.t.render("低落陪伴", nickname="宝贝", attachment="恐惧型", seed=0)
        self.assertTrue(any(s in out for s in ("我在，但你不用马上回", "想说的时候再说")))

    def test_secure_keeps_it_natural(self):
        out = self.t.render("日常", nickname="宝贝", attachment="安全型", seed=0)
        self.assertNotIn("我在，看到就回你", out)
        self.assertNotIn("不用回我", out)

    def test_attachment_suffix_survives_short_preference(self):
        """长度偏好=短也不能砍掉焦虑型最需要的那句确定性"""
        out = self.t.render("久未联系", nickname="宝贝", attachment="焦虑型",
                            length_pref="短", seed=0)
        self.assertIn("我在，看到就回你", out)

    def test_unknown_attachment_safe(self):
        out = self.t.render("久未联系", nickname="宝贝", attachment="火星型", seed=0)
        self.assertTrue(out)

    def test_compose_reads_attachment_from_profile(self):
        import tempfile
        from scripts.user.profile import UserProfileStore
        with tempfile.TemporaryDirectory() as d:
            os.environ["LOVE_COMPANION_DATA_DIR"] = d
            try:
                store = UserProfileStore(d)
                persona = store.get()
                persona["依恋类型"]["判断"] = "回避型"
                store._save_persona(persona)
                out = self.t.compose("久未联系", "某人", d)
                self.assertEqual(out["attachment"], "回避型")
                self.assertTrue(any(s in out["text"] for s in ("不用回我", "忙你的")))
            finally:
                os.environ.pop("LOVE_COMPANION_DATA_DIR", None)


# ==================== trends：按「适不适合聊」取舍 ====================

class TestTrendsLoverFit(unittest.TestCase):
    def setUp(self):
        from scripts.trends import sources
        self.s = sources

    def test_talkability_ranking(self):
        self.assertGreater(self.s.talkability("美食"), self.s.talkability("财经"))
        self.assertGreater(self.s.talkability("旅行"), self.s.talkability("社会新闻"))

    def test_worth_it_filters_low_talkability(self):
        self.assertTrue(self.s.worth_it("美食"))
        self.assertFalse(self.s.worth_it("时政"))

    def test_opener_gives_something_to_say(self):
        opener = self.s.opener("美食", seed=0)
        self.assertTrue(opener)
        self.assertTrue(self.s.opener("美食", seed=1))

    def test_blocked_by_content_boundary(self):
        r = self.s.SourceRouter()
        plan = r.plan("时政要闻", content_bounds=[])
        self.assertFalse(plan["值得抓"])
        with tempfile.TemporaryDirectory() as d:
            r2 = self.s.SourceRouter(d)
            plan2 = r2.plan("美食", content_bounds=["不谈前任"])
            self.assertTrue(plan2["值得抓"])
            plan3 = r2.plan("前任相关", content_bounds=["不谈前任"])
            self.assertFalse(plan3["值得抓"])
            self.assertIn("边界", plan3["拒绝原因"])

    def test_plan_has_opener(self):
        plan = self.s.SourceRouter().plan("美食")
        self.assertTrue(plan["开口"])
        self.assertTrue(plan["primary"])

    def test_platform_set_is_lover_relevant(self):
        """不做全网覆盖——只有恋人陪伴真用得上的源"""
        self.assertLessEqual(len(self.s.PLATFORMS), 4)
        for name in ("知乎", "豆瓣", "RSS", "GitHub", "YouTube"):
            self.assertNotIn(name, self.s.PLATFORMS)


# ==================== multimodal：v1 人设驱动 ====================

class TestImagePlanV1Driven(unittest.TestCase):
    def setUp(self):
        from scripts.multimodal import image_plan
        self.ip = image_plan

    def _planner(self):
        with tempfile.TemporaryDirectory() as d:
            return self.ip.ImagePlanner(d)

    def test_intimacy_level_bands(self):
        self.assertEqual(self.ip.intimacy_level(1), "低")
        self.assertEqual(self.ip.intimacy_level(3), "中")
        self.assertEqual(self.ip.intimacy_level(5), "高")
        self.assertEqual(self.ip.intimacy_level(None), "中")

    def test_low_intimacy_forbids_close_shots(self):
        self.assertIn("自拍", self.ip.INTIMACY_FRAME["低"]["禁忌元素"])
        self.assertEqual(self.ip.INTIMACY_FRAME["低"]["距离"], "只拍物与景，不出现人物")

    def test_care_style_drives_subject(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.ip.ImagePlanner(d)
            detail = p.style_for({"相处模式": {"关心方式": "细节型，会注意到你没说的小事"}}, "日常")
            action = p.style_for({"相处模式": {"关心方式": "行动型，直接替你把事办了"}}, "日常")
            self.assertIn("细小事物", detail["主体"])
            self.assertIn("正在为你做的事", action["主体"])

    def test_content_boundary_replaces_elements(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.ip.ImagePlanner(d)
            persona = {"相处模式": {"关心方式": "细节型"},
                       "内容边界": ["窗台的一小片光"]}
            style = p.style_for(persona, "日常")
            self.assertNotIn("窗台的一小片光", style["元素"])

    def test_style_has_frame_and_subject(self):
        with tempfile.TemporaryDirectory() as d:
            p = self.ip.ImagePlanner(d)
            style = p.style_for({"亲密尺度": 3}, "想念")
            for key in ("色调", "光线", "氛围", "构图", "元素", "主体", "拍摄距离"):
                self.assertIn(key, style)


if __name__ == "__main__":
    unittest.main(verbosity=2)
