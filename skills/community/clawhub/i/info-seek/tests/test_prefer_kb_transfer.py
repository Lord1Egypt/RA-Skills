#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_prefer_kb_transfer.py — v1.7.2 C：prefer_kb 跨模块透传

覆盖：
  T1 信号产出（detect_domain.prefer_kb）
  T2 单源 kb_intersect_bonus（8/12/0）
  T3 G2 三份实现收敛一致
  T4 透传链（compute_final_score_v2 prefer_kb → domain_bonus）
  T5 G12 subject 注入（subject 参数 == source['subject']）
  T6/T7 kb_merge 交集优先（默认 +5 / prefer_kb +8/+12）+ 非交集零变化 parity
  T8 score_source 透传（trust_bonus 提升）
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'core'))

# 隔离：禁用平台 WebSearch（防 WorkBuddy sidecar 自动 spawn 污染）
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')

from domain_router import (  # noqa: E402
    apply_profile_to_score, detect_domain, kb_intersect_bonus, trust_source_bonus,
)
from anchor_adapter import calculate_score, _compute_domain_bonus  # noqa: E402
from anchor_score_v2 import compute_domain_bonus_v2, compute_final_score_v2  # noqa: E402
from infoseek_core_v2 import score_source  # noqa: E402
from trusted_kb import kb_merge  # noqa: E402

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
PROF = {'name': 't', 'raw': '| 来源 | Tier |\n| Baosteel | Tier 1 |'}

print('[T1] 信号产出')
r = detect_domain(MULTI)
check('T1 交集场景 prefer_kb=True', r['is_intersect'] is True and r['prefer_kb'] is True, str(r['intersect_domains']))
check('T1 非交集 prefer_kb=False', detect_domain(SINGLE)['prefer_kb'] is False)

print('[T2] 单源 kb_intersect_bonus')
check('T2 单 KB +8', kb_intersect_bonus({'_kb_domain': 'x', '_kb_hit_count': 1}) == 8)
check('T2 多 KB +12', kb_intersect_bonus({'_kb_domain': 'x', '_kb_hit_count': 2}) == 12)
check('T2 无 KB 0', kb_intersect_bonus({}) == 0)

print('[T3] G2 三份实现收敛一致')
s3 = {'url': 'https://baosteel.com/x', 'platform': 'web', '_kb_domain': 'steel', '_kb_hit_count': 2}
v = [apply_profile_to_score(dict(s3), PROF, prefer_kb=True)['domain_bonus'],
     compute_domain_bonus_v2(dict(s3), PROF, prefer_kb=True),
     _compute_domain_bonus(dict(s3), PROF, True)]
check('T3 三方同值(5+12=17)', len(set(v)) == 1 and v[0] == 17, str(v))

print('[T4] 透传链 compute_final_score_v2')
s4 = {'url': 'https://x.com', 'platform': 'web', '_kb_domain': 't', '_kb_hit_count': 2}
r_off = compute_final_score_v2(dict(s4), 'x', with_domain=True, domain_profile=PROF, prefer_kb=False)
r_on = compute_final_score_v2(dict(s4), 'x', with_domain=True, domain_profile=PROF, prefer_kb=True)
check('T4 prefer_kb 令 domain_bonus +12', r_on['domain_bonus'] == r_off['domain_bonus'] + 12,
      f"{r_off['domain_bonus']}->{r_on['domain_bonus']}")

print('[T5] G12 subject 注入')
a5 = compute_domain_bonus_v2({'url': 'https://x.com', 'subject': SINGLE}, None, False)
b5 = compute_domain_bonus_v2({'url': 'https://x.com'}, None, False, SINGLE)
check('T5 subject 参数 == source[subject]', a5 == b5, str((a5, b5)))

print('[T6/T7] kb_merge 交集优先 + 非交集 parity')
web = [{'entry': 'https://a.com', 'score': 70}]
kb1 = {'entry': 'https://kb1.com', '_credibility_base': 80, '_kb_domain': 't', '_kb_hit_count': 1}
kb2 = {'entry': 'https://kb2.com', '_credibility_base': 80, '_kb_domain': 't', '_kb_hit_count': 2}
check('T6 默认 KB +5 (parity=85)', [x['score'] for x in kb_merge([dict(w) for w in web], [dict(kb1)])] == [70, 85])
check('T6 prefer_kb 单 KB +8', [x['score'] for x in kb_merge([dict(w) for w in web], [dict(kb1)], prefer_kb=True)] == [70, 88])
check('T6 prefer_kb 多 KB +12', [x['score'] for x in kb_merge([dict(w) for w in web], [dict(kb2)], prefer_kb=True)] == [70, 92])
check('T7 非交集(prefer_kb=False) 与默认一致',
      [x['score'] for x in kb_merge([dict(w) for w in web], [dict(kb1)], prefer_kb=False)]
      == [x['score'] for x in kb_merge([dict(w) for w in web], [dict(kb1)])])

print('[T8] score_source 透传')
s8 = {'url': 'https://x.com', 'platform': 'web', '_kb_domain': 't', '_kb_hit_count': 2}
try:
    off = score_source(dict(s8), 'x', prefer_kb=False)
    on = score_source(dict(s8), 'x', prefer_kb=True)
    check('T8 trust_bonus 提升 12', on['trust_bonus'] == off['trust_bonus'] + 12,
          f"{off['trust_bonus']}->{on['trust_bonus']}")
except Exception as e:  # noqa: BLE001
    check('T8 score_source 透传', False, repr(e)[:80])

print('[T9] calculate_score 生效版透传（不报错 + prefer_kb 字段语义）')
try:
    res = calculate_score(dict(s4), MULTI, with_llm_readability=True, with_domain=True, prefer_kb=True)
    check('T9 calculate_score 返回 domain_bonus', 'domain_bonus' in res, str(res.get('domain_bonus')))
except Exception as e:  # noqa: BLE001
    check('T9 calculate_score 透传', False, repr(e)[:80])

print('[T10-T12] run_pipeline / execute_anchor 全链贯穿')
import infoseek_pipeline as _ip  # noqa: E402
import tempfile  # noqa: E402

_a = [{'name': MULTI, 'platform': 'web', 'score': 70, 'entry': 'https://a.com', 'entry_type': 'URL'}]
_rep = _ip.run_pipeline(_a, tempfile.mkdtemp(prefix='pk_'), min_anchors=99)
check('T10 report.prefer_kb=True', _rep.get('prefer_kb') is True)
check('T11 anchor 注入 _prefer_kb', _a[0].get('_prefer_kb') is True)
_rep2 = _ip.run_pipeline(
    [{'name': SINGLE, 'platform': 'web', 'score': 70, 'entry': 'https://b.com', 'entry_type': 'URL'}],
    tempfile.mkdtemp(prefix='pk_'), min_anchors=99)
check('T10 非交集 report.prefer_kb=False', _rep2.get('prefer_kb') is False)
_r = _ip.execute_anchor(
    {'name': 'x', 'platform': 'web', 'score': 10, 'entry': 'https://a.com',
     'entry_type': 'URL', '_prefer_kb': True}, tempfile.mkdtemp(prefix='pk_'))
check('T12 execute_anchor 传播 prefer_kb', _r.get('prefer_kb') is True and _r['status'] == 'skipped',
      str(_r.get('status')))

print('[T13-T14] core_v2 评分入口透传')
import infoseek_core_v2 as _c2  # noqa: E402
import inspect as _inspect  # noqa: E402

_pk_fns = ['score_source', 'render_report', 'research', 'async_research',
           'streaming_research', 'score_sources_batch_async']
_missing = [f for f in _pk_fns
            if 'prefer_kb' not in _inspect.signature(getattr(_c2, f)).parameters]
check('T13 六入口签名含 prefer_kb', not _missing, str(_missing))

_s13 = [{'url': 'https://x.com', 'platform': 'web', '_kb_domain': 't',
         '_kb_hit_count': 2, 'title': 't', 'snippet': 's'}]
_rr = _c2.render_report(MULTI, [dict(x) for x in _s13], format='md', prefer_kb=True)
check('T14 render_report 透传不报错', isinstance(_rr, str) and len(_rr) > 0)
_off = _c2.score_source(dict(_s13[0]), MULTI, prefer_kb=False)
_on = _c2.score_source(dict(_s13[0]), MULTI, prefer_kb=True)
check('T14 score_source prefer_kb +12', _on['trust_bonus'] == _off['trust_bonus'] + 12,
      f"{_off['trust_bonus']}->{_on['trust_bonus']}")

print(f'\n=== test_prefer_kb_transfer: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
