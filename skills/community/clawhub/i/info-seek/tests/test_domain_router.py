#!/usr/bin/env python3
"""test_domain_router.py — v1.8.2 A(多域交集非破坏性扩展) + B(prefer_kb 加分分段)

覆盖：
  A. detect_domain 多域交集判定（intersect_domains / is_intersect / prefer_kb）
     含默认分支字段齐全、gap env 可配、向后兼容
  B. apply_profile_to_score 泛化信任源解析 + prefer_kb 加分分段 + 上限
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))

from domain_router import (  # noqa: E402
    apply_profile_to_score,
    detect_domain,
    _extract_trust_sources,
    _intersect_gap,
)

_P = _F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  PASS {name} {extra}')
    else:
        _F += 1
        print(f'  FAIL {name} {extra}')


MULTI = 'AI 大模型 股票 估值 财务 钢铁 宝钢 高炉'
SINGLE = 'AI 大模型 芯片 算力 英伟达'

# ─────────────────────── A. detect_domain 多域交集 ───────────────────────
print('[A] detect_domain 多域交集')

r = detect_domain(SINGLE)
check('A1 单域 is_intersect=False', r['is_intersect'] is False, r['domain'])
check('A1 单域 prefer_kb=False', r['prefer_kb'] is False)

r = detect_domain(MULTI)
check('A2 多域 is_intersect=True', r['is_intersect'] is True, str(r['intersect_domains']))
check('A2 intersect_domains>=2', len(r['intersect_domains']) >= 2, str(r['intersect_domains']))
check('A2 prefer_kb=is_intersect', r['prefer_kb'] == r['is_intersect'])
check('A2 domain 保留 best 且属交集', r['domain'] in r['intersect_domains'], r['domain'])
check('A2 向后兼容含旧字段', all(k in r for k in ('domain', 'score', 'candidates', 'profile_path', 'is_default')))

r = detect_domain('')
check('A3 空主题 is_default', r['is_default'] is True)
check('A3 空主题三字段齐全', r['intersect_domains'] == [] and r['is_intersect'] is False and r['prefer_kb'] is False)

os.environ['INFOSEEK_DOMAIN_INTERSECT_GAP'] = '99'
check('A4 gap=99 生效', _intersect_gap() == 99.0)
check('A4 gap 拉大→宽松(判交集)', detect_domain(MULTI)['is_intersect'] is True)
os.environ['INFOSEEK_DOMAIN_INTERSECT_GAP'] = '0'
check('A4 gap=0→严格(多域不判交集)', detect_domain(MULTI)['is_intersect'] is False)
check('A4 gap=0→单域不判交集', detect_domain(SINGLE)['is_intersect'] is False)
os.environ['INFOSEEK_DOMAIN_INTERSECT_GAP'] = 'abc'
check('A4 gap 非法值回落 2.0', _intersect_gap() == 2.0)
del os.environ['INFOSEEK_DOMAIN_INTERSECT_GAP']
check('A4 gap 缺省 2.0', _intersect_gap() == 2.0)

# ─────────────────────── B. apply_profile_to_score ───────────────────────
print('[B] apply_profile_to_score prefer_kb 分段 + 泛化信任源')

PROF = {'name': 't', 'raw': '| 来源 | Tier |\n| 宝钢 | Tier 1 |'}
base = {'url': 'http://example.com/a', 'platform': 'web'}
kb1 = {'url': 'http://example.com/a', 'platform': 'web', '_kb_domain': '钢铁', '_kb_hit_count': 1}
kb2 = {'url': 'http://example.com/a', 'platform': 'web', '_kb_domain': '钢铁', '_kb_hit_count': 2}

check('B1 无kb→0', apply_profile_to_score(dict(base), PROF, prefer_kb=True)['domain_bonus'] == 0)
check('B1 kb×1→8', apply_profile_to_score(dict(kb1), PROF, prefer_kb=True)['domain_bonus'] == 8)
check('B1 kb×2→12', apply_profile_to_score(dict(kb2), PROF, prefer_kb=True)['domain_bonus'] == 12)
check('B2 prefer_kb=False→kb不加分', apply_profile_to_score(dict(kb2), PROF, prefer_kb=False)['domain_bonus'] == 0)
check('B2 默认参数(向后兼容)=False', apply_profile_to_score(dict(kb2), PROF)['domain_bonus'] == 0)
check('B3 分段不越上限20', apply_profile_to_score(dict(kb2), PROF, prefer_kb=True)['domain_bonus'] <= 20)
check('B3 domain_applied 保留', apply_profile_to_score(dict(base), PROF)['domain_applied'] == 't')

check('B4 抽取「来源/Tier」行', len(_extract_trust_sources(PROF['raw'])) > 0)
check('B4 无提示行→空', _extract_trust_sources('随便一段没有标记的文本 关键词') == [])
check('B4 空 raw 安全', _extract_trust_sources('') == [])

s = {'url': 'http://baosteel.com.cn/report', 'platform': 'web'}
r = apply_profile_to_score(s, {'name': 'steel', 'raw': '| 来源 | Tier |\n| Baosteel | Tier 1 |'})
check('B5 信任源命中+5', r['domain_bonus'] == 5, str(r['domain_bonus']))

check('B6 空 profile 原样返回', apply_profile_to_score({'url': 'x'}, {}) == {'url': 'x'})

print(f'\n=== test_domain_router: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
