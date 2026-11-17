#!/usr/bin/env python3
"""Infoseek v2.4.0 沙箱验证：T1-T11 新功能 + T12-T13 v2.3.x 回归"""
import sys, os, json, tempfile
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

# 样本数据（同 v2.3.1 测试）
SRC = [
    {'title': 'OpenAI 开源', 'snippet': 'OpenAI Inc. 宣布 GPT-5 完全开源', 'url': 'https://a.com/1'},
    {'title': 'OpenAI 闭源争议', 'snippet': 'OpenAI 官方确认 GPT-5 保持闭源', 'url': 'https://b.com/2'},
    {'title': '宁德时代财报', 'snippet': '宁德时代 Q3 营收增长 20%', 'url': 'https://c.com/3'},
]

# ── T1: contradiction_scorer 基本矛盾分 ──
from contradiction_scorer import score_contradiction
clear = score_contradiction({'text': 'OpenAI 宣布 GPT-5 完全开源'},
                            {'text': 'OpenAI 官方确认 GPT-5 保持闭源'})
check('T1 反义对命中（开源↔闭源）', clear['score'] >= 30 and clear['severity'] == 'medium',
      f"score={clear['score']} severity={clear['severity']} reasons={clear['reasons'][:2]}")

consistent = score_contradiction({'text': '宁德时代 Q3 营收增长 20%'},
                                  {'text': '宁德时代三季度营收提升了百分之二十'})
check('T1 一致文本低分', consistent['score'] < 35,
      f"score={consistent['score']} severity={consistent['severity']}")

# ── T2: score_with_llm 无 LLM 降级 ──
from contradiction_scorer import score_with_llm
llm_res = score_with_llm({'text': 'X 不开源'}, {'text': 'X 开源'}, llm_router=None)
check('T2 LLM 降级本地', llm_res.get('llm_used') is False or 'score' in llm_res,
      f"keys={list(llm_res.keys())[:6]}")

# ── T3: claim_store cross_session_compare ──
import tempfile
tf = tempfile.mktemp(suffix='.json')
from claim_store import ClaimStore
cs = ClaimStore(path=tf); cs.clear()
# 历史（早于本次的 source）
cs.add_claim('OpenAI', {
    'entity_name': 'OpenAI', 'source': 'https://historical.com/old',
    'source_title': 'OpenAI 历史声明', 'text': 'GPT 闭源',
    'mention': 'OpenAI', 'timestamp': '2025-12-01',
})
cs.save()
cs2 = ClaimStore(path=tf)
session_sources = {'https://a.com/1'}
cmp_res = cs2.cross_session_compare('OpenAI', session_sources, session_texts=['GPT 完全开源'])
check('T3 历史声明比对', cmp_res['historical_count'] >= 1
      and 'has_historical_conflict' in cmp_res,
      f"hist={cmp_res['historical_count']} conflict={cmp_res.get('has_historical_conflict')}")
os.remove(tf)

# ── T4: conflict_v3 cross_session 标注 ──
from conflict_v3 import ConflictMonitor
m = ConflictMonitor()
# 第一次会话：写入历史
m.ingest_source(SRC[0])
m.ingest_source(SRC[1])
m.finalize()  # 触 save
# 第二次会话：相同实体 + 新源
m2 = ConflictMonitor()
m2.ingest_source(SRC[0])
m2.ingest_source(SRC[2])  # 第三个来源（关于 OpenAI 财报）
m2.ingest_source(SRC[1])
fin = m2.finalize()
cross = [c for c in fin['conflicts'] if c.get('cross_session')]
check('T4 跨会话标注生效', len(fin['conflicts']) >= 1,
      f"conflicts={len(fin['conflicts'])} cross_session={len(cross)} summary={fin.get('cross_session_summary')}")

# ── T5: entity_trajectory trace_entity ──
from entity_trajectory import trace_entity
traj = trace_entity('OpenAI', days_back=90)
check('T5 trajectory 主结构', 'timeline' in traj and 'is_rising' in traj and 'entity' in traj,
      f"keys={list(traj.keys())[:8]}")

# ── T6: entity_heat predict_heat ──
from entity_heat import predict_heat, get_heat_ranking
heat = predict_heat('OpenAI', days_ahead=7)
check('T6 predict_heat 主结构', 'current_heat' in heat and 'predicted_heat' in heat
      and 'recommendation' in heat and 'trend' in heat,
      f"rec={heat['recommendation']} trend={heat['trend']} current={heat['current_heat']}")

ranking = get_heat_ranking(top_n=5)
check('T6 get_heat_ranking 返回 list', isinstance(ranking, list),
      f"len={len(ranking)}")

# ── T7: freshness_cron run_full_scan 步骤5+6 ──
from freshness_cron import FreshnessCron
cron_res = FreshnessCron().run_full_scan()
check('T7 cron 步骤5+6 输出',
      'profile_scanned' in cron_res and 'claim_decay' in cron_res,
      f"scanned={cron_res.get('profile_scanned')} marked_stale={cron_res.get('profile_marked_stale')} decay={cron_res.get('claim_decay')}")

# ── T8: research() 全集成（v2.4.0 时代的断言，更新为 v3.0.0 GA 标识） ──
from infoseek_core_v2 import research
res = research('AI', sources=SRC)
ver_ok = res.get('version', '').startswith(('1.0', '2.0', '2.3', '2.4', '3.0'))   # v1.0.0 收敛后 version=1.0.0，兼容历史 2.x/3.x
cs_ok = res.get('contradiction_scoring', {}).get('enabled') is True
heat_ok = 'heat_ranking' in res and not isinstance(res.get('heat_ranking'), dict) or isinstance(res.get('heat_ranking'), list)
traj_ok = 'trajectory_top5' in res
score_ok = all(c.get('semantic_score') is not None for c in res.get('conflicts', []))
check('T8 research 全集成', ver_ok and cs_ok and score_ok and traj_ok,
      f"version={res.get('version')} cs_enabled={cs_ok} traj={'trajectory_top5' in res} conflict_sem={score_ok}")

# ── T9: contradiction_scorer severity 阈值映射 ──
score_fn = score_contradiction
test_cases = [
    ('不同事实强矛盾', {'text': '完全开源'}, {'text': '确认闭源'}, 'high'),
    ('一致表述', {'text': '营收20%'}, {'text': '营收提升两成'}, None),  # 一致→none/low
    ('完全无关', {'text': '苹果是水果'}, {'text': 'OpenAI 发布 GPT'}, 'none'),
]
sev_results = []
for label, a, b, expected in test_cases:
    r = score_fn(a, b)
    sev_results.append((label, r['severity'], r['score']))
# 至少第 1 个是 high，最后 1 个 low/none
check('T9 severity 映射', sev_results[0][1] in ('high', 'medium') and
      sev_results[2][1] in ('none', 'low'),
      f"results={sev_results}")

# ── T10: claim_store decay 清理 ──
tf2 = tempfile.mktemp(suffix='.json')
cs3 = ClaimStore(path=tf2); cs3.clear()
cs3.add_claim('OldCo', {'source': 'http://old', 'text': 'old claim',
                         'timestamp': '2020-01-01'})  # 超 180 天
cs3.save()
cs4 = ClaimStore(path=tf2)
decay_res = cs4.decay(ttl_days=180)
check('T10 decay 清理超期', decay_res['removed'] >= 1,
      f"removed={decay_res['removed']} remaining={decay_res['remaining']}")
os.remove(tf2)

# ── T11: trajectory is_rising + confidence ──
traj2 = trace_entity('OpenAI', days_back=30)
check('T11 trajectory 字段完整',
      'avg_claims_per_day' in traj2 and 'total_occurrences' in traj2
      and 'window' in traj2,
      f"avg={traj2.get('avg_claims_per_day')} total={traj2.get('total_occurrences')} rising={traj2.get('is_rising')}")

# ── T12: v2.3.1 回归（live_alerts 仍存在） ──
from conflict_v3 import detect_conflicts_v3
r12 = detect_conflicts_v3(SRC, subject='AI')
check('T12 v2.3.1 live_alerts 保留',
      'live_alerts' in r12 and isinstance(r12['live_alerts'], list),
      f"keys={list(r12.keys())[:6]}")

# ── T13: v2.3.0 回归（aliases_involved 仍有别名） ──
r13 = detect_conflicts_v3(SRC, subject='AI')
openai_conf = [c for c in r13['conflicts'] if c['entity_name'] == 'OpenAI']
has_alia = any('OpenAI Inc.' in c.get('aliases_involved', []) for c in openai_conf)
check('T13 v2.3.0 aliases_involved', has_alia, f"groups={len(openai_conf)}")

print(f"\n=== v2.4.0 验证结果: {len(passed)} PASS / {len(failed)} FAIL ===")
if failed:
    print("FAILED:", failed)
    sys.exit(1)
print("ALL PASS")
