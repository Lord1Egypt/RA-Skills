# -*- coding: utf-8 -*-
"""v6.1.0 契约测试（test_v60100）：报告解读器 / 错误词典扩展 / quickstart 超时 /
架构外迁 / 最佳实践指南 / 稳定性声明。"""
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
PY = sys.executable


def _run(*args, timeout=120, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    return subprocess.run([PY, *map(str, args)], capture_output=True,
                          text=True, timeout=timeout, cwd=str(PKG), env=env)


class TestExplain(unittest.TestCase):
    """报告解读器：结论/证据/行动清单三段人话。"""

    def test_explain_workflow_sample(self):
        r = _run(SCRIPTS / "pp_explain.py", PKG / "examples" / "outputs" / "workflow_sample.json")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        for kw in ("【结论】", "【证据】", "【行动清单】", "档位"):
            self.assertIn(kw, r.stdout, f"解读缺段: {kw}")
        self.assertIn("pp.py fix", r.stdout)
        self.assertNotIn("Traceback", r.stderr)

    def test_explain_rejects_non_report(self):
        junk = Path(tempfile.mkdtemp(prefix="expl_")) / "junk.json"
        junk.write_text('{"hello": 1}', encoding="utf-8")
        r = _run(SCRIPTS / "pp_explain.py", junk)
        self.assertEqual(r.returncode, 2)
        self.assertIn("pp.py workflow", r.stderr)

    def test_explain_registered_and_reachable(self):
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        self.assertIn('"explain"', src)
        r = _run(SCRIPTS / "pp.py", "explain",
                 PKG / "examples" / "outputs" / "workflow_sample.json")
        self.assertEqual(r.returncode, 0, r.stderr[-300:])
        self.assertIn("【结论】", r.stdout)
        # recommend 路由可达
        r2 = _run(SCRIPTS / "pp.py", "recommend", "帮我解读这份报告，下一步做什么")
        self.assertIn("explain", r2.stdout)


class TestErrorGlossary(unittest.TestCase):
    """错误词典扩展：AST/漂移/签发/门禁层 术语人话化。"""

    def test_render_covers_new_phrases(self):
        sys.path.insert(0, str(SCRIPTS))
        from pp_errors import render
        cases = [
            (Exception("AST 网络命中 2 处"), "结构化自证"),
            (Exception("基线漂移: AUROC 下降"), "pp_doctor"),
            (Exception("REJECTED: 模型指纹不在作者签发注册表中"), "pp_setup"),
            (Exception("层2解析失败(rc=124)"), "中性分"),
        ]
        for exc, expect in cases:
            title, nxt = render(exc)
            self.assertIn(expect, title + nxt, f"{exc} 未人话化")

    def test_verify_wired(self):
        src = (SCRIPTS / "pp_verify.py").read_text(encoding="utf-8")
        self.assertIn("pp_errors", src)

    def test_passthrough_pointer(self):
        r = _run(SCRIPTS / "pp.py", "detect", "/tmp/definitely_not_here_610.txt")
        self.assertEqual(r.returncode, 2)
        self.assertIn("契约", r.stderr)


class TestStabilityStatement(unittest.TestCase):
    """超时与重试：quickstart 子步 180s 保护 + 稳定性声明入册。"""

    def test_quickstart_timeouts(self):
        src = (SCRIPTS / "pp.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(src.count("timeout=180"), 3)

    def test_gate_layer_retry_documented(self):
        src = (SCRIPTS / "deai_gate.py").read_text(encoding="utf-8")
        self.assertIn("timeout=120", src)  # 层级 120s 超时 + 一次重试（v4.9.0）


class TestProgressiveMove(unittest.TestCase):
    """架构/保鲜外迁 references/，SKILL 保留摘要+链接。"""

    def test_architecture_file_exists(self):
        ref = PKG / "references" / "architecture.md"
        self.assertTrue(ref.is_file())
        content = ref.read_text(encoding="utf-8")
        for kw in ("ai_detector.py", "layers_surface.py", "指纹保鲜", "Architecture"):
            self.assertIn(kw, content, f"外迁文件缺: {kw}")

    def test_skill_has_summary_and_link(self):
        for doc in _docs.DOCS:
            t = (PKG / doc).read_text(encoding="utf-8")
            self.assertIn("references/architecture.md", t, f"{doc} 缺外迁链接")
            self.assertIn("references/best-practices.md", t, f"{doc} 缺最佳实践链接")
            # 深水区已不在主文档（EN 架构大块 / ZH v3 架构大块）
            self.assertNotIn("layers_surface.py", t, f"{doc} 仍残留架构大块")


class TestBestPractices(unittest.TestCase):
    """最佳实践指南：场景化怎么用。"""

    def test_file_covers_key_scenarios(self):
        bp = PKG / "references" / "best-practices.md"
        self.assertTrue(bp.is_file())
        t = bp.read_text(encoding="utf-8")
        for kw in ("journal", "段落归因", "rewrite-check", "熔断", "integrity"):
            self.assertIn(kw, t, f"最佳实践缺: {kw}")

    def test_examples_readme_scenarios(self):
        r = (PKG / "examples" / "outputs" / "README.md").read_text(encoding="utf-8")
        self.assertIn("场景", r)


if __name__ == "__main__":
    unittest.main()
