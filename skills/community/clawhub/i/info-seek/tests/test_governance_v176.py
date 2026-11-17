#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_governance_v176.py — 治理闭环三缺口修复验证

G2-1 generate_feedback 单源收敛（pipeline ⟷ report.py 对拍）
G2-2 质量反馈维（低 relevance 成功源 −5）
G2-3 apply_feedback 路径锚定（INFOSEEK_DATA_DIR / 回退）
"""
import json
import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
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


DETAILS = [
    {'status': 'failed', 'anchor': {'name': 'a', 'entry': 'https://a', 'score': 70},
     'steps': [{'status': 'fail', 'reason': 'x'}]},
    {'status': 'dead_link', 'anchor': {'name': 'd', 'entry': 'https://d', 'score': 70}},
    {'status': 'needs_tier2', 'anchor': {'name': 'e', 'entry': 'https://e', 'score': 70}},
    {'status': 'success', 'anchor': {'name': 'b', 'entry': 'https://b', 'score': 70}, 'relevance': 10},
    {'status': 'success', 'anchor': {'name': 'c', 'entry': 'https://c', 'score': 70}, 'relevance': 50},
]

print('[G2-2] 质量反馈维')
fb = p.generate_feedback(DETAILS)
by = {f['anchor_name']: f for f in fb}
check('failed → −10', by['a']['suggested_penalty'] == -10 and by['a']['feedback_type'] == 'failure')
check('dead_link → −20', by['d']['suggested_penalty'] == -20)
check('needs_tier2 → −10', by['e']['suggested_penalty'] == -10)
check('low_relevance(10) → −5 质量维',
      by['b']['feedback_type'] == 'quality' and by['b']['suggested_penalty'] == -5)
check('relevance(50) 无反馈', 'c' not in by)
check('质量维带 failure_type=low_relevance', by['b']['failure_type'] == 'low_relevance')
check('每条含 suggested_new_score', all('suggested_new_score' in f for f in fb))

print('[G2-1] 单源收敛对拍')
import infoseek_report as rep  # noqa: E402
check('report.generate_feedback == pipeline', rep.generate_feedback(DETAILS) == fb)
check('空输入一致', rep.generate_feedback([]) == p.generate_feedback([]))

print('[G2-3] 路径锚定')
_d = tempfile.mkdtemp(prefix='gov_')
os.environ['INFOSEEK_DATA_DIR'] = _d
check('锚定 INFOSEEK_DATA_DIR', p._default_anchor_db_path() == os.path.join(_d, 'anchor_db.json'))
del os.environ['INFOSEEK_DATA_DIR']
check('无 env → ~/.infoseek', p._default_anchor_db_path().endswith(os.path.join('.infoseek', 'anchor_db.json')))

print('[G2-3b] apply_feedback 实写')
os.environ['INFOSEEK_DATA_DIR'] = _d
_db = os.path.join(_d, 'anchor_db.json')
with open(_db, 'w', encoding='utf-8') as f:
    json.dump([{'name': 'a', 'entry': 'https://a', 'score': 70}], f)
n = p.apply_feedback(p.generate_feedback(DETAILS))
with open(_db, encoding='utf-8') as f:
    db = json.load(f)
check('应用 1 条降级', n == 1, str(n))
check('分数 70→60（−10）', db[0]['score'] == 60, str(db[0]['score']))
check('score_history 记录', db[0].get('score_history') == [70], str(db[0].get('score_history')))
del os.environ['INFOSEEK_DATA_DIR']

print(f'\n=== test_governance_v176: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
