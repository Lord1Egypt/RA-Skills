#!/usr/bin/env python3
"""
Knowledge Graph Builder for Memory System
从 MEMORY.md 和 memory/*.md 提取实体和关系，生成 NetworkX 图，导出为 HTML 可视化文件
"""

import os
import re
import json
import argparse
from datetime import datetime
from pathlib import Path
from collections import defaultdict

import networkx as nx
from pyvis.network import Network

# 实体类型定义
ENTITY_TYPES = {
    'model': ['qwen2.5:7b', 'phi-4-mini', 'all-MiniLM-L6-v2', 'nomic-embed-text'],
    'person': ['迹大人', '迹', 'Cyan'],
    'tool': ['iflow', 'ollama', 'memory_search', 'memory_watchdog'],
    'file': ['MEMORY.md', 'TOOLS.md', 'SOUL.md', 'USER.md'],
    'concept': ['记忆系统', '语义搜索', 'FAISS', '知识图谱', '冲突检测'],
    'skill': ['agent-browser', 'github-cli', 'notion-skill', 'pdf', 'memory-watchdog'],
    'status': ['✅', '❌', '⏳', '⚠️'],
}

# 关系类型定义
RELATION_PATTERNS = [
    (r'(.+?)\s*使用\s*(.+)', 'uses'),
    (r'(.+?)\s*依赖\s*(.+)', 'depends_on'),
    (r'(.+?)\s*包含\s*(.+)', 'contains'),
    (r'(.+?)\s*创建\s*(.+)', 'creates'),
    (r'(.+?)\s*安装\s*(.+)', 'installs'),
    (r'(.+?)\s*→\s*(.+)', 'leads_to'),
    (r'(.+?)\s*=\s*(.+)', 'equals'),
]


class MemoryKnowledgeGraph:
    """记忆系统知识图谱构建器"""
    
    def __init__(self, workspace_path: str):
        self.workspace_path = Path(workspace_path)
        self.graph = nx.DiGraph()
        self.entities = defaultdict(list)  # type -> [entities]
        self.relations = []  # [(source, relation, target, metadata)]
        
    def extract_entities(self, text: str) -> list:
        """从文本中提取实体"""
        found_entities = []
        
        for entity_type, patterns in ENTITY_TYPES.items():
            for pattern in patterns:
                if pattern.lower() in text.lower():
                    found_entities.append({
                        'name': pattern,
                        'type': entity_type,
                        'count': text.lower().count(pattern.lower())
                    })
        
        # 提取日期实体
        date_pattern = r'\d{4}-\d{2}-\d{2}'
        for match in re.finditer(date_pattern, text):
            found_entities.append({
                'name': match.group(),
                'type': 'date',
                'count': 1
            })
        
        # 提取时间戳
        time_pattern = r'\d{2}:\d{2}'
        for match in re.finditer(time_pattern, text):
            found_entities.append({
                'name': match.group(),
                'type': 'time',
                'count': 1
            })
        
        return found_entities
    
    def extract_relations(self, text: str, context: str = '') -> list:
        """从文本中提取关系"""
        relations = []
        lines = text.split('\n')
        
        for line in lines:
            # 提取任务完成关系
            if '✅' in line:
                task_match = re.search(r'✅\s*(.+?)(?:\s*-|$)', line)
                if task_match:
                    relations.append({
                        'source': 'memory_system',
                        'relation': 'completed',
                        'target': task_match.group(1).strip(),
                        'context': context
                    })
            
            # 提取待办关系
            if '⏳' in line or '[ ]' in line:
                task_match = re.search(r'(?:⏳|\[\s*\])\s*(.+?)(?:\s*-|$)', line)
                if task_match:
                    relations.append({
                        'source': 'memory_system',
                        'relation': 'pending',
                        'target': task_match.group(1).strip(),
                        'context': context
                    })
            
            # 提取警告关系
            if '⚠️' in line:
                warn_match = re.search(r'⚠️\s*(.+?)(?:\s*-|$)', line)
                if warn_match:
                    relations.append({
                        'source': 'memory_system',
                        'relation': 'warning',
                        'target': warn_match.group(1).strip(),
                        'context': context
                    })
            
            # 提取决策关系
            if '决定' in line or '决策' in line:
                relations.append({
                    'source': 'user',
                    'relation': 'decided',
                    'target': line.strip(),
                    'context': context
                })
        
        return relations
    
    def process_memory_file(self, file_path: Path) -> dict:
        """处理单个记忆文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        entities = self.extract_entities(content)
        relations = self.extract_relations(content, str(file_path.name))
        
        return {
            'file': str(file_path.name),
            'entities': entities,
            'relations': relations,
            'word_count': len(content.split()),
            'char_count': len(content)
        }
    
    def build_graph(self):
        """构建知识图谱"""
        # 处理 MEMORY.md
        memory_file = self.workspace_path / 'MEMORY.md'
        if memory_file.exists():
            data = self.process_memory_file(memory_file)
            self._add_to_graph(data, 'long_term')
        
        # 处理 memory/*.md
        memory_dir = self.workspace_path / 'memory'
        if memory_dir.exists():
            for md_file in memory_dir.glob('*.md'):
                data = self.process_memory_file(md_file)
                self._add_to_graph(data, 'daily')
        
        # 添加实体间的关系
        self._infer_relations()
        
        return self.graph
    
    def _add_to_graph(self, data: dict, memory_type: str):
        """将提取的数据添加到图中"""
        # 添加文件节点
        file_node = f"file:{data['file']}"
        self.graph.add_node(file_node, 
                           type='file',
                           label=data['file'],
                           memory_type=memory_type,
                           word_count=data['word_count'],
                           title=f"{data['file']}\n字数: {data['word_count']}")
        
        # 添加实体节点
        for entity in data['entities']:
            entity_id = f"{entity['type']}:{entity['name']}"
            
            if not self.graph.has_node(entity_id):
                self.graph.add_node(entity_id,
                                   type=entity['type'],
                                   label=entity['name'],
                                   count=entity['count'],
                                   title=f"{entity['type']}: {entity['name']}\n出现次数: {entity['count']}")
            
            # 添加文件-实体关系
            self.graph.add_edge(file_node, entity_id, 
                               relation='contains',
                               weight=entity['count'])
        
        # 添加关系边
        for rel in data['relations']:
            target_id = f"task:{rel['target'][:30]}"  # 截断长任务名
            if not self.graph.has_node(target_id):
                self.graph.add_node(target_id,
                                   type='task',
                                   label=rel['target'][:30],
                                   status=rel['relation'],
                                   title=rel['target'])
            
            self.graph.add_edge(file_node, target_id,
                               relation=rel['relation'])
    
    def _infer_relations(self):
        """推断实体间的隐式关系"""
        # 模型与工具关系
        model_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'model']
        tool_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'tool']
        
        for model in model_nodes:
            for tool in tool_nodes:
                if not self.graph.has_edge(model, tool):
                    self.graph.add_edge(model, tool, relation='uses', inferred=True)
        
        # 概念关系
        concept_nodes = [n for n, d in self.graph.nodes(data=True) if d.get('type') == 'concept']
        for i, c1 in enumerate(concept_nodes):
            for c2 in concept_nodes[i+1:]:
                self.graph.add_edge(c1, c2, relation='related', inferred=True)
    
    def export_html(self, output_path: str, height: str = '800px', width: str = '100%'):
        """导出为 HTML 可视化文件"""
        net = Network(height=height, width=width, directed=True, 
                     notebook=False, cdn_resources='in_line')
        
        # 设置颜色映射
        color_map = {
            'model': '#FF6B6B',
            'person': '#4ECDC4',
            'tool': '#45B7D1',
            'file': '#96CEB4',
            'concept': '#FFEAA7',
            'skill': '#DDA0DD',
            'task': '#98D8C8',
            'date': '#F7DC6F',
            'time': '#BB8FCE',
            'status': '#E8E8E8'
        }
        
        # 添加节点
        for node, data in self.graph.nodes(data=True):
            node_type = data.get('type', 'unknown')
            color = color_map.get(node_type, '#CCCCCC')
            
            net.add_node(node,
                        label=data.get('label', node),
                        title=data.get('title', node),
                        color=color,
                        size=20 if node_type in ['model', 'person', 'concept'] else 15)
        
        # 添加边
        for source, target, data in self.graph.edges(data=True):
            relation = data.get('relation', 'related')
            color = '#FF6B6B' if relation in ['completed'] else '#45B7D1'
            
            net.add_edge(source, target,
                        title=relation,
                        color=color,
                        arrows='to')
        
        # 设置物理布局
        net.set_options("""
        {
            "physics": {
                "hierarchicalRepulsion": {
                    "centralGravity": 0.0,
                    "springLength": 200,
                    "springConstant": 0.01,
                    "nodeDistance": 200,
                    "damping": 0.09
                },
                "minVelocity": 0.75,
                "solver": "hierarchicalRepulsion"
            },
            "configure": {
                "enabled": true,
                "filter": "physics"
            }
        }
        """)
        
        net.save_graph(output_path)
        return output_path
    
    def export_stats(self) -> dict:
        """导出图谱统计信息"""
        return {
            'node_count': self.graph.number_of_nodes(),
            'edge_count': self.graph.number_of_edges(),
            'node_types': dict(nx.get_node_attributes(self.graph, 'type')),
            'density': nx.density(self.graph),
            'is_connected': nx.is_weakly_connected(self.graph) if self.graph.number_of_nodes() > 0 else False,
            'generated_at': datetime.now().isoformat()
        }


def main():
    parser = argparse.ArgumentParser(description='构建记忆系统知识图谱')
    parser.add_argument('--workspace', '-w', 
                       default='/home/claw/.openclaw/workspace',
                       help='工作空间路径')
    parser.add_argument('--output', '-o',
                       default='memory/knowledge_graph.html',
                       help='输出HTML文件路径')
    parser.add_argument('--stats', '-s',
                       default='memory/state/knowledge_graph_stats.json',
                       help='统计信息输出路径')
    
    args = parser.parse_args()
    
    print("🔍 开始构建知识图谱...")
    
    builder = MemoryKnowledgeGraph(args.workspace)
    graph = builder.build_graph()
    
    # 导出HTML
    output_path = Path(args.workspace) / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    html_path = builder.export_html(str(output_path))
    
    # 导出统计
    stats = builder.export_stats()
    stats_path = Path(args.workspace) / args.stats
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with open(stats_path, 'w', encoding='utf-8') as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 知识图谱已生成: {html_path}")
    print(f"📊 节点数: {stats['node_count']}, 边数: {stats['edge_count']}")
    print(f"📈 图密度: {stats['density']:.4f}")
    
    return stats


if __name__ == '__main__':
    main()
