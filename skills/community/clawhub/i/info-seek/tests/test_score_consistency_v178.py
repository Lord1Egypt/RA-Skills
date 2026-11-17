#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_score_consistency_v178.py — v1.7.8 评分口径一致性

核心断言：生效版 anchor_adapter.calculate_score ≡ core.anchor_score_v2.compute_final_score_v2
（同输入 → 同输出，逐字段恒等）。

背景：v1.7.8 删除 v1.2 activity 死代码链（471 行）后，calculate_score 仅为转调
compute_final_score_v2 的兼容 shim。本测试防止未来 calculate_score 偏离 v2 口径，
并验证「唯一评分口径 = v2 四维」声明落地（SKILL.md §5.1）。

覆盖：
  C1 全字段恒等（3 source × 9 参数组 = 27）
  C2 关键字段（after_whitelist_final + classification）
  C3 shim 验证（calculate_score 发 DeprecationWarning）
  C4 死代码清零（v1.2 activity / v1.5 / v1.6 孤儿符号已删除）
"""
import os
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'core'))

# 隔离：禁用平台 WebSearch（防 sidecar 自动 spawn 污染）
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
warnings.filterwarnings('ignore', category=DeprecationWarning)

import anchor_adapter  # noqa: E402
from anchor_adapter import calculate_score  # noqa: E402
from anchor_score_v2 import compute_final_score_v2  # noqa: E402

_P = _F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  PASS {name} {extra}')
    else:
        _F += 1
        print(f'  FAIL {name} {extra}')


# ── 3 个典型 source（高分中文 / 中分混合 / 空边界）──
SOURCES = [
    {'interaction': 80, 'topic_match': 90, 'credibility': 95, 'llm_readability': 85,
     'url': 'https://baosteel.com/x', 'platform': '宝钢集团', 'text': '钢卷分切工艺圆盘刀重叠量'},
    {'interaction': 30, 'topic_match': 40, 'credibility': 50, 'llm_readability': 45,
     'url': 'https://zhihu.com/q', 'platform': '知乎', 'text': 'AI 大模型估值讨论'},
    {'interaction': 0, 'topic_match': 0, 'credibility': 0, 'llm_readability': 0,
     'url': '', 'platform': '', 'text': ''},
]

PROF = {'name': 'steel', 'raw': '| 来源 | Tier |\n| Baosteel | Tier 1 |'}

# ── 9 组参数（覆盖各维度开关 + domain profile + prefer_kb + 边界）──
PARAM_SETS = [
    dict(subject='钢卷分切工艺', with_llm_readability=True),
    dict(subject='钢卷分切工艺', with_llm_readability=False),
    dict(subject='AI 大模型', with_llm_readability=True, with_semantic=True),
    dict(subject='AI 大模型', with_llm_readability=True, with_cross_platform=True, platforms=5),
    dict(subject='钢铁 宝钢', with_llm_readability=True, with_domain=True),
    dict(subject='钢铁 宝钢 高炉', with_llm_readability=True, with_domain=True, prefer_kb=True),
    dict(subject='钢铁 宝钢', with_llm_readability=True, with_domain=True, domain_profile=PROF),
    dict(subject='钢卷分切', with_llm_readability=True, with_semantic=True,
         with_cross_platform=True, with_domain=True, domain_profile=PROF,
         platforms=3, prefer_kb=True),
    dict(subject='', with_llm_readability=True, days_since_published=200),
]

print('[C1] 全字段恒等 calculate_score == compute_final_score_v2')
for si, src in enumerate(SOURCES):
    for pi, params in enumerate(PARAM_SETS):
        r1 = calculate_score(dict(src), **params)
        r2 = compute_final_score_v2(dict(src), **params)
        same = (r1 == r2)
        check(f'C1 S{si}P{pi} 全字段恒等', same,
              '' if same else f'\n    calc={r1}\n    v2  ={r2}')

print('[C2] 关键字段 after_whitelist_final + classification')
for si, src in enumerate(SOURCES):
    params = dict(subject='钢卷分切工艺', with_llm_readability=True, with_semantic=True)
    r1 = calculate_score(dict(src), **params)
    r2 = compute_final_score_v2(dict(src), **params)
    check(f'C2 S{si} after_whitelist_final 一致',
          r1.get('after_whitelist_final') == r2.get('after_whitelist_final'),
          f"={r1.get('after_whitelist_final')}")
    check(f'C2 S{si} classification 一致',
          r1.get('classification') == r2.get('classification'),
          f"={r1.get('classification')}")

print('[C3] shim 验证（calculate_score 转调 v2 + DeprecationWarning）')
with warnings.catch_warnings(record=True) as wl:
    warnings.simplefilter('always')
    calculate_score({'interaction': 50, 'topic_match': 50, 'credibility': 50,
                     'llm_readability': 50}, 'x', with_llm_readability=True)
    dep = any(issubclass(x.category, DeprecationWarning) for x in wl)
check('C3 calculate_score 发 DeprecationWarning（shim 标志）', dep)

print('[C4] v1.2 activity / v1.5 / v1.6 死代码清零')
check('C4 无 compute_anchor_score（v1.2 四轴）', not hasattr(anchor_adapter, 'compute_anchor_score'))
check('C4 无 apply_resurrection_batch（双层复活）', not hasattr(anchor_adapter, 'apply_resurrection_batch'))
check('C4 无 WEIGHTS（activity 权重）', not hasattr(anchor_adapter, 'WEIGHTS'))
check('C4 无 TIER1_THRESHOLD（activity 阈值）', not hasattr(anchor_adapter, 'TIER1_THRESHOLD'))
check('C4 无 compute_anchor_score_v15（v1.5 孤儿）', not hasattr(anchor_adapter, 'compute_anchor_score_v15'))
check('C4 无 compute_cross_platform_score（v1.6 孤儿）', not hasattr(anchor_adapter, 'compute_cross_platform_score'))

print(f'\n=== test_score_consistency_v178: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
