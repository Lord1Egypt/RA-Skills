#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_domain_orchestrator_v200.py — domain_orchestrator 模板存储演进测试（v2.0.0）

覆盖范围：
  T1  yaml 模板加载（主路径 templates.yaml，6 模板）
  T2  渲染一致性（yaml 加载 vs 原始 .md.j2 文本，逐字节对比输出）
  T3  path 逻辑路径（templates.yaml#<key>）
  T4  旧版 .md.j2 目录回退兼容（构造临时目录模拟 v1.x 部署）
  T5  fallback 兜底（无模板目录时返回空 dict）
  T6  render_report 端到端（domain_override + template_used）

用法：
  python test_domain_orchestrator_v200.py
退出码：0 = 全 PASS
"""
import os
import sys
import tempfile
import shutil
from pathlib import Path

INFOSEEK_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK_ROOT / 'scripts'))

PASS, FAIL = 0, 0


def check(name, cond, detail=''):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f'  ✓ {name}')
    else:
        FAIL += 1
        print(f'  ✗ FAIL {name} {detail}')


def load_original_j2() -> dict:
    """加载原始 .md.j2 文本（若目录仍存在）作为基准"""
    tdir = INFOSEEK_ROOT / 'domains' / 'templates'
    result = {}
    if tdir.exists():
        for f in sorted(tdir.glob('*.md.j2')):
            result[f.stem.replace('.md', '')] = f.read_text(encoding='utf-8')
    return result


def main():
    print('═══ T1: yaml 模板加载（主路径） ═══')
    from domain_orchestrator import DomainOrchestrator
    orch = DomainOrchestrator()
    tpls = orch.templates
    check('T1.1 模板数 = 6', len(tpls) == 6, f'got {len(tpls)}')
    expected_keys = {'competitor-intel', 'default', 'finance-research',
                     'market-research', 'policy-research', 'tech-research'}
    check('T1.2 key 集合完整', set(tpls.keys()) == expected_keys,
          f'diff={expected_keys ^ set(tpls.keys())}')
    check('T1.3 每模板含 raw/path', all({'raw', 'path'} <= set(v) for v in tpls.values()))

    print('═══ T2: 渲染一致性（yaml vs 原始 j2） ═══')
    originals = load_original_j2()
    ctx = {'subject': '新能源汽车竞争格局', 'domain': 'competitor-intel',
           'sources': [{'title': 'A公司财报', 'score': 92, 'url': 'https://a.com',
                        'platform': '微博', 'snippet': '营收增长30%'},
                       {'title': 'B行业报告', 'score': 78, 'url': 'https://b.com',
                        'platform': '公众号', 'snippet': '市场份额' * 30}],
           'sources_count': 2, 'is_default_template': False}
    from jinja2 import Template
    if originals:
        diff = 0
        for k in expected_keys:
            a = Template(originals[k]).render(**ctx)
            b = Template(tpls[k]['raw']).render(**ctx)
            if a != b:
                diff += 1
                print(f'    RENDER DIFF: {k}')
        check('T2.1 全部模板渲染输出一致', diff == 0, f'{diff} 个不一致')
    else:
        check('T2.1 渲染输出（仅 yaml 路径）', all(
            '{{' not in Template(tpls[k]['raw']).render(**ctx) for k in expected_keys))

    print('═══ T3: path 逻辑路径 ═══')
    check('T3.1 path = templates.yaml#<key>',
          all(v['path'] == f'templates.yaml#{k}' for k, v in tpls.items()),
          str(tpls.get('competitor-intel', {}).get('path')))

    print('═══ T4: 旧版 .md.j2 目录回退兼容 ═══')
    with tempfile.TemporaryDirectory() as tmp:
        tdir = Path(tmp) / 'templates'
        tdir.mkdir()
        (tdir / 'legacy-test.md.j2').write_text('# {{ subject }}\n旧版模板', encoding='utf-8')
        orch_legacy = DomainOrchestrator(profile_dir=tmp, template_dir=str(tdir))
        check('T4.1 旧版目录被加载', 'legacy-test' in orch_legacy.templates)
        check('T4.2 旧版 path = 真实文件路径',
              orch_legacy.templates['legacy-test']['path'] == str(tdir / 'legacy-test.md.j2'))
        md = Template(orch_legacy.templates['legacy-test']['raw']).render(subject='S', domain='D', sources=[])
        check('T4.3 旧版模板可渲染', 'S' in md and '旧版模板' in md)

    print('═══ T5: fallback 兜底 ═══')
    orch_empty = DomainOrchestrator(profile_dir='/tmp/nonexistent_dir_xyz')
    check('T5.1 无模板目录 → 空 dict', orch_empty.templates == {})

    print('═══ T6: render_report 端到端 ═══')
    result = orch.render_report('新能源汽车竞争格局', [
        {'title': 'A公司财报', 'score': 92, 'url': 'https://a.com', 'platform': '微博',
         'snippet': '营收增长30%'},
        {'title': 'B行业报告', 'score': 78, 'url': 'https://b.com', 'platform': '公众号',
         'snippet': '市场份额持续提升'},
    ], domain_override='competitor-intel')
    check('T6.1 markdown 非空且含主题', result['markdown'] and '新能源汽车竞争格局' in result['markdown'])
    check('T6.2 template_used = templates.yaml#competitor-intel',
          result['template_used'] == 'templates.yaml#competitor-intel',
          str(result['template_used']))
    check('T6.3 qualified_count = 2', result['qualified_count'] == 2)
    check('T6.4 is_default_template = False', result['is_default_template'] is False)

    print(f'\n结果: {PASS} PASS / {FAIL} FAIL')
    sys.exit(0 if FAIL == 0 else 1)


if __name__ == '__main__':
    main()
