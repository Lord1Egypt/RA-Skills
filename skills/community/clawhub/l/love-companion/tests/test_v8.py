#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v2 排查补充用例（test_v8）——覆盖现网 272 项回归没碰到的核心路径

本文件固定的是排查整改后的行为：
- 数据文件损坏 → 模块降级为空数据并留证，绝不抛异常
- settings.json 的「注入预算」「衰减参数」「隐私.采集开关」真实生效
- 蒸馏回填 v1 后，句式描述在卡片里只出现一次
- 未知关怀类型不产出「在吗。」这种无意义话术
- 全新用户（空数据目录）首轮全流程不崩、不注入空壳内容

运行：python -m unittest discover -s tests -t .
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.care import templates as care_templates          # noqa: E402
from scripts.memory.store import MemoryStore                  # noqa: E402
from scripts.panel.controls import Controls                   # noqa: E402
from scripts.persona.adapt import lover_card                   # noqa: E402
from scripts.persona.mirror import MirrorModel                 # noqa: E402
from scripts.pipeline.orchestrator import Session              # noqa: E402
from scripts.trends.store import TrendStore                    # noqa: E402
from scripts.user.profile import UserProfileStore              # noqa: E402

BROKEN = "{ 这不是合法 JSON "


class TempDataMixin(unittest.TestCase):
    def setUp(self):
        self._old = os.environ.get("LOVE_COMPANION_DATA_DIR")
        self.tmp = tempfile.mkdtemp(prefix="lc_v8_")
        self.data_dir = self.tmp
        # 合规闸门默认未确认；测试环境统一视为已确认成年人
        Path(self.tmp, "settings.json").write_text(
            json.dumps({"合规": {"已满18周岁确认": True}}), encoding="utf-8")

    def tearDown(self):
        if self._old is None:
            os.environ.pop("LOVE_COMPANION_DATA_DIR", None)
        else:
            os.environ["LOVE_COMPANION_DATA_DIR"] = self._old

    def break_file(self, name: str) -> None:
        (Path(self.data_dir) / name).write_text(BROKEN, encoding="utf-8")


class TestCorruptedDataResilience(TempDataMixin):
    """数据文件损坏时，各模块降级为空数据而不是抛异常"""

    def test_memory_json_broken(self):
        self.break_file("memory.json")
        self.assertEqual(MemoryStore(self.data_dir).all(), [])

    def test_relations_json_broken(self):
        self.break_file("relations.json")
        self.assertIsInstance(MirrorModel(self.data_dir).intimacy("任意"), float)

    def test_trends_json_broken(self):
        self.break_file("trends.json")
        self.assertEqual(TrendStore(self.data_dir).topics(), [])

    def test_settings_json_broken(self):
        self.break_file("settings.json")
        self.assertIsInstance(Controls(self.data_dir).switches(), dict)

    def test_user_persona_json_broken(self):
        self.break_file("user_persona.json")
        self.assertIsInstance(UserProfileStore(self.data_dir).get(), dict)

    def test_care_state_json_broken(self):
        self.break_file("care_state.json")
        from scripts.care.trigger import CareTrigger
        self.assertIsInstance(
            CareTrigger(self.data_dir).evaluate().get("should"), bool)

    def test_broken_file_is_quarantined(self):
        """损坏文件会被复制为 .bad-<时间戳> 留证，不悄悄吞掉"""
        self.break_file("memory.json")
        MemoryStore(self.data_dir).all()
        bad = list(Path(self.data_dir).glob("memory.json.bad-*"))
        self.assertTrue(bad, "坏文件应留证")

    def test_write_is_atomic_no_tmp_left(self):
        """原子写完成后目录里不残留临时文件"""
        MemoryStore(self.data_dir).add("喜欢三分糖", "偏好")
        leftovers = [p.name for p in Path(self.data_dir).glob(".*.tmp")]
        self.assertEqual(leftovers, [])

    def test_session_survives_all_broken(self):
        """最坏情况：所有数据文件同时损坏，一轮对话仍要能开场"""
        for name in ("memory.json", "relations.json", "trends.json",
                     "settings.json", "user_persona.json", "user_signals.json",
                     "care_state.json", "explanations.json", "multimodal.json"):
            self.break_file(name)
        pre = Session(data_dir=self.data_dir, slug="").prepare("你好")
        self.assertIsInstance(pre.get("render"), str)
        self.assertLessEqual(pre["total_tokens"], 500)


class TestSettingsTakeEffect(TempDataMixin):
    """settings.json 的旋钮真实生效（排查缺陷 2 的回归）"""

    def test_decay_params_from_settings(self):
        from datetime import datetime
        st = MemoryStore(self.data_dir)
        st.add("喜欢三分糖", "偏好", importance=1.0)
        # 把记忆的时间戳改到 100 天前，然后把半衰期调到 365 天
        memories = st.all()
        for m in memories:
            m["updated_at"] = "2026-06-01T00:00:00"
            m["created_at"] = "2026-06-01T00:00:00"
        st._save(memories)
        Path(self.data_dir, "settings.json").write_text(
            json.dumps({"衰减参数": {"half_life_days": 365},
                        "合规": {"已满18周岁确认": True}}), encoding="utf-8")
        st.decay(now=datetime(2026, 9, 20))
        imp = st.all()[0]["importance"]
        # 半衰期 365 天时 100 天只衰减到 ~0.83；若还是常量 30 天会掉到 ~0.1
        self.assertGreater(imp, 0.6, f"settings 里的半衰期没生效：{imp}")

    def test_injection_budget_from_settings(self):
        Path(self.data_dir, "settings.json").write_text(
            json.dumps({"注入预算": {"合计上限": 100},
                        "合规": {"已满18周岁确认": True}}), encoding="utf-8")
        pre = Session(data_dir=self.data_dir, slug="").prepare("你好" * 200)
        self.assertLessEqual(pre["total_tokens"], 100,
                             f"settings 里的总预算没生效：{pre['total_tokens']}")

    def test_collection_switch_off(self):
        Path(self.data_dir, "settings.json").write_text(
            json.dumps({"隐私": {"采集开关": False},
                        "合规": {"已满18周岁确认": True}}), encoding="utf-8")
        from scripts.pipeline.queue import TaskQueue
        from scripts.pipeline.runner import run_idle
        TaskQueue(self.data_dir).enqueue("memory.extract", {"text": "我喜欢三分糖"})
        report = run_idle(self.data_dir)
        self.assertEqual(report["done"], 1)
        self.assertEqual(MemoryStore(self.data_dir).all(), [],
                         "采集开关关闭后不应写入任何记忆")


class TestAgeGate(TempDataMixin):
    """合规闸门（v2.1）：未确认年满 18 周岁前不注入任何恋人上下文"""

    def test_unconfirmed_returns_notice_only(self):
        # 删掉 setUp 预写的确认设置 → 深合并回默认 False
        (Path(self.data_dir) / "settings.json").unlink()
        pre = Session(data_dir=self.data_dir, slug="").prepare("今天好累")
        self.assertTrue(pre.get("age_gate"))
        self.assertEqual(pre["sections"], {})
        self.assertEqual(pre["total_tokens"], 0)
        self.assertIn("18", pre["render"])
        self.assertNotIn("记忆", pre["sections"])

    def test_confirmed_injects_normally(self):
        # setUp 已写入已确认，行为应与闸门上线前一致
        pre = Session(data_dir=self.data_dir, slug="").prepare("今天好累")
        self.assertFalse(pre.get("age_gate", False))


class TestNoDuplicateInLoverCard(unittest.TestCase):
    """蒸馏回填 v1 后，同一句描述不会被写进两个字段"""

    def test_tone_and_habit_do_not_repeat(self):
        persona = {
            "对话风格": {
                "语气": "句尾常带呀、啦；短句连发，一条消息一句话",
                "语言习惯": "几乎不用表情",
            }
        }
        card = lover_card(persona, budget=100)
        self.assertEqual(card.count("短句连发"), 1,
                         f"同一描述重复出现，浪费预算：{card}")

    def test_distilled_shape_not_written_twice(self):
        """从声线蒸馏一次，回填后句式描述在 v1 里只能落地一次"""
        from scripts.persona import adapt
        voice = {"语气词": ["呀", "啦"], "句式": "短句连发，一条消息一句话",
                 "平均句长": 8, "emoji频率": 0.0, "标点习惯": "~～"}
        v1 = adapt.apply_to_v1({}, {"声线": voice, "思维": {}, "性格": {}})
        style = v1.get("对话风格") or {}
        joined = "；".join(str(style.get(k) or "") for k in ("语气", "语言习惯"))
        self.assertEqual(joined.count("短句连发"), 1,
                         f"句式描述被写进了两个字段：{joined}")

    def test_shape_derived_from_avg_len_when_missing(self):
        """句式缺失时按平均句长推导，仍然只落在「语气」一处"""
        from scripts.persona import adapt
        voice = {"平均句长": 8, "emoji频率": 0.0}
        v1 = adapt.apply_to_v1({}, {"声线": voice, "思维": {}, "性格": {}})
        style = v1.get("对话风格") or {}
        self.assertIn("短句连发", str(style.get("语气") or ""))
        self.assertNotIn("短句连发", str(style.get("语言习惯") or ""))


class TestUnknownCareKind(unittest.TestCase):
    """未知关怀类型：宁肯不发，不发无意义话术"""

    def test_unknown_kind_is_empty(self):
        self.assertEqual(care_templates.render("不存在的类型", nickname=""), "")

    def test_empty_kind_is_empty(self):
        self.assertEqual(care_templates.render("", nickname="小美"), "")

    def test_compose_unknown_kind_returns_empty_text(self):
        out = care_templates.compose("不存在的类型", "小美", data_dir=None)
        self.assertEqual(out["text"], "")


class TestFreshUserFullLoop(TempDataMixin):
    """全新用户（空数据目录）首轮全流程不崩，且不注入空壳内容"""

    def test_prepare_after_reply_proactive(self):
        s = Session(data_dir=self.data_dir, slug="")
        pre = s.prepare("你好")
        self.assertIsInstance(pre["render"], str)
        self.assertLessEqual(pre["total_tokens"], 500)
        # 没配过人设时不该注入「主动程度：中；亲密尺度 3」这类默认值噪音
        self.assertNotIn("亲密尺度", pre["render"])
        out = s.after_reply("嗨呀，在呢～", "你好")
        self.assertIsInstance(out, dict)
        self.assertIsInstance(s.proactive(), dict)

    def test_first_round_never_exceeds_budget(self):
        s = Session(data_dir=self.data_dir, slug="")
        pre = s.prepare("我最近好累，想吃点甜的" * 20)
        self.assertLessEqual(pre["total_tokens"], 500)


class TestDataSovereigntyAfterPurge(TempDataMixin):
    """一键清除后磁盘上不该残留可被读回的记忆"""

    def test_purge_leaves_no_readable_memories(self):
        st = MemoryStore(self.data_dir)
        st.add("喜欢三分糖", "偏好")
        st.add("生日 5 月 20", "事实")
        self.assertEqual(len(st.all()), 2)
        st.clear()
        self.assertEqual(MemoryStore(self.data_dir).all(), [])

    def test_export_is_valid_json_after_roundtrip(self):
        st = MemoryStore(self.data_dir)
        st.add("喜欢三分糖", "偏好")
        dumped = json.loads(st.export())
        self.assertTrue(isinstance(dumped, list) and dumped)


class TestCliSmoke(TempDataMixin):
    """带 __main__ 的模块抽样直跑不崩（排查缺陷 5 的回归）"""

    def _run(self, rel: str, *args: str) -> None:
        env = dict(os.environ, LOVE_COMPANION_DATA_DIR=self.data_dir,
                   PYTHONIOENCODING="utf-8")
        r = subprocess.run([sys.executable, rel, *args], cwd=str(ROOT),
                           env=env, capture_output=True, timeout=60)
        self.assertEqual(r.returncode, 0,
                         f"{rel} 直跑失败：{r.stderr.decode('utf-8', 'replace')[-300:]}")

    def test_storage_modules(self):
        self._run("scripts/memory/store.py", "stats")
        self._run("scripts/persona/library.py", "list")
        self._run("scripts/trends/store.py", "digest")

    def test_entry_points(self):
        self._run("scripts/pipeline/orchestrator.py", "--status")
        self._run("scripts/panel/controls.py", "status")


if __name__ == "__main__":
    unittest.main(verbosity=2)
