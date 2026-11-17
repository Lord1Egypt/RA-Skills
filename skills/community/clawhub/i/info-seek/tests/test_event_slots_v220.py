#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_event_slots_v220.py — v2.1.2 事件槽批次守护（F-06 / F-04 / F-07）

批次：GA11 事件槽重构阶段 1-3（v2.1.1-openfix-p3stage0 已解除主体前置依赖）。
文件名保留 v220（批次立项名），实际版本 2.1.2（PATCH）。

断言五组：
  A F-06 事件抽取（分句 / schema / event_sig / 多事实句不串味 / 有界 / 异常降级）
  B F-04 期间裁决（不相交降权 / 相交不降权 / 缺失不降权 / 跨主体·空主体不裁决 / 不滤除）
  C F-07 time 路（旧签名零回归 / 事件级对齐 / 跨主体不误报 / 主体过滤 / 无同方面事件对）
  D claim 穿透（conflict_v3 在原始 body 抽事件 / 跨越两级截断 / 就地兜底）
  E 零回归（既有语料判定不变 / 返回 schema 超集 / 旧 time 断言不变）

风格：顶层直跑 + sys.exit + 自报 N PASS / N FAIL，由 tests/run_all.py 收集。
"""

import os
import sys

os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for p in (os.path.join(_ROOT, 'scripts'), os.path.join(_ROOT, 'core'), _ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

_PASS = 0
_FAIL = 0


def check(name, cond, extra=''):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
    else:
        _FAIL += 1
        print(f'  [FAIL] {name} {extra}')


import contradiction_scorer as cs  # noqa: E402

try:
    import conflict_v3 as cv3
    _CV3_OK = True
except Exception as _e:  # pragma: no cover
    cv3, _CV3_OK = None, False
    print(f'[WARN] conflict_v3 导入失败：{_e}')


def _sp(label, s, e):
    return {'label': label, 'start': s, 'end': e}


def _ev(subject, aspect, span=None, polarity='pos'):
    return {'subject': subject, 'aspect': aspect, 'value': None,
            'polarity': polarity, 'time_span': span,
            'event_sig': f'{subject}|{aspect}'}


# ═══════════════════════════════════════════════════════════
# A F-06 事件抽取
# ═══════════════════════════════════════════════════════════
print('== A · F-06 事件抽取 ==')
cl = cs._split_clauses('甲公司成立。乙公司上市！丙公司退市？丁公司并购；戊公司拆分')
check('A1 标点分句（。！？；）→ 5 句', len(cl) == 5, str(len(cl)))
check('A2 分句去空白 / 剔空句', cs._split_clauses('  甲 。  乙  ') == ['甲', '乙'])
check('A3 换行亦为句界', len(cs._split_clauses('甲\n乙\n丙')) == 3)
check('A4 非字符串输入安全（None→[]；数字→str 归一）',
      cs._split_clauses(None) == [] and cs._split_clauses('') == []
      and cs._split_clauses(123) == ['123'])
check('A5 分句有界（≤24 句）', len(cs._split_clauses('甲。' * 100)) <= cs._EVENT_MAX_CLAUSES)

evs = cs._extract_events('甲公司2024年Q1营收增长12%。', '甲')
check('A6 事件非空且 schema 六字段齐备',
      evs and all({'subject', 'aspect', 'value', 'polarity',
                   'time_span', 'event_sig'} <= set(e) for e in evs), str(len(evs)))
check('A7 event_sig 规则 = f"{subject}|{aspect}|{time_key}"（v2.2.0 三元身份）',
      all(e['event_sig'] == f"{e['subject']}|{e['aspect']}|{e.get('time_key', 'na')}"
          for e in evs))
check('A8 subject 透传为 claim 主体键', all(e['subject'] == '甲' for e in evs))
check('A9 revenue 事件带 time_span',
      any(e['aspect'] == 'revenue' and e['time_span']
          and e['time_span']['label'] == '2024年Q1' for e in evs))

# 多事实句不跨句串味（F-06 原始缺口：全文单次扫描归属）
multi = cs._extract_events('甲公司2024年Q1营收增长12%。乙公司2025年Q3利润下滑35%。', '甲')
rev = [e for e in multi if e['aspect'] == 'revenue']
prf = [e for e in multi if e['aspect'] == 'profit']
check('A10 多事实句：revenue 归属第 1 句（无跨句串味）',
      all(e['time_span']['label'] == '2024年Q1' for e in rev) and rev, str(len(rev)))
check('A11 多事实句：profit 归属第 2 句',
      all(e['time_span']['label'] == '2025年Q3' for e in prf) and prf, str(len(prf)))
check('A12 无方面句 → 无事件', cs._extract_events('今天天气不错。', '甲') == [])
check('A13 空/None 文本 → []',
      cs._extract_events('', '甲') == [] and cs._extract_events(None, '甲') == [])
check('A14 事件数有界', len(cs._extract_events('营收增长。' * 200, '甲')) <= cs._EVENT_MAX_EVENTS)
check('A15 抽取异常不崩（返回列表）', isinstance(cs._extract_events('营收增长。', None), list))

# ═══════════════════════════════════════════════════════════
# B F-04 期间裁决
# ═══════════════════════════════════════════════════════════
print('== B · F-04 期间裁决 ==')
_d = cs._period_adjudicate(
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('甲', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('B1 同主体同方面期间不相交 → disjoint', _d['disjoint_slots'] == ['revenue'], str(_d))
check('B2 降权 reasons 含「期间裁决」', any('期间裁决' in x for x in _d['reasons']))

_o = cs._period_adjudicate(
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))])
check('B3 期间相同 → overlap（不降权）', _o['disjoint_slots'] == [] and _o['overlap_slots'] == ['revenue'])

_n = cs._period_adjudicate(
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('甲', 'revenue', None)])
check('B4 任一期间缺失 → 不判 disjoint', _n['disjoint_slots'] == [])

_x = cs._period_adjudicate(
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('乙', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('B5 跨主体 → 不裁决', _x['disjoint_slots'] == [] and _x['overlap_slots'] == [])

_e = cs._period_adjudicate(
    [_ev('', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('B6 空主体 → 不裁决（旧契约）', _e['disjoint_slots'] == [])

_dif = cs._period_adjudicate(
    [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01')),
     _ev('甲', 'trend_dir', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
    [_ev('甲', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01')),
     _ev('甲', 'trend_dir', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('B7 多槽并列 → disjoint 排序稳定', _dif['disjoint_slots'] == ['revenue', 'trend_dir'])

# 端到端：降权但不滤除
_r = cs.score_contradiction({'text': '2024年Q1营收增长12%', 'entity': '甲'},
                            {'text': '2025年Q3营收大幅下滑', 'entity': '甲'})
check('B8 端到端 期间不相交 → 降权（60→30）', _r['score'] == 30, str(_r['score']))
check('B9 降权不滤除（score ≥ 1 且仍判 conflict）',
      _r['score'] >= 1 and _r['verdict'] == 'conflict')
check('B10 端到端 period_adjudication=disjoint', _r['period_adjudication'] == 'disjoint')
check('B11 端到端 disjoint 槽含 revenue 与 trend_dir',
      set(_r['period_disjoint_slots']) == {'revenue', 'trend_dir'}, str(_r['period_disjoint_slots']))

# ═══════════════════════════════════════════════════════════
# C F-07 time 路（主体闸 + 事件级对齐）
# ═══════════════════════════════════════════════════════════
print('== C · F-07 time 路 ==')
_legacy = cs.time_slot_score('产品2023年Q1发布', '产品2024年第三季度才发布')
check('C1 旧 2 参签名兼容（全文级 conflict 60）',
      _legacy['conflict'] is True and _legacy['score'] == 60
      and _legacy.get('mode') == 'fulltext', str(_legacy.get('mode')))
check('C2 None 公开调用不崩（coverage=partial）',
      cs.time_slot_score(None, '2024年Q1')['coverage'] == 'partial')
_ov = cs.time_slot_score('2024年3月发布', '2024年第一季度发布')
check('C3 旧签名同季度相容不冲突', _ov['conflict'] is False)

_ea = [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))]
_eb = [_ev('甲', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01'))]
_rev = cs.time_slot_score('', '', '甲', '甲', _ea, _eb)
check('C4 同主体同方面事件级 → 冲突 60（mode=event）',
      _rev['conflict'] is True and _rev['score'] == 60 and _rev['mode'] == 'event')
check('C5 事件级 time_slots 取自事件', _rev['time_slots_a'][0]['label'] == '2024年Q1')

_cross = cs.time_slot_score('2024年Q1营收增长', '2025年Q3营收下滑', '甲', '乙')
check('C6 跨主体 → 不可对拍（partial / 0 分，不误报）',
      _cross['coverage'] == 'partial' and _cross['conflict'] is False
      and _cross.get('note') == 'cross_subject')

_asp = cs.time_slot_score('', '', '甲', '甲', _ea,
                          [_ev('甲', 'profit', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('C7 无同方面事件对 → 不可对拍（partial）',
      _asp['coverage'] == 'partial' and _asp['conflict'] is False, str(_asp.get('coverage')))

_over = cs.time_slot_score('', '', '甲', '甲', _ea,
                           [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))])
check('C8 同方面期间相交 → 不冲突（both_timed）',
      _over['conflict'] is False and _over['coverage'] == 'both_timed')

_mix = cs.time_slot_score('', '', '甲', '甲',
                          [_ev('甲', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01')),
                           _ev('乙', 'revenue', _sp('2024年Q1', '2024-01-01', '2024-04-01'))],
                          [_ev('甲', 'revenue', _sp('2025年Q3', '2025-07-01', '2025-10-01'))])
check('C9 主体过滤：他主体事件不参与', _mix['conflict'] is True and _mix['score'] == 60)
check('C10 事件级返回 event_pairs',
      isinstance(_rev.get('event_pairs'), list) and _rev['event_pairs'])

# ═══════════════════════════════════════════════════════════
# D claim 穿透（conflict_v3）
# ═══════════════════════════════════════════════════════════
print('== D · claim 穿透 ==')
try:
    _srcs = [{'title': 'T1', 'url': 'https://a/1', 'text': 'OpenAI 2024年Q1营收增长12%。'},
         {'title': 'T2', 'url': 'https://b/2', 'text': 'OpenAI 2025年Q3营收大幅下滑。'}]
    _claims = cv3._extract_fact_claims(_srcs, {}) if _CV3_OK else []
    check('D1 _extract_fact_claims 产出 claim 携带 events 字段',
          bool(_claims) and 'events' in _claims[0] and _claims[0]['events'],
          str(len(_claims)))
    _confs = cv3._group_and_detect(_claims, {}) if _CV3_OK else []
    check('D2 _group_and_detect 的 claim_a/b 携带 events',
          bool(_confs) and _confs[0]['claim_a'].get('events') is not None
          and _confs[0]['claim_b'].get('events') is not None)
    if _confs:
        _sc = cs.score_contradiction(_confs[0]['claim_a'], _confs[0]['claim_b'])
        check('D3 生产链端到端触发期间裁决（disjoint）',
              _sc['period_adjudication'] == 'disjoint' and _sc['score'] == 30,
              f"score={_sc['score']} adj={_sc['period_adjudication']}")
    else:
        check('D3 生产链端到端触发期间裁决（disjoint）', False, 'no conflict')
except Exception as _ex:  # noqa: BLE001
    check('D1 _extract_fact_claims 产出 claim 携带 events 字段', False, str(_ex))
    check('D2 _group_and_detect 的 claim_a/b 携带 events', False, str(_ex))
    check('D3 生产链端到端触发期间裁决（disjoint）', False, str(_ex))

# 事件在原始 body 抽取（超越 text[:500] 截断）
_long_body = 'OpenAI' + '。' + '无关内容' * 300 + '。OpenAI 2024年Q1营收增长12%。'
_long_ev = cs._extract_events(_long_body, 'OpenAI')
check('D4 长正文事件不丢（原始 body 抽取，越 500 截断）', bool(_long_ev), str(len(_long_ev)))
check('D5 claim 无 events → scorer 就地兜底不崩',
      cs.score_contradiction({'text': '甲 2024年Q1营收增长12%', 'entity': '甲'},
                             {'text': '甲 2025年Q3营收下滑', 'entity': '甲'})['score'] >= 1)

# ═══════════════════════════════════════════════════════════
# E 零回归
# ═══════════════════════════════════════════════════════════
print('== E · 零回归 ==')
_p2 = cs.score_contradiction(
    {'text': '该公司 2024年Q1 营收同比增长 30%，实现盈利，业务开源。'},
    {'text': '该公司 2025年Q3 营收同比下滑，出现亏损，项目闭源。'})
check('E1 既有时间矛盾语料判定不变（无主体 → 不降权，≥60）',
      _p2['verdict'] == 'conflict' and _p2['score'] >= 60, str(_p2['score']))
_c15 = cs.score_contradiction({'text': '该公司2023年Q1发布新品'},
                              {'text': '该产品2024年第三季度才发布'})
check('E2 无主体时间矛盾 → mode=time / time_score=60（全文级零回归）',
      _c15['scorer_mode'] == 'time' and _c15['time_score'] == 60)
_c18 = cs.score_contradiction({'text': '公司营收增长35%', 'entity': 'X'},
                              {'text': '公司营收仅增长12%', 'entity': 'X'})
check('E3 键控数值冲突零回归（无时间 → 不裁决）',
      _c18['verdict'] == 'conflict' and 'revenue' in _c18['conflict_slots']
      and _c18['period_adjudication'] == 'none')
_need = {'score', 'severity', 'reasons', 'neg_hits', 'shared_slots', 'slot_score',
         'neg_score', 'keyed_score', 'conflict_slots', 'scorer_mode', 'time_score',
         'time_slots_a', 'time_slots_b', 'time_coverage', 'assessable', 'verdict'}
_sc0 = cs.score_contradiction({'text': 'a'}, {'text': 'b'})
check('E4 返回 schema 为超集（既有 16 字段 + 新增字段）',
      _need.issubset(set(_sc0)) and {'period_adjudication', 'event_count_a',
                                     'time_mode'} <= set(_sc0))
check('E5 既有语料 period_adjudication 默认 none',
      _sc0['period_adjudication'] == 'none')
check('E6 空 claim 不崩且事件计数为 0',
      cs.score_contradiction({}, {})['event_count_a'] == 0)

# ═══════════════════════════════════════════════════════════
# F · 三缺口收口守护（v2.1.2 批次补强：B2 去重 / event_matches / B层透传）
# ═══════════════════════════════════════════════════════════
print('== F · 三缺口收口 ==')
# Gap3 B2：同主体+同方面+同值+同极性+同期间 → 同一事实，去重
_dup = cs._extract_events(
    '甲公司2024年Q1营收增长12%。甲公司2024年Q1营收增长12%。', '甲')
_dup_rev = [e for e in _dup if e['aspect'] == 'revenue']
check('F1 同事实重复句 → 去重为 1（B2 独立去重键）',
      len(_dup_rev) == 1, str(len(_dup_rev)))
_diffv = cs._extract_events(
    '甲公司2024年Q1营收增长12%。甲公司2024年Q1营收增长15%。', '甲')
# 百分比增长率按 v2.0.0 既定裁决归属 trend_dir（一值双属只归最近指标词）
_diffv_td = [e for e in _diffv if e['aspect'] == 'trend_dir']
check('F2 同主体同方面不同值 → 不去重（2 条 trend_dir）',
      len(_diffv_td) == 2, str(len(_diffv_td)))

# Gap2：event_matches 明细字段
_m = cs.score_contradiction(
    {'text': '甲公司2024年Q1营收增长12%', 'entity': '甲'},
    {'text': '甲公司2025年Q3营收下滑', 'entity': '甲'})
check('F3 score_contradiction 返回含 event_matches', 'event_matches' in _m)
_fm = [x for x in _m['event_matches'] if x['aspect'] == 'revenue']
check('F4 event_matches 含 revenue 对，time_relation=disjoint',
      bool(_fm) and _fm[0]['time_relation'] == 'disjoint', str(_fm))
check('F5 event_matches 结构五字段齐备',
      bool(_fm) and {'subject', 'aspect', 'time_relation',
                     'value_relation', 'score'} <= set(_fm[0]),
      str(_fm[0]) if _fm else 'empty')

# Gap1：B 层 score_with_llm_async 透传 A 层结构化字段
import asyncio  # noqa: E402


async def _llm_passthrough():
    def _fake(_p):
        return '80'
    return await cs.score_with_llm_async(
        {'text': '甲公司2024年Q1营收增长12%', 'entity': '甲'},
        {'text': '甲公司2025年Q3营收下滑', 'entity': '甲'},
        llm_router=_fake)


_r = asyncio.run(_llm_passthrough())
check('F6 B层透传 keyed_score（非 None）', _r.get('keyed_score') is not None,
      str(_r.get('keyed_score')))
check('F7 B层透传 verdict/conflict_slots/scorer_mode/time_mode/event_matches',
      {'verdict', 'conflict_slots', 'scorer_mode', 'time_mode',
       'event_matches'}.issubset(set(_r)),
      str({k: _r.get(k) is not None for k in
           ('verdict', 'conflict_slots', 'scorer_mode', 'time_mode', 'event_matches')}))

print(f'\n=== event_slots 套件结果: {_PASS} PASS / {_FAIL} FAIL ===')
if _FAIL:
    sys.exit(1)
print('ALL PASS')
