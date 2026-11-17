# -*- coding: utf-8 -*-
"""P1 硬化守护（2026-09-18）：类型保护 + bool 排除 + 渲染兜底 + 矛盾路 None 防护。

对应缺口：
  DEF-09  score='0.72' 字符串脏分曾 TypeError 击穿评分链 → 入口类型保护
  DEF-08  score=True 布尔被量纲归一为 100（bool 是 int 子类）→ bool 排除
  G-05    模板源缺 score/title/text、非 dict 源、subject=None 曾击穿渲染 → 渲染兜底
  F-12    claim text=None/数字曾 AttributeError 击穿矛盾评分 → 入参归一

风格：顶层直跑 + sys.exit + 自报 N PASS / N FAIL，由 tests/run_all.py 收集。
"""
import os
import sys

os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
_ROOT = '/root/.skills/infoseek'
for p in (f'{_ROOT}/scripts', f'{_ROOT}/core'):
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


# ── 类型保护 + bool 排除（score_source 入口）──────────────────────
print('== P1 · score 入参类型保护 / bool 排除 ==')
from infoseek_core_v2 import score_source, _coerce_incoming_score  # noqa: E402

U = 'http://example.com/p'

# 直接锁定纯函数契约
check('coerce str "0.72" → 72 normalized',
      _coerce_incoming_score('0.72') == (72.0, True, False))
check('coerce str "72" → 72 不归一', _coerce_incoming_score('72') == (72.0, False, False))
check('coerce str "abc" → 0 invalid', _coerce_incoming_score('abc') == (0, False, True))
check('coerce str " 0.5 " strip → 50', _coerce_incoming_score(' 0.5 ') == (50.0, True, False))
check('coerce bool True → 0 不归一 invalid=False',
      _coerce_incoming_score(True) == (0, False, False))
check('coerce bool False → 0', _coerce_incoming_score(False) == (0, False, False))
check('coerce None → 0', _coerce_incoming_score(None) == (0, False, False))
check('coerce nan → 0 invalid', _coerce_incoming_score(float('nan'))[0] == 0
      and _coerce_incoming_score(float('nan'))[2] is True)
check('coerce inf → 0 invalid', _coerce_incoming_score(float('inf'))[2] is True)
check('coerce 1.0001 原样透传不归一',
      _coerce_incoming_score(1.0001) == (1.0001, False, False))
check('coerce -0.5 原样（不崩）', _coerce_incoming_score(-0.5) == (-0.5, False, False))
check('coerce 72 百分制', _coerce_incoming_score(72) == (72.0, False, False))
check('coerce 0 empty 不归一', _coerce_incoming_score(0) == (0, False, False))

# 端到端：字符串脏分不再击穿，且正确归一
r = score_source({'url': U, 'title': 't', 'snippet': '', 'score': '0.72'}, '无关主题xyz')
check('E2E str 0.72 不崩 + base=72', r['base_score'] == 72 and r['final_score'] >= 40,
      f"base={r['base_score']} final={r['final_score']}")
check('E2E str 0.72 scale_normalized', r['scale_normalized'] is True)

r = score_source({'url': U, 'title': 't', 'snippet': '', 'score': 'abc'}, 'x')
check('E2E str abc 不崩 + invalid=True', r['score_invalid'] is True and r['base_score'] == 0)

r = score_source({'url': U, 'title': 't', 'snippet': '', 'score': True}, 'x')
check('E2E bool True 不被归一为100', r['base_score'] == 0 and r['scale_normalized'] is False)

r = score_source({'url': U, 'title': 't', 'snippet': '', 'score': None}, 'x')
check('E2E None 不崩', r['base_score'] == 0)

r = score_source({'url': U, 'title': 't', 'snippet': '', 'score': float('nan')}, 'x')
import math as _m
check('E2E nan 归零不传播', _m.isnan(r['base_score']) is False and r['score_invalid'] is True)

# 零回归：既有 OPEN-04 数值契约
check('回归 0.72 数值仍归一', score_source({'url': U, 'title': 't', 'score': 0.72},
      '无关xyz')['scale_normalized'] is True)
check('回归 72 数值不归一', score_source({'url': U, 'title': 't', 'score': 72},
      'x')['scale_normalized'] is False)

# ── 矛盾路 None / 非字符串防护 ────────────────────────────────────
print('== P1 · 矛盾评分 None/非字符串防护 ==')
import contradiction_scorer as cs  # noqa: E402

r = cs.score_contradiction({'text': None}, {'text': '公司2024年Q1成立'})
check('text=None 不崩 verdict 产出', r['verdict'] in ('conflict', 'no_conflict', 'not_assessable')
      and r['score'] == 0, f"verdict={r.get('verdict')}")
check('text=None 覆盖率 partial', r['time_coverage'] == 'partial')

r = cs.score_contradiction(None, {'text': 'x'})
check('claim=None 不崩', r['verdict'] == 'not_assessable' and r['score'] == 0)

r = cs.score_contradiction({'text': 123}, {'text': 456})
check('text 数字 不崩且不伪造矛盾', r['score'] == 0 and r['verdict'] == 'not_assessable')

r = cs.score_contradiction(None, None)
check('双侧 None neither', r['time_coverage'] == 'neither')

r = cs.time_slot_score(None, '2024年Q1')
check('time_slot_score(None) 公开调用不崩', r['coverage'] == 'partial' and r['conflict'] is False)

# v2.1.2 F-04 语义：同主体同方面、双方期间均已知且不相交 → 期间裁决**降权**（×0.5，不滤除）
r = cs.score_contradiction({'text': '2024年Q1营收增长12%', 'entity': '甲'},
                           {'text': '2025年Q3营收大幅下滑', 'entity': '甲'})
check('F-04 期间不相交 → 降权 60→30（不滤除）',
      r['score'] == 30 and r['verdict'] == 'conflict'
      and r['period_adjudication'] == 'disjoint'
      and 'revenue' in r['period_disjoint_slots'],
      f"score={r['score']} adj={r.get('period_adjudication')}")
# v2.1.2 F-04 语义：期间相同/相交 → 走现值冲突规则，不降权
r = cs.score_contradiction({'text': '2024年Q1营收增长12%', 'entity': '甲'},
                           {'text': '2024年Q1营收大幅下滑', 'entity': '甲'})
check('F-04 同期间 → 不降权（走现值冲突规则）',
      r['period_adjudication'] == 'overlap' and r['score'] >= 35,
      f"score={r['score']} adj={r.get('period_adjudication')}")
# v2.1.2 F-07：跨主体 → time 路主体闸生效，不误报
r = cs.score_contradiction({'text': '2024年Q1营收增长12%', 'entity': '甲'},
                           {'text': '2025年Q3营收大幅下滑', 'entity': '乙'})
check('F-07 跨主体 → time 路不误报（time_score=0）', r['time_score'] == 0,
      f"time={r['time_score']}")

# ── 渲染兜底 ─────────────────────────────────────────────────────
print('== P1 · 报告渲染兜底 ==')
from domain_orchestrator import DomainOrchestrator  # noqa: E402

orch = DomainOrchestrator()

res = orch.render_report('人工智能', [{'score': 80}])  # 缺 title/url/platform/text
check('源缺字段不崩', isinstance(res['markdown'], str) and len(res['markdown']) > 0)
check('缺字段源仍入围', res['qualified_count'] == 1)

bad_mix = ['str源', 123, None, {'score': 70, 'title': '正规源', 'url': U, 'platform': 'web'}]
res = orch.render_report('人工智能', bad_mix)
check('非 dict 脏源被跳过不崩', res['qualified_count'] == 1,
      f"q={res['qualified_count']}")
check('total 计原始数 / dropped 可观测',
      res['total_count'] == 4 and res['dropped_non_dict'] == 3,
      f"total={res['total_count']} drop={res['dropped_non_dict']}")

res = orch.render_report(None, [{'score': 70, 'title': 't', 'url': U}])
check('subject=None 不崩', isinstance(res['markdown'], str) and len(res['markdown']) > 0)

res = orch.render_report(123, [{'score': 70, 'title': 't', 'url': U}])
check('subject=数字 不崩', res is not None and 'markdown' in res)

res = orch.render_report('AI', None)
check('sources=None 不崩', res['total_count'] == 0 and res['qualified_count'] == 0)

# 全部模板（default + 5 域）脏上下文都不崩
for dom in list(orch.templates.keys()):
    try:
        r2 = orch.render_report('某主题', [{'score': 75}], domain_override=dom)
        ok = isinstance(r2['markdown'], str)
    except Exception as e:
        ok = False
        print(f'    模板 {dom} CRASH {type(e).__name__}: {e}')
    check(f'模板[{dom}] 最小上下文不崩', ok)

print(f'\n{_PASS} PASS / {_FAIL} FAIL')
sys.exit(1 if _FAIL else 0)
