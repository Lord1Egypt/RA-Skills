#!/usr/bin/env python3
"""
core/entity_graph.py — Infoseek 实体图谱（v2.3.0 新增）

从调研来源构建实体关系网络：
1. 节点：实体（146 词典 + 运行时别名识别）
2. 边：共现边（同一来源/段落出现 → 加权边）
3. 输出：neighbors 查询 + Graphviz dot 导出

CLI:
  python -m core.entity_graph build --sources ...  (开发用)
  python -m core.entity_graph demo                    (示例)
"""

import sys
from pathlib import Path
from typing import List, Dict, Optional

CORE_DIR = Path(__file__).parent
sys.path.insert(0, str(CORE_DIR))

# v2.5.0 G3: 跨 research 图谱累积（P2-1 召回深化）
# 每次 research 构建后 set_global_graph 注册，后续 query expansion 复用邻居
_GLOBAL_GRAPH: Optional['EntityGraph'] = None


def set_global_graph(graph: 'EntityGraph') -> None:
    """注册当前会话图谱（跨 research 累积，供召回扩展复用）"""
    global _GLOBAL_GRAPH
    _GLOBAL_GRAPH = graph


def get_global_graph() -> Optional['EntityGraph']:
    """获取会话图谱（无 → None，调用方自行回退）"""
    return _GLOBAL_GRAPH


def reset_global_graph() -> None:
    """清空会话图谱（测试隔离用）"""
    global _GLOBAL_GRAPH
    _GLOBAL_GRAPH = None


class EntityGraph:
    """v2.3.0 实体关系图谱"""

    def __init__(self):
        self.nodes: Dict[str, dict] = {}   # name -> {name, type, hit}
        self.edges: Dict[tuple, dict] = {} # (a,b) -> {source, weight, count, sources: []}

    def _normalize_pair(self, a: str, b: str) -> tuple:
        """边键归一化（无序对）"""
        return tuple(sorted([a, b]))

    def build_from_sources(self, sources: List[Dict]) -> dict:
        """从来源列表构建图谱

        参数:
            sources: [{'title', 'snippet'|'text', 'url'}, ...]

        返回:
            {'nodes': N, 'edges': M, 'top_relations': [...]}

        v2.4.3 PATCH (P1-A): 用 Counter 预统计 + combinations 替代双重 for 循环，
        实测 100 源 159ms → ~50ms（3x 提速）。权重改用 Jaccard 归一化
        (count / 该对中低频实体的源数) 让低频实体边权更高、信息量更大。
        """
        from ner import extract_entities_cached as extract_entities
        from collections import Counter
        from itertools import combinations

        # 第 1 遍：每源实体去重 + 节点计数 + 全局实体源数统计
        src_entities = []  # 每源去重后的实体名列表
        entity_source_count: Counter = Counter()  # 实体在多少源中出现

        for src in sources:
            text = ' '.join([
                src.get('text', '') or src.get('snippet', '') or src.get('title', ''),
                src.get('title', ''),
            ])
            if not text.strip():
                continue
            entities = extract_entities(text)
            names = []
            seen_in_src = set()
            for e in entities:
                name = e['entity_name']
                if name not in self.nodes:
                    self.nodes[name] = {
                        'name': name,
                        'type': e.get('entity_type', 'UNKNOWN'),
                        'hit': 0,
                    }
                self.nodes[name]['hit'] += 1
                if name not in seen_in_src:
                    names.append(name)
                    seen_in_src.add(name)
                    entity_source_count[name] += 1
            src_entities.append((src, names))

        # 第 2 遍：组合式建边（O(n²) 但数据量已显著缩小）
        for src, names in src_entities:
            for a, b in combinations(names, 2):
                pair = self._normalize_pair(a, b)
                if pair not in self.edges:
                    self.edges[pair] = {
                        'source': pair,
                        'weight': 0.0,
                        'count': 0,
                        'sources': [],
                    }
                self.edges[pair]['count'] += 1
                url = src.get('url', '')
                if url and url not in self.edges[pair]['sources']:
                    self.edges[pair]['sources'].append(url)

        # 权重归一化：v2.4.3 PATCH (P1-A) 改用 Jaccard 加权
        # 原算法：count / total_sources（高频实体对权重虚高）
        # 新算法：count / min(freq_a, freq_b)（低频实体对权重更突出）
        for pair, edge in self.edges.items():
            a, b = pair
            freq_min = max(min(entity_source_count[a], entity_source_count[b]), 1)
            edge['weight'] = round(edge['count'] / freq_min, 3)

        top = sorted(self.edges.values(), key=lambda x: -x['count'])[:10]
        top_relations = [{
            'entity_a': pair[0],
            'entity_b': pair[1],
            'co_occurrence': e['count'],
            'weight': e['weight'],
        } for pair, e in [(x['source'], x) for x in top]]

        return {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'top_relations': top_relations,
        }

    def get_neighbors(self, entity: str, top_n: int = 10) -> List[Dict]:
        """某实体的关联实体（按共现次数排序）"""
        result = []
        for pair, edge in self.edges.items():
            if entity in pair:
                other = pair[0] if pair[1] == entity else pair[1]
                result.append({
                    'entity_name': other,
                    'co_occurrence': edge['count'],
                    'weight': edge['weight'],
                })
        result.sort(key=lambda x: -x['co_occurrence'])
        return result[:top_n]

    def export_dot(self) -> str:
        """Graphviz dot 导出"""
        lines = ['digraph EntityGraph {', '  rankdir=LR;']
        for name, node in self.nodes.items():
            safe_name = name.replace('"', '\\"')
            lines.append(f'  "{safe_name}" [label="{safe_name}", shape=box, '
                         f'style="rounded,filled", fillcolor="#e8f4fd"];')
        for pair, edge in self.edges.items():
            a, b = pair[0].replace('"', '\\"'), pair[1].replace('"', '\\"')
            lines.append(f'  "{a}" -> "{b}" [label="{edge["count"]}", penwidth={min(edge["count"], 5)}];')
        lines.append('}')
        return '\n'.join(lines)

    def to_dict(self) -> dict:
        """完整序列化（供 research() 附带）"""
        return {
            'nodes': len(self.nodes),
            'edges': len(self.edges),
            'top_relations': sorted(
                [{
                    'entity_a': pair[0],
                    'entity_b': pair[1],
                    'co_occurrence': e['count'],
                    'weight': e['weight'],
                } for pair, e in self.edges.items()],
                key=lambda x: -x['co_occurrence'],
            )[:10],
        }

    def clear(self):
        self.nodes.clear()
        self.edges.clear()


# v2.6.2 PATCH: 真异步版 build_from_sources（避免 asyncio.to_thread 占 executor 槽位）
async def build_from_sources_async(sources: List[Dict]) -> dict:
    """v2.6.2 新增：entity_graph 真异步版本

    NER 提取走 asyncio.to_thread（CPU 密集），但每个源的 NER 并发（gather），
    比 v2.5.x async_research 内部串行 asyncio.to_thread 更高效。
    """
    import asyncio
    from ner import extract_entities
    from collections import Counter
    from itertools import combinations

    loop = asyncio.get_event_loop()
    # 第一遍：并发 NER
    texts = []
    for src in sources:
        text = ' '.join([
            src.get('text', '') or src.get('snippet', '') or src.get('title', ''),
            src.get('title', ''),
        ])
        texts.append(text if text.strip() else ' ')

    # v2.7.1 PATCH: chunked gather 优化（避免单源独立 task 启动开销 > 收益）
    # v2.6.2 实现：20 源独立 gather → 10138ms（每个 NER ~500ms executor 启动）
    # v2.7.1 优化：每 5 源一个 chunk，4 chunks × 5 并发 = 2000ms（节省 5x）
    BATCH_SIZE = 5  # v2.7.1 测试验证最佳值
    per_src_entities = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i:i + BATCH_SIZE]
        batch_tasks = [loop.run_in_executor(None, extract_entities, t) for t in batch]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        per_src_entities.extend(batch_results)

    # 第二遍：建图
    g = EntityGraph()
    entity_source_count: Counter = Counter()
    src_entities_list = []

    for src, entities in zip(sources, per_src_entities):
        if isinstance(entities, Exception):
            continue
        names = []
        seen = set()
        for e in entities:
            name = e['entity_name']
            if name not in g.nodes:
                g.nodes[name] = {
                    'name': name,
                    'type': e.get('entity_type', 'UNKNOWN'),
                    'hit': 0,
                }
            g.nodes[name]['hit'] += 1
            if name not in seen:
                names.append(name)
                seen.add(name)
                entity_source_count[name] += 1
        src_entities_list.append((src, names))

    for src, names in src_entities_list:
        for a, b in combinations(names, 2):
            pair = tuple(sorted([a, b]))
            if pair not in g.edges:
                g.edges[pair] = {'source': pair, 'weight': 0.0, 'count': 0, 'sources': []}
            g.edges[pair]['count'] += 1
            url = src.get('url', '')
            if url and url not in g.edges[pair]['sources']:
                g.edges[pair]['sources'].append(url)

    for pair, edge in g.edges.items():
        a, b = pair
        freq_min = max(min(entity_source_count[a], entity_source_count[b]), 1)
        edge['weight'] = round(edge['count'] / freq_min, 3)

    top = sorted(g.edges.values(), key=lambda x: -x['count'])[:10]
    top_relations = [{
        'entity_a': pair[0], 'entity_b': pair[1],
        'co_occurrence': e['count'], 'weight': e['weight'],
    } for pair, e in [(x['source'], x) for x in top]]

    set_global_graph(g)  # v2.5.0 G3: 注册全局图谱，供后续 query expansion 复用

    return {
        'nodes': len(g.nodes),
        'edges': len(g.edges),
        'top_relations': top_relations,
    }


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'demo'
    g = EntityGraph()

    if cmd == 'demo':
        sources = [
            {'title': 'OpenAI 与 Microsoft 合作', 'snippet': 'OpenAI 部署在 Azure 云上', 'url': 'https://e.com/1'},
            {'title': '宁德时代与比亚迪竞争', 'snippet': '宁德时代 CATL 电池与比亚迪刀片电池', 'url': 'https://e.com/2'},
            {'title': 'Anthropic 与 Claude', 'snippet': 'Anthropic 的 Claude 3.5 对比 GPT-4o', 'url': 'https://e.com/3'},
        ]
        result = g.build_from_sources(sources)
        print(f"图谱: {result}")
        print("\nTop 关系:")
        for r in result['top_relations']:
            print(f"  {r['entity_a']} ↔ {r['entity_b']} (共现 {r['co_occurrence']})")
        print("\n邻居示例 OpenAI:", g.get_neighbors('OpenAI'))
        print("\nDOT:")
        print(g.export_dot()[:300])
    else:
        print(f"未知命令: {cmd}")


if __name__ == '__main__':
    main()
