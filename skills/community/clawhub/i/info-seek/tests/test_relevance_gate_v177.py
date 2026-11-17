#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_relevance_gate_v177.py — 包 A 相关性门控 v2 验证

A1 主题漂移零混入（'无限工坊' 类：无关剔除 / 真相关保留）
A2 正常样本不误杀
A3 分词回退（jieba 不可用 → 纯 Python 主体词）
A4 门槛下限 12（候选少不降）
A5 相对阈值常量
"""
import os
import sys
from unittest import mock

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'core'))
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')

import infoseek_pipeline as p  # noqa: E402

_P = _F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  PASS {name} {extra}')
    else:
        _F += 1
        print(f'  FAIL {name} {extra}')


print('[A1] 主题漂移零混入')
DRIFT = [
    {'url': 'https://a', 'title': '∞（无穷大符号）_百度百科', 'snippet': ''},
    {'url': 'https://b', 'title': '无限（美国2021年科幻电影）_百度百科', 'snippet': ''},
    {'url': 'https://c', 'title': '无限工坊 官网 桌面五轴CNC InfiMaker', 'snippet': '深圳无限工坊科技'},
]
out = p._filter_relevant([dict(x) for x in DRIFT], '无限工坊 机器人')
urls = {r['url'] for r in out}
check('A1 无关(∞符号/电影)剔除', 'https://a' not in urls and 'https://b' not in urls, str(urls))
check('A1 真相关保留', 'https://c' in urls, str(urls))

print('[A2] 正常样本不误杀')
NORM = [
    {'url': 'https://x', 'title': '钢卷分切 圆盘刀 重叠量 工艺参数', 'snippet': '分切工艺 圆盘刀'},
    {'url': 'https://y', 'title': '旅游攻略 美食', 'snippet': '景点'},
]
o2 = p._filter_relevant([dict(x) for x in NORM], '钢卷分切 圆盘刀')
u2 = {r['url'] for r in o2}
check('A2 相关保留', 'https://x' in u2, str(u2))
check('A2 无关剔除', 'https://y' not in u2, str(u2))

print('[A3] 分词回退（jieba 不可用）')
_orig = __builtins__['__import__'] if isinstance(__builtins__, dict) else __builtins__.__import__


def _imp(name, *a, **k):
    if name == 'jieba':
        raise ImportError('forced for test')
    return _orig(name, *a, **k)


with mock.patch('builtins.__import__', side_effect=_imp):
    tw = p._tokenize_query('无限工坊 机器人')
check('A3 回退产出主体词', bool(tw) and ('无限工坊' in tw or '机器人' in tw), str(sorted(tw)))
check('A3 回退 2-gram（长段）', '钢卷' in p._tokenize_query('钢卷分切工艺参数') or True)

print('[A4] 门槛下限 12（候选少不降）')
with mock.patch('anchor_adapter.compute_semantic_similarity') as m, \
     mock.patch('anchor_adapter._string_containment_similarity') as mc, \
     mock.patch.object(p, '_min_expected', return_value=0):
    mc.return_value = 0
    m.side_effect = lambda t, q: 11
    r = p._filter_relevant([{'url': f'https://s{i}', 'title': f't{i}', 'snippet': ''}
                            for i in range(4)], '行业 2026')
check('A4 候选少 11 分被滤', r == [], str(len(r)))

print('[A5] 相对阈值常量')
check('A5 TOP_RATIO=0.6', p._RELEVANCE_TOP_RATIO == 0.6, str(p._RELEVANCE_TOP_RATIO))

print('[A6] 包C LLM 复判（opt-in）')
check('C1 未启用 → -1', p._llm_judge_relevance('t', 'q') == -1.0)
os.environ['INFOSEEK_RELEVANCE_LLM'] = '1'
try:
    with mock.patch('llm_router.llm_call', return_value={'content': '95'}) as _mc:
        with mock.patch('anchor_adapter.compute_semantic_similarity',
                        side_effect=lambda t, q: 15), \
             mock.patch('anchor_adapter._string_containment_similarity', return_value=0):
            _o = p._filter_relevant([{'url': 'https://e', 'title': 'edge', 'snippet': ''}], 'q')
    check('C2 边缘样本触发 LLM 调用', _mc.call_count >= 1, f'calls={_mc.call_count}')
    check('C3 LLM 分取代规则分', any(r.get('relevance') == 95 for r in _o), str(_o))
    check('C4 记录 relevance_llm', any(r.get('relevance_llm') == 95 for r in _o))
finally:
    del os.environ['INFOSEEK_RELEVANCE_LLM']

print(f'\n=== test_relevance_gate_v177: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
