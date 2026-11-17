# -*- coding: utf-8 -*-
"""v7.2.0 契约测试（test_v70200）：MCP HTTP transport / 版本单一来源 / AUROC 清尾 / 口径导航。"""
import json
import os
import subprocess
import sys
import time
import unittest
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"

_TEXT = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
         "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
         "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
         "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
         "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")


def _post(port, payload, timeout=120):
    req = urllib.request.Request(f"http://127.0.0.1:{port}/mcp",
                                 data=json.dumps(payload, ensure_ascii=False).encode(),
                                 headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=timeout).read())


class TestHttpTransport(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8831 + (os.getpid() % 400)  # 并行套件防端口撞（PID 散列）
        cls.proc = subprocess.Popen(
            [sys.executable, str(SCRIPTS / "pp_mcp_server.py"),
             "--transport", "http", "--port", str(cls.port)],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        # 等监听就绪
        for _ in range(30):
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{cls.port}/health", timeout=2)
                break
            except Exception:
                time.sleep(0.5)
        else:
            raise RuntimeError("HTTP server 未在 15s 内就绪")

    @classmethod
    def tearDownClass(cls):
        cls.proc.terminate()
        cls.proc.wait(timeout=10)

    def test_health_probe_reports_pkg_version(self):
        d = json.loads(urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/health", timeout=10).read())
        self.assertTrue(d["ok"])
        pkg = json.loads((PKG / "skill.json").read_text(encoding="utf-8"))["version"]
        self.assertEqual(d["version"], pkg, "server 自报版本必须跟随 skill.json")

    def test_full_session_over_http(self):
        r1 = _post(self.port, {"jsonrpc": "2.0", "id": 1, "method": "initialize",
                               "params": {"protocolVersion": "2024-11-05",
                                          "capabilities": {}}})
        self.assertEqual(r1["result"]["serverInfo"]["name"], "paper-polisher-pro")
        r2 = _post(self.port, {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                               "params": {"name": "pp_detect",
                                          "arguments": {"text": _TEXT}}})
        j = json.loads(r2["result"]["content"][0]["text"].split("\n\n(")[0])
        self.assertEqual(j["overall_ai_score"], 98.1)  # 与 stdio/CLI 逐位一致
        r3 = _post(self.port, {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                               "params": {"name": "pp_detect",
                                          "arguments": {"text": "太短。"}}})
        s = json.loads(r3["result"]["content"][0]["text"].split("\n\n(")[0])
        self.assertEqual(s["overall_risk"], "unknown")

    def test_pp_help_documents_transport(self):
        t = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("--transport http", t)
        self.assertIn("127.0.0.1", t)


class TestVersionSourcing(unittest.TestCase):
    def test_server_version_follows_skilljson(self):
        sys.path.insert(0, str(SCRIPTS))
        import pp_mcp_server as m
        pkg = json.loads((PKG / "skill.json").read_text(encoding="utf-8"))["version"]
        self.assertEqual(m.SERVER_VERSION, pkg)

    def test_no_hardcoded_version_in_server(self):
        import re
        t = (SCRIPTS / "pp_mcp_server.py").read_text(encoding="utf-8")
        self.assertIsNone(re.search(r'SERVER_VERSION\s*=\s*"6\.\d', t), "server 版本又硬编码了")


class TestCaliberGates(unittest.TestCase):
    def test_auroc_residue_zero(self):
        skj = (PKG / "skill.json").read_text(encoding="utf-8")
        zh = _docs.zh_text()  # 双语自适应（CH 英文包形态下本测试 skip）
        rd = (PKG / "README.md").read_text(encoding="utf-8")
        for name, t in (("skill.json", skj), ("SKILL_ZH", zh), ("README", rd)):
            self.assertNotIn("AUROC 1.0", t, f"{name} 仍有 AUROC 1.0 旧口径")
        self.assertIn("0.9998", zh)
        self.assertIn("0.9998", skj)

    def test_current_md_reconciles(self):
        cur = PKG / "eval" / "results" / "CURRENT.md"
        self.assertTrue(cur.is_file(), "口径导航缺失")
        t = cur.read_text(encoding="utf-8")
        for f in ("v35ctl_oldgen.json", "v35ctl_gen2026.json", "golden_detection.json"):
            self.assertIn(f, t)
            self.assertTrue((PKG / "eval" / "results" / f).is_file(), f"{f} 表内在位不符")
        self.assertIn("不得引用", t)  # 档案边界声明在位


if __name__ == "__main__":
    unittest.main()
