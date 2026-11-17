# -*- coding: utf-8 -*-
"""v6.0.0 契约测试（test_v60000）：趋势报告 / 统一错误呈现 / 分组双语入口 / 批处理混沌压测。"""
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
SCRIPTS = PKG / "scripts"
PY = sys.executable


def _run(*args, timeout=180, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([PY, *map(str, args)], capture_output=True,
                          text=True, timeout=timeout, cwd=str(PKG), env=env)


def _mk_workflow(path, score, risk="low", degraded=False):
    d = {"engine_version": "6.0.0",
         "detect": {"overall_ai_score": score, "overall_risk": risk,
                    "degraded_mode": degraded},
         "paragraphs": {"high": max(0, score // 10), "medium": 2, "total": 12}}
    path.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return path


class TestTrend(unittest.TestCase):
    """头牌：多轮趋势仪表盘。"""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="trend_"))
        for i, (s, r) in enumerate([(62, "high"), (41, "medium"), (24, "low")]):
            p = _mk_workflow(cls.dir / f"draft_v{i+1}.workflow.json", s, r)
            os.utime(p, (time.time() - (3 - i) * 86400,) * 2)

    def test_trend_html(self):
        out = self.dir / "trend.html"
        r = _run(SCRIPTS / "pp_trend.py", self.dir, "-o", out)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        html = out.read_text(encoding="utf-8")
        for kw in ("<svg", "逐轮明细", "↓改善", "学术诚信", "62", "24"):
            self.assertIn(kw, html, f"趋势报告缺: {kw}")
        self.assertNotIn("http://cdn", html.replace("http://www.w3.org", ""))
        self.assertNotIn("<script src", html)

    def test_fewer_than_two_inputs_exit_2(self):
        r = _run(SCRIPTS / "pp_trend.py", self.dir / "draft_v1.workflow.json")
        self.assertEqual(r.returncode, 2)
        self.assertIn("至少 2 份", r.stderr)

    def test_trend_registered(self):
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        self.assertIn('"trend"', src)
        self.assertTrue((SCRIPTS / "pp_trend.py").is_file())


class TestFriendlyErrors(unittest.TestCase):
    """统一错误呈现：技术护栏 → 人话两段式。"""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="ferr_"))
        # 高压缩比 zip（解压超 30MB 上限的 docx 样貌）
        zp = cls.dir / "bomb.docx"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("word/document.xml", b"0" * (40 * 1024 * 1024))
        cls.bomb = zp
        cls.fake = cls.dir / "fake.docx"
        cls.fake.write_bytes(b"not a zip")

    def test_zipbomb_friendly_no_traceback(self):
        r = _run(SCRIPTS / "pp_workflow.py", self.bomb)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn("下一步", r.stderr)
        self.assertTrue("另存为" in r.stderr or "拆分" in r.stderr,
                        f"缺可操作建议: {r.stderr[-200:]}")

    def test_corrupt_docx_friendly(self):
        r = _run(SCRIPTS / "ai_detector.py", self.fake)
        self.assertEqual(r.returncode, 2)
        self.assertNotIn("Traceback", r.stderr)
        self.assertIn("下一步", r.stderr)

    def test_exit_code_contract_untouched(self):
        r = _run(SCRIPTS / "pp.py", "no-such-cmd-xyz")
        self.assertEqual(r.returncode, 2)


class TestGroupedBilingualEntry(unittest.TestCase):
    """分组帮助 + 新手三步 + PP_LANG=en 英文入口面。"""

    def test_grouped_help_cn(self):
        r = _run(SCRIPTS / "pp.py")
        self.assertEqual(r.returncode, 0)
        for kw in ("新手三步", "【检测 Detection】", "【报告与可视化 Reports & visuals】", "trend"):
            self.assertIn(kw, r.stdout, f"分组帮助缺: {kw}")

    def test_english_surface(self):
        r = _run(SCRIPTS / "pp.py", env_extra={"PP_LANG": "en"})
        self.assertEqual(r.returncode, 0)
        for kw in ("First 60 seconds", "[Detection]", "Exit-code contract"):
            self.assertIn(kw, r.stdout, f"英文入口缺: {kw}")
        r2 = _run(SCRIPTS / "pp.py", "no-such-cmd-xyz", env_extra={"PP_LANG": "en"})
        self.assertEqual(r2.returncode, 2)
        self.assertIn("Unknown subcommand", r2.stderr)

    def test_lang_documented_as_env_var(self):
        for doc in _docs.DOCS:
            t = (PKG / doc).read_text(encoding="utf-8")
            self.assertIn("PP_LANG", t, f"{doc} 未声明 PP_LANG 环境变量")


class TestBatchChaos(unittest.TestCase):
    """批处理混沌压测：损坏/空/过短/正常混合目录的隔离与熔断。"""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="chaos_"))
        para = ("这一段是正常长度的中文学术文本，用于混沌压测中的有效样本，"
                "确保批处理能够产出可评分行。补充句子以满足最短长度要求，"
                "同时保持内容中性、不触发任何特殊规则。" * 3)
        # 交错命名：坏/好相邻，测逐文件隔离（坏文件计数被好文件复位，不触发熔断）
        plan = []
        for i in range(20):
            plan.append((f"f{i:02d}_a_corrupt.docx", "corrupt"))
            plan.append((f"f{i:02d}_b_valid.txt", "valid"))
        for i in range(4):
            plan.append((f"g{i:02d}_empty.txt", "empty"))
            plan.append((f"g{i:02d}_short.txt", "short"))
        plan.append(("h00_gbk.txt", "gbk"))
        for name, kind in plan:
            fp = cls.dir / name
            if kind == "corrupt":
                fp.write_bytes(b"garbage bytes")
            elif kind == "valid":
                fp.write_text(para, encoding="utf-8")
            elif kind == "empty":
                fp.write_bytes(b"")
            elif kind == "short":
                fp.write_text("太短。" * 3, encoding="utf-8")
            else:
                fp.write_bytes(("这是一段GBK编码的中文文本，" * 20).encode("gbk"))

    def test_chaos_batch_isolated_and_disclosed(self):
        out = self.dir / "chaos.csv"
        # v7.3.0: 420→900s——三线并行（单测+smoke+CH 形态验收）时隔离模式 49 worker
        # 与其他套件抢 CPU，需并行环境余量
        r = _run(SCRIPTS / "ai_detector.py", "--batch", self.dir,
                 "--csv", out, "--format", "json", timeout=900)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        # 交错布局下坏文件不连续 → 熔断不触发，49 个文件全部逐文件隔离处理
        self.assertIsNone(d.get("circuit"), "交错布局不应触发熔断")
        self.assertEqual(d["aggregate"]["files"], 49)
        errors = [f for f in d["files"] if "error" in f]
        self.assertEqual(len(errors), 20, "损坏 docx 应逐文件降级为 ERROR 行")
        import csv as _csv
        with open(out, encoding="utf-8-sig", newline="") as f:
            rows = list(_csv.reader(f))
        self.assertEqual(len(rows), 50, "CSV 应含表头+49 行")
        scored = [row for row in rows[1:] if row and row[1] not in ("ERROR", "")]
        self.assertGreaterEqual(len(scored), 10, "有效样本应全部可评分")

    def test_chaos_all_corrupt_trips_default_circuit(self):
        bad_dir = Path(tempfile.mkdtemp(prefix="chaos_bad_"))
        for i in range(7):
            (bad_dir / f"bad{i}.docx").write_bytes(b"x")
        r = _run(SCRIPTS / "ai_detector.py", "--batch", bad_dir,
                 "--format", "json", timeout=240)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        self.assertTrue(d.get("circuit", {}).get("tripped"),
                        "默认阈值下连续坏文件应触发熔断")


if __name__ == "__main__":
    unittest.main()
