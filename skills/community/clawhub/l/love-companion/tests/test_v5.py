#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M7a / M7b / M7c 回归测试

覆盖：
- trends.sources   抓取计划、故障转移、健康度排序
- trends.store     HTML 清洗、提炼、入库去重、调味料预算
- multimodal       发图闸门、风格推导、衔接话术与纠偏
- panel.explain    依据追溯、渲染、只存引用不存原文
- panel.controls   模块开关、特征权重、遗忘某段关系、导出与清除
- pipeline         五个新离线任务的端到端串联
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import schema  # noqa: E402
from scripts.pipeline.injector import estimate_tokens  # noqa: E402
from scripts.trends import sources as ts, store as tstore  # noqa: E402
from scripts.multimodal import image_plan as ip  # noqa: E402
from scripts.panel import explain as pex, controls as pctl  # noqa: E402


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

    def write_json(self, name: str, data) -> None:
        with open(Path(self.data_dir) / name, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)


# ==================== trends.sources ====================

class TestSourceRouter(TempDataMixin):
    def test_plan_has_primary_and_fallbacks(self):
        plan = ts.SourceRouter(self.data_dir).plan("美食")
        self.assertTrue(plan["primary"])
        self.assertTrue(plan["fallbacks"])
        self.assertIn(plan["primary"], ts.PLATFORMS)

    def test_plan_url_filled(self):
        plan = ts.SourceRouter(self.data_dir).plan("游戏", keyword="黑神话")
        self.assertIn("黑神话", plan["specs"][0]["url"])

    def test_unknown_topic_falls_back_to_default_chain(self):
        plan = ts.SourceRouter(self.data_dir).plan("某个没人注册的 topic")
        self.assertTrue(plan["specs"])

    def test_failure_demotes_source(self):
        r = ts.SourceRouter(self.data_dir)
        before = r.plan("美食")["primary"]
        for _ in range(5):
            r.mark(before, False)
        self.assertNotEqual(r.plan("美食")["primary"], before, "连挂 5 次应换主源")

    def test_success_keeps_source(self):
        r = ts.SourceRouter(self.data_dir)
        first = r.plan("美食")["primary"]
        for _ in range(3):
            r.mark(first, True)
        self.assertEqual(r.plan("美食")["primary"], first)

    def test_next_source_skips_tried(self):
        r = ts.SourceRouter(self.data_dir)
        plan = r.plan("美食")
        nxt = r.next_source("美食", [plan["primary"]])
        self.assertIsNotNone(nxt)
        self.assertNotEqual(nxt["platform"], plan["primary"])

    def test_next_source_exhausted(self):
        r = ts.SourceRouter(self.data_dir)
        allp = [s["platform"] for s in r.plan("美食")["specs"]]
        self.assertIsNone(r.next_source("美食", allp))

    def test_reset(self):
        r = ts.SourceRouter(self.data_dir)
        r.mark("小红书", False)
        r.reset()
        self.assertEqual(r.health(), {})


# ==================== trends.store ====================

SAMPLE_HTML = """
<html><head><style>body{}</style></head><body>
<div class="ad">广告位招商 联系电话 010-12345678</div>
<p>今年夏天的「多巴胺穿搭」真的火了，满屏都在刷，出圈速度惊人。</p>
<p>很多人开始尝试同款配色，评论区都在问链接，已经破防了。</p>
<p>摄影师说这个色调的关键在于高饱和撞色，绝绝子。</p>
<script>var a = 1;</script>
</body></html>
"""


class TestTrendStore(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.store = tstore.TrendStore(self.data_dir)

    def test_strip_html(self):
        text = tstore.strip_html(SAMPLE_HTML)
        self.assertNotIn("<p>", text)
        self.assertNotIn("<script>", text)
        self.assertIn("多巴胺穿搭", text)

    def test_buzzwords(self):
        words = tstore.buzzwords(SAMPLE_HTML)
        self.assertTrue(words)
        self.assertIn("多巴胺穿搭", words)

    def test_digest(self):
        points = tstore.digest(SAMPLE_HTML, topic="穿搭")
        self.assertTrue(points)
        self.assertLessEqual(len(points), 4)
        for p in points:
            self.assertLessEqual(len(p), 22)
        self.assertTrue(any("穿搭" in p for p in points))

    def test_digest_empty(self):
        self.assertEqual(tstore.digest(""), [])

    def test_digest_dedupes(self):
        raw = " ".join(["这件事火了，大家都在讨论。"] * 10)
        points = tstore.digest(raw)
        self.assertLessEqual(len(points), 2)

    def test_ingest(self):
        r = self.store.ingest(SAMPLE_HTML, topic="穿搭", source="小红书")
        self.assertGreater(r["added"], 0)

    def test_ingest_dedupe(self):
        self.store.ingest(SAMPLE_HTML, topic="穿搭")
        before = len(self.store._load()["items"])
        self.store.ingest(SAMPLE_HTML, topic="穿搭")
        self.assertEqual(len(self.store._load()["items"]), before, "重复入库应去重")

    def test_topics_and_by_topic(self):
        self.store.ingest(SAMPLE_HTML, topic="穿搭")
        self.assertIn("穿搭", self.store.topics())
        self.assertTrue(self.store.by_topic("穿搭"))

    def test_seasoning_within_budget(self):
        for i in range(6):
            self.store.ingest(f"第{i}个热点真的火了，大家都在刷屏讨论。", topic="穿搭")
        s = self.store.seasoning(["穿搭"])
        self.assertTrue(s)
        self.assertLessEqual(estimate_tokens(s),
                             schema.DEFAULT_INJECTION_BUDGET["趋势调味料"])

    def test_seasoning_no_data(self):
        self.assertEqual(self.store.seasoning(["穿搭"]), "")

    def test_seasoning_takes_topics_from_profile(self):
        self.store.ingest(SAMPLE_HTML, topic="穿搭")
        self.write_json("user_persona.json", dict(
            schema.user_persona_template(),
            互动偏好={"喜欢的话题": ["穿搭"], "反感的话题": [],
                      "回复长度偏好": "", "主动程度偏好": ""}))
        self.assertTrue(self.store.seasoning())

    def test_purge(self):
        self.store.ingest(SAMPLE_HTML, topic="穿搭")
        self.store.ingest(SAMPLE_HTML, topic="美食")
        self.assertGreater(self.store.purge("穿搭"), 0)
        self.assertNotIn("穿搭", self.store.topics())
        self.store.purge()
        self.assertEqual(self.store.topics(), [])


# ==================== multimodal ====================

class TestImagePlanner(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.planner = ip.ImagePlanner(self.data_dir)

    def test_gate_open_by_default(self):
        self.assertTrue(self.planner.gate()["ok"])

    def test_off_switch(self):
        p = ip.ImagePlanner(self.data_dir, {"开关": False})
        self.assertFalse(p.gate()["ok"])

    def test_cooldown(self):
        self.planner.mark_sent("日常", "随手拍的")
        verdict = self.planner.gate()
        self.assertFalse(verdict["ok"])
        self.assertIn("太近", verdict["reason"])

    def test_daily_cap(self):
        now = datetime.now()
        for _ in range(3):
            self.planner.mark_sent("日常", "x", now)
        self.assertFalse(self.planner.gate(now)["ok"])

    def test_tick_counts_turns(self):
        self.planner.mark_sent("日常", "x")
        for _ in range(6):
            self.planner.tick(False)
        self.assertTrue(self.planner.gate()["ok"])

    def test_style_from_mood(self):
        # 指定白天时刻：不传 now 会取当前时间，深夜跑测试会触发夜间 override 导致误报
        day = datetime.now().replace(hour=10)
        night_style = self.planner.style_for({}, "开心", day)
        self.assertIn("色调", night_style)
        self.assertIn("构图", night_style)
        self.assertIn("元素", night_style)
        self.assertIn("明亮", night_style["色调"])

    def test_style_night_overrides(self):
        now = datetime.now().replace(hour=23)
        style = self.planner.style_for({}, "日常", now)
        self.assertIn("夜", style["色调"])
        self.assertIn("夜", style["元素"])

    def test_style_from_care_style(self):
        """拍什么由 v1 的关心方式决定（不是「价值观 → 审美构图」那类通用路子）"""
        persona = {"相处模式": {"关心方式": "细节型关心，会注意你没说的小事"}}
        style = self.planner.style_for(persona, "日常")
        self.assertIn("细小事物", style["主体"])

    def test_intimacy_scale_limits_framing(self):
        low = self.planner.style_for({"亲密尺度": 1}, "日常")
        high = self.planner.style_for({"亲密尺度": 5}, "日常")
        self.assertEqual(low["拍摄距离"], "只拍物与景，不出现人物")
        self.assertEqual(high["拍摄距离"], "可出现完整人物，居家场景也行")

    def test_caption_in_budget(self):
        text = self.planner.caption("想念", {"语气词": ["呀"], "emoji频率": 0.9})
        self.assertTrue(text)
        self.assertLessEqual(estimate_tokens(text), ip._IMAGE_BUDGET)

    def test_caption_applies_correction(self):
        text = self.planner.caption("想念", corrections=[{"wrong": "随手", "right": "恰好"}])
        self.assertNotIn("随手", text)

    def test_plan_shape(self):
        out = self.planner.plan("美美", mood="想念", data_dir=self.data_dir)
        self.assertTrue(out["should"])
        self.assertIn("prompt_hint", out)
        self.assertIn("style", out)
        self.assertTrue(out["caption"])

    def test_plan_respects_gate(self):
        p = ip.ImagePlanner(self.data_dir, {"开关": False})
        self.assertFalse(p.plan("美美")["should"])

    def test_reset(self):
        self.planner.mark_sent("日常", "x")
        self.planner.reset()
        self.assertTrue(self.planner.gate()["ok"])


# ==================== panel.explain ====================

class TestExplainPanel(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.panel = pex.ExplainPanel(self.data_dir)
        from scripts.memory.store import MemoryStore
        self.mem = MemoryStore(self.data_dir)

    def test_build_evidence_matches_memory(self):
        self.mem.add("用户喜欢三分糖奶茶", "偏好")
        sections = {"记忆片段": "用户喜欢三分糖奶茶"}
        evidence = pex.build_evidence(sections, self.data_dir)
        self.assertTrue(any("三分糖" in c for c in evidence["记忆片段"]))

    def test_build_evidence_matches_persona(self):
        from scripts.persona.library import PersonaLibrary
        lib = PersonaLibrary(self.data_dir)
        lib.create({"姓名": "小美", "昵称": "美美", "声线": {"口头禅": ["想你了呀"]},
                    "思维": {}, "性格": {}})
        sections = {"人格指令": "口头禅：想你了呀"}
        evidence = pex.build_evidence(sections, self.data_dir, slug="美美")
        self.assertIn("声线.口头禅", evidence["人格指令"])

    def test_record_and_render(self):
        entry = self.panel.record({"记忆片段": "用户喜欢三分糖奶茶"})
        text = self.panel.render(entry)
        self.assertIn("记忆片段", text)
        self.assertIn("依据", text)

    def test_record_stores_no_reply_text(self):
        entry = self.panel.record({"记忆片段": "x"}, reply="这是一段很长的回复原文")
        self.assertNotIn("很长的回复原文", json.dumps(entry, ensure_ascii=False))
        self.assertEqual(entry["reply_chars"], len("这是一段很长的回复原文"))

    def test_latest(self):
        self.panel.record({"记忆片段": "a"})
        self.panel.record({"记忆片段": "b"})
        self.assertEqual(len(self.panel.latest(2)), 2)

    def test_render_latest_empty(self):
        self.assertIn("暂无", pex.ExplainPanel(self.data_dir).render_latest())

    def test_clear(self):
        self.panel.record({"记忆片段": "a"})
        self.assertGreater(self.panel.clear(), 0)


# ==================== panel.controls ====================

class TestControls(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.c = pctl.Controls(self.data_dir)

    def test_defaults(self):
        self.assertTrue(self.c.enabled("记忆系统"))
        self.assertFalse(self.c.enabled("趋势感知"), "趋势默认关闭")

    def test_toggle(self):
        self.c.toggle("趋势感知", True)
        self.assertTrue(self.c.enabled("趋势感知"))
        self.c.toggle("趋势感知")
        self.assertFalse(self.c.enabled("趋势感知"))

    def test_toggle_unknown_module(self):
        with self.assertRaises(KeyError):
            self.c.toggle("不存在的模块", True)

    def test_set_weight(self):
        self.c.set_weight("依恋类型.判断", 0.2)
        self.assertEqual(self.c.weight("依恋类型.判断"), 0.2)

    def test_weight_clamped(self):
        self.c.set_weight("大五人格.外向性", 5.0)
        self.assertEqual(self.c.weight("大五人格.外向性"), 1.0)
        self.c.set_weight("大五人格.外向性", -3.0)
        self.assertEqual(self.c.weight("大五人格.外向性"), 0.0)

    def test_apply_weights_drops_low_confidence(self):
        persona = schema.user_persona_template()
        persona["依恋类型"]["判断"] = "焦虑型"
        self.c.set_weight("依恋类型.判断", 0.1)
        marked = self.c.apply_weights(persona)
        self.assertEqual(marked["依恋类型"]["判断"], "", "权重过低应被标记存疑并置空")

    def test_apply_weights_keeps_original(self):
        persona = schema.user_persona_template()
        persona["依恋类型"]["判断"] = "焦虑型"
        self.c.set_weight("依恋类型.判断", 0.1)
        self.c.apply_weights(persona)
        self.assertEqual(persona["依恋类型"]["判断"], "焦虑型", "不得就地修改传入对象")

    def test_reset_weight(self):
        self.c.set_weight("依恋类型.判断", 0.2)
        self.assertTrue(self.c.reset_weight("依恋类型.判断"))
        self.assertIsNone(self.c.weight("依恋类型.判断"))

    def test_set_voice(self):
        self.c.set_voice("轻柔")
        self.assertEqual(self.c._load()["语气强度"], "轻柔")

    def test_set_voice_invalid(self):
        with self.assertRaises(KeyError):
            self.c.set_voice("超强")

    def test_forget_relation(self):
        from scripts.persona.library import PersonaLibrary
        from scripts.persona.mirror import MirrorModel
        from scripts.memory.store import MemoryStore

        PersonaLibrary(self.data_dir).create({"姓名": "小美", "昵称": "美美",
                                              "声线": {}, "思维": {}, "性格": {}})
        MirrorModel(self.data_dir).record("美美", "亲密")
        MemoryStore(self.data_dir).add("一起去看海", "共享事件", conversation_id="美美")

        result = self.c.forget("美美")
        self.assertEqual(result["persona"], 1)
        self.assertEqual(result["relation"], 1)
        self.assertEqual(result["memories"], 1)

    def test_forget_nonexistent(self):
        result = self.c.forget("不存在的人")
        self.assertEqual(result["persona"], 0)

    def test_status(self):
        status = self.c.status()
        self.assertIn("开启模块", status)
        self.assertIn("语气强度", status)

    def test_export_all(self):
        payload = json.loads(self.c.export_all())
        self.assertIn("settings", payload)
        self.assertIn("memory", payload)

    def test_purge_all(self):
        self.c.toggle("趋势感知", True)
        removed = self.c.purge_all()
        self.assertIn("settings.json", removed)


# ==================== pipeline 串联 ====================

class TestPipelineP1(TempDataMixin):
    def _run(self, kind, payload):
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle
        TaskQueue(self.data_dir).enqueue(kind, payload)
        report = run_idle(self.data_dir)
        self.assertEqual(report["done"], 1, f"{kind} 失败：{report['errors']}")
        queue = TaskQueue(self.data_dir)
        done = [t for t in queue.all() if t.get("status") == "done"]
        return (done[-1].get("result") or {})

    def test_trends_plan_task(self):
        result = self._run("trends.plan", {"topic": "美食"})
        self.assertTrue(result.get("primary"))

    def test_trends_plan_marks_failure(self):
        self._run("trends.plan", {"topic": "美食", "failed": "小红书"})
        health = ts.SourceRouter(self.data_dir).health()
        self.assertGreater(health.get("小红书", {}).get("fail", 0), 0)

    def test_trends_ingest_task(self):
        result = self._run("trends.ingest", {"raw": SAMPLE_HTML, "topic": "穿搭",
                                             "source": "小红书"})
        self.assertGreater(result.get("added", 0), 0)
        health = ts.SourceRouter(self.data_dir).health()
        self.assertGreater(health.get("小红书", {}).get("ok", 0), 0)

    def test_trends_ingest_marks_failure_on_empty(self):
        self._run("trends.ingest", {"raw": "!!!", "topic": "穿搭", "source": "B站"})
        health = ts.SourceRouter(self.data_dir).health()
        self.assertGreater(health.get("B站", {}).get("fail", 0), 0)

    def test_image_plan_task(self):
        result = self._run("image.plan", {"slug": "美美", "mood": "想念"})
        self.assertTrue(result.get("should"))
        self.assertTrue(result.get("caption"))

    def test_panel_explain_task(self):
        result = self._run("panel.explain", {"sections": {"记忆片段": "用户喜欢三分糖"},
                                             "slug": "美美"})
        self.assertTrue(result.get("ok"))
        self.assertIn("记忆片段", result.get("evidence", {}))


if __name__ == "__main__":
    unittest.main(verbosity=2)
