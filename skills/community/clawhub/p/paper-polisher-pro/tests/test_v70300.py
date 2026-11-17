# -*- coding: utf-8 -*-
"""v7.3.0 契约测试（test_v70300）：MCP 三原语 / 双语标题闸 / requirements 一致 / SH 形态注记。"""
import json
import subprocess
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import _docs

PKG = Path(__file__).resolve().parent.parent
SCRIPTS = PKG / "scripts"


def _session(msgs):
    inp = "\n".join(json.dumps(m, ensure_ascii=False) for m in msgs)
    p = subprocess.run([sys.executable, str(SCRIPTS / "pp_mcp_server.py")],
                       input=inp, capture_output=True, text=True, timeout=120,
                       encoding="utf-8")
    out = {}
    for ln in p.stdout.strip().splitlines():
        if ln.strip():
            d = json.loads(ln)
            if d.get("id") is not None:
                out[d["id"]] = d
    return out


class TestMcpThreePrimitives(unittest.TestCase):
    def test_capabilities_declares_all_three(self):
        r = _session([{"jsonrpc": "2.0", "id": 1, "method": "initialize",
                       "params": {"protocolVersion": "2024-11-05"}}])
        caps = r[1]["result"]["capabilities"]
        self.assertEqual(sorted(caps.keys()), ["prompts", "resources", "tools"])

    def test_resources_list_and_read(self):
        r = _session([
            {"jsonrpc": "2.0", "id": 2, "method": "resources/list"},
            {"jsonrpc": "2.0", "id": 3, "method": "resources/read",
             "params": {"uri": "ppp://current-caliber"}},
            {"jsonrpc": "2.0", "id": 4, "method": "resources/read",
             "params": {"uri": "ppp://nope"}},
        ])
        uris = [x["uri"] for x in r[2]["result"]["resources"]]
        self.assertEqual(len(uris), 3)
        self.assertTrue(all(u.startswith("ppp://") for u in uris))
        txt = r[3]["result"]["contents"][0]["text"]
        self.assertIn("v35ctl_oldgen.json", txt)  # 现行基线真实入文
        self.assertEqual(r[4]["error"]["code"], -32602)

    def test_prompts_list_and_render(self):
        r = _session([
            {"jsonrpc": "2.0", "id": 5, "method": "prompts/list"},
            {"jsonrpc": "2.0", "id": 6, "method": "prompts/get",
             "params": {"name": "submission-precheck",
                        "arguments": {"manuscript": "thesis.docx"}}},
            {"jsonrpc": "2.0", "id": 7, "method": "prompts/get",
             "params": {"name": "nope"}},
        ])
        names = [x["name"] for x in r[5]["result"]["prompts"]]
        self.assertEqual(names, ["paper-selfcheck", "rewrite-loop", "submission-precheck"])
        msg = r[6]["result"]["messages"][0]["content"]["text"]
        self.assertIn("thesis.docx", msg)
        self.assertIn("pp_workflow", msg)  # 模板含可执行命令
        self.assertEqual(r[7]["error"]["code"], -32602)


class TestConsistency(unittest.TestCase):
    def test_bilingual_title_parity(self):
        import re
        en = re.search(r"^# (.+)$", (PKG / "SKILL.md").read_text(encoding="utf-8"), re.M).group(1)
        zh = re.search(r"^# (.+)$", _docs.zh_text(encoding="utf-8"), re.M).group(1)
        self.assertEqual(en, zh)
        self.assertNotIn("v3", en)

    def test_requirements_declares_regex(self):
        req = (PKG / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("regex>=", req)
        sk = (PKG / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("onnxruntime regex", sk)  # pip 安装行与 requirements 同源

    def test_sh_form_note_in_skillzh(self):
        t = _docs.zh_text(encoding="utf-8")
        self.assertIn("发布形态说明", t)
        self.assertIn("SKILL_ZH.md", t)


if __name__ == "__main__":
    unittest.main()
