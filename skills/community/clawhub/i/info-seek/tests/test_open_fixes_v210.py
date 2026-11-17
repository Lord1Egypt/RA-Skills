#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""test_open_fixes_v210.py — P0-OPEN-04 / P0-OPEN-05 / P0-OPEN-06 缺口守护。

覆盖：
  P0-OPEN-04  score 入口量纲归一化（0–1 → ×100）+ 核心源为 0 禁止空骨架（过滤清单及原因）
  P0-OPEN-06  时间事实槽（年月/季度 → ISO 区间）+ 结果区分 无冲突 / 未评估（覆盖率）
  P0-OPEN-05  路由（GPT-5→tech、PE 不再误命中 openai）+ 模板按域收窄 + 高分源跨源综合段

版本约束：本轮缺口修复**版本号保持 2.1.0 不变**，本套件固化该口径。
脚本风格：顶层直跑 + sys.exit，供 tests/run_all.py 以子进程执行（勿用 pytest 收集）。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / 'scripts'))
sys.path.insert(0, str(ROOT / 'core'))

_P = 0
_F = 0


def check(name, cond, extra=''):
    global _P, _F
    if cond:
        _P += 1
        print(f'  [PASS] {name}')
    else:
        _F += 1
        print(f'  [FAIL] {name} {extra}')


# ─────────────────────────────────────────────────────────────
print('== P0-OPEN-04 · 量纲归一化 ==')
from infoseek_core_v2 import score_source  # noqa: E402

r = score_source({'url': 'https://example.gov.cn/p', 'title': '政府文件',
                  'score': 0.72}, '完全无关主题词xyz')
check('04-1 入参 0.72 自动 ×100 → base 72', r['base_score'] == 72,
      f"base={r['base_score']}")
check('04-2 scale_normalized=True', r['scale_normalized'] is True)
check('04-3 归一后不再被当噪声（final≥40 或 trust 抬升）', r['final_score'] >= 40,
      f"final={r['final_score']}")

r0 = score_source({'url': 'https://example.com/a', 'title': 't', 'score': 0}, 'q')
check('04-4 精确 0 不做归一', r0['scale_normalized'] is False)

r100 = score_source({'url': 'https://example.com/b', 'title': 't',
                     'score': 1}, 'q')
check('04-5 边界 1 归一为 100', r100['base_score'] == 100 and
      r100['scale_normalized'] is True, f"base={r100['base_score']}")

r72 = score_source({'url': 'https://example.com/c', 'title': 't',
                    'score': 72}, 'q')
check('04-6 百分制 72 不被归一', r72['base_score'] == 72 and
      r72['scale_normalized'] is False)


print('== P0-OPEN-04 · 核心源为 0 禁止空骨架 ==')
from domain_orchestrator import DomainOrchestrator  # noqa: E402

orch = DomainOrchestrator()
zero_srcs = [
    {'title': '源A', 'url': 'https://a.com/p', 'platform': 'web', 'score': 0},
    {'title': '源B', 'url': 'https://b.com/p', 'platform': 'zhihu', 'score': 0},
]
res0 = orch.render_report('某主题', zero_srcs, domain_override='tech-research')
check('04-7 全 0 源 qualified_count==0', res0['qualified_count'] == 0)
check('04-8 all_core_zero=True', res0['all_core_zero'] is True)
check('04-9 filtered_out 含全部源及原因', res0['filtered_count'] == 2 and
      all(x['reason'] for x in res0['filtered_out']))
check('04-10 报告前置「无可用核心来源」告警（禁空骨架）',
      '无可用核心来源' in res0['markdown'] and '源A' in res0['markdown']
      and '源B' in res0['markdown'])
check('04-11 告警明确提示评分链断裂而非无资料', '评分链' in res0['markdown'])

mixed = [
    {'title': '好源', 'url': 'https://g.com/p', 'platform': 'web', 'score': 80},
    {'title': '弱源', 'url': 'https://w.com/p', 'platform': 'web', 'score': 20},
]
res_m = orch.render_report('某主题', mixed, domain_override='tech-research')
check('04-12 部分低分：qualified=1 filtered=1 all_core_zero=False',
      res_m['qualified_count'] == 1 and res_m['filtered_count'] == 1 and
      res_m['all_core_zero'] is False)
check('04-13 低分源附可追溯清单（非全 0 折叠块）',
      '被过滤来源' in res_m['markdown'] and '弱源' in res_m['markdown'])


# ─────────────────────────────────────────────────────────────
print('== P0-OPEN-06 · 时间事实槽 ==')
from contradiction_scorer import _parse_time_spans, time_slot_score, \
    score_contradiction  # noqa: E402

check('06-1 解析「2024年Q1」→ ISO 季度区间',
      [(s['start'], s['end']) for s in _parse_time_spans('2024年Q1发布')] ==
      [('2024-01-01', '2024-04-01')])
check('06-2 解析「2023年第三季度」',
      any(s['label'] == '2023年Q3' and s['start'] == '2023-07-01'
          for s in _parse_time_spans('2023年第三季度')))
check('06-3 解析「Q2 2022」',
      any(s['label'] == '2022年Q2' for s in _parse_time_spans('Q2 2022')))
check('06-4 解析「2024年3月」→ 月区间',
      [(s['start'], s['end']) for s in _parse_time_spans('2024年3月上市')] ==
      [('2024-03-01', '2024-04-01')])
check('06-5 解析中文月「2024年十一月」',
      any(s['label'] == '2024年11月' for s in _parse_time_spans('2024年十一月')))
check('06-6 解析英文月「March 2024」',
      any(s['label'] == '2024年3月' for s in _parse_time_spans('March 2024')))
check('06-7 单独年份「公司2023年成立」（中文前缀不误杀）',
      [s['label'] for s in _parse_time_spans('公司2023年成立')] == ['2023年'])
check('06-8 季度序号短语不误抽（「连续3个季度」）',
      _parse_time_spans('连续3个季度增长') == [])
check('06-9 普通金额不误抽时间（「1234万元」）',
      _parse_time_spans('营收1234万元') == [])

q1 = time_slot_score('产品2023年Q1发布', '产品2024年第三季度才发布')
check('06-10 季度时间冲突 60 分 + both_timed',
      q1['conflict'] is True and q1['score'] == 60 and
      q1['coverage'] == 'both_timed')
q2 = time_slot_score('2024年3月发布', '2024年第一季度发布')
check('06-11 月落在同季度区间内 → 不冲突', q2['conflict'] is False)
q3 = time_slot_score('2023年成立', '2024年成立')
check('06-12 年仅粒度跨年 → 粗粒度冲突 35', q3['conflict'] is True and
      q3['score'] == 35)
q4 = time_slot_score('产品很好用', '产品2024年发布')
check('06-13 仅一侧有时间 → partial 未评估不判冲突',
      q4['coverage'] == 'partial' and q4['conflict'] is False)
q5 = time_slot_score('今天天气不错', '这本书封面好看')
check('06-14 双侧无时间 → neither', q5['coverage'] == 'neither')

print('== P0-OPEN-06 · 无冲突 / 未评估 区分 ==')
c_conf = score_contradiction({'text': '该公司2023年Q1发布新品'},
                             {'text': '该产品2024年第三季度才发布'})
check('06-15 时间矛盾 verdict=conflict / mode=time / time_score=60',
      c_conf['verdict'] == 'conflict' and c_conf['scorer_mode'] == 'time' and
      c_conf['time_score'] == 60)
c_nc = score_contradiction({'text': '公司2024年3月完成融资'},
                           {'text': '该轮融资2024年第一季度官宣'})
check('06-16 双侧时间相容 verdict=no_conflict',
      c_nc['verdict'] == 'no_conflict' and c_nc['score'] == 0)
c_na = score_contradiction({'text': '今天适合出门散步'},
                           {'text': '这本书封面很有质感'})
check('06-17 无可对拍事实槽 verdict=not_assessable',
      c_na['verdict'] == 'not_assessable' and c_na['assessable'] is False)
c_num = score_contradiction({'text': '公司营收增长35%', 'entity': 'X'},
                            {'text': '公司营收仅增长12%', 'entity': 'X'})
check('06-18 既有键控数值冲突仍工作（零回归）',
      c_num['verdict'] == 'conflict' and 'revenue' in c_num['conflict_slots'])

# 06-19 时间槽路容错：正则异常不得击穿主评分（L3-05 健壮性契约）
import unittest.mock as _mock  # noqa: E402
import contradiction_scorer as _csm  # noqa: E402
with _mock.patch.object(_csm.re, 'finditer',
                        side_effect=RuntimeError('mock re')):
    try:
        c_robust = score_contradiction({'text': 'X 不发布'}, {'text': 'X 发布'})
        check('06-19 时间解析异常不崩（降级未评估，仍出分）',
              isinstance(c_robust, dict) and 'score' in c_robust and
              c_robust.get('time_coverage') == 'neither')
    except Exception as e:  # noqa: BLE001
        check('06-19 时间解析异常不崩', False, f'raised {type(e).__name__}: {e}')


# ─────────────────────────────────────────────────────────────
print('== P0-OPEN-05 · 路由 ==')
from domain_router import detect_domain  # noqa: E402

for q in ['GPT-5', 'GPT-5 发布', 'GPT5', 'gpt4', 'GPT4o', 'ChatGPT 评测',
          'claude 模型', 'DeepSeek 开源模型']:
    check(f'05-{q} → tech-research', detect_domain(q).get('domain') ==
          'tech-research', f"got={detect_domain(q).get('domain')}")
check('05-路由 OpenAI Agent 不再误判金融（PE 词边界）',
      detect_domain('OpenAI Agent').get('domain') == 'tech-research',
      f"got={detect_domain('OpenAI Agent').get('domain')}")
check('05-路由 真正 PE 市盈率仍判 finance',
      detect_domain('PE 市盈率分析').get('domain') == 'finance-research')
for q, exp in [('股票回测策略', 'finance-research'),
               ('KDJ 金叉', 'finance-research'),
               ('钢卷分切工艺', 'tech-research'),
               ('市场规模 CAGR', 'market-research'),
               ('竞品功能对比', 'competitor-intel')]:
    check(f'05-路由 {q} → {exp}', detect_domain(q).get('domain') == exp)


print('== P0-OPEN-05 · 模板按域收窄 + 跨源综合段 ==')
import yaml  # noqa: E402
from jinja2 import Template  # noqa: E402

_tpl = yaml.safe_load((ROOT / 'domains' / 'templates.yaml')
                      .read_text(encoding='utf-8'))['templates']
check('05-模板 6 个模板齐全', set(_tpl) == {
    'default', 'tech-research', 'finance-research', 'market-research',
    'policy-research', 'competitor-intel'})

srcs = [
    {'title': 'GPT-5官方', 'platform': 'openai.com', 'url': 'https://o.com',
     'score': 92, 'text_excerpt': 'GPT-5 多模态能力增强。'},
    {'title': '第三方评测', 'platform': 'zhihu', 'url': 'https://z.com',
     'score': 75, 'text_excerpt': '推理能力显著提升。'},
    {'title': '低分传闻', 'platform': 'web', 'url': 'https://w.com',
     'score': 20, 'text_excerpt': '传闻。'},
]
ctx = dict(subject='GPT-5', domain='tech-research', sources=srcs,
           sources_count=3, is_default_template=False, filter_block='',
           filtered_count=1)
tech_md = Template(_tpl['tech-research']).render(**ctx)
check('05-模板 tech 去钢铁硬编码（无圆盘刀/钢卷/QC四维度）',
      not any(w in tech_md for w in ['圆盘刀', '钢卷', '锥度张力']))
check('05-模板 tech 含「跨源综合」段', '跨源综合' in tech_md)
check('05-模板 多源综合正确识别 2 个 ≥70 核心源',
      '2 个高分核心源' in tech_md)

one = [{'title': '唯一好源', 'platform': 'web', 'url': 'u', 'score': 80,
        'text_excerpt': '要点'}]
one_md = Template(_tpl['tech-research']).render(
    subject='X', domain='tech-research', sources=one, sources_count=1,
    is_default_template=False, filter_block='')
check('05-模板 单高分源提示补充第二来源', '仅 1 个高分核心源' in one_md)

weak = [{'title': '弱', 'platform': 'web', 'url': 'u', 'score': 45,
         'text_excerpt': 'x'}]
weak_md = Template(_tpl['default']).render(
    subject='X', domain='general', sources=weak, sources_count=1,
    is_default_template=True, filter_block='')
check('05-模板 无 ≥70 源时告警', '无评分 ≥ 70 的高分核心源' in weak_md)

empty_md = Template(_tpl['tech-research']).render(
    subject='X', domain='tech-research', sources=[], sources_count=0,
    is_default_template=False, filter_block='')
check('05-模板 空源守卫提示', '没有入围核心来源' in empty_md)

# 6 模板全部能无异常渲染（无 Jinja 模板错误）
for name in _tpl:
    try:
        Template(_tpl[name]).render(subject='S', domain='tech-research',
                                    sources=srcs, sources_count=3,
                                    is_default_template=False, filter_block='')
        ok = True
    except Exception as e:  # noqa: BLE001
        ok = False
        print(f'    render error {name}: {e}')
    check(f'05-模板 {name} Jinja 渲染无异常', ok)


print(f'\n=== test_open_fixes_v210: {_P} PASS / {_F} FAIL ===')
sys.exit(1 if _F else 0)
