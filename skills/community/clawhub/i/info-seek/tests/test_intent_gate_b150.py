#!/usr/bin/env python3
"""Infoseek v2.5.0 守护（B-150）：意图槽门控堵主题漂移。

锁定 scripts/infoseek_pipeline.py 的意图槽契约（CHANGELOG [2.5.0] - 2026-10-05）：
  A 槽识别：_intent_slots 字面命中 7 组触发词；疑问/时间虚词不入槽
  B trade 同族：price/purchase/market 簇内任一组回显即过
  C 跨族：rank/guide/company 各组必须分别回显
  D 核心实体词：_core_entity_words 剔除意图词与虚词
  E _passes_intent：漂移页拒、同族真相关页过、无槽恒 True
  F _filter_relevant 三路径统一过槽（主门槛/floor 保底/top-k 二级保底）
  G 总开关 INFOSEEK_INTENT_GATE=0 回退旧语义
  H 图谱邻域：带意图槽默认跳过、INFOSEEK_RECALL_GRAPH_INTENT=1 恢复
全离线、零真实网络（打分/桥接/LLM 全 mock）。
"""
import os
import sys
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))

for _k in [k for k in os.environ if k.startswith('INFOSEEK_')]:
    os.environ.pop(_k, None)

passed, failed = [], []


def ok(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  PASS {name} {extra}")
    else:
        failed.append(name); print(f"  FAIL {name} {extra}")


import infoseek_pipeline as p  # noqa: E402

Q = '信阳板栗最新收购价格'

print("\n═══ A 意图槽识别 ═══")
slots = p._intent_slots(Q)
ok("A1 命中 price 组（价格）", 'price' in slots, f"groups={list(slots)}")
ok("A2 命中 purchase 组（收购）", 'purchase' in slots)
ok("A3 slots 值为 (命中词, 全组词) 二元组",
   all(isinstance(v, tuple) and len(v) == 2 for v in slots.values()))
slots_q = p._intent_slots('信阳板栗最新价格')
ok("A4 疑问/时间虚词不单独成槽（最新/今年无对应组）",
   set(p._intent_slots('板栗今年怎么样')) == set())

print("\n═══ B trade 同族（price/purchase/market 簇内任一）═══")
b_slots = p._intent_slots(Q)
ok("B1 只写'收购/采购'的同族页过槽",
   p._passes_intent('信阳板栗今年收购开秤 采购商进村'.lower(), Q, b_slots) is True)
ok("B2 只写'价格/报价/走势'的同族页过槽",
   p._passes_intent('信阳板栗市场价格走势 今日板栗报价'.lower(), Q, b_slots) is True)
ok("B3 query 命中 trade 三族但文本只回显 market 词（行情/供需）即过",
   p._passes_intent(
       '信阳板栗今日行情 供需偏紧 板栗'.lower(),
       '信阳板栗收购价格行情走势',
       p._intent_slots('信阳板栗收购价格行情走势')) is True)
ok("B3b trade 簇三组同属一个 family",
   p._INTENT_GROUP_FAMILY['price'] == 'trade'
   and p._INTENT_GROUP_FAMILY['purchase'] == 'trade'
   and p._INTENT_GROUP_FAMILY['market'] == 'trade')
print("\n═══ C 跨族各组必须分别回显 ═══")
q2 = '板栗十大品牌 做法教程'
s2 = p._intent_slots(q2)
ok("C1 q2 命中 rank 与 guide 两族", set(['rank', 'guide']) <= set(s2))
ok("C2 仅回显 rank 不回显 guide → 拒",
   p._passes_intent('板栗十大品牌排行榜'.lower(), q2, s2) is False)
ok("C3 两组都回显 → 过",
   p._passes_intent('板栗十大品牌 家常做法教程'.lower(), q2, s2) is True)

print("\n═══ D 核心实体词 ═══")
core = p._core_entity_words(Q, b_slots)
ok("D1 核心词保留'板栗'", '板栗' in core, f"core={core}")
ok("D2 核心词剔除意图词'价格'", '价格' not in core)
ok("D3 核心词剔除意图词'收购'", '收购' not in core)
ok("D4 纯英文 tokenize 为空时返回空集（豁免实体条件）",
   p._core_entity_words('Tesla revenue', p._intent_slots('Tesla revenue')) == set())

print("\n═══ E _passes_intent 漂移拦截 ═══")
drift = '信阳板栗旅游攻略 著名景点 美食推荐 板栗之乡游玩'
ok("E1 主题漂移旅游页（有实体无意图回显）被拒",
   p._passes_intent(drift.lower(), Q, b_slots) is False)
ok("E2 营销官网薄壳页被拒",
   p._passes_intent('欢迎访问信阳板栗官网 智能体先行者 企业介绍'.lower(), Q, b_slots) is False)
ok("E3 无意图槽时任意文本恒 True（纯实体查询不额外约束）",
   p._passes_intent('任意无关文本', '板栗', {}) is True)
ok("E4 真相关页（实体+意图）过槽",
   p._passes_intent('信阳板栗2026收购价格行情分析'.lower(), Q, b_slots) is True)

print("\n═══ F _filter_relevant 三路径统一过槽 ═══")
# 全部构造为低分（语义 5 分 < floor 8），从而：主门槛不过 → floor 窗 → top-k 二级保底。
# 区分点只在候选文本是否回显意图词+实体词。
def _run(cands, query):
    with mock.patch('anchor_adapter.compute_semantic_similarity',
                    side_effect=lambda t, q: 5), \
         mock.patch('anchor_adapter._string_containment_similarity',
                    return_value=0), \
         mock.patch.object(p, '_xling_mod') as xm, \
         mock.patch.object(p, '_min_expected', return_value=3), \
         mock.patch.object(p, '_llm_judge_relevance', return_value=-1):
        xm.bridge_score.return_value = 0
        return p._filter_relevant([dict(c) for c in cands], query)

drift_cands = [{'url': f'https://d{i}.com', 'title': f'信阳板栗旅游景点推荐{i}',
                'snippet': '游玩攻略 美食'} for i in range(5)]
good_cands = [{'url': f'https://g{i}.com', 'title': f'信阳板栗2026收购价格行情{i}',
               'snippet': '报价走势'} for i in range(5)]
f_drift = _run(drift_cands, Q)
f_good = _run(good_cands, Q)
ok("F1 漂移候选在 top-k 二级保底仍被意图槽拦截（返回空）", f_drift == [],
   f"len={len(f_drift)}")
ok("F2 过槽低分候选可被 top-k 保送（返回3条）", len(f_good) == 3, f"len={len(f_good)}")
# 主门槛高分路径也要过槽：高分但漂移 → 拒
hi_drift = [{'url': f'https://h{i}.com', 'title': f'信阳板栗旅游景点{i}',
             'snippet': '游玩'} for i in range(5)]
with mock.patch('anchor_adapter.compute_semantic_similarity',
                side_effect=lambda t, q: 90), \
     mock.patch('anchor_adapter._string_containment_similarity', return_value=0), \
     mock.patch.object(p, '_xling_mod') as xm2, \
     mock.patch.object(p, '_llm_judge_relevance', return_value=-1):
    xm2.bridge_score.return_value = 0
    out_hi = p._filter_relevant([dict(c) for c in hi_drift], Q)
ok("F3 高分漂移页主门槛路径也被意图槽拦截", out_hi == [], f"len={len(out_hi)}")

print("\n═══ G 总开关回退旧语义 ═══")
os.environ['INFOSEEK_INTENT_GATE'] = '0'
try:
    out_off = _run(drift_cands, Q)
    ok("G1 INTENT_GATE=0 时漂移候选不再受意图槽约束（被低分保底保送）",
       len(out_off) == 3, f"len={len(out_off)}")
finally:
    os.environ.pop('INFOSEEK_INTENT_GATE', None)

print("\n═══ H 图谱邻域意图感知 ═══")
import inspect  # noqa: E402
# mod-v1.5.2 调度台阶段B：扩展实现主体迁入 _expand_query_variants（返回
# (expanded, extra_list) 供 Stage2），_expand_query 保留为薄封装（旧字符串签名）。
# 源码契约对两者并集检查，表达式仍须真实存在于扩展实现中。
_src_expand = (inspect.getsource(p._expand_query)
               + inspect.getsource(p._expand_query_variants))
# 源码契约：带意图槽时 _graph_allow 计算式存在，且默认 env=False、_has_intent=True
# 时整体为 False（跳过邻居）。锁定 B-3 表达式，防止误删意图门。
ok("H1 _expand_query 含 B-3 图谱意图门表达式（_graph_allow = ... or not _has_intent）",
   '_graph_allow' in _src_expand and '_has_intent' in _src_expand
   and 'INFOSEEK_RECALL_GRAPH_INTENT' in _src_expand)
# 行为等价复算：默认（env 未设）+ 带意图槽 → 不允许邻居
_graph_allow_default = p._env_flag('INFOSEEK_RECALL_GRAPH_INTENT', False) or not bool(p._intent_slots(Q))
ok("H1b 带意图槽 query 默认不允许图谱邻居", _graph_allow_default is False)
os.environ['INFOSEEK_RECALL_GRAPH_INTENT'] = '1'
try:
    _graph_allow_on = p._env_flag('INFOSEEK_RECALL_GRAPH_INTENT', False) or not bool(p._intent_slots(Q))
    ok("H2 RECALL_GRAPH_INTENT=1 恢复邻居（即使带意图槽）", _graph_allow_on is True)
finally:
    os.environ.pop('INFOSEEK_RECALL_GRAPH_INTENT', None)
ok("H3 纯实体 query 无意图槽（邻居默认允许）", p._intent_slots('板栗') == {})

print(f"\ntest_intent_gate_b150: {len(passed)} PASS / {len(failed)} FAIL")
if failed:
    print("未通过：" + ", ".join(failed))
    sys.exit(1)
print("ALL GREEN")
