"""
path-dispatch: Discrete Hamiltonian task dispatcher with hypergraph support.

Exposes core functions for parsing, graph building, shortest paths, and queries.
"""

from .dispatch import (
    # 解析
    parse_triples,
    parse_list,
    smart_split,          # 可选，供高级用户
    # 图构建
    build_graph,
    # 预计算（新版：全源最短路径）
    all_pairs_shortest_paths,
    # 查询
    next_hops,
    bfs_shortest_path,
    # 命令处理（供 CLI 复用）
    cmd_path,
    cmd_query,
    cmd_deps,
    cmd_matrix,
)

# 版本信息
__version__ = "1.0.1"
__author__ = "RoseHammer"

# 公开 API 列表（只列稳定接口）
__all__ = [
    "parse_triples",
    "parse_list",
    "build_graph",
    "all_pairs_shortest_paths",
    "next_hops",
    "bfs_shortest_path",
    "cmd_path",
    "cmd_query",
    "cmd_deps",
    "cmd_matrix",
]