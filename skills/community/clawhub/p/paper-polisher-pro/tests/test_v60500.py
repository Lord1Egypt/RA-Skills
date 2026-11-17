# -*- coding: utf-8 -*-
"""v6.5.0 契约测试（test_v60500）：MCP stdio server 协议/工具/零依赖 + 反模式↔FAQ 去重。"""
import ast
import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

PKG = Path(__file__).resolve().parent.parent
import sys as _sys
_sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs
SCRIPTS = PKG / "scripts"
SERVER = SCRIPTS / "pp_mcp_server.py"

_TEXT = ("值得注意的是，随着人工智能技术的快速发展，其在医疗领域的应用日益受到关注。"
         "具体而言，AI 不仅能够提高诊断效率，而且可以优化治疗方案的制定。"
         "然而，与此同时，我们在享受技术红利的同时也面临着诸多挑战。"
         "在一定程度上，数据安全问题的存在对行业发展产生了一定的制约。"
         "综上所述，本研究为该领域的进一步探索提供了一定的参考价值。")


def _session(msgs, timeout=600):
    """发一轮完整 MCP 会话，返回按 id 索引的回复字典。"""
    lines = [json.dumps(m, ensure_ascii=False) for m in msgs]
    p = subprocess.run([sys.executable, str(SERVER)], input="\n".join(lines),
                       capture_output=True, text=True, timeout=timeout,
                       encoding="utf-8")
    replies = {}
    for ln in p.stdout.strip().splitlines():
        if not ln.strip():
            continue
        d = json.loads(ln)
        if d.get("id") is not None:
            replies[d["id"]] = d
    return replies, p


class TestProtocol(unittest.TestCase):
    def test_initialize_handshake(self):
        replies, p = _session([
            {"jsonrpc": "2.0", "id": 1, "method": "initialize",
             "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                        "clientInfo": {"name": "t", "version": "0"}}},
            {"jsonrpc": "2.0", "method": "notifications/initialized"},
        ])
        self.assertEqual(p.returncode, 0, p.stderr[-200:])
        r = replies[1]["result"]
        self.assertEqual(r["protocolVersion"], "2024-11-05")
        self.assertEqual(r["serverInfo"]["name"], "paper-polisher-pro")
        self.assertIn("tools", r["capabilities"])
        # 通知不得产生回复
        self.assertEqual(len(replies), 1)

    def test_tools_list_eight_with_schema(self):
        replies, _ = _session([{"jsonrpc": "2.0", "id": 2, "method": "tools/list"}])
        tools = replies[2]["result"]["tools"]
        names = [t["name"] for t in tools]
        for want in ("pp_detect", "pp_fix_suggest", "pp_style_norm", "pp_term_check",
                     "pp_workflow", "pp_explain", "pp_faq", "pp_doctor"):
            self.assertIn(want, names)
        for t in tools:
            self.assertIn("inputSchema", t)
            self.assertIn("description", t)

    def test_unknown_method_and_tool(self):
        replies, _ = _session([
            {"jsonrpc": "2.0", "id": 1, "method": "bogus/method"},
            {"jsonrpc": "2.0", "id": 2, "method": "tools/call",
             "params": {"name": "nope", "arguments": {}}},
        ])
        self.assertEqual(replies[1]["error"]["code"], -32601)
        self.assertEqual(replies[2]["error"]["code"], -32602)

    def test_bad_json_gets_parse_error(self):
        p = subprocess.run([sys.executable, str(SERVER)], input="{broken",
                           capture_output=True, text=True, timeout=60,
                           encoding="utf-8")
        d = json.loads(p.stdout.strip().splitlines()[0])
        self.assertEqual(d["error"]["code"], -32700)


class TestToolCalls(unittest.TestCase):
    """工具真跑。合并进两个 session：MCP server 每会话各引擎加载一次，
    分散 session 会成倍放大模型加载开销（smoke 单测步超时的主因）。"""

    def test_session_a_detect_faq_doctor(self):
        replies, _ = _session([
            {"jsonrpc": "2.0", "id": 3, "method": "tools/call",
             "params": {"name": "pp_detect", "arguments": {"text": _TEXT}}},
            {"jsonrpc": "2.0", "id": 4, "method": "tools/call",
             "params": {"name": "pp_detect", "arguments": {"text": "太短了。"}}},
            {"jsonrpc": "2.0", "id": 5, "method": "tools/call",
             "params": {"name": "pp_faq", "arguments": {"query": "医学"}}},
            {"jsonrpc": "2.0", "id": 6, "method": "tools/call",
             "params": {"name": "pp_doctor", "arguments": {}}}],
            timeout=420)
        out = replies[3]["result"]["content"][0]["text"]
        j = json.loads(out.split("\n\n(")[0])
        self.assertIsInstance(j["overall_ai_score"], (int, float))
        self.assertIn(j["overall_risk"], ("high", "medium", "low"))
        short = json.loads(replies[4]["result"]["content"][0]["text"].split("\n\n(")[0])
        self.assertEqual(short["overall_risk"], "unknown")  # 短文本铁律
        self.assertIn("医学", replies[5]["result"]["content"][0]["text"])
        self.assertIn("doctor", replies[6]["result"]["content"][0]["text"])

    def test_session_b_fix_norm_term_workflow(self):
        replies, _ = _session([
            {"jsonrpc": "2.0", "id": 7, "method": "tools/call",
             "params": {"name": "pp_fix_suggest",
                        "arguments": {"text": _TEXT, "top": 3}}},
            {"jsonrpc": "2.0", "id": 8, "method": "tools/call",
             "params": {"name": "pp_style_norm", "arguments": {"text": _TEXT}}},
            {"jsonrpc": "2.0", "id": 9, "method": "tools/call",
             "params": {"name": "pp_term_check", "arguments": {"text": _TEXT}}},
            {"jsonrpc": "2.0", "id": 10, "method": "tools/call",
             "params": {"name": "pp_workflow", "arguments": {"text": _TEXT}}}],
            timeout=600)
        for i in (7, 8, 9):
            self.assertNotIn("mcp_error", replies[i]["result"]["content"][0]["text"],
                             f"tool id={i} errored")
        wf_raw = replies[10]["result"]["content"][0]["text"]
        self.assertNotIn("mcp_error", wf_raw)
        wf = json.loads(wf_raw.split("\n\n(")[0])  # 合法 JSON（完整或摘要）
        if wf.get("truncated_for_mcp"):
            self.assertIn("plain_reading", wf)
            self.assertIn("【结论】", wf["plain_reading"])
        else:
            self.assertIn("detect", wf)

    def test_explain_with_real_report_json(self):
        wf = json.loads((PKG / "examples" / "outputs" / "workflow_sample.json")
                        .read_text(encoding="utf-8"))
        replies, _ = _session([
            {"jsonrpc": "2.0", "id": 11, "method": "tools/call",
             "params": {"name": "pp_explain",
                        "arguments": {"report_json": json.dumps(wf, ensure_ascii=False)}}}],
            timeout=300)
        exp = replies[11]["result"]["content"][0]["text"]
        for kw in ("【结论】", "【证据】", "【行动清单】"):
            self.assertIn(kw, exp)


class TestZeroDependency(unittest.TestCase):
    def test_imports_are_stdlib_only(self):
        tree = ast.parse(SERVER.read_text(encoding="utf-8"))
        mods = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods.update(a.name.split(".")[0] for a in node.names)
            elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
                mods.add(node.module.split(".")[0])
        allowed = {"io", "json", "os", "subprocess", "sys", "tempfile", "pathlib",
                   "http", "argparse"}  # v7.2.0: http.server 回环监听（pp_verify 白名单+绑定断言管着）
        self.assertTrue(mods <= allowed, f"引入了非标准库依赖: {mods - allowed}")


class TestDocs(unittest.TestCase):
    def test_pp_help_mentions_mcp(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "pp.py")],
                           capture_output=True, text=True, timeout=60)
        self.assertIn("mcp", p.stdout)

    def test_skill_both_languages_document_mcp(self):
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("pp_mcp_server.py", t, f"{f} 缺 MCP 配置节")
            self.assertIn("mcpServers", t)

    def test_dedup_crosspointers(self):
        t = (PKG / "references" / "faq.md").read_text(encoding="utf-8")
        self.assertIn("阅读分层", t)
        self.assertIn("反模式", t)
        for f in _docs.DOCS:
            t = (PKG / f).read_text(encoding="utf-8")
            self.assertIn("references/faq.md", t)


if __name__ == "__main__":
    unittest.main()
