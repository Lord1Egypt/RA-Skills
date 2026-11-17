"""MCP stdio 协议端到端测试。"""
import json, subprocess, sys
from pathlib import Path

ws = r"H:\ai\workspace\工具项目\memoryguard\tests\fixtures\workspace"

reqs = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "memoryguard_audit", "arguments": {"workspace": ws}}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "memoryguard_open", "arguments": {"workspace": ws}}},
]
stdin = "\n".join(json.dumps(r) for r in reqs) + "\n"
p = subprocess.run([sys.executable, "-m", "memoryguard.mcp_server"], input=stdin, capture_output=True, text=True)
if p.stderr:
    print("stderr:", p.stderr[:500])
for line in p.stdout.strip().splitlines():
    d = json.loads(line)
    rid = d.get("id")
    if "result" in d:
        r = d["result"]
        if "content" in r:
            print(f"id={rid} tools/call OK: {r['content'][0]['text'][:100]}")
        elif "tools" in r:
            print(f"id={rid} tools/list OK: {len(r['tools'])} tools")
        elif "serverInfo" in r:
            print(f"id={rid} initialize OK: {r['serverInfo']}")
        else:
            print(f"id={rid} OK: {str(r)[:100]}")
    elif "error" in d:
        print(f"id={rid} ERROR: {d['error']}")
