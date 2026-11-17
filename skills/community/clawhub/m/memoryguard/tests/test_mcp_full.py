"""MCP 全工具验证（8 个工具）。"""
import json, subprocess, sys

ws = r"H:\ai\workspace\工具项目\memoryguard\tests\fixtures\workspace"

reqs = [
    {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}},
    {"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
    {"jsonrpc": "2.0", "id": 3, "method": "tools/call", "params": {"name": "memoryguard_audit", "arguments": {"workspace": ws}}},
    {"jsonrpc": "2.0", "id": 4, "method": "tools/call", "params": {"name": "memoryguard_neuron_graph", "arguments": {"workspace": ws}}},
    {"jsonrpc": "2.0", "id": 5, "method": "tools/call", "params": {"name": "memoryguard_extract_memories", "arguments": {"workspace": ws}}},
]
stdin = "\n".join(json.dumps(r) for r in reqs) + "\n"
p = subprocess.run([sys.executable, "-m", "memoryguard.mcp_server"], input=stdin, capture_output=True, text=True)
if p.stderr:
    print("stderr:", p.stderr[:300])
print("=== MCP 响应 ===")
for line in p.stdout.strip().splitlines():
    d = json.loads(line)
    rid = d.get("id")
    if "result" in d:
        r = d["result"]
        if "tools" in r:
            print(f"\nid={rid} tools/list: {len(r['tools'])} 个工具")
            for t in r["tools"]:
                print(f"  - {t['name']}")
        elif "serverInfo" in r:
            print(f"\nid={rid} initialize: {r['serverInfo']}")
        elif "content" in r:
            text = r["content"][0]["text"][:200]
            print(f"\nid={rid} tools/call OK:\n{text}")
        else:
            print(f"\nid={rid} OK: {str(r)[:100]}")
    elif "error" in d:
        print(f"\nid={rid} ERROR: {d['error']}")

# 第二轮：用 neuron_graph 返回的 tentative 节点测 promote
# 先重新拿一次 neuron_graph 获取 light_id
reqs2 = [
    {"jsonrpc": "2.0", "id": 6, "method": "tools/call", "params": {"name": "memoryguard_neuron_graph", "arguments": {"workspace": ws}}},
]
stdin2 = "\n".join(json.dumps(r) for r in reqs2) + "\n"
p2 = subprocess.run([sys.executable, "-m", "memoryguard.mcp_server"], input=stdin2, capture_output=True, text=True)
for line in p2.stdout.strip().splitlines():
    d = json.loads(line)
    if "result" in d and "content" in d["result"]:
        text = d["result"]["content"][0]["text"]
        print(f"\nid=6 neuron_graph (第二次):\n{text[:200]}")
