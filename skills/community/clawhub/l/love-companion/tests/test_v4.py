#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M3a / M5 / M6 回归测试

覆盖：
- persona.parser    三种导出排版、噪声过滤、隐私脱敏、素材指纹
- persona.extract   三层提取（声线/思维/性格）+ 5 层人格模型
- persona.library   CRUD、增量 merge、纠偏层、版本回滚、摘要编译预算
- persona.mirror    关系演化、共鸣、一致性自检、元认知反馈
- care.trigger      三道闸门 + 四类信号
- care.templates    话术生成、声线改写、纠偏生效、预算截断
- pipeline          四个新离线任务的端到端串联
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
from scripts.persona import parser, extract, library, mirror  # noqa: E402
from scripts.care import trigger as care_trigger  # noqa: E402
from scripts.care import templates as care_templates  # noqa: E402
from scripts.pipeline.injector import estimate_tokens  # noqa: E402


class TempDataMixin(unittest.TestCase):
    """每个用例独立数据目录，测试之间零污染"""

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


# ==================== parser ====================

class TestParser(unittest.TestCase):
    def test_colon_format(self):
        corpus = parser.parse_text("小美: 在吗\n小美: 想你了呀")
        self.assertEqual(len(corpus), 2)
        self.assertEqual(corpus[0]["speaker"], "小美")
        self.assertEqual(corpus[0]["text"], "在吗")

    def test_ts_then_speaker_format(self):
        raw = "2024-05-20 14:23:01 小美\n今天加班累死了\n2024-05-20 14:24:00 小美\n想吃点甜的"
        corpus = parser.parse_text(raw)
        self.assertEqual([u["speaker"] for u in corpus], ["小美", "小美"])
        self.assertEqual(corpus[0]["ts"], "2024-05-20 14:23:01")
        self.assertIn("加班", corpus[0]["text"])

    def test_speaker_then_ts_format(self):
        corpus = parser.parse_text("小美 2024/5/20 14:23\n在干嘛呢")
        self.assertEqual(corpus[0]["speaker"], "小美")
        self.assertIn("干嘛", corpus[0]["text"])

    def test_timestamp_colon_not_mistaken_for_speaker(self):
        """14:23 不能被当成说话人"""
        corpus = parser.parse_text("2024-05-20 14:23:01 小美\n在吗")
        self.assertEqual(corpus[0]["speaker"], "小美")

    def test_noise_dropped(self):
        corpus = parser.parse_text("小美: 在吗\n---\n对方撤回了一条消息\n小美: 好吧")
        self.assertEqual(len(corpus), 2)

    def test_privacy_redacted(self):
        corpus = parser.parse_text("小美: 我手机号 13812345678")
        self.assertNotIn("13812345678", corpus[0]["text"])
        self.assertIn("手机号", corpus[0]["redacted"])

    def test_fingerprint_stable(self):
        self.assertEqual(parser.fingerprint("abc"), parser.fingerprint("abc"))
        self.assertNotEqual(parser.fingerprint("abc"), parser.fingerprint("abd"))

    def test_csv(self):
        raw = "talker,content,createtime\n小美,在吗,2024-05-20 14:23:01\n小美,想你了,2024-05-20 14:24:00"
        corpus = parser.parse_csv(raw)
        self.assertEqual(len(corpus), 2)
        self.assertEqual(corpus[0]["speaker"], "小美")

    def test_json(self):
        raw = json.dumps([{"nickname": "小美", "content": "在吗", "time": "2024-05-20 14:23:01"}])
        corpus = parser.parse_json(raw)
        self.assertEqual(corpus[0]["speaker"], "小美")
        self.assertEqual(corpus[0]["text"], "在吗")

    def test_speakers_and_only(self):
        corpus = parser.parse_text("小美: 在吗\n我: 在\n小美: 想你了")
        stat = parser.speakers(corpus)
        self.assertEqual(stat["小美"], 2)
        self.assertEqual(len(parser.only(corpus, "小美")), 2)


# ==================== extract ====================

def _demo_corpus(repeat: int = 6) -> list:
    lines = [
        "小美: 在吗 想你了呀",
        "小美: 今天加班累死了 想吃点甜的～",
        "小美: 你定吧 我都行啦",
        "小美: 算了 不想说了",
        "小美: 宝贝晚安呀",
        "小美: 我就是说我觉得这个挺好的嘛",
    ]
    return parser.parse_text("\n".join(lines * repeat))


class TestExtract(unittest.TestCase):
    def setUp(self):
        self.corpus = parser.only(_demo_corpus(), "小美")

    def test_voice_extracted(self):
        voice = extract.extract_voice(self.corpus)
        self.assertTrue(voice["口头禅"], "应提取出口头禅")
        self.assertIn("想你了呀", voice["口头禅"])
        self.assertTrue(voice["语气词"], "应识别出句尾语气词")
        self.assertGreater(voice["平均句长"], 0)
        self.assertGreater(voice["置信度"], 0)

    def test_thinking_extracted(self):
        think = extract.extract_thinking(self.corpus)
        self.assertIn(think["决策逻辑"], ("依赖型", "直觉型", "权衡型", "果断型", "混合型"))
        self.assertTrue(think["关注顺序"])

    def test_character_extracted(self):
        char = extract.extract_character(self.corpus)
        self.assertIn(char["冲突应对"], ("回避", "妥协", "对抗", "冷战", "就事论事"))
        self.assertGreaterEqual(char["亲密度基线"], 0.2)
        self.assertLessEqual(char["亲密度基线"], 1.0)

    def test_persona_shape(self):
        p = extract.extract_persona(self.corpus, name="小美", nickname="美美")
        for key in ("声线", "思维", "性格"):
            self.assertIn(key, p)
        self.assertEqual(p["昵称"], "美美")
        self.assertEqual(p["语料量"], len(self.corpus))

    def test_empty_corpus_safe(self):
        for fn in (extract.extract_voice, extract.extract_thinking, extract.extract_character):
            self.assertIsInstance(fn([]), dict)

    def test_three_layers_map_to_v1_persona(self):
        """三层提取必须能回写进 v1 人设字段，而不是另立一套体系"""
        from scripts.persona.adapt import apply_to_v1, lover_card
        p = extract.extract_persona(self.corpus, name="小美", nickname="美美")
        v1 = apply_to_v1({}, p)
        for key in ("对话风格", "性格", "相处模式"):
            self.assertIn(key, v1)
        self.assertTrue(v1["对话风格"].get("口头禅"), "声线应映射到对话风格.口头禅")
        self.assertTrue(v1["性格"].get("核心特质"), "性格层应映射到性格.核心特质")

    def test_distill_never_touches_safety_fields(self):
        """亲密尺度 / 内容边界 / 称呼是用户显式设置，蒸馏无权改"""
        from scripts.persona.adapt import apply_to_v1
        base = {"亲密尺度": 2, "内容边界": ["不谈前任"], "对用户的称呼": "宝贝"}
        p = extract.extract_persona(self.corpus, name="小美")
        out = apply_to_v1(base, p)
        self.assertEqual(out["亲密尺度"], 2)
        self.assertEqual(out["内容边界"], ["不谈前任"])
        self.assertEqual(out["对用户的称呼"], "宝贝")

    def test_distill_does_not_overwrite_written_persona(self):
        """用户手写的对话风格不该被蒸馏结果覆盖（overwrite=False）"""
        from scripts.persona.adapt import apply_to_v1
        base = {"对话风格": {"语气": "手写的一句话", "口头禅": ["手写"], "语言习惯": ""}}
        p = extract.extract_persona(self.corpus, name="小美")
        out = apply_to_v1(base, p)
        self.assertEqual(out["对话风格"]["语气"], "手写的一句话")
        self.assertEqual(out["对话风格"]["口头禅"], ["手写"])

    def test_lover_card_from_v1_persona(self):
        from scripts.persona.adapt import lover_card
        v1 = {
            "姓名": "小晴", "对用户的称呼": "宝贝",
            "对话风格": {"语气": "句尾带呀", "口头禅": ["想我了吗"], "语言习惯": "短句连发"},
            "性格": {"核心特质": ["温柔"], "小脾气": ["闹别扭不说话"], "情绪表达": "外放"},
            "相处模式": {"主动程度": "高", "撒娇频率": "高", "关心方式": "细节型"},
            "亲密尺度": 3, "内容边界": ["不谈前任"],
        }
        card = lover_card(v1)
        self.assertIn("小晴", card)
        self.assertIn("宝贝", card)
        self.assertIn("亲密尺度 3", card)
        self.assertIn("不谈前任", card)
        self.assertLessEqual(estimate_tokens(card),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])

    def test_lover_card_within_budget(self):
        from scripts.persona.adapt import lover_card
        v1 = {"姓名": "小晴" * 30, "对用户的称呼": "宝贝" * 20,
              "对话风格": {"语气": "呀" * 50, "口头禅": ["测试"] * 20}}
        self.assertLessEqual(estimate_tokens(lover_card(v1)),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])


# ==================== library ====================

class TestLibrary(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.lib = library.PersonaLibrary(self.data_dir)
        self.persona = extract.extract_persona(
            parser.only(_demo_corpus(4), "小美"), name="小美", nickname="美美",
            source_prints=["abc123"])

    def test_create_and_get(self):
        self.lib.create(self.persona)
        self.assertTrue(self.lib.exists("美美"))
        self.assertEqual(self.lib.get("美美")["姓名"], "小美")

    def test_list(self):
        self.lib.create(self.persona)
        items = self.lib.list()
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["slug"], "美美")

    def test_create_twice_merges_not_overwrite(self):
        self.lib.create(self.persona)
        second = extract.extract_persona(
            parser.only(_demo_corpus(4), "小美"), name="小美", nickname="美美")
        self.lib.create(second)
        p = self.lib.get("美美")
        self.assertEqual(p["版本"], 2, "重复创建应走增量合并而非覆盖")
        self.assertEqual(p["语料量"], self.persona["语料量"] * 2)

    def test_merge_accumulates_fingerprints(self):
        self.lib.create(self.persona)
        second = extract.extract_persona(
            parser.only(_demo_corpus(2), "小美"), name="小美",
            source_prints=["def456"])
        self.lib.merge("美美", second)
        self.assertIn("abc123", self.lib.get("美美")["来源素材"])
        self.assertIn("def456", self.lib.get("美美")["来源素材"])

    def test_merge_list_union(self):
        self.lib.create(self.persona)
        before = set(self.lib.get("美美")["声线"]["口头禅"])
        other = extract.extract_persona(
            parser.parse_text("\n".join(["小美: 真的假的呀"] * 6)), name="小美")
        self.lib.merge("美美", other)
        after = set(self.lib.get("美美")["声线"]["口头禅"])
        self.assertTrue(before.issubset(after) or not before)

    def test_correction_applies_immediately(self):
        self.lib.create(self.persona)
        self.lib.correct("美美", "宝贝", "宝宝")
        self.assertEqual(len(self.lib.corrections("美美")), 1)
        self.assertEqual(self.lib.apply_corrections("宝贝晚安", self.lib.corrections("美美")),
                         "宝宝晚安")

    def test_correction_empty_right_removes(self):
        self.lib.create(self.persona)
        self.lib.correct("美美", "亲亲")
        self.assertEqual(self.lib.apply_corrections("亲亲你", self.lib.corrections("美美")), "你")

    def test_compile_summary_within_budget(self):
        self.lib.create(self.persona)
        summary = self.lib.compile_summary("美美")
        self.assertTrue(summary)
        self.assertLessEqual(estimate_tokens(summary),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])

    def test_compile_summary_huge_persona_still_within_budget(self):
        """口头禅塞满也不能突破预算"""
        self.lib.create(self.persona)
        p = self.lib.get("美美")
        p["声线"]["口头禅"] = ["测试口头禅"] * 50
        self.lib._write("美美", p)
        summary = self.lib.compile_summary("美美")
        self.assertLessEqual(estimate_tokens(summary),
                             schema.DEFAULT_INJECTION_BUDGET["人格指令"])

    def test_compile_summary_missing_persona(self):
        self.assertEqual(self.lib.compile_summary("不存在"), "")

    def test_versions_and_rollback(self):
        self.lib.create(self.persona)
        self.lib.correct("美美", "宝贝", "宝宝")
        versions = self.lib.versions("美美")
        self.assertTrue(versions)
        self.lib.rollback("美美", min(versions))
        self.assertEqual(self.lib.corrections("美美"), [], "回滚后纠偏应消失")

    def test_delete_keeps_versions(self):
        self.lib.create(self.persona)
        self.lib.delete("美美")
        self.assertFalse(self.lib.exists("美美"))
        self.assertTrue(self.lib.versions("美美"), "删除后历史版本应保留，便于找回")

    def test_purge_removes_everything(self):
        self.lib.create(self.persona)
        self.lib.purge("美美")
        self.assertFalse(self.lib.exists("美美"))
        self.assertEqual(self.lib.versions("美美"), [])

    def test_slugify(self):
        self.assertEqual(library.slugify("小美"), "小美")
        self.assertEqual(library.slugify("a b/c"), "a-b-c")
        self.assertTrue(library.slugify(""))


# ==================== mirror ====================

class TestMirror(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.lib = library.PersonaLibrary(self.data_dir)
        self.persona = extract.extract_persona(
            parser.only(_demo_corpus(4), "小美"), name="小美", nickname="美美")
        self.lib.create(self.persona)
        self.m = mirror.MirrorModel(self.data_dir)

    def test_record_and_intimacy_rises(self):
        # 先压下去再升温，避免基线本来就顶到 1.0（示例语料亲密度极高）
        for _ in range(4):
            self.m.record("美美", "冲突", note="吵了一架")
        low = self.m.intimacy("美美")
        for _ in range(8):
            self.m.record("美美", "亲密", note="聊了很久")
        self.assertGreater(self.m.intimacy("美美"), low)

    def test_conflict_lowers_intimacy(self):
        before = self.m.intimacy("美美")
        for _ in range(4):
            self.m.record("美美", "冲突", note="吵了一架")
        self.assertLess(self.m.intimacy("美美"), before)

    def test_intimacy_bounded(self):
        for _ in range(50):
            self.m.record("美美", "里程碑")
        self.assertLessEqual(self.m.intimacy("美美"), 1.0)
        for _ in range(80):
            self.m.record("美美", "冲突")
        self.assertGreaterEqual(self.m.intimacy("美美"), 0.0)

    def test_stage_progression(self):
        self.assertIn(self.m.stage("美美"), ("初识", "暧昧", "热恋", "稳定", "深度依恋", "倦怠", "修复"))
        for _ in range(30):
            self.m.record("美美", "里程碑")
        self.assertIn(self.m.stage("美美"), ("热恋", "稳定", "深度依恋"))

    def test_weary_stage_on_downward_trend(self):
        for _ in range(5):
            self.m.record("美美", "冷落")
        self.assertEqual(self.m.stage("美美"), "倦怠")

    def test_repair_stage(self):
        self.m.record("美美", "冲突")
        for _ in range(4):
            self.m.record("美美", "和解")
        self.assertEqual(self.m.stage("美美"), "修复")

    def test_face_shape(self):
        face = self.m.face("美美")
        for key in ("阶段", "亲密度", "称呼", "主动程度", "话题边界", "亲密度系数"):
            self.assertIn(key, face)

    def test_resonance_shape(self):
        res = self.m.resonance("美美")
        for key in ("共鸣话题", "可带话题", "雷区", "价值观交集", "置信度"):
            self.assertIn(key, res)

    def test_consistency_flags_correction(self):
        self.lib.correct("美美", "乖乖", "")
        ok, issues = self.m.consistency("乖乖，早点睡", "美美")
        self.assertFalse(ok)
        self.assertTrue(any("纠偏" in i for i in issues))

    def test_consistency_flags_content_boundary(self):
        """v1 人设的「内容边界」必须拦住回复"""
        p = self.lib.get("美美")
        p["v1人设"] = {"内容边界": ["不谈前任"]}
        self.lib._write("美美", p)
        ok, issues = self.m.consistency("你前任也不是那样吧", "美美")
        self.assertFalse(ok)
        self.assertTrue(any("内容边界" in i for i in issues))

    def test_consistency_flags_fabricated_memory(self):
        ok, issues = self.m.consistency("我们之前说过去看海的，你记得吗", "美美")
        self.assertFalse(ok)
        self.assertTrue(any("编造" in i for i in issues))

    def test_consistency_flags_emoji_overuse(self):
        p = self.lib.get("美美")
        p["声线"]["emoji频率"] = 0.0
        self.lib._write("美美", p)
        ok, issues = self.m.consistency("好呀🎉🎊✨", "美美")
        self.assertFalse(ok)
        self.assertTrue(any("emoji" in i for i in issues))

    def test_consistency_clean_reply(self):
        ok, issues = self.m.consistency("在吗", "美美")
        self.assertTrue(ok, f"不应误报：{issues}")

    def test_consistency_unknown_slug(self):
        ok, _ = self.m.consistency("在吗", "不存在")
        self.assertTrue(ok)

    def test_feedback_stats(self):
        self.assertEqual(self.m.feedback_stats("美美")["样本"], 0)
        for _ in range(4):
            self.m.feedback("美美", True)
        for _ in range(6):
            self.m.feedback("美美", False)
        stats = self.m.feedback_stats("美美")
        self.assertEqual(stats["好评率"], 0.4)
        self.assertNotIn("维持", stats["建议"], "好评率 0.4 不应给出『维持现状』的建议")

    def test_brief_within_budget(self):
        text = self.m.brief("美美", budget=60)
        self.assertLessEqual(estimate_tokens(text), 60)

    def test_clear(self):
        self.m.record("美美", "亲密")
        self.assertTrue(self.m.clear("美美"))
        self.assertEqual(self.m.intimacy("美美"), self.lib.get("美美")["性格"]["亲密度基线"])


# ==================== care trigger ====================

class TestCareTrigger(TempDataMixin):
    def test_off_switch(self):
        t = care_trigger.CareTrigger(self.data_dir, {"开关": False})
        self.assertFalse(t.evaluate()["should"])

    def test_silent_hours(self):
        now = datetime.now().replace(hour=3)
        t = care_trigger.CareTrigger(self.data_dir, {"静默时段": [3]})
        verdict = t.evaluate(now)
        self.assertFalse(verdict["should"])
        self.assertIn("静默", verdict["reason"])

    def test_daily_cap(self):
        # 显式指定时刻：否则测试在凌晨跑会被「静默时段」先拦下，测不到上限逻辑
        now = datetime.now().replace(hour=15)
        t = care_trigger.CareTrigger(self.data_dir, {"每日上限": 1, "冷却小时": 0})
        t.mark_sent("久未联系", now)
        verdict = t.evaluate(now)
        self.assertFalse(verdict["should"])
        self.assertIn("上限", verdict["reason"])

    def test_cooldown(self):
        now = datetime.now().replace(hour=15)
        t = care_trigger.CareTrigger(self.data_dir, {"冷却小时": 6})
        t.mark_sent("久未联系", now)
        self.assertFalse(t.evaluate(now)["should"])

    def test_user_prefers_low_proactivity(self):
        self.write_json("user_persona.json", dict(
            schema.user_persona_template(),
            互动偏好={"喜欢的话题": [], "反感的话题": [], "回复长度偏好": "", "主动程度偏好": "低"}))
        t = care_trigger.CareTrigger(self.data_dir)
        self.assertFalse(t.evaluate()["should"])

    def test_idle_signal(self):
        ts = (datetime.now().replace(hour=14)).isoformat(timespec="seconds")
        self.write_json("user_signals.json", [{"ts": ts, "emotion": None, "topics": []}])
        # 把最后发言时间推到 20 小时前
        import json as _json
        p = Path(self.data_dir) / "user_signals.json"
        old = datetime.now().replace(hour=14)
        from datetime import timedelta
        data = _json.loads(p.read_text(encoding="utf-8"))
        data[0]["ts"] = (old - timedelta(hours=20)).isoformat(timespec="seconds")
        p.write_text(_json.dumps(data, ensure_ascii=False), encoding="utf-8")

        t = care_trigger.CareTrigger(self.data_dir, {"久未联系小时": 10})
        verdict = t.evaluate(datetime.now().replace(hour=14))
        self.assertTrue(verdict["should"])
        self.assertEqual(verdict["kind"], "久未联系")

    def test_negative_emotion_signal(self):
        now = datetime.now().replace(hour=15)
        self.write_json("user_signals.json", [
            {"ts": now.isoformat(timespec="seconds"), "emotion": "疲惫", "topics": []}
            for _ in range(6)
        ])
        t = care_trigger.CareTrigger(self.data_dir)
        verdict = t.evaluate(now)
        self.assertTrue(verdict["should"])
        self.assertEqual(verdict["kind"], "低落陪伴")

    def test_milestone_signal(self):
        from scripts.memory.store import MemoryStore
        now = datetime.now().replace(hour=15)
        MemoryStore(self.data_dir).add(
            f"{now.year}-{now.month:02d}-{now.day:02d} 我们在一起一周年", "里程碑")
        t = care_trigger.CareTrigger(self.data_dir)
        verdict = t.evaluate(now)
        self.assertTrue(verdict["should"])
        self.assertEqual(verdict["kind"], "纪念日")

    def test_late_night_signal(self):
        now = datetime.now().replace(hour=23)
        t = care_trigger.CareTrigger(self.data_dir)
        verdict = t.evaluate(now)
        self.assertTrue(verdict["should"])
        self.assertEqual(verdict["kind"], "深夜晚安")

    def test_no_signal(self):
        now = datetime.now().replace(hour=15)
        t = care_trigger.CareTrigger(self.data_dir)
        self.assertFalse(t.evaluate(now)["should"])

    def test_reset(self):
        t = care_trigger.CareTrigger(self.data_dir)
        t.mark_sent("久未联系")
        t.reset()
        self.assertEqual(t._load_state()["count"], 0)


# ==================== care templates ====================

class TestCareTemplates(unittest.TestCase):
    def test_render_all_kinds(self):
        for kind in care_templates.TEMPLATES:
            text = care_templates.render(kind, nickname="小美", detail="你说过想去看海")
            self.assertTrue(text, f"{kind} 渲染为空")
            self.assertNotIn("{nick}", text)
            self.assertNotIn("{detail}", text)

    def test_render_within_budget(self):
        for kind in care_templates.TEMPLATES:
            text = care_templates.render(kind, nickname="小美", detail="你说过想去看海")
            self.assertLessEqual(estimate_tokens(text),
                                 schema.DEFAULT_INJECTION_BUDGET["关怀话术"])

    def test_render_no_nickname_has_no_dangling_punctuation(self):
        text = care_templates.render("深夜晚安", nickname="")
        self.assertFalse(text.startswith("，"))
        self.assertNotIn("，。", text)

    def test_voice_applied(self):
        text = care_templates.render("久未联系", nickname="小美",
                                     voice={"语气词": ["呀"], "emoji频率": 0.9, "口头禅": []})
        self.assertTrue(text.endswith("呀") or "🌙" in text)

    def test_emoji_not_added_when_persona_uses_none(self):
        text = care_templates.render("久未联系", nickname="小美",
                                     voice={"语气词": [], "emoji频率": 0.0, "口头禅": []})
        self.assertNotIn("🌙", text)

    def test_correction_applied(self):
        text = care_templates.render("低落陪伴", nickname="宝贝", detail="累",
                                     corrections=[{"wrong": "宝贝", "right": "宝宝"}])
        self.assertNotIn("宝贝", text)

    def test_short_preference_truncates(self):
        full = care_templates.render("低落陪伴", nickname="小美", detail="今天加班很累吧")
        short = care_templates.render("低落陪伴", nickname="小美", detail="今天加班很累吧",
                                      length_pref="短")
        self.assertLessEqual(len(short), len(full))

    def test_pick_template_stable_within_day(self):
        a = care_templates.pick_template("久未联系")
        b = care_templates.pick_template("久未联系")
        self.assertEqual(a, b)

    def test_unknown_kind_safe(self):
        # 未知类型返回空串（宁肯不发，也不发「在吗。」这种无意义话术）
        self.assertEqual(care_templates.render("不存在的类型", nickname="小美"), "")


# ==================== pipeline 串联 ====================

class TestPipelineIntegration(TempDataMixin):
    def test_persona_build_task(self):
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle

        queue = TaskQueue(self.data_dir)
        queue.enqueue("persona.build", {
            "name": "小美", "nickname": "美美", "speaker": "小美",
            "corpus": [{"speaker": "小美", "text": "在吗 想你了呀"},
                       {"speaker": "小美", "text": "你定吧 我都行啦"}],
        })
        report = run_idle(self.data_dir)
        self.assertEqual(report["done"], 1, f"任务失败：{report['errors']}")
        lib = library.PersonaLibrary(self.data_dir)
        self.assertTrue(lib.exists("美美"))

    def test_persona_correct_and_mirror_tasks(self):
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle

        lib = library.PersonaLibrary(self.data_dir)
        lib.create(extract.extract_persona(
            parser.only(_demo_corpus(3), "小美"), name="小美", nickname="美美"))

        queue = TaskQueue(self.data_dir)
        queue.enqueue("persona.correct", {"slug": "美美", "wrong": "宝贝", "right": "宝宝"})
        queue.enqueue("mirror.record", {"slug": "美美", "kind": "亲密", "note": "聊到深夜"})
        report = run_idle(self.data_dir)
        self.assertEqual(report["done"], 2, f"任务失败：{report['errors']}")
        self.assertEqual(lib.corrections("美美")[0]["right"], "宝宝")

    def test_care_evaluate_task(self):
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle

        # 用真实时钟往前推 20 小时造「久未联系」信号，避免测试依赖运行时刻
        from datetime import timedelta
        past = (datetime.now() - timedelta(hours=20)).isoformat(timespec="seconds")
        probe = datetime.now().replace(hour=15)
        self.write_json("user_signals.json", [{"ts": past, "emotion": None, "topics": []}])
        queue = TaskQueue(self.data_dir)
        queue.enqueue("care.evaluate", {"slug": "美美", "now": probe.isoformat()})
        report = run_idle(self.data_dir)
        self.assertEqual(report["done"], 1)

        tasks = queue.all()
        done = [t for t in tasks if t.get("status") == "done"]
        self.assertTrue(done)
        result = done[0].get("result") or {}
        self.assertTrue(result.get("text"), "应生成关怀话术")

    def test_unknown_task_kind_goes_to_failed(self):
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle

        TaskQueue(self.data_dir).enqueue("不存在的任务", {})
        report = run_idle(self.data_dir)
        self.assertEqual(report["skipped"], 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
