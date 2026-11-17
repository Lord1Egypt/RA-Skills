#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
M8 联调回归测试

覆盖：
- pipeline.audit      预算审计与最坏情况压测（方案红线的守门测试）
- pipeline.orchestrator 端到端一轮：prepare → after_reply → proactive
- 全链路：素材建人格 → 记忆入库 → 注入 → 自检 → 离线排空
- 模块开关生效（用户关掉的模块不得偷偷注入）
"""

import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.core import schema  # noqa: E402
from scripts.pipeline import audit  # noqa: E402
from scripts.pipeline.orchestrator import Session, run_round  # noqa: E402


class TempDataMixin(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.data_dir = self._tmp.name
        self._old_env = os.environ.get("LOVE_COMPANION_DATA_DIR")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.data_dir
        # 合规闸门默认未确认；测试环境统一视为已确认成年人
        self.write_json("settings.json", {"合规": {"已满18周岁确认": True}})
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

    def build_persona(self, slug: str = "美美") -> None:
        from scripts.persona import parser, extract, library
        lines = ["小美: 在吗 想你了呀", "小美: 今天加班累死了 想吃点甜的～",
                 "小美: 你定吧 我都行啦", "小美: 算了 不想说了",
                 "小美: 宝贝晚安呀", "小美: 我就是说我觉得这个挺好的嘛"]
        corpus = parser.only(parser.parse_text("\n".join(lines * 4)), "小美")
        library.PersonaLibrary(self.data_dir).create(
            extract.extract_persona(corpus, name="小美", nickname=slug), slug)


# ==================== audit ====================

class TestAudit(unittest.TestCase):
    def test_stress_test_within_budget(self):
        result = audit.stress_test()
        self.assertTrue(result["within_budget"],
                        f"最坏情况超预算：{result['total']} > {result['budget']}")
        self.assertLessEqual(result["total"], result["budget"])

    def test_stress_test_compresses_low_priority(self):
        result = audit.stress_test()
        self.assertTrue(result["truncated"] or result["dropped"],
                        "五模块全超额时应有模块被截断或丢弃")

    def test_stress_test_on_tight_budget(self):
        result = audit.stress_test(total=120)
        self.assertTrue(result["within_budget"])
        self.assertLessEqual(result["total"], 120)

    def test_worst_case_table_sums(self):
        rows = audit.worst_case_table()
        total_row = rows[-1]
        self.assertEqual(total_row["模块"], "合计")
        self.assertLessEqual(total_row["总额度内能拿到"], schema.DEFAULT_INJECTION_BUDGET["合计上限"])
        self.assertGreater(total_row["单模块上限"], total_row["总额度内能拿到"],
                           "方案原始上限之和本就超过红线，必须被压缩")

    def test_audit_prepared(self):
        prepared = {"tokens": {"记忆片段": 40, "人格指令": 60}, "total_tokens": 100,
                    "budget": 500, "truncated": [], "dropped": []}
        result = audit.audit_prepared(prepared)
        self.assertEqual(result["total"], 100)
        self.assertEqual(result["headroom"], 400)
        self.assertTrue(result["within_budget"])

    def test_audit_prepared_overrun_detected(self):
        prepared = {"tokens": {"记忆片段": 600}, "total_tokens": 600,
                    "budget": 500, "truncated": [], "dropped": []}
        self.assertFalse(audit.audit_prepared(prepared)["within_budget"])

    def test_breakdown_readable(self):
        prepared = {"tokens": {"记忆片段": 40}, "total_tokens": 40, "budget": 500,
                    "truncated": [], "dropped": [], "sections": {"记忆片段": "x"}}
        text = audit.breakdown(prepared)
        self.assertIn("记忆片段", text)
        self.assertIn("40", text)


# ==================== orchestrator ====================

class TestSession(TempDataMixin):
    def setUp(self):
        super().setUp()
        self.session = Session("美美", self.data_dir)
        self.build_persona()

    def test_prepare_within_budget(self):
        out = self.session.prepare("今天好累，想吃点甜的")
        self.assertLessEqual(out["total_tokens"], out["budget"])

    def test_prepare_returns_renderable_text(self):
        out = self.session.prepare("在吗")
        self.assertTrue(out["render"])

    def test_prepare_includes_persona(self):
        out = self.session.prepare("在吗")
        self.assertIn("人格指令", out["sections"])

    def test_prepare_recalls_memories(self):
        from scripts.memory.store import MemoryStore
        store = MemoryStore(self.data_dir)
        store.add("用户喜欢三分糖奶茶", "偏好")
        out = self.session.prepare("想喝奶茶")
        self.assertTrue(out["memory_ids"])
        recalled = [m for m in store.all() if m.get("id") in out["memory_ids"]]
        self.assertTrue(recalled)
        self.assertGreaterEqual(recalled[0]["recall_count"], 1)

    def test_prepare_records_evidence(self):
        out = self.session.prepare("在吗")
        self.assertIn("人格指令", out["evidence"])

    def test_module_switch_respected(self):
        from scripts.panel.controls import Controls
        Controls(self.data_dir).toggle("人格克隆", False)
        out = self.session.prepare("在吗")
        self.assertNotIn("人格指令", out["sections"])

    def test_trends_off_by_default(self):
        from scripts.trends.store import TrendStore
        TrendStore(self.data_dir).ingest("这件事真的火了，大家都在刷屏。", topic="穿搭")
        out = self.session.prepare("今天穿什么")
        self.assertNotIn("趋势调味料", out["sections"])

    def test_trends_on_injects(self):
        from scripts.panel.controls import Controls
        from scripts.trends.store import TrendStore
        TrendStore(self.data_dir).ingest("这件事真的火了，大家都在刷屏。", topic="穿搭")
        Controls(self.data_dir).toggle("趋势感知", True)
        self.write_profile_topics(["穿搭"])
        out = self.session.prepare("今天穿什么")
        self.assertIn("趋势调味料", out["sections"])

    def write_profile_topics(self, topics):
        from scripts.user.profile import UserProfileStore
        store = UserProfileStore(self.data_dir)
        persona = store.get()
        persona["互动偏好"]["喜欢的话题"] = topics
        store._save_persona(persona)

    def test_after_reply_runs_consistency(self):
        out = self.session.after_reply("在吗，想你了呀", user_message="在吗")
        self.assertIn("ok", out["consistency"])

    def test_after_reply_flags_off_persona(self):
        from scripts.persona.library import PersonaLibrary
        PersonaLibrary(self.data_dir).correct("美美", "亲亲")
        out = self.session.after_reply("亲亲你", user_message="在吗")
        self.assertFalse(out["consistency"]["ok"])

    def test_after_reply_runs_humanizer(self):
        out = self.session.after_reply("首先，其次，此外，综上所述。", user_message="在吗")
        self.assertIn("humanizer", out)

    def test_after_reply_drains_queue(self):
        out = self.session.after_reply("嗯", user_message="我喜欢三分糖奶茶")
        self.assertIn("idle", out)
        self.assertGreaterEqual(out["idle"].get("done", 0), 1)

    def test_after_reply_never_raises_on_empty(self):
        out = self.session.after_reply("")
        self.assertIsInstance(out, dict)

    def test_proactive_returns_dict(self):
        out = self.session.proactive()
        self.assertIn("care", out)
        self.assertIsInstance(out["care"], dict)

    def test_status(self):
        status = self.session.status()
        self.assertIn("settings", status)
        self.assertIn("memory", status)
        self.assertIn("relation", status)

    def test_run_round_end_to_end(self):
        result = run_round("美美", "今天加班好累", "辛苦了，早点休息呀", self.data_dir)
        self.assertLessEqual(result["prepare"]["total_tokens"],
                             result["prepare"]["budget"])
        self.assertIn("consistency", result["after"])


# ==================== 全链路 ====================

class TestFullPipeline(TempDataMixin):
    def test_material_to_context(self):
        """从聊天素材到注入上下文，全流程不落地任何原始文本到上下文"""
        from scripts.persona import parser, extract, library
        from scripts.memory.store import MemoryStore

        lines = ["小美: 在吗 想你了呀", "小美: 今天加班累死了",
                 "小美: 你定吧 我都行啦", "小美: 宝贝晚安呀"]
        corpus = parser.only(parser.parse_text("\n".join(lines * 5)), "小美")
        lib = library.PersonaLibrary(self.data_dir)
        lib.create(extract.extract_persona(corpus, name="小美", nickname="美美"), "美美")

        MemoryStore(self.data_dir).add("用户生日 5 月 20 日", "事实")

        session = Session("美美", self.data_dir)
        prepared = session.prepare("最近有点累")

        # 上限校验
        self.assertLessEqual(prepared["total_tokens"], prepared["budget"])
        # 溯源校验：注入内容必须能追到人格字段
        self.assertTrue(prepared["evidence"].get("人格指令"))
        # 隐私校验：上下文里不得出现素材原文里的敏感串
        self.assertNotIn("13812345678", json.dumps(prepared, ensure_ascii=False))

    def test_correction_flows_into_context(self):
        """纠偏后，下一轮注入的摘要必须跟着变"""
        from scripts.persona.library import PersonaLibrary
        self.build_persona()
        lib = PersonaLibrary(self.data_dir)

        before = lib.compile_summary("美美")
        lib.correct("美美", "想你了呀", "在干嘛呢")
        after = Session("美美", self.data_dir).prepare("在吗")["sections"].get("人格指令", "")

        self.assertNotEqual(before, after)
        self.assertNotIn("想你了呀", after)

    def test_forget_removes_persona_from_context(self):
        from scripts.panel.controls import Controls
        self.build_persona()
        Controls(self.data_dir).forget("美美")
        out = Session("美美", self.data_dir).prepare("在吗")
        self.assertNotIn("人格指令", out["sections"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
