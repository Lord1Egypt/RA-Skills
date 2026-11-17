#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Love Companion 回归测试（M0 交付物）

覆盖两块：
1. v1 既有能力：预设解析、人设配置、方案/记忆管理、CLI（对应 v1.0.1 + 本次重构）
2. v2 新能力：数据 schema、v1→v2 迁移的**无损性**与**向下兼容**

运行：
    python tests/test_manager.py
    python -m unittest discover tests
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))

import manager as mgr_module  # noqa: E402
from scripts.core import schema  # noqa: E402

PY = sys.executable
PERSONAS = ROOT / "references" / "personas.md"


class PresetTests(unittest.TestCase):
    """v1 预设：唯一数据源 = references/personas.md"""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="lc_test_"))
        os.environ["LOVE_COMPANION_DATA_DIR"] = str(self.tmp)
        self.mgr = mgr_module.LoveCompanionManager()

    def test_personas_md_json_blocks_all_valid(self):
        md = PERSONAS.read_text(encoding="utf-8")
        blocks = re.findall(r"```json\s*\n(.*?)\n```", md, re.S)
        self.assertEqual(len(blocks), 8, "personas.md 应含 8 个预设 JSON 块")
        parsed = [json.loads(b) for b in blocks]  # 解析失败会抛异常
        self.assertEqual([p.get("姓名") for p in parsed][:2], ["小阳", "温婉"])

    def test_list_presets_ids(self):
        ids = [p["id"] for p in self.mgr.list_presets()]
        self.assertEqual(ids, list(range(1, 9)))

    def test_preset_matches_doc(self):
        md = PERSONAS.read_text(encoding="utf-8")
        blocks = re.findall(r"```json\s*\n(.*?)\n```", md, re.S)
        for i, block in enumerate(blocks, 1):
            expected = json.loads(block)
            applied = self.mgr.load_preset(i)
            self.assertEqual(applied, expected, f"预设 #{i} 与文档不一致")

    def test_preset_2_call_regression(self):
        """v1.0.1 遗留回归：2 号称呼应为「宝宝」，不是「宝贝」"""
        self.assertEqual(self.mgr.load_preset(2)["对用户的称呼"], "宝宝")

    def test_cache_not_polluted(self):
        p = self.mgr.load_preset(2)
        p["姓名"] = "被改坏了"
        self.mgr._preset_cache = None
        self.assertEqual(self.mgr.load_preset(2)["姓名"], "温婉")

    def test_bad_json_reports_preset_id(self):
        broken = self.tmp / "broken.md"
        broken.write_text(
            '# 预设\n\n### 【9号】坏预设\n\n```json\n{"姓名": "小"坏""}\n```\n',
            encoding="utf-8",
        )
        os.environ["LOVE_COMPANION_PERSONAS_FILE"] = str(broken)
        try:
            with self.assertRaises(ValueError) as ctx:
                mgr_module.LoveCompanionManager(storage_path=str(self.tmp)).list_presets()
            self.assertIn("9", str(ctx.exception))
        finally:
            del os.environ["LOVE_COMPANION_PERSONAS_FILE"]

    def test_unknown_preset_returns_none(self):
        self.assertIsNone(self.mgr.load_preset(99))

    def test_no_hardcoded_personas_in_manager(self):
        src = (ROOT / "scripts" / "manager.py").read_text(encoding="utf-8")
        for name in ("小阳", "霍霆", "苏妖"):
            self.assertNotIn(name, src, f"manager.py 不应再硬编码预设 {name}")


class SchemeAndMemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="lc_test_"))
        os.environ["LOVE_COMPANION_DATA_DIR"] = str(self.tmp)
        self.mgr = mgr_module.LoveCompanionManager()

    def test_scheme_save_switch_delete(self):
        self.mgr.load_preset(1)
        self.assertTrue(self.mgr.save_scheme("测试方案"))
        self.assertIn("测试方案", [s["name"] for s in self.mgr.list_schemes()])
        self.assertTrue(self.mgr.delete_scheme("测试方案"))
        self.assertFalse(self.mgr.delete_scheme("测试方案"))

    def test_memory_crud(self):
        m = self.mgr.add_memory("用户生日 5 月 20 日")
        self.assertEqual(m["id"], 1)
        self.assertEqual(len(self.mgr.get_memories()), 1)
        self.assertEqual(self.mgr.delete_memory("生日"), 1)
        self.assertEqual(self.mgr.clear_memories(), 0)


class CLITests(unittest.TestCase):
    def run_cli(self, *args, data_dir: str):
        env = dict(os.environ, LOVE_COMPANION_DATA_DIR=data_dir, PYTHONIOENCODING="utf-8")
        return subprocess.run(
            [PY, str(ROOT / "scripts" / "manager.py"), *args],
            capture_output=True, text=True, encoding="utf-8", env=env,
        )

    def test_cli_commands(self):
        with tempfile.TemporaryDirectory() as d:
            r = self.run_cli("presets", data_dir=d)
            self.assertEqual(r.returncode, 0)
            self.assertIn("阳光开朗型", r.stdout)

            r = self.run_cli("apply", "2", data_dir=d)
            self.assertEqual(r.returncode, 0)
            self.assertIn("温婉", r.stdout)

            r = self.run_cli("save", "方案A", data_dir=d)
            self.assertEqual(r.returncode, 0)

            r = self.run_cli("delete-scheme", "方案A", data_dir=d)
            self.assertEqual(r.returncode, 0)

            r = self.run_cli("delete-scheme", "方案A", data_dir=d)
            self.assertNotEqual(r.returncode, 0, "删除不存在的方案应返回非 0")

            r = self.run_cli("status", data_dir=d)
            self.assertIn("preset_count", r.stdout)

            r = self.run_cli("apply", "abc", data_dir=d)
            self.assertNotEqual(r.returncode, 0, "非法编号应返回非 0")

            r = self.run_cli("nonsense", data_dir=d)
            self.assertNotEqual(r.returncode, 0)


class SchemaV2Tests(unittest.TestCase):
    """v2 数据 schema"""

    def test_memory_entry_defaults(self):
        e = schema.memory_entry("示例", entry_id=1)
        self.assertEqual(e["type"], "事实")
        self.assertEqual(e["importance"], 0.5)
        self.assertIn(e["type"], schema.MEMORY_TYPES)

    def test_unknown_type_rejected(self):
        with self.assertRaises(ValueError):
            schema.memory_entry("x", memory_type="不存在的类型")

    def test_normalize_v1_entry_is_superset(self):
        v1 = {"id": 3, "content": "用户喜欢三分糖奶茶", "created_at": "2026-05-01T10:00:00"}
        v2 = schema.normalize_memory_entry(v1, entry_id=3)
        # 原字段原样保留 → 无损
        self.assertEqual(v2["content"], v1["content"])
        self.assertEqual(v2["created_at"], v1["created_at"])
        self.assertEqual(v2["id"], 3)
        # 新增字段补齐
        for k in ("type", "source", "importance", "valence", "recall_count",
                  "updated_at", "last_recalled_at", "conversation_id"):
            self.assertIn(k, v2)

    def test_validate(self):
        ok, errors = schema.validate_memory(schema.memory_entry("有效记忆", entry_id=1))
        self.assertTrue(ok, errors)
        bad, errors = schema.validate_memory({"content": "", "importance": 9})
        self.assertFalse(bad)
        self.assertTrue(errors)

    def test_injection_budget_conflict_is_known_and_handled(self):
        """方案两组数字冲突：各模块上限之和 580 > 红线 500，必须按优先级分配"""
        budget = schema.DEFAULT_INJECTION_BUDGET
        raw_total = sum(v for k, v in budget.items() if k != "合计上限")
        self.assertGreater(raw_total, budget["合计上限"],
                           "若此项失败说明方案已修正预算，可改为直接校验总和")

        alloc = schema.allocate_budget()
        used = sum(v for k, v in alloc.items() if k != "合计上限")
        self.assertLessEqual(used, budget["合计上限"], "分配结果不得超过红线")
        self.assertEqual(alloc["相处指南"], 200, "最高优先级应先拿满")
        self.assertEqual(alloc["记忆片段"], 150)
        # 500 - 200 - 150 - 100 - 80 = 0 → 最低优先级趋势调味料被压到 0
        self.assertEqual(alloc["趋势调味料"], 0)

    def test_allocate_budget_respects_small_total(self):
        alloc = schema.allocate_budget(total=120)
        self.assertEqual(sum(v for k, v in alloc.items() if k != "合计上限"), 120)
        self.assertEqual(alloc["相处指南"], 120)
        self.assertEqual(alloc["记忆片段"], 0)

    def test_templates_serializable(self):
        for tpl in (schema.user_persona_template(), schema.cloned_persona_template("测试"),
                    schema.settings_template()):
            json.dumps(tpl, ensure_ascii=False)  # 可序列化即可


class MigrationTests(unittest.TestCase):
    """v1 → v2 迁移：无损 + 向下兼容"""

    def test_dry_run_and_lossless_migration(self):
        import scripts.migrate.migrate_v1 as mig

        with tempfile.TemporaryDirectory() as d:
            data = Path(d)
            v1_memories = [
                {"id": 1, "content": "用户生日 5 月 20 日", "created_at": "2026-05-01T10:00:00"},
                {"id": 2, "content": "讨厌被敷衍", "created_at": "2026-05-02T10:00:00"},
            ]
            (data / "memory.json").write_text(
                json.dumps(v1_memories, ensure_ascii=False), encoding="utf-8"
            )

            report = mig.run(data, dry_run=True)
            self.assertFalse(report["errors"])
            self.assertEqual(report["v1_entries"], 2)
            self.assertIsNone(report["backup"], "dry-run 不应产生备份")

            report = mig.run(data, dry_run=False)
            self.assertFalse(report["errors"])
            self.assertTrue(Path(report["backup"]).exists(), "应生成备份目录")
            self.assertTrue(report["created_settings"])

            migrated = json.loads((data / "memory.json").read_text(encoding="utf-8"))
            # 内容一条不少
            self.assertEqual([m["content"] for m in migrated],
                             [m["content"] for m in v1_memories])
            self.assertTrue(all(m["type"] == "事实" for m in migrated))

            # 向下兼容：v1 的 manager 仍能读 v2 记忆
            os.environ["LOVE_COMPANION_DATA_DIR"] = str(data)
            mgr = mgr_module.LoveCompanionManager()
            self.assertEqual(len(mgr.get_memories()), 2)
            self.assertEqual(mgr.get_memories()[0]["content"], "用户生日 5 月 20 日")

    def test_migration_on_empty_dir(self):
        import scripts.migrate.migrate_v1 as mig
        with tempfile.TemporaryDirectory() as d:
            report = mig.run(Path(d) / "not_exists", dry_run=True)
            self.assertTrue(report["errors"], "空目录应给出提示而非崩溃")


if __name__ == "__main__":
    unittest.main(verbosity=2)
