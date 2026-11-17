#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""v2.2.0 守护：score_with_llm / score_with_llm_async 字段齐备性。

背景：v2.2.0 阶段 3 收口前，LLM 成功路径返回内联窄白名单 dict，
截断 v2.1.2/v2.2.0 全部 event/period/keyed 字段。本套件固化契约：
  R1 同步成功（router 正常返回）→ 完整 A 层超集 + llm_used=True + 两个 suppression 空列表
  R2 同步 router=None 降级 → A 层超集 + llm_used=False
  R3 同步 router 抛异常 → A 层超集 + llm_used=False + llm_error
  R4 同步 router 正常但返回 None（无数字）→ 不崩，A 层超集
  R5 异步成功（sync callable 经 to_thread）→ 同 R1 契约
风格：顶层直跑 + sys.exit + 自报 N PASS / N FAIL，由 tests/run_all.py 收集。
"""
import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'core'))

import contradiction_scorer as cs  # noqa: E402

_PASS = 0
_FAIL = 0


def check(name, cond, extra=''):
    global _PASS, _FAIL
    if cond:
        _PASS += 1
        print(f'  [OK] {name}')
    else:
        _FAIL += 1
        print(f'  [FAIL] {name} {extra}')


# 多期间同主体同方面语料：保证 A 层产出事件槽/期间/三元相关字段
_A = {'text': '甲公司2023年营收100亿元，2024年营收120亿元',
      'entity': '甲', 'source_title': 'A'}
_B = {'text': '甲公司2023年营收80亿元，2024年营收90亿元',
      'entity': '甲', 'source_title': 'B'}

# A 层（score_contradiction）真实字段集——超集契约的基准
_BASE = cs.score_contradiction(_A, _B)
_BASE_KEYS = set(_BASE.keys())
check('基线 A 层含 v2.2.0 事件槽字段',
      {'event_pairs', 'event_disjoint_slots', 'event_overlap_slots',
       'period_pair_details', 'period_adjudication',
       'event_count_a', 'event_count_b', 'time_mode',
       'llm_time_suppressed', 'llm_time_suppressed_slots'} <= _BASE_KEYS,
      str(sorted(_BASE_KEYS)))

# ── R1 同步成功路径 ──────────────────────────────────────────────
_r1 = cs.score_with_llm(_A, _B, llm_router=lambda _p: '80')
check('R1 llm_used=True', _r1.get('llm_used') is True, str(_r1.get('llm_used')))
check('R1 llm_raw 透传', _r1.get('llm_raw') == '80', str(_r1.get('llm_raw')))
check('R1 score=max(LLM=80, A层)=85', _r1.get('score') == 85, str(_r1.get('score')))
check('R1 返回是 A 层完整超集（无字段截断）',
      _BASE_KEYS <= set(_r1.keys()),
      str(sorted(_BASE_KEYS - set(_r1.keys()))))
check('R1 llm_time_suppressed 显式空列表',
      _r1.get('llm_time_suppressed') == [], str(_r1.get('llm_time_suppressed')))
check('R1 llm_time_suppressed_slots 显式空列表',
      _r1.get('llm_time_suppressed_slots') == [],
      str(_r1.get('llm_time_suppressed_slots')))
check('R1 event_pairs 字段保留（非 None）',
      _r1.get('event_pairs') is not None)
check('R1 period_pair_details 字段保留（非 None）',
      _r1.get('period_pair_details') is not None)
check('R1 keyed/verdict/scorer_mode 保留',
      all(k in _r1 for k in ('keyed_score', 'verdict', 'scorer_mode')))

# ── R2 router=None 降级路径 ──────────────────────────────────────
_r2 = cs.score_with_llm(_A, _B, llm_router=None)
check('R2 llm_used=False', _r2.get('llm_used') is False)
check('R2 返回 A 层完整超集', _BASE_KEYS <= set(_r2.keys()),
      str(sorted(_BASE_KEYS - set(_r2.keys()))))
check('R2 suppression 空列表齐备',
      _r2.get('llm_time_suppressed') == []
      and _r2.get('llm_time_suppressed_slots') == [])

# ── R3 router 抛异常降级路径 ─────────────────────────────────────
def _boom(_p):
    raise RuntimeError('router down')


_r3 = cs.score_with_llm(_A, _B, llm_router=_boom)
check('R3 llm_used=False', _r3.get('llm_used') is False)
check('R3 llm_error 记录异常', 'router down' in str(_r3.get('llm_error')),
      str(_r3.get('llm_error')))
check('R3 返回 A 层完整超集', _BASE_KEYS <= set(_r3.keys()),
      str(sorted(_BASE_KEYS - set(_r3.keys()))))
check('R3 suppression 空列表齐备',
      _r3.get('llm_time_suppressed') == []
      and _r3.get('llm_time_suppressed_slots') == [])

# ── R4 router 返回 None（正则无数字，score=0）不崩 ───────────────
_r4 = cs.score_with_llm(_A, _B, llm_router=lambda _p: None)
check('R4 llm_used=True 且不崩', _r4.get('llm_used') is True)
check('R4 None 归一化为 llm_raw="" （非伪装异常降级）',
      _r4.get('llm_raw') == '' and 'llm_error' not in _r4,
      str({k: _r4.get(k) for k in ('llm_raw', 'llm_error')}))
check('R4 无数字→score 回落 A 层', _r4.get('score') == _BASE.get('score'),
      f"{_r4.get('score')} vs {_BASE.get('score')}")
check('R4 返回 A 层完整超集', _BASE_KEYS <= set(_r4.keys()),
      str(sorted(_BASE_KEYS - set(_r4.keys()))))
check('R4 suppression 空列表齐备',
      _r4.get('llm_time_suppressed') == []
      and _r4.get('llm_time_suppressed_slots') == [])

# ── R5 异步成功路径（同步 callable → to_thread 包装）─────────────


async def _arun():
    return await cs.score_with_llm_async(
        _A, _B, llm_router=lambda _p: '75')


_r5 = asyncio.run(_arun())
check('R5 async llm_used=True', _r5.get('llm_used') is True)
check('R5 async 返回 A 层完整超集', _BASE_KEYS <= set(_r5.keys()),
      str(sorted(_BASE_KEYS - set(_r5.keys()))))
check('R5 async suppression 空列表齐备',
      _r5.get('llm_time_suppressed') == []
      and _r5.get('llm_time_suppressed_slots') == [])
check('R5 async event_pairs/period_pair_details 保留',
      _r5.get('event_pairs') is not None
      and _r5.get('period_pair_details') is not None)

print(f'\n=== llm_fields 套件结果: {_PASS} PASS / {_FAIL} FAIL ===')
if _FAIL:
    sys.exit(1)
print('ALL PASS')
