# -*- coding: utf-8 -*-
"""测试 MCP 接口"""
import json
import urllib.request

BASE_URL = "https://xilejie-silk.com/liuyang-life/"

def test_mcp(method, params=None):
    data = {"jsonrpc": "2.0", "id": 1, "method": method}
    if params:
        data["params"] = params
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(BASE_URL, data=body, headers={"Content-Type": "application/json"})
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read().decode("utf-8"))
    return result

print("=" * 60)
print("1. 测试 initialize")
print("=" * 60)
r = test_mcp("initialize")
print(json.dumps(r, ensure_ascii=False, indent=2))

print("\n" + "=" * 60)
print("2. 测试 tools/list")
print("=" * 60)
r = test_mcp("tools/list")
tools = r.get("result", {}).get("tools", [])
print(f"共 {len(tools)} 个工具:")
for t in tools:
    print(f"  - {t['name']}: {t['description'][:40]}...")

print("\n" + "=" * 60)
print("3. 测试 find_service（找疏通下水道的师傅）")
print("=" * 60)
r = test_mcp("tools/call", {"name": "find_service", "arguments": {"category": "疏通下水道"}})
content = r.get("result", {}).get("content", [{}])[0].get("text", "")
data = json.loads(content)
if data.get("found"):
    print(f"找到 {data['count']} 个师傅:")
    for s in data["services"]:
        print(f"  - {s['name']}（{s['contact']}）电话: {s['phone']}，{s['price_range']}，{s['highlight']}")
else:
    print(data.get("message"))

print("\n" + "=" * 60)
print("4. 测试 find_restaurant（6人500元预算，要风景）")
print("=" * 60)
r = test_mcp("tools/call", {"name": "find_restaurant", "arguments": {
    "budget_per_person": 83, "people_count": 6, "want_scenery": True
}})
content = r.get("result", {}).get("content", [{}])[0].get("text", "")
data = json.loads(content)
if data.get("found"):
    print(f"找到 {data['count']} 家餐厅:")
    for r in data["restaurants"]:
        print(f"  - {r['name']}（{r['avg_price_desc']}）{r['address']}，电话: {r['phone']}")
        print(f"    特色菜: {', '.join(r['specialties'])}")
        print(f"    亮点: {r['highlight']}")
else:
    print(data.get("message"))

print("\n" + "=" * 60)
print("5. 测试 find_hotel（天空剧院附近，400元，有早餐）")
print("=" * 60)
r = test_mcp("tools/call", {"name": "find_hotel", "arguments": {
    "max_price": 400, "need_breakfast": True, "near_landmark": "天空剧院"
}})
content = r.get("result", {}).get("content", [{}])[0].get("text", "")
data = json.loads(content)
if data.get("found"):
    print(f"找到 {data['count']} 家酒店:")
    for h in data["hotels"]:
        print(f"  - {h['name']}（{h['price_range']}）{h['address']}")
        print(f"    早餐: {h['breakfast_desc']}")
        print(f"    位置: {h['nearby_landmark']}")
        print(f"    电话: {h['phone']}")
else:
    print(data.get("message"))
    if data.get("all_hotels"):
        print("所有酒店:")
        for h in data["all_hotels"]:
            print(f"  - {h}")

print("\n✅ 全部测试完成！")
