#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_three_chain_v183.py — §8.4 三链路口径一致性守护（base / 复活 / 信任加权）

背景（ROADMAP §8.4 验收总闸第二条）：v1.7.8 的 test_score_consistency_v178 仅覆盖
「base 链路」（calculate_score ≡ compute_final_score_v2），**复活与信任加权零覆盖**。
本套件补齐三链路，并把 v1.8.3 收敛成果固化为守护断言。

v1.8.3 前的实测分叉（8 处，probe_three_chain.py 坐实）：
  D1 链B 自算 min(base+trust,100)，缺时间衰减环节 → 400 天陈旧源
     链A 38.7(❌噪声) vs 链B 70.7(🟢核心)，**分类翻转级**
  D2 链B 无复活标志（whitelist_triggered 不可观测）
  D3 tier 双口径：链A compute_trust_bonus(...,'general')//10 → 产出**域外非法值 0**；
     链B get_tier_level(url, domain) → 1
  D4 KB 交集加分：链A 走双参（profile intersect_boost 生效），链B 恒单参 → 声明化半失效
  D5 domain bonus cap：domain_router 用 env 可配 _DOMAIN_BONUS_CAP，
     链A compute_domain_bonus_v2 / anchor_adapter._compute_domain_bonus 各自硬编码 20
  D6 trust_bonus 字段语义：链B 混入 KB 加分（37）突破 docstring 声明的 0-30
  D7 分类阈值 70/40 两处各自硬编码（无常量单源）
  D8 文档口径：kb_intersect_bonus docstring「多 KB +4」歧义（实际合计 +12）

覆盖：
  T1 聚合真源单点性（结构守护）      T2 三链路数值恒等（90 组网格对拍）
  T3 复活链路口径                     T4 时间衰减链路口径
  T5 信任加权链路口径（含 cap 单源）  T6 分类阈值单源
  T7 base_origin 可观测               T8 文档口径一致
  T9 零回归契约守护
"""
import os
import sys
import inspect
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'core'))

# 隔离：禁用平台 WebSearch（防 sidecar 自动 spawn 污染）
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')
warnings.filterwarnings('ignore')

import anchor_score_v2 as ASV2                      # noqa: E402
from anchor_score_v2 import (aggregate_score_v2, compute_final_score_v2,   # noqa: E402
                             compute_base_score_v2, compute_domain_bonus_v2,
                             resolve_tier_v2)
import infoseek_core_v2 as C2                        # noqa: E402
from infoseek_core_v2 import score_source            # noqa: E402
import domain_router as DR                           # noqa: E402
from domain_router import (trust_source_bonus, kb_intersect_bonus,          # noqa: E402
                           apply_profile_to_score, domain_bonus_cap)
import anchor_adapter as AA                          # noqa: E402
from anchor_adapter import _compute_domain_bonus     # noqa: E402
from trust_sources import (compute_trust_bonus, get_tier_level,             # noqa: E402
                           build_pattern_index)

_P = _F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  PASS {name} {extra}')
    else:
        _F += 1
        print(f'  FAIL {name} {extra}')


# ── 真实信任源（避免臆造 url 导致 trust_bonus 恒 0 的假通过）──
_IDX = build_pattern_index('tech-research')
_PATS = sorted(_IDX.items(), key=lambda kv: kv[1][0])
assert _PATS, 'trusted-sources.json 无 tech-research 白名单，测试前提不成立'
TRUST_URL = f'https://{_PATS[0][0].strip(".")}.example.com/a'
PLAIN_URL = 'https://no-whitelist-xyz.example.com/a'
SUBJ = 'AI Agent 评测基准'
TRUST_BONUS = compute_trust_bonus(TRUST_URL, 'tech-research', 'arxiv')
assert TRUST_BONUS > 0, f'信任源未命中（bonus={TRUST_BONUS}），测试前提不成立'

# 四维全等 X → base == X（链A 精确构造 base 的手法）
def src_a(base, url=TRUST_URL):
    return {'url': url, 'platform': 'arxiv', 'domain': 'tech-research',
            'interaction': base, 'topic_match': base, 'credibility': base,
            'llm_readability': base, 'title': SUBJ, 'snippet': SUBJ}


def src_b(base, url=TRUST_URL):
    """链B 走 v1_score 入口 → base_score 精确等于 base（base_origin='v1_score'）

    注：**不带 title/snippet** —— 链B 对 `score <= 0` 的源会走语义兜底重算 base
    （v1.0.1 P0-1 既有设计），带文本会使 base=0 组无法与链A 对拍（T2 目的是验聚合，
    非验 base 入口；base 入口差异由 T7 base_origin 单独覆盖）。
    """
    return {'url': url, 'platform': 'arxiv', 'domain': 'tech-research', 'score': base}


# ═══════════════════════════════════════════════════════════════
print('[T1] 聚合真源单点性（结构守护）')
# ═══════════════════════════════════════════════════════════════
_src_a_fn = inspect.getsource(compute_final_score_v2)
_src_b_fn = inspect.getsource(score_source)
check('T1-1 aggregate_score_v2 存在且可调用', callable(aggregate_score_v2))
check('T1-2 链A 委托聚合真源', 'aggregate_score_v2(' in _src_a_fn)
check('T1-3 链B 委托聚合真源', 'aggregate_score_v2(' in _src_b_fn)
# 自算公式仅允许出现在链B 的降级保底分支（1 次），不得作为主路径
_selfcalc = _src_b_fn.count('min(base_score + trust_bonus, 100)')
check('T1-4 链B 自算公式仅存于降级分支（==1）', _selfcalc == 1, f'count={_selfcalc}')
check('T1-5 链B 降级分支带可观测标记 _aggregate_degraded',
      '_aggregate_degraded' in _src_b_fn)
check('T1-6 链A 无残留自算聚合（分类阈值不再硬编码）',
      "classification = '🟢核心'" not in _src_a_fn)
check('T1-7 聚合常量单源存在',
      hasattr(ASV2, 'RESURRECTION_THRESHOLD') and hasattr(ASV2, 'CLASSIFY_CORE')
      and hasattr(ASV2, 'CLASSIFY_POTENTIAL'),
      f"{ASV2.RESURRECTION_THRESHOLD}/{ASV2.CLASSIFY_CORE}/{ASV2.CLASSIFY_POTENTIAL}")

# ═══════════════════════════════════════════════════════════════
print('[T2] 三链路数值恒等（base × days × trust 网格对拍）')
# ═══════════════════════════════════════════════════════════════
BASES = [0, 27.15, 39.95, 40, 45.7, 69.95, 70, 90, 100]
DAYS = [0, 45, 100, 200, 400]
_mis = []
for base in BASES:
    for d in DAYS:
        for url, tag in ((TRUST_URL, 'trust'), (PLAIN_URL, 'plain')):
            ra = compute_final_score_v2(src_a(base, url), subject=SUBJ,
                                        days_since_published=d)
            rb = score_source(src_b(base, url), SUBJ, days_since_published=d)
            if abs(ra['after_whitelist_final'] - rb['final_score']) > 1e-9:
                _mis.append((base, d, tag, ra['after_whitelist_final'], rb['final_score']))
            if ra['classification'] != rb['classification']:
                _mis.append((base, d, tag, ra['classification'], rb['classification']))
check(f'T2-1 {len(BASES)*len(DAYS)*2} 组网格 final+classification 全恒等',
      not _mis, f'分叉={_mis[:4]}' if _mis else f'(base{BASES[0]}..{BASES[-1]} × days{DAYS})')
# 边界带专项：分类翻转风险区（±0.05 round 收敛代价）
_edge = [(39.95, 0), (69.95, 0), (40, 0), (70, 0)]
_ok = all(compute_final_score_v2(src_a(b), subject=SUBJ, days_since_published=d)['classification']
          == score_source(src_b(b), SUBJ, days_since_published=d)['classification']
          for b, d in _edge)
check('T2-2 分类边界带（39.95/40/69.95/70）两链同判', _ok)
# 聚合函数直调 vs 两链（三方同源）
_ag = aggregate_score_v2(45.7, days_since_published=200, trust_bonus=TRUST_BONUS)
_rb = score_source(src_b(45.7), SUBJ, days_since_published=200)
check('T2-3 链B final == 聚合真源直调', abs(_ag['final_score'] - _rb['final_score']) < 1e-9,
      f"{_ag['final_score']} vs {_rb['final_score']}")

# ═══════════════════════════════════════════════════════════════
print('[T3] 复活链路口径（标志位同源 + no-op 事实固化）')
# ═══════════════════════════════════════════════════════════════
for base, exp in [(89.9, False), (90.0, True), (95.0, True), (100.0, True), (0, False)]:
    ra = compute_final_score_v2(src_a(base), subject=SUBJ)
    rb = score_source(src_b(base), SUBJ)
    check(f'T3-1 base={base} whitelist_triggered 两链同值={exp}',
          ra['whitelist_triggered'] == rb['whitelist_triggered'] == exp,
          f"A={ra['whitelist_triggered']} B={rb['whitelist_triggered']}")
_noop = all(abs(compute_final_score_v2(src_a(b), subject=SUBJ)['after_whitelist'] - b) < 1e-9
            for b in [0, 45.7, 89.9, 90, 95, 100])
check('T3-2 简化复活数值 no-op（after_whitelist == base，仅标志位有效）', _noop)
check('T3-3 top3_triggered 恒 False（v1 双层复活 DEPRECATED）',
      compute_final_score_v2(src_a(95), subject=SUBJ)['top3_triggered'] is False
      and aggregate_score_v2(95)['top3_triggered'] is False)
check('T3-4 复活门槛常量 == 90 / 保底 == 70',
      ASV2.RESURRECTION_THRESHOLD == 90 and ASV2.RESURRECTION_FLOOR == 70)
check('T3-5 聚合直调复活标志', aggregate_score_v2(90)['whitelist_triggered'] is True
      and aggregate_score_v2(89.99)['whitelist_triggered'] is False)

# ═══════════════════════════════════════════════════════════════
print('[T4] 时间衰减链路口径（D1 分类翻转级分叉已闭合）')
# ═══════════════════════════════════════════════════════════════
_a400 = compute_final_score_v2(src_a(45.7), subject=SUBJ, days_since_published=400)
_b400 = score_source(src_b(45.7), SUBJ, days_since_published=400)
check('T4-1 400 天陈旧源两链同分', abs(_a400['after_whitelist_final'] - _b400['final_score']) < 1e-9,
      f"A={_a400['after_whitelist_final']} B={_b400['final_score']}")
check('T4-2 400 天陈旧源两链同分类（原链B 误判🟢核心）',
      _a400['classification'] == _b400['classification'] == '❌噪声',
      f"A={_a400['classification']} B={_b400['classification']}")
check('T4-3 decay_factor 两链一致', _b400['decay_factor'] == 0.3
      and _b400['after_decay'] == _a400['after_decay'], f"{_b400['after_decay']}")
check('T4-4 链B 默认零行为变化（不传 days → decay=1.0）',
      score_source(src_b(45.7), SUBJ)['decay_factor'] == 1.0)
check('T4-5 链B 自动读 source[days_since_published]',
      score_source(dict(src_b(45.7), days_since_published=400), SUBJ)['final_score']
      == _b400['final_score'])
check('T4-6 衰减因子分档口径（<30/<90/<180/<365/else）',
      [ASV2.compute_decay_factor_v2(d) for d in (0, 45, 100, 200, 400)]
      == [1.0, 0.9, 0.7, 0.5, 0.3])

# ═══════════════════════════════════════════════════════════════
print('[T5] 信任加权链路口径（D3/D4/D5/D6 闭合）')
# ═══════════════════════════════════════════════════════════════
_ra = compute_final_score_v2(src_a(45.7), subject=SUBJ)
_rb = score_source(src_b(45.7), SUBJ)
check('T5-1 纯信任源加权两链同源（链A trust_bonus == 链B trust_bonus_base）',
      _ra['trust_bonus'] == _rb['trust_bonus_base'] == TRUST_BONUS,
      f"A={_ra['trust_bonus']} B_base={_rb['trust_bonus_base']} 真源={TRUST_BONUS}")
check('T5-2 链B trust_bonus == trust_bonus_base + kb_bonus（拆分可对账）',
      _rb['trust_bonus'] == _rb['trust_bonus_base'] + _rb['kb_bonus'])
check('T5-3 trust_bonus_base 未破 0-30 上限（D6 语义澄清）',
      0 <= _rb['trust_bonus_base'] <= 30 and 0 <= compute_trust_bonus(TRUST_URL, 'tech-research', 'arxiv') <= 30)
# tier 单源（D3）
check('T5-4 tier 两链一致且 == get_tier_level 真源',
      _ra['tier'] == _rb['tier'] == get_tier_level(TRUST_URL, 'tech-research'),
      f"A={_ra['tier']} B={_rb['tier']} 真源={get_tier_level(TRUST_URL, 'tech-research')}")
check('T5-5 tier 恒 ∈ 1..4（域外非法值 0 已消除）',
      all(compute_final_score_v2(src_a(b, u), subject=SUBJ)['tier'] in (1, 2, 3, 4)
          for b in (0, 45.7, 95) for u in (TRUST_URL, PLAIN_URL, '')))
check('T5-6 resolve_tier_v2 委托真源（异常回落 4）',
      resolve_tier_v2(TRUST_URL, 'tech-research') == get_tier_level(TRUST_URL, 'tech-research')
      and resolve_tier_v2('', '') == 4)
# KB 加分同源（D4）
_kbsrc = {'url': PLAIN_URL, 'platform': 'web', '_kb_domain': 't', '_kb_hit_count': 2}
_PROF15 = {'name': 'p', 'raw': 'intersect_boost: 15'}
check('T5-7 KB 加分单源（链B kb_bonus == domain_router.kb_intersect_bonus）',
      score_source(dict(_kbsrc), 'x', prefer_kb=True)['kb_bonus']
      == kb_intersect_bonus(dict(_kbsrc)) == 12)
check('T5-8 链B 双参口径可用（profile intersect_boost=15 → 19）',
      score_source(dict(_kbsrc), 'x', prefer_kb=True, domain_profile=_PROF15)['kb_bonus'] == 19)
check('T5-9 链A/链B KB 加分同源同值（prefer_kb 场景）',
      compute_domain_bonus_v2(dict(_kbsrc), _PROF15, True) - compute_domain_bonus_v2(dict(_kbsrc), _PROF15, False)
      == score_source(dict(_kbsrc), 'x', prefer_kb=True, domain_profile=_PROF15)['kb_bonus']
      - score_source(dict(_kbsrc), 'x', prefer_kb=False)['kb_bonus'])
check('T5-10 kb_intersect_bonus 分段（单 KB 8 / 多 KB 12 / 无 KB 0）',
      (kb_intersect_bonus({'_kb_domain': 'x', '_kb_hit_count': 1}),
       kb_intersect_bonus({'_kb_domain': 'x', '_kb_hit_count': 2}),
       kb_intersect_bonus({})) == (8, 12, 0))
# cap 单源（D5）
_PROF = {'name': 't', 'raw': '| 来源 | Tier |\n| Baosteel | Tier 1 |'}
# platform='web'（不含信任源词）→ url 命中 +5，多 KB +12 → 17，与 test_prefer_kb_transfer T3 同基准
_s3 = {'url': 'https://baosteel.com/x', 'platform': 'web', '_kb_domain': 'steel', '_kb_hit_count': 2}


def _three_way():
    return [apply_profile_to_score(dict(_s3), _PROF, prefer_kb=True)['domain_bonus'],
            compute_domain_bonus_v2(dict(_s3), _PROF, True),
            _compute_domain_bonus(dict(_s3), _PROF, True)]


_old_cap = os.environ.get('INFOSEEK_DOMAIN_BONUS_CAP')
try:
    os.environ['INFOSEEK_DOMAIN_BONUS_CAP'] = '5'
    _v5 = _three_way()
    check('T5-11 cap env=5 → 三方同值且跟随（D5 硬编码已除）',
          len(set(_v5)) == 1 and _v5[0] == 5, str(_v5))
    check('T5-12 domain_bonus_cap() 动态读 env', domain_bonus_cap() == 5)
finally:
    if _old_cap is None:
        os.environ.pop('INFOSEEK_DOMAIN_BONUS_CAP', None)
    else:
        os.environ['INFOSEEK_DOMAIN_BONUS_CAP'] = _old_cap
_v20 = _three_way()
check('T5-13 cap 恢复默认 20 → 三方同值(5+12=17)', len(set(_v20)) == 1 and _v20[0] == 17, str(_v20))

# ═══════════════════════════════════════════════════════════════
print('[T6] 分类阈值单源（D7）')
# ═══════════════════════════════════════════════════════════════
for sc, exp in [(100, '🟢核心'), (70, '🟢核心'), (69.9, '🟡潜力'), (40, '🟡潜力'), (39.9, '❌噪声'), (0, '❌噪声')]:
    _c = aggregate_score_v2(sc, trust_bonus=0)['classification']
    check(f'T6-1 score={sc} → {exp}', _c == exp, f'实得 {_c}')
_src_agg = inspect.getsource(aggregate_score_v2)
check('T6-2 聚合使用常量而非字面量', 'CLASSIFY_CORE' in _src_agg and 'CLASSIFY_POTENTIAL' in _src_agg)
check('T6-3 链B 无自算分类阈值（委托聚合）',
      _src_b_fn.count("classification = '🟢核心'") <= 1)  # 仅降级分支

# ═══════════════════════════════════════════════════════════════
print('[T7] base_origin 可观测（入口差异显式化，非隐性分叉）')
# ═══════════════════════════════════════════════════════════════
check('T7-1 four_dim（含四维字段）',
      score_source(src_a(45.7), SUBJ)['base_origin'] == 'four_dim')
check('T7-2 v1_score（仅 score）', score_source(src_b(45.7), SUBJ)['base_origin'] == 'v1_score')
check('T7-3 semantic_fallback（仅文本）',
      score_source({'title': SUBJ, 'snippet': SUBJ, 'url': PLAIN_URL}, SUBJ)['base_origin']
      == 'semantic_fallback')
check('T7-4 empty（全空）', score_source({}, SUBJ)['base_origin'] == 'empty')
check('T7-5 four_dim 入口 base == 链A 四维 base（同口径）',
      abs(score_source(src_a(45.7), SUBJ)['base_score'] - compute_base_score_v2(src_a(45.7), SUBJ)) < 1e-9)

# ═══════════════════════════════════════════════════════════════
print('[T8] 文档口径一致（D8 勘误落地）')
# ═══════════════════════════════════════════════════════════════
check('T8-1 kb_intersect_bonus docstring 标注「合计 +12」', '合计 +12' in kb_intersect_bonus.__doc__)
check('T8-2 score_source docstring 声明 trust_bonus 0-42 及拆分',
      '0-42' in score_source.__doc__ and 'trust_bonus_base' in score_source.__doc__)
check('T8-3 score_source docstring 声明聚合委托 + 职责边界',
      'aggregate_score_v2' in score_source.__doc__ and '职责边界' in score_source.__doc__)
check('T8-4 aggregate_score_v2 docstring 记录复活 no-op 口径事实',
      'no-op' in aggregate_score_v2.__doc__)
_tk = (os.path.join(ROOT, 'scripts', 'trusted_kb.py'))
with open(_tk, encoding='utf-8') as f:
    _tks = f.read()
check('T8-5 trusted_kb 注释口径对齐（合计 +12）', '合计 +12' in _tks)
check('T8-6 domain_bonus_cap docstring 记录三处硬编码根因', 'min(bonus, 20)' in domain_bonus_cap.__doc__)

# ═══════════════════════════════════════════════════════════════
print('[T9] 零回归契约守护')
# ═══════════════════════════════════════════════════════════════
check('T9-1 空源 final_score == 0（test_deep_v101 B2 契约）',
      score_source({}, '主题')['final_score'] == 0)
check('T9-2 返回 schema 兼容（既有字段全在）',
      all(k in score_source(src_b(45.7), SUBJ) for k in
          ('final_score', 'base_score', 'tier', 'trust_bonus', 'domain_bonus',
           'classification', 'version')))
check('T9-3 algo-v 保持 1.2.0（下游契约不随 skill 版本变动）',
      score_source(src_b(45.7), SUBJ)['version'] == '1.2.0')
_off = score_source(dict(_kbsrc), 'x', prefer_kb=False)
_on = score_source(dict(_kbsrc), 'x', prefer_kb=True)
check('T9-4 prefer_kb trust_bonus +12（test_prefer_kb_transfer T8/T14 契约）',
      _on['trust_bonus'] == _off['trust_bonus'] + 12, f"{_off['trust_bonus']}->{_on['trust_bonus']}")
check('T9-5 纯函数不改输入（链A）',
      (lambda s: (compute_final_score_v2(s, subject=SUBJ), s == src_a(45.7))[1])(src_a(45.7)))
check('T9-6 链B 不注入聚合降级标记（常态路径）',
      '_aggregate_degraded' not in score_source(src_b(45.7), SUBJ))

# ═══════════════════════════════════════════════════════════════
print('[T10] 聚合入口有限性 / 下界夹取（G4/G5 边界硬化）')
# ═══════════════════════════════════════════════════════════════
_r_nan = aggregate_score_v2(float('nan'))
check('T10-1 NaN → final=0 且 score_invalid',
      _r_nan['final_score'] == 0 and _r_nan['score_invalid'] is True,
      f"final={_r_nan['final_score']} invalid={_r_nan['score_invalid']}")
_r_none = aggregate_score_v2(None)
check('T10-2 None → final=0（不 CRASH）',
      _r_none['final_score'] == 0 and _r_none['score_invalid'] is True,
      f"final={_r_none['final_score']}")
_r_neg = aggregate_score_v2(-5)
check('T10-3 负值夹取下界 0', _r_neg['final_score'] == 0, f"final={_r_neg['final_score']}")
check('T10-4 正常值不回归', aggregate_score_v2(50)['final_score'] == 50
      and aggregate_score_v2(50)['score_invalid'] is False)

print(f'\n=== test_three_chain_v183: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
