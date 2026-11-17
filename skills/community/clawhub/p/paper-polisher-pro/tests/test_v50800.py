# -*- coding: utf-8 -*-
"""v5.8.0 契约测试（test_v50800）：可视化仪表盘 / recommend 路由 / 退出码契约 / 限制前置 / 文档收敛。"""
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


def _run_pp(*args, cwd=None):
    """跑 pp.py 子命令，返回 (returncode, stdout, stderr)。"""
    return subprocess.run([PY, str(SCRIPTS / "pp.py"), *args],
                          capture_output=True, text=True, cwd=cwd or str(PKG))


class TestVisualDashboard(unittest.TestCase):
    """pp_report_html.py：从真实样例渲染、零外部资源、转义安全。"""

    OUT_DIR = Path(tempfile.mkdtemp(prefix="t580_"))

    def _render(self, out_name, *inputs):
        out = self.OUT_DIR / out_name
        r = subprocess.run(
            [PY, str(SCRIPTS / "pp_report_html.py"),
             *[str(PKG / "examples" / "outputs" / i) for i in inputs],
             "-o", str(out)],
            capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        return out

    def test_render_from_samples(self):
        out = self._render("dash.html", "workflow_sample.json")
        html = out.read_text(encoding="utf-8")
        for section in ("段落分数分布", "段落热表", "句子级改写建议", "学术写作规范自查",
                        "四层门禁", "Findings Ledger", "学术诚信"):
            self.assertIn(section, html, f"仪表盘缺板块: {section}")

    def test_zero_external_resources(self):
        out = self._render("dash2.html", "workflow_sample.json")
        html = out.read_text(encoding="utf-8")
        for bad in ("<script src", "@import", "url(", "<link rel", "<iframe"):
            self.assertNotIn(bad, html, f"仪表盘含外部资源引用: {bad}")

    def test_mixed_inputs_autodetect(self):
        out = self._render("dash3.html", "detect_sample.json",
                           "fix_suggest_sample.json", "style_norm_llm_jargon_sample.json")
        html = out.read_text(encoding="utf-8")
        self.assertIn("段落分数分布", html)
        self.assertIn("句子级改写建议", html)
        self.assertIn("学术写作规范自查", html)

    def test_xss_escaped(self):
        d = json.load(open(PKG / "examples" / "outputs" / "detect_sample.json",
                           encoding="utf-8"))
        d["paragraph_scores"][0]["text"] = "<script>alert(1)</script> 注入探针"
        evil = self.OUT_DIR / "evil.json"
        json.dump(d, open(evil, "w", encoding="utf-8"), ensure_ascii=False)
        out = self.OUT_DIR / "evil.html"
        r = subprocess.run([PY, str(SCRIPTS / "pp_report_html.py"), str(evil),
                            "-o", str(out)], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn("<script>alert", out.read_text(encoding="utf-8"))

    def test_unrecognized_input_exit_2(self):
        junk = self.OUT_DIR / "junk.json"
        junk.write_text('{"hello": "world"}', encoding="utf-8")
        r = subprocess.run([PY, str(SCRIPTS / "pp_report_html.py"), str(junk),
                            "-o", str(self.OUT_DIR / "junk.html")],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, "不可识别输入应退出码 2")


class TestRecommendRouter(unittest.TestCase):
    """pp.py recommend：中文/英文场景命中与兜底。"""

    def test_route_reduce_ai(self):
        r = _run_pp("recommend", "帮我把这段的AI率降一降")
        self.assertEqual(r.returncode, 0)
        self.assertIn("fix", r.stdout)

    def test_route_detect(self):
        r = _run_pp("recommend", "查一下这篇文章的AI率")
        self.assertEqual(r.returncode, 0)
        self.assertIn("detect", r.stdout)

    def test_route_env(self):
        r = _run_pp("recommend", "环境报错了，模型跑不起来")
        self.assertEqual(r.returncode, 0)
        self.assertIn("doctor", r.stdout)

    def test_route_english(self):
        r = _run_pp("recommend", "detect the ai score of my paper")
        self.assertEqual(r.returncode, 0)
        self.assertIn("detect", r.stdout)

    def test_no_hit_fallback(self):
        r = _run_pp("recommend", "zzzqqq")
        self.assertEqual(r.returncode, 0)
        self.assertIn("workflow", r.stdout)


class TestExitCodeContract(unittest.TestCase):
    """退出码契约：0/1/2/3 在入口行为上锁定。"""

    def test_unknown_subcommand_exit_2(self):
        r = _run_pp("no-such-command")
        self.assertEqual(r.returncode, 2)

    def test_missing_file_exit_2(self):
        r = _run_pp("detect", "/tmp/definitely_not_here_580.txt")
        self.assertEqual(r.returncode, 2)

    def test_help_exit_0(self):
        r = _run_pp("--help")
        self.assertEqual(r.returncode, 0)
        self.assertIn("recommend", r.stdout)
        self.assertIn("退出码契约", r.stdout)

    def test_contract_documented(self):
        for doc in _docs.DOCS:
            t = (PKG / doc).read_text(encoding="utf-8")
            self.assertIn("5.8.0", t)
            self.assertTrue(("Exit-code contract" in t) or ("退出码契约" in t),
                            f"{doc} 缺退出码契约节")


class TestDocs(unittest.TestCase):
    """文档收敛：限制前置 / 残留清理 / 版本一致性 / 新命令入册。"""

    def test_top3_limits_callout(self):
        _sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertTrue("The three limits that matter most" in _sk
                        or "三条最重要的限制" in _sk)
        self.assertIn("三条最重要的限制",
                      _docs.zh_text())

    def test_stale_whatsnew_removed(self):
        en = (PKG / "SKILL.md").read_text(encoding="utf-8")
        zh = _docs.zh_text()
        self.assertNotIn("What's new in v4.9.0", en)
        self.assertNotIn("v4.9.0 更新内容", zh)
        self.assertNotIn("v5.4.0 更新内容", zh)

    def test_zh_history_slimmed(self):
        zh = _docs.zh_text()
        self.assertIn("v5.8.0", zh)
        self.assertNotIn("v3.7.0（2026-09-23 发布）", zh)  # 长列表已收敛
        self.assertNotIn("LES-", zh)  # 内部编号不入包

    def test_new_commands_registered(self):
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        self.assertIn('"html-report"', src)
        self.assertIn("recommend", src)
        self.assertTrue((SCRIPTS / "pp_report_html.py").is_file())

    def test_samples_complete(self):
        out = PKG / "examples" / "outputs"
        wf = json.load(open(out / "workflow_sample.json", encoding="utf-8"))
        for k in ("detect", "paragraphs", "style_norm", "findings_ledger", "engine_version"):
            self.assertIn(k, wf, f"workflow_sample 缺 {k}")
        sample_html = (out / "report_html_sample.html").read_text(encoding="utf-8")
        self.assertIn("学术诚信", sample_html)


if __name__ == "__main__":
    unittest.main()
