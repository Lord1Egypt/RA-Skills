# -*- coding: utf-8 -*-
"""v7.8.0 契约测试（test_v70800）：文档事实契约五闸 + freshness 基线根修 + 极端输入鲁棒电池。

三组契约：
  ① doc_facts 干净树 5/5 绿；篡改矩阵逐闸验证"每个闸都能抓住自己的缺陷类"
    （全部在包副本上隔离进行——正本只读纪律）。
  ② freshness --status 基线对账 archive 感知；缺失基线必须如实上报（禁静默吞错）。
  ③ 极端输入鲁棒：空/空白/控制符/纯 emoji/CRLF/BOM/20 万字单行在 SDK 与 CLI
    两侧行为锁定（短文铁律、编码警示、友好 ValueError）——防回潮。
"""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

sys.path.insert(0, str(SCRIPTS))
sys.path.insert(0, str(PKG / "tests"))
import _docs  # noqa: E402

_LONG_TEXT = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
              "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
              "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
              "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
              "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")


def _doc_facts(root):
    return subprocess.run([sys.executable, str(PKG / "eval" / "doc_facts.py"),
                           "--root", str(root)],
                          capture_output=True, text=True, timeout=180,
                          encoding="utf-8", errors="replace")


class TestDocFactsClean(unittest.TestCase):
    def test_all_gates_pass_on_clean_tree(self):
        p = _doc_facts(PKG)
        self.assertEqual(p.returncode, 0, (p.stdout + p.stderr)[-300:])
        self.assertIn("PASS（5/5 闸）", p.stdout)


class TestDocFactsTamper(unittest.TestCase):
    """篡改矩阵：包副本隔离（正本只读），每例篡改一处→对应闸 FAIL→还原。"""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.mkdtemp(prefix="ppp78_facts_")
        cls.copy = Path(cls._tmp) / "pkg"
        shutil.copytree(PKG, cls.copy, ignore=shutil.ignore_patterns(
            ".git", "__pycache__", ".pytest_cache"))
        for junk in ("examples/gallery", "examples/previews"):
            shutil.rmtree(cls.copy / junk, ignore_errors=True)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tmp, ignore_errors=True)

    def _tamper(self, rel, fn):
        p = self.copy / rel
        orig = p.read_text(encoding="utf-8") if p.is_file() else None
        try:
            fn(p)
            r = _doc_facts(self.copy)
            self.assertNotEqual(r.returncode, 0, "篡改后必须 FAIL（闸失效=假绿）")
            return r.stdout + r.stderr
        finally:
            if orig is None:
                p.unlink(missing_ok=True)
            else:
                p.write_text(orig, encoding="utf-8")

    def test_gate_a_ghost_ref(self):
        def fn(p):
            p.write_text(p.read_text(encoding="utf-8")
                         + "\n基线见 eval/results/ghost_file.json。\n", encoding="utf-8")
        self.assertIn("ghost_file.json", self._tamper("SKILL.md", fn))

    def test_gate_a_archive_masking(self):
        """历史病灶复演：archive 内文件写成顶层引用必须被拦。"""
        def fn(p):
            p.write_text(p.read_text(encoding="utf-8")
                         + "\n基线见 eval/results/v480_rules_oldgen.json。\n", encoding="utf-8")
        self.assertIn("archive/ 前缀", self._tamper("SKILL.md", fn))

    @unittest.skipUnless(_docs.HAS_ZH, "CH 打包形态无 SKILL_ZH.md（闸 C 空过，形态自适应）")
    def test_gate_c_numeric_asymmetry(self):
        def fn(p):
            p.write_text(p.read_text(encoding="utf-8") + "\n补充：0.9400。\n", encoding="utf-8")
        self.assertIn("数字不对称", self._tamper("SKILL_ZH.md", fn))

    def test_gate_d_orphan_doc_ref(self):
        def fn(p):
            p.write_text(p.read_text(encoding="utf-8")
                         + "\n用法：pp.py ghostcmd 文件。\n", encoding="utf-8")
        self.assertIn("ghostcmd", self._tamper("SKILL.md", fn))

    def test_gate_d_unregistered_command(self):
        def fn(p):
            t = p.read_text(encoding="utf-8")
            t = t.replace('BUILTIN = ("quickstart"',
                          'BUILTIN = ("ghostcmd", "quickstart"', 1)
            p.write_text(t, encoding="utf-8")
        self.assertIn("ghostcmd", self._tamper("scripts/pp.py", fn))

    def test_gate_e_metric_anchor_drift(self):
        fp = self.copy / "eval" / "results" / "v35ctl_oldgen.json"
        orig = json.loads(fp.read_text(encoding="utf-8"))
        try:
            d = dict(orig)
            d["auroc"] = 0.5
            fp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            r = _doc_facts(self.copy)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("0.9998", r.stdout)
        finally:
            fp.write_text(json.dumps(orig, ensure_ascii=False), encoding="utf-8")

    def test_gate_f_version_mismatch(self):
        fp = self.copy / "skill.json"
        orig = json.loads(fp.read_text(encoding="utf-8"))
        try:
            d = dict(orig)
            d["version"] = "9.9.9"
            fp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
            r = _doc_facts(self.copy)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("CHANGELOG", r.stdout)
        finally:
            fp.write_text(json.dumps(orig, ensure_ascii=False), encoding="utf-8")


class TestFreshnessBaselineFix(unittest.TestCase):
    def test_status_all_baselines_resolve(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "freshness_refresh.py"),
                            "--status", "--json"],
                           capture_output=True, text=True, timeout=120,
                           encoding="utf-8", errors="replace")
        self.assertEqual(p.returncode, 0, p.stdout[-200:])
        d = json.loads(p.stdout)
        self.assertEqual(d["baselines_missing"], [])
        self.assertEqual(d["baseline_drift"], [])

    def test_missing_baseline_reported_not_silent(self):
        """根修契约：基线缺失必须进 baselines_missing（不得静默伪装成无漂移）。"""
        with tempfile.TemporaryDirectory(prefix="ppp78_fr_") as td:
            res = Path(td) / "results"
            res.mkdir()
            for f in ("v35ctl_oldgen.json", "v35ctl_gen2026.json"):
                shutil.copy2(PKG / "eval" / "results" / f, res / f)
            p = subprocess.run([sys.executable, str(SCRIPTS / "freshness_refresh.py"),
                                "--status", "--json", "--results-dir", str(res)],
                               capture_output=True, text=True, timeout=120,
                               encoding="utf-8", errors="replace")
            self.assertEqual(p.returncode, 0, p.stdout[-200:])
            d = json.loads(p.stdout)
            self.assertEqual(sorted(d["baselines_missing"]),
                             ["archive/v480_rules_gen2026.json",
                              "archive/v480_rules_oldgen.json"])


class TestEdgeInputsSDK(unittest.TestCase):
    """极端输入鲁棒（SDK 侧）：友好报错或诚实降级，禁止意外异常类型。"""

    SHORT_CASES = {
        "empty": "",
        "whitespace": " \n\t ",
    }
    VALID_CASES = {
        "control_chars": "\x00\x01\x02中文\x7f\x00",
        "emoji_only": "😀🚀🌟" * 50,
        "crlf": "第一段。\r\n第二段。\r\n" * 20,
        "long_single_line": "长" * 200000,
        "bom_prefixed": "\ufeff" + _LONG_TEXT * 3,
    }

    def test_empty_friendly_valueerror(self):
        for fn in ("detect_text", "gate_text", "fix_suggest", "workflow", "term_report"):
            with self.subTest(api=fn):
                with self.assertRaises(ValueError) as cm:
                    getattr(__import__("pp_api"), fn)(self.SHORT_CASES["empty"])
                self.assertIn("非空", str(cm.exception))

    def test_whitespace_friendly_valueerror(self):
        import pp_api
        with self.assertRaises(ValueError):
            pp_api.detect_text(self.SHORT_CASES["whitespace"])

    def test_valid_extremes_return_contract_shape(self):
        import pp_api
        required = {"overall_ai_score", "overall_risk", "degraded_mode",
                    "total_paragraphs", "language"}
        for name, t in self.VALID_CASES.items():
            with self.subTest(case=name):
                r = pp_api.detect_text(t)
                self.assertTrue(required <= set(r), f"{name}: 缺键 {required - set(r)}")
                self.assertIsInstance(r["degraded_mode"], bool)

    def test_short_text_unknown_by_design(self):
        """短文铁律：控制符等 <100 字输入不得给出 high/medium 判定。"""
        import pp_api
        r = pp_api.detect_text(self.VALID_CASES["control_chars"])
        self.assertEqual(r["overall_risk"], "unknown")


class TestEdgeInputsCLI(unittest.TestCase):
    """极端输入鲁棒（CLI 侧）：不崩溃、不静默——空文件走短文铁律，二进制带编码警示。"""

    @classmethod
    def setUpClass(cls):
        cls._tmp = tempfile.mkdtemp(prefix="ppp78_edge_")
        t = Path(cls._tmp)
        (t / "empty.txt").write_text("", encoding="utf-8")
        (t / "bin.dat").write_bytes(bytes(range(256)) * 4)
        (t / "crlf.txt").write_bytes(("第一段内容足够长一些。\r\n" * 30).encode("utf-8"))
        (t / "bom.txt").write_bytes("\ufeff".encode("utf-8") + (_LONG_TEXT * 3).encode("utf-8"))

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls._tmp, ignore_errors=True)

    def _run(self, name):
        return subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "detect",
                               str(Path(self._tmp) / name)],
                              capture_output=True, text=True, timeout=300,
                              encoding="utf-8", errors="replace")

    def test_empty_file_short_text_law(self):
        p = self._run("empty.txt")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("过短", p.stdout)

    def test_binary_file_honest_encoding_warning(self):
        p = self._run("bin.dat")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("编码警示", p.stdout)

    def test_crlf_file_normal_detection(self):
        p = self._run("crlf.txt")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("AI痕迹评分", p.stdout)

    def test_bom_file_detected_not_crash(self):
        p = self._run("bom.txt")
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        self.assertNotIn("Traceback", p.stderr)
        self.assertIn("AI痕迹评分", p.stdout)


if __name__ == "__main__":
    unittest.main()
