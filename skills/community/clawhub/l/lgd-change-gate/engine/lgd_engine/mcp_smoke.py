#!/usr/bin/env python3
"""mcp_smoke.py — drive the stdio MCP server once: initialize, tools/list,
tools/call judge_change (plus one denied unauthorized tool to prove L2).

Run from mvp/ :  python lgd_engine/mcp_smoke.py
Exit 0 only when tools/list returns 3 tools and judge_change returns a verdict.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> int:
    proc = subprocess.Popen(
        [sys.executable, str(HERE / "mcp_server.py")],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, cwd=str(HERE.parent),
    )
    requests = [
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
        {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {
            "name": "judge_change", "role": "read-only",
            "arguments": {"change_type": "label_correction",
                           "safety_impact": "none",
                           "recall_class": "none",
                           "predicate_unchanged": True}}},
        {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {
            "name": "merge_decision", "role": "read-only", "arguments": {}}},
    ]
    for req in requests:
        proc.stdin.write(json.dumps(req) + "\n")
    proc.stdin.flush()
    proc.stdin.close()

    ok = True
    for i in range(4):
        line = proc.stdout.readline()
        resp = json.loads(line)
        print(f"--- req id={i+1} -> resp ---")
        print(json.dumps(resp, ensure_ascii=False)[:400])
        if i == 1 and len(resp.get("result", {}).get("tools", [])) != 3:
            ok = False
        if i == 2:
            text = resp["result"]["content"][0]["text"]
            verdict = json.loads(text)["report"]["verdict"]
            print(f"    judge_change verdict = {verdict}")
            if verdict not in ("go", "hold", "reject"):
                ok = False
        if i == 3 and "error" not in resp:
            ok = False
    proc.wait(timeout=15)
    print("SMOKE:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
