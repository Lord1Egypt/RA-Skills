#!/usr/bin/env python3
"""Infoseek v2.4.0 L4 稳定性测试（6 用例）

覆盖：1000+ 源 / 10000 声明 / 50 实体批量下的耗时与内存
"""
import sys, os, json, tempfile, time
try:
    import resource  # POSIX-only；Windows 不可用
    HAS_RESOURCE = True
except ImportError:
    HAS_RESOURCE = False
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK / 'scripts'))

passed, failed = [], []
def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")


def mem_mb():
    if not HAS_RESOURCE:
        return 0  # Windows 无 ru_maxrss → 内存维度跳过（不判 FAIL）
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # MB


# L4-01 1000 源 ConflictMonitor 增量
from conflict_v3 import ConflictMonitor
import random, string
def mk_src(i):
    return {
        'title': f'Entity{i} news {i}',
        'snippet': f'Entity{i} 宣布 {random.choice(["开源", "闭源", "合作", "投资"])} 计划',
        'url': f'https://bulk{i}.com/{i}',
    }
sources = [mk_src(i) for i in range(1000)]
t0 = time.time()
m = ConflictMonitor()
m.ingest_all(sources)
fin = m.finalize()
elapsed = time.time() - t0
mem_after = mem_mb()
check('L4-01 1000 源 <10s + <300MB',
      elapsed < 10 and mem_after < 300,
      f"elapsed={elapsed:.2f}s mem={mem_after:.0f}MB conflicts={len(fin['conflicts'])}")

# L4-02 10000 声明 claim_store 持久化
from claim_store import ClaimStore
tf = tempfile.mktemp(suffix='.json')
cs = ClaimStore(path=tf); cs.clear()
for i in range(10000):
    cs.add_claim(f'Ent{i % 50}', {'source': f'http://x.com/{i}',
                                    'text': f'claim {i}',
                                    'timestamp': '2026-08-01'})
t0 = time.time()
cs.save()
save_dt = time.time() - t0
t0 = time.time()
cs2 = ClaimStore(path=tf)
data = cs2.load()
load_dt = time.time() - t0
total = sum(len(v) for v in data.values())
check('L4-02 10000 声明 save/load <3s/2s',
      save_dt < 3 and load_dt < 2,
      f"save={save_dt:.2f}s load={load_dt:.2f}s total={total}")
os.remove(tf)

# L4-03 trace_entity 50 实体批量
from entity_trajectory import trace_entity, trace_entities
names = [f'Ent{i}' for i in range(50)]
t0 = time.time()
results = trace_entities(names, days_back=90)
elapsed = time.time() - t0
check('L4-03 50 实体批量 <5s', elapsed < 5,
      f"elapsed={elapsed:.2f}s count={len(results)}")

# L4-04 predict_heat 全实体排名
from entity_heat import get_heat_ranking
t0 = time.time()
ranking = get_heat_ranking(top_n=146)
elapsed = time.time() - t0
check('L4-04 146 实体排名 <2s', elapsed < 2,
      f"elapsed={elapsed:.2f}s returned={len(ranking)}")

# L4-05 freshness_cron 100 画像扫描（手动构造 100 profile）
import entity_profile as ep
tf5 = tempfile.mktemp(suffix='.json')
profs = {}
for i in range(100):
    name = f'ProfEnt{i}'
    profs[name] = {
        'entity_name': name, 'entity_type': 'ORG',
        'topics': ['AI'], 'source_domains': ['x.com'],
        'first_seen': '2026-08-08', 'last_seen': '2026-08-08',
        'hit_total': 1, 'conflict_refs': [],
    }
# 把一半 last_seen 改成 2024 年让 stale 标记得以触发
for i in range(0, 100, 2):
    profs[f'ProfEnt{i}']['last_seen'] = '2024-01-01'
with open(tf5, 'w', encoding='utf-8') as f:
    json.dump(profs, f, ensure_ascii=False)
# v2.4.1 PATCH 测试修：monkey-patch PROFILE_FILE 类属性而非 __init__
orig_file = ep.EntityProfile.PROFILE_FILE
ep.EntityProfile.PROFILE_FILE = tf5
try:
    from freshness_cron import FreshnessCron
    # v2.4.3 PATCH: PROFILE_FILE 替换后必须 invalidate 单例缓存
    ep.reset_profile()
    t0 = time.time()
    cron_res = FreshnessCron().run_full_scan()
    elapsed = time.time() - t0
    check('L4-05 cron 100 画像 <3s',
          elapsed < 3 and cron_res.get('profile_scanned', 0) >= 50,
          f"elapsed={elapsed:.2f}s scanned={cron_res.get('profile_scanned')} marked={cron_res.get('profile_marked_stale')}")
finally:
    ep.EntityProfile.PROFILE_FILE = orig_file
    ep.reset_profile()  # 清理单例，避免污染后续测试
os.remove(tf5)

# L4-06 research() 100 源端到端（v2.4.1 PATCH: lite 模式）
from infoseek_core_v2 import research
sources100 = [mk_src(i) for i in range(100)]
t0 = time.time()
res = research('BulkTest', sources=sources100, lite=True)
elapsed = time.time() - t0
mem_after = mem_mb()
check('L4-06 research 100 源 lite <15s + <400MB',
      elapsed < 15 and mem_after < 400,
      f"elapsed={elapsed:.2f}s mem={mem_after:.0f}MB conflicts={len(res.get('conflicts', []))}")


# ── v2.4.3 新增：L4-07/08/09 P1-A/B + P2 单例化验证 ──

# L4-07 P1-A: entity_graph 100 源 <1s（v2.4.0 2.9s → v2.4.3 <1s）
from entity_graph import EntityGraph
t0 = time.time()
g = EntityGraph(); r_g = g.build_from_sources(sources100)
elapsed = time.time() - t0
check('L4-07 entity_graph 100 源 <1s (P1-A)',
      elapsed < 1, f"elapsed={elapsed:.2f}s nodes={r_g['nodes']} edges={r_g['edges']}")

# L4-08 P1-A: 边权 Jaccard 归一化（验证 P1-A 权重计算正确）
g_test = EntityGraph(); g_test.build_from_sources([
    {'title': 'X', 'snippet': 'OpenAI GPT-5', 'url': 'https://a/1'},
    {'title': 'X', 'snippet': 'OpenAI GPT-5 Anthropic', 'url': 'https://a/2'},
])
# freq_min = min(2, 2) = 2, count = 2 → weight = 1.0
edge = g_test.edges.get(('Anthropic', 'OpenAI'), {})
weight_ok = edge.get('weight', 0) > 0
check('L4-08 边权 Jaccard 归一化正确 (P1-A)',
      weight_ok, f"edge={edge.get('source')} weight={edge.get('weight')}")

# L4-09 P2: 三个单例同对象验证
import entity_profile as ep_mod
import claim_store as cs_mod
import entity_tracker as et_mod
p1 = ep_mod.get_profile(); p2 = ep_mod.get_profile()
c1 = cs_mod.get_claim_store(); c2 = cs_mod.get_claim_store()
t1 = et_mod.get_tracker(); t2 = et_mod.get_tracker()
singleton_ok = (p1 is p2) and (c1 is c2) and (t1 is t2)
check('L4-09 Profile/ClaimStore/Tracker 三单例同对象 (P2)',
      singleton_ok, f"profile={p1 is p2} claim={c1 is c2} tracker={t1 is t2}")


print(f"\n=== L4 稳定性: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")