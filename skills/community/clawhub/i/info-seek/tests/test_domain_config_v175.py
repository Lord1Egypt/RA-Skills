#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_domain_config_v175.py — D 声明层配置化

覆盖：
  T1 references/keyword.yaml 唯一真源加载
  T2 env INFOSEEK_KEYWORD_YAML 失效路径 → 内置 fallback（路由不塌）
  T3 加载后 detect_domain 行为一致（交集判定）
  T4 常量配置化（_int_env / _TRUST_HINTS）
  T5 parse_domain_params（domains/*.yaml 声明块解析）
  T6 kb_intersect_bonus profile 覆盖（tech 8 / finance 10 / 多 KB +4）
  T7 domains/*.yaml 声明块实际存在
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
sys.path.insert(0, os.path.join(ROOT, 'core'))
os.environ.setdefault('INFOSEEK_PLATFORM_WEBSEARCH', 'off')

import domain_router as dr  # noqa: E402

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

print('[T1] keyword.yaml 唯一真源加载')
check('T1 五域齐全',
      set(dr.DOMAIN_TRIGGERS.keys()) == {'tech-research', 'market-research',
                                         'finance-research', 'policy-research', 'competitor-intel'},
      str(sorted(dr.DOMAIN_TRIGGERS.keys())))
check('T1 tech 关键词 >=60', len(dr.DOMAIN_TRIGGERS['tech-research']['keywords']) >= 60,
      str(len(dr.DOMAIN_TRIGGERS['tech-research']['keywords'])))
check('T1 每域含 weight/keywords',
      all('weight' in v and v.get('keywords') for v in dr.DOMAIN_TRIGGERS.values()))

print('[T1b] 读取 yaml 生效（独有域探测）+ 文件存在')
import tempfile  # noqa: E402

check('T1c keyword.yaml 文件存在',
      os.path.exists(os.path.join(ROOT, 'references', 'keyword.yaml')))
_tmp = tempfile.mkdtemp(prefix='kw_')
_kw = os.path.join(_tmp, 'kw.yaml')
with open(_kw, 'w', encoding='utf-8') as _f:
    _f.write('domains:\n  zz-probe:\n    weight: 1.0\n    keywords: ["probe"]\n')
os.environ['INFOSEEK_KEYWORD_YAML'] = _kw
dr = importlib.reload(dr)
check('T1b 独有域 zz-probe 出现', 'zz-probe' in dr.DOMAIN_TRIGGERS, str(list(dr.DOMAIN_TRIGGERS.keys())))
del os.environ['INFOSEEK_KEYWORD_YAML']
dr = importlib.reload(dr)
check('T1b reload 后回到五域', len(dr.DOMAIN_TRIGGERS) == 5, str(len(dr.DOMAIN_TRIGGERS)))

print('[T2] fallback（env 指向不存在文件）')
os.environ['INFOSEEK_KEYWORD_YAML'] = '/nonexistent/kw.yaml'
dr = importlib.reload(dr)
check('T2 五域不塌', len(dr.DOMAIN_TRIGGERS) == 5, str(len(dr.DOMAIN_TRIGGERS)))
check('T2 fallback == 内置',
      dr.DOMAIN_TRIGGERS == {
          k: {'weight': v['weight'], 'keywords': list(v['keywords']),
              # DEF-16（v2.1.1）：fallback 同样携带歧义短词边界配置（缺失回退空集）
              'strict_keywords': list(v.get('strict_keywords', [])),
              'false_compounds': list(v.get('false_compounds', []))}
          for k, v in dr._BUILTIN_TRIGGERS.items()})
del os.environ['INFOSEEK_KEYWORD_YAML']
dr = importlib.reload(dr)

print('[T3] 加载后 detect_domain 行为一致')
r = dr.detect_domain(MULTI)
check('T3 交集 tech+finance', r['is_intersect'] is True and r['prefer_kb'] is True, str(r['intersect_domains']))
check('T3 单域不判交集', dr.detect_domain('AI 大模型 芯片 算力 英伟达')['is_intersect'] is False)

print('[T4] 常量配置化')
check('T4 _int_env 缺省回落', dr._int_env('NO_SUCH_VAR_XYZ', 7) == 7)
os.environ['TMP_INT_X'] = 'abc'
check('T4 _int_env 非法回落', dr._int_env('TMP_INT_X', 5) == 5)
os.environ['TMP_INT_X'] = '42'
check('T4 _int_env 生效', dr._int_env('TMP_INT_X', 5) == 42)
del os.environ['TMP_INT_X']
check('T4 _TRUST_HINTS 默认', dr._TRUST_HINTS == ('来源', 'Tier', '白名单'), str(dr._TRUST_HINTS))

print('[T5] parse_domain_params')
check('T5 解析 boost+priority',
      dr.parse_domain_params({'raw': 'intersect_boost: 12\nkb_priority: true'})
      == {'intersect_boost': 12, 'kb_priority': True})
check('T5 缺省 None',
      dr.parse_domain_params({'raw': 'nothing here'})
      == {'intersect_boost': None, 'kb_priority': None})
check('T5 空 profile 安全', dr.parse_domain_params({}) == {'intersect_boost': None, 'kb_priority': None})

print('[T6] kb_intersect_bonus profile 覆盖')
S1 = {'_kb_domain': 'x', '_kb_hit_count': 1}
S2 = {'_kb_domain': 'x', '_kb_hit_count': 2}
check('T6 默认 8（无 profile）', dr.kb_intersect_bonus(S1) == 8)
check('T6 tech boost=8', dr.kb_intersect_bonus(S1, {'raw': 'intersect_boost: 8'}) == 8)
check('T6 finance boost=10', dr.kb_intersect_bonus(S1, {'raw': 'intersect_boost: 10'}) == 10)
check('T6 多 KB 额外 +4', dr.kb_intersect_bonus(S2, {'raw': 'intersect_boost: 10'}) == 14)

print('[T7] domains/*.yaml 声明块存在')
for name, exp in [('tech-research', 8), ('finance-research', 10), ('competitor-intel', 6)]:
    raw = open(os.path.join(ROOT, 'domains', f'{name}.yaml'), encoding='utf-8').read()
    got = dr.parse_domain_params({'raw': raw})['intersect_boost']
    check(f'T7 {name} boost={exp}', got == exp, str(got))

print(f'\n=== test_domain_config_v175: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
