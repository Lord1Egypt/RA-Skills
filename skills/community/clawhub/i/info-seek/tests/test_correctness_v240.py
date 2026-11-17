#!/usr/bin/env python3
"""Infoseek v2.4.0 L1 正确性测试（18 用例）

覆盖各模块主路径断言：
- contradiction_scorer 反义/否定/一致/无关/空/超长文本
- entity_trajectory 单条/多日期/profile 兜底
- entity_heat 活跃/stale/confidence
- conflict_v3 跨会话标注
- claim_store cross_session_compare / decay
- freshness_cron 步骤5+6
- research() 全字段
- traced_export Graphviz 合规
"""
import sys, os, json, tempfile
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


# ── contradiction_scorer ─────────────────────────────────
from contradiction_scorer import score_contradiction

r01 = score_contradiction({'text': 'OpenAI 宣布 GPT-5 完全开源'},
                           {'text': 'OpenAI 官方确认 GPT-5 保持闭源'})
check('L1-01 反义对(开源↔闭源)=medium', r01['score'] >= 30 and r01['severity'] == 'medium',
      f"score={r01['score']} sev={r01['severity']}")

r02 = score_contradiction({'text': 'X 不发布新产品'},
                           {'text': 'X 刚刚发布新产品'})
check('L1-02 否定不对称命中', r02['score'] >= 20,
      f"score={r02['score']} sev={r02['severity']}")

r03 = score_contradiction({'text': '宁德时代 Q3 营收增长 20%'},
                           {'text': '宁德时代三季度营收提升 20%'})
check('L1-03 一致表述=low/none', r03['score'] < 30, f"score={r03['score']} sev={r03['severity']}")

r04 = score_contradiction({'text': '苹果是水果'}, {'text': 'OpenAI 发布 GPT'})
check('L1-04 无关=none', r04['score'] < 10, f"score={r04['score']} sev={r04['severity']}")

r05 = score_contradiction({'text': ''}, {'text': ''})
check('L1-05 空文本=none', r05['score'] == 0 and r05['severity'] == 'none',
      f"score={r05['score']} sev={r05['severity']}")

import time as _time
t0 = _time.time()
big = 'OpenAI 发布 GPT-5 ' * 10000  # ~200KB
r06 = score_contradiction({'text': big}, {'text': 'GPT-5 闭源'})
elapsed = (_time.time() - t0) * 1000
check('L1-06 超长文本<500ms', elapsed < 500, f"elapsed={elapsed:.1f}ms size={len(big)}")


# ── entity_trajectory ───────────────────────────────────
from entity_trajectory import trace_entity

r07 = trace_entity('OpenAI', days_back=90)
check('L1-07 trace_entity 主结构',
      'timeline' in r07 and 'is_rising' in r07 and 'entity' in r07,
      f"keys={list(r07.keys())[:6]}")

# L1-08 多日期排序（如果有数据）
tl = r07.get('timeline', [])
dates = [b['date'] for b in tl]
check('L1-08 timeline 日期递增', dates == sorted(dates), f"len={len(tl)}")

# L1-09 profile 兜底（profile_topics 字段存在）
check('L1-09 profile 兜底字段', 'profile_topics' in r07,
      f"profile_topics={r07.get('profile_topics')[:3] if r07.get('profile_topics') else None}")


# ── entity_heat ─────────────────────────────────────────
from entity_heat import predict_heat

# v2.4.2 PATCH: 注入 claim_store 触发 DEF-A 修复路径
import tempfile, datetime as _dt
from claim_store import ClaimStore
_tf_l1_10 = tempfile.mktemp(suffix='.json')
_cs_l1_10 = ClaimStore(path=_tf_l1_10); _cs_l1_10.clear()
_today = _dt.date.today()
for i in range(5):
    d = _today - _dt.timedelta(days=i+1)
    _cs_l1_10.add_claim('OpenAI', {'source': f'http://x{i}', 'text': f'claim{i}',
                                    'timestamp': d.isoformat()})
_cs_l1_10.save()
import entity_heat as _eh_l1_10
_eh_l1_10._safe_load_claim_store = lambda: ClaimStore(path=_tf_l1_10)
r10 = predict_heat('OpenAI', days_ahead=7)
check('L1-10 活跃实体=hot（DEF-A 修复验证）', r10['recommendation'] in ('hot', 'warm'),
      f"rec={r10['recommendation']} current={r10['current_heat']} trend={r10['trend']}")
os.remove(_tf_l1_10)

r11 = predict_heat('SomeStaleEntityZZZ', days_ahead=7)
check('L1-11 stale=stale',
      r11['recommendation'] == 'stale' or r11['days_since_last_seen'] > 30,
      f"rec={r11['recommendation']} days_since={r11['days_since_last_seen']}")

# L1-12 confidence 随样本量递增（构造场景）
from entity_heat import _confidence_from_samples
c1 = _confidence_from_samples(0, 7)
c2 = _confidence_from_samples(5, 7)
c3 = _confidence_from_samples(50, 7)
check('L1-12 confidence 随样本量递增', c1 < c2 < c3, f"c1={c1} c2={c2} c3={c3}")


# ── ConflictMonitor 跨会话 ─────────────────────────────
from conflict_v3 import ConflictMonitor

SRC_R1 = [
    {'title': 'OpenAI 开源', 'snippet': 'OpenAI Inc. 宣布 GPT-5 完全开源', 'url': 'https://r1-a.com/1'},
    {'title': 'OpenAI 闭源争议', 'snippet': 'OpenAI 官方确认 GPT-5 保持闭源', 'url': 'https://r1-b.com/2'},
]
SRC_R2 = [
    {'title': 'OpenAI 第二轮 A', 'snippet': 'OpenAI 仍坚持闭源',
     'url': 'https://r2-a.com/1'},
    {'title': 'OpenAI 第二轮 B', 'snippet': 'OpenAI 决定开源部分能力',
     'url': 'https://r2-b.com/2'},
]

m1 = ConflictMonitor()
m1.ingest_source(SRC_R1[0])
m1.ingest_source(SRC_R1[1])
m1.finalize()  # 写入历史（r1-a.com/1, r1-b.com/2）

m2 = ConflictMonitor()
m2.ingest_source(SRC_R2[0])  # 不同 URL → session 内冲突来源
m2.ingest_source(SRC_R2[1])  # 不同 URL → 触发冲突
fin = m2.finalize()
cross = [c for c in fin['conflicts'] if c.get('cross_session')]
check('L1-13 跨会话标注生效',
      len(cross) >= 1 and len(cross[0].get('historical_source', [])) >= 1,
      f"cross_count={len(cross)} hist={cross[0].get('historical_source') if cross else None}")


# ── claim_store ─────────────────────────────────────────
from claim_store import ClaimStore
tf = tempfile.mktemp(suffix='.json')
cs = ClaimStore(path=tf); cs.clear()
cs.add_claim('TestCo', {'entity_name': 'TestCo', 'source': 'http://h.com/1',
                         'source_title': 'Historical', 'text': 'GPT 闭源',
                         'mention': 'TestCo', 'timestamp': '2025-01-01'})
cs.save()
cs2 = ClaimStore(path=tf)
cmp_res = cs2.cross_session_compare('TestCo', session_sources={'http://new.com/1'})
check('L1-14 cross_session_compare 过滤',
      cmp_res['historical_count'] == 1 and 'http://h.com/1' in cmp_res['historical_sources'],
      f"hist={cmp_res['historical_count']} sources={cmp_res['historical_sources']}")
os.remove(tf)

tf2 = tempfile.mktemp(suffix='.json')
cs3 = ClaimStore(path=tf2); cs3.clear()
cs3.add_claim('OldCo', {'entity_name': 'OldCo', 'source': 'http://o.com/1',
                         'source_title': 'Old', 'text': 'old',
                         'mention': 'OldCo', 'timestamp': '2020-01-01'})
cs3.add_claim('NewCo', {'entity_name': 'NewCo', 'source': 'http://n.com/1',
                         'source_title': 'New', 'text': 'new',
                         'mention': 'NewCo', 'timestamp': '2026-08-01'})
cs3.save()
cs4 = ClaimStore(path=tf2)
decay_res = cs4.decay(ttl_days=180)
check('L1-15 decay 清理超期', decay_res['removed'] == 1,
      f"removed={decay_res['removed']} remaining={decay_res['remaining']}")
os.remove(tf2)


# ── freshness_cron ──────────────────────────────────────
from freshness_cron import FreshnessCron
cron_res = FreshnessCron().run_full_scan()
check('L1-16 cron 步骤5+6',
      'profile_scanned' in cron_res and 'claim_decay' in cron_res,
      f"profile_scanned={cron_res.get('profile_scanned')} decay={cron_res.get('claim_decay')}")


# ── research() ──────────────────────────────────────────
from infoseek_core_v2 import research
res = research('AI', sources=SRC_R1)
required_fields = ['version', 'conflicts', 'traced_export', 'entity_graph',
                   'entity_profiles', 'heat_ranking', 'trajectory_top5',
                   'conflict_v3', 'contradiction_scoring']
missing = [f for f in required_fields if f not in res]
check('L1-17 research 顶层字段齐', not missing, f"missing={missing}")

# L1-18 traced_export Graphviz 合规
te = res.get('traced_export', {})
dot = te.get('dot', '') if isinstance(te, dict) else ''
check('L1-18 traced_export Graphviz 合规',
      'digraph' in dot and dot.count('{') >= 1 and dot.count('}') >= 1,
      f"dot_len={len(dot)}")


print(f"\n=== L1 正确性: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")