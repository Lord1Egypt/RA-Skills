#!/usr/bin/env python3
"""
HNSW (Hierarchical Navigable Small World) 索引
真正的O(log n)近似最近邻检索算法

基于论文: "Efficient and robust approximate nearest neighbor search using 
Hierarchical Navigable Small World graphs" by Malkov & Yashunin (2018)

核心思想:
- 多层图结构，上层稀疏，下层密集
- 从顶层开始贪婪搜索，逐层下降
- 复杂度: O(log n) 检索, O(n log n) 构建
"""

import json
import math
import random
import heapq
import pickle
import os
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class HNSWNode:
    """HNSW节点"""
    id: str
    vector: List[float]
    level: int
    neighbors: Dict[int, Set[str]] = field(default_factory=dict)  # level -> neighbor_ids
    
    def __post_init__(self):
        if not self.neighbors:
            self.neighbors = {}


class HNSWIndex:
    """
    HNSW索引 - 真正的O(log n)近似最近邻搜索
    
    参数:
        M: 每层最大连接数 (default: 16)
        ef_construction: 构建时的搜索宽度 (default: 200)
        ef_search: 搜索时的搜索宽度 (default: 50)
        mL: 层级因子 (default: 1/ln(M))
    """
    
    def __init__(self, dim: int = 128, M: int = 16, 
                 ef_construction: int = 200, ef_search: int = 50,
                 mL: float = None):
        self.dim = dim
        self.M = M
        self.M_max = M
        self.M_max0 = M * 2  # 第0层连接数翻倍
        self.ef_construction = ef_construction
        self.ef_search = ef_search
        self.mL = mL if mL else 1.0 / math.log(M)
        
        self.nodes: Dict[str, HNSWNode] = {}
        self.entry_point: Optional[str] = None
        self.max_level: int = -1
        
        # 统计信息
        self.stats = {
            'total_nodes': 0,
            'total_searches': 0,
            'avg_search_steps': 0,
            'total_insertions': 0
        }
    
    def _distance(self, v1: List[float], v2: List[float]) -> float:
        """计算余弦距离（1 - 余弦相似度）"""
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        
        if norm1 == 0 or norm2 == 0:
            return 1.0
        
        similarity = dot_product / (norm1 * norm2)
        return 1.0 - similarity
    
    def _random_level(self) -> int:
        """随机生成节点层级（指数分布）"""
        r = random.random()
        level = int(-math.log(r) * self.mL)
        return level
    
    def _search_layer(self, query: List[float], entry_points: Set[str], 
                      ef: int, level: int) -> List[Tuple[float, str]]:
        """
        在指定层搜索最近的ef个节点
        
        返回: [(distance, node_id), ...] 按距离排序
        """
        visited = set(entry_points)
        
        # 候选集（最小堆）
        candidates = []
        for ep in entry_points:
            if ep in self.nodes:
                dist = self._distance(query, self.nodes[ep].vector)
                heapq.heappush(candidates, (dist, ep))
        
        # 结果集（最大堆，存储最近的ef个）
        results = []
        for ep in entry_points:
            if ep in self.nodes:
                dist = self._distance(query, self.nodes[ep].vector)
                heapq.heappush(results, (-dist, ep))  # 负数使其成为最大堆
        
        steps = 0
        while candidates:
            steps += 1
            dist_c, c_id = heapq.heappop(candidates)
            
            # 获取当前最远结果
            if results:
                dist_f = -results[0][0]
                if dist_c > dist_f:
                    break
            
            # 遍历邻居
            if c_id in self.nodes:
                node = self.nodes[c_id]
                neighbors = node.neighbors.get(level, set())
                
                for n_id in neighbors:
                    if n_id not in visited:
                        visited.add(n_id)
                        
                        if n_id in self.nodes:
                            dist_n = self._distance(query, self.nodes[n_id].vector)
                            
                            # 检查是否应该加入结果
                            if len(results) < ef:
                                heapq.heappush(candidates, (dist_n, n_id))
                                heapq.heappush(results, (-dist_n, n_id))
                            elif dist_n < -results[0][0]:
                                heapq.heappop(results)
                                heapq.heappush(candidates, (dist_n, n_id))
                                heapq.heappush(results, (-dist_n, n_id))
        
        # 转换为排序后的列表
        result_list = [(-dist, node_id) for dist, node_id in results]
        result_list.sort()
        
        return result_list, steps
    
    def _select_neighbors_simple(self, candidates: List[Tuple[float, str]], 
                                  M: int) -> List[str]:
        """简单选择：直接取最近的M个"""
        candidates.sort()
        return [node_id for _, node_id in candidates[:M]]
    
    def _select_neighbors_heuristic(self, query: List[float],
                                     candidates: List[Tuple[float, str]], 
                                     M: int) -> List[str]:
        """
        启发式邻居选择：考虑多样性，避免聚集
        """
        if len(candidates) <= M:
            return [node_id for _, node_id in candidates]
        
        candidates.sort()
        selected = []
        
        for dist, node_id in candidates:
            if len(selected) >= M:
                break
            
            # 检查是否与已选节点过于接近
            should_add = True
            node_vec = self.nodes[node_id].vector
            
            for s_id in selected:
                s_vec = self.nodes[s_id].vector
                if self._distance(node_vec, s_vec) < dist:
                    should_add = False
                    break
            
            if should_add:
                selected.append(node_id)
        
        # 如果启发式选择不足，补充最近的
        while len(selected) < M:
            for dist, node_id in candidates:
                if node_id not in selected:
                    selected.append(node_id)
                    break
        
        return selected[:M]
    
    def insert(self, node_id: str, vector: List[float]) -> None:
        """插入新节点"""
        if len(vector) != self.dim:
            raise ValueError(f"向量维度不匹配: 期望{self.dim}, 实际{len(vector)}")
        
        # 如果节点已存在，先删除
        if node_id in self.nodes:
            self._delete_node(node_id)
        
        # 随机分配层级
        level = self._random_level()
        node = HNSWNode(id=node_id, vector=vector, level=level)
        self.nodes[node_id] = node
        
        # 如果是第一个节点
        if self.entry_point is None:
            self.entry_point = node_id
            self.max_level = level
            self.stats['total_nodes'] += 1
            self.stats['total_insertions'] += 1
            return
        
        # 从入口点开始搜索
        curr_entry = self.entry_point
        
        # 从顶层向下搜索到level+1层
        for lc in range(self.max_level, level, -1):
            results, _ = self._search_layer(vector, {curr_entry}, ef=1, level=lc)
            if results:
                curr_entry = results[0][1]
        
        # 从level层向下插入
        for lc in range(min(level, self.max_level), -1, -1):
            results, _ = self._search_layer(vector, {curr_entry}, 
                                            ef=self.ef_construction, level=lc)
            
            # 选择邻居
            M_max = self.M_max0 if lc == 0 else self.M_max
            neighbors = self._select_neighbors_heuristic(vector, results, M_max)
            
            # 设置邻居
            node.neighbors[lc] = set(neighbors)
            
            # 双向连接
            for n_id in neighbors:
                if n_id in self.nodes:
                    neighbor = self.nodes[n_id]
                    if lc not in neighbor.neighbors:
                        neighbor.neighbors[lc] = set()
                    neighbor.neighbors[lc].add(node_id)
                    
                    # 如果邻居连接数超限，裁剪
                    M_max_n = self.M_max0 if lc == 0 else self.M_max
                    if len(neighbor.neighbors[lc]) > M_max_n:
                        # 重新选择邻居
                        candidates = [(self._distance(neighbor.vector, 
                                    self.nodes[n].vector), n) 
                                    for n in neighbor.neighbors[lc] if n in self.nodes]
                        new_neighbors = self._select_neighbors_heuristic(
                            neighbor.vector, candidates, M_max_n)
                        neighbor.neighbors[lc] = set(new_neighbors)
        
        # 更新入口点
        if level > self.max_level:
            self.entry_point = node_id
            self.max_level = level
        
        self.stats['total_nodes'] += 1
        self.stats['total_insertions'] += 1
    
    def _delete_node(self, node_id: str) -> None:
        """删除节点（内部使用）"""
        if node_id not in self.nodes:
            return
        
        node = self.nodes[node_id]
        
        # 移除所有连接
        for level, neighbors in node.neighbors.items():
            for n_id in neighbors:
                if n_id in self.nodes:
                    neighbor = self.nodes[n_id]
                    if level in neighbor.neighbors:
                        neighbor.neighbors[level].discard(node_id)
        
        del self.nodes[node_id]
        self.stats['total_nodes'] -= 1
    
    def search(self, query: List[float], k: int = 10) -> List[Tuple[str, float, float]]:
        """
        搜索k个最近邻
        
        返回: [(node_id, distance, similarity), ...]
        """
        if len(query) != self.dim:
            raise ValueError(f"向量维度不匹配: 期望{self.dim}, 实际{len(query)}")
        
        if self.entry_point is None:
            return []
        
        total_steps = 0
        
        # 从顶层向下搜索
        curr_entry = self.entry_point
        for lc in range(self.max_level, 0, -1):
            results, steps = self._search_layer(query, {curr_entry}, ef=1, level=lc)
            total_steps += steps
            if results:
                curr_entry = results[0][1]
        
        # 在第0层进行详细搜索
        results, steps = self._search_layer(query, {curr_entry}, 
                                           ef=self.ef_search, level=0)
        total_steps += steps
        
        # 更新统计
        self.stats['total_searches'] += 1
        avg_steps = (self.stats['avg_search_steps'] * (self.stats['total_searches'] - 1) 
                    + total_steps) / self.stats['total_searches']
        self.stats['avg_search_steps'] = avg_steps
        
        # 返回top-k结果
        results = results[:k]
        return [(node_id, dist, 1.0 - dist) for dist, node_id in results]
    
    def get_neighbors(self, node_id: str, level: int = 0) -> Set[str]:
        """获取节点的邻居"""
        if node_id not in self.nodes:
            return set()
        return self.nodes[node_id].neighbors.get(level, set())
    
    def get_node_level(self, node_id: str) -> int:
        """获取节点层级"""
        if node_id not in self.nodes:
            return -1
        return self.nodes[node_id].level
    
    def get_stats(self) -> Dict:
        """获取统计信息"""
        level_dist = defaultdict(int)
        for node in self.nodes.values():
            level_dist[node.level] += 1
        
        avg_connections = 0
        if self.nodes:
            total_connections = sum(
                len(n.neighbors.get(0, set())) for n in self.nodes.values()
            )
            avg_connections = total_connections / len(self.nodes)
        
        return {
            **self.stats,
            'max_level': self.max_level,
            'entry_point': self.entry_point,
            'level_distribution': dict(level_dist),
            'avg_connections_per_node': round(avg_connections, 2),
            'theoretical_complexity': f'O(log n) ≈ O({math.log2(max(1, self.stats["total_nodes"])):.2f})'
        }
    
    def save(self, filepath: str) -> None:
        """保存索引"""
        data = {
            'dim': self.dim,
            'M': self.M,
            'ef_construction': self.ef_construction,
            'ef_search': self.ef_search,
            'mL': self.mL,
            'entry_point': self.entry_point,
            'max_level': self.max_level,
            'stats': self.stats,
            'nodes': {}
        }
        
        for node_id, node in self.nodes.items():
            data['nodes'][node_id] = {
                'id': node.id,
                'vector': node.vector,
                'level': node.level,
                'neighbors': {str(k): list(v) for k, v in node.neighbors.items()}
            }
        
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load(self, filepath: str) -> None:
        """加载索引"""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.dim = data['dim']
        self.M = data['M']
        self.ef_construction = data['ef_construction']
        self.ef_search = data['ef_search']
        self.mL = data['mL']
        self.entry_point = data['entry_point']
        self.max_level = data['max_level']
        self.stats = data['stats']
        
        self.nodes = {}
        for node_id, node_data in data['nodes'].items():
            node = HNSWNode(
                id=node_data['id'],
                vector=node_data['vector'],
                level=node_data['level'],
                neighbors={int(k): set(v) for k, v in node_data['neighbors'].items()}
            )
            self.nodes[node_id] = node


def demo_hnsw():
    """演示HNSW索引"""
    import time
    
    print("=" * 60)
    print("HNSW索引演示 - 真正的O(log n)近似最近邻搜索")
    print("=" * 60)
    
    # 创建索引
    dim = 128
    index = HNSWIndex(dim=dim, M=16, ef_construction=200, ef_search=50)
    
    # 生成随机向量
    n = 10000
    print(f"\n插入 {n} 个向量...")
    
    start = time.time()
    for i in range(n):
        vector = [random.gauss(0, 1) for _ in range(dim)]
        # 归一化
        norm = math.sqrt(sum(v * v for v in vector))
        vector = [v / norm for v in vector]
        index.insert(f"node_{i}", vector)
    
    insert_time = time.time() - start
    print(f"插入完成: {insert_time:.2f}秒, 平均 {(insert_time/n)*1000:.3f}毫秒/个")
    
    # 搜索测试
    print(f"\n搜索测试...")
    query = [random.gauss(0, 1) for _ in range(dim)]
    norm = math.sqrt(sum(v * v for v in query))
    query = [v / norm for v in query]
    
    start = time.time()
    for _ in range(100):
        results = index.search(query, k=10)
    search_time = (time.time() - start) / 100
    
    print(f"搜索完成: 平均 {search_time*1000:.3f}毫秒")
    
    # 统计信息
    stats = index.get_stats()
    print(f"\n索引统计:")
    print(f"  总节点数: {stats['total_nodes']}")
    print(f"  最大层级: {stats['max_level']}")
    print(f"  平均连接数: {stats['avg_connections_per_node']}")
    print(f"  平均搜索步数: {stats['avg_search_steps']:.2f}")
    print(f"  理论复杂度: {stats['theoretical_complexity']}")
    
    # 显示搜索结果
    print(f"\nTop 5 搜索结果:")
    for node_id, dist, sim in results[:5]:
        print(f"  {node_id}: 距离={dist:.4f}, 相似度={sim:.4f}")


if __name__ == "__main__":
    demo_hnsw()
