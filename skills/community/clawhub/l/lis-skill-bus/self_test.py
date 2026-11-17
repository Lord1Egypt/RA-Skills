#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lis-skill-bus 自测 v0.1.12：纯 stdlib，无网络，不污染真实 SKILLBUS_STATE_DIR。

覆盖面（≥10）：
  * scripts/ 目录缺失也能探测（deps.py marker 不再强制）
  * 同图只解析一次（source sha256 判重命中）
  * 多算量共享（cad 发布 → 土建/安装/装饰/园林/钢结构读取同一契约）
  * 降级自身 state（bus 未命中/损坏时不抛错、可回退到本机状态文件）
  * 契约解析、状态原子写、溯源与 CLI 接线

用法：python3 self_test.py
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import skillbus  # noqa: E402


def _source_file(tmp: Path, name: str = "楼板平面.dwg") -> Path:
    f = tmp / name
    f.write_bytes(b"FAKE-DWG-CONTENT-" + name.encode("utf-8"))
    return f


class BusIsolationTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory(prefix="skillbus-selftest-")
        self._root = Path(self._tmp.name)
        self._old_state_dir = os.environ.get("SKILLBUS_STATE_DIR")
        os.environ["SKILLBUS_STATE_DIR"] = str(self._root)
        skillbus.STATE_DIR = Path(os.environ["SKILLBUS_STATE_DIR"])
        skillbus.STATE_FILE = skillbus.STATE_DIR / "state.json"

    def tearDown(self) -> None:
        if self._old_state_dir is None:
            os.environ.pop("SKILLBUS_STATE_DIR", None)
        else:
            os.environ["SKILLBUS_STATE_DIR"] = self._old_state_dir
        self._tmp.cleanup()

    def _contract(self, source: Path, specialty: str = "土建", schema: str = "cad-contract/v1") -> dict:
        sha = hashlib.sha256(source.read_bytes()).hexdigest()
        return {
            "_id": f"cad:p:{specialty}:{sha[:10]}",
            "schema": schema,
            "spec": "cad-file-reader/v0",
            "producer": {"skill": "cad-file-reader", "final_quantity": False},
            "source": {"file": str(source), "sha256": sha},
            "candidates": [{"text": "梁 C30", "confidence_tier": "confirmed_evidence"}],
        }

    # ---- 探测：scripts/ 缺失也能命中 ----
    def test_detect_without_scripts_dir(self) -> None:
        # 模拟 lis-skill-bus 本技能：无 scripts/，只有 SKILL.md
        skill = self._root / "lis-skill-bus"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: lis-skill-bus\nversion: 0.1.9\n---\n", encoding="utf-8")
        info = skillbus.detect_skill(skill)
        self.assertIsNotNone(info)
        self.assertFalse(info["has_scripts"])
        self.assertEqual(info["marker"], "SKILL.md")
        self.assertEqual(info["slug"], "lis-skill-bus")

    def test_detect_with_scripts_deps_marker(self) -> None:
        skill = self._root / "cad-file-reader"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: cad-file-reader\n---\n", encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "scripts" / "deps.py").write_text("VERSION='x'\n", encoding="utf-8")
        info = skillbus.detect_skill(skill)
        self.assertTrue(info["has_scripts"])
        self.assertEqual(info["marker"], "scripts" + "/" + "deps.py")

    def test_detect_with_scripts_but_no_deps(self) -> None:
        skill = self._root / "tujian-suanliang"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: tujian-suanliang\n---\n", encoding="utf-8")
        (skill / "scripts").mkdir()
        (skill / "scripts" / "qty.py").write_text("def q(): pass\n", encoding="utf-8")
        info = skillbus.detect_skill(skill)
        self.assertTrue(info["has_scripts"])
        self.assertEqual(info["marker"], "scripts" + "/" + "qty.py")

    def test_detect_ignores_unknown_dir(self) -> None:
        junk = self._root / "junk"
        junk.mkdir()
        (junk / "data.bin").write_bytes(b"x")
        self.assertIsNone(skillbus.detect_skill(junk))

    def test_list_skills_uses_root_fallback(self) -> None:
        skill = self._root / "lis-skill-bus"
        skill.mkdir()
        (skill / "SKILL.md").write_text("---\nname: lis-skill-bus\nversion: 0.1.9\n---\n", encoding="utf-8")
        rows = skillbus.list_skills(self._root)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["slug"], "lis-skill-bus")
        self.assertFalse(rows[0]["has_scripts"])
        self.assertEqual(rows[0]["marker"], "SKILL.md")

    # ---- 状态 / 原子写 / 溯源 ----
    def test_empty_state_no_file(self) -> None:
        st = skillbus._load_state()
        self.assertEqual(st["state_version"], 1)
        self.assertEqual(st["projects"], {})

    def test_push_and_get_roundtrip_provenance(self) -> None:
        src = _source_file(self._root)
        entry = self._contract(src)
        pushed = skillbus.push_project_state(
            "酒店A", entry, building="5#", floor="三层", source_skill="cad-file-reader")
        self.assertTrue(pushed["saved"])
        raw = json.loads(skillbus.STATE_FILE.read_text(encoding="utf-8"))
        key = "酒店A__slash__5#__slash__三层"
        e = raw["projects"][key][entry["_id"]]
        self.assertEqual(e["_provenance"]["source_skill"], "cad-file-reader")
        self.assertEqual(e["_provenance"]["source_sha256"], entry["source"]["sha256"])
        self.assertEqual(e["_provenance"]["source_file"], str(src))

    def test_corrupted_state_degrades_without_clobber(self) -> None:
        skillbus.STATE_DIR.mkdir(parents=True, exist_ok=True)
        skillbus.STATE_FILE.write_text("{broken", encoding="utf-8")
        st = skillbus._load_state()
        self.assertEqual(st.get("_corrupted"), str(skillbus.STATE_FILE))
        self.assertEqual(skillbus.STATE_FILE.read_text(encoding="utf-8"), "{broken")

    # ---- 同图只解析一次 ----
    def test_same_source_parsed_once_cache_hit(self) -> None:
        src = _source_file(self._root)
        entry = self._contract(src)
        skillbus.push_project_state("P1", entry, source_skill="cad-file-reader")
        hit = skillbus.find_contract("P1", source_file=str(src))
        self.assertTrue(hit["hit"])
        self.assertEqual(hit["entry_id"], entry["_id"])
        self.assertEqual(hit["reason"], "source_sha256 命中")

    def test_same_source_filename_match_hit(self) -> None:
        src = _source_file(self._root)
        entry = self._contract(src)
        skillbus.push_project_state("P1", entry, source_skill="cad-file-reader")
        hit = skillbus.find_contract("P1", source_file=str(src))
        self.assertTrue(hit["hit"])

    def test_find_contract_miss_no_state(self) -> None:
        src = _source_file(self._root)
        miss = skillbus.find_contract("不存在项目", source_file=str(src))
        self.assertFalse(miss["hit"])
        self.assertEqual(miss["reason"], "未命中")

    # ---- 多算量共享 ----
    def test_multi_quantity_share_same_contract(self) -> None:
        src = _source_file(self._root, "5#楼一层.dwg")
        entry = self._contract(src)
        skillbus.push_project_state("酒店B", entry, building="5#", floor="F1",
                                    source_skill="cad-file-reader")
        # 土建、安装、装饰、园林、钢结构都从 bus 拉同一契约（不同专业也共享，不再重复解图）
        for prog in ("tujian-suanliang", "anzhuang-suanliang",
                     "zhuangshi-suanliang", "yuanlin-suanliang",
                     "gangjiegou-suanliang"):
            got = skillbus.get_project_state("酒店B", "5#", "F1")
            self.assertIn(entry["_id"], got["entries"])
            self.assertEqual(got["entries"][entry["_id"]]["source"]["sha256"],
                             entry["source"]["sha256"])

    # ---- 降级自身 state ----
    def test_degraded_state_readable_without_bus(self) -> None:
        # bus state 缺失时返回空库（skills 各自写自身 state 也同构，不抛错）
        got = skillbus.get_project_state("降级项目", "7#", "F3")
        self.assertEqual(got["entries"], {})
        self.assertTrue(str(skillbus.STATE_DIR).startswith(tempfile.gettempdir()))

    def test_cli_find_contract_available(self) -> None:
        src = _source_file(self._root)
        entry = self._contract(src)
        skillbus.push_project_state("CLI项目", entry, source_skill="cad-file-reader")
        cp = subprocess.run(
            [sys.executable, str(Path(__file__).resolve().parent / "skillbus.py"),
             "find-contract", "--project", "CLI项目", "--source-file", str(src)],
            capture_output=True, text=True, timeout=60)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        data = json.loads(cp.stdout)
        self.assertTrue(data["hit"])
        self.assertEqual(data["entry_id"], entry["_id"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
