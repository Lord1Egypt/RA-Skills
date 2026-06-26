#!/usr/bin/env python3
"""
Knowledge Graph Visualizer
重新生成 knowledge-graph.html，数据从 Knowledge Engine 读取

用法: python3 visualize.py
输出: ~/Desktop/knowledge-graph.html
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from concept_manager import get_db

DESKTOP = os.path.expanduser("~/Desktop")
OUTPUT = os.path.join(DESKTOP, "knowledge-graph.html")

def export_graph_data():
    conn = get_db()
    
    concepts = conn.execute(
        'SELECT id, concept, tags, confidence, status, context FROM concepts WHERE status="active" ORDER BY created_at'
    ).fetchall()
    
    links = conn.execute('''
        SELECT cl.from_concept, cl.to_concept, cl.relation,
               c1.concept as from_name, c2.concept as to_name
        FROM concept_links cl
        JOIN concepts c1 ON c1.id = cl.from_concept
        JOIN concepts c2 ON c2.id = cl.to_concept
    ''').fetchall()
    
    nodes = []
    for c in concepts:
        tags = json.loads(c['tags']) if isinstance(c['tags'], str) else c['tags']
        level = 'L3' if 'level:l3' in tags else ('L2' if 'level:l2' in tags else 'L1')
        clean_tags = [t for t in tags if not t.startswith('level:')]
        nodes.append({
            'id': c['id'],
            'label': c['concept'],
            'tags': clean_tags,
            'confidence': c['confidence'],
            'level': level,
            'context': (c['context'] or '')[:100]
        })
    
    edges = []
    for l in links:
        edges.append({
            'source': l['from_concept'],
            'target': l['to_concept'],
            'relation': l['relation']
        })
    
    conn.close()
    return {'nodes': nodes, 'edges': edges}


def generate_html(data):
    data_json = json.dumps(data, ensure_ascii=False, indent=2)
    
    # 读取模板（同目录的 template.html）或者内联
    template_path = os.path.join(os.path.dirname(__file__), "viz-template.html")
    if os.path.exists(template_path):
        with open(template_path, 'r', encoding='utf-8') as f:
            html = f.read()
        html = html.replace('GRAPH_DATA_PLACEHOLDER', data_json)
    else:
        # 使用桌面已有的文件作为模板
        existing = os.path.join(DESKTOP, "knowledge-graph.html")
        if os.path.exists(existing):
            with open(existing, 'r', encoding='utf-8') as f:
                html = f.read()
            # 替换数据
            import re
            html = re.sub(
                r'const DATA = \{.*?\};',
                f'const DATA = {data_json};',
                html,
                flags=re.DOTALL
            )
        else:
            print("❌ 找不到模板文件")
            return False
    
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 可视化已生成: {OUTPUT}")
    print(f"   节点: {len(data['nodes'])} | 关联: {len(data['edges'])}")
    return True


if __name__ == "__main__":
    data = export_graph_data()
    generate_html(data)
