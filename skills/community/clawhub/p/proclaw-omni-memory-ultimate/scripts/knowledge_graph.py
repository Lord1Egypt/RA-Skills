#!/usr/bin/env python3
"""
Knowledge Graph - 记忆关联网络
自动发现记忆间的关联关系，构建知识图谱
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime
from typing import List, Dict, Any, Set, Tuple
from collections import defaultdict
import re

# 路径配置
WORKSPACE_ROOT = os.getcwd()
MEMORY_DIR = os.path.join(WORKSPACE_ROOT, "memory")
GRAPH_PATH = os.path.join(MEMORY_DIR, "knowledge_graph.json")

# 关联类型
RELATION_TYPES = {
    "related_to": "相关",
    "causes": "导致",
    "contradicts": "矛盾",
    "supports": "支持",
    "extends": "扩展",
    "supersedes": "替代"
}

# 关联发现阈值
SIMILARITY_THRESHOLD = 0.7
KEYWORD_OVERLAP_MIN = 3


class KnowledgeGraph:
    """记忆知识图谱"""
    
    def __init__(self):
        self.nodes: Dict[str, Dict] = {}  # id -> node
        self.edges: List[Dict] = []        # [{source, target, type, weight}]
        self.keyword_index: Dict[str, Set[str]] = defaultdict(set)  # keyword -> memory_ids
        
        self._load_graph()
    
    def _load_graph(self):
        """加载已有图谱"""
        if os.path.exists(GRAPH_PATH):
            try:
                with open(GRAPH_PATH, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.nodes = data.get('nodes', {})
                    self.edges = data.get('edges', [])
                    # 重建关键词索引
                    for node_id, node in self.nodes.items():
                        for kw in node.get('keywords', []):
                            self.keyword_index[kw].add(node_id)
            except Exception as e:
                print(f"[WARN] Failed to load graph: {e}")
    
    def _save_graph(self):
        """保存图谱"""
        os.makedirs(os.path.dirname(GRAPH_PATH), exist_ok=True)
        with open(GRAPH_PATH, 'w', encoding='utf-8') as f:
            json.dump({
                'nodes': self.nodes,
                'edges': self.edges,
                'updated_at': datetime.now().isoformat()
            }, f, ensure_ascii=False, indent=2)
    
    def add_node(self, memory_id: str, content: str, 
                 memory_type: str, keywords: List[str],
                 metadata: Dict = None) -> bool:
        """
        添加记忆节点
        
        Args:
            memory_id: 记忆ID
            content: 记忆内容
            memory_type: 记忆类型
            keywords: 关键词列表
            metadata: 额外元数据
        
        Returns:
            是否新增
        """
        if memory_id in self.nodes:
            # 更新现有节点
            self.nodes[memory_id]['keywords'] = keywords
            self.nodes[memory_id]['updated_at'] = datetime.now().isoformat()
        else:
            # 新增节点
            self.nodes[memory_id] = {
                'id': memory_id,
                'content': content,
                'type': memory_type,
                'keywords': keywords,
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat(),
                'metadata': metadata or {}
            }
            
            # 更新关键词索引
            for kw in keywords:
                self.keyword_index[kw].add(memory_id)
        
        return True
    
    def discover_relations(self, memory_id: str, content: str, 
                          keywords: List[str]) -> List[Dict]:
        """
        发现记忆关联
        
        策略：
        1. 关键词重叠发现相关记忆
        2. 类型关联规则
        3. 时间序列关联
        
        Returns:
            发现的关联列表
        """
        discovered = []
        
        # 1. 关键词重叠发现
        candidate_ids = set()
        for kw in keywords:
            candidate_ids.update(self.keyword_index.get(kw, set()))
        
        # 移除自己
        candidate_ids.discard(memory_id)
        
        for candidate_id in candidate_ids:
            candidate = self.nodes.get(candidate_id)
            if not candidate:
                continue
            
            # 计算关键词重叠度
            candidate_kws = set(candidate.get('keywords', []))
            overlap = len(set(keywords) & candidate_kws)
            union = len(set(keywords) | candidate_kws)
            jaccard = overlap / union if union > 0 else 0
            
            if overlap >= KEYWORD_OVERLAP_MIN or jaccard > SIMILARITY_THRESHOLD:
                relation = {
                    'source': memory_id,
                    'target': candidate_id,
                    'type': 'related_to',
                    'weight': jaccard,
                    'discovered_by': 'keyword_overlap',
                    'discovered_at': datetime.now().isoformat()
                }
                discovered.append(relation)
        
        # 2. 类型关联规则
        # user类型 → 相关project决策
        # feedback类型 → 相关user偏好
        type_rules = {
            ('user', 'project'): 'influences',
            ('feedback', 'user'): 'corrects',
            ('project', 'reference'): 'uses',
        }
        
        for (src_type, tgt_type), rel_type in type_rules.items():
            # 找到符合类型的目标
            for nid, node in self.nodes.items():
                if nid == memory_id:
                    continue
                if node.get('type') == tgt_type:
                    # 检查是否有共同关键词
                    if set(keywords) & set(node.get('keywords', [])):
                        relation = {
                            'source': memory_id,
                            'target': nid,
                            'type': rel_type,
                            'weight': 0.5,
                            'discovered_by': 'type_rule',
                            'discovered_at': datetime.now().isoformat()
                        }
                        discovered.append(relation)
        
        return discovered
    
    def add_edge(self, source: str, target: str, 
                 relation_type: str, weight: float = 1.0,
                 metadata: Dict = None) -> bool:
        """
        添加关联边
        
        Args:
            source: 源节点ID
            target: 目标节点ID
            relation_type: 关联类型
            weight: 权重
            metadata: 额外元数据
        
        Returns:
            是否成功
        """
        if source not in self.nodes or target not in self.nodes:
            return False
        
        # 检查是否已存在
        for edge in self.edges:
            if (edge['source'] == source and edge['target'] == target) or \
               (edge['source'] == target and edge['target'] == source):
                # 更新权重
                edge['weight'] = max(edge['weight'], weight)
                edge['updated_at'] = datetime.now().isoformat()
                return True
        
        # 新增边
        self.edges.append({
            'source': source,
            'target': target,
            'type': relation_type,
            'weight': weight,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'metadata': metadata or {}
        })
        
        return True
    
    def get_related_memories(self, memory_id: str, 
                             max_depth: int = 2) -> List[Dict]:
        """
        获取关联记忆（BFS遍历）
        
        Args:
            memory_id: 起始记忆ID
            max_depth: 最大遍历深度
        
        Returns:
            关联记忆列表
        """
        if memory_id not in self.nodes:
            return []
        
        visited = {memory_id}
        result = []
        queue = [(memory_id, 0)]
        
        while queue:
            current_id, depth = queue.pop(0)
            
            if depth >= max_depth:
                continue
            
            # 找到所有相邻节点
            for edge in self.edges:
                neighbor = None
                if edge['source'] == current_id:
                    neighbor = edge['target']
                elif edge['target'] == current_id:
                    neighbor = edge['source']
                
                if neighbor and neighbor not in visited:
                    visited.add(neighbor)
                    node = self.nodes.get(neighbor)
                    if node:
                        result.append({
                            'memory': node,
                            'relation': edge['type'],
                            'distance': depth + 1,
                            'weight': edge['weight']
                        })
                        queue.append((neighbor, depth + 1))
        
        # 按距离和权重排序
        result.sort(key=lambda x: (x['distance'], -x['weight']))
        return result
    
    def get_memory_clusters(self) -> List[Dict]:
        """
        发现记忆簇（社群发现）
        使用简单的连通分量算法
        
        Returns:
            记忆簇列表
        """
        # 构建邻接表
        adj = defaultdict(set)
        for edge in self.edges:
            adj[edge['source']].add(edge['target'])
            adj[edge['target']].add(edge['source'])
        
        # 找连通分量
        visited = set()
        clusters = []
        
        for node_id in self.nodes:
            if node_id in visited:
                continue
            
            # BFS找连通分量
            cluster = []
            queue = [node_id]
            
            while queue:
                current = queue.pop(0)
                if current in visited:
                    continue
                visited.add(current)
                cluster.append(current)
                
                for neighbor in adj[current]:
                    if neighbor not in visited:
                        queue.append(neighbor)
            
            if len(cluster) > 1:  # 只保留有连接的簇
                clusters.append({
                    'members': cluster,
                    'size': len(cluster),
                    'types': [self.nodes[nid]['type'] for nid in cluster]
                })
        
        # 按大小排序
        clusters.sort(key=lambda x: -x['size'])
        return clusters
    
    def get_node_stats(self) -> Dict:
        """获取节点统计"""
        type_counts = defaultdict(int)
        for node in self.nodes.values():
            type_counts[node.get('type', 'unknown')] += 1
        
        return {
            'total_nodes': len(self.nodes),
            'total_edges': len(self.edges),
            'by_type': dict(type_counts),
            'clusters': len(self.get_memory_clusters()),
            'avg_connections': len(self.edges) * 2 / len(self.nodes) if self.nodes else 0
        }
    
    def find_path(self, source: str, target: str) -> List[List[str]]:
        """
        找到两个记忆间的路径
        
        Args:
            source: 起点
            target: 终点
        
        Returns:
            路径列表（可能多条）
        """
        if source not in self.nodes or target not in self.nodes:
            return []
        
        # BFS找最短路径
        visited = {source}
        paths = [[source]]
        result = []
        max_paths = 3
        
        while paths and len(result) < max_paths:
            new_paths = []
            for path in paths:
                current = path[-1]
                
                for edge in self.edges:
                    neighbor = None
                    if edge['source'] == current:
                        neighbor = edge['target']
                    elif edge['target'] == current:
                        neighbor = edge['source']
                    
                    if neighbor and neighbor not in path:
                        new_path = path + [neighbor]
                        if neighbor == target:
                            result.append(new_path)
                        else:
                            new_paths.append(new_path)
            
            paths = new_paths
        
        return result
    
    def save(self):
        """保存图谱"""
        self._save_graph()


def extract_keywords(content: str) -> List[str]:
    """
    提取关键词（简化版）
    实际使用可接入NLP工具
    """
    # 简单的关键词提取：去除停用词，提取名词短语
    stopwords = {'的', '是', '在', '和', '了', '有', '不', '这', '我', '你',
                 'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been',
                 'to', 'of', 'and', 'in', 'that', 'have', 'it', 'for'}
    
    # 分词（简化：按空格和标点）
    words = re.findall(r'[\w\u4e00-\u9fff]+', content.lower())
    
    # 过滤停用词
    keywords = [w for w in words if w not in stopwords and len(w) > 1]
    
    # 去重
    return list(set(keywords))[:20]  # 最多20个关键词


def main():
    parser = argparse.ArgumentParser(description="Knowledge Graph - Memory Relations")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # add命令
    add_parser = subparsers.add_parser("add", help="添加记忆节点")
    add_parser.add_argument("--id", required=True, help="记忆ID")
    add_parser.add_argument("--content", required=True, help="记忆内容")
    add_parser.add_argument("--type", default="other", help="记忆类型")
    
    # relate命令
    relate_parser = subparsers.add_parser("relate", help="发现关联")
    relate_parser.add_argument("--id", required=True, help="记忆ID")
    relate_parser.add_argument("--content", required=True, help="记忆内容")
    relate_parser.add_argument("--type", default="other", help="记忆类型")
    
    # query命令
    query_parser = subparsers.add_parser("query", help="查询关联记忆")
    query_parser.add_argument("--id", required=True, help="记忆ID")
    query_parser.add_argument("--depth", type=int, default=2, help="遍历深度")
    
    # path命令
    path_parser = subparsers.add_parser("path", help="查找记忆路径")
    path_parser.add_argument("--from", dest="source", required=True, help="起点ID")
    path_parser.add_argument("--to", dest="target", required=True, help="终点ID")
    
    # clusters命令
    subparsers.add_parser("clusters", help="发现记忆簇")
    
    # stats命令
    subparsers.add_parser("stats", help="查看统计")
    
    args = parser.parse_args()
    graph = KnowledgeGraph()
    
    if args.command == "add":
        keywords = extract_keywords(args.content)
        graph.add_node(args.id, args.content, args.type, keywords)
        
        # 自动发现关联
        relations = graph.discover_relations(args.id, args.content, keywords)
        for rel in relations:
            graph.add_edge(rel['source'], rel['target'], 
                          rel['type'], rel['weight'])
        
        graph.save()
        print(f"[OK] Added node {args.id} with {len(relations)} relations")
        
    elif args.command == "relate":
        keywords = extract_keywords(args.content)
        relations = graph.discover_relations(args.id, args.content, keywords)
        print(json.dumps(relations, ensure_ascii=False, indent=2))
        
    elif args.command == "query":
        related = graph.get_related_memories(args.id, args.depth)
        if related:
            for r in related:
                print(f"[{r['distance']}] {r['memory']['id']}: {r['memory']['content'][:50]}... ({r['relation']})")
        else:
            print("[EMPTY] No related memories found")
            
    elif args.command == "path":
        paths = graph.find_path(args.source, args.target)
        if paths:
            for i, path in enumerate(paths):
                print(f"Path {i+1}: {' -> '.join(path)}")
        else:
            print("[EMPTY] No path found")
            
    elif args.command == "clusters":
        clusters = graph.get_memory_clusters()
        if clusters:
            for i, cluster in enumerate(clusters):
                print(f"Cluster {i+1} (size={cluster['size']}): {cluster['members'][:5]}...")
        else:
            print("[EMPTY] No clusters found")
            
    elif args.command == "stats":
        stats = graph.get_node_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
