#!/usr/bin/env python3
"""
多Agent记忆系统 - 知识图谱构建脚本（通用版）

功能：
  从记忆文件中提取实体，构建知识图谱

作者：光光教授 (光光事务所)
版本：v1.0.0
许可证：MIT
"""

import os
import sys
import json
import re
from pathlib import Path
from datetime import datetime

# ============================================================
# 配置
# ============================================================

WORKSPACE = Path(os.environ.get("MEMORY_WORKSPACE", "/tmp/memory-workspace"))
MEMORY_DIR = WORKSPACE / "memory"
GRAPH_DIR = WORKSPACE / ".memory-graph"

# 实体提取配置
ENTITY_PATTERNS = {
    "agent": r'[Agent|用户|系统|服务|应用]',
    "project": r'v\d+\.\d+|PROJECT-[A-Z]+',
    "tech": r'Python|JavaScript|TypeScript|PostgreSQL|LanceDB|EmbeddingGemma',
    "date": r'\d{4}-\d{2}-\d{2}',
    "metric": r'\d+%|\d+\.\d+|\d+KB|\d+MB|\d+GB'
}

# ============================================================
# 图谱构建器
# ============================================================

class MemoryGraphBuilder:
    """记忆图谱构建器"""
    
    def __init__(self):
        self.graph_dir = GRAPH_DIR
        self.graph_dir.mkdir(parents=True, exist_ok=True)
        self.graph_file = self.graph_dir / "memory-graph.json"
        self.stats_file = self.graph_dir / "graph-stats.json"
        
        # 加载或创建图谱
        if self.graph_file.exists():
            with open(self.graph_file, "r", encoding="utf-8") as f:
                self.graph = json.load(f)
        else:
            self.graph = {
                "nodes": [],
                "edges": [],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "updated": datetime.now().isoformat(),
                    "version": "1.0"
                }
            }
    
    def extract_entities(self, text):
        """提取实体"""
        entities = {}
        
        for entity_type, pattern in ENTITY_PATTERNS.items():
            matches = re.findall(pattern, text)
            if matches:
                entities[entity_type] = list(set(matches))
        
        return entities
    
    def build_graph(self, memory_files=None):
        """构建图谱"""
        if memory_files is None:
            memory_files = list(MEMORY_DIR.glob("*.md"))
        
        print(f"[Graph] 构建图谱: {len(memory_files)}个文件")
        
        new_nodes = 0
        new_edges = 0
        
        for file_path in memory_files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                
                # 提取实体
                entities = self.extract_entities(content)
                
                # 添加节点
                for entity_type, entity_list in entities.items():
                    for entity in entity_list:
                        node_id = f"{entity_type}:{entity}"
                        if node_id not in [n["id"] for n in self.graph["nodes"]]:
                            self.graph["nodes"].append({
                                "id": node_id,
                                "type": entity_type,
                                "name": entity,
                                "file": str(file_path.name),
                                "created": datetime.now().isoformat()
                            })
                            new_nodes += 1
                
                # 添加边（实体共现关系）
                all_entities = []
                for entity_list in entities.values():
                    all_entities.extend(entity_list)
                
                for i in range(len(all_entities)):
                    for j in range(i + 1, len(all_entities)):
                        source_id = all_entities[i]
                        target_id = all_entities[j]
                        
                        edge = {
                            "source": source_id,
                            "target": target_id,
                            "type": "co-occurrence",
                            "file": str(file_path.name)
                        }
                        
                        # 检查边是否已存在
                        edge_exists = False
                        for existing_edge in self.graph["edges"]:
                            if (existing_edge["source"] == edge["source"] and 
                                existing_edge["target"] == edge["target"]):
                                edge_exists = True
                                break
                        
                        if not edge_exists:
                            self.graph["edges"].append(edge)
                            new_edges += 1
                
            except Exception as e:
                print(f"[ERROR] 处理文件失败 {file_path}: {e}", file=sys.stderr)
        
        # 更新元数据
        self.graph["metadata"]["updated"] = datetime.now().isoformat()
        self.graph["metadata"]["node_count"] = len(self.graph["nodes"])
        self.graph["metadata"]["edge_count"] = len(self.graph["edges"])
        
        # 保存图谱
        with open(self.graph_file, "w", encoding="utf-8") as f:
            json.dump(self.graph, f, ensure_ascii=False, indent=2)
        
        # 保存统计
        stats = {
            "total_files": len(memory_files),
            "new_nodes": new_nodes,
            "new_edges": new_edges,
            "total_nodes": len(self.graph["nodes"]),
            "total_edges": len(self.graph["edges"]),
            "timestamp": datetime.now().isoformat()
        }
        
        with open(self.stats_file, "w", encoding="utf-8") as f:
            json.dump(stats, f, ensure_ascii=False, indent=2)
        
        print(f"[Graph] 图谱构建完成:")
        print(f"  新增节点: {new_nodes}")
        print(f"  新增边: {new_edges}")
        print(f"  总节点: {len(self.graph['nodes'])}")
        print(f"  总边: {len(self.graph['edges'])}")
        
        return stats
    
    def query_graph(self, entity, max_depth=2):
        """BFS遍历图谱"""
        print(f"[Graph] 查询实体: {entity}")
        
        # BFS遍历
        visited = set()
        queue = [(entity, 0)]
        results = []
        
        while queue:
            current, depth = queue.pop(0)
            
            if current in visited or depth > max_depth:
                continue
            
            visited.add(current)
            results.append(current)
            
            # 查找邻居
            for edge in self.graph["edges"]:
                if edge["source"] == current and edge["target"] not in visited:
                    queue.append((edge["target"], depth + 1))
                elif edge["target"] == current and edge["source"] not in visited:
                    queue.append((edge["source"], depth + 1))
        
        return results
    
    def get_stats(self):
        """获取图谱统计"""
        if self.stats_file.exists():
            with open(self.stats_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}


# ============================================================
# 主函数
# ============================================================

def main():
    """主函数"""
    print("=" * 60)
    print("多Agent记忆系统 - 知识图谱构建测试")
    print("=" * 60)
    
    # 构建图谱
    print("\n[测试1] 构建图谱")
    builder = MemoryGraphBuilder()
    memory_files = list(MEMORY_DIR.glob("*.md"))[:10]
    stats = builder.build_graph(memory_files)
    print(f"  统计: {json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    # 查询图谱
    print("\n[测试2] 图谱查询")
    results = builder.query_graph("Agent", max_depth=2)
    print(f"  结果: {results}")
    
    print("\n✅ 知识图谱构建测试完成")


if __name__ == "__main__":
    main()
