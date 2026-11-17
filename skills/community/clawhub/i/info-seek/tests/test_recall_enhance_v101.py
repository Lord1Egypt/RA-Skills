#!/usr/bin/env python3
"""test_recall_enhance_v101.py — 搜索召回增强测试（1.2.X-1 · v1.2.x）

覆盖：
  RE1 _expand_query 实体别名扩展（mock 实体库）
  RE2 _expand_query 无命中原样返回
  RE3 _expand_query 实体库异常防御
  RE4 _merge_diverse 轮询防单源垄断
  RE5 _merge_diverse url 去重
  RE6 _query_type / _engine_weight_for 动态权重（finance query）
  RE7 _filter_relevant 自适应门槛（候选多→门槛 14，候选少→门槛 10）
  RE8 search_web 集成（monkeypatch 引擎）：diversity 开 → 结果含 engine 且来源分散
"""

import os
import sys
import tempfile
import unittest.mock as mock
from pathlib import Path

INFOSEEK = Path(__file__).parent.parent
sys.path.insert(0, str(INFOSEEK / 'scripts'))
sys.path.insert(0, str(INFOSEEK / 'core'))
sys.path.insert(0, str(INFOSEEK))  # core 包（core.entities）需要根目录

import engine_lifecycle as el
import infoseek_pipeline as pipe

# 隔离数据目录 + 重置生命周期（避免历史禁用状态影响集成测试）
_tmp = tempfile.mkdtemp()
os.environ['INFOSEEK_DATA_DIR'] = _tmp
el.reset_instance()

passed, failed = [], []
def check(name, cond, detail=''):
    (passed if cond else failed).append(name)
    print(f"[{'PASS' if cond else 'FAIL'}] {name}" + (f" — {detail}" if detail else ""))


# ── RE1/RE2/RE3: _expand_query ──
_ENTS = [
    {'name': '比亚迪', 'aliases': ['BYD', 'byd'], 'category': 'ORG'},
    {'name': 'OpenAI', 'aliases': ['openai', 'OpenAI 公司'], 'category': 'ORG'},
]
with mock.patch('core.entities.get_all_entities', return_value=_ENTS):
    q1 = pipe._expand_query('比亚迪 2026 财报')
    check('RE1 别名扩展命中', 'BYD' in q1 and q1.startswith('比亚迪 2026 财报'), f"={q1}")
    q2 = pipe._expand_query('量子计算 2026 趋势')
    check('RE2 无命中原样返回', q2 == '量子计算 2026 趋势', f"={q2}")
with mock.patch('core.entities.get_all_entities', side_effect=RuntimeError('boom')):
    q3 = pipe._expand_query('某主题')
    check('RE3 实体库异常防御', q3 == '某主题', f"={q3}")


# ── RE4/RE5: _merge_diverse ──
col = {
    'Bing-RSS': [{'url': f'https://bing{i}.com', 'title': f'b{i}', 'snippet': ''} for i in range(5)],
    'Jina-AI': [{'url': f'https://jina{i}.com', 'title': f'j{i}', 'snippet': ''} for i in range(5)],
}
out = pipe._merge_diverse(col, 4, '测试 query')
engs = [r.get('engine') for r in out]
check('RE4 轮询防单源垄断（交替）', len(out) == 4 and len(set(engs)) == 2, f"engs={engs}")
check('RE4 top4 无单源垄断', engs.count('Bing-RSS') <= 2 and engs.count('Jina-AI') <= 2,
      f"={engs}")
# 去重：两个引擎返回相同 url
col2 = {
    'A': [{'url': 'https://dup.com', 'title': 'a', 'snippet': ''}],
    'B': [{'url': 'https://dup.com', 'title': 'b', 'snippet': ''},
          {'url': 'https://uniq.com', 'title': 'u', 'snippet': ''}],
}
out2 = pipe._merge_diverse(col2, 5, 'q')
check('RE5 url 去重', len(out2) == 2, f"={[r['url'] for r in out2]}")


# ── RE6: _query_type / _engine_weight_for ──
check('RE6 finance 分类', pipe._query_type('宁德时代 财报 营收 利润') == 'finance')
check('RE6 tech 分类', pipe._query_type('大模型 芯片 算力') == 'tech')
w_base = pipe._engine_weight_for('Zhipu', '通用 query')
os.environ['INFOSEEK_RECALL_DYN_WEIGHT'] = '1'
try:
    w_fin = pipe._engine_weight_for('Zhipu', '财报 营收 利润')
    check('RE6 动态权重 finance 提升 Zhipu', w_fin > w_base, f"{w_base}→{w_fin}")
    check('RE6 general query 无加成', pipe._engine_weight_for('Zhipu', '通用主题') == w_base)
finally:
    os.environ.pop('INFOSEEK_RECALL_DYN_WEIGHT', None)


# ── RE7: _filter_relevant 自适应门槛 ──
def _mk(n):
    return [{'url': f'https://s{i}.com', 'title': f'条目{i} 行业2026', 'snippet': ''}
            for i in range(n)]
with mock.patch('anchor_adapter.compute_semantic_similarity') as m, \
     mock.patch('anchor_adapter._string_containment_similarity') as mc, \
     mock.patch.object(pipe, '_min_expected', return_value=0):
    # 候选 25（>20）：score 恒 13 → 门槛 14 → 全部过滤 → 返回 []
    mc.return_value = 0  # 关闭 containment 兜底（P1）：分数由 compute mock 完全控制
    m.side_effect = lambda t, q: 13
    r25 = pipe._filter_relevant(_mk(25), '行业 2026 竞争格局')
    check('RE7 候选多→门槛升(14)，13 分全滤', r25 == [], f"len={len(r25)}")
    # 候选 25：title 索引 ≥10 者 15 分（15 条）→ 门槛 14 → 保留 15 条
    def _sc(t, q):
        first = t.split(' ')[0]  # 条目{i}
        num = ''.join(c for c in first if c.isdigit())
        return 15 if num and int(num) >= 10 else 13
    m.side_effect = _sc
    r25b = pipe._filter_relevant(_mk(25), '行业 2026 竞争格局')
    check('RE7 候选多→门槛 14 保留高分', len(r25b) == 15 and all(r['relevance'] >= 14 for r in r25b),
          f"len={len(r25b)}")
    # v1.7.7 包A（P1#5）：自适应门槛下限固定 12（候选少不再降至 10）→ 11 分被门槛滤除
    m.side_effect = lambda t, q: 11
    r4 = pipe._filter_relevant(_mk(4), '行业 2026 竞争格局')
    check('RE7 候选少不降门槛(12)，11 分被滤', r4 == [],
          f"len={len(r4)}")


# ── RE8: search_web 集成（diversity 默认开） ──
def _fake_a(query, n):
    return [{'url': f'https://a{i}.com', 'title': f'A{i} 行业 2026', 'snippet': '行业 2026 分析'} for i in range(3)]
def _fake_b(query, n):
    return [{'url': f'https://b{i}.com', 'title': f'B{i} 行业 2026', 'snippet': '行业 2026 分析'} for i in range(3)]
with mock.patch.object(pipe, '_default_layer', return_value=[('A', _fake_a), ('B', _fake_b)]), \
     mock.patch.object(pipe.time, 'sleep'), \
     mock.patch('infoseek_pipeline._env_flag', side_effect=lambda n, d: True):
    res = pipe.search_web('行业 2026 竞争格局', max_results=6)
    check('RE8 search_web 返回结果', len(res) > 0, f"len={len(res)}")
    engs8 = [r.get('engine') for r in res]
    check('RE8 结果含 engine 标签', all(e in ('A', 'B') for e in engs8), f"={engs8}")
    check('RE8 来源分散（无单源垄断 top-N）',
          len(set(engs8)) == 2 and engs8.count('A') <= 3 and engs8.count('B') <= 3,
          f"={engs8}")


print(f"\n=== 召回增强测试: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)
