# -*- coding: utf-8 -*-
"""v6.9.0 契约测试（test_v60900）：项目工作台（目录级自查+一致性内嵌+总览）。"""
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


def _make_project():
    d = Path(tempfile.mkdtemp(prefix="ppp6900_"))
    (d / "ch1.md").write_text("本研究纳入风湿免疫病患者120例，随访24周。" * 5
                              + "全部患者符合结缔组织病分类标准。" * 2, encoding="utf-8")
    (d / "ch2.md").write_text("第5章：风湿病组的影像学评估显示进展。" * 5
                              + "队列包含胶原病患者亚组分析。" * 2, encoding="utf-8")
    return d


class TestProject(unittest.TestCase):
    def test_full_run_artifacts(self):
        d = _make_project()
        outdir = d / "_project"
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_project.py"),
                            str(d), "--outdir", str(outdir)],
                           capture_output=True, text=True, timeout=600,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stderr[-300:])
        # 逐文件 workflow 产物落盘
        self.assertTrue((outdir / "ch1.workflow.json").is_file())
        self.assertTrue((outdir / "ch2.workflow.md").is_file())
        # 摘要与总览
        r = json.loads((outdir / "project_summary.json").read_text(encoding="utf-8"))
        self.assertEqual(r["aggregate"]["files"], 2)
        self.assertEqual(r["aggregate"]["scored"], 2)
        self.assertEqual(r["aggregate"]["inconsistent_concepts"], 2)
        h = (outdir / "project_overview.html").read_text(encoding="utf-8")
        for block in ("项目自查总览", "逐文件总览", "跨文件术语不一致", "学术诚信"):
            self.assertIn(block, h)
        self.assertIn("不构成任何合规证明", h)

    def test_failure_isolation(self):
        """坏文件只损失一行，项目继续。"""
        d = _make_project()
        (d / "bad.docx").write_bytes(b"PK\x03\x04corrupted-not-real")
        outdir = d / "_project"
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_project.py"),
                            str(d), "--outdir", str(outdir), "--json"],
                           capture_output=True, text=True, timeout=600,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 0, p.stderr[-300:])
        r = json.loads(p.stdout)
        self.assertEqual(r["aggregate"]["failed"], 1)
        self.assertEqual(r["aggregate"]["scored"], 2)
        err_rows = [x for x in r["per_file"] if "error" in x]
        self.assertEqual(len(err_rows), 1)
        self.assertNotIn("Traceback", json.dumps(r))

    def test_single_file_exit_2(self):
        d = Path(tempfile.mkdtemp(prefix="ppp6900b_"))
        (d / "only.md").write_text("足够长的文本内容。" * 40, encoding="utf-8")
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp_project.py"), str(d)],
                           capture_output=True, text=True, timeout=120,
                           encoding="utf-8")
        self.assertEqual(p.returncode, 2)
        self.assertIn("至少 2 份", p.stderr)


class TestWiring(unittest.TestCase):
    def test_pp_help_and_scenario(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("project", p.stdout)
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "scenarios", "项目"],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("项目级自查", p.stdout)

    def test_recommend_routes(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "recommend", "全稿自查项目"],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("project", p.stdout)

    def test_skill_and_faq_documented(self):
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("pp.py project", t, f"{f} 未记录 project")
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("pp.py project", t)

    def test_stdlib_only(self):
        import ast
        allowed = {"argparse", "datetime", "html", "json", "sys", "traceback", "pathlib"}
        tree = ast.parse((SCRIPTS / "pp_project.py").read_text(encoding="utf-8"))
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods.update(x.name.split(".")[0] for x in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods.add(node.module.split(".")[0])
        # 同包模块白名单：docx_text / pp_workflow / pp_errors / pp_term_consistency
        self.assertTrue(mods <= allowed | {"docx_text", "pp_workflow", "pp_errors",
                                           "pp_term_consistency"},
                        f"引入非白名单依赖: {mods - allowed}")


if __name__ == "__main__":
    unittest.main()
