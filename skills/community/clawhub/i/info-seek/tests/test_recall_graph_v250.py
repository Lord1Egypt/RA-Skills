#!/usr/bin/env python3
"""
tests/test_recall_graph_v250.py — 图谱邻域召回回归（P2-1 G3 修复，v2.5.0）

覆盖：
- R1 EntityGraph 全局注册（set/get/reset，跨 research 累积语义）
- R2 _expand_query 图谱邻域词进入（env INFOSEEK_RECALL_GRAPH=1 默认开）
- R3 冷启动无图谱 → 纯别名扩展（零行为变化）
- R4 INFOSEEK_RECALL_GRAPH=0 → 关闭图谱扩展
- R5 词边界补全（P3 漏网）：'PE' 不误命中 'OpenAI'（子串 'pe'⊂'openai'）
- R6 build_from_sources_async 构建后自动注册全局图谱
"""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

os.environ['INFOSEEK_DATA_DIR'] = tempfile.mkdtemp(prefix='infoseek_graph_')
os.environ.pop('INFOSEEK_RECALL_GRAPH', None)

# 统一走顶层导入（与 infoseek_pipeline 图谱分支 / infoseek_core_v2 注册端一致，
# 避免 core.entity_graph 双模块状态分裂）
from entity_graph import (  # noqa: E402
    EntityGraph, set_global_graph, get_global_graph, reset_global_graph,
)
from entity_graph import build_from_sources_async  # noqa: E402

_fails = []


def _check(name, cond, detail=''):
    if cond:
        print(f"  [PASS] {name}")
    else:
        _fails.append(name)
        print(f"  [FAIL] {name} {detail}")


_SOURCES = [
    {"title": "A", "text": "OpenAI 与 NVIDIA 合作训练新模型，推理成本下降"},
    {"title": "B", "text": "OpenAI 的 GPU 来自 NVIDIA，算力租赁价格波动"},
    {"title": "C", "text": "OpenAI 发布新 API，开发者数量增长"},
]


def _make_graph():
    g = EntityGraph()
    g.build_from_sources(_SOURCES)
    return g


def main():
    # R1 全局注册
    print('--- R1 全局注册 ---')
    reset_global_graph()
    _check('初始为 None', get_global_graph() is None)
    g = _make_graph()
    set_global_graph(g)
    _check('set 后可取回', get_global_graph() is g)
    _check('图谱有边', len(g.edges) >= 1, f'edges={len(g.edges)}')
    reset_global_graph()
    _check('reset 后 None', get_global_graph() is None)

    # R2 图谱邻域进入 query
    print('--- R2 图谱邻域召回 ---')
    import infoseek_pipeline as P
    set_global_graph(_make_graph())
    q = P._expand_query('OpenAI')
    _check('邻居 NVIDIA 进 query', 'NVIDIA' in q, q)
    _check('邻域不引入 PE 别名', '市盈率' not in q, q)

    # R3 冷启动
    print('--- R3 冷启动 ---')
    reset_global_graph()
    q2 = P._expand_query('OpenAI')
    _check('无图谱 → 无邻居', 'NVIDIA' not in q2, q2)
    _check('别名仍扩展', 'OpenAI Inc.' in q2 or 'open ai' in q2, q2)

    # R4 关闭开关
    print('--- R4 开关关闭 ---')
    set_global_graph(_make_graph())
    os.environ['INFOSEEK_RECALL_GRAPH'] = '0'
    q3 = P._expand_query('OpenAI')
    _check('关闭后无邻居', 'NVIDIA' not in q3, q3)
    os.environ.pop('INFOSEEK_RECALL_GRAPH', None)

    # R5 词边界补全（P3 漏网）
    print('--- R5 词边界补全 ---')
    q_pe = P._expand_query('PE')
    _check("'PE' 扩展出市盈率", '市盈率' in q_pe, q_pe)
    _check("'PE' 不误命中 OpenAI", 'openai' not in q_pe.lower(), q_pe)

    # R6 async 构建自动注册
    print('--- R6 async 自动注册 ---')
    reset_global_graph()
    import asyncio
    asyncio.run(build_from_sources_async(_SOURCES))
    _check('async 构建后已注册', get_global_graph() is not None)
    q4 = P._expand_query('OpenAI')
    _check('async 注册后邻居可召回', 'NVIDIA' in q4, q4)

    reset_global_graph()
    print()
    if _fails:
        print(f"FAIL: {len(_fails)} 项失败 → {_fails}")
        sys.exit(1)
    print("ALL PASS (test_recall_graph_v250) ✅")
    sys.exit(0)


if __name__ == '__main__':
    main()