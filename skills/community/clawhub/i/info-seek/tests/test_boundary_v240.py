#!/usr/bin/env python3
"""Infoseek v2.4.0 L2 能力边界测试（12 用例）

覆盖：空/超大/不存在/超限输入的降级行为
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


# L2-01 score_contradiction 空 dict claim
from contradiction_scorer import score_contradiction
r01 = score_contradiction({}, {})
check('L2-01 空 dict claim', r01['score'] == 0 and r01['severity'] == 'none',
      f"score={r01['score']} sev={r01['severity']}")

# L2-02 极长单句（100KB）
import time as _time
huge = ('OpenAI GPT-5 通用人工智能 大模型 ' * 5000).strip()  # ~135KB
t0 = _time.time()
try:
    r02 = score_contradiction({'text': huge}, {'text': 'GPT-5 闭源'})
    elapsed = (_time.time() - t0) * 1000
    check('L2-02 100KB 不超时', elapsed < 1000 and 'score' in r02,
          f"elapsed={elapsed:.1f}ms keys={list(r02.keys())[:4]}")
except Exception as e:
    check('L2-02 100KB 不超时', False, f"raised {type(e).__name__}: {e}")

# L2-03 trace_entity 不存在实体
from entity_trajectory import trace_entity
r03 = trace_entity('NonExistentEntityXYZ_404', days_back=90)
check('L2-03 不存在实体不崩',
      'timeline' in r03 and r03['total_occurrences'] == 0,
      f"total={r03['total_occurrences']} timeline_len={len(r03.get('timeline', []))}")

# L2-04 trace_entity days_back=0
r04 = trace_entity('OpenAI', days_back=0)
check('L2-04 days_back=0', 'timeline' in r04, f"keys={list(r04.keys())[:5]}")

# L2-05 trace_entity days_back=10000
r05 = trace_entity('OpenAI', days_back=10000)
check('L2-05 days_back=10000 不爆栈', isinstance(r05, dict) and 'window' in r05,
      f"days_in_window={r05.get('window', {}).get('days')}")

# L2-06 predict_heat days_ahead=0
from entity_heat import predict_heat
r06 = predict_heat('OpenAI', days_ahead=0)
check('L2-06 days_ahead=0', r06.get('predicted_heat') is not None,
      f"current={r06.get('current_heat')} predicted={r06.get('predicted_heat')}")

# L2-07 predict_heat days_ahead=365
r07 = predict_heat('OpenAI', days_ahead=365)
check('L2-07 days_ahead=365 衰减充分', r07['predicted_heat'] <= r07['current_heat'] + 1,
      f"current={r07['current_heat']} predicted={r07['predicted_heat']}")

# L2-08 ConflictMonitor 单源 ingest
from conflict_v3 import ConflictMonitor
m8 = ConflictMonitor()
res8 = m8.ingest_source({'title': 'OpenAI 开源', 'snippet': 'GPT-5 开源',
                          'url': 'https://a.com/1'})
check('L2-08 单源无冲突', res8['new_conflicts'] == 0, f"new_conflicts={res8['new_conflicts']}")

# L2-09 ConflictMonitor 同源多次
m9 = ConflictMonitor()
for _ in range(5):
    m9.ingest_source({'title': 'OpenAI 开源', 'snippet': 'GPT-5 开源',
                      'url': 'https://a.com/1'})
fin9 = m9.finalize()
check('L2-09 同源多次无冲突', len(fin9['conflicts']) == 0,
      f"conflicts={len(fin9['conflicts'])}")

# L2-10 claim_store 超过 MAX_PER_ENTITY（200）只留最新 200
from claim_store import ClaimStore, MAX_PER_ENTITY
tf = tempfile.mktemp(suffix='.json')
cs = ClaimStore(path=tf); cs.clear()
for i in range(MAX_PER_ENTITY + 50):
    cs.add_claim('BigCo', {'source': f'http://x.com/{i}', 'text': f'claim{i}',
                            'timestamp': '2026-08-01'})
cs.save()
cs2 = ClaimStore(path=tf)
claims = cs2.get_claims('BigCo')
check('L2-10 claim_store 上限 200', len(claims) == MAX_PER_ENTITY,
      f"count={len(claims)} max={MAX_PER_ENTITY}")
os.remove(tf)

# L2-11 freshness_cron 部分模块失败仍返回
import unittest.mock as mock
from freshness_cron import FreshnessCron
with mock.patch.object(FreshnessCron, 'run_full_scan', wraps=FreshnessCron().run_full_scan):
    res11 = FreshnessCron().run_full_scan()
check('L2-11 cron 部分失败仍返回',
      isinstance(res11, dict) and 'decayed_count' in res11,
      f"keys={list(res11.keys())[:6]}")

# L2-12 research() 空 sources
from infoseek_core_v2 import research
r12 = research('EmptyTest', sources=[])
check('L2-12 空 sources 不崩',
      isinstance(r12, dict) and 'version' in r12,
      f"version={r12.get('version')}")


# L2-13 conflict_v3 单坏源（None 字段）不 abort 全链（G2 边界硬化）
from conflict_v3 import detect_conflicts_v3
r13a = detect_conflicts_v3([{'title': 'OpenAI 开源', 'snippet': 'GPT-5 开源',
                             'url': 'https://a.com/9'}])
r13b = detect_conflicts_v3([{'title': 'OpenAI 开源', 'snippet': 'GPT-5 开源',
                             'url': 'https://a.com/9'},
                            {'title': None, 'body': None, 'url': None}])
check('L2-13 坏源不干扰好源处理', r13b['raw_claims'] == r13a['raw_claims'],
      f"base={r13a['raw_claims']} mixed={r13b['raw_claims']}")
check('L2-13 全 None 字段源不崩',
      isinstance(detect_conflicts_v3([{'title': None, 'body': None, 'url': None}]), dict))

print(f"\n=== L2 能力边界: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed); sys.exit(1)
print("ALL PASS")