#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_three_chain.py — §8.4 三链路口径一致性勘查探针（K1-K10，只读不改码）

用途：复现 / 审计 v1.8.3 收敛前的三链路（base / 复活 / 信任加权）口径分叉。
体例沿用 ROADMAP 第八章「结构审计 + 逻辑实测 + 反事实验证」：先坐实分叉再动手。

**阅读须知**：本脚本的结论文字（如「链B 无衰减入口 → ★分叉」）是 **v1.8.3 修复前**的
历史勘查记录，用于留证根因；修复后重跑时以**打印的实测数值**为准（K3/K4/K6/K7 的
数值应显示两链一致）。判定口径是否回归请看 `tests/test_three_chain_v183.py`（63 check，
带 PASS/FAIL 断言）—— 本脚本无断言，仅作观测与取证。

实测坐实的 8 处分叉（详见 references/ROADMAP.md §8.10.1）：
  D1 链B 缺时间衰减环节（400 天源 ❌噪声 vs 🟢核心，分类翻转级）
  D2 链B 无复活标志  D3 tier 双口径（链A 产出域外非法值 0）
  D4 KB 加分单参/双参  D5 domain cap 两处硬编码  D6 trust_bonus 突破 0-30 声明
  D7 分类阈值无常量单源  D8 docstring「多 KB +4」歧义（实际合计 +12）

用法：python3 scripts/probe_three_chain.py
"""
import os
import sys
import inspect
import warnings
from pathlib import Path

ROOT = Path(os.environ.get('INFOSEEK_ROOT', str(Path(__file__).resolve().parent.parent)))
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'core'))
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
warnings.filterwarnings('ignore')

from anchor_score_v2 import (compute_base_score_v2, compute_final_score_v2,   # noqa: E402
                             compute_decay_factor_v2, compute_domain_bonus_v2)
from infoseek_core_v2 import score_source as core_v2_score                    # noqa: E402
from trust_sources import compute_trust_bonus, get_tier_level, build_pattern_index  # noqa: E402
import domain_router as dr                                                    # noqa: E402

LINE = '=' * 78


def hdr(t):
    print(f'\n{LINE}\n{t}\n{LINE}')


# 取真实信任源 pattern（避免臆造 url 导致 trust_bonus 恒 0 的假观测）
idx = build_pattern_index('tech-research')
pats = sorted(idx.items(), key=lambda kv: kv[1][0])[:3]
print('[env] tech-research tier1 patterns:', [(p, t, w) for p, (t, w) in pats])
TRUST_URL = f'https://{pats[0][0].strip(".")}.example.com/article' if pats else 'https://example.com'
PLAIN_URL = 'https://no-whitelist-xyz.example.com/a'
print('[env] TRUST_URL =', TRUST_URL,
      '| get_tier_level(tech-research) =', get_tier_level(TRUST_URL, 'tech-research'),
      '| get_tier_level(general) =', get_tier_level(TRUST_URL, 'general'))

S_HIGH = {'url': TRUST_URL, 'platform': 'arxiv', 'domain': 'tech-research',
          'interaction': 95, 'topic_match': 92, 'credibility': 96, 'llm_readability': 90,
          'title': 'AI Agent 评测基准综述', 'snippet': 'AI Agent 评测基准综述 2026',
          'text': 'AI Agent 评测基准综述'}
S_MID = dict(S_HIGH, interaction=40, topic_match=45, credibility=50, llm_readability=42)
S_BARE = {'url': TRUST_URL, 'platform': 'arxiv', 'domain': 'tech-research',
          'score': 95, 'title': 'AI Agent 评测基准', 'snippet': 'AI Agent 评测基准'}
SUBJ = 'AI Agent 评测基准'

hdr('K1 base 链路：四维 base vs 链B base_score（base_origin 标注入口差异）')
for name, s in [('高分完整四维', S_HIGH), ('中分完整四维', S_MID), ('缺三字段(score=95)', S_BARE)]:
    b_v2 = compute_base_score_v2(dict(s), SUBJ)
    a = compute_final_score_v2(dict(s), subject=SUBJ)
    b = core_v2_score(dict(s), SUBJ)
    print(f'  {name:22s} 四维base={b_v2:6.2f} | 链A base={a["base_score"]:6.2f} | '
          f'链B base={b["base_score"]:6.2f} origin={b.get("base_origin")}')
    print(f'  {"":22s} 链A final={a["after_whitelist_final"]:6.2f} 链B final={b["final_score"]:6.2f}')

hdr('K2 复活链路：标志位可观测性（数值恒 no-op）')
s99 = dict(S_HIGH, interaction=99, topic_match=99, credibility=99, llm_readability=99)
a = compute_final_score_v2(dict(s99), subject=SUBJ)
b = core_v2_score(dict(s99), SUBJ)
print(f'  链A base={a["base_score"]} whitelist={a["whitelist_triggered"]} '
      f'after_whitelist={a["after_whitelist"]} top3={a["top3_triggered"]}(DEPRECATED)')
print(f'  链B base={b["base_score"]} whitelist={b.get("whitelist_triggered")} '
      f'(v1.8.3 前该字段不存在)')
print(f'  复活数值实效 = {a["after_whitelist"] - a["base_score"]:+.2f}（恒 no-op，仅标志位有效）')

hdr('K3 时间衰减链路（D1 分类翻转级分叉 → v1.8.3 已闭合）')
print(f'  链B score_source 签名 = {list(inspect.signature(core_v2_score).parameters)}')
for d in (0, 45, 100, 200, 400):
    ra = compute_final_score_v2(dict(S_MID), subject=SUBJ, days_since_published=d)
    rb = core_v2_score(dict(S_MID), SUBJ, days_since_published=d)
    print(f'  days={d:4d} 链A={ra["after_whitelist_final"]:6.2f}({ra["classification"]}) '
          f'链B={rb["final_score"]:6.2f}({rb["classification"]}) '
          f'{"一致" if abs(ra["after_whitelist_final"] - rb["final_score"]) < 1e-9 else "★分叉"}')
print(f'  链B 默认(不传 days) decay_factor = {core_v2_score(dict(S_MID), SUBJ)["decay_factor"]}'
      f'（需 1.0 → 默认零行为变化）')

hdr('K4 tier 口径（D3 → v1.8.3 委托 get_tier_level 真源）')
for name, s in [('高分完整四维', S_HIGH), ('中分完整四维', S_MID)]:
    a = compute_final_score_v2(dict(s), subject=SUBJ)
    b = core_v2_score(dict(s), SUBJ)
    tl = get_tier_level(s['url'], s.get('domain', 'general'))
    print(f'  {name:16s} 链A tier={a["tier"]} | 链B tier={b["tier"]} | 真源={tl} '
          f'→ {"一致" if a["tier"] == b["tier"] == tl else "★分叉"}')

hdr('K5 信任加权字段归属（D6 → v1.8.3 拆分 trust_bonus_base / kb_bonus）')
kb_src = dict(S_HIGH, _kb_domain='tech-research', _kb_hit_count=3)
a = compute_final_score_v2(dict(kb_src), subject=SUBJ, with_domain=True, prefer_kb=True)
b = core_v2_score(dict(kb_src), SUBJ, prefer_kb=True)
print(f'  链A trust_bonus={a["trust_bonus"]} domain_bonus={a["domain_bonus"]}')
print(f'  链B trust_bonus={b["trust_bonus"]} = base {b.get("trust_bonus_base")} + kb {b.get("kb_bonus")}'
      f' | domain_bonus={b["domain_bonus"]}（仅报告不计入 final）')

hdr('K6 kb_intersect_bonus 单参 vs 双参（D4 → v1.8.3 链B 支持 domain_profile）')
prof_boost = {'name': 'probe', 'raw': '领域路由参数\nintersect_boost: 15\nkb_priority: true\n'}
print(f'  单参={dr.kb_intersect_bonus(dict(kb_src))} 双参(intersect_boost:15)='
      f'{dr.kb_intersect_bonus(dict(kb_src), prof_boost)}')
print(f'  链A compute_domain_bonus_v2(profile,prefer_kb) = '
      f'{compute_domain_bonus_v2(dict(kb_src), prof_boost, True, SUBJ)}')
print(f'  链B 默认={core_v2_score(dict(kb_src), SUBJ, prefer_kb=True)["kb_bonus"]} '
      f'传 profile={core_v2_score(dict(kb_src), SUBJ, prefer_kb=True, domain_profile=prof_boost)["kb_bonus"]}')

hdr('K7 domain bonus cap（D5 → v1.8.3 domain_bonus_cap() 单源动态读 env）')
from anchor_adapter import _compute_domain_bonus                             # noqa: E402
from domain_router import apply_profile_to_score, domain_bonus_cap           # noqa: E402
PROF = {'name': 't', 'raw': '| 来源 | Tier |\n| Baosteel | Tier 1 |'}
s3 = {'url': 'https://baosteel.com/x', 'platform': 'web', '_kb_domain': 'steel', '_kb_hit_count': 2}
_old = os.environ.get('INFOSEEK_DOMAIN_BONUS_CAP')
try:
    for cap in ('5', '20'):
        os.environ['INFOSEEK_DOMAIN_BONUS_CAP'] = cap
        v = [apply_profile_to_score(dict(s3), PROF, prefer_kb=True)['domain_bonus'],
             compute_domain_bonus_v2(dict(s3), PROF, True),
             _compute_domain_bonus(dict(s3), PROF, True)]
        print(f'  env cap={cap:2s} → 三方 domain_bonus={v} 同值={len(set(v)) == 1} '
              f'domain_bonus_cap()={domain_bonus_cap()}')
finally:
    if _old is None:
        os.environ.pop('INFOSEEK_DOMAIN_BONUS_CAP', None)
    else:
        os.environ['INFOSEEK_DOMAIN_BONUS_CAP'] = _old

hdr('K8 分类阈值一致性（正例）')
for th in (100, 70, 69.9, 40, 39.9, 0):
    cls = '🟢核心' if th >= 70 else ('🟡潜力' if th >= 40 else '❌噪声')
    print(f'  score={th:6.1f} → {cls}（阈值 70/40 常量单源 CLASSIFY_CORE/CLASSIFY_POTENTIAL）')

hdr('K9 文档口径核对（D8）')
print('  kb_intersect_bonus docstring 首行:', dr.kb_intersect_bonus.__doc__.split('\n')[0].strip())
print(f'  常量 _KB_INTERSECT_BONUS={dr._KB_INTERSECT_BONUS} _KB_MULTI_BONUS={dr._KB_MULTI_BONUS} '
      f'→ 多 KB 实际合计 = {dr._KB_INTERSECT_BONUS + dr._KB_MULTI_BONUS}')

hdr('K10 两链聚合公式对照（v1.8.3 后：同源委托 aggregate_score_v2）')
print('  唯一聚合真源 = core/anchor_score_v2.aggregate_score_v2')
print('  链A: 维度取值(四维 base/跨平台/语义/trust/domain) → 委托聚合')
print('  链B: base 三态入口(v1_score/four_dim/semantic_fallback) + trust/KB 取值 → 委托聚合')
print(f'  链B domain_bonus 来源 = source["_scoring"]["domain_bonus"] 旁路 → 实测='
      f'{core_v2_score(dict(S_HIGH, _scoring={"domain_bonus": 12}), SUBJ)["domain_bonus"]}'
      f'（仅报告不计入 final，防双重计分）')
print('\n[done] 判定口径是否回归请跑 tests/test_three_chain_v183.py（63 check 带断言）')
