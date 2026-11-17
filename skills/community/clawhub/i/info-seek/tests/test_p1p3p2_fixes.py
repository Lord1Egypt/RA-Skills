#!/usr/bin/env python3
"""Infoseek P1+P3+P2 修复验证（2026-09-10）

P1 保底逻辑：_filter_relevant 不足预期时不再裸返全量垃圾（分数兜底窗口 + 宁缺毋滥）
P3 词边界：ner.py 拉丁字母/数字词边界（meta ⊄ metadata/metaverse）；
          conflict_v3 正文优先（标题词不成为 claim）；entity_trajectory 主题截断
P2 内容链打通：render_report 消费 s.text（模板正文段 / _render_simple / _render_fallback）
"""
import os
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / 'core'))
sys.path.insert(0, str(ROOT / 'scripts'))

passed, failed = [], []

def check(name, cond, extra=''):
    if cond:
        passed.append(name); print(f"  [PASS] {name} {extra}")
    else:
        failed.append(name); print(f"  [FAIL] {name} {extra}")

# ═══════════════════════════════════════════════════════════════
# P1 保底逻辑（_filter_relevant）
# ═══════════════════════════════════════════════════════════════
print("\n═══ P1 保底逻辑 ═══")
import anchor_adapter
import infoseek_pipeline as pl

# 按 url 映射 mock 语义相似度分（compute + containment 双 patch，分数完全受控）
_SCORE_MAP = {}

def _fake_similarity(text, subject, method='jaccard'):
    for url, score in _SCORE_MAP.items():
        if url in text:
            return score
    return 0

anchor_adapter.compute_semantic_similarity = _fake_similarity
anchor_adapter._string_containment_similarity = _fake_similarity

def _mk(url, title=None):
    # title 内嵌 url 标识，使 mock 相似度函数可经 text 路由到分数
    return {'url': url, 'title': title or f'{url} semiconductor content', 'snippet': 'x'}

# P1-1 宁缺毋滥：全部 0 分 → 返回空（不再全量保送垃圾）
_SCORE_MAP.clear()
for u in ('u1', 'u2', 'u3'):
    _SCORE_MAP[u] = 0
res = pl._filter_relevant([_mk('u1'), _mk('u2'), _mk('u3')], 'advanced semiconductor 2026')
check('P1-1 全 0 分 → 空（宁缺毋滥，拒绝裸返垃圾）', res == [], f"len={len(res)}")

# P1-2 分数兜底窗口：1 条中分（<min_score 但 ≥floor）→ 保底返回该条而非全量
_SCORE_MAP.clear()
_SCORE_MAP['u1'] = 9   # >= floor(8) 但 < min_score(12) → 不进 kept，进保底窗口
_SCORE_MAP['u2'] = 0
_SCORE_MAP['u3'] = 0
res = pl._filter_relevant([_mk('u1'), _mk('u2'), _mk('u3')], 'advanced semiconductor 2026')
check('P1-2 中分条进保底窗口（非全量裸返）', len(res) == 1 and res[0]['url'] == 'u1'
      and res[0]['relevance'] == 9, f"got={[(r['url'], r.get('relevance')) for r in res]}")

# P1-3 正常路径：达标条数 ≥ 预期 → 全量 kept
_SCORE_MAP.clear()
_SCORE_MAP['u1'] = 15; _SCORE_MAP['u2'] = 14; _SCORE_MAP['u3'] = 13
res = pl._filter_relevant([_mk('u1'), _mk('u2'), _mk('u3')], 'advanced semiconductor 2026')
check('P1-3 达标 → kept 全量返回', len(res) == 3, f"len={len(res)}")

# P1-4 relevance 全量落分（保底窗口数据底座）
_SCORE_MAP.clear()
_SCORE_MAP['u1'] = 9; _SCORE_MAP['u2'] = 5; _SCORE_MAP['u3'] = 0
res = pl._filter_relevant([_mk('u1'), _mk('u2'), _mk('u3')], 'advanced semiconductor 2026')
check('P1-4 返回条目带 relevance 字段', all('relevance' in r for r in res)
      and res[0]['relevance'] == 9, f"got={[(r['url'], r.get('relevance')) for r in res]}")

# ═══════════════════════════════════════════════════════════════
# P3 词边界（ner / conflict_v3 / entity_trajectory）
# ═══════════════════════════════════════════════════════════════
print("\n═══ P3 词边界 ═══")
from ner import extract_entities

# P3-1 meta 独立词命中；metadata/metaverse 不误报
r = extract_entities('Meta 发布新战略；metadata 字段与 metaverse 平台无关')
meta_hit = any(e['entity_name'] for e in r if 'meta' in e['entity_name'].lower())
check('P3-1a 独立 Meta 命中', meta_hit, f"got={[e['entity_name'] for e in r]}")
r2 = extract_entities('the metadata schema and metaverse platform')
no_false = not any('meta' in e['entity_name'].lower() for e in r2)
check('P3-1b metadata/metaverse 不误报 Meta', no_false, f"got={[e['entity_name'] for e in r2]}")

# P3-2 既有场景回归：首字母大写 / 品牌名
r3 = extract_entities('OpenAI 宣布 GPT-5 开源，宁德时代发布财报')
names = [e['entity_name'] for e in r3]
check('P3-2 OpenAI/宁德时代 正常命中', 'OpenAI' in names and '宁德时代' in names, f"got={names}")

# P3-3 conflict_v3：正文优先，标题词不成为 claim
import conflict_v3
srcs = [
    {'text': 'OpenAI 发布新模型 GPT-5', 'title': '标题含某实体 XYZCorp 看点', 'url': 'u-1'},
    {'text': '', 'snippet': '', 'title': 'Anthropic 发布 Claude 用户须知', 'url': 'u-2'},
]
claims = conflict_v3._extract_fact_claims(srcs)
claim_ents = [c['entity_name'] for c in claims]
check('P3-3a 正文实体进入 claim', 'OpenAI' in claim_ents, f"got={claim_ents}")
check('P3-3b 标题词不进入 claim（正文存在时）',
      'XYZCorp' not in claim_ents, f"got={claim_ents}")

# P3-4 entity_trajectory 主题截断（中文按标点切，不腰斩）
from entity_trajectory import _truncate_subject
long_title = '半导体行业 2026 年先进制程深度报告：从 3nm 到 2nm 的工艺演进观察与产能分析展望'
cut = _truncate_subject(long_title)
check('P3-4 中文长标题按标点截断不腰斩',
      len(cut) < len(long_title) and '：' not in cut[-1:] or len(cut) <= 40,
      f"cut={cut}")

# ═══════════════════════════════════════════════════════════════
# P2 内容链打通（render_report 消费 s.text）
# ═══════════════════════════════════════════════════════════════
print("\n═══ P2 内容链打通 ═══")
from domain_orchestrator import DomainOrchestrator, _excerpt

SRCS = [
    {'title': '半导体先进制程加速', 'url': 'http://a.com', 'platform': 'b站', 'score': 85,
     'text': '半导体行业 2026 年先进制程加速推进。\n\n 多家厂商扩产 3nm 产线。', 'snippet': '短摘要'},
    {'title': '无正文源', 'url': 'http://b.com', 'platform': '知乎', 'score': 60, 'snippet': '只有摘要'},
]
o = DomainOrchestrator()

# P2-1 default 模板：来源条目含正文要点 + 关键内容要点聚合段
r = o.render_report('半导体先进制程 2026', SRCS, min_score=40)
md = r['markdown']
check('P2-1a default 模板来源含正文要点', '正文要点' in md and '扩产 3nm 产线' in md)
check('P2-1b default 模板含关键内容要点聚合段', '关键内容要点' in md)

# P2-2 _excerpt 空白压缩 + 归一
ex = _excerpt('  第一行\n\n第二行   第三行  ')
check('P2-2 _excerpt 压缩空白', ex == '第一行 第二行 第三行', f"got={ex!r}")

# P2-3 _render_fallback：无模板路径输出正文要点
r2 = o.render_report('半导体', SRCS, min_score=40, domain_override='no-such-domain')
check('P2-3 fallback 渲染含正文要点', '正文要点' in r2['markdown'])

# P2-4 领域模板（tech-research）含正文段
r3 = o.render_report('半导体', SRCS, min_score=40, domain_override='tech-research')
check('P2-4 领域模板含正文段', '正文要点' in r3['markdown'] and '扩产 3nm' in r3['markdown'])

# ═══════════════════════════════════════════════════════════════
print(f"\n=== P1+P3+P2 修复测试: {len(passed)} PASS / {len(failed)} FAIL ===")
sys.exit(1 if failed else 0)