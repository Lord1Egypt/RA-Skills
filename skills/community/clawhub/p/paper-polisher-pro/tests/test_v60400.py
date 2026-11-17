# -*- coding: utf-8 -*-
"""v6.4.0 契约测试（test_v60400）：批量自动补扫 / failed_files 清单 / tour 导览 / 快速开始样例引用。"""
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

_LONG = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。" * 6
         + "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。" * 4)


def _make_dir(n=2):
    d = Path(tempfile.mkdtemp(prefix="ppp6400_"))
    for i in range(n):
        (d / f"f{i}.txt").write_text(_LONG, encoding="utf-8")
    return d


def _run_batch(d, **kw):
    sys.path.insert(0, str(SCRIPTS))
    import ai_detector as ad
    import io, contextlib
    orig = ad.detect
    if "detect_fn" in kw:
        ad.detect = kw.pop("detect_fn")
    kw.setdefault("isolate", "off")  # v6.8.0: 隔离走子进程会绕过 detect 补丁——单测默认进程内
    try:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            ad.batch_detect(str(d), "json", None, **kw)
        import json
        return json.loads(buf.getvalue())
    finally:
        ad.detect = orig


class TestBatchRetry(unittest.TestCase):
    def test_transient_failure_self_heals(self):
        """首轮失败+补扫成功 → retried 标注，无 failed_files。"""
        d = _make_dir(2)
        calls = {"n": 0}

        def flaky(text, mode):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("transient hiccup")
            class R:
                overall_ai_score = 42.0
                overall_risk = "medium"
                language = "zh"
                degraded_mode = False
            return R()

        r = _run_batch(d, detect_fn=flaky)
        self.assertEqual(r["aggregate"]["failed"], 0)
        self.assertNotIn("failed_files", r)
        hit = [x for x in r["files"] if x.get("retried")]
        self.assertEqual(len(hit), 1)
        self.assertEqual(hit[0]["attempts"], 2)
        self.assertEqual(hit[0]["overall_ai_score"], 42.0)

    def test_exhausted_retries_land_in_failed_files(self):
        """补扫耗尽仍失败 → failed_files 清单（含 attempts）+ 诊断指引。"""
        d = _make_dir(2)

        def always_fail(text, mode):
            raise RuntimeError("persistent corrupt")

        r = _run_batch(d, detect_fn=always_fail)
        self.assertEqual(r["aggregate"]["failed"], 2)
        self.assertEqual(len(r["failed_files"]), 2)
        self.assertTrue(all(f["attempts"] == 2 for f in r["failed_files"]))
        self.assertIn("failed_hint", r)
        self.assertIn("pp.py detect", r["failed_hint"])

    def test_retries_zero_disables(self):
        """retries=0 关闭补扫 → 失败行只试 1 次、无 retried。"""
        d = _make_dir(1)

        def always_fail(text, mode):
            raise RuntimeError("boom")

        r = _run_batch(d, detect_fn=always_fail, retries=0)
        self.assertEqual(r["failed_files"][0]["attempts"], 1)
        self.assertNotIn("retried", r["files"][0])

    def test_circuit_tripped_skips_retry(self):
        """首轮熔断 → 不补扫（无 attempts 补扫标注、无 retried），circuit 字段在位。"""
        d = _make_dir(3)

        def always_fail(text, mode):
            raise RuntimeError("bad batch")

        r = _run_batch(d, detect_fn=always_fail, circuit=2)
        self.assertTrue(r["circuit"]["tripped"])
        self.assertEqual(r["circuit"]["skipped_remaining"], 1)
        # 补扫被跳过：错误行不带补扫轮数标注（attempts 只会是首轮默认值）
        self.assertTrue(all(x.get("attempts", 1) == 1 for x in r["files"]))
        self.assertTrue(all("retried" not in x for x in r["files"]))


class TestTour(unittest.TestCase):
    def test_tour_zh_runs(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "tour"],
                           capture_output=True, text=True, timeout=300)
        self.assertEqual(p.returncode, 0, p.stderr[-300:])
        self.assertIn("站 1/5", p.stdout)
        self.assertIn("站 5/5", p.stdout)
        self.assertIn("路线图小结", p.stdout)

    def test_tour_en_runs(self):
        env = dict(os.environ, PP_LANG="en")
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "tour"],
                           capture_output=True, text=True, timeout=300, env=env)
        self.assertEqual(p.returncode, 0, p.stderr[-300:])
        self.assertIn("Station 1/5", p.stdout)
        self.assertIn("Route map", p.stdout)

    def test_tour_reachable_via_recommend(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py"), "recommend", "功能太多不知从哪开始"],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("tour", p.stdout)


class TestQuickStartDocs(unittest.TestCase):
    def test_skill_quickstart_references_examples(self):
        t = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("examples/outputs", t)
        self.assertIn("--report report.html", t)  # 批量一条龙组合示例
        self.assertIn("--retries", t)

    def test_skill_zh_quickstart_references_examples(self):
        t = _docs.zh_text()
        self.assertIn("examples/outputs", t)
        self.assertIn("五站导览", t)

    def test_help_mentions_tour(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("tour", p.stdout)
        self.assertIn("五站导览", p.stdout)

    def test_faq_batch_retry_entry(self):
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("--retries", t)
        self.assertIn("failed_files", t)


class TestHygieneGate(unittest.TestCase):
    """泄漏红线锁（v6.4.0 起随包）：内部编号/内网 IP/内部系统痕迹不进随包文件。

    禁词一律拼接构造（防打包闸把本文件的断言串自身当命中——自指问题）。"""

    LEAK = ("PROP-" + "2026", "LES-" + "2026", "192.168" + ".",
            "note_178" + "8", "note_179" + "8",
            "归" + "墟", "Agent" + "Ops", "agent" + "ops",
            "localhost:517" + "3", "localhost:800" + "1")

    def test_examples_outputs_clean(self):
        out = PKG / "examples" / "outputs"
        for f in sorted(out.iterdir()):
            if f.suffix.lower() not in (".json", ".md", ".html", ".txt"):
                continue
            t = f.read_text(encoding="utf-8", errors="ignore")
            for pat in self.LEAK:
                self.assertNotIn(pat, t, f"{f.name} 含泄漏模式『{pat}』")

    def test_scripts_comments_clean(self):
        for f in (PKG / "scripts").glob("*.py"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            for pat in self.LEAK:
                self.assertNotIn(pat, t, f"{f.name} 含泄漏模式『{pat}』")


if __name__ == "__main__":
    unittest.main()
