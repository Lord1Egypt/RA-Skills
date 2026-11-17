#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_p0_cn_longtail_v221.py — P0 长尾中文召回增强验证

P0-1 子查询拆解并行召回：_decompose_longtail_cn 对长尾 CJK 拆解、短词/英文不拆解
P0-2 CN-AI-Web 对 CJK 自动启用：_default_layer 含 CJK → 含 CN-AI-Web；
      _search_cn_web 对 CJK 自动跑（mock _http_get，无 env flag）
P0-3 relevance 二级保底送 top-k：全候选 < floor 时返回 top-k（默认开；
      INFOSEEK_RELEVANCE_TOPK_FALLBACK=0 恢复严格空返回）
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
import net_probe  # noqa: E402


def _all_reachable(hosts, timeout=2.0, **kw):
    return {h: {'host': h, 'ok': True, 'elapsed': 0.001, 'err': ''} for h in hosts}

_P = _F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  PASS {name} {extra}')
    else:
        _F += 1
        print(f'  FAIL {name} {extra}')


print('[P0-1] 子查询拆解并行召回')
check('P0-1 纯英文不拆解',
      p._decompose_longtail_cn('Tesla 2026 revenue') == ['Tesla 2026 revenue'])
check('P0-1 短中文不拆解', p._decompose_longtail_cn('信阳板栗') == ['信阳板栗'])
_decomp = p._decompose_longtail_cn('信阳板栗2026年产量')
check('P0-1 长尾中文拆解核心子查询', '信阳板栗' in _decomp, str(_decomp))
check('P0-1 拆解首项为原 query', _decomp[0] == '信阳板栗2026年产量', str(_decomp))
check('P0-1 拆解上限 ≤3',
      len(p._decompose_longtail_cn('信阳板栗2026年产量最新排行榜前十推荐')) <= 3)


print('[P0-2] CN-AI-Web 对 CJK 自动启用')
os.environ.pop('INFOSEEK_CN_AI_SEARCH', None)
lyr_en = p._default_layer('Tesla 2026 revenue')
check('P0-2 英文 query 不含 CN-AI-Web', not any(n == 'CN-AI-Web' for n, _ in lyr_en))
lyr_cn = p._default_layer('信阳板栗2026年产量')
check('P0-2 CJK query 自动含 CN-AI-Web', any(n == 'CN-AI-Web' for n, _ in lyr_cn))
with mock.patch.object(p, '_http_get', return_value=('<title>结果页</title>').encode('utf-8')), \
     mock.patch.object(net_probe, 'check_hosts', side_effect=_all_reachable):
    res = p._search_cn_web('信阳板栗2026年产量', max_results=3)
    check('P0-2 CJK 自动调用 CN-AI-Web（无 env flag）', len(res) >= 1, f'len={len(res)}')
with mock.patch.object(p, '_http_get', side_effect=AssertionError('不应被调用')):
    res2 = p._search_cn_web('Tesla revenue 2026', max_results=3)
    check('P0-2 非 CJK 不跑 CN-AI-Web', res2 == [], f'len={len(res2)}')
os.environ['INFOSEEK_CN_AI_AUTO'] = '0'
try:
    check('P0-2 INFOSEEK_CN_AI_AUTO=0 关闭自动启用',
          not any(n == 'CN-AI-Web' for n, _ in p._default_layer('信阳板栗2026年产量')))
finally:
    os.environ.pop('INFOSEEK_CN_AI_AUTO', None)


print('[P0-3] relevance 二级保底送 top-k')
with mock.patch('anchor_adapter.compute_semantic_similarity', side_effect=lambda t, q: 5), \
     mock.patch('anchor_adapter._string_containment_similarity', return_value=0), \
     mock.patch.object(p, '_xling_mod') as xm, \
     mock.patch.object(p, '_min_expected', return_value=3):
    xm.bridge_score.return_value = 0
    # v2.5.0 起 floor/top-k 保底统一过意图槽：候选须回显意图词（产量）与核心
    # 实体词（板栗）才能进入 safety 保送；此处语义分仍 mock=5（<floor=8），
    # 故依然走「全候选<floor → 二级保底送 top-k」路径，断言目标不变。
    low = [{'url': f'https://s{i}.com',
            'title': f'信阳板栗2026年产量数据简报{i}', 'snippet': ''} for i in range(5)]
    out = p._filter_relevant([dict(x) for x in low], '信阳板栗2026年产量')
    check('P0-3 全候选<floor 且过意图槽 送 top-k', len(out) == 3, f'len={len(out)}')
os.environ['INFOSEEK_RELEVANCE_TOPK_FALLBACK'] = '0'
try:
    with mock.patch('anchor_adapter.compute_semantic_similarity', side_effect=lambda t, q: 5), \
         mock.patch('anchor_adapter._string_containment_similarity', return_value=0), \
         mock.patch.object(p, '_xling_mod') as xm, \
         mock.patch.object(p, '_min_expected', return_value=3):
        xm.bridge_score.return_value = 0
        out2 = p._filter_relevant(
            [{'url': 'https://x', 'title': 't', 'snippet': ''}], '某主题 2026')
        check('P0-3 FALLBACK=0 严格空返回', out2 == [], f'len={len(out2)}')
finally:
    os.environ.pop('INFOSEEK_RELEVANCE_TOPK_FALLBACK', None)


print(f'\n=== test_p0_cn_longtail_v221: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
