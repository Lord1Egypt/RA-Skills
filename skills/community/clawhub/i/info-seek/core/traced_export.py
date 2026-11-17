#!/usr/bin/env python3
"""
core/traced_export.py — Infoseek 引用图 + 实体图联合导出（v2.3.1 新增，主题②）

把 v2.3.0 的 entity_graph（实体共现边）并入"来源引用结构"，
输出可追溯的联合图（dot + markdown），供 research() 报告嵌入。

设计：
- build_traced(sources, entity_graph)：联合节点/边
    - 边类型 'co_occurrence'：实体共现（来自 entity_graph.top_relations）
    - 边类型 'reference'：来源 → 其提及的实体（来自 NER / 图谱节点）
- to_dot() / to_markdown()：两种导出格式
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))


def _source_label(src: Dict) -> str:
    return src.get('url', '') or src.get('title', 'Untitled')


def build_traced(sources: List[Dict], entity_graph: Optional[Dict] = None) -> Dict:
    """联合导出：来源节点 + 实体共现边 + 来源→实体引用边

    参数:
        sources: research() 来源列表
        entity_graph: EntityGraph.to_dict() 输出（含 top_relations）

    返回:
        {'nodes': [...], 'edges': [...], 'source_count', 'entity_relation_count'}
    """
    nodes = []
    edges = []
    seen_nodes = set()

    # 1) 实体共现边（来自图谱）
    if entity_graph:
        for rel in entity_graph.get('top_relations', []):
            a, b = rel['entity_a'], rel['entity_b']
            for n in (a, b):
                if n not in seen_nodes:
                    seen_nodes.add(n)
                    nodes.append(n)
            edges.append({
                'from': a, 'to': b,
                'type': 'co_occurrence',
                'weight': rel.get('weight', 1),
            })

    # 2) 来源节点 + 来源→实体引用边（轻量 NER）
    try:
        from ner import extract_entities
        for src in sources:
            label = _source_label(src)
            slabel = f'src:{label}'
            if slabel not in seen_nodes:
                seen_nodes.add(slabel)
                nodes.append(slabel)
            text = ' '.join([
                src.get('text', '') or src.get('snippet', '') or '',
                src.get('title', ''),
            ])
            if text.strip():
                for e in extract_entities(text):
                    ent = e['entity_name']
                    if ent not in seen_nodes:
                        seen_nodes.add(ent)
                        nodes.append(ent)
                    edges.append({
                        'from': slabel, 'to': ent,
                        'type': 'reference',
                        'weight': 1,
                    })
    except Exception:
        pass  # NER 失败不阻断

    return {
        'nodes': nodes,
        'edges': edges,
        'source_count': len({_source_label(s) for s in sources}),
        'entity_relation_count': sum(1 for e in edges if e['type'] == 'co_occurrence'),
    }


def to_dot(traced: Dict) -> str:
    """Graphviz dot 导出（两类边用不同颜色）"""
    lines = ['digraph TracedExport {', '  rankdir=LR;']
    for n in traced['nodes']:
        safe = n.replace('"', '\\"')
        fill = '#fff7e6' if n.startswith('src:') else '#e8f4fd'
        shape = 'ellipse' if n.startswith('src:') else 'box'
        lines.append(f'  "{safe}" [shape={shape}, style="rounded,filled", fillcolor="{fill}"];')
    color = {'co_occurrence': '#2c7fb8', 'reference': '#999999'}
    for e in traced['edges']:
        a = e['from'].replace('"', '\\"')
        b = e['to'].replace('"', '\\"')
        c = color.get(e['type'], '#cccccc')
        lines.append(f'  "{a}" -> "{b}" [color="{c}", penwidth={min(e.get("weight", 1), 5)}];')
    lines.append('}')
    return '\n'.join(lines)


def to_markdown(traced: Dict, subject: str = '') -> str:
    """Markdown 溯源导出"""
    lines = [f'# 溯源导出：{subject}', '',
             f'- 来源数：{traced["source_count"]}',
             f'- 实体关系边数：{traced["entity_relation_count"]}', '']
    co = [e for e in traced['edges'] if e['type'] == 'co_occurrence']
    if co:
        lines.append('## 实体共现关系')
        for e in co:
            lines.append(f'- {e["from"]} ↔ {e["to"]}（权重 {e.get("weight", 1)}）')
    refs = [e for e in traced['edges'] if e['type'] == 'reference']
    if refs:
        lines.append('')
        lines.append(f'## 来源→实体引用（{len(refs)} 条）')
        for e in refs[:30]:
            lines.append(f'- {e["from"]} → {e["to"]}')
    return '\n'.join(lines)


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    import sys as _sys
    import json as _json
    if len(_sys.argv) < 2:
        print("Usage: python -m core.traced_export demo")
        return
    # demo
    demo_sources = [
        {'title': 'OpenAI 开源 GPT-5', 'snippet': 'OpenAI 与 Microsoft 合作', 'url': 'https://a.com/1'},
        {'title': '宁德时代财报', 'snippet': '宁德时代 营收增长', 'url': 'https://b.com/2'},
    ]
    g = None
    try:
        from entity_graph import EntityGraph
        eg = EntityGraph()
        eg.build_from_sources(demo_sources)
        g = eg.to_dict()
    except Exception:
        pass
    traced = build_traced(demo_sources, g)
    print(_json.dumps(traced, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
