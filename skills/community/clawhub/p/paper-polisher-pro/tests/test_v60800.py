# -*- coding: utf-8 -*-
"""v6.8.0 契约测试（test_v60800）：批量子进程隔离 / 错误话语扩展 / Traceback 残留锁。"""
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

_LONG = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。" * 6
         + "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。" * 4)


def _make_dir(n=2):
    d = Path(tempfile.mkdtemp(prefix="ppp6800_"))
    for i in range(n):
        (d / f"f{i}.txt").write_text(_LONG, encoding="utf-8")
    return d


def _batch(d, flag, timeout=600):
    p = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"),
                        "--batch", str(d), "--isolate", flag, "--format", "json"],
                       capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8")
    return json.loads(p.stdout)


class TestIsolation(unittest.TestCase):
    def test_on_off_deterministic_equivalence(self):
        """隔离与进程内必须逐位一致（worker=CLI 同源，零新打分代码）。"""
        d = _make_dir(2)
        iso = _batch(d, "on")
        inproc = _batch(d, "off")
        self.assertEqual(iso["aggregate"]["failed"], 0)
        s_iso = {r["file"]: r["overall_ai_score"] for r in iso["files"]}
        s_in = {r["file"]: r["overall_ai_score"] for r in inproc["files"]}
        self.assertEqual(s_iso, s_in)
        self.assertIn("on", iso["worker_isolation"])
        self.assertIn("off", inproc["worker_isolation"])

    def test_corrupt_docx_friendly_passthrough(self):
        """rc=2 的 worker 友好错误透传，不包装成『worker 崩溃』。"""
        d = Path(tempfile.mkdtemp(prefix="ppp6800b_"))
        (d / "ok.txt").write_text(_LONG, encoding="utf-8")
        (d / "bad.docx").write_bytes(b"PK\x03\x04corrupted-not-real")
        r = _batch(d, "on")
        self.assertEqual(r["aggregate"]["failed"], 1)
        err = r["failed_files"][0]["error"]
        self.assertNotIn("worker 崩溃", err, "输入类错误不应报崩溃")
        self.assertTrue(err)  # 透传了友好标题

    def test_isolation_field_in_result(self):
        d = _make_dir(1)
        r = _batch(d, "on")
        self.assertIn("worker_isolation", r)


class TestErrorGlossary(unittest.TestCase):
    def test_worker_crash_rendering(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_errors as pe
        title, nxt = pe.render(RuntimeError("worker 崩溃: 退出码 -11，信号 11"))
        self.assertIn("隔离", title)
        self.assertIn("ai_detector.py", nxt)

    def test_encoding_rendering(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_errors as pe
        title, _ = pe.render(UnicodeDecodeError("utf-8", b"", 0, 1, "bad"))
        self.assertIn("编码", title)

    def test_timeout_rendering(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_errors as pe
        import subprocess as sp
        title, _ = pe.render(sp.TimeoutExpired("x", 600))
        self.assertIn("超时", title)


class TestResidueLock(unittest.TestCase):
    def test_no_traceback_leak(self):
        """技术词残留锁：任何脚本源码不得出现 Traceback（裸栈泄漏只可能来自 print_exc）。"""
        for f in (PKG / "scripts").glob("*.py"):
            t = f.read_text(encoding="utf-8", errors="ignore")
            self.assertNotIn("Traceback", t, f"{f.name} 疑似裸栈泄漏")
            self.assertNotIn("print_exc", t, f"{f.name} 使用了裸异常打印")

    def test_cli_isolate_flag(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "ai_detector.py"), "--help"],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("--isolate", p.stdout)


class TestDocs(unittest.TestCase):
    def test_skill_documents_isolation(self):
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("--isolate", t, f"{f} 未记录隔离模式")

    def test_faq_mentions_isolation(self):
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("隔离", t)


if __name__ == "__main__":
    unittest.main()
