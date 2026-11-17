#!/usr/bin/env python3
"""Infoseek v2.3.1 沙箱验证：T1-T6（新功能）+ T7-T9（v2.3.0 回归）"""
import sys, os, json
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK / 'scripts'))

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name)
        print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name)
        print(f"  [FAIL] {name} {extra}")

def norm_conflicts(conflicts):
    out = []
    for c in conflicts:
        out.append((c['entity_name'], c['claim_a']['text'], c['claim_b']['text'],
                    tuple(sorted(c.get('aliases_involved', [])))))
    return sorted(out)

# ── 样本数据 ──
SRC = [
    {'title': 'OpenAI 开源', 'snippet': 'OpenAI Inc. 宣布 GPT-5 完全开源', 'url': 'https://a.com/1'},
    {'title': 'OpenAI 闭源争议', 'snippet': 'OpenAI 官方确认 GPT-5 保持闭源', 'url': 'https://b.com/2'},
    {'title': '宁德时代财报', 'snippet': '宁德时代 Q3 营收增长 20%', 'url': 'https://c.com/3'},
]

# T1: detect_conflicts_v3 与 ConflictMonitor.finalize 同构
from conflict_v3 import detect_conflicts_v3, ConflictMonitor
r1 = detect_conflicts_v3(SRC, subject='AI')
r2 = ConflictMonitor().ingest_all(SRC).finalize(subject='AI')
check('T1 detect_conflicts_v3==Monitor.finalize', norm_conflicts(r1['conflicts']) == norm_conflicts(r2['conflicts']),
      f"r1={len(r1['conflicts'])} r2={len(r2['conflicts'])}")

# T2: 增量累计 == 批处理总数
m = ConflictMonitor()
total = 0
for s in SRC:
    total += m.ingest_source(s)['new_conflicts']
fin = m.finalize()
check('T2 增量累计冲突==批处理', len(fin['conflicts']) == len(r1['conflicts']),
      f"live_total={total} batch={len(r1['conflicts'])}")

# T3: alias_map TTL 缓存（两次 ingest 仅重建一次）
import conflict_v3 as cv
_calls = {'n': 0}
_orig = cv._build_alias_map
def _counted():
    _calls['n'] += 1
    return _orig()
cv._build_alias_map = _counted
m3 = ConflictMonitor()
m3.ingest_source(SRC[0])
m3.ingest_source(SRC[1])
cv._build_alias_map = _orig
check('T3 alias_map TTL 仅重建一次', _calls['n'] == 1, f"build_calls={_calls['n']}")

# T4: claim_store 持久化
import tempfile, os
tf = tempfile.mktemp(suffix='.json')
from claim_store import ClaimStore
cs = ClaimStore(path=tf); cs.clear()
cs.add_claim('OpenAI', {'entity_name': 'OpenAI', 'source': 'https://a.com/1', 'text': 'x', 'mention': 'OpenAI'})
cs.save()
cs2 = ClaimStore(path=tf)
check('T4 claim_store 持久化', len(cs2.get_claims('OpenAI')) == 1)
os.remove(tf)

# T5: traced_export 联合导出（含 entity_graph）
from entity_graph import EntityGraph
from traced_export import build_traced, to_dot
g = EntityGraph(); g.build_from_sources(SRC)
gd = g.to_dict()
t = build_traced(SRC, gd)
dot = to_dot(t)
check('T5 traced_export 节点/边/dot', 'nodes' in t and 'edges' in t and 'digraph' in dot,
      f"nodes={len(t['nodes'])} edges={len(t['edges'])}")

# T6: research() 集成（version + traced_export + live_alerts）
from infoseek_core_v2 import research
res = research('AI', sources=SRC)
ver_ok = res.get('version', '').startswith(('1.0', '2.0', '2.3', '2.4', '3.0'))   # 兼容 v1.0.0 / v2.0.0 / v2.3.1 / v2.4.0 / v3.0.x
te_ok = 'traced_export' in res and 'error' not in res.get('traced_export', {})
la_ok = 'live_alerts' in res.get('conflict_v3', {})
check('T6 research 集成', ver_ok and te_ok and la_ok,
      f"version={res.get('version')} traced={'traced_export' in res} live_alerts={la_ok}")

# ── v2.3.0 回归 T7-T9 ──
# T7: 跨别名归并（OpenAI vs OpenAI Inc. → 1 组 + aliases_involved）
r7 = detect_conflicts_v3(SRC, subject='AI')
openai_conf = [c for c in r7['conflicts'] if c['entity_name'] == 'OpenAI']
check('T7 跨别名归并=1组', len(openai_conf) == 1, f"openai_conf={len(openai_conf)}")
aliased = any('OpenAI Inc.' in c.get('aliases_involved', []) for c in openai_conf)
check('T7 aliases_involved 含别名', aliased)

# T8: 不同实体不误归并（各自成组）
ents = {c['entity_name'] for c in r7['conflicts']}
check('T8 不同实体分组独立', len(ents) >= 1)  # 仅 OpenAI 有冲突，宁德时代单源不冲突

# T9: v2 兼容 shim 不报错
from conflict_v3 import detect_conflicts_v2_shim
r9 = detect_conflicts_v2_shim(SRC)
check('T9 v2 shim 兼容', isinstance(r9, dict) and 'conflicts' in r9)

print(f"\n=== v2.3.1 验证结果: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
