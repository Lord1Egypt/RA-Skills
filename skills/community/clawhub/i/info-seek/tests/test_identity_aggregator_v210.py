# -*- coding: utf-8 -*-
"""
test_identity_aggregator_v210.py — Maigret×Sherlock 双源聚合去重引擎守护（v2.1.0）

覆盖：平台/URL 归一化去重、双源交叉确认+置信增强、单源高误报平台丢弃、
跨源复活、单源低质量降档、CN/IN/global 分区、缺口标记排除、空输入。
纯本地零网络。
"""
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, '..'))

from core.identity_aggregator import (
    aggregate, dedup_key, _norm_platform, _url_key, _region_of,
)

_P = 0
_F = 0


def check(name, cond, detail=''):
    global _P, _F
    if cond:
        _P += 1
    else:
        _F += 1
    print(('[PASS] ' if cond else '[FAIL] ') + name + (f'  ({detail})' if detail else ''))


def acc(platform, url, source, conf=0.85, rank=0, http=200, tags=None, gap=False):
    d = {'platform': platform, 'url': url, 'username': 'u', 'confidence': conf,
         'source': source, 'http_status': http, 'site_rank': rank}
    if tags:
        d['tags'] = tags
    if gap:
        d['_gap'] = True
    return d


# 归一化原语
check('平台别名 github→GitHub', _norm_platform('github') == 'GitHub')
check('平台别名 Twitter→X', _norm_platform('Twitter') == 'X')
check('URL 键去 www/尾斜杠/大小写',
      _url_key('https://www.GitHub.com/Alice/') == 'github.com|/alice')
check('不同路径不同键',
      _url_key('https://github.com/a') != _url_key('https://github.com/b'))

# 同账号跨平台大小写 + www 归一 → 去重为一并交叉确认
r = aggregate({'Maigret': [acc('GitHub', 'https://github.com/u', 'Maigret', 0.9, rank=10)],
               'Sherlock': [acc('github', 'https://www.github.com/u/', 'Sherlock', 0.85)]})
check('跨源同账号去重为 1', len(r['accounts']) == 1, str(r['stats']))
gh = r['accounts'][0]
check('双源交叉确认标记', gh['cross_source_confirmed'] is True)
check('双源 sources 集合', set(gh['sources']) == {'Maigret', 'Sherlock'})
check('双源置信增强封顶0.99', abs(gh['confidence'] - 0.99) < 1e-9, str(gh['confidence']))
check('stats cross_confirmed=1', r['stats']['cross_confirmed'] == 1)
check('duplicates 记录', len(r['duplicates']) == 1)

# 各源独有平台保留
r2 = aggregate({'Maigret': [acc('GitHub', 'https://github.com/u', 'Maigret', 0.9),
                            acc('WordPress', 'https://wp.org/u', 'Maigret', 0.9)],
                'Sherlock': [acc('Reddit', 'https://reddit.com/u', 'Sherlock')]})
check('独有平台全保留', len(r2['accounts']) == 3, str(r2['stats']))

# 单源高误报平台（Droners）丢弃
r3 = aggregate({'Sherlock': [acc('Droners', 'https://droners.io/accounts/u', 'Sherlock')]})
check('单源高误报平台丢弃', len(r3['accounts']) == 0 and r3['stats']['dropped_fp'] == 1,
      str(r3['stats']))

# 双源都命中高误报平台 → 复活
r4 = aggregate({'Maigret': [acc('droners', 'https://droners.io/accounts/u', 'Maigret', 0.9)],
                'Sherlock': [acc('Droners', 'https://droners.io/accounts/u', 'Sherlock')]})
check('跨源高误报平台复活', len(r4['accounts']) == 1
      and r4['stats']['dropped_fp'] == 0 and r4['accounts'][0]['cross_source_confirmed'],
      str(r4['stats']))

# 单源低质量降档：超大 rank 或非 2xx
r5 = aggregate({'Sherlock': [acc('LongTail', 'https://lt.example/u', 'Sherlock',
                                 conf=0.85, rank=90_000_000, http=200)]})
check('单源长尾降档', r5['accounts'][0].get('weak_single_source') is True
      and r5['accounts'][0]['confidence'] <= 0.55, str(r5['accounts'][0]))
check('weak_single 统计', r5['stats']['weak_single'] == 1)

r5b = aggregate({'Sherlock': [acc('Blocked', 'https://b.example/u', 'Sherlock',
                                  conf=0.85, rank=100, http=403)]})
check('单源非2xx降档', r5b['accounts'][0].get('weak_single_source') is True)

# 分区：tags in → IN；.cn 域名 → CN；其余 global
check('tags in → IN', _region_of({'tags': ['coding', 'in'], 'url': 'https://x.com/u'}) == 'IN')
check('.cn 域名 → CN', _region_of({'url': 'https://weibo.cn/u'}) == 'CN')
check('无标记 → global', _region_of({'url': 'https://github.com/u'}) == 'global')
r6 = aggregate({'Maigret': [acc('GitHub', 'https://github.com/u', 'Maigret', tags=['in'])],
                'Sherlock': [acc('Weibo', 'https://weibo.com/u', 'Sherlock')]})
check('by_region 统计 IN/CN',
      r6['stats']['by_region'].get('IN') == 1 and r6['stats']['by_region'].get('CN') == 1,
      str(r6['stats']['by_region']))

# 缺口标记（manual_review 末端）不参与聚合
r7 = aggregate({'manual_review': [acc('X', '', 'manual_review', gap=True)]})
check('缺口标记排除', r7['stats']['raw_total'] == 0 and r7['accounts'] == [])

# 空输入
r8 = aggregate({})
check('空输入安全', r8['accounts'] == [] and r8['stats']['raw_total'] == 0)

# 同源重复条目（同一源两条同键）→ 去重但不算交叉确认
r9 = aggregate({'Sherlock': [acc('GitHub', 'https://github.com/u', 'Sherlock'),
                             acc('GitHub', 'https://github.com/u/', 'Sherlock')]})
check('同源重复去重为1', len(r9['accounts']) == 1)
check('同源重复不算交叉', r9['accounts'][0]['cross_source_confirmed'] is False
      and r9['accounts'][0]['sources'] == ['Sherlock'])

print(f'\n=== identity_aggregator 测试: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
