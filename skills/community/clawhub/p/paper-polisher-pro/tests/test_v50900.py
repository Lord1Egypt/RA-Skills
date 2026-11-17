# -*- coding: utf-8 -*-
"""v5.9.0 契约测试（test_v50900）：上手闭环（模型获取指南）/ 批处理熔断 / 新造词探测 / 版本头卫生。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
SCRIPTS = PKG / "scripts"
PY = sys.executable


def _run(*args, timeout=120):
    return subprocess.run([PY, *map(str, args)], capture_output=True,
                          text=True, timeout=timeout, cwd=str(PKG))


class TestSetupGuide(unittest.TestCase):
    """模型获取路径透明化（上手闭环）。"""

    def test_guide_command(self):
        r = _run(SCRIPTS / "pp_setup.py", "--guide")
        self.assertEqual(r.returncode, 0)
        for kw in ("获取指南", "签发", "降级", "quickstart"):
            self.assertIn(kw, r.stdout, f"--guide 缺关键词: {kw}")

    def test_setup_entry_registered_with_guide(self):
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        self.assertIn("--guide", src)

    def test_doctor_hint_wired(self):
        src = (SCRIPTS / "pp_doctor.py").read_text(encoding="utf-8")
        self.assertIn("pp_setup.py --guide", src)

    def test_setup_check_hint_wired(self):
        src = (SCRIPTS / "pp_setup.py").read_text(encoding="utf-8")
        self.assertIn("--guide 查看获取指南", src)


class TestBatchCircuit(unittest.TestCase):
    """批处理连续错误熔断（稳健性）。"""

    @classmethod
    def setUpClass(cls):
        cls.dir = Path(tempfile.mkdtemp(prefix="circuit_"))
        for i in range(1, 7):
            (cls.dir / f"bad{i}.docx").write_bytes(b"not a zip at all")
        (cls.dir / "good.txt").write_text(
            "这是一段完全正常的中文文本，用于让批处理目录里存在可成功解析的文件。"
            "它长度超过一百个字符，以通过最短长度检查并被计为成功项，"
            "从而验证熔断计数会被成功文件复位。", encoding="utf-8")

    def test_circuit_trips_and_discloses(self):
        r = _run(SCRIPTS / "ai_detector.py", "--batch", self.dir,
                 "--circuit", "3", "--format", "json", timeout=180)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        self.assertTrue(d["circuit"]["tripped"])
        self.assertEqual(d["circuit"]["threshold"], 3)
        self.assertGreater(d["circuit"]["skipped_remaining"], 0)

    def test_circuit_off_processes_all(self):
        r = _run(SCRIPTS / "ai_detector.py", "--batch", self.dir,
                 "--circuit", "0", "--format", "json", timeout=240)
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        d = json.loads(r.stdout)
        self.assertIsNone(d.get("circuit"))
        self.assertEqual(d["aggregate"]["files"], 7)

    def test_single_file_docx_error_contract_intact(self):
        r = _run(SCRIPTS / "ai_detector.py", self.dir / "bad1.docx")
        self.assertEqual(r.returncode, 2, "单文件坏 docx 应保持退出码 2（输入错误）")


class TestNeologismProbe(unittest.TestCase):
    """creativity：词典外新造词探测（opt-in、建议性、明示未校准）。"""

    def test_invented_word_flagged_only_with_flag(self):
        sys.path.insert(0, str(SCRIPTS))
        from term_check import load_terminology, find_neologisms
        terms = load_terminology()
        text = ("针对梭罗酶活性的报道相互矛盾，我们复测了梭罗酶。"
                "同时按年龄特异性参考区间复判，首要监测指标为 IgA。")
        hints = find_neologisms(text, terms)
        self.assertTrue(any(h["term"] == "梭罗酶" for h in hints), "造词未被提示")
        self.assertFalse(any("特异" in h["term"] for h in hints), "库内词片段误报")

    def test_flag_wiring(self):
        src = (SCRIPTS / "term_check.py").read_text(encoding="utf-8")
        self.assertIn("--neologism", src)
        self.assertIn("未校准", src)

    def test_default_run_has_no_probe(self):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False,
                                         encoding="utf-8") as f:
            f.write("按年龄特异性参考区间复判，首要监测指标为 IgA，检验报告已出具。" * 3)
            path = f.name
        r = _run(SCRIPTS / "term_check.py", path)
        self.assertNotIn("未校准", r.stdout, "默认运行不应出现新造词提示")
        r2 = _run(SCRIPTS / "term_check.py", path, "--neologism")
        self.assertIn("未校准", r2.stdout)


class TestVersionHeaderHygiene(unittest.TestCase):
    """脚本头部游离版本号防回潮（一致性）。"""

    def test_no_stray_versions_in_headers(self):
        import re
        stray = []
        for p in sorted(SCRIPTS.glob("*.py")):
            head = "\n".join(p.read_text(encoding="utf-8", errors="replace").splitlines()[:6])
            if re.search(r"paper-polisher( pro)? v\d+\.\d+", head):
                stray.append(p.name)
        self.assertEqual(stray, [], f"游离版本号: {stray}")

    def test_detector_header_version_neutral(self):
        head = (SCRIPTS / "ai_detector.py").read_text(encoding="utf-8").splitlines()[:6]
        self.assertTrue(any("SKILL.md frontmatter" in ln for ln in head))


class TestProgressiveNav(unittest.TestCase):
    """FAQ 分组导航前置（渐进披露）。"""

    def test_faq_nav_lines(self):
        _sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue("five parts" in _sk or "分五组" in _sk)
        self.assertIn("分五组", _docs.zh_text())

    def test_architecture_read_on_demand(self):
        _sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue("read on demand" in _sk or "按需查阅" in _sk or "按需阅读" in _sk)
        self.assertIn("按需阅读", _docs.zh_text())


if __name__ == "__main__":
    unittest.main()
