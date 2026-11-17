#!/usr/bin/env python3
"""test_domain_bonus_no_double_count.py — domain_bonus 收口守护（v2.3.2 更新）

锁定三链路口径一致性（§8.4），v2.3.2 起链B 完成收口：
- 链A/链B 统一经聚合真源 aggregate_score_v2 计入 domain_bonus；
- 链B domain_bonus = 纯领域特定信任段 domain_router.trust_source_bonus，
  source['_scoring'].domain_bonus 旁路值不再采信（防旁路口径分叉）；
- KB 交集段仍在 trust_bonus，不进入 domain_bonus，故无双重计分；
- 信任源提取器 _extract_trust_sources 能从 profile 表格数据行抽取实体
  （v2.3.2 修复：旧实现只命中表头，领域段长期为 0）。
纯 import，无网络、无副作用。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT / 'scripts'))

_fails = []


def check(name, cond, detail=''):
    if cond:
        print(f'  [PASS] {name}')
    else:
        _fails.append(name)
        print(f'  [FAIL] {name} {detail}')


def main():
    from anchor_score_v2 import aggregate_score_v2, compute_final_score_v2  # noqa: E402
    from infoseek_core_v2 import score_source  # noqa: E402
    import domain_router as dr  # noqa: E402

    print('--- 链A 聚合真源 domain_bonus 计入 final ---')
    r_agg = aggregate_score_v2(40, trust_bonus=10, domain_bonus=20)
    check('链A 聚合计入 domain_bonus', r_agg['final_score'] == 70, str(r_agg))

    print('--- 链B 收口：_scoring 旁路不再采信 ---')
    # 旧口径：_scoring.domain_bonus=12 被回显；新口径：不采信，普通 url 无 profile 命中 → 0
    src = {'score': 40, 'url': 'https://example.com/x', 'title': 't', 'snippet': 's',
           '_scoring': {'domain_bonus': 12}}
    rb = score_source(src, '某普通主题', prefer_kb=False)
    exp_b = aggregate_score_v2(rb['base_score'], trust_bonus=rb['trust_bonus'],
                               domain_bonus=rb['domain_bonus'])['final_score']
    check('链B 旁路 _scoring.domain_bonus=12 不采信（=0）',
          rb['domain_bonus'] == 0, f"domain={rb.get('domain_bonus')}")
    check('链B final 经聚合真源（含 domain_bonus）', rb['final_score'] == exp_b,
          f"final={rb['final_score']} exp={exp_b}")
    check('链B 报告 domain_bonus 字段', 'domain_bonus' in rb)

    print('--- 链B 领域命中：信任源真实计入 final ---')
    srcf = {'url': 'https://www.wind.com.cn/n',
            'interaction_score': 60, 'citation': 60, 'credibility': 60,
            'topic_match': 60, 'llm_readability': 60}
    rf = score_source(srcf, '宁德时代 估值', prefer_kb=False)
    exp_f = aggregate_score_v2(rf['base_score'], trust_bonus=rf['trust_bonus'],
                               domain_bonus=rf['domain_bonus'])['final_score']
    check('finance + Wind URL → domain_bonus=5', rf['domain_bonus'] == 5,
          f"domain_bonus={rf['domain_bonus']}")
    check('领域段计入 final', abs(rf['final_score'] - exp_f) < 1e-9)

    print('--- 信任源提取器从表格数据行抽取实体（v2.3.2 修复）---')
    prof = dr.load_profile('finance-research')
    kws = set(dr._extract_trust_sources(prof['raw']))
    check('抽取到 Wind/SEC/证监会', {'Wind', 'SEC', '证监会'} <= kws, str(sorted(kws)))
    check('噪声词不混入（监管/权重/类型）',
          not ({'监管', '权重', '类型', '信任源白名单'} & kws))

    print('--- KB 段在 trust_bonus，不进 domain_bonus（无双重计分）---')
    src4 = {'url': 'https://www.wind.com.cn/kb', '_kb_domain': 'finance-research',
            '_kb_hit_count': 1,
            'interaction_score': 60, 'citation': 60, 'credibility': 60,
            'topic_match': 60, 'llm_readability': 60}
    r4 = score_source(src4, '宁德时代 估值', domain_profile=prof, prefer_kb=True)
    check('KB 段计入 kb_bonus', r4['kb_bonus'] > 0, f"kb={r4['kb_bonus']}")
    check('trust_bonus == base + kb',
          r4['trust_bonus'] == r4['trust_bonus_base'] + r4['kb_bonus'])
    check('domain_bonus 仅领域段=5（不含 KB）', r4['domain_bonus'] == 5,
          f"domain_bonus={r4['domain_bonus']}")

    print('--- 链A compute_final_score_v2 经聚合真源计入 domain ---')
    ra = compute_final_score_v2({'score': 40, 'url': 'https://example.com/x'},
                                '主题', with_domain=True, prefer_kb=True)
    exp_a = aggregate_score_v2(ra['base_score'], trust_bonus=ra['trust_bonus'],
                               domain_bonus=ra.get('domain_bonus', 0))['final_score']
    check('链A final == aggregate(base,trust,domain)',
          ra['after_whitelist_final'] == exp_a,
          f"final={ra['after_whitelist_final']} exp={exp_a}")

    print()
    if _fails:
        print(f'FAIL: {len(_fails)} 项失败 → {_fails}')
        sys.exit(1)
    print('ALL PASS (test_domain_bonus_no_double_count) ✅')
    sys.exit(0)


if __name__ == '__main__':
    main()
