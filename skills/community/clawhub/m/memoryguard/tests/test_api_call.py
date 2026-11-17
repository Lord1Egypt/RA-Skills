"""调用 GovernanceApi 各方法，展示交互式面板背后的数据。"""
import json
from pathlib import Path
from memoryguard.gui import GovernanceApi

ws = r"H:\ai\workspace\工具项目\memoryguard\tests\fixtures\workspace"
api = GovernanceApi(ws)

print("=" * 60)
print("1. run_audit() - 全扫描 + 规则引擎")
print("=" * 60)
r = api.run_audit()
print(f"  对象: {r['summary']['object_count']}, 问题: {len(r['findings'])}, 健康: {r['health_score']}")
for f in r["findings"][:3]:
    print(f"    [{f['severity']}] {f['rule_id']}: {f['evidence'][:60]}")

print()
print("=" * 60)
print("2. get_neuron_graph() - 光点神经树快照（核心）")
print("=" * 60)
g = api.get_neuron_graph()
s = g["stats"]
print(f"  记忆片段: {s['claim_count']}")
print(f"  光点节点: {s['node_count']} (topic={s['topic_count']}, anchor={s['anchor_count']})")
print(f"  状态: tentative={s['tentative_count']}, confirmed={s['confirmed_count']}")
print(f"  边: {s['edge_count']}")
print(f"  合并建议: {len(g['merge_suggestions'])}")
print()
print("  神经树节点:")
for n in g["nodes"][:10]:
    kind = n["node_kind"]
    cnt = n.get("claim_count", 0)
    decay = n.get("decay_score", 0)
    print(f"    [{n['status']:9s}] {kind:14s} {n['label'][:30]:30s} claim={cnt} decay={decay:.2f}")

print()
print("=" * 60)
print("3. 萃取的记忆片段（KnowledgeClaim）")
print("=" * 60)
for c in g["claims"][:8]:
    print(f"  #{c['id']} [{c['memory_type']:12s}] {c['display_label'][:40]}")
    print(f"     body: {c['body'][:60]}...")
    print(f"     source: {c['source']}")

print()
print("=" * 60)
print("4. 治理操作演示: promote_neuron (晋升一个 tentative)")
print("=" * 60)
tentative = [n for n in g["nodes"] if n["status"] == "tentative"]
if tentative:
    tid = tentative[0]["light_id"]
    print(f"  晋升前: {tentative[0]['label']} (tentative)")
    r = api.promote_neuron(tid)
    print(f"  promote_neuron('{tid}') -> ok={r['ok']}")
    # 找晋升后的节点
    promoted = [n for n in r["snapshot"]["nodes"] if n["light_id"] == tid]
    if promoted:
        print(f"  晋升后: {promoted[0]['label']} ({promoted[0]['status']})")
else:
    print("  无 tentative 节点可晋升")

print()
print("=" * 60)
print("5. 治理操作演示: dissolve_neuron (凋亡一个 topic)")
print("=" * 60)
topics = [n for n in g["nodes"] if n["node_kind"] == "topic" and n["status"] != "dissolved" and n["light_id"] != "main"]
if topics:
    did = topics[0]["light_id"]
    print(f"  凋亡前: {topics[0]['label']} ({topics[0]['status']})")
    r = api.dissolve_neuron(did)
    print(f"  dissolve_neuron('{did}') -> ok={r['ok']}")
    dissolved = [n for n in r["snapshot"]["nodes"] if n["light_id"] == did]
    if dissolved:
        print(f"  凋亡后: {dissolved[0]['label']} ({dissolved[0]['status']})")

print()
print("=" * 60)
print("全部调用完成。交互式面板窗口仍在桌面运行，可点击操作。")
print("=" * 60)
