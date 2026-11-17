# -*- coding: utf-8 -*-
"""v6.6.0 契约测试（test_v60600）：检测证据报告 + 多文档术语一致性。"""
import json
import os
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

_AI_TEXT = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
            "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
            "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
            "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
            "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")


def _run(args, timeout=300):
    return subprocess.run([sys.executable] + args, capture_output=True,
                          text=True, timeout=timeout, encoding="utf-8",
                          errors="replace")


class TestEvidenceReport(unittest.TestCase):
    def test_dual_output_with_fixed_statements(self):
        tmp = Path(tempfile.mkdtemp(prefix="ppp_ev_"))
        src = tmp / "draft.txt"
        src.write_text(_AI_TEXT, encoding="utf-8")
        outdir = tmp / "evidence"
        r = _run([str(SCRIPTS / "pp_evidence_report.py"), str(src),
                  "--outdir", str(outdir)])
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        h = (outdir / "draft.evidence.html").read_text(encoding="utf-8")
        m = (outdir / "draft.evidence.md").read_text(encoding="utf-8")
        for block in ("报告定位", "特征证据明细", "段落分级", "局限声明",
                      "学术诚信声明", "复现信息"):
            self.assertIn(block, h, f"HTML 缺区块: {block}")
        self.assertIn("不构成「未使用 AI」的任何证明", h)
        self.assertIn("不构成「未使用 AI」的任何证明", m)
        self.assertIn("2631df3d388b", h)  # 监督模型指纹（签发注册表口径）
        self.assertIn("逐特征", m)

    def test_short_text_ironrule_exit_2(self):
        tmp = Path(tempfile.mkdtemp(prefix="ppp_ev2_"))
        src = tmp / "short.txt"
        src.write_text("太短了。", encoding="utf-8")
        r = _run([str(SCRIPTS / "pp_evidence_report.py"), str(src)])
        self.assertEqual(r.returncode, 2)
        self.assertIn("铁律", r.stderr)

    def test_missing_file_exit_2(self):
        r = _run([str(SCRIPTS / "pp_evidence_report.py"), "/no/such/file.txt"])
        self.assertEqual(r.returncode, 2)


class TestTermConsistency(unittest.TestCase):
    def _make_pair(self):
        d = Path(tempfile.mkdtemp(prefix="ppp_tc_"))
        (d / "ch1.md").write_text("本研究纳入风湿免疫病患者120例，随访24周。" * 5
                                  + "全部患者符合结缔组织病分类标准。" * 2, encoding="utf-8")
        (d / "ch2.md").write_text("第5章：风湿病组的影像学评估显示进展。" * 5
                                  + "队列包含胶原病患者亚组分析。" * 2, encoding="utf-8")
        return d

    def test_inconsistent_concepts_with_recommendation(self):
        d = self._make_pair()
        r = _run([str(SCRIPTS / "pp_term_consistency.py"), str(d), "--json"])
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        j = json.loads(r.stdout)
        inc = [m for m in j["matrix"] if m["inconsistent"]]
        self.assertEqual(len(inc), 2)
        for m in inc:
            self.assertEqual(m["recommend"], m["concept"])  # 标准名在场→推荐标准名
            self.assertEqual(m["basis"], "库标准名")
        self.assertEqual(j["aggregate"]["files"], 2)
        self.assertEqual(j["aggregate"]["inconsistent_concepts"], 2)

    def test_text_output_shows_advice(self):
        d = self._make_pair()
        r = _run([str(SCRIPTS / "pp_term_consistency.py"), str(d)])
        self.assertIn("跨文件不一致 2 个", r.stdout)
        self.assertIn("建议统一为「风湿免疫病」", r.stdout)
        self.assertIn("只覆盖库内概念", r.stdout)  # 诚实边界固定输出

    def test_html_matrix_renders(self):
        d = self._make_pair()
        out = d / "matrix.html"
        r = _run([str(SCRIPTS / "pp_term_consistency.py"), str(d), "--html", str(out)])
        self.assertEqual(r.returncode, 0, r.stderr[-200:])
        h = out.read_text(encoding="utf-8")
        self.assertIn("跨文件不一致", h)
        self.assertIn("风湿免疫病", h)
        self.assertIn("学术诚信", h)

    def test_single_file_exit_2(self):
        d = Path(tempfile.mkdtemp(prefix="ppp_tc1_"))
        (d / "only.md").write_text("足够长的文本。" * 40, encoding="utf-8")
        r = _run([str(SCRIPTS / "pp_term_consistency.py"), str(d)])
        self.assertEqual(r.returncode, 2)
        self.assertIn("至少两份", r.stderr)


class TestWiring(unittest.TestCase):
    def test_pp_help_lists_both(self):
        p = _run([str(SCRIPTS / "pp.py")])
        self.assertIn("evidence", p.stdout)
        self.assertIn("term-project", p.stdout)

    def test_recommend_routes(self):
        p = _run([str(SCRIPTS / "pp.py"), "recommend", "被质疑AI写作要说明材料"])
        self.assertIn("evidence", p.stdout)
        p = _run([str(SCRIPTS / "pp.py"), "recommend", "学位论文章节术语统一"])
        self.assertIn("term-project", p.stdout)

    def test_skill_quickstart_documents_both(self):
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("pp.py evidence", t, f"{f} 缺 evidence")
            self.assertIn("pp.py term-project", t, f"{f} 缺 term-project")

    def test_faq_documents_boundary(self):
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("term-project", t)
        self.assertIn("不构成「未使用 AI」的任何证明", t)

    def test_new_scripts_stdlib_only(self):
        import ast
        allowed = {"argparse", "html", "json", "os", "re", "subprocess", "sys",
                   "tempfile", "datetime", "pathlib"}
        for name in ("pp_evidence_report.py", "pp_term_consistency.py"):
            tree = ast.parse((SCRIPTS / name).read_text(encoding="utf-8"))
            mods = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    mods.update(x.name.split(".")[0] for x in node.names)
                elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                    mods.add(node.module.split(".")[0])
        # pp_term_consistency 同包 import term_check（包内模块，白名单单列）
        self.assertTrue(mods <= allowed | {"term_check", "docx_text"},
                        f"{name} 引入非白名单依赖: {mods - allowed}")


if __name__ == "__main__":
    unittest.main()
