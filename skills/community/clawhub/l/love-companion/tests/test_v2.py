#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
v2 模块回归测试：M1 离线管线 / 注入器，M2 记忆系统

运行：
    python tests/test_v2.py
    python -m unittest discover tests
"""

import json
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from scripts.core import schema, privacy  # noqa: E402
from scripts.pipeline.queue import TaskQueue  # noqa: E402
from scripts.pipeline.injector import Injector, estimate_tokens, truncate_to_tokens  # noqa: E402
from scripts.pipeline import runner  # noqa: E402
from scripts.memory.store import MemoryStore  # noqa: E402
from scripts.memory.extract import extract_memories  # noqa: E402
from scripts.memory.retrieve import top_k, render, score_entry  # noqa: E402


class PrivacyTests(unittest.TestCase):
    def test_masks_phone_and_email(self):
        text, hits = privacy.filter_text("我叫小明，手机 13812345678，邮箱 a@b.com")
        self.assertNotIn("13812345678", text)
        self.assertNotIn("a@b.com", text)
        self.assertIn("手机号", hits)
        self.assertIn("邮箱", hits)

    def test_has_sensitive(self):
        self.assertTrue(privacy.has_sensitive("我的卡号 6222021234567890123"))
        self.assertFalse(privacy.has_sensitive("我喜欢三分糖奶茶"))


class QueueTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lc_v2_")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.tmp
        self.q = TaskQueue(self.tmp)

    def test_enqueue_and_pending_order(self):
        self.q.enqueue("a.kind", {"x": 1}, priority=9)
        tid = self.q.enqueue("b.kind", {"x": 2}, priority=1)
        pending = self.q.pending()
        self.assertEqual(pending[0]["id"], tid, "优先级小的应先执行")

    def test_claim_complete(self):
        tid = self.q.enqueue("kind", {})
        self.assertIsNotNone(self.q.claim(tid))
        self.assertTrue(self.q.complete(tid, {"ok": True}))
        self.assertEqual(self.q._load(tid)["status"], "done")
        self.assertEqual(len(self.q.pending()), 0)

    def test_retry_then_dead(self):
        tid = self.q.enqueue("kind", {}, max_attempts=2)
        self.q.claim(tid)
        self.q.fail(tid, "boom")
        self.assertEqual(self.q._load(tid)["status"], "pending", "未达上限应放回队列")
        self.q.claim(tid)
        self.q.fail(tid, "boom again")
        self.assertEqual(self.q._load(tid)["status"], "dead")

    def test_stats(self):
        self.q.enqueue("k", {})
        self.assertIn("pending", self.q.stats())


class InjectorTests(unittest.TestCase):
    def test_estimate_tokens_cjk_is_conservative(self):
        self.assertGreaterEqual(estimate_tokens("你好世界"), 4)
        self.assertEqual(estimate_tokens(""), 0)

    def test_truncate(self):
        text = "你" * 1000
        out = truncate_to_tokens(text, 50)
        self.assertLessEqual(estimate_tokens(out), 50)

    def test_budget_is_hard_constraint(self):
        inj = Injector(total_budget=500)
        for key in schema.INJECTION_PRIORITY:
            inj.add(key, "内容" * 400)  # 每段都远超上限
        built = inj.build()
        self.assertLessEqual(built["total_tokens"], 500, "总预算是硬约束")
        self.assertTrue(built["truncated"], "超限应被截断")

    def test_low_priority_dropped_when_budget_exhausted(self):
        inj = Injector(total_budget=500)
        inj.add("相处指南", "指" * 200)
        inj.add("记忆片段", "记" * 150)
        inj.add("人格指令", "人" * 100)
        inj.add("关怀话术", "关" * 80)
        inj.add("趋势调味料", "趋" * 50)
        built = inj.build()
        self.assertEqual(built["sections"].get("趋势调味料"), None,
                         "预算被前面吃满时最低优先级应被丢弃")

    def test_render_contains_sections(self):
        inj = Injector()
        inj.add("记忆片段", "用户喜欢三分糖奶茶")
        text = inj.render()
        self.assertIn("记忆片段", text)
        self.assertIn("三分糖奶茶", text)


class RunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lc_v2_")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.tmp

    def test_unknown_kind_is_skipped(self):
        TaskQueue(self.tmp).enqueue("no.such.kind", {})
        report = runner.run_idle(self.tmp)
        self.assertEqual(report["skipped"], 1)
        self.assertEqual(report["done"], 0)

    def test_memory_extract_task_end_to_end(self):
        q = TaskQueue(self.tmp)
        q.enqueue("memory.extract", {"text": "我叫小明，我喜欢三分糖奶茶", "conversation_id": "c1"})
        report = runner.run_idle(self.tmp)
        self.assertEqual(report["done"], 1, report["errors"])
        store = MemoryStore(self.tmp)
        self.assertGreaterEqual(len(store.all()), 2)
        self.assertTrue(any("三分糖" in str(m["content"]) for m in store.all()))

    def test_max_tasks_limit(self):
        q = TaskQueue(self.tmp)
        for _ in range(5):
            q.enqueue("no.such.kind", {})
        report = runner.run_idle(self.tmp, max_tasks=2)
        self.assertEqual(report["picked"], 0)
        self.assertEqual(report["skipped"], 2, "单次调用应受 max_tasks 限制")


class MemoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lc_v2_")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.tmp
        self.store = MemoryStore(self.tmp)

    def test_add_and_types(self):
        e = self.store.add("用户生日 5 月 20 日", "事实", importance=0.8)
        self.assertEqual(e["type"], "事实")
        self.assertEqual(len(self.store.by_type("事实")), 1)

    def test_dedup(self):
        self.store.add("喜欢三分糖奶茶", "偏好")
        self.store.add("喜欢三分糖奶茶", "偏好")
        self.assertEqual(len(self.store.all()), 1)

    def test_v1_manager_can_read_v2_memories(self):
        """向下兼容：v1 的 manager 仍能读 v2 记忆"""
        self.store.add("喜欢三分糖奶茶", "偏好")
        import manager as v1
        v1mgr = v1.LoveCompanionManager(storage_path=self.tmp)
        memories = v1mgr.get_memories()
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0]["content"], "喜欢三分糖奶茶")

    def test_data_sovereignty(self):
        self.store.add("记忆A", "事实")
        self.store.add("记忆B", "情绪")
        self.store.add("会话记忆", "共享事件", conversation_id="c9")
        self.assertTrue(self.store.delete(1))
        self.assertEqual(self.store.delete_keyword("记忆B"), 1)
        self.assertEqual(self.store.delete_conversation("c9"), 1)
        self.assertEqual(len(self.store.all()), 0)
        self.store.add("再记一条", "事实")
        self.assertEqual(self.store.clear(), 1)

    def test_export(self):
        self.store.add("可导出", "事实")
        data = json.loads(self.store.export())
        self.assertEqual(len(data), 1)

    def test_recall_boosts_importance(self):
        e = self.store.add("会被召回", "事实", importance=0.5)
        before = self.store.get(e["id"])["importance"]
        self.store.recall([e["id"]])
        after = self.store.get(e["id"])["importance"]
        self.assertGreater(after, before)
        self.assertEqual(self.store.get(e["id"])["recall_count"], 1)

    def test_decay_lowers_importance(self):
        e = self.store.add("会衰减", "事实", importance=0.8)
        store = MemoryStore(self.tmp)
        memories = store.all()
        for m in memories:
            m["updated_at"] = (datetime.now() - timedelta(days=30)).isoformat(timespec="seconds")
        store._save(memories)
        self.assertGreater(store.decay(), 0)
        self.assertLess(store.get(e["id"])["importance"], 0.8)

    def test_stats(self):
        self.store.add("a", "事实")
        self.store.add("b", "情绪")
        stats = self.store.stats()
        self.assertEqual(stats["total"], 2)
        self.assertEqual(stats["by_type"]["情绪"], 1)


class ExtractTests(unittest.TestCase):
    def test_extracts_multiple_types(self):
        text = "我叫小明，我的生日是5月20日，我喜欢三分糖奶茶，我讨厌被敷衍，今天我们一起去看了电影，最近压力大"
        items = extract_memories(text)
        types = {i["type"] for i in items}
        self.assertIn("事实", types)
        self.assertIn("偏好", types)
        self.assertIn("共享事件", types)
        self.assertIn("情绪", types)
        # 每条都必须能溯源到原句
        self.assertTrue(all(i["source"] for i in items))

    def test_no_fabrication_on_unknown_text(self):
        self.assertEqual(extract_memories("嗯。"), [])
        self.assertEqual(extract_memories(""), [])

    def test_sensitive_text_dropped(self):
        self.assertEqual(extract_memories("我叫小明，我的手机号是13812345678"), [],
                         "含敏感信息的句子应整句放弃")

    def test_valence_sign(self):
        items = extract_memories("我喜欢猫咪")
        self.assertGreater(items[0]["valence"], 0)
        items = extract_memories("我讨厌被敷衍")
        self.assertLess(items[0]["valence"], 0)


class RetrieveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="lc_v2_")
        os.environ["LOVE_COMPANION_DATA_DIR"] = self.tmp
        self.store = MemoryStore(self.tmp)
        self.store.add("用户喜欢三分糖奶茶", "偏好", importance=0.6)
        self.store.add("用户生日是 5 月 20 日", "事实", importance=0.8)
        self.store.add("我们一起去看过海", "共享事件", importance=0.7)
        self.store.add("用户最近压力大，在做项目", "情绪", importance=0.7)

    def test_top_k_respects_budget(self):
        hits = top_k(self.store.all(), "我好累，压力大", k=3, token_budget=150)
        self.assertLessEqual(len(hits), 3)
        self.assertLessEqual(estimate_tokens(render(hits)), 150)

    def test_relevance(self):
        hits = top_k(self.store.all(), "压力大", k=1)
        self.assertIn("压力", hits[0]["content"])

    def test_relational_boost(self):
        """关系类记忆（共享事件/里程碑）在同等条件下更优先"""
        e1 = {"content": "普通事实", "type": "事实", "importance": 0.7}
        e2 = {"content": "普通事实", "type": "共享事件", "importance": 0.7}
        now = datetime.now()
        self.assertGreater(score_entry(e2, "普通事实", now), score_entry(e1, "普通事实", now))

    def test_render_with_ids(self):
        hits = top_k(self.store.all(), "生日", k=2)
        text = render(hits)
        self.assertIn("#", text, "渲染结果应带 id 便于追溯")


if __name__ == "__main__":
    unittest.main(verbosity=2)
